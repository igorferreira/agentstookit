# Consulta de Advogado no CNA (Cadastro Nacional da OAB) — método validado 10/09/2026

## Contexto
Quando Igor pedir "consulta advogado OAB/RJ XXXXX" (ex.: checar situação, nome completo,
endereço, sociedade do advogado de um caso), a fonte oficial é o CNA — `cna.oab.org.br`.

## Por que não dá pra usar a API direta
O CNA é uma SPA Angular. As rotas internas existem, mas exigem token reCAPTCHA v3 gerado no browser:
- `GET /cna-interno/api/advogado/search?Uf=RJ&Inscricao=NNNNNN` → retorna `items[]` com `nome`,
  `inscricao`, `tipoInscOab` e um `parametro` (hex codificado, necessário pro detail).
- `GET /cna-interno/api/advogado/detail?parametro=<hex>` → nome completo, situação, organização
  (subseção), logradouro/bairro/cidade/CEP, `sociedades[]` (nome + OAB), foto (base64 — descartar).
- Chamadas sem o header de token retornam `403 {"message":"Recaptcha token is missing"}`.

## Método que funciona (Chrome headless + CDP)
1. Subir Chrome isolado:
   `google-chrome --headless=new --remote-debugging-port=9223 --remote-allow-origins='*' \
     --user-data-dir=/tmp/chrome-cna --no-first-run --disable-gpu --disable-dev-shm-usage --no-sandbox about:blank`
   (`--remote-allow-origins='*'` é OBRIGATÓRIO — sem ele o websocket CDP devolve 403 no handshake).
2. Criar venv com websocket-client se não existir: `uv venv /tmp/wsvenv && uv pip install --python /tmp/wsvenv/bin/python websocket-client`
3. Via CDP: navegar a `https://cna.oab.org.br/`, preencher o input `formcontrolname="inscricao"`
   + select seccional (dispatch de eventos `input`/`change` pra Angular), clicar no botão "Pesquisar".
4. Habilitar `Network.enable` ANTES de clicar; interceptar `Network.requestWillBeSent` /
   `Network.responseReceived` das URLs `/cna-interno/api/advogado/*` e capturar o corpo com
   `Network.getResponseBody`. A requisição feita pela página JÁ leva o token reCAPTCHA.
5. Guardar o JSON (sem o campo `foto`) em `/tmp/oab_<nome>.json` e escrever a ficha `.md`.

### Código esqueleto (reusar)
```python
import json, urllib.request, websocket, time
tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9223/json/list').read())
tab = [t for t in tabs if t['type']=='page'][0]
ws = websocket.create_connection(tab['webSocketDebuggerUrl'], timeout=240)
mid = 0
def send(method, **params):
    global mid; mid += 1
    ws.send(json.dumps({"id":mid,"method":method,"params":params}))
    ws.settimeout(5)
    while True:
        try: r = json.loads(ws.recv())
        except Exception: return {'timeout': True}
        if r.get('id') == mid: return r

send('Page.navigate', url='https://cna.oab.org.br/'); time.sleep(8)
send('Network.enable')
# preencher inscrição e seccional via Runtime.evaluate (dispatch input/change)
# clicar Pesquisar; loop lendo Network.responseReceived com 'advogado' na URL
# → Network.getResponseBody para pegar search (obtém o `parametro`) e depois detail
```

### Pitfalls
- **O clique deve ser no `<li>` do card de resultado**, não num `<div>` genérico — o card é
  `li` clicável; clicar no div interno não dispara o service Angular.
- **O `parametro` do detail é por sessão** — navegar direto para uma URL com `parametro` antigo
  (ou copiado de outra sessão) cai em "Nenhum resultado encontrado". Repetir search → pegar o
  `parametro` fresco → interceptar o detail na MESMA sessão de página.
- `Runtime.evaluate` com `awaitPromise` numa chamada fetch própria NÃO resolve o token — o token
  só existe quando o próprio app Angular dispara a requisição (por isso interceptar, não chamar).
- Ao parsear o body do detail: `Network.getResponseBody` pode devolver `body` já como dict
  (não string) — tratar `isinstance(body, str)` antes de `json.loads`.

## Ano de formação do advogado (não consta no CNA)
O CNA não publica data de graduação. Estimar por:
1. **Série de inscrição**: matrículas OAB/RJ antigas (faixa ~70-80k) ≈ fim dos anos 1990/início
   dos 2000 (a OAB/RJ hoje passa de 180k).
2. **Primeiro registro público de atuação**: buscar o nome + OAB em diários oficiais
   (DOERJ/IOERJ/Jusbrasil) — o processo mais antigo em que aparece dá o piso de atuação.
3. Entregar como **estimativa fundamentada** ("formado provavelmente entre ~1996-2001, atuante
   há 20+ anos"), nunca como dado oficial; data exata só via OAB/RJ ou o próprio advogado.

## Onde salvar
- Ficha do advogado: dentro da pasta do processo (ex.: `processo_marica_igor/FICHA-ADVOGADO-<NOME>-OAB<NUM>.md`),
  não solta em `legal_publico/`. Inclui: dados OAB, endereço, sociedade, contato, papel no caso
  e o método de consulta no rodapé.