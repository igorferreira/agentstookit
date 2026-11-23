# Análise de Cenários e Pedaladas

## Quando usar

- "vale a pena pedalar?"
- "compara opção A vs B"
- "simula X vs Y"
- "qual o impacto de fazer Z?"
- "se eu receber R$ X, como fica?"

## Estrutura da análise

Toda análise deve responder em 3 blocos:

### 1. Comparativo rápido (tabela)

| | Sem pedalada | Com pedalada |
|---|---|---|
| CDB mínimo | R$ X | R$ Y |
| CDB final | R$ X | R$ Y |
| Custo | R$ 0 | R$ Z |

### 2. Mecânica (passo a passo)

Explicar em 3-5 linhas o que acontece mês a mês:
- Set: Pix crédito X → líquido Y → cobre déficit → CDB não mexe
- Out: paga fatura + pedala de novo → CDB cobre Z
- Nov: 13º quita

### 3. Veredito

- ✅ Vale a pena se: [condição]
- ❌ Não vale se: [condição]
- ⚠️ Depende de: [fator]

## Regras para pedaladas

### Pedalada com cartão ativo (ex: Carrefour, Luiza)

- O cartão PRECISA ser pago (ativo)
- Cada ciclo: paga fatura → libera limite → Pix crédito → dinheiro entra
- Custo: taxa do Pix crédito (~5%)
- A dívida fica no próprio cartão (bola de neve)
- Só funciona se o 13º/quitar no curto prazo (até Nov/Dez)
- Risco: se não pagar a fatura seguinte, o cartão ativo vira inadimplente

### Pedalada com cartão de negociação (ex: Inter, Digio)

- Cartão NÃO está sendo pago
- Usar limite disponível antes que seja bloqueado
- Custo real = valor pedalado × (1 - desconto negociação)
- Ex: pedala R$ 1.000, desconto 50% → custo real R$ 500
- ⚠️ Igor prefere pedalar com cartão ATIVO, não de negociação

### Cálculo do líquido

```
líquido = limite_disponível × (1 - taxa)
```

Taxas típicas:
- Pix crédito RecargaPay: ~5%
- Pix crédito direto do app do banco: ~5-8%

## Salvamento

Após a análise:
1. Salvar MD + PDF em `YYYY/_Analises/AAAA-MM-DD_ANALISES-<TOPICO>.md`
2. Atualizar `INDEX-CENARIOS.md` com a nova linha
3. Salvar JSON do cenário se for um novo X(N) em `cenarios/fluxo_xN.json`
