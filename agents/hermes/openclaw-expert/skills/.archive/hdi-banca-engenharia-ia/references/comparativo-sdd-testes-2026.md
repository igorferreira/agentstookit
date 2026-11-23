# Comparativo SDD — Testes Próprios Validados (04/09/2026)

Resultado real de rodar a MESMA feature nos 3 frameworks (GET /apolices/{numero}/parcelas,
FastAPI + pytest, sandbox `~/sandbox-sdd/`, dados sintéticos estilo InsureMO).
Todos: 6/6 requisitos cobertos, 6/6 testes passando, zero retrabalho de código.

## Comandos de instalação (validados)

- **SpecKit v1.0.4** (github/spec-kit): `uv tool install specify-cli` →
  `specify init <proj> --integration claude --ignore-agent-tools`
  (⚠️ flag é `--integration`, NÃO `--ai`). Cria `.specify/` + skills
  `speckit-specify/plan/tasks/implement` e templates em `.specify/templates/`.
- **OpenSpec v1.12.0** (Fission-AI/OpenSpec): `npm install -g @fission-ai/openspec` →
  `openspec init <dir> --tools claude`. Fluxo: `openspec new change <nome>` →
  `openspec instructions proposal|specs|design|tasks --change <n>` (imprime as instruções
  que o agente deve seguir) → `openspec validate <change>` (⚠️ sem `--change`; o nome é posicional).
- **TLC Spec Driven v3.3.0** (tech-leads-club/agent-skills): sem CLI — é uma skill Claude.
  Copiar `packages/skills-catalog/skills/(development)/tlc-spec-driven/` para
  `.claude/skills/`. Validadores determinísticos em `scripts/`:
  `validate_spec.py`, `validate_tasks.py`, `check_commit.py`, `validate_state.py`.

## Diferenciais observados

- **SpecKit (9/10, ADOPT p/ governança):** template rígido força user stories independentes
  P1-P3 + acceptance scenarios; constitution de projeto pronta p/ normas ADA.
- **OpenSpec (8/10, TRIAL):** único com **validador de delta specs** — exige frase SHALL +
  `#### Scenario:` por requirement; pegou 2 requirements malformados antes de qualquer código.
  Mudanças são "changes" (proposal → design → tasks → archive).
- **TLC (9/10, ADOPT p/ squads piloto):** gate determinístico em Python — `validate_spec.py`
  **reprovou** a spec na 1ª execução (faltava `## Requirement Traceability` com IDs `PARC-01..`).
  Notação EARS (WHEN/THEN, IF/THEN, WHILE, SHALL), auto-sizing de cerimônia
  (small/medium/large/complex), Verifier independente (author ≠ verifier).

## Métricas do teste

| Métrica | SpecKit | OpenSpec | TLC |
|---|---|---|---|
| Correções no artefato de spec | 0 | 2 (validador) | 1 (validador) |
| Etapas até 1ª spec | 4 | 5 | 3 |

## Veredito

Onda 1 HDI = **TLC Spec Driven** nos squads piloto (rigor sem burocracia);
**SpecKit** como referência de governança enterprise (normas do ADA);
**OpenSpec** em TRIAL (validador de deltas é candidato a incorporar ao harness).

## Artefatos

Planilha preenchida: `~/MEGA/Documentos/trabalho_projetos_ti/hdi/programa-ia-desenvolvimento/MATERIAIS-SUPORTE/comparativo-sdd.xlsx`
Evidências brutas: mesmo pacote, `testes-sdd/` (sandbox original em `~/sandbox-sdd/`).
