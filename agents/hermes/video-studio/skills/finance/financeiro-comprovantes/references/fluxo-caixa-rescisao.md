# Fluxo de Caixa — Cenários de Rescisão

## Quando usar

Quando Igor pedir "fluxo de caixa rescisão", "e se eu for demitido", "prevenção rescisão" ou similar: combinar os cálculos de rescisão da pasta CARREIRA com o fluxo de caixa mensal para mostrar quanto tempo cada cenário cobre.

## Fontes de dados

1. **Rescisão**: `~/MEGA/Documentos/carreira/rescisao_clt/`
   - `dados-contrato.json` — premissas atualizadas (salário, FGTS, modalidade, VALLO)
   - `relatorios/2026-07-23_ESTIMATIVA-RESCISAO-FGTS-REAL.md` — estimativa mais recente

2. **Fluxo de caixa**: `~/MEGA/Comprovantes/`
   - `FLUXO-CAIXA-2026-2030.md` — projeção normal (com renda)
   - `HOME-EQUITY.md` — cronograma SAC (continua pós-rescisão)
   - `CONTRACHEQUE.md` — projeção salarial

## Premissas pós-rescisão

| Item | Tratamento |
|---|---|
| CLT | **R$ 0** — cessa com o vínculo |
| VALLO | **R$ 0** — vinculado ao emprego |
| Home Equity | **Continua** — empréstimo pessoal, parcela SAC decrescente |
| Empréstimo folha | Descontado da rescisão (saldo devedor abatido) |
| Custo de vida | Mantido (R$ 4.421/mês em cartões pós-Jul/2027) |
| FGTS (saque-aniversário) | **Não libera saldo** na dispensa — só multa de 40% |
| CDB | Reserva intacta — pode ser usada como extensão |

## Estrutura do relatório

1. **Resumo dos cenários** — tabela com os 4 cenários (pedido demissão com/sem desconto, dispensa, dispensa + seguro)
2. **Premissas** — saída mensal (HE + custo de vida), o que cessa
3. **Mês a mês por cenário** — tabela mostrando saldo inicial → −HE → −custo de vida → saldo final, até zerar
4. **CDB como rede de segurança** — repetir cada cenário adicionando o saldo do CDB
5. **Alerta FGTS bloqueado** — destacar que saque-aniversário impede acesso ao saldo
6. **Recomendações** — cancelar saque-aniversário, manter CDB ≥ R$ 35k, nunca pedir demissão

## Fórmula mensal

```
saldo_final = saldo_inicial - parcela_HE - custo_de_vida
```

- `parcela_HE`: usar cronograma SAC real do `HOME-EQUITY.md`
- `custo_de_vida`: R$ 4.421 (fixo após Jul/2027, pode ser maior antes com parcelamentos)
- Para cenários com seguro-desemprego: adicionar +R$ 2.519 por 5 meses

## Pitfalls

- **Não somar FGTS bloqueado ao caixa imediato** — saque-aniversário impede
- **Não presumir que o HE para** — é empréstimo pessoal, continua
- **Não usar R$ 9.000 como custo mensal sem verificar** — o valor real é ~R$ 8.680 (HE + faturas)
- **Atualizar após cada dissídio** — a rescisão cresce com o salário

## Arquivo gerado

`~/MEGA/Comprovantes/FLUXO-CAIXA-RESCISAO.md`
