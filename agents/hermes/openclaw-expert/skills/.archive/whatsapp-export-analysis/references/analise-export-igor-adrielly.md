# Análise de export WhatsApp Igor↔Adrielly — workflow validado (set/2026)

## Convenções de remetente
- Contato da Adrielly salvo como **"A"** na agenda do Igor (não ver nome completo). Em exports, `A` = Adrielly, `igor ferreira` = Igor. Mapear A→Adrielly nas análises SEM alterar o arquivo original.
- Exports vêm com ou sem mídia; quando com imagens, analisar conteúdo visual também.

## Workflow de análise (validado 07-08/09/2026)
1. Receber .zip como ARQUIVO no Telegram (não importar como chat). Salvar em `/tmp/conv_<id>/` e `unzip -o`.
2. **Dedup por md5sum** — Igor costuma reenviar o mesmo export várias vezes; comparar hash antes de reanalisar.
3. Limpar caracteres bidi invisíveis (`\u200e\u200f\u202a-\u202e\u2066-\u2069`) antes de parsear.
4. Parsear linhas `DD/MM/YYYY, HH:MM - remetente: msg` (regex); mensagens multilinha pertencem ao remetente anterior.
5. Estatísticas que o Igor considera padrão: contagem por remetente, % volume, tempo de resposta (mediana + P75/P90, ignorando gaps >24h), quem quebra silêncios >2h, perguntas, emojis afetivos, mensagens apagadas, distribuição por hora/dia.
6. **Verificar atribuição de frases-chave com grep antes de citar** — Igor pegou erro de atribuição 2x ("vc é muito forte" era dele, não dela). Confirmar autor de citações literais sempre.
7. Salvar análise em `~/MEGA/Documentos/relacionamentos/adrielly/` (`2026-09-07_ANALISE-EXPORT-WHATSAPP-IGOR-A.md`, `RAFAEL-ANALISE-EXPORT-FINAL.md`) e atualizar `DIARIO-RELACIONAMENTO-ADRIELLY.md`.

## Cuidados de interpretação (lições do Igor)
- NÃO inventar eventos: se o export termina às 02:14, mensagens de meio-dia do mesmo dia não estão lá — o export novo precisa ser solicitado/recebido.
- Números são espelho para Igor, nunca argumento contra a Adrielly ("mando mais").
- Mensagens apagadas = sofrimento filtrado, não prova de culpa.
- Padrão confirmado nos dados: assimetria perseguidor-distanciador (Igor 62% volume, quebra silêncio 9×2, perguntas 51×20) — citar como fato medido, não julgamento.
