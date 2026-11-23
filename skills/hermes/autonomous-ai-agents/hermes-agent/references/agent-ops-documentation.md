---
name: agent-ops-documentation
description: Use when configuring Hermes/OpenClaw agents, profiles, gateways, permissions, cron jobs, routing, or operational workflows; document durable changes in local Markdown docs with changelog and verification.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, openclaw, agents, operations, documentation, gateway, profiles, changelog]
    related_skills: [hermes-agent]
---

# Agent Operations Documentation

## Overview

Use this skill when changing operational agent setup: Hermes/OpenClaw profiles, gateway services, Telegram routing, agent personas, permissions, cron jobs, Kanban routing, or reusable workflow conventions.

The key lesson: operational changes should leave a durable, human-readable trail in `/home/usuario/.hermes/docs/`. The docs should explain what changed, why, where it lives, how to verify it, and how to operate it later. Do not rely only on chat history.

## When to Use

Use this skill when the user asks to:

- create or modify Hermes/OpenClaw agents or profiles;
- activate, restart, install, or troubleshoot Hermes/OpenClaw gateway services;
- configure agent filesystem permissions or working directories;
- create routing conventions such as `@finance` or Kanban assignees;
- add recurring jobs or automation for an agent;
- create reusable runbooks, templates, scripts, or skills for agent workflows;
- document what was done in `/home/usuario/.hermes/docs/`;
- make a plan and then execute operational improvements.

Do not use this skill for one-off application code changes unless they affect agent operations or local assistant workflow.

## Documentation Location

Default local documentation directory:

`/home/usuario/.hermes/docs/`

Keep the directory organized with:

- `INDEX.md` — table of contents and important paths;
- `CHANGELOG.md` — chronological change history;
- numbered context docs, e.g. `08-plano-execucao-melhorias-finance-senior.md`;
- optional subdirectories for reusable material, e.g. `templates-financeiro/`.

## Required Workflow

### 1. Gather context first

Before changing anything, inspect the relevant live state with the appropriate tools:

- profile list/status;
- gateway status/logs;
- config paths;
- current profile `SOUL.md`;
- existing docs under `/home/usuario/.hermes/docs/`;
- relevant filesystem permissions.

Do not invent paths, profiles, tokens, or service names.

### 2. Make the operational change

Apply changes through tools, not by telling the user what to do. Examples:

- `hermes profile create ...`
- `hermes --profile <name> config set ...`
- `hermes gateway install/start/restart/status`
- update `SOUL.md` with `patch` or `write_file`;
- create scripts/templates/agent-ops-documentation/docs with `write_file`;
- create cron jobs with the cron tool when requested.

Avoid stopping OpenClaw or migrating secrets unless the user explicitly asks.

### 3. Verify with real output

Before claiming success, run at least one verification appropriate to the change:

- `hermes profile list` for profile creation;
- `hermes kanban assignees` for routing availability;
- `hermes gateway status` for gateway changes;
- read back modified docs/config/persona files;
- execute a safe create/read/delete test for filesystem permission changes;
- list cron jobs after creating one.

### 4. Document the change

For every durable improvement, update docs in `/home/usuario/.hermes/docs/`:

- create or update a context-specific Markdown file;
- update `INDEX.md` with the new file;
- update `CHANGELOG.md` with date/time, affected agent, files changed, validation, and next steps.

Use the system date from `date` when a timestamp is needed.

### 5. Keep secrets out of docs

Never write bot tokens, API keys, OAuth tokens, or raw secret values into Markdown docs or final summaries. It is fine to document:

- bot username;
- service name;
- config file path;
- whether validation succeeded;
- fingerprint/presence only when necessary and non-sensitive.

## Recommended Doc Shapes

Reusable templates are included:

- `templates/agent-ops-documentation/context-doc.md` — starting point for a context-specific operational doc.
- `templates/agent-ops-documentation/changelog-entry.md` — starting point for entries in `/home/usuario/.hermes/docs/CHANGELOG.md`.

### Context doc

Use a focused title and explain:

- objective;
- scope;
- current state;
- changes applied;
- commands/configuration involved;
- files changed;
- validation performed;
- operational commands;
- risks/cautions.

### Execution plan

For plans that will be executed, include microtasks by phase:

- documentation/rastreabilidade;
- skill/workflow creation;
- templates;
- scripts;
- cron jobs;
- routing/security;
- final verification.

Save plans as Markdown in docs, not only in chat.

### Changelog entry

Each entry should include:

- timestamp;
- affected agent/profile;
- type of change;
- summary of change;
- files created/altered;
- validation performed;
- next steps.

## Common Pitfalls

1. **Doing the change but not documenting it.**
   The user explicitly wants operational improvements recorded under `/home/usuario/.hermes/docs/`.

2. **Only saving a plan but not executing when the user said “faz tudo”.**
   If the user asks to plan and execute, save the plan first, then continue execution until verified.

3. **Using chat history as the source of truth.**
   Chat history is not enough. Create durable Markdown files and read them back to verify.

4. **Leaking secrets into docs.**
   Document paths, service names, bot usernames, and validation status, but not tokens or keys.

5. **Changing OpenClaw when the user wants parallel operation.**
   Preserve OpenClaw unless the user explicitly asks to stop, migrate, or replace it.

6. **Forgetting the index/changelog.**
   New context docs are incomplete unless `INDEX.md` and `CHANGELOG.md` are updated.

## Verification Checklist

- [ ] Relevant live state inspected before changes.
- [ ] Operational change applied with tools.
- [ ] Real verification command/test executed.
- [ ] Context doc saved under `/home/usuario/.hermes/docs/`.
- [ ] `INDEX.md` updated.
- [ ] `CHANGELOG.md` updated.
- [ ] No secrets written to docs.
- [ ] Final response includes changed paths and verification results.
