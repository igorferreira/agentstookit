# 📄 Workflow: Gerar PDF do Fluxo de Caixa (MD → wkhtmltopdf)

> Atualizado: 13/08/2026 (X23, ~76 KB / 2 páginas)

## Pipeline completo (XLSX → MD → PDF)

```bash
# 1. Garantir que XLSX está recalculado
ls -la /tmp/recalc_out/model.xlsx

# 2. Regenerar .md a partir do .xlsx
python3.12 ~/.hermes/skills/finance/atualizar-controles/scripts/regenerate_md_from_xlsx.py

# 3. Gerar PDF do .md via pandoc + wkhtmltopdf
pandoc ~/MEGA/Comprovantes/FLUXO-CAIXA-2026-2030.md \
  -o ~/MEGA/Comprovantes/FLUXO-CAIXA-2026-2030.pdf \
  --pdf-engine=wkhtmltopdf \
  --pdf-engine-opt=--no-background \
  -V geometry:margin=1.5cm \
  -V fontsize=8pt
```

## Orientação: paisagem (landscape)

Para o fluxo de caixa (muitas colunas), usar **paisagem**. Para outros relatórios (dossiê advogado, rescisão), usar **retrato** (portrait).

```bash
# Paisagem (fluxo de caixa, 9 colunas)
pandoc X.md -o X.pdf --pdf-engine=wkhtmltopdf \
  -V geometry:landscape \
  -V geometry:margin=1.5cm \
  -V fontsize=8pt

# Retrato (dossiês, rescisão)
pandoc X.md -o X.pdf --pdf-engine=wkhtmltopdf \
  -V geometry:margin=2cm \
  -V fontsize=10pt
```

## Customizar template HTML (para visual mais rico)

Quando precisar de cores, bordas customizadas, etc:

```bash
# 1. Converter MD → HTML com template custom
pandoc ~/MEGA/.../FLUXO.md -o /tmp/fluxo.html \
  --standalone \
  --template=/tmp/dossie-style.html

# 2. Gerar PDF com CSS custom
wkhtmltopdf --no-background --enable-local-file-access \
  /tmp/fluxo.html /tmp/fluxo.pdf

# 3. Mover para destino final
mv /tmp/fluxo.pdf ~/MEGA/.../FLUXO.pdf
```

## Template HTML recomendado (`/tmp/dossie-style.html`)

```html
<!DOCTYPE html>
<html>
<head>
<style>
@page { size: A4 landscape; margin: 1.5cm; }
body { font-family: Arial, sans-serif; font-size: 8pt; line-height: 1.3; }
h1 { font-size: 16pt; color: #1F4E78; border-bottom: 2px solid #1F4E78; }
h2 { font-size: 11pt; color: #1F4E78; border-bottom: 1px solid #ccc; }
table { border-collapse: collapse; width: 100%; font-size: 7pt; }
th { background: #1F4E78; color: #fff; padding: 3px 4px; border: 1px solid #ccc; }
td { padding: 2px 4px; border: 1px solid #ccc; }
tr:nth-child(even) { background: #f7f7f7; }
tr:nth-child(odd) { background: #fff; }
.page-break { page-break-after: always; }
hr { border: 0; border-top: 1px solid #ddd; margin: 8px 0; }
</style>
</head>
<body>
$body$
</body>
</html>
```

## Pitfalls

1. **`pandoc --pdf-engine=wkhtmltopdf`** é mais rápido e flexível que `wkhtmltopdf` direto (pula etapa MD→HTML manual).
2. **`--no-background`** desabilita gradientes de fundo (mantém PDF limpo para impressão).
3. **Warnings de "Gtk-Message"** do LibreOffice são inofensivos — ignorar.
4. **PDF em modo paisagem:** passar `geometry:landscape` como `-V` (não funciona no CSS `@page` quando via pandoc).
5. **PDF fica pequeno demais?** Ajustar `-V fontsize` para 9pt ou 10pt.
6. **Colunas muito largas?** Reduzir `geometry:margin` para 1cm.

## Comando completo (one-liner para Igor)

```bash
python3.12 ~/.hermes/skills/finance/atualizar-controles/scripts/regenerate_md_from_xlsx.py \
  && pandoc ~/MEGA/Comprovantes/FLUXO-CAIXA-2026-2030.md \
       -o ~/MEGA/Comprovantes/FLUXO-CAIXA-2026-2030.pdf \
       --pdf-engine=wkhtmltopdf \
       --pdf-engine-opt=--no-background \
       -V geometry:landscape \
       -V geometry:margin=1.5cm \
       -V fontsize=8pt
```