---
name: self-hosted-agent-platforms
description: Use when installing or managing agent platforms.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags:
      - paperclip
      - openbot
      - copilotkit
      - openduet
      - agent-orchestration
      - self-hosted
    related_skills:
      - software-deployment
---

# Self-Hosted Agent Platforms (install & operate)

## When to Use
- Trigger when the user asks to install, set up, upgrade, troubleshoot, or operate a self-hosted agent-orchestration platform (e.g., Paperclip, OpenBot/CopilotKit) on their Linux server.

Class skill for installing/upgrading self-hosted agent-orchestration platforms (Paperclip, OpenBot/CopilotKit-OpenDuet, and similar Node.js control planes) on the user's Linux home server.

## Always-on rules
- Before touching an existing instance, run `npx paperclipai doctor` (or platform equivalent) — diagnose before change.
- Never delete or re-initialize `~/.paperclip/instances/default/` — that is the user's live data (Postgres DB, secrets, backups). Back up first if asked to reset.
- Keep server bound to loopback (127.0.0.1) unless the user explicitly asks for LAN/tailnet exposure.
- User expects delivery in Portuguese, terse status + link to relatório file in MEGA, not full prose in chat.

## Procedure: fresh install (Paperclip, verified path)
1. Check prerequisites: `node --version` (needs 24.11+), `pnpm --version` (9.15+), Docker optional.
2. Install CLI: `npx --registry https://registry.npmjs.org paperclipai@latest onboard --yes` — install dir lands in `~/.paperclip/cli/installs/npm/<version>/`. The `--registry` flag avoids E404 from a private `~/.npmrc`.
3. Onboard creates embedded Postgres (port 54329, `~/.paperclip/instances/default/db`), `.env` JWT secrets, `secrets/master.key`, and a systemd user service `paperclipai.service` with linger (starts at boot).
4. Verify: `curl -s http://127.0.0.1:3100/api/health` → expect `{"status":"ok","bootstrapStatus":"ready"}`; `systemctl --user status paperclipai`. Initial backup warning (no backup yet, 60min schedule) is expected and self-resolves.
5. Post-install, remaining user steps: configure LLM provider (`npx paperclipai configure`), hire agents (OpenClaw/Claude Code/etc. auto-discovered), create first company via http://127.0.0.1:3100.

## Procedure: test-drive (no persistent state)
`npx paperclipai test-drive` — foreground, temp dir, no service, no first task. Pass `--data-dir` to reuse; `--no-browser` to stay headless. Use for demos or before committing.

## Ops commands
```bash
systemctl --user restart|stop|status paperclipai
npx paperclipai configure     # edit settings/LLM provider
npx paperclipai doctor        # full diagnostic
```

## Pitfalls
- E404 on `paperclipai`: private npm registry in `~/.npmrc` shadows npmjs — always pass `--registry https://registry.npmjs.org` for this install.
- Fresh-instance backup warning right after start is expected; do not report as failure.
- Health endpoint is `/api/health`, not `/health`.

## Procedure: OpenBot / CopilotKit via OpenDuet (validado até o login)
- Repo OpenDuet (construído sobre o OpenBot) em `~/openduet-openbot-ui-diagnose`. Usar branch tracking upstream main; o upstream agora suporta nativamente `OPENBOT_HOST` e allowlist de Host header — NÃO reaplicar o diff antigo de `vite.config.ts` (virou desnecessário).
- Pré-requisitos: Bun (`curl -fsSL https://bun.sh/install | bash` → `~/.bun/bin`), Node 22, Docker. `cp .env.example .env`; `bun install` na raiz (openbot/ instala no primeiro start).
- Subir: `bash scripts/start.sh` → Postgres + computadores Docker + API :3001 + worker + app dev (vite) :3010. O servidor SE RECUSA a subir sem a chave do CopilotKit Intelligence (`INTELLIGENCE_API_KEY`) e sem model key no .env — o Usuário edita o .env ele mesmo (nunca receber chave colada no chat).
- Login do Intelligence: `npx --yes copilotkit@latest login` (interativo). Rodar em background com pty; no prompt "Press Enter to continue..." enviar `\r` via process_manage (write) — newline simples pode não disparar o próximo passo; então o CLI imprime a URL de auth. O callback cai em `127.0.0.1:<porta>` — o link SÓ funciona aberto no navegador da própria máquina. Se o browser exibir um código curto, colá-lo no CLI.
- Pitfall: NUNCA deixar o CLI de login esperando sem o usuário clicar — o spinner dele vaza memória e o node morre com OOM (exit 134) em ~1–2 dias de espera. URL/token expiram antes disso: se o usuário não estiver pronto, matar o processo e relançar no momento do clique.
- Exposição externa: seguir a skill `devops/acesso-remoto-maquina` (ngrok http com `--host-header="localhost:3010"` + basic-auth obrigatório; app single-user = quem alcança a porta é admin). Após ter a URL do ngrok, acrescentá-la em `TRUSTED_ORIGINS` no .env e reiniciar o app.
- Pendente (passo do usuário): completar login CopilotKit → seleção de projeto → model key no .env → start.sh → verificar 3010/3001 → ngrok.

## Reporting
Write installation report to `~/MEGA/Documentos/<ToolName>/INSTALACAO-RELATORIO.md`: what it is (1 line), status table of install steps, how-to-use, remaining config steps, data layout, ops commands, next steps. Link the file in chat; don't paste the whole report.

references/: `paperclip-architecture.md` (deployment modes, data layout, update/rollback, upgrade path).
