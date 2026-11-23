---
name: pdf-form-overlay-fill
description: Preencher formulários PDF impressos sobrepondo texto.
---

# PDF Form Overlay Fill (formulário impresso, sem campos AcroForm)

Use quando precisar **preencher um formulário PDF** que foi gerado como imagem/impressão e **não possui campos de formulário (AcroForm)** — típico de requerimentos de prefeituras, órgãos públicos, bancos. Preenchimento real por sobreposição de texto nas coordenadas certas, **verificado por análise de pixels** (sem depender de visão).

> Complementa a skill bundled `pdf` (que cobre AcroForm via pypdf/reportlab). Quando o PDF tiver campos reais (`pdf_read.py --fields` mostrar campos), use `pdf_fill_form.py` da skill `pdf` em vez desta.

## Quando usar
- Formulário de órgão público (ex.: Requerimento Geral de prefeitura) chega como PDF anexo em e-mail, sem campos editáveis.
- Preciso preencher com dados do titular e gerar um PDF "preenchido" limpo para impressão.

## Pré-requisitos
- `fitz` (PyMuPDF) — instalar na venv que tenha o python certo: `pip install PyMuPDF` (testar `python3.12 -c "import fitz"`).
- `pdftoppm` (poppler) para rasterizar e verificar por pixels.
- Fonte TTF com acentos: `/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf` (≈Arial). Verificar com `fc-list`.

## Procedimento (passo a passo que funciona)

1. **Extraia texto e geometria do formulário**
   ```
   fitz: page.get_text('dict')['blocks'] → spans com bbox (x0,y0,x1,y1)
   page.get_drawings() → retangulos/linhas-guia
   ```
   Mapeie cada **rótulo** (etiqueta do campo) com seu bbox, e cada **linha-guia** (underline).

2. **Entenda o layout real ANTES de posicionar.** O erro mais comum (ocorrido na sessão): colocar o `baseline` na MESMA altura do rótulo, fazendo o texto sobrepor a etiqueta. Regra:
   - Cada campo = rótulo (texto pequeno) no topo + célula/linha-guia embaixo.
   - O valor vai na **faixa em branco (banda vazia) entre rótulos ou logo abaixo da linha-guia**, alinhado à coluna do rótulo correspondente.

3. **Não preencha campos sem relação com o caso.** Ex.: em requerimento sobre desvinculação de empresa, `Registro IPTU` (taxa de imóvel) não se aplica — **deixe em branco**. Só preencha `Inscrição Mercantil`/campos pertinentes. (Correção explícita do usuário: "iptu não faz sentido preencher".)

4. **Sobreponha o texto com fitz (`insert_text`)**
   ```python
   page.insert_font("lib", "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf")
   page.insert_text((x, y), texto, fontname="lib", fontsize=10, color=(0.05,0.2,0.85))  # azul
   ```
   - `y` é o **baseline**. Para texto "sentado" sobre a linha-guia use baseline ligeiramente acima (linha_guia - 1..3); para banda vazia, centralize o baseline nela. Fonte ~9-10pt para caber em células curtas.
   - Cor azul sinaliza "preenchido digitalmente" (e permite a verificação por pixel depois).

5. **VERIFICAÇÃO por análise de pixels (crítico — valida sem visão).** Renderize original e preenchido com `pdftoppm -png -r 200` e compare em numpy:
   - Pixel preto no ORIGINAL = rótulos/linhas.
   - Pixel azul no PREENCHIDO (`B>120 e B>R+30 e G<180`) = meu texto.
   - Separe **linhas-guia** (faixas horizontais ocupando >40% da largura) do **rótulo** (texto agrupado).
   - Colisão = pixel azul sobre pixel preto que **não é linha-guia** (ou seja, sobre rótulo). Zero colisões = OK; ~4-10px residuais costumam ser só o traço da fonte tocando a linha-guia (normal).
   ```python
   black_O=(O.mean(axis=2)<140)
   # line_mask: para cada y, linha onde soma de dark na linha > W*0.40
   text_mask = black_O & ~line_mask
   blue = (F[...,2]>110)&(F[...,2]>F[...,0]+30)&(F[...,1]<180)
   colisao = (blue & text_mask).sum()   # deve ser ~0
   ```
   Se colidir → reposicionar `x`/`y`, refazer, reverificar. Iterar até zerar.

6. **Salve em local canônico** (ex.: `.../processo_marica_igor/formulario_simplifica/`) o **original vazio** + o **preenchido** + um **PACOTE_IMPRESSAO/** com o preenchido e anexos, para mandar imprimir.

## Como obter dados corretos do titular
- **RG/órgão/data de emissão**: confirmar no documento físico (OCR com tesseract da imagem; RX se necessário). NÃO confundir com a CNH (números e datas diferentes). Nesta sessão o RG do cartão era `11.599.465-9` DETRAN-RJ 01/02/2017, enquanto a CNH mostrava outro número.
- **Endereço/comprovante**: extrair do comprovante (ex.: fatura Naturgy) no processo.
- Dados canônicos (CPF, telefone, e-mail) de memória / CONTATOS.md.

## Pitfalls
- `himalaya message view` NÃO existe em 2026; usar `himalaya message read` (corpo) e `himalaya attachment download --downloads-dir <dir>` (SEM `--downloads-dir` tenta salvar em path de origem inexistente e falha `No such file or directory`).
- O rodapé do e-mail pode citar `<#part type=application/pdf filename="...">` — é só o marco do anexo, não conteúdo.
- `pdftoppm -r200` (unido) falha em poppler 24.x — usar args separados: `["pdftoppm","-png","-r","200",src,out]`.
- fitz pode estar só no python3.12: testar qual interpretador importa a lib.
- Não responder ao Igor com tabelas Markdown no Telegram (não renderiza) — usar listas/bullets.

## Verificação final
`pdftoppm` → verificação de colisão zerada + conferir que todos os dados corretos estão no texto extraído (`page.get_text()`). Assinatura/Data deixadas em branco para assinar à mão após impressão (salvo se o fluxo exigir assinatura digital).