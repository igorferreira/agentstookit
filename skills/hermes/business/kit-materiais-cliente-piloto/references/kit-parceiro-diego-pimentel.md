# Kit Parceiro — Diego Pimentel (validado 04-05/09/2026)

Caso de referência para produzir kit do TimeAutomático para um **PARCEIRO** (indicador de contatos), que difere do kit de cliente-piloto final.

## Perfil traçado (pesquisa web)
- Alvo: Diego Rodrigues Pimentel, RJ, gerente comercial/expansão (saúde auditiva — Reabilita, Menthel), sócio de Drogaria Cariocão (RJ) e CLUB Conceito (Recife).
- **Pitfall homônimos:** "Diego Pimentel" retorna 5+ perfis LinkedIn (Marília/SP, Campinas/SP, MS, 2 no RJ). Confirmar cidade/área com o Usuário ANTES de pesquisar; apresentar os candidatos e deixar ele escolher.
- Fontes: LinkedIn público + registros societários (EFIRMA) — suficiente para perfil sem invasão.

## Diferenças vs kit de cliente-piloto
1. Deck tem slide DEDICADO ao modelo de parceria (indicador recebe material pronto, execução fica por conta do Usuário, reciprocidade caso a caso).
2. Tom: respeitoso, confiável, orientado a processo — NADA de hype/malandragem (perfil religioso do público-alvo).
3. Sem preços na primeira abordagem.
4. Mensagens WhatsApp: 2 mensagens + ordem de envio explícita (msg1 → áudio1 → PDF → áudios 2-3 → msg2 → áudio4).

## Artefatos produzidos (em 05-execucao-clientes/ do repo hermes-as-service)
- `DIEGO-PIMENTEL-PARCEIRO.md` — perfil (fatos de fontes públicas separados de hipóteses)
- `20260904_TIMEAUTOMATICO-PARCEIRO-DIEGO-PIMENTEL.{pptx,pdf}` — deck 9 slides
- `audios/20260904_DIEGO-PIMENTEL_0{1..4}-*.ogg` — 4 áudios piper
- `20260904_DIEGO-PIMENTEL-MENSAGENS-WHATSAPP.md`

## Pipeline executado (funcionou)
1. web_search 2 queries (nome+comercial+LinkedIn; nome+sócios) → distinguir homônimos.
2. Escrever perfil em `05-execucao-clientes/` (commit + rsync Drive: pasta correta é `03_Dev_IA/ia_agentes/hermes-as-service/`).
3. Deck delegado via `delegate_task` (goal único; leaf roda em ~50s) — exigir no prompt: verificação pdfinfo ANTES de responder.
4. Áudios via tool `text_to_speech` DIRETA (não importável dentro de execute_code) — 4 roteiros, output .ogg.
5. Auditoria visual: pdftoppm → montage 3x3 → vision_analyze pedindo cortes/sobreposições/espanhol.
6. Commit GitHub + rsync Drive + confirmar.

## Lição de agendamento (cron pós-kit)
Nada específico do kit, mas cron jobs criados na mesma sessão precisam de model pin — ver `cron-horas-hdi-vigia.md`.