# CDP batch viewport race — debugging log e workaround

Sintoma: ao rodar QA sequencial por várias páginas via `Emulation.setDeviceMetricsOverride` + `Page.navigate` no mesmo Chrome headless, a partir da 2ª iteração `innerWidth`/`innerHeight` voltam ao tamanho físico da janela (980×2078 retrato, 980×463 paisagem), a página renderiza sem agentes e todo o batch falha.

## O que foi tentado e o que aconteceu

Tentativa | Resultado
---|---
`setDeviceMetricsOverride({width:384,height:814,...})` + `Page.navigate` em **script único** | ✅ funciona — `innerWidth=384, agentes=7`
Mesma sequência em **loop de 3+ páginas** | ❌ a 2ª iteração retorna `innerWidth=980`
`clearDeviceMetricsOverride` antes do `set` | ❌ reverte para 980×2078 (chave: clear RESETA para o tamanho da janela física, não para "default")
`Network.setUserAgentOverride` mobile antes de nav | ❌ UA muda, mas viewport continua 980×2078
Pre-warm com `Page.navigate({url:'about:blank'})` antes do loop | ❌ não ajuda — clear sobrescreve
`Page.reload()` logo após `Page.navigate` | ❌ funciona ISOLADAMENTE mas em loop volta a falhar
Drenar eventos do WebSocket entre chamadas | ❌ não resolve
Fresh chrome por iteração (subir e matar processo) | ⚠️ funciona mas demora 5–10s por iteração (inviável para 8+ páginas)
**`Browser.setWindowBounds {windowId, bounds:{width,height}}` ANTES de `setDeviceMetricsOverride`** | ✅ **WORKAROUND VALIDADO**

## Diagnóstico

`Emulation.setDeviceMetricsOverride` no Chrome headless aceita o valor sem erro e `Page.captureScreenshot` mostra a viewport correta, mas o **renderer da página continua usando o tamanho da janela física do chrome**. `Page.navigate` lê o tamanho da janela física para definir `innerWidth`/`innerHeight`. O override só "cola" depois que a janela física é redimensionada — daí a necessidade de `Browser.setWindowBounds` antes.

Sinais observados que confirmam o diagnóstico:
- `innerWidth=980, innerHeight=2078` ≈ 384×2.55 e 814×2.55 (Pixel 5 chrome default)
- `screen.width=800, screen.height=600` no `clearDeviceMetricsOverride` → chrome window real é 800×600
- Em test isolado o `setDeviceMetricsOverride` "cola" porque o chrome está em estado inicial limpo; em loop o estado já tem override anterior pendente

## Workaround validado (script reproduzível)

`scripts/qa_batch_viewport.py`:

```python
import socket, struct, base64, os, time, json, urllib.request
from urllib.parse import urlparse

PORT = 9225  # headless dedicado em porta não-conflitante
T = [x for x in json.load(urllib.request.urlopen(f'http://127.0.0.1:{PORT}/json')) if x.get('type') == 'page'][0]
u = urlparse(T['webSocketDebuggerUrl'])
s = socket.socket(); s.settimeout(15); s.connect((u.hostname, u.port))
k = base64.b64encode(os.urandom(16)).decode()
s.send((f'GET {u.path} HTTP/1.1\r\nHost:{u.hostname}:{u.port}\r\n'
        f'Upgrade:websocket\r\nConnection:Upgrade\r\n'
        f'Sec-WebSocket-Key:{k}\r\nSec-WebSocket-Version:13\r\n\r\n').encode()); s.recv(4096)

def send(o):
    p = json.dumps(o).encode(); m = os.urandom(4); n = len(p)
    h = b'\x81' + (bytes([0x80|n]) if n < 126 else bytes([0xfe]) + struct.pack('>H', n))
    s.send(h + m + bytes(b ^ m[i%4] for i,b in enumerate(p)))
def recv():
    h = s.recv(2); n = h[1] & 127
    if n == 126: n = struct.unpack('>H', s.recv(2))[0]
    d = b''
    while len(d) < n: d += s.recv(n - len(d))
    return json.loads(d.decode())
i = 0
def cdp(m, p=None):
    global i; i += 1; z = i; send({'id': z, 'method': m, 'params': p or {}})
    while True:
        r = recv()
        if r.get('id') == z: return r.get('result', {})

cdp('Page.enable'); cdp('Runtime.enable')
WINDOW_ID = cdp('Browser.getWindowForTarget', {}).get('windowId', 1)

def nav(w, h, page):
    # 1. Redimensionar a janela FÍSICA primeiro
    cdp('Browser.setWindowBounds', {'windowId': WINDOW_ID, 'bounds': {'width': int(w), 'height': int(h)}})
    time.sleep(0.3)
    # 2. Só então aplicar override de emulação
    cdp('Emulation.setDeviceMetricsOverride', {'width': int(w), 'height': int(h),
        'deviceScaleFactor': 1, 'mobile': int(w) < 900, 'screenWidth': int(w), 'screenHeight': int(h)})
    cdp('Network.setUserAgentOverride', {'userAgent':
        'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Mobile Safari/537.36'})
    cdp('Page.navigate', {'url': f'http://127.0.0.1:8090/{page}?inv={time.time()}'})
    time.sleep(3.5)

# Loop: agora funciona para QUALQUER número de páginas
import glob
for page in glob.glob('/home/igorferreira/projetos/hermes-as-service/demos/**/*.html', recursive=True):
    nav(384, 814, page)
    r = cdp('Runtime.evaluate', {'expression':
        'JSON.stringify({iw:innerWidth,ih:innerHeight,agents:document.querySelectorAll(".humano").length})',
        'returnByValue': True}).get('result', {}).get('value')
    print(page, r)  # sempre 384×814 com agentes renderizados
    nav(814, 384, page)
    r = cdp('Runtime.evaluate', {'expression':
        'JSON.stringify({iw:innerWidth,ih:innerHeight})', 'returnByValue': True}).get('result', {}).get('value')
    print(page, r)
```

## Subir Chrome headless limpo (workaround #2)

Quando `~/.local/bin/browser-use-real` (porta 9222) trava em "aceita TCP mas não responde HTTP":

```bash
pkill -9 -f "chrome.*--type=zygote"
google-chrome \
  --headless=new --disable-gpu --no-sandbox --no-first-run \
  --user-data-dir=/tmp/chrome-qa-$(date +%s) \
  --remote-debugging-port=9225 --remote-allow-origins='*' \
  --disable-extensions --disable-background-networking --no-default-browser-check \
  --disable-component-update --disable-default-apps --disable-sync \
  --metrics-recording-only --no-pings \
  about:blank > /tmp/chrome-qa.log 2>&1 &
sleep 3
curl -m 6 http://127.0.0.1:9225/json/version  # deve devolver "Chrome/..."
```

Portas para tentar em ordem: 9223, 9224, 9225, 9226 (a 9222 está ocupada pelo chrome real do usuário).