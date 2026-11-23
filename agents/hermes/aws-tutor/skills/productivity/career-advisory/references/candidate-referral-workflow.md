# Candidate Referral Workflow

When Igor asks to refer a candidate to a company (especially his own employer Noorden):

## 4-part email structure

1. **Perfil do candidato** — data, diferenciais, trajetória (table format)
2. **Aderência às vagas** — honest fit analysis per published position, with ✅/❌/🔧 markers
3. **Onde entrega valor real** — even if no published position matches perfectly, map to company's actual service areas
4. **Disponibilidade e condições** — availability, location, contract model

## Critical rules

- **Make a FORMAL explicit indication** for a specific position. Don't just analyze — say "Estou indicando Fulano para a vaga de X." Igor corrected: "faltou vc indicar a vaga para o perfil dele diretamente."
- **CC the candidate** on the email. Igor: "nao esquece enviar para o guilherme em copia."
- **Be honest about fit gaps** but highlight transferable skills. "O gap é ferramental, não conceitual."
- **Send follow-up in the same thread** if the first email was too analytical and not direct enough.
- **Attach CV as PDF** — generate via wkhtmltopdf from markdown source.
- **Use the company's actual careers portal** to find published positions. For Noorden: noorden.pandape.infojobs.com.br.

## When no published position matches

- Check the company's declared service areas on their website
- Map candidate skills to those areas
- Offer the candidate for unlisted positions: "Se tiver cliente precisando de X, ele entrega de imediato."
- Still make a formal indication for the closest matching area

## PDF generation

```bash
# Convert CV markdown to HTML, then PDF
wkhtmltopdf --encoding UTF-8 input.html output.pdf
```

## Email delivery

Use himalaya CLI with MML attachments:
```
<#multipart type=related>
<#part type=application/pdf filename="/absolute/path/to/cv.pdf" name="Candidate-Name-CV.pdf"><#/part>
<#/multipart>
```
