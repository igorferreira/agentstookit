# Cenário de Pagamento — Só Essenciais (por Banco)

## Quando usar

Quando os parcelamentos futuros dos cartões inviabilizarem o cenário de
"pagar todos" e o usuário decidir manter ativos apenas os cartões de
bancos estratégicos. O restante vai para negociação (280 dias).

## Procedimento

### 1. Identificar bancos essenciais

O usuário define quais bancos manter. Exemplo real (31/07/2026):
- Nubank (conta corrente, cartão principal)
- Itaú (Passaí, Signature, Luiza Ouro — e Porto Seguro, administrado pelo Itaú)
- C6 (empréstimo, sem cartão ativo)

### 2. Calcular reserva após pagamentos

Subtrair do saldo total (conta corrente + CDB) apenas os cartões dos bancos
essenciais + dívidas pessoais prioritárias. O restante vira reserva.

### 3. Projetar parcelamentos futuros apenas dos essenciais

Montar matriz apenas com os cartões que continuam ativos. Os cartões que
foram pra negociação têm seus parcelamentos CANCELADOS (vão compor a dívida
negociada, não o fluxo mensal).

### 4. Projetar reserva mês a mês

```
Reserva inicial = saldo - pagamentos essenciais

Para cada mês:
  fluxo = renda - C6 - custo_vida - parcelas_essenciais
  reserva += fluxo
```

### 5. Incluir eventos de renda extra

- Dissídio anual: reflete no contracheque de outubro/novembro (~4%)
- 13º 1ª parcela: novembro (50% bruto, sem descontos)
- 13º 2ª parcela: dezembro (com INSS+IRRF)
- VALLO extra no 13º (valor a confirmar)

### 6. Projetar até a data-alvo de quitação

Estender a projeção até dezembro do ano seguinte (ou mais) para mostrar
quanto dinheiro estará acumulado quando os acordos de negociação estiverem
maduros (após ~280 dias).

## Indicadores-chave

| Indicador | O que mostra |
|---|---|
| Reserva inicial | Quanto sobra após pagar os essenciais |
| Pior momento | Mês com menor reserva — se zerar, inviabiliza |
| Reserva em dez/ano+1 | Quanto terá para quitar acordos |
| Folga mensal pós-parcelas | A partir de quando o fluxo vira positivo |

## Pitfalls

### Não confundir "banco administrador" com "banco diferente"
Porto Seguro cartão de crédito é administrado pelo Itaú. Se o usuário
decidir "manter só Itaú", o Porto Seguro entra no pacote.

### Parcelamentos dos cartões negociados SOMEM do fluxo
Quando um cartão vai pra negociação, seus parcelamentos futuros deixam
de ser despesa mensal e passam a compor o montante a negociar. Isso
MELHORA o fluxo de caixa futuro — é a principal vantagem do cenário.

### A reserva pode cair antes de subir
É normal a reserva diminuir nos primeiros 2-3 meses (parcelamentos
ainda altos) e depois começar a subir quando os parcelamentos expiram.
O importante é que nunca zere.
