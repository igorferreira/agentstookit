---
name: timeautomatico-realtime-integration
description: "TimeAutomático integration with Hermes real events."
tags: [timeautomatico, realtime, hermes, sse, plugins, legacy-hardening]
---

# TimeAutomático · Integração real-time com Hermes

Padrão validado em 12/09/2026 com Banca de Saúde TimeAutomático.

## Arquitetura

```
Hermes (perfil instrumentado)
    ↓ hooks oficiais (pre_llm_call, post_tool_call, subagent_start/stop, ...)
   ~/.cache/timeautomatico/events.jsonl   ← canônico, origin=hermes-plugin
    ↓ sidecar SSE (fail-closed)
   :8765/events?office=<officeId>
    ↓ nginx proxy
   Frontend EventSource('/events')
    ↓ applyEvent()
   AgentState (Map) → renderAgent() + pushFeed()
```

## Plugin oficial Hermes

Fonte versionada: `integracoes/hermes-plugin/timeautomatico-realtime/`

**Arquivos:**
- `plugin.yaml` — manifest com `provides_hooks`
- `__init__.py` — 8 hooks registrados: `pre_llm_call`, `post_llm_call`, `pre_tool_call`, `post_tool_call`, `api_request_error`, `subagent_start`, `subagent_stop`, `on_session_end`

**Regras obrigatórias:**
- Todo evento real carrega `origin=hermes-plugin` + `producer=timeautomatico-realtime`
- Heartbeat por processo em `~/.cache/timeautomatico/producers/producer-<profile>.json`
- Nunca gravar prompt, argumentos, resultados, reasoning ou resposta — somente metadados de lifecycle
- Só atribuir atividade a um especialista quando houver perfil/subagente real correlacionável

**Instalação:**
```bash
cp -r integracoes/hermes-plugin/timeautomatico-realtime/ ~/.hermes/plugins/timeautomatico-realtime/
for profile in saude saude-master health-performance-board ...; do
  cp -r ~/.hermes/plugins/timeautomatico-realtime/ ~/.hermes/profiles/$profile/plugins/
  hermes --profile "$profile" plugins enable timeautomatico-realtime
done
```

**Validação:**
```bash
hermes plugins doctor ~/.hermes/plugins/timeautomatico-realtime
# esperado: OK, registrations: 8 hooks

hermes --profile saude chat -q 'Teste: responda OK' --quiet

curl -fsS http://127.0.0.1:8090/source-status
# esperado: mode=hermes-real-only, active=true, eventsSeen>0
```

## Sidecar SSE (fail-closed)

Arquivo canônico: `demos/realtime/sse_server.py`

**Filtros obrigatórios:**
```python
if ev.get("origin") != "hermes-plugin" or ev.get("producer") != "timeautomatico-realtime":
    continue  # rejeita tudo que não é Hermes autêntico
```

**Endpoints:**
- `GET /events?office=<id>` — SSE com dedup por eventId, backoff 4s
- `GET /snapshot` — estado agregado (somente eventos reais)
- `GET /source-status` — heartbeat + active=true/false + eventsSeen
- `GET /health` — liveness

**Pump loop:** único leitor do JSONL, agrega e transmite a todos os subscribers via asyncio.Queue. Poll a cada 0.3s.

## Hardening de escritórios legados

Escritórios HTML antigos usam `Math.random()` + `setInterval()` para atividade cenográfica. O usuário **rejeita simulação**.

**Padrão:** `demos/principal/legacy-real-only.js` (3.6 KB) injetado via `<script>` no final de cada HTML legado.

**O que faz:**
1. Marca `<html data-realtime-mode="hermes-real-only">`
2. Cria badge fixo no topo ("☕ Hermes real desligado" / "● Hermes ativo")
3. Desabilita inputs de chat (`disabled=true`, `aria-disabled="true"`)
4. Substitui nodes de chat por clones bloqueados
5. `setInterval(enforceIdle, 500ms)` reatribui `estadoAg='Parado'` e remove classes `trab`/`andando`
6. Overwrites funções globais: `cicloEstados`, `ciclo`, `reuniao`, `mostrarAlerta` → vazio
7. `fetch('/source-status')` a cada 4s atualiza badge

**Como aplicar a um novo HTML legado:**
```html
<html lang="pt-BR" data-realtime-mode="hermes-real-only">
<!-- ... conteúdo ... -->
<script src="/legacy-real-only.js"></script>
</body>
</html>
```

## Zoom acessível

Padrão: `demos/clientes/banca-saude/js/camera.js`

**Requisitos:** botões `+`, `−`, `↺` (44px touch-target), roda do mouse, gesto de pinça, persistência por orientação (localStorage key: retrato/paisagem separados), range 65%–240%, step 15%.

**API:**
```js
export function fitCamera(scene, width, height, { reloadPreference = false } = {})
export function zoomIn(scene)
export function zoomOut(scene)
export function resetZoom(scene)
export function initCameraControls(scene, host)  // botões + wheel + pinch
```

## Minifiguras 3D em Phaser (runtime, sem assets)

Padrão: `demos/clientes/banca-saude/js/agentes.js`

**Partes:**
- `drawCylinder(scene, color)` — cabeça cilíndrica (corpo + topo + rosto)
- `drawCHand(graphics, x, y, color, mirror)` — mão em C
- `drawBlockTorso(scene, color)` — tronco em bloco (jaleco + cor + crachá)
- `drawArticulatedLegs(scene, color)` — pernas articuladas (calças + sapatos)
- `accessory(scene, agent)` — acessório único por especialista

**Visualização de delegações:** `demos/clientes/banca-saude/js/delegacoes.js` — seta laranja A→B animada (fade out 3s) para eventos `agent.delegated` autenticados.

## Painel flutuante mobile-otimizado

Padrão: `demos/clientes/banca-saude/js/painel-papeis.js`

- Minimizado no mobile inicial (sem histórico salvo)
- Redimensionável (handle ↘)
- Arrastável (cabeçalho)
- Persistência por localStorage
- `constrain()` limita posição ao bounding da stage

## QA automatizada

Script: `demos/qa/qa_banca_saude_final.py` (Playwright + Firefox headless)

**Valida:** 6 agentes com todas as partes, zoom +/−/↺, persistência localStorage, roda do mouse, layout retrato/paisagem sem overflow, estado inicial inativo.

**Execução:**
```bash
python3 demos/qa/qa_banca_saude_final.py
# Saída: JSON com violations (lista vazia = PASS) + screenshots em /tmp/
```

## Pitfalls conhecidos

| Pitfall | Mitigação |
|---------|-----------|
| Plugin Hermes não registra hooks | Verificar `provides_hooks` no plugin.yaml bate com `register_hook()` em `__init__.py` |
| Heartbeat expira (>15s) | `active=false` no `/source-status`, frontend mostra "Hermes real desligado" |
| Snapshot reativa agentes sem produtor vivo | Guard `state.backendUp` — snapshot só hydrate se `active=true` |
| `fetch` em JSDOM não implementado | Harness precisa injetar `window.fetch = mock` |
| `<template>.content.cloneNode` perde filhos em JSDOM | Fallback: `<div hidden id="agent-ref">` com árvore completa |
| CSP `https://*.tts.*` inválido | Wildcard só no final: `https://*.example.com` |
| `Phaser.AUTO` em headless sem GPU | Forçar `type: Phaser.CANVAS` |
| `import Phaser from '...'` retorna undefined | Phaser é UMD: `<script src="/vendor/phaser.min.js">` + `const Phaser = window.Phaser` |
| Firefox `--virtual-time-budget` congela async | Usar Playwright `page.wait_for_timeout()` |
| Container realtime sem porta mapeada | `ports: ["8765:8765"]` no docker-compose.yml |
| nginx buffering quebra SSE | `proxy_buffering off` + `X-Accel-Buffering: no` + `Cache-Control: no-store` |

## Referências

- Plugin canônico: `integracoes/hermes-plugin/timeautomatico-realtime/`
- Sidecar: `demos/realtime/sse_server.py`
- Hardening legados: `demos/principal/legacy-real-only.js`
- Camera zoom: `demos/clientes/banca-saude/js/camera.js`
- Minifiguras: `demos/clientes/banca-saude/js/agentes.js`
- Delegações: `demos/clientes/banca-saude/js/delegacoes.js`
- Painel: `demos/clientes/banca-saude/js/painel-papeis.js`
- QA: `demos/qa/qa_banca_saude_final.py`
