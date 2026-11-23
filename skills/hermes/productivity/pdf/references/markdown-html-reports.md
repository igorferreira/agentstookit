---
name: markdown-html-reports
description: "Use when rendering Markdown reports as styled PDFs."
version: 1.0.0
author: Hermes
metadata:
  hermes:
    tags: [pdf, markdown, pandoc, chrome]
    related_skills: [pdf]
---

# Markdown/HTML report PDFs with Pandoc and Chrome

## When to Use

Use when the source is Markdown and needs CSS-controlled pagination, selectable text, or tables. Keep Markdown canonical; treat generated HTML and PDF as build artifacts.

## Procedure

1. **Choose isolated output paths.** Keep intermediate HTML, Chrome profile data, rendered page images, and temporary CSS in the approved scratch/work directory. Write the final PDF to the requested deliverable location.
2. **Convert Markdown to standalone HTML.** Include the CSS and document language explicitly:

   ```bash
   pandoc report.md --from=gfm --to=html5 --standalone \
     --metadata lang=pt-BR --css=report.css --output=report.html
   ```

   Do not set Pandoc's `title` metadata when the Markdown already starts with a visible H1 unless the title block is suppressed; otherwise the HTML may print two titles.
3. **Print with headless Chrome/Chromium.** Use a disposable user-data directory and disable browser-generated headers/footers so local browser state and date/URL decorations do not enter the deliverable:

   ```bash
   google-chrome --headless=new --no-sandbox --disable-gpu \
     --disable-dev-shm-usage --no-pdf-header-footer \
     --user-data-dir="$SCRATCH/chrome-pdf-profile" \
     --print-to-pdf="$OUTPUT.pdf" "file://$PWD/report.html"
   ```

   Substitute the installed Chrome/Chromium executable and actual absolute paths. Keep `--no-sandbox` only where the host's sandbox setup requires it.
4. **Tune print CSS for legibility and pagination.** Set an explicit `@page` size/margin; use readable body and table text; avoid page breaks immediately after headings; repeat table headers and avoid splitting rows where practical. Example:

   ```css
   @page { size: A4; margin: 12mm 13mm 13mm; }
   body { font: 9.5pt/1.35 Arial, sans-serif; color: #222; }
   h1, h2, h3 { break-after: avoid; page-break-after: avoid; }
   thead { display: table-header-group; }
   tr { break-inside: avoid; page-break-inside: avoid; }
   ```

   Adjust to the content; do not compress text below a comfortable reading size just to force a page count. Avoid nearly empty trailing pages by correcting the HTML/CSS pagination rather than deleting pages from the PDF.
5. **Verify both content and appearance.** Run `pdfinfo` to confirm page count and page dimensions; extract with `pdftotext -layout` and compare key headings, amounts, symbols, and tables against the Markdown; render every page with `pdftoppm -png -r 140 "$OUTPUT.pdf" "$SCRATCH/page"`; visually inspect every rendered page for clipped text, split rows, duplicated headings, illegible type, unexpected whitespace, and blank/sparse pages. Rebuild and repeat if any gate fails.

## Reusing an already-running Chrome via CDP printToPDF

When a Chrome is already running with `--remote-debugging-port` and a profile you must not disturb (e.g. a logged-in session), do NOT launch a second Chrome with `--print-to-pdf` on the same user-data-dir — the profile lock fails the second instance. Reuse the running one over CDP instead: connect to its `/json/list` tab websocket, `Page.enable`, `Page.navigate` to the `file://` HTML, then `Page.printToPDF` (params `printBackground`, `paperWidth/paperHeight`, margins in inches). The base64 PDF comes back nested under `result.data` — not at the top level. Same for `Page.captureScreenshot` (also requires `Page.enable` first).

## Acceptance checks

- The PDF is selectable/searchable and contains the expected text.
- Page count and page boundaries are intentional; no blank or nearly empty page remains.
- Tables retain their headers and each important row is readable.
- The title appears once, and no browser header/footer or local file path is printed.
- The Markdown source remains unchanged unless the content itself needs correction; layout-only fixes belong in CSS/HTML generation.
