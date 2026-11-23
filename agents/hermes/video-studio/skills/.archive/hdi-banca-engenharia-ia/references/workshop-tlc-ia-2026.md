# Fonte Externa Validada: Workshop TLC — Desenvolvimento Assistido por IA (set/2026)

Pesquisa e extração validadas em 04/09/2026. Fonte da proposta de Programa de IA da HDI.

## O evento

- Workshop "Desenvolvimento Assistido por IA Avançado" — Tech Leads club
- 12-13/set/2026, 10h-17h, Zoom, 10h/2 dias/7 módulos, R$37, hands-on
- Público: devs sêniores/Tech Leads/Staff/EMs em codebases 100k+ linhas
- Landing: https://workshop-ia.techleads.club/v3 (SPA React — extração via bundle disassembly, ver abaixo)

## Os 4 pilares (vocabulário de mercado a usar em materiais HDI)

1. **SPEC** — Spec-Driven Development: desenhar antes de gerar
2. **HARNESS** — plataforma ao redor do agente: codebase harness, loop engineering, validação automática
3. **ARQUITETURA** — sistemas que agentes entendem; legado em <30min via context engineering
4. **REVIEW** — mental alignment checklist; julgamento humano; atrofia de skill como risco

## Os 7 módulos

Dia 1 (IA-first): IA First · Spec-Driven Development · Harness
Dia 2 (sistemas/arquitetura): O novo Dev · Software Architecture in the age of AI · Workflows pessoais e memory layer · Construção hands-on

## Professores (bios verificadas)

- **William Calderipe** — Co-Founder & CTO TLC, ex-Atlassian (Clojure/TS/AWS) e ThoughtWorks, baseado em Paris. LinkedIn: wcalderipe
- **Felipe Adamoli** — Co-Founder TLC, ex-sócio nav9 (+140 projetos, SBT/Caju)
- **Felipe Rodrigues** — Staff AI Engineer BHub, Líder Grupo de Pesquisa IA TLC; criou Agent Skills (registry de skills p/ agentes de código) e linkedin-mcpserver; Cursor Ambassador, AWS Community Builder
- **Rogério Chaves** — Co-Founder LangWatch (LLMOps/evals/simulação de agentes; €1M funding; open-source Apache 2.0; ex-Booking.com). GitHub: rogeriochaves
- **Julio Santos** — Staff Engineer, iFood
- **William Fernandes** — Senior SWE PayPal Risk & Fraud; 20+ anos; testa SpecKit, OpenSpec e TLC Spec Driven na ponta

## Evidências de mercado citáveis

- HBR: "AI-Generated 'Workslop' Is Destroying Productivity"
- MIT Media Lab: 95% das organizações sem ROI mensurável em IA
- "IA em produção sem estratégia de contexto é como refatoração sem testes"

## Materiais bônus (entregáveis do workshop)

Rules & Skills (Context Engineering Rules, Code Review Skills, Architecture Analysis Skills, Refactoring Rules) · Frameworks Plug-and-Play (SDD template, RPI, PRD, Design Doc) · Guia de Adoção de IA no Time (estratégia, métricas, gestão de mudança) · Certificado

## Dossiê local completo

`~/projetos/hdi/Arquitetura/2026-09-04_programa-ia-desenvolvimento/2026-09-04_WORKSHOP-TLC-IA-AVANCADO-DOSSI-COMPLETO.md`

## Técnica de extração (SPA React/Vite landing pages)

Landing pages React frequentemente retornam shell HTML quase vazio. Método validado:

1. Baixar o HTML e ler o FIM do arquivo: script inline com a lista de chunks `assets/<nome>-<hash>.js` (modulepreload). Nomes de chunks vazam a estrutura da página (ex: `workshopSpeakers-*.js`, `InstructorsSectionContent-*.js`).
2. Baixar os chunks (curl direto em /assets/...).
3. Extrair texto com Python: regex de strings duplas entre aspas → `unicode_escape` → filtrar por linguagem natural (padrão palavra-espaço-palavra com stopwords pt/en) descartando classes Tailwind (`flex|grid|absolute|text-\[|px-|py-|w-\d|h-\d`), imports e URLs.
4. Dados estruturados: `re.finditer(r'(name|title|role)\s*:\s*"..."')` revela bios/professores.
5. Cuidado: código do embla-carousel e Radix UI polui os chunks — filtrar agressivamente; conteúdo real costuma estar em chunks lazy referenciados dentro de outros chunks.
