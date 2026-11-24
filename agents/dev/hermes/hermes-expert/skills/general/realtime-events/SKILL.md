---
name: realtime-events
description: Use ao criar/consumir o pipeline realtime Hermes → JSONL → SSE → frontend para escritórios TimeAutomático.
---

# TimeAutomático · Realtime events

Padrão validado em 12/09/2026 com Banca de Saúde funcional.

## Arquitetura

```
Hermes / agentes / ferramentas
            ↓ (chamadas Python emit.emit)
   ~/.cache/timeautomatico/events.jsonl   ← canônico
            ↓ (tail)
   sidecar SSE 127.0.0.1:8765
            ↓ (proxy nginx /events → painel:80 → realtime:8765)
   Frontend EventSource('/events?office=X')
            ↓ (applyEvent)
   AgentState (Map) → renderAgent() + renderSummary() + pushFeed()
```

## Arquivos canônicos

- `realtime/emit.py` — grava 1 evento no JSONL canônico
- `realtime/sse_server.py` — tail JSONL, expõe SSE + snapshot + health
- `realtime/dev_simulator.py` — simulador DEV (NUNCA produção)
- `demos/docker/docker-compose.yml` — adiciona container `realtime`
- `demos/docker/nginx.conf` — proxy `/events` e `/snapshot`
- `demos/clientes/escritorio_banca_saude.html` — consumidor (referência)

## Schema do evento (versão 1)

```json
{
  "v": 1,
  "eventId": "uuid-v4",
  "timestamp": "ISO-8601 UTC ms",
  "officeId": "string",
  "agentId": "string|null",
  "type": "agent.status.changed|...",
  "status": "working|thinking|tool_call|delegating|waiting|completed|error|idle|offline",
  "activity": "string|null",
  "taskId": "string|null",
  "tool": "string|null",
  "delegatedBy": "string|null",
  "delegatedTo": "string|null",
  "to": "string|null",
  "message": "string|null"
}
```

## Tipos aceitos

| Família | Tipos |
|---------|-------|
| Banca | `banca.started`, `banca.completed` |
| Arquivo | `file.received`, `file.quarantined`, `file.scanning`, `file.approved`, `file.blocked` |
| Agente (estado) | `agent.started`, `agent.idle`, `agent.thinking`, `agent.status.changed` |
| Agente (tarefa) | `agent.task.started`, `agent.task.completed`, `agent.task.failed` |
| Agente (ferramenta) | `agent.tool.started`, `agent.tool.completed` |
| Agente (delegação) | `agent.delegated` |
| Agente (mensagem) | `agent.message` (com `to` e `message`) |
| Agente (erro/offline) | `agent.error`, `agent.offline`, `agent.completed`, `agent.waiting` |

## Princípios arquiteturais (NÃO QUEBRAR)

1. **Estado separado do DOM**: `state.agents = new Map()` é a fonte de verdade. Render é função pura do estado.
2. **Render incremental**: cada evento atualiza 1 nó (ou 0); nunca `innerHTML` no container.
3. **EventSource com dedup por `eventId`**: cliente mantem Set dos últimos 500 IDs e descarta duplicatas (caso reconecte e o servidor replay).
4. **Reconexão automática**: `EventSource.onerror` mostra toast + tenta reconectar a cada 4s.
5. **Snapshot inicial**: ao abrir, `fetch('/snapshot')` antes de SSE; evita "escritório vazio" por 1-2s até primeiro evento.
6. **`prefers-reduced-motion`**: animations desativadas via media query no CSS do consumidor.
7. **Touch targets ≥ 44px**: status badge e ações devem ter min-height 44px para mobile.
8. **CORS permissivo**: o sidecar adiciona `Access-Control-Allow-Origin: *` direto nas respostas (sem preflight, EventSource não dispara OPTIONS).
9. **`/health` e `/snapshot` separados**: `/health` é check rápido; `/snapshot` retorna o agregado atual derivado dos eventos lidos.
10. **Replay opcional via `?last=<offset>`**: cliente pode pedir todos os eventos desde um offset inicial.
11. **Todos os agentes visíveis em mobile portrait (390×844)**: grid 12-col responsivo com `grid-column:span 6` mobile / `span 2` desktop. Nunca `min-height:XXXpx` que esconde os agentes.
12. **Layout flex, não `calc(100vh - NNNpx)`**: body como `flex column`, header/summary/feed `flex:none`, office `flex:1`. Magic numbers no `calc` quebram quando header muda.
13. **3D visual com CSS perspective**: cubo 6-faces + olhos/boca em `translateZ` real. Avatar chapado = "não tá 3D" (feedback literal do usuário 12/09/2026).
14. **Feed colapsado por padrão em mobile**: usuário pediu "todo.mundi na tela" — feed `max-height:30vh` recolhido vira 30px de barra única, expansível no clique.

## Pitfalls conhecidos (validados)

| Pitfall | Mitigação |
|---------|-----------|
| `<template>.content.cloneNode` perde filhos em JSDOM | manter `<div hidden id="agent-ref">` com estrutura equivalente como fallback |
| `face.querySelector('.ant::after')` retorna `null` (pseudo-elemento) | apenas `querySelector('.ant')` |
| nginx buffering quebra SSE | `proxy_buffering off` + `X-Accel-Buffering: no` + `Cache-Control: no-store` |
| Sidecar lê offset EOF após bootstrap e ignora novos | revisar `JsonlTail._bootstrap_full_history()` ao reiniciar; salva em `state.json` |
| EventSource re-conectando pode duplicar eventos | dedup por `eventId` no cliente |
| Initial "escritório vazio" antes do SSE conectar | `fetch('/snapshot')` ANTES de abrir EventSource |
| Container python:3.12-slim sem libs | `pip install aiohttp` no `command:` do compose |

## Como adicionar uma nova banca

1. Adicionar entry em `AGENTES_DEF` no HTML com `{id, nome, role, cor}` (cor por status).
2. Trocar `OFFICE_ID` para o novo officeId.
3. Atualizar `dev_simulator.py` para emitir eventos com esse officeId.
4. Rebuild + restart.
5. Validar JSDOM (`/tmp/banca_final.js` é o harness; adaptar para o novo HTML).

## Integração obrigatória com Hermes real

Usar o plugin oficial versionado em `integracoes/hermes-plugin/timeautomatico-realtime/`, com hooks `pre/post_llm_call`, `pre/post_tool_call`, `subagent_start/stop`, `api_request_error` e `on_session_end`.

Regras obrigatórias:
- Todo evento real carrega `origin=hermes-plugin` e `producer=timeautomatico-realtime`.
- O sidecar e o frontend validam os dois campos e rejeitam todo o restante (fail-closed).
- O plugin mantém heartbeat por processo em `~/.cache/timeautomatico/producers/`.
- O selo verde depende de `/source-status.active=true`; conexão SSE sozinha NÃO prova realtime.
- Sem produtor Hermes real, exibir `Hermes real desligado` e manter agentes no café.
- Nunca gravar prompt, argumentos, resultados, reasoning ou resposta nos eventos públicos; somente metadados de lifecycle.
- Só atribuir atividade a um especialista quando houver perfil/subagente real correlacionável. Não distribuir trabalho cenográfico.

## Teste rápido ponta-a-ponta real-only

```bash
# 1. Validar plugin
hermes plugins doctor integracoes/hermes-plugin/timeautomatico-realtime

# 2. Subir/recriar sidecar + painel
cd demos/docker && docker compose up -d --build --force-recreate realtime painel

# 3. Sem Hermes instrumentado, deve ficar inativo
curl -fsS http://127.0.0.1:8090/source-status
# esperado: mode=hermes-real-only e active=false

# 4. Rodar um turno REAL em um perfil instrumentado
hermes --profile saude chat -q 'Teste técnico: responda apenas OK' --quiet

# 5. Confirmar evento real e snapshot
curl -fsS http://127.0.0.1:8090/snapshot
# esperado: eventsSeen>0; eventos têm origem hermes-plugin
```

O antigo `dev_simulator.py` foi removido. Não recriar simulador nem usar eventos sintéticos para demonstrar atividade ao usuário.

## Troubleshooting (destravado com tentativa/erro)

Validação JSDOM, Firefox `--virtual-time-budget`, smoke-test ngrok, bug específico do `<template>.content` em JSDOM, reconstrução Docker sem pull full e reset do sidecar: ver `references/sse-debugging.md`.

## Design patterns visuais (cubos 3D, grid responsivo, feed colapsável)

Como fazer **avatar realmente 3D** (cubo CSS perspective, não emoji), **grid 12-col** com todos os agentes visíveis em mobile, **feed colapsado por padrão**, e **texto longo sem cortar**: `references/css-design-patterns.md`.
