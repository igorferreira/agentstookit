# Extração real: workshop-ia.techleads.club/v3 (2026-09-04)

Caso de referência validado com Igor — React + Vite + lazy routes, landing promocional
de workshop ("Desenvolvimento Assistido por IA Avançado", Tech Leads club).

## Sinais de que é SPA shell

- `web_extract` → ~504 chars (só hero)
- HTML baixado: ~28 KB, texto visível <500 chars
- Bundles Vite carregados tardiamente por script inline perto de `</body>`

## Chunks que continham o conteúdo (nomes reais)

- `WorkshopSection-BhZxWxmw.js` — títulos/descrições dos 7 módulos
- `workshopSpeakers-C2HqD27q.js` — tabela `name:/role:` com 7 professores + bios longas
- `InstructorsSectionContent-uvmTqKNW.js` — materiais bônus (rules, frameworks, guia)
- `FAQSection-DuCvJieB.js` — perguntas frequentes
- `RealProblemSection-DmPaoEOM.js` — evidências de mercado (HBR, MIT)
- `V5-q9Kl2U71.js` — versão A/B da landing (assistentes, CTAs)

Campos estruturados recuperados verbatim: `NAME = Waldemar Neto / ROLE = Co-Founder @TechLeadsClub` etc.

## Sequência exata que funcionou

```bash
curl -sL URL -A "Mozilla/5.0 ... Chrome/126" -o ws.html
grep -o 'assets/[A-Za-z0-9_-]*\.js' ws.html index.js   # descobrir chunks
for c in WorkshopSection-BhZxWxmw workshopSpeakers-C2HqD27q ...; do
  curl -sL "https://site/assets/$c.js" -o "c_$c.js"
done
python3 extract_strings.py c_*.js > conteudo.txt
```

## O que NÃO funcionou (não repetir)

- **web_extract direto**: 504 chars — inútil para SPA shell
- **Wayback**: sem snapshot (`archived_snapshots: {}`) e mesmo com snapshot não renderizaria JS
- **Extrair strings de todos os chunks de uma vez**: misturou engine de carousel (Embla,
  ~20 KB de lixo `function wt(e,t,n,r)...`) com o conteúdo — filtrar por chunk
- **Regex com range literal `Ã-Ã¿`**: crash de `re.error: bad character range` — usar `\u00e0-\u00ff`
- **Primeiro filtro muito frouxo** (`[a-zá...]{3}\s`): 264 strings com 80% de ruído —
  apertar com stoplist de classes Tailwind + exigir stopwords pt-BR (de/para/com/que)

## Cross-check dos nomes próprios

Bios dos professores cruzadas com web_search (LinkedIn/GitHub/imprensa) para:
confirmar cargo atual, tempo de experiência, empresas anteriores. Ex.: Rogério Chaves
confirmado como Co-Founder LangWatch (Amsterdã, €1M funding, ex-Booking.com, open-source Apache 2.0).
