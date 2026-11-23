# OpenRouter API — Referência detalhada (FinOps)

Documentação de campo para o script `~/.hermes/scripts/finops-openrouter.py`.
Base URL: `https://openrouter.ai/api/v1` — header: `Authorization: Bearer <OPENROUTER_KEY>`

---

## GET /credits

Resposta (200):

```json
{
  "data": {
    "total_credits": 25.00,
    "total_usage": 18.42,
    "total_balance": 6.58
  }
}
```

| Campo | Tipo | Significado |
|---|---|---|
| `data.total_credits` | float USD | Total de créditos comprados/presentes na conta |
| `data.total_usage` | float USD | Total consumido historicamente |
| `data.total_balance` | float USD | Saldo disponível = total_credits − total_usage. **≤ 0 → HTTP 402 em toda chamada de inferência** |

Erros: `401` (chave inválida), `402` (sem crédito — para inferência; /credits continua respondendo), `429` (rate limit — respeitar `Retry-After`).

---

## GET /activity

Uso por geração individual. Query params:

| Param | Tipo | Descrição |
|---|---|---|
| `page` | int | Página (default 1), 100 itens por página; avançar enquanto a página vier cheia/não vazia |
| `p_start_date` | date | Início da janela, `YYYY-MM-DD` (opcional) |
| `p_end_date` | date | Fim da janela, `YYYY-MM-DD` (opcional) |
| `p_model` | slug | Filtro por modelo, ex. `z-ai/glm-5.3-flash` (opcional) |

Item típico de `data`:

```json
{
  "id": "gen-...",
  "created_at": "2026-09-21T13:44:02.123Z",
  "model": "z-ai/glm-5.3-flash",
  "app_id": null,
  "streamed": true,
  "cancelled": false,
  "generator_name": "hermes-agent",
  "cost": 0.000412,
  "usage": 0.000412,
  "tokens_prompt": 1520,
  "tokens_completion": 340,
  "tokens_total": 1860,
  "native_tokens_prompt": null,
  "native_tokens_completion": null,
  "native_tokens_reasoning": null,
  "num_media_prompt": null,
  "num_media_completion": null,
  "num_search_results": null
}
```

Campos-chave para agregação:

| Campo | Uso |
|---|---|
| `created_at` | Data/hora UTC da geração → base do agrupamento por dia/mês |
| `model` | Slug do modelo → agrupamento custo-por-modelo |
| `cost` | Custo em USD desta geração → somatório principal |
| `tokens_prompt` / `tokens_completion` | Volume de tokens → projeções e simulação de troca de modelo |
| `cancelled` | Ignorar gerações canceladas no cálculo de custo (cost já costuma vir 0) |

Notas:

- Timestamps em **UTC**; o relatório deve declarar o fuso usado na agregação.
- Rate limit: moderado (ordem de dezenas de req/min). Script usa paginação sequencial + backoff em 429.

---

## GET /models (público, sem auth)

Lista de modelos com preços:

```json
{
  "data": [
    {
      "id": "z-ai/glm-5.3-flash",
      "name": "Z.AI GLM 5.3 Flash",
      "pricing": {
        "prompt": "0.00000011",
        "completion": "0.00000044"
      },
      "context_length": 131072
    }
  ]
}
```

- `pricing.prompt` / `pricing.completion`: USD **por token**.
- Custo simulado = tokens_prompt × prompt_price + tokens_completion × completion_price.
- Use para: benchmark preço/qualidade, simular "mês de Igor no modelo X" e routing de modelos mais baratos.

---

## Segurança (regra do Igor)

- A chave vive APENAS no keyring (`secret-tool lookup service hermes-openrouter account igor`) ou env `OPENROUTER_API_KEY`.
- Nunca logar o header Authorization; nunca escrever a chave em disco/JSON; nunca ecoar erro HTTP que contenha a chave.
- Prefixo visível em erros deve ser omitido — reportar apenas "chave ausente/inválida".
