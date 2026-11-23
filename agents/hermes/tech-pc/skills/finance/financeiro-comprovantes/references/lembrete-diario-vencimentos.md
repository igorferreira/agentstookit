# Lembrete automático diário de vencimentos

## Quando usar

Quando o usuário pedir **notificação de contas a vencer**, **alerta no Telegram**, **cron de vencimentos** ou **lembrete diário**.

## Arquitetura

```
~/.hermes/scripts/
├── verificar-vencimentos.py    ← script Python (no_agent=True)
└── dados-vencimentos.json      ← cadastro de todas as contas
```

O cron executa `verificar-vencimentos.py` diariamente com `no_agent=True`:
- **stdout vazio** → silêncio (nada a vencer nos próximos 5 dias)
- **stdout não vazio** → entrega no Telegram

## Estrutura do JSON

O cadastro tem três seções:

### `recorrentes` — contas fixas todo mês

```json
{"nome": "Condomínio", "dia": 5, "valor": 1019.73, "categoria": "fixa"}
```

- `dia`: dia do vencimento (1–31)
- `categoria`: `"fixa"` para contas de consumo/moradia/academias/assinaturas
- Repetido a cada mês automaticamente pelo script

### `cartoes_padrao` — cartões com vencimento fixo, sem valor conhecido

```json
{"nome": "Nubank", "dia": 1, "categoria": "cartao"}
```

- Cartões cujo valor da fatura varia a cada mês entram aqui
- O script pula o cartão se houver entrada específica no mesmo dia (evita duplicidade)

### `meses_especificos` — obrigações com valor e data definidos

```json
{"nome": "Banco PAN/Buscapé final 5014 — ago", "ano": 2026, "mes": 8, "dia": 1, "valor": 6723.33, "categoria": "cartao"}
```

- Usar para: faturas de agosto com valor conhecido, parcelamentos `x/y`, empréstimos, pedaladas
- O nome deve conter o mês e um identificador único (ex.: `" — ago"`, `" — parcela 3/5"`, `" — em atraso"`)
- A deduplicação com `cartoes_padrao` funciona pelo nome base (tudo antes do `" — "`) + dia

## Como manter atualizado

Sempre que uma nova fatura chegar ou um valor mudar:

1. Adicionar ou atualizar a entrada em `meses_especificos` com o mês/ano/dia/valor corretos
2. Se for conta fixa recorrente nova, adicionar em `recorrentes`
3. Se um cartão novo aparecer (ex.: fatura nunca vista antes), adicionar em `cartoes_padrao`
4. Validar: `python3 verificar-vencimentos.py` com `FAKE_DATE=AAAA-MM-DD` para simular

## Categorias e emojis

| Categoria | Emoji |
|---|---:|
| `cartao` | 💳 |
| `fixa` | 🏠 |
| `emprestimo` | 🏦 |
| Outros | 📄 |

## Exemplo de saída

```
📋 Agenda de vencimentos — próximos dias

🔴 VENCENDO HOJE:
  🏠 Smartfit — R$ 139,00
  💳 Banco PAN/Buscapé final 5014 — ago — R$ 6.723,33

  💳 Méliuz final 2048 — ago (fechada) — R$ 704,98 — 2d (03/08 (seg))
  🏠 Condomínio — R$ 1.019,73 — 4d (05/08 (qua))

— Lembrete automático
```

## Agendamento do cron

```bash
hermes cron create \
  --name "Verificar vencimentos diário" \
  --schedule "0 8 * * *" \
  --script verificar-vencimentos.py \
  --no-agent \
  --deliver telegram
```

O cron roda às 8h da manhã. Dias sem contas nos próximos 5 dias = silêncio.

## Pitfalls

- **Cartões sem valor fixo**: se um cartão está em `cartoes_padrao` sem `mes_especifico` para o mês, o alerta mostra `—` no lugar do valor. Isso é esperado — o script não inventa valores.
- **Deduplicação por nome**: a chave de matching é `nome.split(" — ")[0]` + `dia`. Se mudar o naming pattern dos específicos, verificar se a dedup ainda funciona.
- **Mês corrente**: o script gera recorrentes e cartões padrão para o mês atual. Uma conta com vencimento dia 31 pode ser ignorada em meses com 30 dias — verificar.
- **Valor antigo no JSON**: se uma fatura fechada substituir um valor aberto, atualizar o JSON. O alerta usará o valor antigo até a atualização.
