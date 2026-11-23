---
name: whatsapp-export-analysis
description: Analisa export zip de conversa do WhatsApp do Igor.
version: 1.0
---

# Análise de Export de Conversa WhatsApp

## Fluxo validado
1. Igor manda o .zip como ARQUIVO no Telegram (nunca importar como chat). Path chega em ~/.hermes/cache/documents/
2. Descompactar em /tmp/conv_<tag>/ — contém `Conversa do WhatsApp com <X>.txt` (+ .vcf, + mídias se export "com mídia")
3. Parsear em Python: regex `^(\d{2}/\d{2}/\d{4}) (\d{2}:\d{2}) - (autor): (msg)$`
   - **ANTES: limpar bidi/invisíveis** — `re.sub(r'[\u200e\u200f\u202a-\u202e\u2066-\u2069]', '', txt)` (o WhatsApp injeta U+200E que quebra o regex e o grep)
4. Estatísticas core: total/autor, % volume, chars (não só nº de msgs), quem abre o dia, quem quebra silêncio >2h, tempo de resposta por BLOCO (rajada = 1 bloco, janela ≤5min) — média E mediana, P25/50/75/90, perguntas ("?"), emojis afetivos, mensagens apagadas por autor, picos por hora
5. Entregar: números + leitura separando FATOS de HIPÓTESES + salvar relatório .md na pasta do caso

## ⚠️ PITFALL Nº1 — ATRIBUIÇÃO DE AUTORIA (Igor corrigiu 2× na mesma sessão)
- NUNCA atribuir citação de mensagem sem grepar a linha EXATA no export (`grep -n "trecho" arquivo.txt`). Lembretes de conversa / rascunhos ditados pelo Igor NÃO são mensagens no export.
- Duas falhas clássicas: (a) confundir quem disse um elogio ("vc é muito forte" era do Igor, não da outra pessoa); (b) tratar rascunho que o Igor "está pensando em mandar" como se já tivesse sido enviado por ela.
- Se o export não cobre o período que o Igor menciona (ex: msgs de hoje após a hora do arquivo), DIZER que não há dado — nunca inferir o que rolou.

## ⚠️ PITFALL Nº2 — EXPORTS DUPLICADOS
Igor frequentemente reenvia o mesmo zip (testar md5sum antes de reanalisar). Delta = msgs com timestamp > última análise.

## Regras do domínio (contexto Igor)
- Contato da parceira salvo como "A" ou "Adrielly" — mapear A→Adrielly sem alterar o arquivo original
- Análise de relacionamento é do Rafael (perfil relationship-senior): separar fatos vs hipóteses, não julgar, recomendação prática
- Salvar em ~/MEGA/Documentos/relacionamentos/<caso>/ + atualizar DIARIO quando existir
- Se export vier "com mídia": áudios .ogg podem ser transcritos (faster-whisper) — oferecer
- Igor valoriza números objetivos para desarmar ansiedade (ex: P90 de resposta dela ~44min vs percepção de "demora sempre" — dados matam fantasia melhor que conselho)
