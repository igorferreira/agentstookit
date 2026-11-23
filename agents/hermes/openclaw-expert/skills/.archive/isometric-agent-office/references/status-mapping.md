# Status mapping — SSE eventos → Office comportamento

Mapeamento canônico entre eventos do `realtime-events` (skill `general/realtime-events`) e o comportamento do escritório isométrico (skill `general/isometric-agent-office`).

## Tipos SSE → STATUS

| Evento SSE | STATUS resultante | Posição | Animação |
|-----------|------------------|---------|----------|
| `banca.started` | (broadcast, não muda agente) | — | — |
| `banca.completed` | (broadcast) | — | — |
| `file.received` | (broadcast) | — | — |
| `agent.started` | `working` | cadeira à frente da mesa | braço direito mexe |
| `agent.idle` | `idle` | corredor/café/estante (aleatório) | leve tilt + respiração (bêbedo no café) |
| `agent.thinking` | `thinking` | cadeira | cabeça balança |
| `agent.status.changed` | `ev.status` | posição correspondente | animação correspondente |
| `agent.task.started` | `working` | cadeira | braço direito pequeno tic (digitando) |
| `agent.task.completed` | `completed` | perto da mesa, lado | idle |
| `agent.task.failed` | `error` | perto da mesa | mão na cabeça |
| `agent.tool.started` | `tool_call` | cadeira apontando pra tela | ⚙ girando |
| `agent.tool.completed` | `thinking` | cadeira | cabeça balança |
| `agent.delegated` | `delegating` | apontando pra lado | braço direito horizontal |
| `agent.waiting` | `waiting` | de pé ao lado da mesa | idle, parado |
| `agent.message` | (status atual) | — | mostra 💬 na fala por 5s |
| `agent.error` | `error` | perto da mesa | mão na cabeça |
| `agent.offline` | `offline` | longe, estático | invisível/separado |
| `agent.completed` | `completed` | perto da mesa, lado | idle |

## Cores canônicas (STATUS_COLOR)

| STATUS | Hex |
|--------|-----|
| `offline` | `#666666` |
| `idle` | `#7a8ba2` |
| `waiting` | `#f1c40f` (amarelo) |
| `working` | `#27ae60` (verde) |
| `thinking` | `#5b8def` (azul) |
| `tool_call` | `#8e44ad` (roxo) |
| `delegating` | `#ff8c00` (laranja) |
| `completed` | `#1FD3C4` (ciano) |
| `error` | `#c0392b` (vermelho) |

## Guardrails

- Não trocar status se `agent.status === novo` (exceto se `activity` mudou). Evita tween em cima de tween.
- Sempre cancelar tween anterior antes de iniciar novo (`agent.tweenHandle.remove()`).
- Se `event.message` chega, mostrar `💬` no label por 5s (`setTimeout`), depois restaurar nome.
- Deduplicação por `eventId` é responsabilidade do consumidor (`sse.js`), não do escritório.
