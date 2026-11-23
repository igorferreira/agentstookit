# Varredura Completa do Plano Financeiro

## Quando usar

Quando o usuário disser "atualiza todo o nosso plano", "atualiza o planejamento", ou após uma sessão com múltiplos pagamentos/mudanças de estado.

## Sequência de atualização (14+ arquivos)

Executar nesta ordem para evitar inconsistências:

### Fase 1: Saldos (sempre primeiro)
1. `_saldos/SALDO_ITAU.md`
2. `_saldos/SALDO_C6.md`
3. `_saldos/SALDO_99PAY.md`
4. `_saldos/SALDO_NUBANK.md` (se mudou)
5. `_saldos/INDEX.md`

### Fase 2: Controles mensais
6. `2026/2026_MM_MES/2026-MM_00_CONTROLE_PAGAMENTOS.md`
7. `2026/2026_MM_MES/2026-MM_00_DIVIDA.md`
8. `2026/2026_MM_MES/AGENDA.md`

### Fase 3: Arquivos canônicos da raiz
9. `ENDIVIDAMENTO.md`
10. `AVISOS.md`

### Fase 4: Índices
11. `_controles/CONTROLE_INDICE.md`
12. `2026/2026_MM_MES/INDEX.md`

### Fase 5: Fluxo de caixa (mais pesado, por último)
13. Recalcular JSON (X+1) e salvar em `_Analises/cenarios/`
14. Gerar MD + CSV + XLSX

## Pitfalls

- **Ordem importa**: se atualizar ENDIVIDAMENTO antes de CONTROLE_PAGAMENTOS, os totais podem divergir
- **Cartão quitado**: ao pagar um cartão que estava como "ativo", mover de Ativos → Quitados no CONTROLE_INDICE e ENDIVIDAMENTO
- **Parcelas futuras**: se o pagamento gerar parcelas (ex: acordo Paulo Guerra), adicionar ao fluxo como "Outros" e registrar em CONTROLE_PAGAMENTOS, DIVIDA e AGENDA
- **CDB**: SEMPRE verificar o saldo real do CDB antes de recalcular o fluxo. O CDB inicial do fluxo anterior pode estar defasado
