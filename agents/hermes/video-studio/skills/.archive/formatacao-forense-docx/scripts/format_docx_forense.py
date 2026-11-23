#!/usr/bin/env python3
"""Aplica padrão forense/ABNT a um DOCX de peça processual e (opcional) gera PDF fiel.

Uso:
    python format_docx_forense.py <entrada.docx> <saida.docx> [--pdf-dir DIR]

Aplica: página A4 retrato, margens sup3/esq3/dir2/inf2cm, fonte Arial (ascii/hAnsi/cs/eastAsia)
em todas as runs + estilo Normal, cor preta 000000 em cada run, remove highlight/shading,
espaçamento 1,5, corpo justificado, títulos centralizados, recuo 1ª linha 1,25cm no corpo.
Se --pdf-dir dado, roda LibreOffice para gerar o PDF fiel naquele diretório.

Requer: python-docx (ex.: `uv venv .venv && uv pip install python-docx`). LibreOffice p/ PDF.
"""
import sys, os, subprocess
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn

SRC, DST = sys.argv[1], sys.argv[2]
pdf_dir = None
if "--pdf-dir" in sys.argv:
    pdf_dir = sys.argv[sys.argv.index("--pdf-dir") + 1]

doc = Document(SRC)

# 1) Página A4 + margens ABNT
for section in doc.sections:
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(3); section.bottom_margin = Cm(2)
    section.left_margin = Cm(3); section.right_margin = Cm(2)
    section.header_distance = Cm(1.5); section.footer_distance = Cm(1.5)

# 2) Estilo Normal -> Arial preto
n = doc.styles["Normal"]
n.font.name = "Arial"; n.font.size = Pt(12); n.font.color.rgb = RGBColor(0,0,0)
rpr = n.element.get_or_add_rPr()
for t in list(rpr.findall(qn("w:highlight"))): rpr.remove(t)
npf = n.paragraph_format
npf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
npf.space_before = Pt(0); npf.space_after = Pt(6)

def set_arial(el):
    rpr = el.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = rpr.makeelement(qn("w:rFonts"), {}); rpr.append(rf)
    for a in ("w:ascii","w:hAnsi","w:cs","w:eastAsia"):
        rf.set(qn(a),"Arial")

def fmt_par(par, heading):
    pf = par.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    pf.space_before = Pt(0); pf.space_after = Pt(6)
    pf.alignment = WD_ALIGN_PARAGRAPH.CENTER if heading else WD_ALIGN_PARAGRAPH.JUSTIFY
    for run in par.runs:
        run.font.name = "Arial"; run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0,0,0)
        set_arial(run._element)
        rr = run._element.get_or_add_rPr()
        for t in list(rr.findall(qn("w:highlight"))): rr.remove(t)
    if not heading and par.text.strip():
        up = par.text.strip()[:40].upper()
        if len(par.text.strip()) > 60 and not up.startswith(("TITULAR","CPF","PROCESSO","JUÍZO",
            "AUTOR","PROTOCOLO","DATA","VALOR","INSTITUIÇÃO","ISPB","AGÊNCIA","CONTA","CHAVE",
            "INDICAÇÃO","ALCANÇADA","NUBANK","BANCO","EXCELENTÍSSIMO")):
            pf.first_line_indent = Cm(1.25)

for par in doc.paragraphs:
    fmt_par(par, par.style.name.startswith("Heading"))

for t in doc.tables:
    for row in t.rows:
        for cell in row.cells:
            for par in cell.paragraphs:
                fmt_par(par, False)

doc.save(DST)
print("DOCX formatado ->", DST)

if pdf_dir:
    os.makedirs(pdf_dir, exist_ok=True)
    r = subprocess.run(["soffice","--headless","--convert-to","pdf","--outdir",pdf_dir,DST],
                       capture_output=True, text=True)
    print("PDF:", "ok" if r.returncode == 0 else r.stderr[-200:])
    pdf = os.path.join(pdf_dir, os.path.splitext(os.path.basename(DST))[0] + ".pdf")
    if os.path.exists(pdf):
        print("PDF gerado em", pdf)