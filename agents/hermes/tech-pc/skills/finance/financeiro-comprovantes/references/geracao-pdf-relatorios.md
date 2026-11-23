# Geração de PDF para relatórios financeiros (pandoc + wkhtmltopdf)

## Contexto

Relatórios financeiros (dossiê, diagnóstico, agenda) precisam ser gerados em PDF com aparência profissional. O ambiente não tem weasyprint/pdflatex, então usamos pandoc → HTML → wkhtmltopdf com template CSS customizado.

## Problema: fundo preto do wkhtmltopdf

O wkhtmltopdf herda o tema escuro do sistema se não houver CSS explícito. O resultado são PDFs com fundo preto e tabelas ilegíveis.

## Solução: template HTML com CSS forçado

Criar um template HTML com CSS explícito que força fundo branco e estiliza tabelas:

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
body {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 10pt;
  color: #111;
  background: #fff;
  line-height: 1.4;
  max-width: 100%;
  padding: 20px;
}
h1 { font-size: 16pt; color: #1a1a1a; border-bottom: 2px solid #333; padding-bottom: 4px; }
h2 { font-size: 13pt; color: #222; border-bottom: 1px solid #999; padding-bottom: 2px; margin-top: 18px; }
h3 { font-size: 11pt; color: #333; margin-top: 14px; }
table {
  border-collapse: collapse;
  width: 100%;
  margin: 8px 0 12px 0;
  font-size: 9pt;
  page-break-inside: avoid;
}
th {
  background: #e0e0e0;
  color: #111;
  font-weight: bold;
  text-align: left;
  padding: 4px 6px;
  border: 1px solid #999;
}
td {
  padding: 3px 6px;
  border: 1px solid #ccc;
  background: #fff;
  color: #111;
}
tr:nth-child(even) td { background: #f7f7f7; }
blockquote {
  background: #fff3cd;
  border-left: 3px solid #ffc107;
  margin: 8px 0;
  padding: 6px 10px;
  font-size: 9pt;
}
code { background: #f0f0f0; padding: 1px 3px; font-size: 9pt; }
strong { color: #1a1a1a; }
ul, ol { margin: 4px 0; }
p { margin: 4px 0; }
hr { border: none; border-top: 1px solid #ccc; margin: 12px 0; }
@media print { body { padding: 0; } }
</style>
</head>
<body>
BODYCONTENT
</body>
</html>
```

## Fluxo completo (método simplificado com CSS externo)

```bash
# 1. Converter Markdown para HTML
pandoc relatorio.md -t html --standalone --metadata title="Título" -o /tmp/relatorio.html

# 2. Gerar PDF com CSS externo (contém regras de page-break, widows, etc.)
wkhtmltopdf --no-background --enable-local-file-access \
  --page-size A4 --margin-top 15mm --margin-bottom 12mm \
  --margin-left 12mm --margin-right 12mm \
  --user-style-sheet /tmp/dossie-fix.css \
  /tmp/relatorio.html relatorio.pdf

# 3. Verificar páginas e órfãos
python3 -c "
import subprocess, re
result = subprocess.run(['pdftotext', '-layout', 'relatorio.pdf', '-'],
                       capture_output=True, text=True)
pages = result.stdout.split('\f')
# ... script de detecção de órfãos (ver seção Verificação)
"
```

### Método alternativo (HTML template inline com pandoc `--css`)

```bash
pandoc relatorio.md -t html --standalone --metadata title="Título" \
  --css=/tmp/estilo.css -o /tmp/relatorio.html
```

O `--css` adiciona um `<link>` ao stylesheet. O CSS externo (`--user-style-sheet` no wkhtmltopdf) é preferível porque o pandoc pode não embutir o CSS referenciado.

## Fluxo completo (método antigo com template HTML injetado)

### Pitfall: pandoc default CSS renders as visible text

pandoc's `--standalone` flag generates a default `<style>` block with dark-theme styles (`background: #fdfdfd`, max-width, etc.). If you inject custom CSS by replacing `</head>`, the pandoc default `<style>` block remains and **both** style blocks may render as visible text in wkhtmltopdf output.

**Fix:** Strip pandoc's default `<style>...</style>` block before injecting custom CSS:

```python
import re
html = re.sub(r'<style>.*?</style>', '', html, flags=re.DOTALL)
html = html.replace('</head>', f'<style>\n{css}\n</style>\n</head>')
```

Always verify with `pdftotext -f 1 -l 1 file.pdf - | head -10` that no CSS fragments leaked into the visible text layer.

- **--no-background**: essencial para evitar que o wkhtmltopdf preserve qualquer fundo escuro residual.
- **sed table width**: pandoc gera `<table>` sem estilo; o `sed` adiciona `width:100%` para evitar tabelas coladas à esquerda. Com CSS externo via `--user-style-sheet`, a regra `table { width: 100% }` resolve isso sem sed.
- **Tamanho da fonte**: 9-10pt funciona bem para tabelas densas. Acima de 10pt, tabelas com 8+ colunas podem quebrar. Ajustar `font-size` em ±0.5pt para controlar a paginação final.
- **page-break-inside: avoid**: útil em tabelas, mas pode criar páginas quase vazias se a tabela for grande. Para tabelas de 25+ linhas, considerar não usar essa regra ou dividir a tabela manualmente.
- **Emojis no título**: wkhtmltopdf renderiza emojis no texto mas pode falhar em headers. Prefira emojis no corpo do texto ou use texto puro nos títulos.
- **Encoding do pdftotext**: `pdftotext -layout` pode distorcer acentos (ex: "próximos" → caracteres quebrados), causando falsos negativos em grep/verificação de conteúdo. Para busca de texto, usar `pdftotext -raw`. Para análise de estrutura de página (form feeds), usar `-layout`.
- **Página extra vazia**: comum quando o conteúdo não preenche a última página. Ajustar `--margin-bottom` (reduzir 2-3mm) ou aumentar `font-size` (0.5pt) para forçar redistribuição. Verificar com script de detecção após cada ajuste.
- **CSS do pandoc conflitando com CSS customizado**: quando se usa `pandoc --standalone`, o HTML gerado inclui um bloco `<style>` padrão (max-width: 36em, padding, etc.) que conflita com regras de layout do CSS customizado (margem, largura de tabela). Antes de injetar CSS próprio, remover o `<style>` padrão com regex: `re.sub(r'<style>.*?</style>', '', html, flags=re.DOTALL)`. Depois injetar o CSS customizado antes de `</head>`. Sem esse passo, tabelas podem ficar limitadas a 36em de largura ou o texto pode ficar com padding excessivo.
- **CSS vazando como texto visível no PDF**: usar `pandoc -H arquivo.css` injeta o conteúdo do CSS como raw HTML no `<head>`, mas dependendo da versão do pandoc pode acabar no `<body>`, tornando o CSS visível no PDF gerado. Prefira sempre o método standalone + Python injection: gere HTML com `--standalone`, remova o `<style>` padrão, e injete o CSS customizado ANTES de `</head>`.

## Verificação de qualidade do PDF (antes de entregar)

### Verificação automatizada de órfãos com Python

O script abaixo detecta headings (`##`, `###`) que ficaram no final de uma página com o conteúdo na página seguinte, além de páginas vazias e transições suspeitas:

```python
import subprocess, re

result = subprocess.run(
    ['pdftotext', '-layout', 'relatorio.pdf', '-'],
    capture_output=True, text=True
)
pages = result.stdout.split('\f')

# 1. Páginas vazias
for i, page in enumerate(pages, 1):
    lines = [l.strip() for l in page.split('\n') if l.strip()]
    if not lines:
        print(f"❌ Página {i}: VAZIA")

# 2. Headings como última linha da página
orphans = 0
for i, page in enumerate(pages, 1):
    lines = [l.strip() for l in page.split('\n') if l.strip()]
    if not lines:
        continue
    for line in lines[-3:]:  # últimas 3 linhas
        if re.match(r'^#{1,4}\s', line):
            print(f"🔴 Pág {i}: órfão → '{line[:80]}'")
            orphans += 1

# 3. Transições — primeira linha de cada página
for i, page in enumerate(pages[1:], 2):
    lines = [l.strip() for l in page.split('\n') if l.strip()]
    if lines:
        print(f"Pág {i} começa com: '{lines[0][:100]}'")
```

**Critérios de aprovação:**
- Nenhuma página vazia (exceto se for a última e tiver conteúdo real).
- Nenhum heading nas últimas 3 linhas de qualquer página.
- Primeira linha de cada página (a partir da 2ª) não deve começar com minúscula depois de um heading na página anterior.

### ⚠️ Encoding: pdftotext -layout vs -raw

`pdftotext -layout` pode distorcer caracteres acentuados (ex: "próximos" → "proximos"), causando falsos negativos no grep. Para verificação de conteúdo, usar `pdftotext -raw` que preserva o encoding original. O `-layout` é melhor para análise de posição de página (form feeds), mas o `-raw` é melhor para busca de texto.

### Página vazia no final — correção por margem

Se o PDF gerar uma página extra vazia no final, ajustar `--margin-bottom` para baixo (ex: de 15mm para 12mm) força o conteúdo a ocupar a última página. Se isso cortar conteúdo, aumentar o `font-size` no CSS em 0.5pt para forçar o layout a usar mais páginas com conteúdo real.

**Fluxo de tentativa e erro:**
1. Gerar com `--margin-bottom 12mm` → se cortar conteúdo, voltar para 14mm
2. Se voltar a ter página vazia com 14mm, aumentar `font-size` de 11pt para 11.5pt
3. Repetir até ter N páginas com a última contendo conteúdo real

### CSS refinado para evitar órfãos e quebras

```css
body {
    background: #fff;
    font-family: 'DejaVu Sans', Arial, sans-serif;
    font-size: 11pt;         /* ajustar ±0.5pt para controlar paginação */
    line-height: 1.45;
    color: #222;
}

h1, h2, h3, h4 {
    page-break-after: avoid;  /* evita heading órfão */
    break-after: avoid;
}

table {
    page-break-inside: avoid;  /* evita quebra de tabela */
    break-inside: avoid;
}

p {
    widows: 2;                /* mínimo 2 linhas no fim da página */
    orphans: 2;               /* mínimo 2 linhas no topo da página */
}

blockquote {
    page-break-inside: avoid;  /* mantém callout inteiro */
}
```

### Checklist de qualidade do PDF

1. **Títulos órfãos**: rodar script de detecção automática. Corrigir com `page-break-after: avoid` no CSS ou inserindo quebra explícita antes da seção no Markdown.
2. **Tabelas divididas**: `break-inside: avoid` em `table` resolve a maioria. Se a tabela for muito grande (>25 linhas), considerar dividi-la manualmente em um ponto lógico.
3. **Fundos e contraste**: CSS `background: #fff` no body + `--no-background` no wkhtmltopdf.
4. **Páginas vazias**: ajustar margens ou font-size. Rodar script de detecção.
5. **Encoding na verificação**: usar `pdftotext -raw` para busca de texto, `-layout` para análise estrutural.
6. **Última página**: validar que contém conteúdo real, não apenas footer ou linha solta.
7. **Valores-chave**: verificar totais, vencimentos e números críticos no texto extraído.
