---
name: ocr-image-text-extraction
description: "OCR images via tesseract; fetch receipt data from links."
---

# OCR / Image Text Extraction (local fallback) + Payment-Link Receipt Data

Extract text from images when the vision tool is **unavailable** (e.g. `40x · No endpoints found for google/gemini-2.0-flash-001` — that is CONFIG state, not a permanent tool failure), or when OCR is needed on many prints. Also covers pulling structured receipt data directly from a payment link.

## 1. Prefer the link, not the image, when there is one

If the user gave both an image AND a payment/receipt link (e.g. InfinitePay `recibo.infinitepay.io/<id>`), **fetching the link gives far cleaner data than OCR**: exact amounts, parcel breakdown, merchant, timestamp, transaction ID, NSU.

```bash
curl -sL --max-time 25 "<PAYMENT_URL>" -A "Mozilla/5.0" | \
  python3 -c "import sys,re,html; t=sys.stdin.read(); t=re.sub(r'<script.*?</script>','',t,flags=re.S); t=re.sub(r'<style.*?</style>','',t,flags=re.S); t=re.sub(r'<[^>]+>',' ',t); print(html.unescape(t))" \
  | tr -s ' \n' ' \n' | head -60
```
The receipt page embeds the data as plain text. Verify against the image to confirm no divergence.

## 2. Local tesseract preprocessing recipe (works when vision is down)

Plain `tesseract` on a screenshot/photo misses text. The recipe that works reliably:

```bash
# 1) grayscale + 2x upscale + sharpen
python3 -c "
from PIL import Image, ImageFilter
im = Image.open('img.jpg').convert('L')
im = im.resize((im.width*2, im.height*2), 3)   # LANCZOS
im = im.filter(ImageFilter.SHARPEN)
im.save('/tmp/big.png')"

# 2) OCR em português, testando PSM 3, 4 e 6 (cada um pega layouts diferentes)
tesseract /tmp/big.png stdout -l por --psm 4 | sed '/^\s*$/d'
tesseract /tmp/big.png stdout -l por --psm 6 | sed '/^\s*$/d'
```
- Preprocess BEFORE binarizing; upscaling + sharpen alone usually lifts legibility enough.
- Run multiple `--psm` (3, 4, 6) and merge; no single PSM is universal.
- Read the raw output critically: tesseract occasionally inverts/merges words. Do NOT present OCR output as if seen — label it as OCR-extracted and confirm the key figures (R$, dates, card digits, parcel counts) against another source (the link, or the user).

## 3. Pitfalls
- **Never claim you "saw" what you only parsed with OCR** — say it was OCR-extracted and list what could not be read verifiably.
- If OCR yields only fragments, ask the user to describe the image and/or provide the audio/link rather than inventing content.
- tesseract needs the `por` traineddata for Portuguese: `sudo apt install tesseract-ocr-por` (install is the fix; not a durable blocker).

## Related
- Pairs with the `ocr-and-documents` skill for full PDF/document OCR workflows (that skill may be protected/hub-owned; don't duplicate it, just hand off).