---
name: interactive-html-demos
description: Use ao criar demos HTML animadas com Docker, ngrok e QA CDP.
---

# Demos HTML interativas (escritórios vivos / painéis animados)

Padrão validado no projeto TimeAutomático (`~/projetos/hermes-as-service/demos/`): páginas HTML únicas, vanilla JS + CSS animado, servidas por Docker (nginx :8090) + TTS Piper em container irmão, expostas via ngrok.

## Arquitetura canônica
- `principal/` (uso interno), `tematicos/` (demos seguras pra clientes — SEM dados pessoais do Igor), `clientes/` (demos por cliente), `docker/` (Dockerfile+compose+nginx.conf), `tts/` (Piper pt-BR).
- Dockerfile copia das 3 pastas; docker-compose com `context: ..` e `dockerfile: docker/Dockerfile` (context é o PAI de docker/).
- Index de links: `INDEX_ESCRITORIOS_TIMEAUTOMATICO.md` + `LINK-PUBLICO-ATUAL.txt` (atualizar sempre que o túnel mudar).

## QA — lições críticas desta sessão
1. **Screenshot NÃO é QA funcional.** Robôs "apareciam" certos mas o script tinha erros que matavam listeners (botão ENVIAR morto). QA funcional obrigatório: Chrome headless com CDP (`--headless=new --remote-debugging-port=9223`), conectar via websocket mínimo (socket raw + frames), `Runtime.evaluate` para: setar input, `btn.click()`, contar `.bubble`s. **Cuidado:** filtrar targets `type=page` excluindo `chrome-extension://` — o primeiro target costuma ser extensão.
2. **Capturar erros com `Runtime.enable` + evento `Runtime.exceptionThrown`** — erros silenciosos (ReferenceError em setInterval) só aparecem assim. Erro num setInterval não impede listeners já anexados, mas erro no top-level do script mata tudo abaixo.
3. **Pitfall TDZ:** função helper criada por patch que referencia `const msg` declarada depois quebra com "Cannot access before initialization" em runtime. Usar `document.getElementById(...)` direto dentro da função em vez da const de escopo.
4. **Pitfall refatoração por regex em massa:** ao remover/rename funções, checar TODOS os call sites (ex: `trocarTarefa` apagada mas `sentar()` ainda chamava; `walk()` chamada órfã). Depois de qualquer edit massivo: `node -e "new Function(body)"` em TODOS os arquivos + reload com querystring anti-cache (`?v=timestamp`) antes de re-testar.
5. **Pitfall edição em massa de arrays:** substituir `('a','b')` por `['a','b']` com regex global embaralha aspas. Reconstruir o bloco inteiro do zero em vez de patch por linha.
6. **Pitfall batch-loop CDP (viewport race):** rodar QA sequencial por várias páginas via `setDeviceMetricsOverride`+`Page.navigate` funciona isoladamente, mas a partir da 2ª iteração o `innerWidth` retorna `980×2078` (Pixel 5 default) e a página renderiza sem agentes. O `setDeviceMetricsOverride` aceita o valor mas o `Page.navigate` na mesma sessão reverte ao tamanho da janela física. Mitigações testadas e FALHARAM: `clearDeviceMetricsOverride` antes, pre-warm `about:blank`, `Network.setUserAgentOverride`, `Page.reload` após nav, drenar eventos do WebSocket entre chamadas, `Browser.setWindowBounds` antes de cada nav (esta última está documentada no script `scripts/qa_batch_viewport.py` como WORKAROUND VALIDADO mas em batch real de 9 páginas na sessão de 11/09/2026 também retornou 980×2078 — workaround ainda NÃO confirmado em loop). Detalhes + script reproduzível em `references/cdp-batch-viewport-race.md`. Pitfall adicional descoberto nesta sessão: `Page.captureScreenshot` via WebSocket CDP **trava** (timeout) em páginas com muitos elementos animados (espetinho, advocacia) — não é confiável como substituto de `playwright.screenshot()`.
7. **Chrome real (perfil do usuário) em `~/.local/bin/browser-use-real` na porta 9222 pode entrar em estado "aceita TCP mas não responde HTTP"** após uso intenso — sintoma: `curl http://127.0.0.1:9222/json/version` trava no timeout. Workaround: matar e subir nova instância headless `--headless=new --user-data-dir=/tmp/chrome-qa-<data> --remote-debugging-port=9225 --remote-allow-origins='*'` (porta nova evita `bind() failed: Endereço já em uso`). Verificar com `curl -m 6 /json/version` antes de começar QA.
8. **Fallback quando Chrome/CDP fica totalmente bloqueado.** Se Browser Use pedir `Allow remote debugging` e Chrome headless/Playwright também travarem antes de renderizar, não repetir tentativas por 20 minutos nem declarar HTTP 200 como QA. Use duas camadas complementares: (a) **JSDOM** com `runScripts:'dangerously'`, timers, polyfills de `ResizeObserver`/Audio/fetch e clique real no botão para validar runtime, criação de robôs, nomes, xícaras, estados, ETA, resize e resposta do chat; (b) **Firefox headless real** (`firefox --headless --no-remote --profile /tmp/perfil --window-size 390,844 --screenshot saida.png URL`) para prova visual em pixels. JSDOM sozinho NÃO é QA visual; Firefox/screenshot + inspeção visual é a camada de pixels. Use perfil temporário existente (`mkdir -p`) e um processo limpo por página.
9. **Túnel ngrok fica preso se for derrubado durante QA.** Sintoma: `curl http://127.0.0.1:4040/api/tunnels` retorna lista vazia ou trava. Workaround: `pkill -f ngrok` + relançar em background com `ngrok http 8090 &`; link MUDA (free tier), atualizar `LINK-PUBLICO-ATUAL.txt` antes de passar URL ao usuário.
9. **QA sênior após gerar N variantes em lote (template-based)** — NÃO confiar em "passa o smoke test local+ngrok=200". Validar **cross-contamination**: cada HTML gerado deve conter SÓ os agentes do seu próprio escritório. Bug da aula 11/09/2026: `build_escritorios.py` falhou em substituir o array `agents=[...]` porque o end_marker tinha quebra de linha (`}];\nconst stations`), e os 3 escritórios novos saíram com os 8 agentes do Espetinho (Tonho, Bia, Drica, Zé, Carlão, Sônia, Rita, Igor) por baixo do header laranja correto do Escape Room. Validador mínimo (Python): `json.loads(html.slice(html.find('const agents=['), html.find('const stations', ...))); assert all(agent['nome'] in client_expected_agents)`. Referência: skill `escritorios-vivos-sims` seções "Pitfalls do gerador" e "Workflow de Onda de escritórios".

### Pitfall: CSP style-src 'self' bloqueia tags <style> inline
Se o servidor HTTP local retorna Content-Security-Policy com `style-src 'self'`, o navegador bloqueia rigorosamente qualquer tag `<style>` ou estilos inline, resultando em páginas sem formatação visual (layout quebrado). 
**Fix:** Extrair o CSS para um arquivo `.css` externo na mesma pasta pública e referenciá-lo com `<link rel="stylesheet" href="arquivo.css">` servido pelo próprio servidor.

## Referências operacionais
- `references/cdp-batch-viewport-race.md` — transcript completo do bug, tabela de tentativas, workaround `Browser.setWindowBounds` + script.
- `references/evoluir-tecnicamente-oficinas-locked-ui.md` — filosofia "preservar por fora, evoluir por dentro" + LOCKED UI contract + AgentStateStore + AgentEntity + OfficeStation + Idle/Coffee behavior + pathfinding A*. LER PRIMEIRO antes de qualquer evolução técnica que não envolva redesenhar por completo. Complementa as regras de estética de `escritorios-vivos-sims` (The Sims style) e o motor de `interactive-html-demos` (Docker + Phaser + SSE).
- `references/escritorios-master-json-pattern.md` — estrutura canônica + workflow de regeneração de `demos/escritorios-master.json` (enciclopédia técnica paralela ao `offices.json` de routing SSE).
- `references/operacoes-escritorios-sessao-setembro-2026.md` — log operacional das sessões do Igor em setembro/2026 (audit trail, bugs e correções).
- `scripts/qa_batch_viewport.py` — versão re-rodável do QA batch em loop. Roda contra chrome headless em `PORT=9225` e imprime viewport por página.

## Mobile (o usuário testa no celular via ngrok — QA em 390px obrigatória)
- Grade de posições: **determinística** (sem random dentro da célula), com função `relayout()` chamada em `resize` + após load; cols = 3 no mobile, `ceil(sqrt(n*1.6))` no desktop (grade compacta).
- CSS `@media (max-width:768px)`: escalar mesa (0.78x), cadeira, robô (0.85x), plaquinha/tag de nome.
- Screenshot mobile: `google-chrome --headless --screenshot --window-size=390,844` + análise visual em 2 rodadas.

## Workflow de entrega
Editar HTML da pasta certa → validar JS de todos com node → `docker compose build` + `up -d --force-recreate` (no docker/) → QA CDP funcional + screenshots mobile/desktop → commit no repo privado + push → atualizar INDEX/LINK-PUBLICO-ATUAL → abrir no navegador da máquina e passar links ngrok ao usuário.

## ngrok
- `ngrok http 8090` em background; URL via `curl http://127.0.0.1:4040/api/tunnels`. Túnel free = link muda a cada restart. Validar a versão nova PELO TÚNEL (`curl "$BASE/page.html" | grep <marco do fix>`) antes de passar link ao usuário — cache do navegador celular exige refresh forçado.
- **NUNCA persistir URLs ngrok em git/Insync/GitHub** (regra do Igor, confirmada 12/09/2026 — link do túnel free muda a cada restart e vira referência stale/orfã). Pode salvar em MD da sessão para consulta local, mas **NÃO** comitar nem copiar pro Drive sincronizado.
- Para Igor abrir o escritório agora: passar link inline + atualizar `demos/LINK-PUBLICO-ATUAL.txt` apenas se ele precisar de persistência local entre sessões. Nunca propagar via Insync/GitHub.

## Validação JSDOM sem browser (camada adicional de QA, validada 12/09/2026)
- **Pitfall `<template>`**: `tpl.content.cloneNode(true)` funciona em browsers reais, mas **JSDOM em algumas versões retorna o template SEM os filhos do `.content`** (cloneNode perde profundidade). Detectado quando `node.querySelector('.face .head')` retorna `null` no JSDOM mesmo com a estrutura presente no `.content`. Workaround: manter um `<div hidden id="agent-ref">` com a mesma árvore DOM completa como fallback; o `ensureAgent()` tenta `template` primeiro e cai no `agent-ref` se a árvore vier vazia.
- **Pitfall `querySelector` em pseudo-elemento**: `el.querySelector('.ant::after')` retorna `null` (não é seletor de DOM real). Use só `.ant` e deixe o `::after` no CSS.
- **Pitfall `fetch` em JSDOM**: JSDOM NÃO implementa `fetch` por padrão. Em qualquer harness que injete EventSource mock, **também injete `window.fetch = () => Promise.resolve({json:()=>Promise.resolve({})})`**, senão o bootstrap do snapshot joga Uncaught ReferenceError e mata o script.
- **Harness modelo (a criar `scripts/qa_jsdom_dispatch.py`)**: injeta Fake EventSource + Fake fetch, carrega HTML com `runScripts:'dangerously', pretendToBeVisual:true`, espera N eventos × delay + 2s, dumpa `stations.length / summary / conn / feed / cada agente (status, activity, tool, deleg)`. Usar este harness para validar qualquer demo realtime antes do Firefox screenshot.

## Realtime via SSE no nginx (validado 12/09/2026)
Para demos que precisam de SSE (ex. Banca de Saúde TimeAutomático, futuros dashboards), o proxy nginx exige:
```
location /events {
    proxy_pass http://realtime:8765/events;
    proxy_http_version 1.1;
    proxy_buffering off;          # CRÍTICO — sem isso o SSE acumula em buffer
    proxy_cache off;
    proxy_read_timeout 24h;
    proxy_send_timeout 24h;
    proxy_set_header Connection '';
    add_header X-Accel-Buffering "no" always;
    add_header Cache-Control "no-store" always;
    add_header Access-Control-Allow-Origin * always;
}
```
Sem `proxy_buffering off` + `X-Accel-Buffering: no`, o cliente conecta mas só recebe eventos em lotes lentos (ou nunca, se o buffer lotar antes do flush). Padrão completo do pipeline realtime em `general/realtime-events`.

### Pitfall: Container realtime sem porta mapeada
Se o container `realtime` no docker-compose NÃO tem `ports: ["8765:8765"]`, o frontend não consegue conectar em `http://127.0.0.1:8765` (apenas interno ao Docker network). Sintoma: SSE mostra "🟡 reconectando" em loop infinito.

**Fix:** Adicionar `ports: ["8765:8765"]` no service `realtime` do docker-compose.yml:
```yaml
realtime:
  ports: ["8765:8765"]  # ← ADICIONAR ESTA LINHA
```

**Verificação:**
```bash
docker port timeautomatico-realtime  # → 8765->8765/tcp
curl -s http://127.0.0.1:8765/health  # → {"status": "ok"}
```

### Pitfall: CSP wildcard inválido (`https://*.tts.*`)
CSP com `https://*.tts.*` causa warning no console: `Content-Security-Policy: Couldn't parse invalid host`. O wildcard `*` só é válido no **final** do host (`https://*.example.com`), não no meio.

**Fix:** Substituir por host exato ou wildcard válido:
```html
<!-- ANTES (inválido) -->
connect-src 'self' https://*.tts.*;

<!-- DEPOIS (válido) -->
connect-src 'self' https://localhost:8777;
```

**Regra CSP:** `connect-src` aceita apenas:
- `'self'`
- Protocolo + host exato (`https://api.example.com`)
- Wildcard no final (`https://*.example.com`)
- Portas específicas (`https://example.com:8443`)

## Acessibilidade obrigatória (regra do Igor, validada 11–12/09/2026)
- **Todo elemento com `animation` ou `transition` contínua** (blink, pulso, fade) precisa de fallback em `@media (prefers-reduced-motion: reduce)` que zere `animation: none !important; transition: none !important;`. Não basta reduzir velocidade — alguns usuários (vestibulares, labirintite, epilepsia fotossensível) precisam de animação parada por completo. Padrão:
```css
@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; transition: none !important; }
}
```
- **Touch targets ≥ 44×44px** em todos os botões que o usuário toca (incluindo minimizar `–` e zoom `+/−`/`↺`). Não basta ícone visual grande: usar `padding` invisível + `min-width/min-height: 44px`.
- **Botão minimizar não pode estar atrás do `<h4>`** que serve de drag handle: ou `pointer-events: none` no h4 com botão filho absoluto, ou separar hit-zones. Hit-zone errada = clique não acerta o botão.
- **`aria-label`** em todo botão de ícone (➤, 🔇, –, ↺) sem texto visível.

## Skill relacionada (overlap detectado)
- `general/realtime-events` cobre o pipeline Hermes→SSE→Frontend (emit + sidecar + nginx + frontend). Sobrepõe esta skill no ponto "demos HTML que recebem eventos". Ao criar demo realtime nova, começar pela skill realtime-events para o pipeline e usar esta aqui só para a camada de renderização/DOM.
- `general/isometric-agent-office` cobre demos Phaser 3 isométricos especificamente (Banca de Saúde, escritórios 2.5D). Sobrepõe esta skill no ponto "demos com Phaser". Antes de criar demo Phaser isométrica, carregar `isometric-agent-office` primeiro — lá estão os pitfalls do Phaser (UMD vs ES modules, CANVAS vs AUTO, headless canvas).

## Phaser 3 — pitfalls que afetam QUALQUER demo Phaser (12/09/2026)

Se a demo usa Phaser 3, estes são class-level — não vão mudar:

1. **Phaser é UMD, não ES Module.** Não existe `export default Phaser` no bundle. Workaround canônico:
   ```html
   <script src="/vendor/phaser.min.js"></script>  <!-- ANTES do module -->
   <script type="module">
     const Phaser = window.Phaser;  // acessar global, não importar
     ...
   </script>
   ```
   `import Phaser from '/vendor/...'` falha silenciosamente — `Phaser` fica `undefined`, canvas vazio.

2. **`Phaser.AUTO` em headless sem GPU** tenta WebGL primeiro, falha, canvas vazio sem erro visível. Forçar `type: Phaser.CANVAS`:
   ```js
   new Phaser.Game({ type: Phaser.CANVAS, ... });
   ```

3. **CSP precisa de `'unsafe-eval'`** ou Phaser falha ao criar scene tree:
   ```html
   <meta http-equiv="Content-Security-Policy" content="
     script-src 'self' 'unsafe-inline' 'unsafe-eval' blob:; ...">
   ```

4. **Caminhos de import absolutos** no nginx: `import Phaser from '/vendor/...'` (não `'../../tematicos/...'`). Nginx serve pela raiz, paths relativos quebram.

5. **Firefox `--virtual-time-budget` congela async JS** após load event. Use Playwright Python com `page.wait_for_timeout(N)` para QA visual confiável.

6. **Helper functions em ES modules**: `function` declarations são hoisted, mas `const f = () => {...}` NÃO é. Se helper é chamado antes da definição como `const`, trava com TDZ. Sempre declarar helpers no topo do módulo.

7. **`void <var>;` FORA do escopo onde `const` foi declarado** — bug sutil e letal. Exemplo:
   ```js
   function drawCorredor(scene) {
     for (let x = 0; x < N; x++) {
       const { x: sx, y: sy } = gridToScreen(x, 4);  // sy é block-scoped
       dot.fillRect(sx - 2, sy - 2, 4, 4);
     }
     void sy;  // ❌ ReferenceError: sy is not defined
   }
   ```
   Solução: remover `void sy;` ou mover para dentro do loop. Este tipo de erro mata o bootstrap do módulo inteiro (top-level `ReferenceError` propaga pro `window.__bank` não ser atribuído).

8. **`const` dentro do loop vs `let`** — `const` é block-scoped ao bloco `for`, `let` também. Ambos são inválidos fora do loop. Se precisa de valor fora, usar `let` no topo da função.

Referência completa em `references/phaser-3-debugging-workflow.md` (workflow de debug Phaser + Docker + SSE).

### Pattern: LOCKED UI — Evoluir por dentro, preservar por fora
Quando o usuário aprova evolução do motor visual de um escritório/demo, tratar os elementos existentes como CONTRATO DE INTERFACE imutável:

**NÃO modificar (sem autorização humana):**
- Responsividade atual (breakpoints, comportamento mobile, organização da tela)
- Controles de zoom (botões +/-/↺, percentual exibido, localização conceitual)
- Painel de atividades (representação textual/cronológica)
- Painel papéis/agentes (estrutura e propósito)
- Funções dos agentes (papel, especialidade, responsabilidade)
- Contadores superiores (trabalhando, pensando, tool_call, aguardando, concluídos, erro)
- Hierarquia geral da interface (cabeçalho → status → contadores → papéis → escritório → atividade)

**Pode evoluir:**
- Motor de renderização (Canvas manual → Phaser/Tiled)
- Personagens/sprites/animações/pathfinding
- Integração SSE real-time
- Performance e observabilidade interna

**Arquitetura:** Hermes → eventos → AgentStateStore → escritório visual + painel atividades (dois consumers independentes). Se Phaser falhar, painel atividades continua funcionando.

**Documento canônico:** criar `<nome-office>/CONTRATO_INTERFACE_TRAVADA.md` listando o que é protegido + `ui-contract.json` com seletores CSS obrigatórios + `qa_<nome>_ui_contract.py` para validação automatizada (check HEADERS, ORDER, STATES, agents integrity).

**Regra de ouro:** a visualização OBSERVA E REPRESENTA. Nunca define função do agente. A camada visual é consequência do comportamento do agente, não sua origem. Mudanças externas exigem proposta escrita (proposta, motivo, benefício, risco, impacto) + aprovação humana.

### Pattern: Escritórios multi-agente — estrutura de módulos JS separados
Para escritórios/vistas animadas com múltiplos agentes (>10), usar arquitetura modular em vez de arquivo monolítico:

**Estrutura canônica (`<office-name>/`):**
```
<script type="module" src="/<office>/js/boot.js"></script>  <!-- entry point -->
```
Cada módulo JS na pasta `js/`:
- **`constants.js`** — fonte única da verdade: OFFICE_ID, STATUS, GRID, TILE, STATUS_COLOR, STATUS_EMOJI, AGENTES (array completo), MESAS (grid positions). Também exporta `initState()` para estado global compartilhado.
- **`escritorio.js`** — cenário isométrico/diagrama: chão, paredes, mesas, decoração. Usa gridToScreen() de constants. Exporta `buildEscritorio(scene)`.
- **`agentes.js`** — personagens visuais: minifigurinhas LEGO 3D, acessórios por grupo, hit-area zones. Exporta `initAgents(state)`. Acessa window.__agentsDOM para registro global.
- **`camera.js`** — zoom +/-/+ reset, touch pinça 2 dedos, scroll wheel, pan arrastar 1 dedo. Persiste zoom via localStorage com prefix `timeautomatico:<office>:zoom:`. Exporta `initCamera(state)`.
- **`sse.js`** — conexão EventSource autenticada: officeId filter, HMAC/auth check, dedup eventId, realProducer check, snapshot fetch. Exporta `startRealtime(handlers)`.
- **`painel-papeis.js`** — painel flutuante drag+resize+minimize com localStorage persist. Lista agentes agrupados por grupo/mesa. Exporta `initRolePanel(state)`.
- **`boot.js`** — ponto de entrada único: importa TODOS os módulos acima, inicia Phaser scene, conecta SSE handlers, inicializa câmera/panel, clock.

**Regras:**
1. NUNCA imports externos ou fetchs desnecessários nos scripts — tudo autocontido.
2. HTML referencia SOMENTE boot.js. Nenhum outro script no HTML.
3. initState() retorna objeto congelado compartilhado entre módulos.
4. Agentes registram-se em window.__agentsDOM para consulta global.
5. Validar sintaxe de TODOS os .js com `node --check` antes de entregar.

### Workflow: Verificar se Docker incluiu novos arquivos
**Pitfall frequente:** `docker compose build` CACHEia COPY stages mesmo quando novos arquivos foram adicionados à pasta de contexto. Sintoma: `docker ps` mostra container rodando mas `docker exec <container> ls /path` não lista os novos arquivos.

**Sintomas:**
- HTTP 200 no HTML mas conteúdo antigo
- Arquivos existem no host mas não dentro do container
- Build output mostra `CACHED` em todos os COPY stages

**Diagnóstico:**
```bash
docker exec <container> ls -la /usr/share/nginx/html/<diretorio-novo>/
# Se vazio ou ausente = cache problem
```

**Fix:** Reconstruir sem cache:
```bash
docker compose stop && docker compose build && docker compose up -d
```
Ou forçar recriação:
```bash
docker compose rm -f <service> && docker compose up -d <service>
```

**Verificação pós-build:**
```bash
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8090/<office>/<office>.html
# Deverá retornar 200 se os arquivos foram copiados corretamente
```

**Importante:** O caminho URL é `/escritorio_juridico/escritorio_juridico.html` (pasta + arquivo), NÃO `/escritorio_juridico.html` (arquivo solto no root). Validar ambos.

### Pitfall: Normalização de nomes em mapeamento de grupos
Ao mapear folders como `direitos-humanos`, `execucao_penal`, etc. para grupos temáticos, lembrar que os keys do dicionário Python devem corresponder aos nomes NORMALIZADOS (underscores, não hífens):

```python
folder_normalized = agent['folder'].replace('juris-', '').replace('-', '_')
group = mapeamento.get(folder_normalized, 'especial')
```

Sem o `.replace('-', '_')`, 16 de 54 mapeamentos falham silenciosamente (todos caem no fallback 'especial'), criando distribuição totalmente desbalanceada (um grupo com 23+ agentes, outros com 1).

### Checklist pré-entrega: validação final obrigatória
Antes de passar link ngrok ao usuário, executar EM ORDEM:
1. `docker exec <painel> ls /path/<office>/` — confirmar arquivos estão no container
2. `curl -s http://127.0.0.1:8090/<office>/<office>.html | head -3` — verificar HTML serve
3. Para cada JS: `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8090/<office>/js/<file>.js` — todos 200?
4. `node --check js/*.js` — syntax OK em cada módulo
5. Validar `initState()` existe em constants.js e é chamado no boot
6. Validar `window.__agentsDOM` é registrado pelos agentes
7. Validar botão `initRolePanel(state)` é chamado no boot.js
8. Validar CSS tem media queries para mobile (max-width: 768px e max-width: 480px)
9. Validar touch-action:none nos controles interativos
10. Validação cross-contamination: cada escritório tem SÓ seus próprios agentes
