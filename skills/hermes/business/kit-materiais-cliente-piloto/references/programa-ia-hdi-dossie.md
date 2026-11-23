# Programa IA HDI — dossiê técnico completo (set/2026)

Projeto irmão do TimeAutomático, mas com identidade e público diferentes. Este arquivo preserva o estado da arte validado na construção do pacote, para reuso em futuras propostas/materiais HDI.

## Contexto

- Usuário é Arquiteto de Inovação e IA na HDI (via [EMPRESA]). Proposta: Programa de Desenvolvimento Assistido por IA para a engenharia HDI, estruturado em 4 pilares validados pelo mercado BR (Tech Leads club, iFood, PayPal, BHub, LangWatch).
- **Fluxo de aprovação**: primeiro Bruno Velasco (AI Principal do Grupo HDI, gatekeeper) → feedback → banca de arquitetos. NUNCA apresentar à banca antes do endosso do Bruno.
- Pasta canônica: `~/MEGA/Documentos/trabalho_projetos_ti/hdi/programa-ia-desenvolvimento/` (INDEX.md é o índice com log de fases). Repos: `~/projetos/hdi/Arquitetura/` (git, cópia física — NÃO symlink: git não segue symlink para fora do repo).

## Perfil Bruno Velasco (gatekeeper) — pontos-chave

- AI Principal do Grupo HDI (desde ~meados 2026); antes: SulAmérica → RD Saúde (mentor de 46 squads/400 devs) → Alest (Chief AI Officer, "enterprise vibe coding"). MIT xPRO.
- Agenda dele: "Inteligência Combinada" (humano+IA coagentes, IA amplia não substitui), Enterprise Vibe Coding, Agentes de IA, governança responsável, supervisão humana.
- **Estratégia de abordagem validada**: "sua agenda está certa — falta o método" (ele define o porquê, a proposta entrega o como). Posicionar o programa como COMPLEMENTO da governança que ele lidera, nunca substituição. Deck dele: 8 slides, estratégico.

## Os 4 pilares (vocabulário padrão emergente do mercado BR)

1. **SPEC** — Spec-Driven Development: spec aprovada antes do código; frameworks: SpecKit (GitHub, aderência ALTA), OpenSpec (comunidade, MÉDIA), TLC Spec Driven (ALTA)
2. **HARNESS** — plataforma ao redor do agente: codebase harness, loop engineering, gates no CI/CD, validação automática
3. **ARQUITETURA** — sistemas que agentes entendem; context engineering (progressive disclosure, compactação); legado <30min; anti-overengineering
4. **REVIEW** — mental alignment checklist (8 itens), revisão acelerada, atrofia de skill como risco de carreira

Evidências de mercado: HBR "AI-Generated Workslop"; MIT Media Lab 95% sem ROI; "IA sem estratégia de contexto é refatoração sem testes".

## Materiais do pacote (estrutura reutilizável)

- PROPOSTA formal (resumo, 3 ondas/90 dias, métricas, riscos, budget, alinhamento estratégia HDI 22.94.30, próximos passos)
- 10 fichas temáticas (formato fixo: Conceito → Prática do mercado → Aplicação HDI → Riscos → Referências, com tabelas de risco/mitigação)
- 3 decks: Bruno (8), Banca (10), Geral (14) — python-pptx, identidade HDI: fundo branco, azul #0033A0, laranja #FF6600, Arial, sóbrio
- Suporte: CHECKLIST-SPEC-READY (1 pág, revisão de arquiteto 🔒), METRICAS-ADOCACAO, GLOSSARIO-IA-PTBR, comparativo-sdd.xlsx (template)
- Plano corretivo em fases F0-F7 com checkboxes (modelo para outros projetos: cada fase com entregável verificável, commit+sync por fase)

## Métricas do programa (consolidadas — batem em todos os artefatos)

Retrabalho pós-geração −30% · tempo de review −40% · legado <1h · 80% features com spec aprovada antes do código · eNPS IA ≥+20. Budget piloto 90 dias: R$ 8.500-12.500 (licenças 10 devs R$4.500 + workshop R$4-8k).

## Lições da revisão profunda (v1.1)

- Números derivados (budget) precisam bater em TODOS os artefatos: grep por valores em .md + scripts geradores + PDFs.
- Validar referências internas programaticamente (regex sobre `` `arquivo.ext` `` resolvendo caminho relativo a partir da pasta do arquivo) — 12 quebras encontradas em 18 arquivos.
- Ortografia: aspell sem root falha; usar `uv run --with pyspellchecker` (lang pt) com triagem (checador reprova termos técnicos válidos; filtrar palavras minúsculas plausíveis-pt antes de corrigir — 2 erros reais em ~200 suspeitas).
- Workshop TLC (12-13/09/2026): Usuário participará; absorver material em v1.2 (fase F3 do plano). Detalhes do evento em `references/workshop-tlc-ia-avancado-2026.md`.
