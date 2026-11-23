---
name: ocr-and-documents
description: "Extract text from PDFs/scans (pymupdf, marker-pdf), edit PDFs with natural language (nano-pdf), and work with Office documents."
version: 2.3.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [PDF, Documents, Research, Arxiv, Text-Extraction, OCR, nano-pdf]
    related_skills: [powerpoint]
---

# PDF & Document Extraction and Editing

## Umbrella Router

- **Extract text from PDFs (text-based):** pymupdf — see section below.
- **Extract text from scanned PDFs / images / equations:** marker-pdf — see section below.
- **Read/extract from remote URLs:** `web_extract` (try first — handles PDF-to-markdown via Firecrawl).
- **Edit PDF text with natural-language instructions:** see `references/nano-pdf.md` (nano-pdf CLI).
- **Create/edit/read .pptx PowerPoint files:** see the `powerpoint` skill (uses python-pptx).
- **Read/edit .docx Word files:** use `python-docx` (parses actual document structure, far better than OCR).

## Step 1: Remote URL Available?

If the document has a URL, **always try `web_extract` first**:

```
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])
web_extract(urls=["https://example.com/report.pdf"])
```

This handles PDF-to-markdown conversion via Firecrawl with no local dependencies.

Only use local extraction when: the file is local, web_extract fails, or you need batch processing.

## Step 2: Choose Local Extractor

| Feature | pymupdf (~25MB) | marker-pdf (~3-5GB) |
|---------|-----------------|---------------------|
| **Text-based PDF** | ✅ | ✅ |
| **Scanned PDF (OCR)** | ❌ | ✅ (90+ languages) |
| **Tables** | ✅ (basic) | ✅ (high accuracy) |
| **Equations / LaTeX** | ❌ | ✅ |
| **Code blocks** | ❌ | ✅ |
| **Forms** | ❌ | ✅ |
| **Headers/footers removal** | ❌ | ✅ |
| **Reading order detection** | ❌ | ✅ |
| **Images extraction** | ✅ (embedded) | ✅ (with context) |
| **Images → text (OCR)** | ❌ | ✅ |
| **EPUB** | ✅ | ✅ |
| **Markdown output** | ✅ (via pymupdf4llm) | ✅ (native, higher quality) |
| **Install size** | ~25MB | ~3-5GB (PyTorch + models) |
| **Speed** | Instant | ~1-14s/page (CPU), ~0.2s/page (GPU) |

**Decision**: Use pymupdf unless you need OCR, equations, forms, or complex layout analysis.

If the user needs marker capabilities but the system lacks ~5GB free disk:
> "This document needs OCR/advanced extraction (marker-pdf), which requires ~5GB for PyTorch and models. Your system has [X]GB free. Options: free up space, provide a URL so I can use web_extract, or I can try pymupdf which works for text-based PDFs but not scanned documents or equations."

---

## pymupdf (lightweight)

```bash
pip install pymupdf pymupdf4llm
```

**Via helper script**:
```bash
python scripts/extract_pymupdf.py document.pdf              # Plain text
python scripts/extract_pymupdf.py document.pdf --markdown    # Markdown
python scripts/extract_pymupdf.py document.pdf --tables      # Tables
python scripts/extract_pymupdf.py document.pdf --images out/ # Extract images
python scripts/extract_pymupdf.py document.pdf --metadata    # Title, author, pages
python scripts/extract_pymupdf.py document.pdf --pages 0-4   # Specific pages
```

**Inline**:
```bash
python3 -c "
import pymupdf
doc = pymupdf.open('document.pdf')
for page in doc:
    print(page.get_text())
"
```

---

## marker-pdf (high-quality OCR)

```bash
# Check disk space first
python scripts/extract_marker.py --check

pip install marker-pdf
```

**Via helper script**:
```bash
python scripts/extract_marker.py document.pdf                # Markdown
python scripts/extract_marker.py document.pdf --json         # JSON with metadata
python scripts/extract_marker.py document.pdf --output_dir out/  # Save images
python scripts/extract_marker.py scanned.pdf                 # Scanned PDF (OCR)
python scripts/extract_marker.py document.pdf --use_llm      # LLM-boosted accuracy
```

**CLI** (installed with marker-pdf):
```bash
marker_single document.pdf --output_dir ./output
marker /path/to/folder --workers 4    # Batch
```

---

## Arxiv Papers

```
# Abstract only (fast)
web_extract(urls=["https://arxiv.org/abs/2402.03300"])

# Full paper
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])

# Search
web_search(query="arxiv GRPO reinforcement learning 2026")
```

## Split, Merge & Search

pymupdf handles these natively — use `execute_code` or inline Python:

```python
# Split: extract pages 1-5 to a new PDF
import pymupdf
doc = pymupdf.open("report.pdf")
new = pymupdf.open()
for i in range(5):
    new.insert_pdf(doc, from_page=i, to_page=i)
new.save("pages_1-5.pdf")
```

```python
# Merge multiple PDFs
import pymupdf
result = pymupdf.open()
for path in ["a.pdf", "b.pdf", "c.pdf"]:
    result.insert_pdf(pymupdf.open(path))
result.save("merged.pdf")
```

```python
# Search for text across all pages
import pymupdf
doc = pymupdf.open("report.pdf")
for i, page in enumerate(doc):
    results = page.search_for("revenue")
    if results:
        print(f"Page {i+1}: {len(results)} match(es)")
        print(page.get_text("text"))
```

No extra dependencies needed — pymupdf covers split, merge, search, and text extraction in one package.

---

## Technical Diagrams and Dense Screenshots

For architecture diagrams, flowcharts, sequence charts, schematics, and other images with small labels, OCR the image in regions and verify the relationships visually before writing a description:

1. Preserve the original image. If copying it into a study folder, verify the copy with a SHA-256 comparison rather than relying only on matching filenames or sizes.
2. Check Tesseract availability and the required language packs, then run a full-image pass to build a rough label inventory, for example: `tesseract diagram.png stdout -l por+eng --psm 11`.
3. Inspect the image and crop distinct boxes/lanes or dense regions. Upscale crops 2–3× with Pillow `Image.Resampling.LANCZOS`; use `--psm 11` for sparse labels and `--psm 6` for a dense text block. Keep OCR output for each region separate so labels remain traceable to their location.
4. Cross-check every important label and every arrow direction against the image at enlarged scale. OCR is a transcription aid, not evidence for a connection or security property.
5. Write the Markdown in layers: exact visible labels; visible components and boundaries; relationships that are visually clear; then a separate section for ambiguous text and interpretations. Preserve uncertainty instead of repairing a label by guesswork.
6. Build Mermaid only from the verified transcription. Use dashed edges or explicit uncertainty notes for relationships that are inferred, and state that the diagram documents the supplied drawing rather than proving the deployed implementation. Validate with a local Mermaid parser/renderer when available; otherwise run structural checks (balanced subgraphs, declared edge endpoints) and disclose that rendering was not validated.

```python
from PIL import Image
import pytesseract

img = Image.open("diagram.png")
x0, y0, x1, y1 = 120, 80, 520, 360  # coordinates chosen from visual inspection
crop = img.crop((x0, y0, x1, y1))
w, h = crop.size
crop = crop.resize((w * 3, h * 3), Image.Resampling.LANCZOS)
print(pytesseract.image_to_string(crop, lang="por+eng", config="--psm 11"))
```

**Pitfalls:** Do not treat a successful OCR run as proof that all labels were captured; diagram text density and direction vary by region. Do not claim a vulnerability, authorization rule, or runtime behavior from a diagram alone; the drawing may omit implementation details.

## Mobile Screenshot OCR (Tesseract + crop strategy)

When OCR-ing a mobile app screenshot (JPG/PNG, typically 720×1280 or similar), full-image Tesseract often produces garbled output because of UI chrome, colored backgrounds, and mixed font sizes. The effective approach is:

1. **Identify regions of interest** by cropping vertical slices (80–120px tall) across the full image width.
2. **Upscale each crop 2×** with `Image.LANCZOS` before OCR.
3. **Use `--psm 6`** (assume a uniform block of text) for best results on mobile UI labels.
4. **Scan from top to bottom**, printing only slices that contain keywords (`R$`, `fatura`, `valor`, `total`, `vencimento`, `limite`).

```python
import pytesseract
from PIL import Image

img = Image.open("screenshot.jpg")
w, h = img.size

for y_start in range(0, h, 80):
    crop = img.crop((0, y_start, w, min(y_start + 120, h)))
    crop = crop.resize((w * 2, 240), Image.LANCZOS)
    text = pytesseract.image_to_string(crop, lang="por", config="--psm 6")
    if any(kw in text.lower() for kw in ["r$", "fatura", "valor", "total", "vencimento", "limite"]):
        print(f"--- y={y_start} ---")
        print(text.strip())
```

**Pitfall:** The "Home" tab of credit-card apps often shows limit/status but NOT the fatura value. When the image shows bottom navigation tabs (`Home | Fatura | Limite`), ask the user for the **"Fatura" tab** screenshot to extract the actual bill amount.

## Notes

- `web_extract` is always first choice for URLs
- pymupdf is the safe default — instant, no models, works everywhere
- marker-pdf is for OCR, scanned docs, equations, complex layouts — install only when needed
- Both helper scripts accept `--help` for full usage
- marker-pdf downloads ~2.5GB of models to `~/.cache/huggingface/` on first use
- For Word docs: `pip install python-docx` (better than OCR — parses actual structure)
- For PowerPoint: see the `powerpoint` skill (uses python-pptx)
- Tesseract installation: `pip install pytesseract` (bindings) + `tesseract` (system binary, usually pre-installed). Verify with `tesseract --version` and `tesseract --list-langs | grep por` for Portuguese support.
- When Tesseract returns garbled text on a full image, use the crop-based approach in the "Mobile Screenshot OCR" section above.
