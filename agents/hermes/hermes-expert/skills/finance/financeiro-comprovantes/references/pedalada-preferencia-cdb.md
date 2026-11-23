# Pedalada estratégica — preferências e mecânica (13/08/2026)

> **PREFERÊNCIA #1 DO USUÁRIO (13/08/2026): preservar o CDB a qualquer custo.**

Quando o usuário cogitar "pedalar", "girar" ou "deixar para pagar depois" no cartão para evitar saldo negativo, esta é a referência. A escolha de mecanismo depende da diferença de custo vs resgate do CDB e do quanto o usuário valoriza manter a reserva intacta.

## Os 4 caminhos para "pedalar" (do mais barato ao mais caro)

Para um valor de **R$ 1.200, 1 mês** (cenário típico de Usuário):

| # | Mecanismo | Custo 1 mês | Custo 3 meses | Preserva CDB? | Custo de score? |
|---|---|---:|---:|:---:|:---:|
| 1 | Resgate do CDB C6 | −R$ 12 (perde rendimento) | −R$ 36 (perde rendimento) | ❌ Não | Não |
| 2 | **PIX no crédito Carrefour 4,99% a.m.** | **R$ 60** | **R$ 191** | **✅ Sim** | Não |
| 3 | Cheque especial Nubank ~8% a.m. | R$ 96 | R$ 314 | ✅ Sim | Sim (uso de OD) |
| 4 | Rotativo tradicional Carrefour ~15% a.m. | R$ 180 | R$ 625 | ✅ Sim | Sim (alta utilização) |

> ⚠️ **Atenção:** o app do Carrefour pode chamar a opção de "pedalar a fatura" de várias formas — "parcelar fatura", "parcelamento automático", "rotativo", "PIX no crédito" ou "refinanciamento". Antes de calcular o custo, **perguntar qual mecanismo o usuário escolheu**. Não assumir rotativo 15% por padrão.

## Preferência explícita do Usuário

> "gastar o CDB" incomoda muito mais que "pagar juros em PIX no crédito"

Mesmo quando o resgate do CDB é **R$ 60 mais barato** que o PIX no crédito, Usuário prefere pagar os R$ 60 de juros e manter o CDB intacto. A justificativa dele: "a tranquilidade da reserva vale mais que a economia".

**Implicação operacional:**
- Antes de sugerir resgate de CDB, **mostrar essa preferência e perguntar** se ainda quer manter.
- Padrão de resposta: comparar os 4 caminhos com custo em reais + "qual te incomoda mais — gastar o CDB ou pagar R$ X de juros?"
- Não usar tom prescritivo ("você deveria resgatar o CDB"). Usar escolha informada.

## Estrutura padrão de resposta quando o usuário cogita pedalar

```markdown
1. Acolhimento (1-2 linhas): "Entendo, vamos olhar com calma."
2. Os 4 caminhos com custo em R$:
   - Tabela com 4 linhas, custo 1 mês e 3 meses
   - Marcar qual preserva o CDB
3. Pergunta: "qual te incomoda mais — gastar o CDB ou pagar R$ X de juros?"
4. Após a escolha: aplicar a mecânica no fluxo
5. Atualizar: `_fichas/FICHA_CARTAO_*.md` (parcelamento novo), `CONTROLE_FATURAS_MANTIDOS.md` (próximo mês), `FLUXO-CAIXA-2026-2030.md` (+custo juros), playbook específico
6. Finalizar mostrando saldo do CDB
```

## Consequências não-óbvias (registrar na resposta)

- **Rotativo tradicional** (15% a.m.): banco força parcelamento depois de 1-2 meses → perda de controle, CET pior, uso do limite sobe e derruba score, pode bloquear novas compras.
- **PIX no crédito** (4,99% a.m.): tratado como **compra parcelada comum**. Sem efeito colateral no score, sem mudança no uso do limite visível, sem forçar parcelamento. É o mecanismo preferido do Usuário.
- **Cheque especial** (8% a.m.): juros compostos diariamente. Um déficit de R$ 1.000 vira R$ 1.349 em 30 dias, R$ 1.820 em 60 dias. Sempre modelar a projeção.
- **CDB resgate** (1% a.m. perdido): sem custo direto mas zera a reserva — Usuário valoriza manter a reserva.

## Checklist operacional após pedalar

1. Salvar a evidência (imagem/PDF) na pasta mensal com sufixo identificando a operação (ex.: `COMPROVANTE-PIX-CREDITO-CARREFOUR-R1000`).
2. Criar `.md` com metadados: data, valor, mecanismo, fatura de origem, fatura de destino, custo (juros).
3. Atualizar `_fichas/FICHA_CARTAO_*.md` com nova linha de parcelamento (valor, mês, parcelas restantes).
4. Atualizar `_controles/CONTROLE_FATURAS_MANTIDOS.md`: marcar a fatura de origem como "paga parcial R$ X" e adicionar linha na fatura de destino com o valor pedaled.
5. Atualizar `FLUXO-CAIXA-2026-2030.md`: somar o pedaled + juros na linha "Faturas" do mês de destino; reduzir CDB em "Saldo" do mês de origem (se for resgate) — ou **não** reduzir (se for PIX no crédito).
6. Gerar/atualizar o `playbook-negociacao-cartoes.md` ou `playbook-pagamentos.md` específico da operação.
7. Conferir se o app **não** deixou sobra (ex.: R$ 6,87) cair em rotativo 15% — se sobrar, pagar junto.

## Pitfall: sobra residual vai para rotativo automaticamente

Se o usuário pedala R$ 1.000 de uma fatura de R$ 2.006,87, o app do Carrefour pode deixar os R$ 6,87 restantes caírem em **rotativo tradicional 15% a.m.** em vez de parcelar junto. Para evitar isso:

- Pagar valor exato que cobre o que vai pedalar (R$ 1.000) **mais a sobra** (R$ 6,87) = R$ 1.006,87 direto → não sobra nada para rotativo.
- OU pagar um pouco a mais para garantir que o app entenda a operação como "pagar + parcelar X".

Confirmar isso na fatura do mês seguinte, especialmente se o app mostrou o valor pago e o valor restante.

## Pedalada "R$ 1.000 pedalar" ≠ "R$ 1.000 de dívida nova"

Quando Usuário pedala R$ 1.000:
- O custo é **só a taxa** (R$ 49,90 a 4,99% Carrefour, ou R$ 12 perdido do CDB).
- A dívida **migra** para a próxima fatura como compra parcelada comum, não vira rotativo novo.
- A diferença importa para o **score**: PIX no crédito não aumenta utilização de limite do jeito que rotativo faz.

---

**Veja também:**
- `references/playbook-pagamentos.md` — passo a passo prático de cada pedalada
- `references/analise-pedaladas.md` — análise comparativa entre cenários de pedalada
- `references/cdb-ponte-deficit.md` — uso do CDB como ponte de déficit (a EVITAR para Usuário)
- `references/cenarios-financeiros-ab.md` — comparação entre estratégias maiores
