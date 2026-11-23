# Resolução de Escritórios Duplicados — Fluxo Validado

Sintoma típico: o usuário diz *"Por que temos duas bancas de saúde??? Não faz sentido"* ou *"Não devemos ter 2 escritórios de saude"*. Quase sempre aparece após criar uma variante (`escritorio_banca_saude.html`) sem deletar a canônica (`banca_saude.html`), ou após clonar a base modular e esquecer o rename completo.

## Fluxo de resolução (validado 12/09/2026 — Banca de Saúde)

1. **Listar os 2 candidatos** com `ls demos/clientes/banca*.html`. Comparar:
   - **Motor** (Phaser 3 modular vs PixiJS monolítico vs DOM puro) — preferir o modular.
   - **Estrutura JS** (ES modules separados em `js/` vs inline monolítico) — preferir ES modules.
   - **`agent-manifest.json`** — se um dos candidatos não tem mapeamento oficial, é derivado.
   - **LOCKED UI contrato** (`ui-contract.json` + `CONTRATO_INTERFACE_TRAVADA.md`) — o que respeita o contrato é o candidato canônico.

2. **Escolher o canônico** seguindo a hierarquia:
   - **Phaser 3 + ES modules + agent-manifest.json + ui-contract.json** → canônico (sobrevive a todos)
   - **PixiJS monolítico inline** → sempre deletar (mistura motores sem justificativa)
   - **DOM puro pequeno** → deletar se já existe versão Phaser equivalente

3. **Migrar agentes soltos** se houver (*"Os agentes soltos vc coloca no escritório da ISFCONSULT"*):
   - Criar `escritorio_<dominio>_loose.html` (ou nomear conforme pedido, ex: `isficonsult.html`).
   - Inherit da base modular Phaser (passo "Criar Novo Escritório" no SKILL.md principal).
   - Adicionar `officeId` ao manifesto.
   - Não migrar agentes que já estão em algum escritório ativo — perguntar antes.

4. **Deletar o perdedor** após Docker rebuild + smoke test do canônico. Backup git antes.

5. **Atualizar manifesto** nos DOIS locais (`demos/realtime/offices.json` + `integracoes/hermes-plugin/timeautomatico-realtime/offices.json`).

## Caso real: Banca de Saúde (12/09/2026)

Confronto entre os dois candidatos:

| Critério | `banca_saude.html` (canônico) | `escritorio_banca_saude.html` (perdedor) |
|---|---|---|
| Tamanho | 18.8 KB | 41.6 KB |
| Motor | Phaser 3 + ES Modules | **PixiJS v8 monolítico inline** |
| Módulos JS separados | 12 arquivos (`boot.js`, `state.js`, `agentes.js`, ...) | Inline em `<script>` |
| `agent-manifest.json` | ✅ presente | ❌ ausente |
| LOCKED UI contrato | ✅ presente | ❌ ausente |
| Contadores / Feed / Papéis | ✅ funcionais | ✅ funcionais |
| node --check | ✅ PASSOU | ✅ PASSOU |

**Decisão**: manter `banca_saude.html`, deletar `escritorio_banca_saude.html` na próxima rodada de cleanup (mantida por enquanto porque tem features extras: `btnPause`, `clock` em tempo real, comportamentos de animação mais ricos — pode servir como referência de evolução).

## Pitfall: PixiJS vs Phaser (não misture motores)

`escritorio_banca_saude.html` mistura PixiJS v8 com a convenção dos outros 13 escritórios (Phaser 3). PixiJS é melhor para:
- Centenas de sprites + shaders WebGL
- Efeitos visuais avançados (filters, blend modes)

Phaser 3 é melhor para:
- Lógica de jogo (scenes, tweens, física arcade built-in)
- Init síncrono (sobrevive a Firefox `--virtual-time-budget`)
- Containers com `setData`/`setInteractive`

**Regra**: a família TimeAutomático é **Phaser 3 por padrão**. Não introduzir PixiJS a não ser que seja para um caso de uso WebGL pesado específico. Se aparecer inconsistência, migrar PixiJS → Phaser antes de aceitar como novo escritório.

---

# `demos/escritorios-master.json` — Fonte da Verdade Canônica

JSON único que descreve TODOS os escritórios existentes: id, título, arquivo HTML, URL ngrok, motor, status, lista de agentes, controles UI. **NÃO commitar no git** (URL ngrok muda a cada restart; vive no sistema de arquivos local).

## Schema mínimo por escritório

```json
{
  "escritorio": "banca-saude",
  "titulo": "🏥 Banca de Saúde · ao vivo",
  "tipo": "moderno-phaser-esm",
  "arquivo": "clientes/banca_saude.html",
  "url_ngrok": "https://xxxx.ngrok-free.app/banca_saude.html",
  "status": "completo",
  "num_agentes": 6,
  "motor": { "engine": "phaser-v3", "import_style": "esm-module" },
  "agentes": [{"id": "angelica", "nome": "Angélica", "profile": "saude"}],
  "conectividade_sse": { "url": "/events?office=banca-saude" }
}
```

## Por que existe (não é redundante com `offices.json`)

O `offices.json` no realtime tem só `officeId` + `agents` (mínimo para roteamento); o agente precisa de metadata para QA, links ngrok para o usuário, e motor para detectar inconsistências (ex: escritório com PixiJS quando o resto é Phaser).

## Regras de manutenção

- Atualizar quando escritório novo/duplicado/deletado.
- **NUNCA commitar no git** — URL ngrok fica órfã em horas. Salvá-lo em `demos/escritorios-master.json` no filesystem local.
- Útil para QA: `python3 demos/qa/check_master.py --missing url_ngrok` lista escritórios sem link atualizado.

## Quando regenerar

- **Criou novo escritório**: adicionar entry com `status: "completo"` ou `status: "criado mas ainda não validado"`.
- **Deletou escritório**: remover entry + remover do `offices.json` (2 locais).
- **Mudou motor**: atualizar campo `motor.engine` e `tipo`.
- **Migrou agente entre escritórios**: atualizar `agentes[]` em ambos os escritórios no master.
- **Renomeou HTML**: atualizar `arquivo` em ambos.

## Validação ao adicionar escritório novo

1. `node --check` em todos os scripts inline (HTML) E em todos os `.js` da pasta `js/`
2. Validar `agent-manifest.json` é JSON válido e tem 1:1 profile→avatar
3. Validar que o escritório aparece em `offices.json` (ambos os locais: `demos/realtime/` + `integracoes/hermes-plugin/timeautomatico-realtime/`)
4. Docker rebuild + smoke test:
   ```bash
   docker compose up -d --build --force-recreate painel realtime
   curl -sS http://127.0.0.1:8090/<arquivo>.html
   ```
   Deve retornar 200.
5. Se ngrok estiver exposto: `curl -sS -m 5 -o /dev/null -w '%{http_code}' https://xxxx.ngrok-free.app/<arquivo>.html` retorna 200.
6. Rodar QA específico (`qa_<office>_ui_contract.py`) — para Banca Saúde e Faculdade são contratos LOCKED.

Só depois de tudo passar, atualizar `status` para `"completo"` no master.
