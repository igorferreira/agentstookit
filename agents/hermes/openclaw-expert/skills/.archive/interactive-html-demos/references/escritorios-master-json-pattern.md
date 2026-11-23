# escritorios-master.json — Fonte única da verdade dos escritórios

Padrão de canonical knowledge que Igor pediu em 12/09/2026 ("É precisamos ter um json com toda a definição de todos os escritórios"). Não é apenas outro manifesto: é a **enciclopédia técnica** dos escritórios, mantida em paralelo ao `offices.json` (que é só routing para SSE).

## Por que dois arquivos?

| Arquivo | Propósito | Quem escreve |
|---------|-----------|--------------|
| `demos/realtime/offices.json` | **Routing para SSE** — officeId → agentId → profile, validado pelo plugin Hermes HMAC. Hot path: precisa ser pequeno e rápido de parsear. | Hermes plugin ao validar eventos |
| `demos/escritorios-master.json` | **Enciclopédia técnica** — todos os escritórios + estado real (motor, zoom, responsividade, agentes, conectividade, lacunas). Não é hot path: é referência para auditorias, migrações, novos clientes, gap analysis. | Subagent de auditoria (manual + automático) |

Manter ambos. O `master` referencia mas não duplica o `offices.json` (apenas guarda o `officeId`).

## Estrutura canônica

```json
{
  "versao": "1.0.0",
  "gerado_em": "2026-09-13",
  "fonte_dos_dados": "Batch 1 architecture mapping + Batch 1 realtime map",
  "base_ngrok": "https://90a7-2804-1b3-7141-e583-cc0-be56-bdb8-97bc.ngrok-free.app",
  "total_escritorios": 14,
  "escritorios": [
    {
      "escritorio": "banca-saude",
      "titulo": "🏥 Banca de Saúde · ao vivo",
      "tipo": "moderno-phaser-esm",  // ou "lego-dom-monolitico", "minimal-modular"
      "arquivo": "clientes/banca_saude.html",
      "url_ngrok": ".../banca_saude.html",
      "status": "completo",  // ou "criado mas ainda não validado", "pendente correções"
      "num_agentes": 6,
      "motor": {
        "engine": "phaser-v3",
        "import_style": "esm-module",
        "imports_javascript": ["/banca-saude/js/state.js", "/banca-saude/js/boot.js"]
      },
      "responsividade": {
        "media_queries": ["max-width:1024px", "max-width:768px", "max-width:480px", "landscape"],
        "mobile_first": true
      },
      "controles_zoom": {
        "tem_controles": true,
        "formato": "HTML buttons + output",
        "funcionais": true
      },
      "agentes": [
        {"id": "angelica", "nome": "Angélica", "profile": "saude", "cor_hex": "#1FD3C4"}
      ],
      "elementos_dom": ["header", "stage", "canvas-host", "rolePanel", "feed", "summary"],
      "conectividade_sse": {
        "usa_legacy_real_only": false,
        "event_source_url": "/events?office=banca-saude",
        "consumo_direto": true
      }
    }
  ]
}
```

## Regra de ouro: NULL é honesto

Se um campo não existe para aquele escritório (ex: `faculdade` define agentes em `boot.js` externo, não inline; `escritorio_juridico` foi criado agora e ainda não foi auditado responsividade/zoom), deixar o campo como `null`. NÃO inventar dados.

- ✅ 14 escritórios com `titulo`/`tipo`/`arquivo`/`status`/`motor` preenchidos (mínimo garantido)
- ⚠️ 1-2 escritórios com `agentes`/`responsividade`/`controles_zoom` null (campo desconhecido)

O relatório do auditor deve mostrar `campos_preenchidos` vs `campos_nulos` por escritório.

## Quando regenerar

- Novo escritório adicionado: regenerar `escritorios-master.json` com o novo entry
- Bug visual corrigido em massa: regenerar `tipo` se a estrutura mudou
- Novo critério de classificação criado: regenerar
- **Não** regenerar só porque alguém fez um patch de 5 linhas num único escritório — o custo de regeneração > valor de manter precisão absoluta do arquivo

## Como regenerar (workflow)

1. Rodar subagent de auditoria que lê TODOS os `.html` de `clientes/` (mais os módulos JS internos)
2. Subagent lê os manifestos `offices.json` para cruzamento
3. Para cada escritório, classificar `tipo`:
   - `moderno-phaser-esm` — HTML minimal + boot.js/state.js + ES Modules + Phaser v3
   - `lego-dom-monolitico` — HTML único grande + JS inline + Phaser ou DOM
   - `minimal-modular` — HTML lean (~8-13 KB) + sem lógica no HTML
4. Preencher campos a partir do HTML lido (sem inventar)
5. Cruzar lista com `offices.json` — se `officeId` existe lá mas não tem HTML correspondente, marcar `status: "pendente"`. Se tem HTML mas não está no `offices.json`, é escritório **novo** que precisa ser adicionado no manifesto.

## Onde fica

- Arquivo canônico: `demos/escritorios-master.json`
- Atualizar junto com o `INDEX_ESCRITORIOS_TIMEAUTOMATICO.md` quando houver mudanças estruturais

## Output esperado

Quando Igor pede "dicionário técnico dos escritórios" ou "estado atual dos escritórios":
1. Resumir `escritorios-master.json` em tabela Markdown (uma linha por escritório)
2. Destacar lacunas (campos null) como oportunidades de auditoria
3. Cruzar com `offices.json` para detectar drift (escritórios órfãos)
4. Validar JSON antes de entregar

NÃO confiar em memória cacheada sobre o estado — sempre reler do disco.
