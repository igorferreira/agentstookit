#!/usr/bin/env python3
"""Decodificação de NFC-e (Nota Fiscal de Consumidor Eletrônica) a partir de foto.

Pipeline: QR Code -> validação da chave de acesso (dígito verificador,
módulo 11) -> consulta ao portal público da SEFAZ (via URL embutida no
próprio QR) -> parsing dos itens -> fallback de OCR do cabeçalho quando a
consulta estruturada falha.

Uso:
    python3 decodificar_nfce.py /caminho/foto.jpg
    python3 decodificar_nfce.py /caminho/foto.jpg --output resultado.json -v

Saída (JSON): ver `ResultadoExtracao.to_dict()`.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import cv2
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

LOG = logging.getLogger("decodificar_nfce")

# --------------------------------------------------------------------------
# Constantes
# --------------------------------------------------------------------------

CHAVE_ACESSO_REGEX = re.compile(r"(?<!\d)\d{44}(?!\d)")
VALOR_REGEX = re.compile(r"\d{1,3}(?:\.\d{3})*,\d{2}|\d+\.\d{2}")
DATA_REGEX = re.compile(r"(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{4})")

# Primeiros 2 dígitos da chave de acesso = código IBGE da UF emissora.
CODIGO_UF = {
    "11": "RO", "12": "AC", "13": "AM", "14": "RR", "15": "PA", "16": "AP",
    "17": "TO", "21": "MA", "22": "PI", "23": "CE", "24": "RN", "25": "PB",
    "26": "PE", "27": "AL", "28": "SE", "29": "BA", "31": "MG", "32": "ES",
    "33": "RJ", "35": "SP", "41": "PR", "42": "SC", "43": "RS", "50": "MS",
    "51": "MT", "52": "GO", "53": "DF",
}

# Fallback: usado só quando o QR não traz a URL completa (raro — o QR de
# NFC-e normalmente já embute o link pronto de consulta). Cobertura parcial
# e sujeita a mudança pelos governos estaduais; não confiar cegamente.
URL_CONSULTA_POR_UF = {
    # URL oficial vigente desde 19/12/2023; o endereço www4 é legado.
    "RJ": "https://consultadfe.fazenda.rj.gov.br/consultaNFCe/QRCode",
    "SP": "https://www.nfce.fazenda.sp.gov.br/qrcode",
    "MG": "https://portalsped.fazenda.mg.gov.br/portalnfce/sistema/qrcode.xhtml",
}

USER_AGENT = (
    "Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120 Mobile Safari/537.36"
)

TIMEOUT_PADRAO = 15
TENTATIVAS_PADRAO = 3


# --------------------------------------------------------------------------
# Modelos de dados
# --------------------------------------------------------------------------

class FonteExtracao(str, Enum):
    SEFAZ = "sefaz"
    OCR_PARCIAL = "ocr_parcial"
    FALHA = "falha"


@dataclass
class ItemNota:
    descricao: str
    quantidade: float
    unidade: str
    valor_unitario: float
    valor_total: float


@dataclass
class ResultadoExtracao:
    fonte: FonteExtracao
    chave_nfce: Optional[str] = None
    uf: Optional[str] = None
    mercado: Optional[str] = None
    data: Optional[str] = None
    valor_total: Optional[float] = None
    itens: list[ItemNota] = field(default_factory=list)
    erro: Optional[str] = None

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["fonte"] = self.fonte.value
        return payload


# --------------------------------------------------------------------------
# Exceções
# --------------------------------------------------------------------------

class NFCeError(Exception):
    """Erro base do pipeline de decodificação de NFC-e."""


class QRCodeNaoDetectadoError(NFCeError):
    pass


class ChaveAcessoInvalidaError(NFCeError):
    pass


class ConsultaSefazError(NFCeError):
    pass


# --------------------------------------------------------------------------
# Validação da chave de acesso (dígito verificador, módulo 11)
# --------------------------------------------------------------------------

def validar_digito_verificador(chave: str) -> bool:
    """Valida o DV (44º dígito) da chave de acesso via módulo 11.

    Referência: Manual de Orientação do Contribuinte (MOC) da NF-e/NFC-e.
    Rejeitar aqui uma chave malformada evita gastar uma requisição de rede
    (e potencialmente vazar dados) numa chave que o próprio QR corrompeu.
    """
    if len(chave) != 44 or not chave.isdigit():
        return False

    corpo, dv_informado = chave[:43], int(chave[43])
    pesos = (2, 3, 4, 5, 6, 7, 8, 9)
    soma = sum(int(digito) * pesos[i % len(pesos)] for i, digito in enumerate(reversed(corpo)))
    resto = soma % 11
    dv_calculado = 0 if resto in (0, 1) else 11 - resto

    return dv_calculado == dv_informado


def identificar_uf(chave: str) -> Optional[str]:
    """Extrai a UF emissora a partir dos 2 primeiros dígitos da chave."""
    return CODIGO_UF.get(chave[:2])


# --------------------------------------------------------------------------
# QR Code
# --------------------------------------------------------------------------

class QRCodeDecoder:
    """Decodifica QR codes de imagens usando OpenCV (sem dependências extras)."""

    def __init__(self) -> None:
        self._detector = cv2.QRCodeDetector()

    def decodificar(self, imagem_path: Path) -> str:
        img = cv2.imread(str(imagem_path))
        if img is None:
            raise QRCodeNaoDetectadoError(f"Não foi possível ler a imagem: {imagem_path}")

        texto, _, _ = self._detector.detectAndDecode(img)
        if texto:
            return texto

        # Fotos de celular costumam ter o QR pequeno/distante; upscaling 2x
        # com interpolação cúbica recupera boa parte desses casos.
        altura, largura = img.shape[:2]
        img_grande = cv2.resize(img, (largura * 2, altura * 2), interpolation=cv2.INTER_CUBIC)
        texto, _, _ = self._detector.detectAndDecode(img_grande)
        if texto:
            return texto

        raise QRCodeNaoDetectadoError("QR code não encontrado na imagem (mesmo após upscaling)")


def extrair_url_e_chave(texto_qr: str) -> tuple[Optional[str], str]:
    """Extrai a URL completa (se houver) e a chave de acesso do payload do QR."""
    match_chave = CHAVE_ACESSO_REGEX.search(texto_qr)
    if not match_chave:
        raise ChaveAcessoInvalidaError(
            f"Não encontrei uma chave de acesso de 44 dígitos no payload do QR: {texto_qr[:120]!r}"
        )

    chave = match_chave.group(0)
    if not validar_digito_verificador(chave):
        raise ChaveAcessoInvalidaError(f"Chave de acesso com dígito verificador inválido: {chave}")

    url = texto_qr if texto_qr.startswith("http") else None
    return url, chave


# --------------------------------------------------------------------------
# Cliente SEFAZ
# --------------------------------------------------------------------------

def _sessao_http(tentativas: int) -> requests.Session:
    sessao = requests.Session()
    retry = Retry(
        total=tentativas,
        backoff_factor=0.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
    )
    adaptador = HTTPAdapter(max_retries=retry)
    sessao.mount("https://", adaptador)
    sessao.mount("http://", adaptador)
    sessao.headers.update({"User-Agent": USER_AGENT})
    return sessao


class SefazClient:
    """Consulta o portal público da SEFAZ para obter os itens de uma NFC-e."""

    def __init__(self, timeout: int = TIMEOUT_PADRAO, tentativas: int = TENTATIVAS_PADRAO) -> None:
        self._sessao = _sessao_http(tentativas)
        self._timeout = timeout

    def consultar(self, chave: str, url_qr: Optional[str]) -> ResultadoExtracao:
        uf = identificar_uf(chave)
        url = url_qr or URL_CONSULTA_POR_UF.get(uf) if uf else url_qr

        if not url:
            raise ConsultaSefazError(
                f"Sem URL de consulta disponível (QR sem link e UF '{uf}' sem fallback conhecido)"
            )

        self._validar_dominio_gov_br(url)

        LOG.debug("Consultando SEFAZ (UF=%s): %s", uf, url)
        try:
            resposta = self._sessao.get(url, timeout=self._timeout)
            resposta.raise_for_status()
        except requests.RequestException as exc:
            raise ConsultaSefazError(f"Falha HTTP na consulta à SEFAZ: {exc}") from exc

        itens, mercado, data, valor_total = self._parsear_html(resposta.text)
        if not itens:
            raise ConsultaSefazError("Portal respondeu, mas não consegui extrair itens da página")

        return ResultadoExtracao(
            fonte=FonteExtracao.SEFAZ,
            chave_nfce=chave,
            uf=uf,
            mercado=mercado,
            data=data,
            valor_total=valor_total,
            itens=itens,
        )

    @staticmethod
    def _validar_dominio_gov_br(url: str) -> None:
        host = urlparse(url).netloc
        if not host.endswith(".gov.br"):
            raise ConsultaSefazError(f"URL fora do domínio .gov.br, recusando por segurança: {url}")

    @staticmethod
    def _parsear_html(html: str) -> tuple[list[ItemNota], Optional[str], Optional[str], Optional[float]]:
        """Extração best-effort dos itens/cabeçalho.

        O layout HTML varia por estado — cada SEFAZ mantém seu próprio portal
        de consulta pública, sem padrão nacional único. A estratégia aqui é
        genérica (varre qualquer <table> da página); funciona bem contra os
        portais que usam tabela simples de itens, mas pode precisar de um
        seletor dedicado por UF se o formato usar componentes JS dinâmicos.
        """
        soup = BeautifulSoup(html, "html.parser")
        # Parser dedicado ao layout clássico da SEFAZ-RJ. Os seletores foram
        # usados publicamente para exportar a tabela #tabResult para CSV.
        itens = SefazClient._parsear_dom_rj(soup)
        if not itens:
            itens = SefazClient._parsear_tabela_generica(soup)
        if not itens:
            itens = SefazClient._parsear_cartoes_itens(soup)
        mercado = SefazClient._extrair_mercado(soup)
        data = SefazClient._extrair_data(soup)
        valor_total = SefazClient._extrair_valor_total(soup)
        return itens, mercado, data, valor_total

    @staticmethod
    def _parsear_dom_rj(soup: BeautifulSoup) -> list[ItemNota]:
        """Extrai itens do layout tabular clássico do portal da SEFAZ-RJ."""
        itens: list[ItemNota] = []
        for linha in soup.select("#tabResult > tbody > tr"):
            descricao_el = linha.select_one(".txtTit")
            quantidade_el = linha.select_one(".Rqtd")
            unidade_el = linha.select_one(".RUN")
            unitario_el = linha.select_one(".RvlUnit")
            total_el = linha.select_one(".valor")
            if not all((descricao_el, quantidade_el, unidade_el, unitario_el, total_el)):
                continue

            quantidade = _parse_numero_localizado(
                re.sub(r"^\s*Qtde\.?:?\s*", "", quantidade_el.get_text(" ", strip=True), flags=re.IGNORECASE)
            )
            unitario = _parse_numero_localizado(
                unitario_el.get_text(" ", strip=True).replace("Vl. Unit.:", "", 1).strip()
            )
            total = _parse_numero_localizado(total_el.get_text(" ", strip=True))
            if quantidade is None or unitario is None or total is None:
                continue

            unidade = re.sub(
                r"^\s*UN\s*:\s*", "", unidade_el.get_text(" ", strip=True), flags=re.IGNORECASE
            ).strip()
            itens.append(
                ItemNota(
                    descricao=descricao_el.get_text(" ", strip=True),
                    quantidade=quantidade,
                    unidade=unidade.upper() or "UN",
                    valor_unitario=unitario,
                    valor_total=total,
                )
            )
        return itens

    @staticmethod
    def _parsear_tabela_generica(soup: BeautifulSoup) -> list[ItemNota]:
        itens: list[ItemNota] = []
        for tabela in soup.find_all("table"):
            for linha in tabela.find_all("tr"):
                celulas = linha.find_all("td")
                if len(celulas) < 3:
                    continue

                textos = [c.get_text(strip=True) for c in celulas]
                descricao = textos[0]
                if not descricao or descricao.lower() in {"item", "descrição", "descricao", "total"}:
                    continue

                valores = [v for v in (_parse_valor_brl(t) for t in textos[1:]) if v is not None]
                if not valores:
                    continue

                valor_unitario = valores[-2] if len(valores) >= 2 else valores[-1]
                valor_total_item = valores[-1]

                itens.append(
                    ItemNota(
                        descricao=descricao,
                        quantidade=1.0,
                        unidade="UN",
                        valor_unitario=valor_unitario,
                        valor_total=valor_total_item,
                    )
                )
        return itens

    @staticmethod
    def _parsear_cartoes_itens(soup: BeautifulSoup) -> list[ItemNota]:
        """Extrai os cartões da consulta simplificada atual da SEFAZ-RJ."""
        rotulos = ("qtde", "un:", "vl. unit", "vl. total")
        candidatos = []
        for elemento in soup.find_all(("article", "li", "div", "section")):
            texto = " ".join(elemento.get_text(" ", strip=True).split())
            if all(rotulo in texto.lower() for rotulo in rotulos):
                candidatos.append((elemento, texto))

        elementos_candidatos = {id(elemento) for elemento, _ in candidatos}
        itens: list[ItemNota] = []
        for elemento, texto in candidatos:
            if elemento.find(
                lambda filho: filho is not elemento and id(filho) in elementos_candidatos
            ):
                continue
            item = SefazClient._parsear_cartao_item(texto)
            if item is not None:
                itens.append(item)
        return itens

    @staticmethod
    def _parsear_cartao_item(texto: str) -> Optional[ItemNota]:
        compacto = " ".join(texto.split())
        padrao = re.compile(
            r"^(?P<descricao>.+?)\s+Qtde\.?\s*:\s*(?P<quantidade>[\d.,]+)"
            r"\s+UN\s*:\s*(?P<unidade>[A-Za-z0-9²³]+)"
            r"\s+Vl\.\s*Unit\.?\s*:\s*R?\$?\s*(?P<unit>[\d.,]+)"
            r"\s+Vl\.\s*Total\s*:?\s*R?\$?\s*(?P<total>[\d.,]+)",
            re.IGNORECASE,
        )
        match = padrao.search(compacto)
        if not match:
            return None
        quantidade = _parse_numero_localizado(match.group("quantidade"))
        unitario = _parse_numero_localizado(match.group("unit"))
        total = _parse_numero_localizado(match.group("total"))
        if quantidade is None or unitario is None or total is None:
            return None
        descricao = match.group("descricao").strip(" -:;")
        if not descricao:
            return None
        return ItemNota(
            descricao=descricao,
            quantidade=quantidade,
            unidade=match.group("unidade").upper(),
            valor_unitario=unitario,
            valor_total=total,
        )

    @staticmethod
    def _extrair_mercado(soup: BeautifulSoup) -> Optional[str]:
        for seletor in ("[class*=emitente]", "[class*=fornecedor]", "h1", "h2"):
            el = soup.select_one(seletor)
            if el and el.get_text(strip=True):
                return el.get_text(strip=True)
        return None

    @staticmethod
    def _extrair_data(soup: BeautifulSoup) -> Optional[str]:
        match = DATA_REGEX.search(soup.get_text())
        if not match:
            return None
        dia, mes, ano = match.groups()
        return f"{ano}-{mes.zfill(2)}-{dia.zfill(2)}"

    @staticmethod
    def _extrair_valor_total(soup: BeautifulSoup) -> Optional[float]:
        for texto_node in soup.find_all(string=re.compile(r"valor\s*total", re.IGNORECASE)):
            pai = texto_node.find_parent()
            if pai:
                trecho = pai.get_text(" ", strip=True)
                match = re.search(
                    r"valor\s*total[^\d]*(?P<valor>[\d.]+(?:,[\d]{2})?|[\d]+(?:\.[\d]{2})?)",
                    trecho,
                    re.IGNORECASE,
                )
                valor = _parse_numero_localizado(match.group("valor")) if match else None
                if valor is not None:
                    return valor
        return None


def _parse_valor_brl(texto: str) -> Optional[float]:
    match = VALOR_REGEX.search(texto)
    if not match:
        return None
    bruto = match.group(0)
    if "," in bruto:
        bruto = bruto.replace(".", "").replace(",", ".")
    try:
        return float(bruto)
    except ValueError:
        return None


def _parse_numero_localizado(texto: str) -> Optional[float]:
    """Converte 1.234,56/1234.56/98 sem depender do locale."""
    bruto = texto.strip().replace("R$", "").replace(" ", "")
    if not bruto:
        return None
    if "," in bruto:
        bruto = bruto.replace(".", "").replace(",", ".")
    elif bruto.count(".") > 1:
        bruto = bruto.replace(".", "")
    try:
        return float(bruto)
    except ValueError:
        return None


# --------------------------------------------------------------------------
# OCR fallback
# --------------------------------------------------------------------------

class OCRExtractor:
    """Fallback via OCR (tesseract) quando a consulta à SEFAZ falha."""

    def __init__(self, timeout: int = 15) -> None:
        self._timeout = timeout

    def extrair_cabecalho(self, imagem_path: Path) -> ResultadoExtracao:
        try:
            texto = self._rodar_tesseract(imagem_path)
        except FileNotFoundError:
            return ResultadoExtracao(
                fonte=FonteExtracao.FALHA,
                erro="tesseract não instalado (apt install tesseract-ocr)",
            )
        except subprocess.TimeoutExpired:
            return ResultadoExtracao(fonte=FonteExtracao.FALHA, erro="OCR excedeu o timeout")

        return ResultadoExtracao(
            fonte=FonteExtracao.OCR_PARCIAL,
            mercado=self._extrair_mercado(texto),
            data=self._extrair_data(texto),
            valor_total=self._extrair_valor(texto),
        )

    def _rodar_tesseract(self, imagem_path: Path) -> str:
        resultado = subprocess.run(
            ["tesseract", str(imagem_path), "stdout", "-l", "por+eng", "--psm", "4"],
            capture_output=True,
            text=True,
            timeout=self._timeout,
            check=False,
        )
        return resultado.stdout

    @staticmethod
    def _extrair_valor(texto: str) -> Optional[float]:
        candidatos = VALOR_REGEX.findall(texto)
        valores = [v for v in (_parse_valor_brl(c) for c in candidatos) if v is not None]
        # Heurística: o maior valor impresso num cupom costuma ser o total.
        return max(valores) if valores else None

    @staticmethod
    def _extrair_data(texto: str) -> Optional[str]:
        match = DATA_REGEX.search(texto)
        if not match:
            return None
        dia, mes, ano = match.groups()
        return f"{ano}-{mes.zfill(2)}-{dia.zfill(2)}"

    @staticmethod
    def _extrair_mercado(texto: str) -> Optional[str]:
        for linha in texto.splitlines()[:5]:
            linha = linha.strip()
            if len(linha) >= 4 and linha.upper() == linha and any(c.isalpha() for c in linha):
                return linha
        return None


# --------------------------------------------------------------------------
# Orquestração
# --------------------------------------------------------------------------

class ProcessadorNotaFiscal:
    """Ponto único de entrada do pipeline: QR -> SEFAZ -> OCR fallback."""

    def __init__(
        self,
        timeout: int = TIMEOUT_PADRAO,
        tentativas: int = TENTATIVAS_PADRAO,
        usar_ocr_fallback: bool = True,
    ) -> None:
        self._qr = QRCodeDecoder()
        self._sefaz = SefazClient(timeout=timeout, tentativas=tentativas)
        self._ocr = OCRExtractor()
        self._usar_ocr_fallback = usar_ocr_fallback

    def processar(self, imagem_path: Path) -> ResultadoExtracao:
        if not imagem_path.exists():
            return ResultadoExtracao(fonte=FonteExtracao.FALHA, erro=f"Arquivo não encontrado: {imagem_path}")

        try:
            texto_qr = self._qr.decodificar(imagem_path)
            LOG.info("QR code detectado")
        except QRCodeNaoDetectadoError as e:
            LOG.warning("%s", e)
            return self._fallback_ocr(imagem_path, motivo=str(e))

        try:
            url, chave = extrair_url_e_chave(texto_qr)
            LOG.info("Chave de acesso validada: %s (UF=%s)", chave, identificar_uf(chave))
        except ChaveAcessoInvalidaError as e:
            LOG.warning("%s", e)
            return self._fallback_ocr(imagem_path, motivo=str(e))

        try:
            resultado = self._sefaz.consultar(chave, url)
            LOG.info("%d itens extraídos da SEFAZ", len(resultado.itens))
            return resultado
        except ConsultaSefazError as e:
            LOG.warning("Consulta à SEFAZ falhou: %s", e)
            resultado_ocr = self._fallback_ocr(imagem_path, motivo=str(e))
            resultado_ocr.chave_nfce = chave
            resultado_ocr.uf = identificar_uf(chave)
            return resultado_ocr

    def _fallback_ocr(self, imagem_path: Path, motivo: str) -> ResultadoExtracao:
        if not self._usar_ocr_fallback:
            return ResultadoExtracao(fonte=FonteExtracao.FALHA, erro=motivo)
        LOG.info("Caindo para OCR fallback (%s)", motivo)
        return self._ocr.extrair_cabecalho(imagem_path)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def _configurar_logging(verbose: bool) -> None:
    nivel = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=nivel, format="%(levelname)s %(message)s", stream=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(description="Decodificar NFC-e a partir de foto de nota fiscal")
    parser.add_argument("imagem", type=Path, help="Caminho da foto da nota fiscal")
    parser.add_argument("--output", type=Path, help="Arquivo de saída JSON (default: stdout)")
    parser.add_argument("--timeout", type=int, default=TIMEOUT_PADRAO, help="Timeout de rede em segundos")
    parser.add_argument("--tentativas", type=int, default=TENTATIVAS_PADRAO, help="Tentativas de retry na SEFAZ")
    parser.add_argument("--no-ocr-fallback", action="store_true", help="Desativa o fallback de OCR")
    parser.add_argument("-v", "--verbose", action="store_true", help="Log detalhado (debug)")

    args = parser.parse_args()
    _configurar_logging(args.verbose)

    processador = ProcessadorNotaFiscal(
        timeout=args.timeout,
        tentativas=args.tentativas,
        usar_ocr_fallback=not args.no_ocr_fallback,
    )
    resultado = processador.processar(args.imagem)
    saida = json.dumps(resultado.to_dict(), ensure_ascii=False, indent=2)

    if args.output:
        args.output.write_text(saida, encoding="utf-8")
        LOG.info("Resultado salvo em: %s", args.output)
    else:
        print(saida)

    return 0 if resultado.fonte != FonteExtracao.FALHA else 1


if __name__ == "__main__":
    sys.exit(main())
