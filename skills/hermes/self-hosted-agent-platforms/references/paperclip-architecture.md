# Paperclip — architecture & ops depth

## What it is
Open-source orchestration for teams of AI agents ("company" vs the agent being the "employee"). Node.js server + React UI + embedded PostgreSQL. MIT, github.com/paperclipai/paperclip. Works with OpenClaw, Claude Code, Codex, Cursor, Gemini CLI, OpenCode, Pi, Hermes, Grok, Kimi — any agent that can receive a heartbeat.

## Pillars
- Agentic task manager (ticket-based, atomic checkout, execution locks)
- Org chart for agents (roles, reporting lines, permissions, budgets)
- Agent employee training (Skill Studio, evals, version history)
- Agentic OS (any model/provider, sandboxing, MCP, cost controls)

## Data layout (~/.paperclip/)
```
instances/default/
├── config.json
├── db/              # embedded PostgreSQL (port 54329)
├── .env             # JWT secrets
├── secrets/master.key
├── data/storage/    # local or S3-compatible file storage
├── data/backups/    # auto-backup: 60min interval, 30d retention
└── logs/
cli/installs/npm/<version>/   # CLI install location
```

## Deployment modes
- trusted local loopback (default after onboard): no auth from localhost, bind 127.0.0.1:3100
- authenticated/private: `onboard --bind lan` or `--bind tailnet` — use for any non-localhost exposure
- production: external Postgres + Docker deploy; docs.paperclip.ing/reference/deploy/

## Update / rollback
- Upgrade: `npx paperclipai@latest onboard` rerun keeps existing config; pin versions for stability
- Canary/git-ref installs available; rollback documented in docs.paperclip.ing/reference/cli/installation/
- `test-drive` never installs a service and never persists unless `--data-dir` given — safe for demos
- Company export/import (org packages, secret scrubbing) for portability; full-instance recovery uses backups

## Key docs
- Docs: https://docs.paperclip.ing
- Installation: docs.paperclip.ing/reference/cli/installation/
- Deployment modes: docs.paperclip.ing/reference/deploy/deployment-modes/
