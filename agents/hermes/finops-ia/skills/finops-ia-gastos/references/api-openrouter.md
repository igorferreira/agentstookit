# OpenRouter API — endpoints de FinOps (verificado na doc oficial 23/09/2026)

Fontes: https://openrouter.ai/docs/api/api-reference/credits/get-remaining-credits e
https://openrouter.ai/docs/api/api-reference/analytics/get-user-activity-grouped-by-endpoint

## Pré-requisito: MANAGEMENT KEY

Ambos os endpoints exigem **Management API Key** (criar em https://openrouter.ai/settings/management-keys).
Chave de chat normal → `403 {"error": {"code": 403, "message": "Only management keys can perform this operation"}}`.
Management keys NÃO funcionam para chamadas de completion — são só administrativas. Recomenda-se criar com data de expiração.

## GET /api/v1/credits — saldo

```
curl -H "Authorization: Bearer $KEY" https://openrouter.ai/api/v1/credits
```
200 → `{"data": {"total_credits": 100.5, "total_usage": 25.75}}` (USD; saldo = credits − usage).
Erros: 401 (header/inválida), 403 (não é management key), 500.

## GET /api/v1/activity — uso agregado por dia/modelo

```
curl -H "Authorization: Bearer $KEY" "https://openrouter.ai/api/v1/activity?date=2026-09-23"
```

- **`date`** (único filtro de tempo aceito): UM dia UTC, somente nos **últimos 30 dias UTC completos**. Sem range, sem paginação.
- Outros filtros: `api_key_hash`, `user_id`, `group_by=workspace`, `workspace_id`.
- Linhas de resposta (campo por campo):
  - `date` (YYYY-MM-DD UTC), `model`, `model_permaslug`, `provider_name`, `endpoint_id`
  - `usage` — **custo total USD (créditos OpenRouter gastos)**
  - `byok_usage_inference` — custo BYOK (créditos externos)
  - `requests` — nº de gerações
  - `prompt_tokens`, `completion_tokens`, `reasoning_tokens`
- Agregação já vem pronta por (data, modelo, endpoint) — não precisa somar geração a geração.

### Consequência para o FinOps do Igor

- Para montar um mês: iterar `date` de 1 a fim do mês, agregando `usage` por `model`.
- Meses anteriores à janela de 30 dias → vazio. Histórico só nos JSONs de `IA-FINOPS/` (por isso o cron mensal roda todo dia 1º e o script reporta mês corrente + anterior).
- 429 → respeitar `Retry-After` (o script já faz).

## Crédito estourado (HTTP 402)

Chamadas de chat falham com 402 quando o saldo acaba. O script projeta `total_cost` do mês e compara com `total_balance`, emitindo alerta ANTES do estouro (limite crítico ≤ 0; alerta quando projeção > saldo; atenção quando saldo < 25% da projeção).
