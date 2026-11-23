# Controle de Faturas — Cartões Mantidos

Sistema de rastreamento mensal das faturas dos cartões ativos (que continuam gerando gastos).

## Arquivos

| Arquivo | Finalidade |
|---|---|
| `~/MEGA/Comprovantes/CONTROLE_FATURAS_MANTIDOS.md` | Visão mensal agregada de todos os cartões ativos |
| `~/MEGA/Comprovantes/FICHA_CARTAO_<NOME>_<FINAL>.md` | Ficha individual por cartão com histórico mês a mês |

## Cartões ativos (6)

Nubank 3033, Passaí 6698, Signature 6651, Luiza 9105, Amazon 3018, Carrefour 3825.
Porto Seguro 8121 monitorado separadamente (bloqueado).

## Estrutura da ficha individual

```markdown
# 🛒 Ficha — <Nome> <Final>
> **Emissor:** <banco> | **Status:** Ativo/Bloqueado

## 📅 Histórico mensal
| Mês | Valor fatura | Limite disp. | Fecha | Vence | Status |

## 📈 Tendência
(comparação mês anterior vs atual)

## 📦 Parcelamentos futuros
| Mês | Valor | Parcela |

## Observações
```

## Fluxo de atualização

Quando o usuário enviar print de fatura parcial:
1. Atualizar a ficha individual do cartão (nova linha no histórico mensal)
2. Atualizar a linha correspondente no `CONTROLE_FATURAS_MANTIDOS.md` (seção do mês)
3. Se o valor subiu em relação ao mês anterior, marcar tendência (📈/📉)
4. Se o limite disponível caiu muito (>50%), alertar sobre risco de estouro
5. Registrar a data da captura (fatura pode crescer até fechar)
