#!/usr/bin/env python3
"""Audita materiais comerciais sem imprimir possíveis segredos.

Uso:
    python3 auditar_materiais_comerciais.py /caminho/do/projeto

Retorna 0 quando não há falhas bloqueantes e 1 quando encontra
arquivo sensível, chave privada ou padrão forte de credencial.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

IGNORAR = {".git", "__pycache__", ".pytest_cache", ".mypy_cache"}
TEXTOS = {".md", ".py", ".svg", ".txt", ".json", ".yaml", ".yml", ".html", ".css", ".csv"}
SENSIVEIS = {".env", ".pem", ".key", ".p12", ".pfx", ".jks", ".keystore"}
PADROES = {
    "chave privada": re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
    "segredo atribuído": re.compile(
        r"(?im)^\s*(?:api[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret|password|senha)\s*[:=]\s*[\"']?(?!\[?REDACTED\]?|EXEMPLO|<)[A-Za-z0-9_./+\-=]{12,}"
    ),
    "token conhecido": re.compile(r"\b(?:sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{30,}|hf_[A-Za-z0-9]{24,})\b"),
}
ESPANHOL = re.compile(
    r"(?i)\b(?:usted|ustedes|entonces|preguntas|respuestas|mantenimiento|creación|configuración|puede|pueden|nuestro|nuestra)\b"
)


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: auditar_materiais_comerciais.py DIRETORIO")
        return 2
    raiz = Path(sys.argv[1]).expanduser().resolve()
    if not raiz.is_dir():
        print("FALHA | diretório inexistente")
        return 2

    falhas: list[tuple[str, str]] = []
    alertas: list[tuple[str, str]] = []
    total = 0
    for arquivo in raiz.rglob("*"):
        if not arquivo.is_file() or any(p in IGNORAR for p in arquivo.parts):
            continue
        total += 1
        rel = arquivo.relative_to(raiz).as_posix()
        if arquivo.suffix.lower() in SENSIVEIS or arquivo.name.lower() in {"id_rsa", "id_ed25519", ".netrc"}:
            falhas.append(("arquivo potencialmente sensível", rel))
            continue
        if arquivo.suffix.lower() not in TEXTOS:
            continue
        texto = arquivo.read_text(encoding="utf-8", errors="ignore")
        for categoria, padrao in PADROES.items():
            if padrao.search(texto):
                falhas.append((categoria, rel))
        if arquivo.name != Path(__file__).name and ESPANHOL.search(texto):
            alertas.append(("possível termo em espanhol", rel))

    falhas = list(dict.fromkeys(falhas))
    alertas = list(dict.fromkeys(alertas))
    print(f"Arquivos examinados: {total}")
    print(f"Falhas bloqueantes: {len(falhas)}")
    print(f"Alertas para revisão: {len(alertas)}")
    for categoria, rel in falhas:
        print(f"FALHA | {categoria} | {rel}")
    for categoria, rel in alertas:
        print(f"ALERTA | {categoria} | {rel}")
    if falhas:
        print("RESULTADO: FALHA")
        return 1
    print("RESULTADO: APROVADO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
