---
name: hermes-multiagent-squad-builder
description: "Build a Hermes multi-agent squad: orchestrator + skills."
metadata:
  version: 0.1.0
---

# Hermes Multi-Agent Squad Builder

## When to use

Igor asks for a "banca" / "equipe multiagente" / "síndico virtual"-style system: one
orchestrator plus several cooperating specialist sub-agents for a domain (condomínio,
saúde, engenharia, jurídico, vendas, etc.). Distinguish from a single skill request:
this pattern is for MULTIPLE cooperating specialist roles behind one orchestrator, not
one narrow capability.

Existing examples of this pattern already built in this install — read one as a live
reference before starting a new one: `agente-orquestrador-sindico-virtual` + `agente-*`
(condomínio, Condomínio Residencial), `hdi-banca-engenharia-ia` (engenharia HDI).

## Architecture pattern (validated 04/09/2026 building the Síndico Virtual squad)

1. **Inventory first, always.** Before creating anything: `hermes profile list`,
   `find ~/.hermes/skills -name SKILL.md`, check `config.yaml` sections (delegation,
   kanban, model), `hermes kanban boards list`, `hermes cron list`. Never assume a
   resource (kanban, delegation depth, MCP) exists — verify live.
2. **Backup before touching anything:** copy `config.yaml` + profile list + skills-dir
   listing to `~/.hermes/backups/<project>-<timestamp>/` before the first write.
3. **One orchestrator profile** (`hermes profile create <slug>`), NOT one profile per
   specialist. The orchestrator's `SOUL.md` carries the persona + the delegation
   protocol: when to convene which specialists, prioritization scheme, source-of-truth
   hierarchy, and hard security limits (what the squad may never do autonomously —
   payments, contracts, firing people, legal representation, etc.).
4. **Specialists = skills, not profiles.** Put each specialist at
   `~/.hermes/skills/<category>/agente-<nome>/SKILL.md` — the SHARED skills dir, not
   inside the orchestrator profile's own `skills/`. Writing a skill inside another
   profile's private directory is blocked by a cross-profile guard. This also keeps
   ~20 specialists cheap (skills) instead of ~20 expensive profiles.
5. **Model config for the new profile:** `hermes config set model.default <model>
   --profile <slug>` and `model.provider` the same way — match whatever the user's
   other working profiles already use (read 2-3 existing profiles' `config.yaml`
   `model:` block first; don't guess a provider).
6. **Task model / durable state:** a dedicated Kanban board
   (`hermes kanban boards create <slug>`) doubles as the structured-task tracker
   (ID, status, assignee) most "banca" specs ask for in prose — don't hand-roll a
   second task system when Kanban already covers it.
7. **Recurring review:** one cron job for periodic housekeeping (e.g. daily
   critical-pending review). `hermes cron create "<schedule>" "<prompt>" --profile
   <slug> --workdir <profile dir> --skill <a> --skill <b> ...` — `schedule` and
   `prompt` are POSITIONAL arguments, not flags; `--skill` is repeatable.
8. **Memory areas:** one `.md` per data area under `<profile>/memoria/` (profile-scoped,
   not the shared skills dir), with an `INDEX.md` pointer. Never mix permanent facts
   with session-temporary notes in the same file.

## Testing — mandatory before declaring the squad "done"

- Smoke test: `hermes --profile <slug> chat -q "<identity question>"` — confirm
  persona + team awareness in the reply.
- **Multi-agent delegation test is not optional.** Use `delegate_task` with a `tasks`
  batch (2-3 parallel), one per specialist role, each given ONLY that role's context
  plus its hard limits (e.g. "never move money," "must route to a human professional
  for X"). Read the results and verify each agent actually respected its stated
  limits — didn't invent data, didn't take an irreversible action, flagged the right
  escalation. This is the cheapest way to catch a specialist skill that's too
  permissive before a real user relies on it.

## Pitfalls

### `config.yaml` cannot be edited directly
Direct file writes to `~/.hermes/config.yaml` are refused ("Agent cannot modify
security-sensitive configuration"). Always go through `hermes config set <key>
<value>` / `hermes config unset <key>`. Get the **nesting right** — e.g. model
settings live under top-level `model:` (`model.default`, `model.provider`), most
timeouts live under `agent:` (`agent.gateway_timeout`, `agent.clarify_timeout`), not
under `gateway:`/`terminal:` even though those surface names look tempting. A wrong
prefix silently creates an unrecognized top-level key — `hermes config set` warns but
still writes it. Always `grep -n <key>` the file after setting to confirm it landed
in the right nested block, and `hermes config unset <wrong.key>` immediately if it
didn't.

### Language leakage in generated documents (pt-BR or any fixed target language)
When a task requires committing a document permanently in Portuguese and the
underlying model intermittently answers in a different language, **do not trust a
"regenerate the whole file" retry loop** — it can repeat the same leak multiple times,
even across delegated sub-agent rewrites of the same file.

What actually works:
1. **Verify before declaring done:** `grep -inE "\b(es un|del sistema|deberá|será|
   reglamento|proveedor)\b" <file>` (adjust the wordlist to the leaking language) —
   zero hits required before delivering.
2. If leakage is found, don't re-prompt the same way — rewrite the offending
   sections manually, paragraph by paragraph, with direct attention to each sentence.
3. If leakage keeps recurring across unrelated tasks in the same session, it's a
   **model-level** issue, not a prompt issue — switch the active model
   (`hermes config set model.default <model>`) instead of continuing to patch
   symptoms. Observed 04/09/2026: `deepseek/deepseek-v4-flash-0731` intermittently
   answered in Spanish despite explicit pt-BR instructions repeated across many
   turns; switching to `qwen/qwen3.7-flash` resolved it for this user.
4. File/document **naming** must also stay in the target language — a
   literal-sounding borrowed word from the source language (e.g. Spanish "creación"
   wrongly rendered as "creacao" instead of the correct Portuguese "criação" /
   accent-free "criacao") is a distinct, easy-to-miss leakage that survives even
   after the document body itself is clean. Check file names, not just file content.

## Composes with

- `business-brainstorm` — if the "squad" being built is actually a monetizable
  service offering (not just an internal tool), pressure-test the business case there
  before or alongside the build.
