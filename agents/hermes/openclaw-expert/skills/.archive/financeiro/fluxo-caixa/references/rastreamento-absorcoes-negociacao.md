# 💀 Rastreamento de absorções por cartão de negociação

Quando o usuário decide usar crédito de um cartão que **não será pago** (vai pra negociação) para pagar cartões mantidos, cada pagamento **aumenta a dívida de negociação**.

## Padrão de atualização

Cada absorção segue 3 passos:

### 1. Registrar no controle de pagamentos

No `CONTROLE_PAGAMENTOS.md` do mês, marcar:
- Status: `✅ Pago`
- Fonte pagadora: `Inter (💀 negociação)` ou `Dígio (💀 negociação)`

### 2. Atualizar o total da dívida de negociação

Manter um running total em memória ou no arquivo de diagnóstico:

```
💀 Inter: R$ 17.517 + Méliuz R$ 705 + Carrefour R$ 3.721 + Atacadão R$ 421 + C&A R$ 407 = R$ 22.771
```

### 3. Atualizar o fluxo de caixa

O fluxo de caixa (`FLUXO-CAIXA-2026-2030.md`) não é alterado a cada absorção — ele já considera que esses cartões vão pra negociação. A atualização só é necessária quando:
- O total absorvido muda significativamente o CDB disponível (ex: Porto Seguro foi pro Inter → CDB preservou R$ 6.792)
- A data do acordo de negociação é definida

## Exemplo da sessão

| Cartão pago | Valor | Fonte | Inter acumulado |
|---|---|---|---|
| Méliuz 2048 | R$ 705 | Inter | R$ 18.222 |
| Carrefour 3825 | R$ 3.721 | Inter | R$ 21.943 |
| Atacadão 1843 | R$ 421 | Inter | R$ 22.364 |
| C&A Pay | R$ 407 | Inter | R$ 22.771 |

## Relação com CDB

- Cada absorção pelo Inter/Dígio **preserva** o CDB
- Se o Porto Seguro (R$ 6.792) for absorvido → CDB economiza R$ 6.792
- Meta: usar o máximo de crédito de negociação possível, preservando CDB para emergências

## ⚠️ Pitfall: absorvido ≠ quitado

Cartões "absorvidos" pelo Inter (Méliuz 2048, C&A Pay, etc.) tiveram a fatura de **agosto** paga, mas o cartão **continua ativo** e pode ter **parcelamentos futuros**. Cada mês gera nova fatura.

| Cartão | Agosto | Setembro+ |
|---|---|---|
| Méliuz 2048 | ✅ Pago (Inter) | ⬜ Parcelamentos? |
| C&A Pay | ✅ Pago (Inter) | ⬜ Parcelamentos? |

> **Regra:** sempre perguntar se o cartão absorvido tem parcelamentos. Se tiver, manter a ficha individual ativa e rastrear mês a mês. Só marcar como "quitado/arquivado" se confirmado que não há parcelamentos futuros (ex: PicPay, que foi absorvido pelo PAN e não tem parcelamentos).
