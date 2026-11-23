---
name: estilo-diogo-juridico
description: "Petições do caso Maricá — padrão forense Dr. Diogo."
version: 1.0.0
---

# Estilo Diogo Jurídico

Padrão canônico de formatação para TODAS as versões das petições do processo Maricá (exceção de pré-executividade). Fonte da verdade visual: PDF da versão 6 de 01/09/2026 (Dr. Diogo Simas, renderizado pelo Google Docs).

## Configuração da página (medidas REAIS da V6)

| Item | Valor |
|---|---|
| Página | **A4** (21 × 29,7 cm), retrato |
| Margem superior | 2,9 cm (82 pts) |
| Margem esquerda | 2,54 cm (72 pts = 1") |
| Margem direita | 2,57 cm |
| Margem inferior | 2,78 cm |
| Recuo 1ª linha | ~1 cm (28 pts) |
| Fonte | **Arial** (normal + negrito) — NÃO Times New Roman |
| Cor | **Preto puro `#000000` no branco — SEM CORES, SEM highlight, SEM shading** |
| Espaçamento entre linhas | 1,5 |
| Alinhamento | Corpo justificado; títulos centralizados |

> 📌 Medidas reais medidas do PDF da V6 (Google Docs). Preferir estes valores aos "ABNT teóricos" — fidelidade ao estilo Diogo é a prioridade.

## Estrutura obrigatória (ordem)

1. Endereçamento em CAIXA ALTA (`EXCELENTÍSSIMO SENHOR DOUTOR JUIZ...`).
2. `Processo nº 0040223-62.2021.8.19.0031`.
3. Preâmbulo/qualificação do peticionante (parágrafo contínuo).
4. Título da peça em CAIXA ALTA.
5. `pelos fundamentos a seguir expostos.`
6. Tese em seções `I.` a `XI.` (romano, caixa alta, negrito).
7. Pedidos numerados `1.` a `12.` (ou quantos forem).
8. Fechamento: `Termos em que,` / `Pede deferimento.` / local e data / assinaturas.

## Formatação de parágrafos

- Recuo de primeira linha **1,25 cm** no corpo.
- Espaçamento 1,5 em tudo.
- Sem cor em nenhuma run.

## Blocos de dados (campos)

Formato `campo: valor;` — **um campo por linha**, recuado.
Bloqueios: Itaú, Nubank (3814619-1), C6 (59310-9).

## Listas numeradas (pedidos)

Itens `1.`–`12.` recuados; cada um termina com `;`, último com `.`.

## Checklist de conformidade

- [ ] A4 retrato; margens sup3/esq3/dir2/inf2.
- [ ] Arial, 11–12pt.
- [ ] Sem cor (`w:color`, `w:highlight`, `w:shd` ausentes no DOCX).
- [ ] Espaçamento 1,5.
- [ ] Títulos romanos `I.`–`XI.` negrito caixa alta.
- [ ] Recuo 1ª linha 1,25 cm.
- [ ] Pedidos numerados recuados.
- [ ] Rodapé com número de página centralizado.

## Nomenclatura de arquivos

Todas as versões seguem: `TIPO_VERSAO_DESCRICAO.ext`
Ex.: `PETICAO_V7_EXCECAO_PRE_EXECUTIVIDADE.pdf`
UPPER_SNAKE_CASE, sem acentos, sem espaços, extensão minúscula, versão preservada (V1..Vn).

## ⚫ NEGRITOS E ESPAÇAMENTOS (OBRIGATÓRIO — estilo Diogo/V6)

Reproduzir EXATAMENTE os negritos e espaços da V6 canônica (fontes de verdade: `CATALOGO_NEGRITOS_ESPACAMENTOS_DIOGO.md` no MEGA e a V6 PDF).

### Espaçamentos (primeira página) — regras EXATAS da V6 original (18 pág)
Linha normal = 21 pts; bloco extra ≈ 30 pts por linha vazia.
- **Endereçamento** → ~123 pts (≈ 4–5 linhas vazias) → **Processo nº**
- **Processo nº** → ~61 pts (≈ 2–3 linhas vazias) → **preâmbulo**
- **Preâmbulo** → ~61 pts → **título da peça**
- **Título da peça** → ~62 pts → **"pelos fundamentos a seguir expostos."**
- **"pelos fundamentos"** → ~61 pts → **I. O QUE EXIGE APRECIAÇÃO IMEDIATA**
- **Seções do corpo** (`II.` em diante): separadas por ~1–2 linhas vazias.

Regra no DOCX: 3–4 parágrafos vazios entre blocos da 1ª página; 1–2 entre seções do corpo; nunca colar.

### Espaçamentos (corpo / outras páginas)
- Entre linhas: 1,5 (gap 21 pts); entre parágrafos: 1 linha vazia (~30 pts).
- Listas numeradas: recuo do item, itens em linha normal.
- Títulos de seção: caixa alta + negrito + 1 linha vazia antes do parágrafo.
- Margens: esq 2,54 / dir 2,57 / topo ~2,55 cm.

### Negritos essenciais (primeira página)
- **Endereçamento** (caixa alta), **Processo nº**, **título da peça** → negrito.
- **IGOR DOS SANTOS FERREIRA** e **MUNICÍPIO DE MARICÁ** (no preâmbulo) → negrito.
- "pelos fundamentos a seguir expostos." → normal.

### Negritos no corpo da tese
- **Datas-marcos**: "21 de setembro de 2007:", "2017 e 2019:", "27 de agosto de 2026:", "29 de agosto de 2026:" → negrito.
- **Nomes dos sócios**: Marcio dos Santos Carrinho, Denilson Passos de Brito → negrito.
- **Nº do processo (0040223-62.2021.8.19.0031)** e **CPF (XXX.XXX.XXX-XX)** → negrito.
- **Valores R$** ("R$ 5.730,64", "R$ 12,15") → negrito.
- **Citações da decisão** ("reiteração automática da ordem de bloqueio por 30 dias") e **pergunta-chave** ("Pode o patrimônio pessoal de Igor responder...?") → negrito.
- **Títulos de seção** `I.`–`XI.` → caixa alta + negrito.

### Regra genérica
- Nomes próprios relevantes, datas-marcos, CPF, nº processo, valores, citações/destaques → negrito.
- Parágrafos de fundamentação → NORMAL.
- Fonte Arial + preto, sem cores, A4, espaçamento 1,5.