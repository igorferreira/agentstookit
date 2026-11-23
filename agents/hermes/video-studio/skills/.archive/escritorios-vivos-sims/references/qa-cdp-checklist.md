# QA CDP Checklist — Escritórios Vivos (validado 11/09/2026)

Sequência real usada para provar o botão ENVIAR, o zoom e o alinhamento. Chrome headless com CDP:

```bash
google-chrome --headless=new --remote-debugging-port=9223 --remote-allow-origins='*' \
  --user-data-dir=/tmp/chrome-qa "http://127.0.0.1:8090/<pagina>.html?v=N" &
```

## 1. Pegar o target certo

`/json` lista extensões também — filtrar `type==='page'` e excluir URLs `chrome-extension://`. Um teste que bateu na extensão devolveu `None` para tudo.

## 2. Provar o botão ENVIAR (não basta screenshot)

```python
ev = lambda e: cdp('Runtime.evaluate', {'expression': e, 'returnByValue': True}).get('result',{}).get('result',{}).get('value')
ev("document.getElementById('msg').value='preço camisa'")
ev("document.getElementById('btnEnviar').click()")
# esperar ~0.5s e checar:
ev("[...document.querySelectorAll('.bubble.me')].length")      # bolha IGOR apareceu
ev("[...document.querySelectorAll('.bubble:not(.me)')].length") # resposta do agente
ev("document.getElementById('msg').value===''")                 # input limpo
```

## 3. Capturar erros de script (a causa nº1 de "botão morto")

```python
cdp('Runtime.enable')
cdp('Page.enable'); cdp('Page.reload')
# coletar r['method']=='Runtime.exceptionThrown' em todas as respostas
```

Bugs reais achados assim: função perdida em refatoração (`trocarTarefa` undefined matava `sentar()` → script morria antes do `addEventListener` do botão); `walk` órfã; TDZ de `msg`; array `('a','b')` em vez de `['a','b']` → banner "undefined undefined".

## 4. Provar o zoom

```python
ev("document.getElementById('zm+').click(); document.getElementById('zoomPct').textContent")  # 110%
ev("document.getElementById('office').style.transform")  # scale(1.1)
ev("(()=>{const e=new WheelEvent('wheel',{deltaY:-100,ctrlKey:true,cancelable:true}); window.dispatchEvent(e); return document.getElementById('zoomPct').textContent})()")
```

## 5. QA visual por rodada

```bash
google-chrome --headless --screenshot=/tmp/qa_desk.png --window-size=1400,900 "http://127.0.0.1:8090/<p>.html?v=N"
google-chrome --headless --screenshot=/tmp/qa_mob.png  --window-size=390,844  "http://127.0.0.1:8090/<p>.html?v=N"
```

Analisar cada screenshot com vision_analyze (nota 1-10 + falhas). Iterar v1→vN.
Versão headless captura ~1-2s após load: timers >2s não terão rodado — por isso grade determinística + ResizeObserver (ver SKILL.md).

## 6. Reconstruir antes de QA

O container copia o HTML — editar sem rebuild = testar versão antiga:

```bash
cd demos/docker && docker compose build painel && docker compose up -d --force-recreate painel
```

Usar `?v=N` na URL contra cache do navegador.

## 7. Validar JS de todos os arquivos após qualquer passada de edição

```bash
for f in principal/*.html tematicos/*.html clientes/*.html; do
  node -e "const s=require('fs').readFileSync('$f','utf8');new Function(s.match(/<script>([\s\S]*?)<\/script>/)[1]);console.log('$f OK')"
done
```