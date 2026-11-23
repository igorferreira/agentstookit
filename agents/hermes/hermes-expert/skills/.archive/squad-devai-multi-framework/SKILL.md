---
name: squad-devai-multi-framework
description: Use when creating or porting an AI dev squad to a framework.
version: 1.0.0
---

# Squad DevAI Multi-Framework — Porting & Operating AI Dev Squads

Canonical repo: `/home/igorferreira/projetos/hdi/devai` (private GitHub `igorferreira/devai`).

## When to use
- User asks to create a dev squad of AI agents for a new framework/tool.
- User asks to "do the same as X for Y" where X is an existing framework guide.

## Core principle: one agnostic catalog, N framework adapters
The 7 role prompts live ONCE in `prompts/squad/<NN-role>/prompt-*-hdi.md`. Each framework gets only a thin **adapter guide** (`guia-criacao-squad-<framework>.md`) that maps roles to that tool's persona mechanism. NEVER duplicate role prompts per framework.

## Framework adapter matrix

| Framework | Context/root file | Per-agent persona | Invocation |
|---|---|---|---|
| Claude Code | `.claude/CLAUDE.md` | prompt file injected via CLI | `claude "<instruction>"` |
| Hermes Agent | `~/.hermes/profiles/<name>/SOUL.md` + `USER.md` | profile isolation | `hermes --profile <name> "<cmd>"`; parallel via `delegate_task(role=leaf)` |
| OpenClaw | `~/.openclaw/agents/<name>/SOUL.md` + `AGENTS.md`, registered in `openclaw.json` | workspace dir + memory dir | `openclaw agent --name <name> "<cmd>"` |
| Codex CLI | `.codex/AGENTS.md` | prompt file injected via CLI | `codex "<instruction>"` |
| Antigravity | `.antigravity/rules.md` | persona block in task prompt | prompt/task injection |

## Steps to add a new framework
1. `mkdir -p prompts/<framework>/{system-prompts,workspaces,custom-instructions}`.
2. Write `guia-criacao-squad-<framework>.md`: root-context file template, a provisioning shell script (loop over the 7 `prompts/squad/*` files copying them to the framework's persona path), per-role invocation commands, and the comparison-matrix row.
3. Add the folder + one-line description to the README tree and commit/push with conventional commits.

## Pitfalls
- **Do not invent framework config formats.** If the target's config schema is unknown (e.g., exact `openclaw.json` agent keys), write the adapter as a best-effort template and say so in the doc rather than presenting guessed keys as verified.
- **Preserve existing files**: when asked for a consolidated artifact (e.g., `PROMPT-MESTRE-SQUAD-COMPLETO.md`), keep the modular per-role files untouched — user explicitly requires both forms.
- **GitHub collaborator handles**: users quote logins like `someone.github`. Resolve the real login via `gh api search/users?q=<fragment>` before inviting; the PUT returns 404 for nonexistent users (misleading). Invitation is pending until accepted.
