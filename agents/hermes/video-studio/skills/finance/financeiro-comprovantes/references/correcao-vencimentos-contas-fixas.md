# Correção de Vencimentos — Contas Fixas

Quando um alerta de vencimento (cron job ou agenda) mostrar uma data que o usuário contesta, corrigir com evidência documental, não com estimativa.

## Fluxo

1. **Aceitar a contestação do usuário** — ele sabe quando paga as contas
2. **Buscar evidência nas faturas reais** dos últimos 3 meses:
   ```
   search_files em 2026/{meses anteriores}/ por "Conta.*venc|vencimento.*Conta"
   ```
3. **Extrair a data real** de vencimento da fatura mais recente
4. **Atualizar TODOS os arquivos afetados**:
   - `YYYY_MM_MES/AGENDA.md` (agenda mensal)
   - `_Controle_Anual/AGENDA-VENCIMENTOS-2026.md` (agenda anual)
   - Qualquer outro arquivo que referencie a data errada
5. **Marcar como pago** se o usuário confirmar

## Exemplo real (09/08/2026)

| Conta | Venc. errado (cadastrado) | Venc. real (fatura) | Evidência |
|---|---|---|---|
| Light | ~10/08 | **24/08** | 24/07, 24/04, 24/03 |
| Claro | ~20 | **15** | 15/07, 15/04 |
| Naturgy | ~15 | **20** | 20/07, 20/06, 20/05, 20/03, 20/01 |
| Condomínio | ~05 | **10** | 10/07, 10/06 |
| Vivo | ~20 | **10** | Fatura real 10/08/2026 R$102,23 |

O erro original veio de comprovantes PIX/RecargaPay que não informavam vencimento — a data de pagamento foi confundida com vencimento.

## Pitfalls

⚠️ **Comprovante de PIX NÃO informa vencimento.** Se a única fonte for um comprovante RecargaPay/PIX, o vencimento real está na fatura original (PDF da conta). Sempre preferir a fatura ao comprovante. O erro clássico: pagou dia 20 via PIX → cadastrou vencimento como dia 20. A fatura real pode mostrar vencimento dia 10.

⚠️ **Meses anteriores podem ter pistas erradas.** Se todos os comprovantes anteriores são PIX/RecargaPay sem vencimento visível, a data de vencimento cadastrada é a data de PAGAMENTO, não de VENCIMENTO. Exemplo real: Vivo aparecia como vencimento "~dia 20" em todos os controles porque os pagamentos eram feitos dia 20 via PIX. A fatura real de agosto mostrou vencimento **dia 10** e pagamento configurado como **cartão de crédito**. Sempre pedir a fatura original quando houver dúvida.

⚠️ **Forma de pagamento pode mudar.** Uma conta paga por PIX em meses anteriores pode estar configurada como débito automático ou cartão de crédito no ciclo atual. A fatura real é a única fonte confiável tanto para vencimento quanto para forma de pagamento.
