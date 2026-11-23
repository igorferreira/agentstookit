# Projeção de Longo Prazo — Limpar o Nome (até Dez/Ano+1)

## Quando usar

Quando o usuário quiser saber se, com o cenário de pagamento escolhido,
conseguirá acumular dinheiro suficiente para quitar as dívidas negociadas
após o período de 280 dias (Lei do Superendividamento / Consumidor.gov.br).

## Procedimento

### 1. Definir o ponto de partida

- Reserva inicial: saldo após pagamentos do mês corrente
- Renda mensal base (CLT líquido recorrente + VALLO)
- Compromissos fixos: C6 (SAC, parcela decrescente), custo de vida

### 2. Mapear eventos de renda extra no horizonte

| Evento | Quando | Como projetar |
|---|---|---|
| Dissídio anual | Out/Nov | +4% sobre salário e VALLO |
| 13º 1ª parcela | Nov | 50% do bruto, sem descontos |
| 13º 2ª parcela | Dez | 50% do bruto − INSS − IRRF |
| 2º dissídio | Out/Nov ano+1 | +4% sobre novos valores |

### 3. Projetar mês a mês

Criar tabela com colunas: Mês, Renda, 13º, C6, Custo, Parcelas, Fluxo, Reserva.

### 4. Marcar o fim dos parcelamentos

Identificar em que mês TODOS os parcelamentos dos cartões ativos chegam a
zero. A partir desse mês, a folga mensal dá um salto.

### 5. Simular quitação no ponto-alvo

No mês em que os 280 dias de negociação terminam (~junho do ano seguinte),
simular o pagamento dos acordos:

```
Dívida total negociada × (1 − desconto estimado) 
  = valor a pagar
Reserva acumulada − valor a pagar 
  = saldo pós-quitação
```

Usar faixa de desconto (ex.: 40% a 60%) para mostrar cenários conservador
e otimista. Não tratar nenhum percentual como garantido.

### 6. Projetar até dezembro do ano seguinte

Estender a projeção até dezembro para mostrar o saldo acumulado com um
ano completo de folga positiva pós-parcelamentos.

## Exemplo real (31/07/2026)

> **⚠️ Exemplo histórico (31/07/2026) — números desatualizados.** A dívida em negociação já mudou (era 15 cartões/~R$67.000; hoje ver `~/MEGA/Comprovantes/ENDIVIDAMENTO.md` seção 1 para a contagem e o total atuais). Mantido aqui só para ilustrar a estrutura do cálculo, não como referência de valor.

Cenário Z (Nubank + Itaú + Porto):
- Reserva inicial: R$ 34.245
- Parcelamentos zeram em ago/27
- Reserva em dez/27: R$ 108.491
- Dívida a negociar: ~R$ 67.000 (15 cartões)
- Após desconto 40-60%: R$ 26.800 a R$ 40.200
- Pós-quitação: R$ 68.000 a R$ 81.000 livres

## Pitfalls

### Não projetar dissídio antes de outubro
Historicamente o dissídio FEAAC (data-base agosto) só reflete no
contracheque de outubro ou novembro. Não inflar a renda de ago-set.

### C6 é SAC — a parcela cai todo mês
Modelar a redução de ~R$ 40/mês na parcela do C6. Não usar valor fixo.

### A reserva pode cair nos primeiros meses
Os parcelamentos ainda altos consomem mais que a renda nos meses iniciais.
A reserva cai até os parcelamentos expirarem — isso é esperado.
O que importa é que nunca zere.

### Não confundir "negociado" com "quitado"
A projeção mostra o dinheiro acumulado para PAGAR os acordos. Os acordos
em si dependem de negociação efetiva com os credores — a projeção mostra
CAPACIDADE de pagamento, não garantia de acordo.
