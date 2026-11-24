---
name: paperclip-orchestrator
version: 1.0
author: Hermes Agent
license: Proprietary
description: Setup Paperclip e integrar agentes via CLI (empresa, CEO, contratação).
metadata:
  hermes:
    tags:
      - paperclip
      - orchestrator
      - llm
      - systemd
    related_skills:
      - agent-orchestration
---

# Paperclip (orquestrador de agentes de IA)

## When to Use
Use este skill quando o usuário pedir para instalar, configurar, atualizar ou diagnosticar o Paperclip (orquestrador de agentes de IA) ou relacionado à injeção de chaves de API em serviços systemd.

## Context
Paperclip é o 'empresa dos agentes' — orquestra OpenClaw, Claude Code, Codex etc. numa org chart. Este skill cobre setup local, provider LLM (env vars), e manutenção do serviço systemd.

## Procedure
1. **Instalação**: usar `npx --registry https://registry.npmjs.org paperclipai@latest onboard` para instalar a CLI e as migrações de banco.
2. **Serviço**: usar `npx paperclipai@latest service install` + `systemctl --user enable --now paperclipai.service` + `loginctl enable-linger <user>` para garantir boot no startup.
3. **Health check**: validar em `http://127.0.0.1:3100/api/health` para confirmar `status:ok`.
4. **LLM provider**: injetar `OPENAI_API_KEY` em `~/.paperclip/instances/default/.env` (runtime dotenv) E em `~/.config/systemd/user/paperclipai.service.d/<nome>.conf` (systemd environ), depois restart.
5. **Verificação**: checar `/proc/<pid>/environ` para garantir que a chave está ativa no processo.
6. **Documentação**: registrar relatório em `~/MEGA/Documentos/Paperclip/INSTALACAO-RELATORIO.md`.

## Pitfalls
- **Nunca imprima a chave**: use apenas prefixo/sufixo e tamanho ao reportar em chat.
- **`database_backup_missing` é normal**: logo após start, o backup não existe ainda. Some na próxima hora.
- **Environ vs .env**: dotenv carrega em runtime, então `/proc/environ` não reflete o `.env`. O drop-in systemd cobre isso.
- **API local precisa de token**: endpoints como `/api/llm/providers` exigem bearer token. Sem token salvo localmente, configure via UI.
- **Wizard é interativo**: `paperclipai configure -s llm` não serve para automação não-interativa.

## Integração de agentes (contratação via CLI, sem UI)
Resumo: contratação de agente exige empresa + agente CEO ATIVO; o fluxo é empresa → CEO → convite → join request → aprovação board → claim da chave. Detalhes em references/integracao-agentes.md — leia antes de qualquer hire.

Regras duras:
- CRIE o CEO antes de contratar qualquer funcionário — aprovação de join request falha com "no active CEO" se a empresa não tem agente CEO. "CEO" é papel de AGENTE (role=ceo), nunca membershipRole de membro humano (os válidos: owner/admin/operator/viewer).
- Fluidez no CLI: `company create` → `agent create --payload-json` (role=ceo) → `openclaw invite-prompt` → POST /api/invites/{id}/accept → POST /api/companies/{cid}/join-requests/{rid}/approve (bearer do BOARD) → POST /api/join-requests/{rid}/claim-api-key com claimSecret (single-use).
- O token de runtime-state exige bearer de BOARD; a chave de agente (pcp_...) retorna 403 nesses endpoints.
- `paperclipai connect` é interativo — para automação use `context set --api-base ... --persona board --api-key-env-var-name PAPERCLIP_API_KEY --use`.

## Acesso remoto via ngrok (UI de fora da máquina)
O Paperclip em `local_trusted` rejeita hosts desconhecidos com "This hostname is not allowed". O hostname do túnel ngrok TEM que estar explicitamente na allowlist — passá-lo como argumento CLI (`allowed-hostname <host>`) fica em timeout; editar config direto é o caminho confiável.

```bash
# 1. subir o túnel (daemon, background — roda sozinho)
ngrok http 3100
# pegar URL: curl -s http://localhost:4040/api/tunnels | python3 -c "import sys,json; print(json.load(sys.stdin)['tunnels'][0]['public_url'])"

# 2. extrair o host (ex: SEU-TUNNEL.ngrok-free.app) e adicionar ao config
#    em ~/.paperclip/instances/default/config.json → server.allowedHostnames[]

# 3. restart + validar por cima do túnel
systemctl --user restart paperclipai
curl -s -o /dev/null -w "%{http_code}" https://<host>.ngrok-free.app/api/health  # expect 200
```

O ID do dispositivo ngrok (ex: HDILAGSPE08CT4Q) NÃO é URL de acesso — o Usuário pode confundir; a URL de acesso é sempre o `<hash>.ngrok-free.app`. Sem autenticação de tela além do warning "Visit Site" do ngrok.

## References
- Health endpoint: `http://127.0.0.1:3100/api/health`
- Instância: `~/.paperclip/instances/default/`
- Relatório: `~/MEGA/Documentos/Paperclip/INSTALACAO-RELATORIO.md`