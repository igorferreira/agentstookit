# CV Generation Toolchain — Igor Ferreira

## Conversion pipeline (confirmed working on this machine)

```bash
# DOCX
pandoc "input.md" -o "output.docx"

# PDF (via wkhtmltopdf — preserves emoji and Markdown tables better than pandoc's LaTeX path)
pandoc "input.md" -o /tmp/cv.html --standalone
wkhtmltopdf \
  --enable-local-file-access \
  --margin-top 15mm --margin-bottom 15mm \
  --margin-left 18mm --margin-right 18mm \
  --page-size A4 --quiet \
  /tmp/cv.html "output.pdf"
```

Installed: `pandoc 3.1.3`, `wkhtmltopdf 0.12.6`, `LibreOffice 24.2`

## Folder structure (current)

```
~/MEGA/Documentos/cv/Igor_Ferreira/         ← historical versions (DO NOT modify)
  Fonte_Editavel/Curriculo_Igor_Ferreira_pt.md   ← full history since 2005
  ATUAL/CV_Igor_Ferreira_2026_ATS_Optimized_pt.md ← most recent ATS version

~/MEGA/Documentos/carreira/curriculos/      ← active working copy
  2026-07-23_CURRICULO-IGOR-FERREIRA-V2.*   ← base (MD + DOCX + PDF)
  arquiteto-ia/   ← COMPLETO + RESUMIDO × 3 formats
  java-senior/
  open-finance/
  seguros/
```

## Segmentation rules

| Area | Resume headline focus | Experience order | Competencies block 1st |
|---|---|---|---|
| Arquiteto IA | LLMs · Cloud · Java | HDI → Zup → SulAmérica | IA & Inovação |
| Java Sênior | Java · Spring · Tech Lead | HDI → Zup → SulAmérica | Backend & Java |
| Open Finance | BACEN · Camel · Kafka | Zup → HDI → SulAmérica | Open Finance & Regulatório |
| Seguros | Seguros · InsurTech · IA | HDI → SulAmérica → Zup | Seguros & InsurTech |

## Resumido vs Completo

- **Resumido (2 pages):** last 5 companies (HDI, Zup, SulAmérica, B2W + one more) with full bullets + block `### Experiência anterior em portais enterprise Oracle/BEA (2005–2013)` summarising 8 older companies in 3 lines.
- **Completo:** all 10 companies listed individually since Riopol (Dec/2005).

## LinkedIn scraping limitation

LinkedIn blocks unauthenticated full-profile access. The public view only shows:
- Name, headline, location, follower count
- Summary truncated (~150 chars)
- Services listed
- First entry of Experience section (company name only)
- Certifications list (visible without login in some views)
- Recommendations snippets

**Always check local CV files first** before trying to scrape LinkedIn.
