# OCR Card Statement Extraction

When Igor sends a print of a credit card statement (extrato/fatura), extract all data via tesseract OCR.

## Pre-processing

```bash
python3 << 'PYEOF'
from PIL import Image, ImageEnhance

img = Image.open('/path/to/image.jpg')
# Enhance contrast and sharpness
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(2.5)
enhancer = ImageEnhance.Sharpness(img)
img = enhancer.enhance(2.5)
# Grayscale + resize (3x) + threshold to pure B&W
img = img.convert('L')
img = img.resize((img.width*3, img.height*3), Image.LANCZOS)
img = img.point(lambda x: 0 if x < 128 else 255, '1')
img.save('/tmp/card_ocr_prep.png')
PYEOF
```

## OCR with multiple PSM modes

```bash
for psm in 3 4 6; do
    echo "=== PSM $psm ==="
    tesseract /tmp/card_ocr_prep.png stdout -l por --psm $psm
done
```

- PSM 3: Fully automatic (best for most statements)
- PSM 4: Single column of text
- PSM 6: Uniform block of text
- Always use `-l por` for Portuguese

## Post-processing

After OCR, manually parse the output:

1. **Identify the card**: look for "Final XXXX" or "Visa Platinum"
2. **Separate sections**: physical card (parcelamentos) vs virtual card (à vista)
3. **Extract parcelamentos**: look for "Parcela X de Y" pattern
4. **Calculate remaining**: for each installment, compute: total, já pago, falta pagar, última parcela

## Pattern recognition

```
R$ 215,00
JIM.COM NUCLEO DE M
Parcela 4 de 10
```
→ This means: R$ 215,00/month, currently on installment 4 of 10, 6 remaining

## Pitfalls

- **99Pay transactions**: often appear as "99* OSASCO" or "99 *99Pay*IGOR DOS SAN" — these are Pix no crédito, usually à vista
- **Google subscriptions**: appear as "Google YouTube", "Google Claude", etc. — recurring charges
- **Payment credits**: "Recebemos seu pagamento" with negative value (−R$ X.XXX) — not a charge
- **IOF returns**: "DEVOLUCAO IOF COMPRA" — small credit, ignore for planning
- **Statement may be truncated**: if the image is a partial screenshot, only the visible data is reliable. Ask for the full statement if needed.
