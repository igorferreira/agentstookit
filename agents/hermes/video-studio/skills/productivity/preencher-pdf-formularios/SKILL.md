---
name: preencher-pdf-formularios
description: Preencha formulários PDF sobrepondo texto nos campos.
---

# Preencher Formulários PDF (overlay de texto)

Preenche formulários PDF que NÃO têm campos editáveis, sobrepondo texto (fonte com acentos) exatamente sobre as linhas-guia, com validação objetiva por análise de pixels.

## Quando usar
- Formulário em PDF que é imagem/texto (requerimentos, cadastros, fichas)
- Preencher com dados do Usuário e gerar versão preenchida
- Ex: Requerimento Geral do Simplifica [REDACTADO], cadastros de órgãos, fichas bancárias

## Requisitos
- Python 3.12 com PyMuPDF (fitz) e Pillow: `pip install PyMuPDF Pillow`
- `pdftoppm` (poppler-utils)
- Fonte Liberation Sans (`/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf`) — tem acentos e é ≈Arial
- NÃO usar fonte sem acentos (texto sai corrompido: "Ã", "para o garantir")

## Passo a passo

### 1. Mapear a geometria do formulário
```python
import fitz
doc = fitz.open("formulario.pdf")
page = doc[0]
print("page rect:", page.rect)
# Rótulos (etiquetas dos campos) com posição
for b in page.get_text("dict")["blocks"]:
    for l in b.get("lines", []):
        for s in l.get("spans", []):
            print(f"label:'{s['text']}' bbox=({s['bbox'][0]:.1f},{s['bbox'][1]:.1f})-({s['bbox'][2]:.1f},{s['bbox'][3]:.1f})")
# Línhas-guia (underlines longas) onde se escreve
for d in page.get_drawings():
    r = d["rect"]
    if r.height < 3 and r.width > 80:
        print(f"linha-guia y={r.y0:.1f} x={r.x0:.1f}-{r.x1:.1f}")
```

### 2. Determinar as BANDAS DE ESCRITA (crítico)
O padrão de formulário: rótulo (etiqueta) no topo da célula + linha-guia abaixo. O valor deve ser escrito na faixa em branco abaixo do rótulo / sobre a linha-guia. NUNCA na altura do rótulo (colide com a etiqueta).

Calcule a banda vazia de cada campo por projeção de pixels:
```python
from PIL import Image  # renderize a 200 DPI primeiro: pdftoppm -png -r 200
import numpy as np
a = np.array(Image.open("pag-1.png").convert("L"))
scale = 200/72
# localize a faixa em branco de cada campo para posicionar o texto
faixa = a[int(y0*scale):int(y1*scale), int(x0*scale):int(x1*scale)]
# use projeção de colunas escuras para separar rótulos (texto) de linhas-guia
```

### 3. Inserir o texto (baseline na linha-guia)
```python
page.insert_font("libf", FONT)
BLUE = (0.06, 0.27, 0.94)  # azul padrão de formulário preenchido
def put(text, x, baseline, size):
    page.insert_text((x, baseline), text, fontname="libf", fontsize=size, color=BLUE)
```
- baseline = y da linha-guia (texto "assentado" sobre a linha) OU centro da banda vazia
- fonte ~9-11pt para caber em células pequenas
- padrão visual: azul escuro, igual escrita manual

### 4. Validar por colisão de pixels (obrigatório)
Renderize ORIGINAL e PREENCHIDO a 200 DPI. Pixels pretos no original = rótulos+linhas; no preenchido, pixels azuis = texto novo. Medir se azul colide com rótulos (agrupamentos curtos). Permitir toque com linha-guia (normal).
```python
O = np.array(Image.open("orig-1.png").convert("RGB")).astype(int)
F = np.array(Image.open("fill-1.png").convert("RGB")).astype(int)
diff = np.abs(O - F) > 30
azul = np.all(F > [140,120,120], axis=-1) & np.all(F < [240,220,255], axis=-1)
colisao = diff & ~azul & (O < 160)
# contar por região de campo; 0-10px = OK (traço tocando underline)
```

### 5. Salvar
`doc.save("FORMULARIO_PREENCHIDO.pdf")` — manter o ORIGINAL e o PREENCHIDO. Gerar também imagem de conferência (`pdftoppm -png -r 150`).

## Pitfalls
- Campos que não se aplicam ficam em branco (ex: Registro IPTU em requerimento de empresa). Não inventar valor.
- Confirmar dados com fontes (RG no cartão físico, endereço em comprovante) antes de preencher. Nunca adivinhar.
- Assinatura e Data quase sempre deixadas em branco para assinar à mão ao imprimir.
- `himalaya attachment download` precisa de `--downloads-dir` (senão tenta salvar no caminho original e falha).
- Texto colorido do cabeçalho (logo) do formulário NÃO é preenchimento seu — não confundir na validação.
- O parâmetro baseline do `insert_text` é a origem do texto; ajuste manualmente para centralizar.

## Verificação final
Antes de entregar:
1. Dados corretos no texto extraído (`pdftotext -layout`)
2. Zero/negligível colisão azul × rótulos por campo
3. Texto não invade campo de assinatura/rodapé
4. Campos não aplicáveis em branco