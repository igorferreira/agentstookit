# Padrão de versões (4 formatos) + DOCX canônico + formatação ABNT (petições)

Consolidado empiricamente com o Igor ao padronizar o acervo `processo_marica_igor` (01/09/2026). Aplica à classe "organizar/entregar arquivos de processo".

## 4 versões por documento (regra do Igor)

Todo documento do processo deve existir em **4 formatos** com o **MESMO nome base** (ex.: `PETICAO_EXCECAO_PRE_EXECUTIVIDADE_V7`):

- `.md`   — fonte de texto / nota interna
- `.gddoc` — atalho Google Docs (canônico quando o advogado edita no Docs; NÃO criável por CLI — ver SKILL)
- `.pdf`  — entrega / leitura
- `.docx` — **formato EDITÁVEL canônico** para o advogado trabalhar em Word

Nada apagado; todas as versões mantidas. Mesmos arquivos nas 3 pastas (MEGA canônica + cópia compartilhada do advogado + backup Drive), byte-idênticos (hash).

## Fluxo de edição: trabalhar primeiro no DOCX (correção explícita do Igor)

O Igor corrigiu a ordem: **"Não é melhor você trabalhar no DOCX e depois gerar o Markdown e o PDF?"**

Fluxo canônico de geração:
1. Editar/gerar o **`.docx`** primeiro (é a fonte editável da verdade).
2. Derivar o **`.md`** do DOCX: `pandoc base.docx -f docx -t gfm -o base.md` (mantém consistência).
3. Derivar o **`.pdf`** do DOCX: `soffice --headless --convert-to pdf` (mais fiel ao Word que pandoc/wkhtmltopdf).

## Formatação ABNT / forense brasileira no DOCX (python-docx)

Aplicada ao editar o DOCX canônico com `python-docx`:

- **Página A4, retrato**: `section.page_width = Cm(21)`, `page_height = Cm(29.7)`
- **Margens (ABNT)**: superior 3 cm, esquerda 3 cm, direita 2 cm, inferior 2 cm
- **Espaçamento entre linhas 1,5** em todos os parágrafos (`WD_LINE_SPACING.ONE_POINT_FIVE`)
- **Fonte Times New Roman 12** em todo texto (estilo Normal + cada run, incluindo `w:rFonts` ascii/hAnsi/cs/eastAsia)
- **Alinhamento**: corpo justificado (`JUSTIFY`); títulos de seção centralizados + negrito
- `space_before = Pt(0)`, `space_after = Pt(6)`; recuo de 1ª linha 1,25 cm no corpo (não em listas/endereçamento)

Ambiente python-docx: venv dedicado com `uv` (`uv venv && uv pip install python-docx`); o python3 do sistema e o venv do Hermes não têm pip/python-docx — não retentar instalar neles.

## Regra anti-título-órfão e anti-página-em-branco no PDF (exigência do Igor)

Ao gerar o PDF final, VALIDAR:
- **Nenhum título de seção órfão** = título isolado no fim da página com o corpo na página seguinte. Ocorreu com o "X. DOS HONORÁRIOS..." na V7.
- **Nenhuma página em branco no fim** (wkhtmltopdf e LibreOffice às vezes emitem uma página vazia final).

Verificação rápida: `pdftotext -layout final.pdf out.txt`; dividir por `\x0c` (form feed) e, em cada página, checar se a **última linha não-vazia** casa com um cabeçalho romano (`^(I{1,3}|IV|V|VII?|VIII|IX|X|XI)\s*\.`) → título órfão; página vazia → remover.

Remoção de página em branco: `pdfseparate in.pdf clean/p%d.pdf`, eliminar a página vazia, `pdfunite ... out.pdf`.

Prevenção de título órfão (wkhtmltopdf): CSS `h1,h2,h3{page-break-after:avoid;}` + envolver cada `<h2>` com o bloco seguinte em `div{page-break-inside:avoid}`. Com LibreOffice a partir do DOCX esse problema raramente aparece.

## Verificação de fidelidade de margens/página

`pdfinfo -box final.pdf` → `MediaBox` deve ser `595.30 x 841.89 pts` (A4). Se cair em `612 x 792` (Letter), o DOCX está em papel errado — corrigir page_width/height para Cm(21)/Cm(29.7), não só as margens.