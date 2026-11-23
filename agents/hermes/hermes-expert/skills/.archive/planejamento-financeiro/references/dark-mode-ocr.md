# OCR em screenshots de modo escuro

Apps de banco e cartão frequentemente usam modo escuro, o que quebra o Tesseract.

## Técnica que funciona

```python
from PIL import Image, ImageEnhance, ImageOps
import pytesseract

img = Image.open('screenshot.jpg')
# 1. Inverter cores (dark mode → light mode)
img = ImageOps.invert(img.convert('RGB'))
# 2. Converter para escala de cinza
img = img.convert('L')
# 3. Aumentar contraste
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(2.0)
# 4. Testar múltiplos thresholds
for thresh in [70, 80, 90, 100, 120]:
    test = img.point(lambda x: 0 if x < thresh else 255)
    text = pytesseract.image_to_string(test, config='--oem 3 --psm 6 -l por')
    if len(text.strip()) > 40:
        break
```

## Quando o OCR falha

- Imagens com barras coloridas sobre fundo escuro são especialmente difíceis
- Se 3 tentativas com thresholds diferentes falharem, **pedir para o usuário ditar os valores**
- Não insistir — o OCR de dark mode é imprevisível

## Padrões comuns em apps de cartão

- Gráfico de barras horizontais: "Próximas faturas"
- Labels: "ago/26", "set/26" etc (meses abreviados)
- Valor da barra acima ou abaixo do gráfico
- Seção "Resumo da fatura" com detalhes do mês selecionado
