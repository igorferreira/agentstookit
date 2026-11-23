# Estilo Diogo — medidas REAIS vs. ABNT (correção 02/09/2026)

**Fonte:** medição por `pdftotext -bbox` do PDF da V6 original de 18 páginas. **Esta ref SUPERSEDE os valores 3/3/2/2 e recuo 1,25 cm que constam em `references/estilo-diogo-juridico.md`** (eram a presunção ABNT, NÃO a realidade do Google Docs).

## Margens reais (A4 596×842 pts)
| Margem | Valor real | pts |
|---|---|---|
| Superior | **2,9 cm** | ~82 |
| Esquerda | **2,54 cm (1")** | 72 |
| Direita | **2,57 cm** | ~73 |
| Inferior | **varia 2,7–4,2 cm** | conforme rodapé |
| Recuo 1ª linha | **~1,0 cm** | ~100,5 pts − 72 |

As margens do Google Docs = **padrão 1" de fábrica** (2,54 cm), não ABNT 3/2 cm.

## Espaçamento da 1ª página — padrão de parágrafos vazios 5/3/3/3/3
Linha normal = **21 pts**. Cada linha vazia soma ~30 pts. Gap medido (pts):
- Endereçamento→`Processo nº`: **~123 pts ≈ 5 vazios**
- `Processo nº`→preâmbulo: **~61 pts ≈ 3 vazios**
- Preâmbulo→título: **~61 pts ≈ 3 vazios**
- Título→`pelos fundamentos`: **~62 pts ≈ 3 vazios**
- `pelos fundamentos`→primeira seção: **~61 pts ≈ 3 vazios**
- **Seções do corpo**: separadas por ~1–2 vazios; nunca colar blocos.

## Pipeline de produção para gerar a peça fiel (pandoc NÃO reproduz isso)
1. `pandoc peca.md -o base.docx`
2. python-docx: forçar Arial em todas as runs + preto puro `RGB(0,0,0)` + remover `w:highlight` (`to_arial.py`).
3. python-docx: A4, margens 2,9/2,54/2,57/2,78 cm, espaçamento 1,5, e **inserir parágrafos vazios `w:p` nos gaps 5/3/3/3/3** localizando os blocos por prefixo de texto (`EXCELENT`, `Processo nº`, `IGOR DOS SANTOS`, `EXCEÇÃO DE PRÉ`, `pelos fundamentos`, `I. O QUE`).
4. `soffice --headless --convert-to pdf` → remover página vazia final com `pdfseparate`+`pdfunite`.

## Verificação de fidelidade
- 1ª página via `pdftotext -layout -f 1 -l 1 out.pdf - | cat -A` → esperar `$` (vazios) nas posições certas.
- Contagem de vazios no DOCX: percorrer `doc.paragraphs`, contar sequência de parágrafos sem texto → deve bater `[5,3,3,3,3]`.
- Negritos essenciais por `grep`-style: endereçamento, `Processo nº`, título, `IGOR DOS SANTOS FERREIRA`, `MUNICÍPIO DE MARICÁ`, datas-marcos, `R$ ...`, `CPF ...`.