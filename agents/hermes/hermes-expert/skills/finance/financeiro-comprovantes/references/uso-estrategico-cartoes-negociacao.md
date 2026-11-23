# Uso Estratégico de Cartões que Vão pra Negociação

## Conceito

Antes de parar de pagar um cartão (que vai pra negociação), usar o limite disponível dele para cobrir despesas essenciais que seriam pagas com dinheiro (CDB/conta). Cada real gasto no cartão "não vou pagar" = 1 real preservado no bolso.

## Pré-requisitos

- O cartão está na lista de **negociação** (não será pago)
- O cartão ainda tem **limite disponível**
- A operação é feita **antes** do vencimento (cartão ainda ativo)
- O valor cabe no limite sem estourar

## Padrões de uso

### 1. Pagamento de contas essenciais (luz, gás, água)

Usar o limite do cartão de negociação para pagar boletos de consumo via RecargaPay.

**Exemplo real (31/07/2026):**
- Cartão Dígio (negociação) → RecargaPay → pagou Naturgy (R$ 146,22 + R$ 23,30) + Light (R$ 778,04)
- Total: R$ 947,56 que **não saíram do CDB**

**Fluxo:**
1. RecargaPay → Pagar boleto → escolher "Cartão de Crédito"
2. Selecionar o cartão de negociação como pagador
3. O valor aparece na fatura do cartão de negociação (que não será paga)
4. Salvar comprovante como `COMPROVANTE-DIGIO` (identificar o cartão usado)

### 2. Cobertura de cheque especial

Quando o cheque especial (8% a.m. no Nubank) vai debitar juros pesados, usar PIX crédito de um cartão de negociação para cobrir.

**Exemplo real (31/07/2026):**
- Cheque especial Nubank: R$ 4.231,80 (juros + IOF, débito 03/08)
- Cartão Inter (negociação, limite R$ 20.000) → RecargaPay PIX crédito → conta Nubank
- ~R$ 4.400 no Inter cobre os R$ 4.232 do CE
- Custo real: zero (cartão não será pago)

**Fluxo:**
1. RecargaPay → PIX no crédito
2. Valor = dívida + ~3,99% (taxa RecargaPay)
3. PIX para a conta que será debitada
4. O débito automático cobre o cheque especial
5. A dívida aparece na fatura do cartão de negociação

### 3. Antecipação do limite antes do bloqueio

Se o emissor costuma bloquear o cartão logo após o primeiro atraso, **concentrar o uso antes do vencimento**:

- Pagar todas as contas possíveis no mesmo dia
- Fazer PIX crédito se ainda houver limite
- O objetivo é esgotar o limite enquanto o cartão está ativo

## Regras de registro

- Criar `.md` com sufixo `COMPROVANTE-DIGIO`, `COMPROVANTE-INTER` etc. (identificar o cartão)
- No controle mensal, adicionar nota: "Pago com cartão X (negociação)"
- Somar ao total "queimado" do cartão: valor original + pedaladas
- NÃO subtrair do CDB — o dinheiro fica preservado
- NO fluxo de caixa: essas despesas NÃO aparecem como saída de caixa

## Cuidados

- ⚠️ Fazer ANTES do vencimento do cartão (cartão vencido = bloqueado)
- ⚠️ RecargaPay cobra ~3,99% para Pix crédito e pagamento de boleto com cartão
- ⚠️ O limite do cartão de negociação é finito — priorizar as maiores despesas
- ⚠️ Não usar cartão de banco que você quer MANTER (ex.: não queimar Nubank ou Itaú)
- ⚠️ Guardar todos os comprovantes — o advogado vai precisar

## Impacto no fluxo de caixa

| Sem estratégia | Com estratégia |
|---|---|
| Contas saem do CDB | Contas saem do cartão de negociação |
| CDB diminui | CDB preservado |
| Dívida do cartão de negociação = só fatura | Dívida = fatura + contas + Pix |

> 🎯 A diferença líquida: o CDB fica maior, a dívida total também, mas a dívida adicional está num cartão que **já não seria pago de qualquer forma**.
