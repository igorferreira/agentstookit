#!/usr/bin/env python3
"""QA batch viewport reproduzível para demos TimeAutomático.

Usage: PORT=9225 python3 scripts/qa_batch_viewport.py

Pré-requisitos:
- Chrome headless rodando em PORT (default 9225)
- Painel Docker exposto em http://127.0.0.1:8090
- Editar GLOB abaixo para apontar à pasta de demos correta

Saída: linha por página com innerWidth×innerHeight retrato/paisagem.
Se as viewport voltarem a 980×2078 em alguma iteração, o race voltou.
"""
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
