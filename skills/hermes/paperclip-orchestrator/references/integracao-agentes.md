# Fluxo de integração de agente no Paperclip (via CLI, sem UI)

Pré-requisitos: Paperclip rodando (health ok), CLI conectada como board.

## Passo 1 — Conectar CLI como board operator (se ainda não conectada)
```bash
paperclipai token board create  # gera pcp_board_...
export PAPERCLIP_API_KEY=pcp_board_<token>
paperclipai context set --api-base http://127.0.0.1:3100 --persona board --api-key-env-var-name PAPERCLIP_API_KEY --use
```
`paperclipai connect` é interativo — não serve para automação.

## Passo 2 — Criar empresa
```bash
paperclipai company create --payload-json '{"name":"<Nome>"}' --json
```
Guarda o `id` (usado em todos os comandos seguintes via `-C <companyId>`).

## Passo 3 — Criar agente CEO (OBRIGATÓRIO antes de contratar)
Aprovação de join request falha com "no active CEO" sem ele. Role ceo é papel de agente, não membershipRole humano (válidos: owner/admin/operator/viewer).
```bash
paperclipai agent create -C <cid> --payload-json '{"name":"CEO","role":"ceo","status":"active","title":"CEO","capabilities":"..."}' --json
```
O CEO nasce paused/preparing (adapter process placeholder) — normal; pode receber instruções depois.

## Passo 4 — Convite para o agente externo
```bash
paperclipai openclaw invite-prompt --payload-json '{"agentMessage":"..."}' --json
```
Retorna `inviteUrl`, `invitePath` e o onboarding.txt (GET `<base><onboardingTextPath>`) com o payload exato.

## Passo 5 — Join request (lado do agente)
POST `<base>/api/invites/<inviteToken>/accept` com JSON:
- `requestType: "agent"`, `adapterType: "openclaw_gateway"` (ou `hermes_gateway` / `hermes_local`)
- `agentDefaultsPayload`:
  - openclaw_gateway: `url` (ws://127.0.0.1:18789 se gateway local), `headers.x-openclaw-token` (de `~/.openclaw/.env` → OPENCLAW_GATEWAY_TOKEN; auth.mode=token no clawdbot.json aponta para essa env var), `paperclipApiUrl`, `sessionKeyStrategy: "issue"`, `role`, `scopes`
  - hermes_gateway: `apiBaseUrl` (ex: http://127.0.0.1:9119 — dashboard root é mapeado para /api), `apiKey` (mesmo valor de API_SERVER_KEY), `paperclipApiUrl`
Resposta traz `id` (requestId), `status: pending_approval` e `claimSecret` (single-use, expira).

## Passo 6 — Aprovação (bearer do BOARD, não do agente)
```bash
curl -X POST -H "Authorization: Bearer $PAPERCLIP_API_KEY" -d '{}' \
  http://127.0.0.1:3100/api/companies/<cid>/join-requests/<rid>/approve
```

## Passo 7 — Claim da chave de API do agente
```bash
curl -X POST -d '{"claimSecret":"<secret>"}' \
  http://127.0.0.1:3100/api/join-requests/<rid>/claim-api-key
```
Salvar o token em arquivo privado (chmod 600). A partir daí o agente responde com identity própria via `paperclipai agent me --api-key <pcp_...>`.

## Gotchas
- runtime-state e outros endpoints de gestão exigem bearer de BOARD; chave de agente dá 403.
- `agent approve <id>` (CLI) espera agentId, não joinRequestId — use o endpoint REST de join-requests.
- Endpoints inexistentes retornam `API route not found` (não 404 HTTP puro) — teste variantes antes de concluir.
- Nunca imprimir tokens completos em chat/log; salvar direto em arquivo com chmod 600.
