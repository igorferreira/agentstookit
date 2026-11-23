# QA Funcional de Demos HTML via CDP (clique real)

## Por quê
Screenshot e `node -e "new Function(...)"` validam SINTAXE e COMPOSIÇÃO, não comportamento. Um `ReferenceError`/TDZ em runtime mata o script inteiro e listeners definidos depois nunca anexam — o botão "não faz nada" sem erro visível para o usuário.

## Setup

```bash
google-chrome --headless=new --remote-debugging-port=9223 --remote-allow-origins='*' \
  --user-data-dir=/tmp/chrome-qa "http://127.0.0.1:8090/pagina.html" &
# pegar target de PÁGINA (ignorar chrome-extension://):
curl -s http://127.0.0.1:9223/json
```

Cliente WS mínimo (stdlib Python) — padrão usado e validado:

```python
import json, urllib.request, socket, base64, os, struct
from urllib.parse import urlparse
targets = json.load(urllib.request.urlopen('http://127.0.0.1:9223/json'))
ws = [t for t in targets if 'page' in t['type'] and 'chrome-extension' not in t['url']][0]
u = urlparse(ws['webSocketDebuggerUrl']); s = socket.create_connection((u.hostname, u.port))
key = base64.b64encode(os.urandom(16)).decode()
s.send((f"GET {u.path} HTTP/1.1\r\nHost: {u.hostname}:{u.port}\r\nUpgrade: websocket\r\n"
        f"Connection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n").encode())
s.recv(4096)
def send(sock, data):
    p = data.encode(); m = os.urandom(4); h = b'\x81'; ln = len(p)
    h += bytes([0x80|ln]) if ln < 126 else bytes([0x80|126]) + struct.pack('>H', ln)
    sock.send(h + m + bytes(b ^ m[i%4] for i, b in enumerate(p)))
def recv(sock):
    hdr = sock.recv(2); ln = hdr[1] & 0x7f
    if ln == 126: ln = struct.unpack('>H', sock.recv(2))[0]
    d = b''
    while len(d) < ln: d += sock.recv(ln - len(d))
    return d.decode()
mid = 0
def cdp(method, params=None):
    global mid; mid += 1
    send(s, json.dumps({'id': mid, 'method': method, 'params': params or {}}))
    while True:
        r = json.loads(recv(s))
        if r.get('id') == mid: return r
ev = lambda e: cdp('Runtime.evaluate', {'expression': e, 'returnByValue': True}) \
        .get('result', {}).get('result', {}).get('value')
```

## Roteiro de QA funcional

1. **Capturar erros de script** (o silencioso é o pior):
   `cdp('Runtime.enable'); cdp('Page.enable')` → `Page.reload` (ou `Page.navigate` com `?v=<timestamp>` anti-cache) → coletar `Runtime.exceptionThrown`.
   **Zero erros é pré-requisito** — se houver qualquer erro, corrigir antes de testar interações.
2. **Clique real no botão**:
   `ev("document.getElementById('msg').value='texto teste'")`
   `ev("document.getElementById('btnEnviar').click()")`
   → contar/ler os elementos produzidos: `ev("[...document.querySelectorAll('.bubble')].map(b=>b.textContent.slice(0,60)).join(' || ')")`
   → verificar efeitos colaterais (input limpo, `document.querySelectorAll('.robo.sentado').length`).
3. **Se `click()` não dispara mas `funcao()` direta funciona** → o listener não anexou ⇒ há erro de script ANTES da linha do `addEventListener`. Buscar o erro com o roteiro 1, não com força bruta.
4. **Se um símbolo reporta "Cannot access X before initialization"** → TDZ/ordem de declaração ou duplicação de `const` após refatoração regex; conferir o arquivo que o SERVIDOR entrega (`curl URL | sed -n 'N,Mp'`) contra o nº de linha do stack.
5. **Divergência container vs navegador**: `curl` da URL mostra versão nova mas o erro cita linha da versão velha ⇒ cache do navegador; navegar com querystring anti-cache e re-testar.

## Lições do caso real (11/09/2026, escritórios Sims)

- 3 bugs raiz só apareceram com este método: `trocarTarefa` apagada por refatoração regex, `walk()` chamada sem definição, TDZ de `msg`. Sintaxe validava OK em todos — o erro era runtime.
- `.click()` programático dispara listeners; se o script morreu antes do `addEventListener`, o clique é no-op silencioso. O sintoma "despachar existe, botão existe, clique não gera nada" = listener nunca anexado.
- Sempre rodar o teste ATÔMICO numa única `Runtime.evaluate` (set value + click + count na mesma expressão) para eliminar falsos negativos de timing entre chamadas CDP.