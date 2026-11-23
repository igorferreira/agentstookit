# Phaser 3 + Docker + SSE — Workflow de Debug

## Problemas recorrentes nesta sessão (12/09/2026)

### 1. Canvas vazio + bootstrap mata

**Sintoma:** Screenshot 175KB (header+HUD renderizam, canvas azul escuro vazio).

**Causas (em ordem de probabilidade):**

| # | Causa | Diagnóstico | Fix |
|---|-------|-------------|-----|
| 1 | `import Phaser from '/vendor/...'` | `Phaser` fica `undefined` (UMD não tem default export) | `<script src>` + `const Phaser = window.Phaser` |
| 2 | `void sy;` fora do escopo do `const` | `ReferenceError: sy is not defined` mata top-level module | Remover `void sy;` ou mover dentro do loop |
| 3 | `Phaser.AUTO` sem GPU | WebGL falha silenciosamente, canvas vazio | `type: Phaser.CANVAS` |
| 4 | CSP bloqueando `'unsafe-eval'` | Phaser falha ao criar scene tree | Adicionar `'unsafe-eval'` ao `script-src` |

**Workflow de diagnóstico (ordem):**

```bash
# 1. Verifica se Phaser carrega como global
curl -fsS http://127.0.0.1:8090/banca_saude.html | grep -o 'phaser\|Phaser' | head -3

# 2. Verifica se módulos ES carregam (node test)
node --input-type=module -e '
  const c = await import("/path/to/constants.js");
  console.log("constants OK:", Object.keys(c));
'

# 3. Verifica CSP no HTML
curl -fsS http://127.0.0.1:8090/banca_saude.html | grep -o 'Content-Security-Policy="[^"]*"'

# 4. Firefox headless screenshot
timeout 60s firefox --headless --no-remote --profile /tmp/ff --window-size=1440,900 \
  --virtual-time-budget=30000 --screenshot /tmp/test.png 'http://127.0.0.1:8090/banca_saude.html'
stat -c '%s' /tmp/test.png  # >150KB = canvas vazio
```

### 2. Realtime SSE "reconectando" em loop

**Sintoma:** Header mostra `🟡 reconectando` (ponto amarelo piscando), 0 EventSources ativos.

**Causa:** Container `realtime` não tem porta mapeada no host.

**Fix:**

```yaml
# docker-compose.yml
realtime:
  ports: ["8765:8765"]  # ← ADICIONAR ESTA LINHA
```

```bash
# Verificar se realtime responde
curl -s http://127.0.0.1:8765/health  # → {"status": "ok"}

# Verificar se simulador está rodando
ps aux | grep dev_simulator | grep -v grep

# Verificar JSONL com eventos
tail -3 ~/.cache/timeautomatico/events.jsonl
```

**Se ainda não conecta:**

1. Reiniciar container: `docker compose up -d --force-recreate realtime`
2. Verificar logs: `docker logs timeautomatico-realtime --tail 20`
3. Verificar se nginx proxy está configurado (location /events → http://realtime:8765/events)

### 3. CSP warning: `https://*.tts.*`

**Sintoma:** Console warning: `Content-Security-Policy: Couldn't parse invalid host https://*.tts.*`

**Causa:** Wildcard `*.tts.*` não é válido no CSP. O wildcard só funciona no final do host (`*.example.com`), não no meio.

**Fix:**

```html
<!-- ANTES (invalido) -->
<meta http-equiv="Content-Security-Policy" content="
  connect-src 'self' http://127.0.0.1:8765 https://*.tts.*; ...">

<!-- DEPOIS (correto) -->
<meta http-equiv="Content-Security-Policy" content="
  connect-src 'self' http://127.0.0.1:8765 https://localhost:8777; ...">
```

**Regra:** CSP `connect-src` só aceita:
- `'self'`
- Protocolo + host exato (`https://api.example.com`)
- Wildcard no final (`https://*.example.com`)
- Portas específicas (`https://example.com:8443`)

**NUNCA usar:** `https://*.tts.*` (wildcard no meio)

### 4. Agentes sobrepostos no canto

**Sintoma:** Todos os 6 agentes aparecem empilhados no canto superior esquerdo.

**Causa:** Posição IDLE calculada fora do loop de criação, mas `createAgent()` usa `mesa.gx + 1` como gx inicial. Se `positionForStatus()` retorna posição IDLE, mas `createAgent()` ignora, agentes ficam na mesma posição.

**Fix:**

```js
// boot.js — calcular IDLE ANTES de criar sprite
for (const def of AGENTES) {
  const mesa = MESAS[def.mesaIdx];
  const idleSpot = positionForStatus(def, STATUS.IDLE);  // ← calcular primeiro
  
  const a = createAgent(def, mesa);
  a.gx = idleSpot.gx;  // ← sobrescrever posição inicial
  a.gy = idleSpot.gy;
  
  createAgentSprite(this, a);
  state.agents.set(def.id, a);
}
```

**IDLE_SPOTS deve ter ≥ N posições** (onde N = número de agentes):

```js
const IDLE_SPOTS = [
  { gx: 11, gy: 4 },   // café
  { gx: 3,  gy: 8 },   // estante
  { gx: 5,  gy: 4 },   // corredor
  { gx: 9,  gy: 8 },   // área inferior direita
  { gx: 7,  gy: 5 },   // meio do corredor
  { gx: 10, gy: 3 },   // perto do café
];
```

### 5. Câmera cortando estante ou criando faixa preta

**Sintoma:** estante não aparece, escritório fica espremido para a direita e uma faixa preta/vazia ocupa parte do canvas, principalmente no mobile.

**Causa:** `camera.setPosition(x, y)` desloca o VIEWPORT da câmera dentro do canvas; não centraliza o mundo. A região fora do viewport deixa de ser renderizada. Além disso, o mundo isométrico usa coordenadas X negativas.

**Fix:** manter o viewport em `(0,0,width,height)`, calcular zoom pelo tamanho disponível e usar `centerOn()` para enquadrar o mundo:

```js
function fitCamera(scene, width, height) {
  const bounds = { left: -320, right: 448, top: -76, bottom: 376 };
  const worldW = bounds.right - bounds.left;
  const worldH = bounds.bottom - bounds.top;
  const zoom = Math.min(1.15, (width - 24) / worldW, (height - 24) / worldH);

  const cam = scene.cameras.main;
  cam.setViewport(0, 0, width, height);
  cam.setZoom(Math.max(0.42, zoom));
  cam.centerOn((bounds.left + bounds.right) / 2,
               (bounds.top + bounds.bottom) / 2);
}
```

Chamar no `create()` e registrar `scene.scale.on('resize', size => fitCamera(scene, size.width, size.height))`. **Nunca usar `camera.setPosition()` para enquadrar o mundo.**

## Checklist de QA pós-deploy

```bash
# 1. Docker
docker compose ps  # todos UP
docker port timeautomatico-realtime  # 8765:8765

# 2. Realtime
curl -s http://127.0.0.1:8765/health  # → {"status": "ok"}

# 3. Simulador
ps aux | grep dev_simulator | grep -v grep  # deve estar rodando
tail -5 ~/.cache/timeautomatico/events.jsonl  # deve ter eventos

# 4. Frontend
curl -fsS http://127.0.0.1:8090/banca_saude.html | grep -o 'phaser\|Phaser'  # deve ter
curl -fsS http://127.0.0.1:8090/banca_saude.html | grep -o 'Content-Security-Policy="[^"]*"'  # sem *.tts.*

# 5. Screenshot (Firefox headless)
timeout 60s firefox --headless --no-remote --profile /tmp/ff --window-size=1440,900 \
  --virtual-time-budget=30000 --screenshot /tmp/final.png 'http://127.0.0.1:8090/banca_saude.html'
stat -c '%s' /tmp/final.png  # <150KB = canvas renderizou

# 6. Screenshot (Playwright Python)
python3 -c "
import sys; sys.path.insert(0, '/home/igorferreira/.local/lib/python3.12/site-packages')
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    page = browser.new_page()
    page.goto('http://127.0.0.1:8090/banca_saude.html')
    page.wait_for_timeout(10000)
    page.screenshot(path='/tmp/pw.png')
    browser.close()
"
```

## Referências

- `references/cdp-batch-viewport-race.md` — bug de viewport em QA batch
- `references/auditoria-command-center-vanilla.md` — auditoria de estado do painel
- `scripts/qa_batch_viewport.py` — QA batch em loop
