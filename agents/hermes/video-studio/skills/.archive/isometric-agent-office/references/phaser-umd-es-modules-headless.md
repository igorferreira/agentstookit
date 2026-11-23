# Phaser UMD + ES Modules + Headless rendering

Three gotchas que custaram ~2h nesta sessão e que qualquer demo Phaser nova vai encontrar.

## 1. Phaser UMD não tem `default` export

Phaser 3 é distribuído como **UMD bundle** (`phaser.min.js`). O header é:
```js
!function(t,e){
  "object"==typeof exports&&"object"==typeof module ? module.exports=e()
  : "function"==typeof define&&define.amd ? define("Phaser",[],e)
  : "object"==typeof exports ? exports.Phaser=e()
  : t.Phaser=e()
}(this, ...)
```

**Não existe `export default Phaser`** — só há side-effects (atribuição em `window.Phaser`).

Tentar `import Phaser from '/vendor/phaser.min.js'` em ES module falha silenciosamente — `Phaser` fica `undefined`. Isso é um **bug clássico** que aparece como "Phaser carregado mas não funciona".

### ✅ Padrão correto (2 passos)

```html
<!-- 1. Carregar como UMD via <script> clássico (síncrono, antes do module) -->
<script src="/vendor/phaser.min.js"></script>

<script type="module">
  // 2. Acessar via window.Phaser
  const Phaser = window.Phaser;
  const game = new Phaser.Game({...});
</script>
```

### ❌ Anti-patterns (causam `Phaser undefined`)

| Forma | Falha |
|-------|-------|
| `import Phaser from '/vendor/phaser.min.js'` | UMD não tem `default` export |
| `import * as Phaser from '/vendor/phaser.min.js'` | retorna namespace vazio |
| `const Phaser = await import('/vendor/phaser.min.js')` | retorna `{Phaser: ..., default: undefined}` (Phaser fica em `.Phaser`) |
| `<script type="module" src="...">` direto | funciona, mas bloqueia init do UMD se vier antes |

### Verificação rápida

```js
// Coloque isso antes de usar Phaser:
if (typeof Phaser === 'undefined') throw new Error('Phaser not loaded — check <script src> placement');
if (typeof Phaser.Scene !== 'function') throw new Error('Phaser global is broken');
```

## 2. `Phaser.AUTO` vs `Phaser.CANVAS` em headless

`Phaser.AUTO` tenta WebGL primeiro; se falhar, cai para CANVAS. Em **headless server sem GPU**, WebGL falha e o canvas fica vazio. **Mas:** o fallback do AUTO é silencioso — você não vê erro, só um canvas em branco.

### Workaround: forçar `Phaser.CANVAS`

```js
new Phaser.Game({
  type: Phaser.CANVAS,  // ← EXPLICITAMENTE CANVAS, não AUTO
  ...
});
```

Resultado testado em 12/09/2026 (Linux headless, sem GPU): canvas renderiza normalmente (círculos, retângulos, texto, tweens).

Se você precisa de WebGL de verdade (shaders, post-processing), instale Mesa/swiftshader no servidor ou rode em browser real com GPU.

## 3. Firefox `--virtual-time-budget` congela async JS

`firefox --headless --screenshot --virtual-time-budget=30000 ...` é o padrão para gerar screenshots em CI. Mas:

- O **virtual clock avança até o budget esgotar**
- Ao esgotar, Firefox **pausa o real clock também**
- Consequência: `setTimeout(100)`, `await fetch(...)`, `await import(...)` agendados durante o load **nunca rodam** porque o virtual clock só avança durante a fase síncrona
- Você vê: "Phaser importou mas cena vazia", "setTimeout nunca disparou", "fetch nunca resolveu"

### Evidência (12/09/2026)

Testei setTimeout de 100ms, 500ms, 2000ms, 5000ms — **nenhum disparou**. Mas `node --input-type=module -e "import('./file.js')"` resolve tudo em <100ms (não usa virtual clock).

### Mitigações

| Estratégia | Eficácia |
|-----------|----------|
| Aumentar `--virtual-time-budget` para 60000+ | ❌ Não ajuda — o clock congela no mesmo ponto |
| Usar `--virtual-time-budget=0` (sem virtual clock) | ⚠️ Possível, mas perde a precisão de timing |
| Usar Playwright com `page.wait_for_timeout(8000)` | ✅ Funciona — Playwright usa real clock |
| Rodar browser **real** (Xvfb + Chromium não-headless) | ✅ Funciona, mas pesado |
| Testar via `node --input-type=module` (sem browser) | ✅ Valida sintaxe + imports, mas não renderiza canvas |

### Workflow recomendado para validar demos Phaser

1. **Sintaxe e imports**: `node --input-type=module -e "import('./file.js'); console.log('OK')"` — falha em <1s se houver erro
2. **Render real**: Playwright Python (`sync_playwright`) com `page.wait_for_timeout(5000)` antes do screenshot
3. **CI/CD**: Playwright headless **com** `wait_for_timeout` é o caminho confiável

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://localhost:8090/demo.html')
    page.wait_for_timeout(5000)  # ← CRÍTICO, dá tempo pro Phaser inicializar
    page.screenshot(path='/tmp/demo.png')
    browser.close()
```

## 4. Validação Node para módulos ES

Validar que imports/sintaxe de cada módulo JS estão OK antes de tentar no browser:

```bash
node --input-type=module -e "
  const m = await import('/path/to/module.js');
  console.log('Exports:', Object.keys(m).join(', '));
"
```

Use isso para cada módulo do escritório. Falha em <100ms, não em 30s como no browser.

## 5. CSP mínimo para Phaser 3

Phaser usa `eval()` internamente (em alguns hot paths do scene graph). CSP sem `'unsafe-eval'` quebra silenciosamente:

```html
<meta http-equiv="Content-Security-Policy" content="
  default-src 'self';
  script-src 'self' 'unsafe-inline' 'unsafe-eval' blob:;
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: blob:;
  connect-src 'self' http://127.0.0.1:8765;
  frame-ancestors 'none';
  base-uri 'self';
  form-action 'self'
">
```

Sem `'unsafe-eval'`: scene tree falha ao criar filhos, console mostra `EvalError`, canvas fica vazio.