---
name: finops-ia-gastos
description: Use ao medir e otimizar o custo de IA do Usuário — gastos OpenRouter (pay-per-token) vs assinaturas fixas (ChatGPT Plus, Claude Pro, Gemini Advanced, Manus), projeção de saldo, alerta de crédito 402 e relatório mensal. Segurança absoluta: a chave de API nunca é lida, impressa ou colada — só via keyring/env pelo próprio Usuário.
---

# FinOps IA — gastos de IA do Usuário (OpenRouter vs assinaturas)

Você cuida do dinheiro que a IA do Usuário custa. Números primeiro, enrolação nunca.

## Fontes de verdade

- **Assinaturas fixas:** `ASSINATURAS-FIXAS.md` (nesta skill) — também espelhado em `~/MEGA/Documentos/financas_bancos/ASSINATURAS.md`.
- **Relatórios gerados:** `~/MEGA/Documentos/financas_bancos/IA-FINOPS/` (JSON + `INDEX.md`).
- **Script de coleta:** `~/.hermes/scripts/finops-openrouter.py`.
- **Regras do Usuário:** `~/MEGA/Regras/financas.md` antes de agir.

## Regra ABSOLUTA de segurança (não negociável)

**NUNCA ler, buscar, imprimir, copiar ou expor chaves de API ou credenciais** — nem `.env`, nem `config.yaml`, nem keyring. Vale checar apenas PRESENÇA (retorna vazio vs não-vazio), nunca conteúdo.

- A chave vive SÓ em: `secret-tool lookup service hermes-openrouter account usuario` ou `OPENROUTER_API_KEY` (o script já faz isso).
- Se ausente, peça ao Usuário para armazenar ELE MESMO (nunca colar no chat):
  ```
  secret-tool store --label=OpenRouter service hermes-openrouter account usuario
  ```

## API OpenRouter (o que funciona de verdade — verificado na doc oficial em 23/09/2026)

Detalhes completos em `references/api-openrouter.md`. Resumo operacional:

1. **`GET /api/v1/credits`** — saldo: `total_credits`, `total_usage`, `total_balance` (USD).
2. **`GET /api/v1/activity?date=YYYY-MM-DD`** — UM dia UTC por chamada, agregado por modelo: `usage` (custo USD), `requests`, `prompt_tokens`, `completion_tokens`, `model`. **Não existe** filtro de período (`start_date`) nem paginação.
3. **Janela de 30 dias UTC**: dias mais antigos que ~30 voltam vazios. Histórico > 30 dias é IMPOSSÍVEL via API — o histórico real vive nos JSONs de `IA-FINOPS/`. Por isso o cron mensal é obrigatório.
4. **MANAGEMENT KEY obrigatória**: os dois endpoints rejeitam chave de chat com `403 "Only management keys can perform this operation"`. Usuário precisa criar uma Management Key em `https://openrouter.ai/settings/management-keys` e armazená-la no keyring.
5. **402 = sem crédito**: previsto pelo script (alerta de projeção vs saldo) antes de acontecer.

## Procedimento padrão

### Coleta mensal (cron, automático)
Cron `finops-ia-relatorio-mensal` — roda dia 1º de cada mês 09h, `--no-agent`, entrega no Telegram. Captura mês corrente + anterior (o anterior fica ~1–2 dias furado dentro da janela de 30 — documentado; se precisar do mês fechado completo, rodar manualmente no dia 2).

### Relatório manual
```
python3 ~/.hermes/scripts/finops-openrouter.py --compare   # mês corrente + anterior + saldo + comparativo
python3 ~/.hermes/scripts/finops-openrouter.py --month 2026-09
```

### Como responder ao Usuário
- Tabela por modelo + total + projeção + saldo.
- Todo número tem fonte: "medido (API)" ou "estimativa (fórmula)".
- Câmbio US→BRL: citar a taxa usada e a data; sem cotação do dia, declarar estimativa.
- Comparativo típico: fixas US$ 79,99/mês (≈ R$ 408) vs OpenRouter variável; opinião de otimização SÓ depois dos números.
- Nunca cancelar/alterar assinatura sem pedido explícito.

## Otimização (o valor do Caco)

- **Pay-per-token vs assinatura**: assinatura compensa quando o uso mensal do serviço ≥ valor da mensalidade em tokens; com dados reais do `/activity`, calcular o equivalente. O modelo usual do Usuário no OpenRouter é `z-ai/glm-5.3-flash` (flash barato — quase sempre mais barato por token que dedicação de assinatura para uso pesado de agente).
- **Routing**: tarefas mecânicas em flash/barato; raciocínio pesado pontual em modelo caro. Medir antes de trocar.
- **Alerta 402**: o script avisa quando projeção do mês excede saldo — agir ANTES do estouro, nunca depois.
