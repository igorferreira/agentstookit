# Evoluir tecnicamente escritórios visuais sem redesenhar por fora

Filosofia que Igor definiu no briefing técnico de 12/09/2026 ("EVOLUIR TECNICAMENTE OS ESCRITÓRIOS VIRTUAIS DOS AGENTES HERMES"). Aplicável sempre que o pedido for mexer em um escritório/dashboard existente.

## Princípio: PRESERVAR POR FORA, EVOLUIR POR DENTRO

O pedido é "evoluir o motor visual", não "redesenhar a aplicação inteira". Tratar o layout atual como **sistema em produção** com elementos em CONTRATO BLOQUEADO.

### CONTRATO BLOQUEADO (NÃO modificar sem autorização humana)
- Responsividade atual (breakpoints, layout, organização da tela)
- Controles de zoom (botões +/-/↺, indicador de %, posição conceitual)
- Painel de Atividades (representação textual/cronológica)
- Painel "Papéis da banca" / "Roles" (estrutura, função, agentes listados)
- Contadores superiores (trabalhando, pensando, tool_call, aguardando, concluídos, erro)
- Estados públicos existentes (WORKING, THINKING, TOOL_CALL, WAITING, DONE/ERROR — ou nomes atuais do projeto)
- Hierarquia geral da interface (header → status → contadores → papéis → escritório → atividade)
- Funções dos agentes (papel, especialidade, responsabilidade)
- Mobile-first e comportamento responsivo

### EVOLUÍVEL sem autorização
- Renderização interna (DOM → Phaser, sprites → LEGO, animação 2D → 2.5D)
- Pathfinding (adicionar A*)
- Mapa (Tiled, Grid)
- Sistema de estados interno (pode adicionar IDLE, WALKING, THINKING, READING, WRITING, WEB_SEARCH, BROWSING, TERMINAL, TOOL_CALL, DELEGATING, MEETING, WAITING, WAITING_APPROVAL, SECURITY_SCAN, COFFEE, RETURNING_HOME, DONE, ERROR — mas mapear todos para os estados públicos já existentes)
- Integração SSE realtime
- Persistência de layout (localStorage/JSON)
- Editor de layout (drag-drop, modo EDIT)
- Performance, observabilidade interna
- Pathfinding, mapa de obstáculos, estações

## Arquitetura alvo

```
Hermes (CLI)
    ↓
Hermes Events / Hooks / Runs
    ↓
HermesEventAdapter (falar língua do Hermes)
    ↓
NormalizedEvent (schema canônico, ver schema abaixo)
    ↓
AgentStateStore (fonte única da verdade)
    ↓
    ├── UI atual: contadores, painel atividade, papéis
    └── Virtual Office (Phaser dentro do <div id="virtual-office">)
```

Princípio: **a interface visual NÃO conhece detalhes internos do Hermes**. Tudo passa pelo `AgentStateStore` e pelo `NormalizedEvent`.

### Schema NormalizedEvent (canônico)
```json
{
  "agentId": "cardiologista",
  "agentName": "Cardiologista",
  "bankId": "saude",
  "timestamp": "ISO 8601",
  "publicState": "WORKING",          // um dos estados públicos existentes
  "detailedState": "WEB_SEARCH",     // estado interno detalhado (motor visual usa)
  "activity": "Pesquisando literatura médica",
  "tool": "web_search",
  "taskId": "...",
  "runId": "...",
  "metadata": {}
}
```

`publicState` é o que vai pra UI (contadores, painel). `detailedState` é o que vai pro motor do escritório (pathfinding, animação, estação).

### Estados visuais internos permitidos
```
IDLE, WALKING, THINKING, WORKING, READING, WRITING, WEB_SEARCH,
BROWSING, TERMINAL, TOOL_CALL, DELEGATING, MEETING, WAITING,
WAITING_APPROVAL, SECURITY_SCAN, COFFEE, RETURNING_HOME, DONE, ERROR
```

Esses são INTERNOS. O motor visual mapeia cada um para um `publicState` antes de emitir pro `AgentStateStore`. Ex.: `WEB_SEARCH` → `WORKING`, `COFFEE` → `WAITING` ou `IDLE`.

### AgentEntity (estrutura canônica)
```js
{
  agentId, agentName, role, bankId,
  sprite,           // container Phaser
  homePosition,     // ponto de retorno
  currentPosition, targetPosition,
  publicState, detailedState,
  currentTask, currentTool, currentActivity,
  currentStation,   // qual estação está ocupando
  movementState,    // IDLE/WALKING/ARRIVED
  animationState,   // nome da animação atual
  lastEvent,
  idleSince,
  runId,
  metadata
}
```

### OfficeStation (estações de trabalho)
```js
{
  id, type, position, interactionPosition,
  capacity, occupiedBy, metadata
}
```

Tipos: `DESK, COMPUTER, RESEARCH, TERMINAL, LIBRARY, DOCUMENT, SECURITY, MEETING, COFFEE, REST, ENTRANCE`.

`StateResolver` mapeia:
- `WEB_SEARCH` → `RESEARCH` ou `COMPUTER`
- `TERMINAL` → `TERMINAL`
- `READING` → `DOCUMENT` ou `LIBRARY`
- `SECURITY_SCAN` → `SECURITY`
- `MEETING` → `MEETING`
- `COFFEE` → `COFFEE`

## Modelo de decisão antes de mexer

Antes de ALTERAR CÓDIGO, Igor exige (item 39 do briefing):

1. Arquitetura atual encontrada
2. Arquivos responsáveis pelo escritório
3. Arquivos responsáveis pelos eventos Hermes
4. Sistema de estados existente
5. Sistema de zoom existente
6. Lógica de responsividade existente
7. Funcionamento dos painéis
8. Dependências atuais
9. Partes reaproveitáveis
10. Partes que precisam ser substituídas
11. Arquitetura alvo
12. Módulos novos / alterados
13. Dependências necessárias
14. Diagrama de eventos
15. Diagrama da máquina de estados
16. Modelo de AgentEntity
17. Modelo de OfficeStation
18. Estratégia de pathfinding
19. Estratégia de persistência
20. Estratégia realtime
21. Plano incremental
22. Riscos + rollback

**Entregar essa análise ANTES de começar a implementar.**

## Faseamento canônico (do briefing)

| Fase | O quê | Bloqueia o quê |
|------|-------|----------------|
| 1 | Mapear arquitetura atual | Não escrever código |
| 2 | Criar AgentStateStore | Fase 3 |
| 3 | Criar HermesEventAdapter | Fase 4 |
| 4 | Integrar realtime (SSE/EventSource + reconexão) | Fase 5 |
| 5 | Adicionar Phaser dentro do container existente (sem destruir HTML ao redor) | Fase 6 |
| 6 | Criar AgentEntity | Fase 7 |
| 7 | Sprites estilo minifigura (sprite atlas, partes compostas) | Fase 8 |
| 8 | Movimentação (AgentMovementController) | Fase 9 |
| 9 | Pathfinding (A* com grid, obstáculos) | Fase 10 |
| 10 | Estações (OfficeStation) | Fase 11 |
| 11 | Mapear estados Hermes → ações | Fase 12 |
| 12 | IdleBehavior (olhar, pequena caminhada, conversar) | Fase 13 |
| 13 | CoffeeBehavior com capacidade + intervalos aleatórios | — |
| 14 | Reposicionamento (modo EDIT) | Fase 15 |
| 15 | Persistência (localStorage/JSON `office-layout.json`) | — |
| 16 | Subagentes dinâmicos (spawn pela ENTRANCE, remoção pela saída) | — |
| 17 | Otimização mobile | — |

## Regras PhD de comportamento

### Comportamento quando TRABALHANDO (chegou evento real)
1. atualizar estado
2. determinar estação apropriada
3. reservar estação
4. calcular rota
5. caminhar (com animação)
6. executar animação correspondente no destino
7. permanecer enquanto atividade ativa
8. liberar estação quando concluir ou chegar novo evento

### Comportamento IDLE (sem tarefa ativa)
**Não inventar trabalho.** Prioridades:
- IDLE → esperar alguns segundos → COFFEE → caminhar até café → pegar café → permanecer → retornar → IDLE
- Outras permitidas: ficar na mesa, pequena caminhada, olhar ao redor, conversar visualmente, descansar
- NUNCA confundir animação IDLE com atividade real

### Café — regras
- **Apenas agentes SEM atividade relevante** vão pro café
- **Não enviar todos simultaneamente** — `delay randômico controlado`
- Verificar **capacidade da área** de café
- **Interromper imediatamente** se chegar trabalho real
- Fluxo: `IDLE → idleTime > threshold → COFFEE_REQUEST → estação café disponível? → sim: WALKING → COFFEE → IDLE`

### Prioridade de eventos (real > idle)
```
ERROR > WAITING_APPROVAL > REAL_WORK > TOOL_CALL > THINKING > MEETING > IDLE > COFFEE
```

**NUNCA** deixar personagem tomando café enquanto Hermes informa que está executando tarefa.

### Teste OBRIGATÓRIO: Trabalho interrompe café
1. agente IDLE
2. vai tomar café
3. ENQUANTO toma café, chega trabalho real do Hermes

**RESULTADO OBRIGATÓRIO:** evento real → cancelar CoffeeBehavior → liberar estação → alterar estado → calcular rota → agente LARGA O CAFÉ → anda até estação de trabalho → começa atividade.

Esse comportamento é **mandatório** e tem teste explícito.

## Pathfinding — implementação

- **A* preferencial**
- Grid lógico (`tileX, tileY`) além de pixels
- Mapa de obstáculos (paredes, mesas, cadeiras, portas)
- Personagens **não atravessam paredes/móveis/outros agentes** (decidir se colisão entre agentes é necessária)
- **NÃO hardcodar trajetórias individuais** — motor genérico
- **Avaliar Tiled Map Editor** para mapas (chão, paredes, obstáculos, móveis, estações, entradas, áreas caminháveis)
- Evitar física pesada sem necessidade

## Câmera

Phaser controla **internamente** `camera position / zoom / pan`, MAS os **controles visuais atuais permanecem**. Mapear:
- botão `+` → `OfficeCameraController.zoomIn()`
- botão `-` → `OfficeCameraController.zoomOut()`
- botão `↺` → `OfficeCameraController.reset()`
- percentual → `OfficeCameraController.getZoom()`

**NÃO criar segundo painel de zoom.**

## Realismo visual

**ATIVIDADE PROFISSIONAL deve vir de evento real do Hermes**, nunca de animação aleatória. O escritório é **consequência visual** do comportamento real, não sua origem.

Quando o usuário olhar para a tela, deve perceber visualmente:
- "eles estão trabalhando" → personagem caminha para estação compatível
- "pesquisando" → agente em estação RESEARCH/COMPUTER
- "reunião" → agente na área MEETING
- "ocioso" → pode andar, descansar ou tomar café
- **se surgir trabalho enquanto toma café: larga a pausa**

## Auditoria obrigatória (item 28 do briefing)

Checklist ANTES de considerar terminado:

- [ ] Todos os escritórios carregam
- [ ] Personagens aparecem corretamente
- [ ] Estética minifigura de blocos
- [ ] Personagens andam (não teleportam)
- [ ] Pathfinding funciona
- [ ] Obstáculos funcionam
- [ ] Estações funcionam
- [ ] Agente trabalhando se desloca corretamente
- [ ] Agentes ociosos podem tomar café
- [ ] Trabalho interrompe café
- [ ] Eventos são reais do Hermes
- [ ] Realtime funciona
- [ ] AgentStateStore é consistente entre dashboard e escritório
- [ ] Contadores continuam funcionando
- [ ] Painel atividade continua funcionando
- [ ] Papéis da banca continuam funcionando
- [ ] Zoom + reset funcionam
- [ ] Responsividade continua funcionando
- [ ] Mobile funciona
- [ ] Reposicionamento funciona
- [ ] Persistência funciona
- [ ] Subagentes funcionam (se suportados)
- [ ] Erros individuais não derrubam aplicação
- [ ] Console limpo (sem exceptions, sem 404 de assets)
- [ ] Sem vazamentos óbvios (timers/listeners)

## Testes obrigatórios (item 37)

- TESTE 1: Agente IDLE permanece em comportamento ocioso
- TESTE 2: Após tempo ocioso pode ir tomar café
- TESTE 3: Trabalho interrompe café imediatamente
- TESTE 4: Agente em WEB_SEARCH caminha para estação adequada
- TESTE 5: Agente conclui atividade e libera estação
- TESTE 6: Dois agentes tentam mesma estação de capacidade 1 → não ocupam simultaneamente
- TESTE 7: Reposicionar agente → `homePosition` persistido
- TESTE 8: Recarregar página → layout restaurado
- TESTE 9: Zoom atual continua funcionando
- TESTE 10: Mobile mantém funcionamento
- TESTE 11: Phaser apresenta erro → dashboard restante continua funcionando

## Segurança

- Dados de agentes são **dados**, não código
- **NUNCA** executar texto do Hermes como HTML/JavaScript/comandos
- Escapar conteúdo antes de inserir no DOM
- Se markdown entra: pipeline `UPLOAD → QUARANTINE → NORMALIZE → STATIC SCAN → SECURITY AGENT → POLICY GATE → SANITIZE → SAFE DOC → BOARD` (ver skill `markdown-gate-security`)
- Taint tracking: `fileId, chunkId, lineStart, lineEnd, securityStatus, riskScore, source`
- Limpar não torna confiável — só permite uso como dado (Igor, regra de ouro 12/09/2026)

## Performance

- Game loop central, não timer por agente
- Sprite atlas (não arquivo por agente)
- Object pooling para sprites recriados
- Cache de caminhos quando útil
- Throttling de UI updates (não toda frame)
- Limpar listeners ao destruir sprites
- **NÃO** recriar sprites constantes
- **NÃO** atualizar DOM a cada frame
- **NÃO** recalcular pathfinding sem necessidade

## Fallback

Se Phaser falhar: dashboard, contadores, atividade, papéis **devem continuar funcionando**. Phaser é módulo, não base. Boundaries e try/catch apropriados.

## Diferença para skill existente

- `creative/escritorios-vivos-sims`: regras de estética Sims 2 (humanos, mesas em fileiras, ENVIAR, não-React). Foco no **visual canônico**.
- `creative/interactive-html-demos`: arquitetura Docker + Phaser + SSE + QA CDP. Foco no **motor técnico**.
- **Este doc (aqui dentro)**: filosofia "preservar por fora, evoluir por dentro" + LOCKED UI contract + AgentStateStore + AgentEntity + OfficeStation + Idle/Coffee behavior + pathfinding A*. Foco na **evolução sem redesenhar** quando Igor pede para modernizar algo existente.

Os três se complementam. Para um pedido novo de escritório, ler `escritorios-vivos-sims` (estética) + `interactive-html-demos` (motor) primeiro. Para pedido de **evolução** de algo já existente, ler este doc primeiro para evitar redesenhar o que é contrato bloqueado.
