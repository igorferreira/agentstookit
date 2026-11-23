# SSE Debugging — realtime-events

Notas de debugging destravadas durante a construção do pipeline realtime.

## JSDOM quebra `<template>.content.cloneNode` em algumas versões

**Bug**: `tpl.content.firstElementChild.cloneNode(true)` retorna station sem `.face`, `.head`, `.eye`, `.ant`.

```js
// QUEBRA EM JSDOM:
const node = tpl.content.firstElementChild.cloneNode(true);
node.querySelector('.face .head') // null
```

**Causa**: JSDOM (< 25) representa `<template>.content` como DocumentFragment mas não clona os filhos corretamente em algumas configs de parser.

**Fix validado 12/09/2026**: Dupla estratégia.

```html
<!-- Template para browsers reais -->
<template id="agent-template">
  <article class="station">...toda estrutura com filhos...</article>
</template>

<!-- Reference node para JSDOM/tests -->
<div hidden id="agent-ref" style="display:none;position:absolute;left:-9999px">
  <article class="station">...mesma estrutura...</article>
</div>
```

```js
try {
  node = tpl.content.firstElementChild.cloneNode(true);
  // valida: precisa ter .face3d .cubo
  if (!node.querySelector('.face3d .cubo')) throw new Error('template vazio');
} catch (_) {
  const ref = document.getElementById('agent-ref');
  node = ref.firstElementChild.cloneNode(true);
}
```

**Regra de ouro**: se o template é usado em testes JSDOM, SEMPRE criar fallback DOM explícito.

---

## `querySelector` rejeita pseudo-elemento

**Bug**:
```js
face.querySelector('.ant::after') // null
face.querySelector('.ant') // funciona
```

**Causa**: `querySelector` segue CSS selector spec; `::after` é pseudo-elemento CSS que não existe como nó no DOM.

**Fix**: CSS puro para o que era ::after:
```css
.ant::after { content: ''; ... } /* funciona */
```

---

## Firefox headless sem render

**Bug**: `--screenshot` sai em ~26 KB antes do JS executar — sempre branco/vazio.

**Fix validado 12/09/2026**: usar `--virtual-time-budget=N(ms)`:
```bash
firefox --headless --window-size 390,844 \
  --virtual-time-budget=12000 \
  --screenshot out.png \
  'http://127.0.0.1:8090/escritorio_banca_saude.html'
```

12000ms (12s) é suficiente para fetch(/snapshot) + ~30s de SSE + render. Sem isso, screenshot captura só o DOM inicial estático.

**Atenção**: `virtual-time-budget` é experimental e está em headless mode. Rodar em xvfb ou em CI headless real pode dar resultado diferente.

---

## nginx buffering mata SSE

**Bug**: Cliente conecta em `https://x.ngrok-free.app/events` mas recebe **zero eventos**. Logs nginx mostram 200 OK + conexão longa, mas o front-end não atualiza.

**Causa**: nginx por padrão bufferiza respostas de upstream. SSE envia chunks incrementais; sem desabilitar buffer, nginx acumula tudo e libera só no disconnect.

**Fix validado 12/09/2026**:
```nginx
location /events {
  proxy_pass http://realtime:8765/events;
  proxy_buffering off;
  proxy_cache off;
  proxy_read_timeout 24h;
  proxy_send_timeout 24h;
  proxy_set_header Connection '';
  add_header X-Accel-Buffering "no" always;
  add_header Cache-Control "no-store" always;
}
```

---

## Smoke-test ngrok público

**Validação**: depois de configurar nginx + Docker, validar que o tunnel público realmente entrega SSE, não só HTTP simples.

```bash
URL=https://x.ngrok-free.app
curl -fsS -o /dev/null -w 'HTTP %{http_code} time=%{time_total}s\n' $URL/escritorio_banca_saude.html
curl -fsS $URL/realtime-health  # deve retornar JSON {"status":"ok", ...}

# Captura SSE via HTTPS público (timeout 60s)
timeout 60 curl -fsSN "$URL/events?office=banca-saude" > /tmp/sse_public.txt 2>/dev/null
# wc -l /tmp/sse_public.txt  # ~70+ linhas por rodada do simulador (1 rodada = 36 eventos = ~108 linhas por header event:/id:/data:)
```

**Esperado por rodada do simulador (~20s)**:
- 1 `banca.started`
- 1 `agent.task.started` (angelica)
- 5 `agent.delegated` (1 para cada sub-agente)
- 5 `agent.task.started` (sub-agentes)
- 1 `agent.tool.started` (oswaldo → AWS Emulator)
- 1-2 `agent.message` (conversas A↔B)
- 5 `agent.task.completed` (sub-agentes)
- 1 `agent.tool.completed`
- 1 `agent.status.changed` (angelica consolidando)
- 1 `banca.completed`
- 1 `agent.status.changed` (angelica idle)

~28 eventos × 4 linhas (`:ok\n\nevent:\nid:\ndata:\n`) ≈ 112 linhas.

---

## Reconstrução Docker sem rebuild full

**Atalho que economiza ~30s** quando só HTML/CSS mudou:
```bash
docker compose up -d --force-recreate painel
```

Quando Python ou nginx.conf mudou:
```bash
docker compose build painel && docker compose up -d --force-recreate painel
```

Quando o painel não rebuilda nginx:
- O `COPY docker/nginx.conf` está com CACHED no build
- `docker compose build --no-cache painel` força full rebuild
- OU editar o nginx.conf (qualquer espaço) invalida o CACHE

---

## Reset rápido do sidecar (sem matar)

Apaga state e re-leitura do início do JSONL:
```bash
rm -f ~/.cache/timeautomatico/sidecar_state.json
# mata o processo antigo (se em background) e sobe de novo
```

Se foi via Docker:
```bash
docker compose restart realtime
```
