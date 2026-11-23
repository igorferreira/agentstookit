# 💀 Rastreamento de Absorções por Cartões de Negociação

> Padrão usado em Ago/2026: Inter absorveu Méliuz 2048, Carrefour, Atacadão, C&A Pay.
> Cada absorção preserva o CDB e concentra a dívida de negociação.

## O padrão

Quando Igor decide que um cartão **não será pago** (vai pra negociação), o limite disponível pode ser usado para pagar outros cartões antes do default:

1. **Identificar limite disponível real** = limite total − fatura atual − parcelamentos futuros
2. **Listar cartões pequenos a absorver** (ordem crescente de valor)
3. **Calcular**: cada absorção = `dívida_negociação += valor_absorvido`, `CDB_preservado += valor_absorvido`
4. **Atualizar controle**: fonte pagadora = "Inter (💀 negociação)", status = ✅ Pago
5. **Manter tabela viva** no CONTROLE_PAGAMENTOS.md e no dossiê do advogado

## Exemplo real (Inter, Ago/2026)

| Absorvido | Valor | CDB preservado |
|---|---|---|
| Méliuz 2048 | R$ 705 | +R$ 705 |
| Carrefour 3825 | R$ 3.721 | +R$ 3.721 |
| Atacadão 1843 | R$ 421 | +R$ 421 |
| C&A Pay | R$ 407 | +R$ 407 |
| **Total** | **R$ 5.254** | **R$ 5.254** |

> Sem as absorções, o CDB teria caído de R$ 39.000 para R$ 33.746. Com elas, ficou em R$ 39.000 (só Paulo saiu).

## Regras

- **NÃO subtrair do CDB** — a dívida só mudou de credor
- **Somar ao total de negociação** do cartão absorvente
- **Registrar comprovante** com sufixo identificando a fonte (ex: `COMPROVANTE-INTER.jpg`)
- **Atualizar dossiê** sempre que houver nova absorção
