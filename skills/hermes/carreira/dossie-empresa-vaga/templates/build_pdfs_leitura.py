#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# TEMPLATE VALIDADO (Zenvia, nov/2026): gera PDFs de leitura com capa + outline (weasyprint).
# Para outra empresa/entrevista, copie para ~/.hermes/cache/scratch/ e adapte:
#   Z        -> pasta dos MDs de origem (oportunidades/<Empresa>/)
#   OUT      -> pasta destino dos PDFs (padrao e -CELULAR)
#   TOPOS    -> dict {nome_do_MD: (bloco_topo_html, adendo_html)} — o bloco_topo usa COMO_LER + bloco([...pontos...])
#   TPL      -> texto do cabecalho da capa (empresa, data, hora da entrevista)
# Rodar: python3 build_pdfs_leitura.py            (versao padrao 10pt)
#        python3 build_pdfs_leitura.py celular   (versao 13.5pt, pasta -CELULAR)
# IMPORTANTE: titulos da capa sao divs (.t-topo), NUNCA h2/h3 — h* vira bookmark do outline.
# Renderizador: use o binario que tiver weasyprint (aqui /usr/local/bin/python3.12); fallback = pandoc + chrome headless.
import subprocess, os, sys, tempfile
TMPDIR = tempfile.mkdtemp()

Z = os.path.expanduser("~/MEGA/Documentos/oportunidades/Zenvia")
CELULAR = len(sys.argv) > 1 and sys.argv[1] == "celular"
if CELULAR:
    OUT = os.path.expanduser("~/MEGA/Comprovantes/_Analises/PDF-DOSSIES-ZENVIA-CELULAR")
else:
    OUT = os.path.expanduser("~/MEGA/Comprovantes/_Analises/PDF-DOSSIES-ZENVIA")
os.makedirs(OUT, exist_ok=True)

CSS = """
@page { size: A4; margin: 16mm 14mm 18mm 14mm; }
* { box-sizing: border-box; }
body { font-family: 'DejaVu Sans', sans-serif; font-size: 10pt; line-height: 1.55; color: #1c2833; }
h1 { font-size: 16pt; color: #1a5276; border-bottom: 3px solid #1a5276; padding-bottom: 5px; margin: 4px 0 10px; page-break-after: avoid; }
h2 { font-size: 12.5pt; color: #1a5276; border-bottom: 1px solid #a9cce3; padding-bottom: 3px; margin: 18px 0 8px; page-break-after: avoid; }
h3 { font-size: 11pt; color: #21618c; margin: 12px 0 6px; page-break-after: avoid; }
p { margin: 5px 0; }
strong { color: #0b2e4f; }
ul, ol { margin: 5px 0 9px; padding-left: 20px; }
li { margin-bottom: 2.5px; }
table { width: 100%; border-collapse: collapse; table-layout: fixed; font-size: 8.7pt; margin: 10px 0; page-break-inside: avoid; }
th, td { border: 1px solid #aab7b8; padding: 4px 6px; overflow-wrap: anywhere; word-break: break-word; vertical-align: top; text-align: left; }
th { background: #eaf2f8; color: #1a5276; }
tr { page-break-inside: avoid; }
blockquote { background: #fdf6e3; border-left: 4px solid #d4ac0d; margin: 8px 0; padding: 7px 12px; page-break-inside: avoid; }
code { font-size: 8.5pt; overflow-wrap: anywhere; }
a { color: #1a5276; overflow-wrap: anywhere; word-break: break-all; }
hr { border: none; border-top: 1px solid #d5dbdb; margin: 12px 0; }
img { max-width: 100%; }
.topo { background: #eaf2f8; border: 2px solid #1a5276; border-radius: 8px; padding: 10px 14px 8px; margin-bottom: 14px; page-break-inside: avoid; }
.topo h2 { margin: 0 0 6px; border: none; font-size: 13pt; color: #154360; }
.topo h3 { margin: 8px 0 3px; font-size: 10.5pt; color: #1a5276; }
.topo ul { margin: 3px 0 5px; }
.adendo { background: #e8f8f5; border: 1.5px solid #117a65; border-radius: 8px; padding: 10px 14px; margin-top: 16px; page-break-inside: avoid; }
.adendo h2 { margin: 0 0 6px; border: none; color: #0e6655; }
.rodape { margin-top: 14px; font-size: 8pt; color: #5d6d7e; border-top: 1px solid #d5dbdb; padding-top: 6px; }
.capa { page-break-after: always; }
.capa-rotulo { color: #1a5276; font-weight: bold; letter-spacing: 2px; font-size: 9.5pt; text-transform: uppercase; margin-top: 26mm; }
.capa-titulo { font-size: 22pt; font-weight: bold; color: #154360; margin: 8px 0 6px; line-height: 1.25; }
.capa-sub { color: #5d6d7e; font-size: 10.5pt; margin-bottom: 20px; border-bottom: 2.5px solid #1a5276; padding-bottom: 12px; }
.capa .virar { margin-top: 22px; font-size: 10pt; color: #154360; font-weight: bold; }
.t-topo { font-size: 12pt; font-weight: bold; color: #154360; margin: 10px 0 3px; }
h1 { bookmark-level: 1; }
h2 { bookmark-level: 2; }
h3 { bookmark-level: 3; }
"""

if CELULAR:
    for a, b in [
        ("font-size: 10pt; line-height: 1.55", "font-size: 13.5pt; line-height: 1.62"),
        ("h1 { font-size: 16pt", "h1 { font-size: 19.5pt"),
        ("h2 { font-size: 12.5pt", "h2 { font-size: 15.5pt"),
        ("h3 { font-size: 11pt", "h3 { font-size: 13.5pt"),
        (".t-topo { font-size: 12pt", ".t-topo { font-size: 14.5pt"),
        ("table-layout: fixed; font-size: 8.7pt", "table-layout: fixed; font-size: 10.5pt"),
        ("th, td { border: 1px solid #aab7b8; padding: 4px 6px", "th, td { border: 1px solid #aab7b8; padding: 6px 8px"),
        ("code { font-size: 8.5pt", "code { font-size: 10.5pt"),
        (".rodape { margin-top: 14px; font-size: 8pt", ".rodape { margin-top: 14px; font-size: 9.5pt"),
        (".capa-titulo { font-size: 22pt", ".capa-titulo { font-size: 27pt"),
        (".capa-rotulo { color: #1a5276; font-weight: bold; letter-spacing: 2px; font-size: 9.5pt", ".capa-rotulo { color: #1a5276; font-weight: bold; letter-spacing: 2px; font-size: 11pt"),
        (".capa-sub { color: #5d6d7e; font-size: 10.5pt", ".capa-sub { color: #5d6d7e; font-size: 12.5pt"),
        (".capa .virar { margin-top: 22px; font-size: 10pt", ".capa .virar { margin-top: 22px; font-size: 12.5pt"),
    ]:
        assert a in CSS, "NAO ACHOU: " + a
        CSS = CSS.replace(a, b)

TPL = """<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">
<title>{title}</title><style>{css}</style></head><body>
<div class="capa">
<div class="capa-rotulo">DOSSIÊ DE ENTREVISTA · ZENVIA · SEGUNDA 23/11 · 10:30</div>
<div class="capa-titulo">{title}</div>
<div class="capa-sub">Edição de leitura — capa + instruções de leitura + pontos-chave. O documento começa na página 2; use o painel de marcadores do seu leitor de PDF para navegar pelos títulos.</div>
{topo}
<div class="virar">▶ Vire a página — o documento começa agora</div>
</div>
{body}
{adendo}
<div class="rodape">Gerado em 21/11/2026 — Dossiês Entrevista Zenvia (23/11 10:30) · MEGA/_Analises/PDF-DOSSIES-ZENVIA</div>
</body></html>"""

COMO_LER = """<div class="t-topo">📖 Como ler este documento (3 passos)</div>
<ul>
<li><strong>1ª leitura (5 min):</strong> só este topo — a caixa e os ⭐. Você já fica preparado por cima.</li>
<li><strong>2ª leitura (completa):</strong> o documento inteiro, sublinhando no máximo 3 frases por seção.</li>
<li><strong>3ª leitura (véspera):</strong> só o topo + as frases que você sublinhou. Domingo à noite é o momento.</li>
</ul>
<div class="t-topo">🧠 Dicas de memorização (o que funciona)</div>
<ul>
<li><strong>Números viram história:</strong> não decore “R$ 988” — decore “o Alelo Tudo de R$988 paga meu Home Equity”.</li>
<li><strong>Repita em voz alta:</strong> conteúdo dito em voz alta fica ~2× mais tempo na cabeça que o lido em silêncio.</li>
<li><strong>3 palavras por seção:</strong> feche cada seção anotando 3 palavras-chave no caderno — é seu “índice de bolso”.</li>
<li><strong>Não decore o texto, decore a estrutura:</strong> sabe os 3 grandes temas (números / empresa / entrevistador) e o resto flui.</li>
<li><strong>Teste real:</strong> 5 min de perguntas em voz alta valem mais que 20 min de releitura em silêncio.</li>
</ul>"""


def bloco(pontos):
    lis = "".join("<li>" + p + "</li>" for p in pontos)
    return ("<div class=\"t-topo\">⭐ Pontos mais importantes (se fechar só isso, você tá pronto)</div><ul>" + lis + "</ul>")

# EXEMPLO de entrada (um por documento do pacote):
TOPOS = {
"20261117_DOSSIE-ZENVIA": (COMO_LER + bloco([
 "<strong>Ponto 1 mais importante</strong> — frase curta que ele precisa lembrar.",
 "<strong>Ponto 2</strong> — número exato com fonte.",
 "<strong>Ponto 3</strong> — frase pronta para usar na conversa.",
]), """<h2>Adendo — mais informações</h2>
<ul>
<li>Contexto extra no fim do documento (adendo verde).</li>
</ul>"""),
}

DOCS = list(TOPOS.keys())

def pandoc_md_to_html(path):
    r = subprocess.run(["pandoc", "-f", "markdown+emoji", "-t", "html", path],
                       capture_output=True, text=True, check=True)
    return r.stdout

ok, fail = [], []
for name in DOCS:
    md = os.path.join(Z, name + ".md")
    if not os.path.exists(md):
        fail.append((name, "FALTA"))
        continue
    body = pandoc_md_to_html(md)
    topo, adendo = TOPOS[name]
    title = name.replace("20261121_", "").replace("20261117_", "").replace("-", " ")
    html_full = TPL.format(title=title, css=CSS, topo=topo, body=body, adendo=adendo)
    html_path = os.path.join(TMPDIR, name + ".html")
    pdf_path = os.path.join(OUT, name + ".pdf")
    with open(html_path, "w") as f:
        f.write(html_full)
    r = subprocess.run(["/usr/local/bin/python3.12", "-m", "weasyprint", html_path, pdf_path],
                       capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        print("WEASY ERR", name, r.stderr[-300:])
    if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 20000:
        ok.append((name, os.path.getsize(pdf_path)))
    else:
        fail.append((name, "erro"))

for n, s in ok:
    print("OK  ", n, s)
for n, e in fail:
    print("FAIL", n, e)
