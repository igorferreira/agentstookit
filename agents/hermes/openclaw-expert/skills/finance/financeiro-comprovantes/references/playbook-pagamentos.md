# Playbook de Pagamentos — Guia Prático de Execução

Quando o usuário pedir um "passo a passo", "playbook", "guia de execução" ou "como eu faço" para executar pagamentos de múltiplos cartões em cenários financeiros.

## Estrutura do playbook

### 1. Cabeçalho com saldo real
- Confirmar com o usuário onde cada recurso está (Nubank, C6, outras contas)
- Listar o que já está na conta vs. o que precisa ser transferido
- Mostrar saldo total após concentração

### 2. Passo 0 — HOJE (preparação)
- Resgate de CDB, transferências entre contas
- Concentrar todo dinheiro na conta de pagamento (Nubank)
- Usar checkboxes `✅` para o que já está feito, `⬜` para pendências

### 3. Blocos por data

Organizar os pagamentos em ordem cronológica:

```
📅 01/08 — Bloco CDB
📅 03/08 — Bloco Renda
📅 05/08 — Bloco Renda
...
```

Cada linha de pagamento com:

| # | Cartão/Conta | App | Valor |
|---|---|---|---|
| 1 | 👤 Paulo Guerra | Nubank → PIX (chave CPF) | R$ 10.000,00 |
| 2 | 💳 Nubank (3033) | Nubank → Cartão → Pagar fatura | R$ 5.660,52 |

### 4. Ordem das pedaladas

Pedaladas (Pix crédito via RecargaPay ou outro intermediário) **só depois** de pagar a fatura do cartão-fonte, para liberar o limite.

Sinalizar com ⚠️ e seção separada `🦶 Bloco — Pedaladas`.

### 5. Resultado final

Tabela-resumo com: pagos, sobra, parcela extra, não pagos e total a negociar.

### 6. Se houver recurso pendente

Adicionar seção "E se o crédito X chegar depois?" com recomendação de qual cartão abater primeiro.

## Nomenclatura

Nomear como `AAAA-MM-DD_PASSO-A-PASSO-<CENARIO>.md` na pasta mensal `~/MEGA/Comprovantes/YYYY/YYYY_MM_MES/`.

## Exemplo real

Arquivo: `2026-07-31_PASSO-A-PASSO-E-AJUSTADO.md`

Contexto: Cenário sem crédito extra da Caixa, Inter pago, Casas Bahia + PANs para negociação. Salário e VALLO já no Nubank, CDB a resgatar do C6.
