# Reconciliação de Pagamentos — Fluxo Completo

Quando o usuário pedir "atualiza tudo" ou "revisa o que foi pago", seguir esta ordem:

## Passo 1 — Levantamento de comprovantes

```bash
find ~/MEGA/Comprovantes/2026/ -name "*COMPROVANTE*" | sort
```

Incluir tanto a pasta do mês atual quanto meses adjacentes (pagamentos de fatura de Agosto processados em 31/07 ficam em Julho).

## Passo 2 — Cruzamento com controle

Para cada comprovante encontrado:
- Identificar cartão/obrigação correspondente no `CONTROLE_PAGAMENTOS.md`
- Marcar: ✅ Pago (com link do comprovante e fonte pagadora)
- Se não existir no controle: adicionar nova linha

## Passo 3 — Atualização do orçamento realizado

Atualizar `ORCAMENTO.md` do mês:
- Coluna "Realizado" ← valor pago
- Coluna "Δ" ← diferença vs planejado
- Coluna "Status" ← ✅ Pago / ⬜ Em aberto

## Passo 4 — Atualização do CDB

- Registrar cada saque do CDB no arquivo de tracking (`CDB-C6-*.md`)
- Calcular saldo atual: `aplicação_inicial − Σ(saques)`
- Comparar com o CDB projetado no fluxo de caixa
- Se divergência > R$ 100: investigar e, se necessário, recalcular o fluxo

## Passo 5 — Verificação do fluxo

- Confirmar que o CDB real bate com o CDB inicial do `FLUXO-CAIXA-2026-2030.md`
- Se bater: ✅ fluxo válido
- Se não bater: recalcular projeção a partir do CDB real

## Passo 6 — Resumo final

Apresentar:
- Cartões pagos (mantidos) com fonte
- Cartões absorvidos por Inter/Dígio (💀)
- Pendentes com valores
- CDB atual e projeção
- Dívida de negociação atualizada
