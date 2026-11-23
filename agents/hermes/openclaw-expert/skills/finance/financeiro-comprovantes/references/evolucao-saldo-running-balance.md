# Evolução do Saldo — Running Balance Visual

## Quando usar

Quando o usuário pedir para visualizar o impacto de cada pagamento no saldo
da conta, ou quiser "ver o dinheiro saindo" ao longo do mês. Útil após
definir um cenário de pagamento e antes da execução.

## Estrutura do documento

### Cabeçalho

```
# 💸 Cenário X — Evolução do Saldo | Pagamento por Pagamento
> Saldo inicial: R$ XX.XXX,XX (Nubank R$ X + CDB C6 R$ X já transferido)
```

### Blocos por data

Cada bloco tem: data, tabela com #, Cartão/Conta, Débito, Saldo.

```
## 📅 01 de Agosto (sexta)
| # | Cartão/Conta | Débito | Saldo |
| | 💰 Saldo inicial | | R$ 52.923,34 |
| 1 | 👤 Paulo Guerra (PIX) | −R$ 10.000,00 | R$ 42.923,34 |
```

### Gráfico ASCII

No final, incluir gráfico de barras mostrando a curva de queda:

```
52.923 █
42.923 █░ (Paulo -10k)
37.262 █░░ (Nubank -5,6k)
  ...
 2.524 █░░░░░░░░░░░░░░ (BrasilCard final)
```

## Regras

- O saldo inicial deve ser o **saldo real confirmado** pelo usuário (não o teórico)
- Cada débito subtrai do saldo anterior
- Pedaladas (Pix crédito) são marcadas como "não sai do caixa" e não afetam o saldo
- O saldo final deve bater com a reserva/CDB final do cenário
- Incluir seção de "Não pagos" e "Zerados" ao final
