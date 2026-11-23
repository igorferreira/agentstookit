---
name: openclaw-to-hermes-migration
description: Recreate or migrate OpenClaw agents into Hermes profiles, preserving specialist roles without blindly importing secrets or gateway settings.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [openclaw, hermes, migration, profiles, agents, kanban, gateway]
---

# OpenClaw to Hermes Migration

Use this skill when the user asks to analyze an OpenClaw config, recreate OpenClaw agents in Hermes, or migrate OpenClaw agent roles into Hermes profiles.

## Core workflow

1. Inspect the OpenClaw config first.
   - Default source: `~/.openclaw/openclaw.json`.
   - Look for `agents.defaults`, `agents.list`, model settings, workspaces, `subagents.allowAgents`, `groupChat.mentionPatterns`, tool permissions, gateway/channel config, and secrets placeholders.

2. Run a Hermes migration preview before applying anything broad.
   - Use: `hermes claw migrate --source /path/to/.openclaw --dry-run --preset full`.
   - Review conflicts, skipped items, and warnings.
   - If OpenClaw is running, expect a warning about gateway/bot-token contention.

3. If the user asked to create “the same agents”, prefer Hermes profiles.
   - Create one profile per OpenClaw agent id:
     - `hermes profile create <agent-id> --clone --description '<role description>'`
   - Use `--clone` so model/provider/tooling baseline follows the active Hermes profile.
   - Keep names identical to OpenClaw ids when valid, because Kanban routing and user muscle memory benefit from stable names.

4. Add a profile persona for each created agent.
   - Write `/home/<user>/.hermes/profiles/<profile>/SOUL.md` or the equivalent under the active `HERMES_HOME`.
   - The persona should summarize the specialist role, default language/tone, and safety boundaries.
   - For coding agents, include repository discipline: read relevant files first, make minimal changes, run relevant checks.

5. Validate creation.
   - `hermes profile list` should show each profile.
   - `hermes kanban assignees` should list the profiles as available assignees.
   - Read back at least one `SOUL.md` to confirm persona writing worked.

## Important boundaries

- Do not migrate secrets, bot tokens, Telegram settings, gateway settings, or provider keys unless the user explicitly asks.
- If OpenClaw is still running, do not assume the user wants a cutover. Ask/confirm whether they want coexistence or replacement when the next step is gateway activation.
- For coexistence, keep OpenClaw running and start Hermes only if Hermes uses a different bot token/channel. Validate with a non-secret fingerprint or Telegram `getMe`; never print tokens.
- Messaging platforms may allow only one active session per bot token. Stop OpenClaw only when the user explicitly wants Hermes to take over the same token/channel.
- Do not overwrite existing Hermes profiles blindly. If a profile already exists, treat it as a conflict and either skip or ask before replacing its persona/config.
- Avoid copying raw OpenClaw runtime state, sessions, auth-state files, or binary/sensitive data into Hermes profiles unless the user explicitly requests a full migration and accepts the risk.

## Gateway coexistence workflow

When the user wants both OpenClaw and Hermes running:

1. Check both gateway statuses before changing anything:
   - `hermes gateway status`
   - `systemctl --user is-active openclaw-gateway.service || true`
   - `pgrep -af 'openclaw|hermes.*gateway'`
2. Compare Telegram configuration without revealing secrets.
   - Inspect whether Hermes has `TELEGRAM_BOT_TOKEN` and whether OpenClaw has a Telegram bot token.
   - Print only presence/fingerprints or validate Hermes with Telegram `getMe` and report bot username/id.
3. Install/start Hermes gateway as a user service when safe:
   - `printf 'Y\nY\n' | hermes gateway install --force`
   - `hermes gateway status`
   - `hermes gateway list`
4. If `.env` has deprecated `MESSAGING_CWD`, move it to config:
   - `hermes config set terminal.cwd /path`
   - remove `MESSAGING_CWD=...` from `~/.hermes/.env`
   - restart Hermes gateway and verify logs.

## Profile-scoped permissions after migration

When a migrated specialist needs broad access to a domain directory, prefer profile-scoped config over global Hermes changes:

1. Set the specialist profile working directory:
   - `hermes --profile <profile> config set terminal.cwd /absolute/path`
2. If the user explicitly grants full operational permission, set approvals for that profile only:
   - `hermes --profile <profile> config set approvals.mode off`
   - Verify the YAML value is the string `'off'`; some config setters may serialize bare `off` as boolean `false`, so patch the profile `config.yaml` if needed.
3. If files from that directory must be delivered through the gateway, configure profile media allow dirs as a YAML list:
   - `gateway.media_delivery_allow_dirs:
     - /absolute/path`
   - Verify it is a list, not a JSON-looking string.
4. Reinforce filesystem owner permissions only when appropriate:
   - `chmod -R u+rwX /absolute/path`
5. Update the profile `SOUL.md` with the user-granted scope, including allowed operations and directory boundary.
6. Verify with a harmless create/read/delete test inside the target directory and remove the test file.

## Local documentation handoff

When a session configures multiple profiles/gateways/permissions, proactively offer or create local Markdown documentation if the user asks for persistence outside memory/skills.

- Use a dedicated docs directory such as `~/.hermes/docs` unless the user names another path.
- Split by context rather than writing one long log: summary, source config analysis, profiles created, gateway coexistence, profile permissions, operational commands, decisions/cautions.
- Add an `INDEX.md` with document descriptions and important paths.
- Do not include secrets, bot tokens, API keys, raw auth-state, or full runtime session logs.
- Keep concrete commands and verification results, because these docs are for future operations.
- See `references/openclaw-migration/usuario-2026-06-openclaw-hermes-coexistence.md` for a compact worked example of the docs structure and session-specific details.

## Example commands

```bash
hermes claw migrate --source /home/usuario/.openclaw --dry-run --preset full
hermes profile create python-senior --clone --description 'Engenheiro Python sênior para backend, automações, dados, testes, FastAPI e qualidade de código.'
hermes profile list
hermes kanban assignees
```

## Persona pattern

For each profile, keep `SOUL.md` short and operational:

```markdown
# Hermes Agent Persona

Você é o agente <name>. Atue como <specialist role>. Responda em português do Brasil por padrão, com objetividade e foco em execução. <Add domain-specific safety or workflow constraints.>
```

## Verification checklist

- Profiles exist in `hermes profile list`.
- Profiles appear in `hermes kanban assignees`.
- Each profile has a readable `SOUL.md`.
- No secrets or gateway tokens were copied unless explicitly requested.
- Final response states exactly what was created and what was intentionally not migrated.
