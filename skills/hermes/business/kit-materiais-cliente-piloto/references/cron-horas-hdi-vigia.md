# Vigia de horas [EMPRESA] + pitfall de cron (05/09/2026)

## O vigia
Job cron `85e92800ae50` — "📋 [EMPRESA]/[EMPRESA] — Conferir horas lançadas (semanal)", sexta 17h (`0 17 * * 5`).
- Lê a planilha do mês corrente em `~/MEGA/Documentos/trabalho_projetos_ti/timesheets/` (padrão `Controle horas [EMPRESA] - <MÊS> <ANO> - igor dos santos ferreira.xlsx`).
- Confere seg–sex da semana corrente: 8h/dia útil, feriados SP não recebem horas.
- Reporta no Telegram: dias OK ✅, faltando ⚠️ (dia da semana + data). NUNCA edita a planilha (só leitura).
- Planilha inexistente → apontar gerador `gerar_timesheet_noorden_2026.py`.
- Complementado pelo job `f64d25d2f9ed` (dia 27, 9h: envio da planilha à [EMPRESA]).

## PITFALL — drift_skip em cron job (causou erro silencioso)
Cron job **sem model pin** quando o modelo global do Hermes muda (deepseek→glm etc.) entra em `drift_skip`: pula a execução para "evitar spend não intencional" e grava `last_status: error` **sem rodar nada**. Sintoma: lembretes param de chegar sem nenhum log claro.

Fix (por job):
```bash
hermes cron edit <job_id> --provider openrouter --model z-ai/glm-5.3-flash
```
Depois: conferir campo `model` no jobs.json e rodar `hermes cron run <job_id>` uma vez para testar de verdade (exit code + last_status=succeeded).

Auditar periodicamente todos os jobs: jobs criados antes de uma troca de modelo global são candidatos a drift_skip.