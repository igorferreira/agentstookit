# Padrão 4: Absorção de outros cartões

Quando um cartão de negociação tem **limite alto** e vários cartões pequenos têm dívidas, usar o cartão grande para "absorver" as dívidas dos pequenos, consolidando tudo em um único bloco de negociação.

## Caso real: Inter absorvendo 5 cartões (31/07/2026)

> **⚠️ Exemplo histórico (31/07/2026) — anterior à reclassificação de 03/08/2026** (quando Porto Seguro e Atacadão passaram para ativos). Os valores de "cartões para negociar" abaixo não refletem o estado atual — ver `~/MEGA/Comprovantes/ENDIVIDAMENTO.md` seção 4 e `CONTROLES.md`. Mantido só para ilustrar o padrão de absorção.

### Situação inicial

| Cartão | Valor | Status |
|---|---|---|
| Inter (1982) | R$ 17.517 | 💀 Negociação |
| Limite disponível | R$ 20.490 | |

### Absorção executada

| Absorvido | Valor | Como |
|---|---|---|
| Méliuz 2048 | R$ 705 | Pagamento via Inter |
| Carrefour 3825 | R$ 3.721 | Pagamento via Inter |
| Atacadão 1843 | R$ 421 | Pix crédito Inter |
| C&A Pay | R$ 407 | Pix crédito Inter |
| Porto Seguro 8121 | R$ 6.792 | ⬜ Tentando |

### Resultado

| | Antes | Depois |
|---|---|---|
| Cartões para negociar | 12 separados | 7 blocos (Inter consolidado) |
| CDB preservado | R$ 0 | **R$ 6.792** (Porto não saiu do CDB) |
| Dívida Inter | R$ 17.517 | **R$ 22.771** |

## Quando usar

- Cartão de negociação tem **limite ≥ R$ 15.000 disponível**
- Cartões a absorver têm dívidas pequenas/médias (R$ 400–R$ 4.000)
- A absorção **preserva CDB** que seria usado para pagar esses cartões
- O cartão absorvedor **já vai pra negociação de qualquer forma**

## Vantagens

- 🎯 **Consolidação**: em vez de 12 CNPJs diferentes negociando, são ~7
- 📦 **CDB preservado**: cada real absorvido = 1 real a mais na reserva
- 📊 **Negociação mais simples**: um bloco grande é mais fácil de negociar que vários pequenos
- 🛡 **Proteção contra processo**: valores pequenos diluídos num bloco grande têm menos risco individual

## Cuidados

- ⚠️ Verificar se o limite do absorvedor comporta TODOS os absorvidos + taxa RecargaPay (~3,99%)
- ⚠️ Não absorver cartão do mesmo emissor que você quer manter (ex: não usar Inter pra absorver Itaú se você quer manter relação com Itaú)
- ⚠️ Se o absorvedor tiver risco de processo (ex: Santander), não concentrar tudo nele
- ⚠️ Registrar cada absorção com comprovante e atualizar controle de pagamentos
