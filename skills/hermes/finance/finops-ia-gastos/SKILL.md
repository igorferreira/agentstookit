---
name: finops-ia-gastos
description: "Use quando Igor pedir gastos de IA / FinOps: quanto gastou no OpenRouter (por modelo/mês), comparativo com assinaturas fixas (ChatGPT Plus, Claude Pro, Gemini Advanced, Manus Pro Entry), projeção de saldo, alerta de crédito 402."
version: 1.0.0
author: agente finops-ia (Caco)
---

# FinOps de IA — Gastos OpenRouter vs Assinaturas Fixas

Skill para visão consolidada de custos de IA do Igor: assinaturas mensais fixas + uso variável pay-per-token no OpenRouter.

## Triggers

- "finops", "gastos de IA", "quanto gastei de IA", "OpenRouter"
- "crédito OpenRouter", "402", "estourou o crédito"
- "vale a pena assinatura ou pay-per-token"
- "relatório de IA", "custo de LLM"

## Regra ABSOLUTA de segurança

**NUNCA ler, imprimir ou expor o valor de chaves de API/credenciais** (.env, config.yaml, keyring etc.). Checar apenas PRESENÇA. O script de coleta lê a chave EXCLUSIVAMENTE de:

1. `secret-tool lookup service hermes-openrouter account igor` (keyring do Igor), ou
2. variável de ambiente `OPENROUTER_API_KEY`

Jamais de config.yaml, .env ou qualquer arquivo. Se ausente, o script sai com erro claro e você deve instruir o Igor (ele digita o valor no próprio terminal, você nunca o recebe):

```
secret-tool store --label=OpenRouter service hermes-openrouter account igor
```

(o comando pede o "secret"/valor — ele digita a chave `sk-or-...` e aperta Enter)

## Assinaturas fixas do Igor (fonte de verdade: ASSINATURAS-FIXAS.md)

| Serviço | Plano | Valor mensal (US$) | Valor mensal (R$, estimativa @5,10) |
|---|---|---:|---:|
| ChatGPT | Plus | 20,00 | ~102,00 |
| Claude | Pro | 20,00 | ~102,00 |
| Gemini | Advanced | 19,99 | ~101,95 |
| Manus | Pro Entry | 20,00 | ~102,00 |
| **TOTAL FIXO** | | **US$ 79,99** | **~R$ 408** |

Valores em R$ foram conferidos contra `~/MEGA/Documentos/financas_bancos/ASSINATURAS.md` (última atualização 19/09/2026: cada uma ~R$ 101,9x). Confirme na fatura do cartão quando pedir número exato.

## API OpenRouter — referência

Base: `https://openrouter.ai/api/v1` — autenticação `Authorization: Bearer <chave>` (a chave NUNCA aparece em log/saída).

### 1. Créditos — `GET /api/v1/credits`

Saldo e limites da conta.

- `data.total_credits` — total já comprado/acumulado (USD)
- `data.total_usage` — total já consumido (USD)
- `data.total_balance = total_credits - total_usage` — **saldo disponível**; se ≤ 0, próximas chamadas retornam HTTP 402 Payment Required

### 2. Atividade — `GET /api/v1/activity`

Uso por geração (cada chamada a modelo). Query params:

- `page` (int) — paginação, 100 registros por página; siga enquanto houver resultados
- `p_start_date` / `p_end_date` (opcionais) — janela em `YYYY-MM-DD`
- `p_model` (opcional) — filtra por modelo (ex.: `z-ai/glm-5.3-flash`)

Campos relevantes de cada item:

- `created_at` / `time` — timestamp da geração (base para agregação por dia/mês)
- `model` — modelo canônico usado (base para agregação por modelo)
- `cost` — custo da geração em USD (chave da agregação)
- `tokens_prompt`, `tokens_completion`, `tokens_total` — consumo de tokens
- `usage` — blocos de usage nativo do provider quando disponível

### Granularidade e agregação

- **Por modelo**: agrupar `cost` por `model`.
- **Por dia/mês**: agrupar por data de `created_at` (fuso: os dados vêm em UTC — o relatório informa o fuso da agregação).
- **Rate limit**: endpoint de activity tem rate limit moderado; o script usa paginação sequencial (sem paralelismo) e sleep entre páginas quando necessário. Não chamar em loop apertado.

### Custos por modelo (tabela pública, sem auth)

- `GET https://openrouter.ai/api/v1/models` — lista todos com `pricing` (`prompt`/`completion` por token, em USD). Use para benchmarks preço/qualidade e para simular "quanto custaria rodar o mês no modelo X".

## Script de coleta

`~/.hermes/scripts/finops-openrouter.py` — uso:

```
python3 ~/.hermes/scripts/finops-openrouter.py            # mês atual (por modelo) + saldo
python3 ~/.hermes/scripts/finops-openrouter.py --month 2026-09
python3 ~/.hermes/scripts/finops-openrouter.py --last 3   # últimos 3 meses
python3 ~/.hermes/scripts/finops-openrouter.py --compare  # comparativo com assinaturas fixas
```

Saída: tabela mensal de custo por modelo + total + projeção do mês + saldo OpenRouter; grava JSON em `/home/igorferreira/MEGA/Documentos/financas_bancos/IA-FINOPS/` e atualiza INDEX.md.

## Comparador assinaturas vs OpenRouter

Com os dois números na mão (fixo US$ 79,99 + variável OpenRouter do mês), avalie:

1. **Custo total de IA/mês** = fixo + variável, em US$ e R$ (informar câmbio/data).
2. **Vale plano?** Se o gasto mensal do OpenRouter com UM modelo premium se aproximar do preço da assinatura equivalente dele (ex.: US$ 20), apontar a assinatura como provável melhor custo/benefício para aquele uso — mas conferir limites de uso da assinatura antes de afirmar.
3. **Routing de modelos mais baratos**: comparar o custo do modelo atual (`z-ai/glm-5.3-flash`) com alternativas na tabela `/models` para o MESMO volume de tokens; sugerir troca só se a economia for relevante e a qualidade aceitável para a tarefa.
4. **Alerta 402 ANTES de estourar**: se `saldo > 0` e `projecção_de_gasto_até_fim_do_mês > saldo`, disparar alerta com data estimada do estouro (fórmula: `dias_restantes = saldo / gasto_diário_médio`). Também alertar quando saldo < 25% do gasto do mês anterior.

## Fluxo recomendado (relatório mensal)

1. Rodar `finops-openrouter.py --compare` (mês corrente + mês anterior se disponível).
2. Ler JSON gerado em IA-FINOPS/ e montar resumo: fixo vs variável, top modelos, projeção, status do saldo.
3. Gravar/atualizar INDEX.md na pasta IA-FINOPS.
4. Se algo der errado sem chave: seguir a Regra ABSOLUTA e instruir o Igor.

## 💾 Prompt Caching — Otimização de Custos (sempre ativo)

O Hermes usa OpenRouter com caching automático de prompt pela Alibaba Cloud. Quando o prefixo do sistema prompt é idêntico entre chamadas, os primeiros N tokens são servidos pelo cache ($0,006/M vs $0,030/M para Qwen 3.7 Flash — economia de ~80% no input).

### Regras de engenharia de prompt para maximizar cache hits

- **SOUL.md nunca muda o prefixo.** Linhas iniciais devem ser estáticas entre turnos. Editar SOUL alterando as primeiras linhas = perda de cache hit até próxima mudança ser estabilizada.
- **Bloco `[Agora]` com data/hora injetado NO FINAL do prompt.** Não afeta o prefixo cache da OpenRouter (que cobre SOUL.md + instruções base). Pode ficar assim sempre.
- **Compression não interfere no cache da OpenRouter.** A compressão do Hermes opera nas mensagens ANTIGAS (quando o window enche), apagando/resumindo histórico. Nunca modifica o prefixo do sistema prompt que alimenta o cache do provider. São mecanismos complementares.
- **Sempar campo `prompt_cache_enabled` no config.yaml.** O caching é automático na API OpenRouter quando o prefixo bate — nenhuma flag especial. Existe `cache_ttl: 5m` como controle interno do Hermes.
- **Economia esperada:** ~30-40% no custo total de input tokens com mix ~40-50% de cache hit rate (prefixo estático garantido).

Referência completa: `references/cache-engineering.md`.
