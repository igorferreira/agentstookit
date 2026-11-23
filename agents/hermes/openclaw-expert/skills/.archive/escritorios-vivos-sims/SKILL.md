---
name: escritorios-vivos-sims
description: Use ao criar/evoluir demos Escritório Vivo estilo Sims 2.
---

# Escritórios Vivos TimeAutomático (estilo The Sims 2)

## Regras fixas do Igor (não negociáveis)

1. **Personagens = HUMANOS estilo The Sims** — cabeça redonda (pele + cabelo escuro), 2 olhos que piscam, boca, tronco com camisa colorida por função + gravata, braços e pernas. NUNCA mini robôs com antena/olhos LED (Igor rejeitou explicitamente: "tudo deve ser humanos").
2. **Mesas em FILEIRAS de 6 (desktop ≥1100px), 4 (≥640px) ou 3 (mobile)** — alinhadas em grade regular, sem sobreposição.
3. **Nome do agente numa plaquinha EM CIMA da cabeça.**
4. **Zoom obrigatório** — botões +/− com indicador de %, Ctrl+scroll no PC, pinça de 2 dedos no mobile.
5. **Botão ENVIAR (➤) no rodapé** — envio NÃO pode depender só do Enter (quebra no mobile).
6. **Demos temáticas e de cliente NÃO podem expor dados pessoais** (agentes pessoais, dívidas, processos, relacionamentos). O escritório "principal" com agentes pessoais fica uso interno.
7. **Vanilla JS, um HTML por escritório** — Igor decidiu NÃO usar React nas demos (animação é 90% CSS/DOM; React só valeria para um painel de produto com estado complexo).

## Arquitetura validada

- Estrutura: `demos/principal/`, `demos/tematicos/`, `demos/clientes/`, `demos/docker/` (nginx + Piper TTS), `demos/tts/`.
- Docker compose: painel (:8090) + tts (:8777); nginx faz proxy `/tts` → container TTS.
- **O container Docker copia o arquivo — qualquer edição exige `docker compose build painel && docker compose up -d --force-recreate painel`.** Esquecer o rebuild = QA contra versão antiga (cache engana).
- Regenerar temáticos após editar o principal: `python3 gerar_escritorios_tematicos.py`.
- Índice canônico de links: `demos/INDEX_ESCRITORIOS_TIMEAUTOMATICO.md` + `demos/LINK-PUBLICO-ATUAL.txt` (ngrok free, link muda a cada restart).

## Posicionamento: grade determinística (maior lição da sessão)

Posicionamento por `randomPos()` aleatório dentro de células + relayout via setTimeout é **INCONFIAVÉL**: screenshot headless captura antes dos timers, posições ficam caóticas, e `randomPos` esgota a grade (`gradeOcupada`) devolvendo posições espalhadas.

**Padrão que funcionou:**
1. **Grade determinística na própria criação** — `randomPos()` vira função de `gradeIdx++` (zero aleatório): `x = margem + (idx%cols)*cw + 10; y = 150 + Math.floor(idx/cols)*ch + 20`.
2. `relayout()` recalcula e move **estação + robô + tag juntos** (estação guarda `{est,x,y}`).
3. **Chamar relayout em todas as âncoras**: `resize` + `load` + `[100,300,600,1200,2000,3000,4500].forEach(t=>setTimeout(relayout,t))` + `setInterval(relayout,3000)` + **`new ResizeObserver(relayout).observe(office); relayout();`** — o ResizeObserver é o que garante alinhamento no load.
4. **Ciclo de passeio automático DESATIVADO por padrão** (todos sentados, fileiras perfeitas). Reativar só sob pedido, máx. 1 agente passeando, e a tag NÃO acompanha o passeio.
5. `y` inicial ≥150 para não colidir com painel de expediente/alertas do topo.

## QA funcional (obrigatório antes de "pronto")

Igor exige QA real — "funciona no meu browser" não é prova:

- **Clique via CDP** (Chrome headless `--remote-debugging-port=9223`): digitar no `#msg`, clicar `#btnEnviar`, contar `.bubble` e conferir resposta do agente. `Runtime.exceptionThrown` captura erros de script que matam listeners silenciosamente.
- **Screenshot + vision_analyze por rodada** (desktop 1400x900 e mobile 390x844); iterar v1→vN até nota alta.
- Pegar o **target correto** do CDP (`type==='page'`, excluir `chrome-extension://`).
- **Zoom funcional**: clicar `#zm+`/`#zm-` e conferir `#zoomPct` + `office.style.transform`; simular Ctrl+wheel com `WheelEvent('wheel',{deltaY:-100,ctrlKey:true})`.

## Pitfalls

- **Injeção de código em massa com regex em 8 arquivos** corrompeu aspas 2× (strings embaralhadas). Preferir patch cirúrgico por arquivo + validar JS de TODOS: `node -e "new Function(s.match(/<script>([\s\S]*?)<\/script>/)[1])"`.
- **JS anexado fora de `<script>`** vaza como texto no rodapé (aconteceu com o bloco de zoom). Conferir se o código caiu dentro de `<script>`.
- **CSS legado sobrevive a refatoração parcial** (robô velho + humano novo coexistindo) — reescrever o bloco inteiro de uma vez.
- **Cache**: navegador e container guardam versão antiga; usar `?v=N` no QA e rebuild forçado.
- Erros que matam o script ANTES dos listeners (botão morto): função perdida em refatoração (`trocarTarefa`), TDZ de `msg`, chamada `walk()` órfã, array com `('a','b')` em vez de `['a','b']` → banner "undefined undefined".

## Pitfalls do gerador `build_escritorios.py` (template-based, aula 11/09/2026)

Gerador Python que reaproveita um template `escritorio_X.html` para criar variantes customizadas (escape room, portões, política, etc.). **Ponto crítico:** substituir o array `const agents=[...]` no template copiado.

- **End_marker NÃO pode ser `'];const stations'` literal.** O template tem `}];\nconst stations={};\nconst cores` (quebra de linha). `html.find('];const stations', si)` retorna `-1`, a substituição é silenciosamente pulada e o HTML novo sai com o array de agents do template ORIGINAL (não do cliente certo). Resultado: cross-contamination — escritório Escape Room mostrava Mestre Tonho, Bia, Drica, Zé, Carlão, Sônia, Rita, Igor (todos do Espetinho) por baixo do header laranja correto. **Bug só foi pego pelo QA sênior do Igor no Telegram.**

  Padrão correto:
  ```python
  start_marker = 'const agents=['
  end_marker = 'const stations'      # sem '];' — pega só o identificador seguinte
  si = html.find(start_marker)
  ei = html.find(end_marker, si)
  if si >= 0 and ei > si:
      arr_end = html.rfind('];', si, ei)   # acha o '];' mais próximo
      if arr_end > si:
          html = html[:si] + f'const agents={agents_json_str}' + html[arr_end+2:]
  ```

- **JSON.parse do array extraído pelo QA**: se o array termina em `}]` (sem `];`), o `json.loads` falha. Adicionar `]+` antes de parsear: `json_str = raw + ']' if not raw.endswith(']') else raw`. Mesma técnica no QA.

- **Cookie key:** o template tem `ta_layout__escritorio_<slug>_`; o gerador aplica `replace('escritorio_espetinho_gabinal_', f'ta_layout__{cookie_key}_')`. Mas a string original não tem prefixo `escritorio_` — comparar com `ta_layout__<cookie_key>_` (sem o `escritorio_` no cookie). Pitfall ao auditar: o QA procurava `ta_layout__{slug}_` (com prefixo) e dava falso negativo; corrigir para `cookie_key = slug.replace('escritorio_', '')`.

## Workflow de "Onda de escritórios" (validado 11/09/2026)

Quando o Igor pedir vários escritórios de uma vez (ex: 3 novos clientes):

1. **Plano único** em `05-execucao-clientes/PLAN-O-ESCRITORIOS-<ONDA>.md` — listar cada escritório com tema, agentes (papel + função + cor), decorações, rotina típica, perguntas de revisão (cores, foco, separação).
2. **`clarify` com 4-5 perguntas curtas** sobre cada escritório (cores, foco, Igor consultor presente?). Exemplo bem-sucedido: 5 perguntas, todas respondidas em 1 turno, plano ajustado.
3. **Implementar via `build_escritorios.py`** (Python parametrizado) — NÃO copiar/colar 3 vezes (risco de esquecer um `agents=[]` ou cookie). 1 chamada por escritório com agentes distintos.
4. **JS sintaxe em todos** — `node -e "new Function(html.match(/<script>([\s\S]*?)<\/script>/)[1])"` antes de subir Docker.
5. **Docker rebuild + smoke test** — `docker compose build painel && docker compose up -d --force-recreate` + `curl -sS -m 5 -o /dev/null -w '%{http_code}'` em cada URL.
6. **QA sênior antes de declarar pronto** (Igor exige explicitamente, ver mensagem "executa um QA senior dnovo"):
   - Validar **agentes REAIS** (não do template) — checar nomes específicos por escritório + cross-contamination check (nenhum nome de outro escritório aparece).
   - Validar Igor consultor presente, cookie único, 8 agents, JS válido, local 200, ngrok 200.
   - Se QA falhar, regenerar (NÃO patchear) — o bug estrutural está no gerador, não no HTML.
7. **Commit + Drive sync + atualizar `LINK-PUBLICO-ATUAL.txt` + PEDIDOS.md** com versão e contagem de passes.

## Suporte

- `references/qa-cdp-checklist.md` — sequência exata de testes funcionais via CDP (clique, bolhas, console errors, zoom, screenshots desktop/mobile).
- `templates/escritorio_base.html` — esqueleto known-good (humanos Sims + grade + zoom + TTS + botão ENVIAR).
- `scripts/build_escritorios.py` — gerador parametrizado com fix do end_marker (vide pitfall acima).