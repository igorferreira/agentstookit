# Multa FGTS 40% — optante saque-aniversário (receita de cálculo)

Base legal: art. 18 §1º e art. 20-D §7º da Lei 8.036/90; TST IRR 255. Fonte de consulta: fgts.gov.br.

## Regras que definem o valor

- A base legal da multa é o **histórico completo de depósitos corrigidos**, NÃO o saldo atual da conta. Saques-aniversário já realizados não reduzem a base — recalcular a partir do saldo atual subestima a multa.
- Optante saque-aniversário saca **apenas a multa de 40%** na dispensa sem justa causa. O saldo (garantia da antecipação + parte livre) fica retido; nem o retorno ao saque-rescisão no 25º mês libera o saldo desta demissão.
- Extrato com mais de ~3 meses é dado não atual: estimar depósitos desde então, rotular como estimativa e não lançar no fluxo de caixa.

## Dois cenários do depósito rescisório (apresentar sempre os dois)

O depósito rescisório de 8% entra na base da multa, mas a lei não define se incide sobre todas as verbas ou só sobre o saldo de salário:

| | Padrão trabalhista (recomendado) | Conservador |
|---|---|---|
| Base da multa | extrato + depósitos mensais + 8% sobre TODAS as verbas do TRCT | extrato + depósitos mensais + 8% só sobre o saldo de salário |

A diferença entre os cenários passa de R$ 2.000 (base de 3+ anos). O valor exato sai no FGTS Digital/TRCT — apresentar o padrão como principal e o conservador como piso.

## Âncora real: o campo "VALOR PARA FINS RESCISÓRIOS" do extrato Caixa

Quando o extrato FGTS da Caixa chegar, o campo **VALOR PARA FINS RESCISÓRIOS** substitui as estimativas — ele JÁ É a base completa corrigida (histórico de depósitos + JAM), então as parcelas S + M da fórmula se fundem num único número real:

- Multa = 0,4 × (valor para fins rescisórios + R), onde R é o depósito rescisório do cenário
- Os mesmos dois cenários de R continuam obrigatórios (8% sobre todas as verbras vs 8% só saldo de salário)
- Ler também do extrato: saldo final da conta, o valor bloqueado pela antecipação (para separar "retido" de "sacável") e a data do último depósito
- Truncar estimativas antigas no relatório: substituir a tabela de estimativa e marcar as pendências de FGTS como resolvidas, apontando o arquivo do extrato como fonte

## Fórmula fechada (quando o saldo atualizado ainda não chegou)

Com S = saldo informado pelo Igor, depósitos mensais M = 8% da base × meses desde o extrato, e R = depósito rescisório do cenário:

- Multa padrão = 0,4 × (S + M + R)

Entregar a fórmula com S como única variável pendente, e recalcular/reemitir o relatório quando o valor chegar — não recomeçar o cálculo do zero.

## O que entra em M

- Depósitos mensais: 8% da base salarial × meses desde o extrato usado (mês do extrato já está dentro dele).
- R (padrão) = 0,08 × TRCT bruto total (incluindo saldo, aviso, 13º, férias — TODAS as verbas).
- R (conservador) = 0,08 × saldo de salário apenas.
