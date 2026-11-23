---
trigger: "Gerenciar múltiplos escritórios virtuais TimeAutomático: criar novos, mover agentes, alterar contrato de interface, rodar QA ou debuggar renderização/zoom/sse."
name: timeautomatico-offices
category: business
description: "Criar escritórios e mover agentes com contrato LOCKED UI."
---

# TimeAutomático — Gestão de Escritórios Virtuais

Cada escritório é um subdiretório em `demos/clientes/<nome>/` contendo:

```
banca_saude.html          ← ponto de entrada único (HTML autocontido)
js/constants.js           ← OFFICE_ID, GRID, TILE, STATUS, AGENTES[], MESAS[]
js/boot.js                ├── Phaser Game config + Scene + SSE connect
js/camera.js              │── camera zoom, pan, reset
js/comportamento.js       │── animações por status
js/agentes.js             │── drawIsoBlock, drawCylinderHead, drawLEGOCharacter
js/escritorio.js          ├── buildEscritorio() cenário isométrico
js/painel-papeis.js       ── role panel flutuante
js/state.js               │── AgentStateStore
js/sse.js                 ──── RealEventSource (events, snapshot, source-status)
agent-manifest.json       ← mapping id→profileHermes→avatar
ui-contract.json          ← LOCKED UI selectors + states públicos
CONTRATO_INTERFACE_TRAVADA.md ← descrição humana das restrições
```

## Regras Críticas (sem exceção sem aprovação humana)

### 1. LOCKED UI — NÃO modificar funcionalmente estes elementos
- Responsividade atual (breakpoints, mobile/tablet/desktop)
- Controles de zoom (`#zoomOut`, `#zoomValue`, `#zoomIn`, `#zoomReset`)
- Painel Atividade (`#feed`, `#events`) — texto cronológico independente do canvas
- Painel Papéis da Banca (`#rolePanel`) — relação papel→agentId→personagem
- Funções dos agentes (papel, especialidade, responsabilidades, fluxo) — visualização é read-only observation
- Estados públicos (`working`, `thinking`, `tool_call`, `waiting`, `completed`, `error`) — máquina interna pode ser mais rica mas DEVE mapear aos estados públicos acima
- Contadores superiores (`#ctWorking`, `#ctThinking`, etc.) — leem do mesmo AgentStateStore
- Hierarquia geral: header → status → contadores → papéis → escritório → atividade

### 2. Área liberada para evolução profunda
Motor visual: renderização, personagens, iluminação, pathfinding, mapa, salas, animações, câmera interna, performance, integração com eventos Hermes, Tiled, spritesheets, Asset Manager, HermesEventAdapter.

### 3. Filosofia EVOLUIR POR DENTRO, PRESERVAR POR FORA
Novo motor substitui o antigo POR DENTRO sem destruir a experiência POR FORA.

## Criar Novo Escritório

### Passo 1 — Clone base
```bash
cp -a demos/clientes/banca-saude demos/clientes/<novo-nome>
```

### Passo 2 — Renomear referências no HTML
Substituir title, header aria-label, imports JS (`/banca-saude/js/` → `/novo-nome/js/`).

### Passo 3 — constants.js
Definir OFFICE_ID, definir AGENTES[] e MESAS[].

### Passo 4 — agent-manifest.json
Mapeamento 1:1 perfil Hermés → avatar visual. profilePath apontando para `~/.hermes/profiles/<perfil>/SOUL.md`.

### Passo 5 — Validar contratos antes de subir
Rodar todos os QAs listados em [Validação](#validação-automatizada-antes-de-qualquer-merge).

## Mover Agente Entre Escritórios

Quando agente sai de Escritório A e vai para B:

1. **Remover de A**:
   - Remover de `AGENTES[]` e `MESAS[]` em `constants.js` de A
   - Remover do `agent-manifest.json` de A
   - Remover de `PROFILE_TO_AGENT` no plugin realtime (`__init__.py`)
   - Remover regex da `SPECIALTY_RULES` em `__init__.py`
   - Remover de `ALLOWED_AGENTS` em `event_security.py`
   - Remover do `EXPECTED_IDS` no QA correspondente
   - Se hardcoded `_append("tool.started","nome_hardcoded")` → trocar pelo agent dinâmico via `_agent_for_session(key)`

2. **Adicionar em B**:
   - Adicionar em `AGENTES[]` e `MESAS[]` de B
   - Adicionar ao `agent-manifest.json` de B
   - Adicionar ao `PROFILE_TO_AGENT` do plugin realtime
   - Adicionar à `SPECIALTY_RULES` do plugin realtime (regex específica do perfil)
   - Adicionar à `ALLOWED_AGENTS` do `event_security.py`
   - Adicionar ao `EXPECTED_IDS` do QA de B

3. **Validar**: Rodar todos os QAs de A e B. Nenhum deve falhar.

### Pitfall: Tool events sempre pertencem ao executor real
NUNCA fazer `_append("agent.tool.started","nome_hardcoded")`. Isso causa eventos desconectados do perfil Hermés real. Usar `agent = _agent_for_session(key)` e passar esse objeto ao `_append`.

## Validação Automatizada Antes de Qualquer Merge

```bash
python3 demos/qa/qa_agent_manifest.py
python3 demos/qa/qa_minifigura_3d.py
python3 demos/qa/qa_<office>_ui_contract.py    # se existir no escritório
python3 demos/qa/qa_faculdade_manifest.py      # oficina-specific quando aplicável
```

Verificar sintaxe JS de todos os scripts inline em cada HTML:
```bash
for f in demos/clientes/*.html; do
  node --check <(python3 -c "import re; t=open('$f').read(); print(re.findall(r'<script(?![^>]*src=)[^>]*>([\s\S]*?)</script>',t,re.I)[0])" 2>/dev/null) || echo "FAIL: $f"
done
```

## Debugging

### HTML corrompido com `... [truncated]` ou prefixo de linha
Possível corrupção textual do write_file. **Fix rápido:** `git show HEAD:demos/clientes/<file>.html > demos/clientes/<file>.html`

### SyntaxError no Node `const stations={}; unexpected token const`
Provavelmente variável duplicada após injeção de funções LEGO. **Debug:** extrair cada `<script>` inline e validar individualmente com `node --check`.

### Popup Chrome "Allow remote debugging?" na sessão isolada
Cada `browser_exec(session=X)` abre Chrome isolado que precisa confirmação manual UMA VEZ. **Workaround:** abrir manualmente `google-chrome --remote-debugging-port=9222 --remote-allow-origins='*'`, confirmar o popup, depois reutilizar a mesma porta. Ou evitar sessões isoladas desnecessárias.

### Plugin realtime não roteia evento para agente correto
Checklist: (a) `PROFILE_TO_AGENT` tem mapeamento profile→avatar? (b) `SPECIALTY_RULES` cobre o termo do goal? (c) `_agent_for_session()` retorna algo != None? (d) `ALLOWED_AGENTS` inclui o agent ID? Check log: `tail -f ~/.cache/timeautomatico/events.jsonl`.