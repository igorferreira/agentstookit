# Cenários financeiros A/B — documento de decisão

Quando o usuário estiver entre duas estratégias financeiras mutuamente exclusivas (ex.: pagar cartão A vs cartão B, usar Pix crédito vs não usar), gerar um documento de comparação.

## Estrutura

1. **O que é IGUAL nos dois cenários** — tabela com todos os itens comuns, para não repetir.
2. **O que MUDA** — tabela de 2 colunas (Cenário A vs Cenário B) com a decisão binária.
3. **Cenário A detalhado** — caixa, pagos, não pagos, projeção mensal, riscos.
4. **Cenário B detalhado** — mesma estrutura.
5. **Comparativo final** — tabela lado a lado com indicadores-chave.
6. **Resumo** — 1-2 linhas por cenário.

## Indicadores-chave no comparativo

| Indicador | Por que importa |
|---|---|
| CDB final | Reserva de emergência após todos os pagamentos |
| Folga mensal (set+) | Quanto sobra por mês após parcela C6 |
| Parcela extra | Compromisso mensal adicional (ex.: Pix crédito) |
| Total não pagos | Valor que vai para negociação |
| Risco imediato | Qual cartão já está atrasado ou vence primeiro |

## Regras

1. Os dois cenários devem ser autônomos — cada um pode ser lido isoladamente.
2. Se o usuário pedir "cria um arquivo pra cada cenário", gerar arquivos separados com nome `CENARIO-A-<TEMA>.md` e `CENARIO-B-<TEMA>.md`.
3. Incluir prós/contras em cada cenário com ✅ e ❌.
4. Nunca escolher pelo usuário — apresentar dados, deixar a decisão para ele.
5. Atualizar a seção de RISCOS com o pior cenário realista (negativação, juros, perda de giro).

## Pitfall: contaminação de subtotais

Ao calcular totais de "A PAGAR", garantir que o filtro é exato: `"✅ A PAGAR" in status`, NÃO `"PAGO" in status` (que capturaria incorretamente "NÃO PAGO"). Verificar com `assert` ou inspeção manual antes de gravar.
