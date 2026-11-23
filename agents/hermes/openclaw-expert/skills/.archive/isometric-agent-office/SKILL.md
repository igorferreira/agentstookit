---
name: isometric-agent-office
description: Isometric 2.5D Phaser 3 office demo with realtime agents.
---

# Isometric 2.5D agent office

Validated 12/09/2026 com Banca de Saúde TimeAutomático funcional. Padroniza a criação de escritórios isométricos onde personagens andam, sentam-se, vão ao café, em resposta a eventos realtime.

**Triggers**: "escritório isométrico", "2.5D office", "Phaser office", "Phaser 3 demo", "personagens andando".

## Por que Phaser 3 (e não PixiJS)

| Critério | Phaser 3 | PixiJS v8 |
|----------|----------|-----------|
| Init síncrono (sobrevive a Firefox `--virtual-time-budget`) | ✅ `new Phaser.Game({})` é sync | ❌ `app.init()` retorna Promise → screenshot fica antes do canvas |
| Tweens nativos + scene graph + física arcade | ✅ built-in | ❌ depende de GSAP/tweens.js externo |
| Container com `setData`/`setInteractive` | ✅ | ✅ |
| Bundle size | ~1.18MB minified | ~666KB minified |

**Decisão**: Para isométrico com 6–30 agentes e comportamento animado, **Phaser 3 com bundle local** (`vendor/phaser.min.js`). PixiJS é melhor quando precisa de centenas de sprites + shaders; DOM é melhor quando os "personagens" são cards minimalistas.

## Layout de pastas (regra "evite arquivos muito grandes")

```
demos/clientes/<office-slug>/
├── <office-slug>.html              ← ~7KB, mínimo (skeleton + CSS + module boot)
└── js/                              ← módulos focados, ≤10KB cada
    ├── constants.js                STATUS, GRID, TILE, AGENTES, MESAS, STATUS_COLOR
    ├── utils.js                     hexCss, lerp, easeInOutCubic, gridToScreen, darken/lighten
    ├── state.js                     createState(), createAgent()
    ├── escritorio.js                buildEscritorio() — chão, paredes, mesas, café, estante
    ├── agentes.js                   createAgentSprite() — pernas/torso/braços/cabeça/label/aura
    ├── comportamento.js            positionForStatus() + tweenTo() + applyBehavior()
    ├── sse.js                       startRealtime({onEvent,onSnapshot,onConn})
    ├── hud.js                       renderSummary, renderSelected, pushFeedRow, setConnBadge
    └── boot.js                      Phaser.Scene que monta tudo e conecta SSE
```

Cada módulo ≤ 10KB, 1 responsabilidade, JSDoc no topo, funções puras exportadas. Total ~30KB de código próprio + Phaser bundled local.

## Padrão de Sprite (sem assets externos)

Cada agente é um `Phaser Container` (`scene.add.container(0, 0)`) com 5 partes:

| Parte | Como construir |
|-------|----------------|
| **Pernas** | dois retângulos finos `#34495e` |
| **Tronco** | retângulo `darken(cor, 0.3)` + duas linhas verticais brancas (jaleco) |
| **Braços** | container com 2 graphics, rotacionáveis em rad |
| **Cabeça** | losango (`beginPath/moveTo/lineTo/closePath/fillPath`) em `cor`, com highlight `lighten(cor, 0.18)` no triângulo superior, 2 retângulos pretos como olhos, retângulo como boca |
| **Aura** | elipse embaixo, cor = `STATUS_COLOR[status]` |
| **Label** | texto `Segoe UI 11px` com `stroke 3px` preto, ancorado em `(0.5, 1)` |
| **Hit-area** | `scene.add.zone(0, -16, 28, 48)` + `setInteractive({useHandCursor: true})` |

Origem do container = **pés do personagem**. Pernas -10 a 0; tronco -22 a -10; cabeça y=-22; label y=-36.

## Conversão isométrica

```js
const TILE = { W: 64, H: 32 };
function gridToScreen(gx, gy) {
  return { x: (gx - gy) * (TILE.W / 2), y: (gx + gy) * (TILE.H / 2) };
}
```

Mesas fixadas em (gx,gy): `{ gx: 2, gy: 2, label: 'Nutró' }`, etc. Cadeiras em `(mesa.gx + 1, mesa.gy)`. Café em `(12, 4)`, estante em `(1, 8)`.

## Comportamento por status

| Status | Posição | Animação |
|--------|---------|----------|
| `working` / `thinking` / `tool_call` / `delegating` | cadeira à frente da mesa | braço direito mexe, cabeça balança |
| `completed` / `idle` | corredor central / cantinho do café / estante | leve tilt + respiração = "bêbedo no café" |
| `waiting` / `error` | mesa de pé / mão na cabeça | idle, ou mão na cabeça |
| `offline` | longe, estático | invisível/separado |

**Regra `bêbedo no café`** (pedido do usuário, 12/09/2026): quando IDLE, agentes vão ao café com leve tilt + respiração suave — não é simulação vazia.

## Tween com cancelamento

```js
function tweenTo(scene, agent, toGx, toGy, dur = 1100) {
  if (agent.tweenHandle) { agent.tweenHandle.remove(); agent.tweenHandle = null; }
  return new Promise((resolve) => {
    const fromGx = agent.gx, fromGy = agent.gy;
    const obj = { t: 0 };
    const tw = scene.tweens.add({
      targets: obj, t: 1, duration: dur, ease: 'Sine.easeInOut',
      onUpdate: () => {
        agent.gx = lerp(fromGx, toGx, obj.t);
        agent.gy = lerp(fromGy, toGy, obj.t);
        setAgentGridPos(agent);
      },
      onComplete: () => { agent.tweenHandle = null; resolve(); },
    });
    agent.tweenHandle = tw;
  });
}
```

Cancelar tween anterior evita "pulo" quando o status muda rápido.

## QA workflow (validado 12/09/2026)

1. **Validar sintaxe** de cada módulo: `node -e 'new Function(fs.readFileSync(f,"utf8"))'` ou `node --input-type=module` para arquivos com `import`.
2. **JSDOM** com EventSource + fetch mockados para verificar se DOM reage a eventos.
3. **Firefox headless com `--virtual-time-budget=Nms`** para screenshot — **budget precisa ser ≥ 30000** para Phaser terminar init + tweens + animations em demo com 6 agentes.
4. **Inspeção visual** com `vision_analyze` em mobile (390×844) e desktop (≥1280×720).

### Pitfalls validados nesta sessão

- **PixiJS v8 com `await app.init({})` async** — Firefox `--screenshot` captura frame **antes** do canvas ser desenhado, mesmo com `--virtual-time-budget`. Workaround: trocar para Phaser 3 (sync) ou PixiJS v7 (`new PIXI.Application({...})` sync).
- **`Phaser.AUTO` em headless sem GPU** — tenta WebGL primeiro, falha silenciosamente, canvas fica vazio. Workaround: `type: Phaser.CANVAS` explícito. Ver `references/phaser-umd-es-modules-headless.md`.
- **`import Phaser from '/vendor/...'` retorna `undefined`** — Phaser é UMD, não tem `default` export. Workaround: `<script src="/vendor/phaser.min.js">` antes do module, depois `const Phaser = window.Phaser`. Ver `references/phaser-umd-es-modules-headless.md`.
- **Firefox `--virtual-time-budget` congela async JS** — `setTimeout`, `fetch`, `await import` não rodam após load event quando o virtual clock se esgota. Use Playwright Python com `page.wait_for_timeout()` para validar demos em CI. Ver `references/phaser-umd-es-modules-headless.md`.
- **`<script type="module">` via CDN `esm.sh`** — Firefox headless timeout antes do fetch resolver. Workaround: bundle local.
- **Vendor local em `tematicos/vendor/`** — Dockerfile precisa copiar explicitamente para `/usr/share/nginx/html/vendor/` (não implícito via COPY de `clientes/`).
- **Caminho relativo `import Phaser from '../../tematicos/vendor/...'`** — 404 no nginx. Workaround: **caminho absoluto** `import Phaser from '/vendor/phaser.min.js'`. Mesma regra para `./js/state.js` → `/clientes/<office>/js/state.js`.
- **`<template>.content.cloneNode` perde filhos em JSDOM** — alternativa é criar nós via `scene.add.container()` direto.
- **`fetch` em JSDOM** — não implementado por padrão. Harness precisa injetar mock.
- **Funções declaradas depois de usadas em módulos ES** — `gridToScreen` declarado no final de `escritorio.js` mas chamado em `drawFloor` no topo. Em strict mode ES modules, function declarations são hoisted, mas **arrow functions** e `function` expressadas como `const` não são. Se trocar por `const f = () => {...}` e referenciar antes da definição, trava silenciosamente. Workaround: declarar helpers no topo do módulo antes dos exports.

## Referências adicionais

- **`references/phaser-umd-es-modules-headless.md`** — padrão UMD+ES modules, `Phaser.AUTO` vs `CANVAS` em headless, Firefox `--virtual-time-budget` caveats, validação Node-only de módulos, CSP mínimo para Phaser 3.

## Hubs / padronização (autor: Igor)
- Padrão canônico TimeAutomático: vanilla JS, ≤10 KB por arquivo, JSDoc por módulo, sem React/Vue/Svelte, sem mega-monolitos. Demanda literal do usuário (12/09/2026): "código organizado em funções tudo em funções pra facilitar leitura e testes automatizados e tudo documentado" + "evite arquivos muito grandes".
- Cada função pura `export`ada (não closures anônimas) → testável isoladamente via `node --input-type=module -e "import('./file.js')"`.
- Diretorio de modulos por projeto: `demos/clientes/<slug>/js/*.js`.

## Integração com realtime-events

Esta skill é a **camada de renderização** que consome o pipeline `general/realtime-events`. Para demos Phaser isométricas (Banca de Saúde, escritórios 2.5D), usar:

```js
import { startRealtime } from './sse.js';
startRealtime({
  onEvent: (ev) => applyEvent(this, state, ev),
  onConn:  (status) => setConnBadge(status, ...),
  onSnapshot: (snap) => { /* hydrate state from snap.agents */ },
}, { officeId: OFFICE_ID });
```

Mapeie `agent.task.started` → `STATUS.WORKING`, etc. Tabela completa em `references/status-mapping.md`.

## CSP crítico para módulos locais

```html
<meta http-equiv="Content-Security-Policy"
  content="default-src 'self';
           script-src 'self' 'unsafe-inline' 'unsafe-eval' blob:;
           style-src 'self' 'unsafe-inline';
           img-src 'self' data: blob:;
           connect-src 'self' http://127.0.0.1:8765 https://*.tts.*;
           frame-ancestors 'none'; base-uri 'self'; form-action 'self'">
```

Sem `'unsafe-eval'` no `script-src`, Phaser 3 falha (eval usado internamente).

## Extensões futuras

- **Pathfinding A→B com corredor** — `positionForStatus` hoje teleporta o agente. Próximo passo: BFS próprio sobre o grid 2D.
- **Bubbles de fala entre agentes** — parcial (`a.parts.label.text = "💬"`). Próximo passo: seta SVG A→B curva entre containers + auto-fade após 5s.
- **PixiJS v7 sync** — se migrar para WebGL real, PixiJS v7 ainda tem `new PIXI.Application({})` síncrono.
- **Sprites Aseprite** — quando assets externos forem OK, gerar sheets Idle/Walk/Sit/Coffee e usar `scene.anims.create()`.

## Lições do usuário (sessão 12/09/2026)

1. **"Adiciona uma tarefa na fila q esse código precisa estar organizado em funções tudo em funções pra facilitar leitura e testes automatizados e tudo documentado"** — código de demos grandes = organizado em módulos focados, JSDoc no topo, funções puras exportáveis.
2. **"Evite arquivos muito grandes"** — quebra HTML/JS em módulos ≤ 10KB. Preferir 5+ arquivos pequenos a 1 monolito.
3. **"O gráfico não tá legal. E melhor como era antes eles sentados em cadeiras e andando pelos corredores bêbedo café"** — visual isométrico deve retratar personagens **sentados em cadeiras**, **andando pelos corredores**, e **indo ao cantinho do café bêbedo** (tilt + respiração) — não apenas pontos brilhantes em cards.
4. **"Personagens devem conseguir falar entre si"** — `agent.message` no SSE deve refletir seta A→B visível temporária com texto da conversa.
5. **"Os agentes q não são dela"** — usar agentes **do contexto real do escritório**, não nomes genéricos. Para Banca de Saúde do Igor: Dr. Nutrólogo, Dr. Cardiologista, Dra. Endocrinologista, Preparador Físico, Coach, Psicóloga (fonte: `~/.hermes/profiles/saude/SOUL.md`).
