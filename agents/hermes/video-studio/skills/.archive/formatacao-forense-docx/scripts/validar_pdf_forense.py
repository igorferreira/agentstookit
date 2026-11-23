#!/usr/bin/env python3
"""Valida um PDF de peça forense: detecta páginas em branco e título de seção órfão.

Uso: python validar_pdf_forense.py <arquivo.pdf>

Percorre cada página (via pdfseparate para /tmp) e:
  - lista páginas VAZIAS (devem ser removidas com pdfunite das páginas com conteúdo);
  - marca página cuja ÚLTIMA linha parece um título órfão: começa com numeral romano
    (I., II., ..., X., XI.) e está no fim de página sem corpo na mesma página.

Requer: poppler-utils (pdfseparate, pdftotext).
"""
import subprocess, glob, re, os, sys, tempfile

pdf = sys.argv[1]
td = tempfile.mkdtemp(prefix="valpdf_")
subprocess.run(["pdfseparate", pdf, os.path.join(td, "p%d.pdf")], check=True)
files = sorted(glob.glob(os.path.join(td, "p*.pdf")))
print(f"Páginas: {len(files)}")
vazias, orfaos = [], []
for i, f in enumerate(files, 1):
    txt = subprocess.run(["pdftotext","-layout",f,"-"], capture_output=True, text=True).stdout
    body = [l.rstrip() for l in txt.split("\n") if l.strip() and not re.fullmatch(r"\d{1,2}", l.strip())]
    if not body:
        vazias.append(i); continue
    last = body[-1].strip()
    if re.match(r"^(I{1,3}|IV|V|VI{1,3}|VII{1,3}|VIII|IX|X|XI)\s*\.\s+[A-ZÀ-Ú]", last):
        orfaos.append((i, last[:60]))

print("PÁGINAS VAZIAS (remover):", vazias if vazias else "nenhuma")
print("TÍTULOS ÓRFÃOS:", orfaos if orfaos else "nenhum")
if vazias:
    print("Correção: pdfunite das páginas com conteúdo p/ um novo pdf.")