---
name: whatsapp-export-analysis
description: Analisa export zip de conversa do WhatsApp do Igor.
version: 1.0
---

# Análise de Export de Conversa WhatsApp

## Fluxo validado
1. Igor manda o .zip como ARQUIVO no Telegram (nunca importar como chat). Path chega em ~/.hermes/cache/documents/
2. Antes de extrair, aplique o gate de SHA-256 do Pitfall Nº2; mantenha cada ZIP distinto em diretório de trabalho próprio e preserve os originais. O TXT inclui mensagens e, se exportado "com mídia", .vcf e arquivos de mídia.
3. Parsear em Python: regex `^(\d{2}/\d{2}/\d{4}) (\d{2}:\d{2}) - (autor): (msg)$`
   - **ANTES: limpar bidi/invisíveis** — `re.sub(r'[\u200e\u200f\u202a-\u202e\u2066-\u2069]', '', txt)` (o WhatsApp injeta U+200E que quebra o regex e o grep)
4. Estatísticas core: total/autor, % volume, chars (não só nº de msgs), quem abre o dia, quem quebra silêncio >2h, tempo de resposta por BLOCO (rajada = 1 bloco, janela ≤5min) — média E mediana, P25/50/75/90, perguntas ("?"), emojis afetivos, mensagens apagadas por autor, picos por hora. Declare denominadores, tamanho da amostra e exclusões; essas métricas descrevem somente a interação visível e não medem afeto, intenção, compromisso ou consentimento.
5. Para uma segunda análise independente, examine primeiro os exports originais, reconstrua a cronologia e formule a leitura preliminar antes de consultar o relatório anterior; só depois compare convergências e divergências, citando evidência. Isso reduz ancoragem.
6. Entregar: números + leitura separando FATOS de HIPÓTESES + limites do material + salvar relatório .md na pasta canônica do caso. Nomeie com clareza o perfil/agente que realmente executou; um fallback isolado não pode ser apresentado como trabalho do perfil solicitado.

## Verificação de autoria e cobertura
- Localize cada citação no TXT do export e confirme remetente e timestamp antes de atribuí-la.
- Separe mensagens exportadas, rascunhos não enviados e relatos sobre eventos externos.
- Se o export não cobrir o período, declare a lacuna; não complete a cronologia por inferência.

## ⚠️ PITFALL Nº2 — EXPORTS DUPLICADOS OU COM MESMO NOME
Antes de extrair, compare SHA-256 do ZIP recebido com exports anteriores relevantes (`sha256sum novo.zip anterior.zip`). Nome igual ou tamanho parecido não prova duplicidade. Hash igual significa arquivo idêntico: não reanalise, confira se já está associado à tarefa. Hash diferente significa export distinto, mesmo se o nome coincidir: preserve o original, extraia em diretório separado e alinhe o trecho sobreposto por ordem, autor e corpo; compare horários separadamente para identificar mudanças só de timestamp e enumere os registros adicionais. Não presuma que o arquivo diferente contém apenas um delta. Se os arquivos pertencem ao mesmo pedido, mantenha-os associados à mesma tarefa e análise, sem criar uma tarefa duplicada.

## PITFALL Nº3 — LACUNAS DE COBERTURA
Export pedido de dia cobre só até a hora da exportação — presencial/madrugada recente NÃO está no arquivo. Se o Igor relatar fatos de período posterior ao último timestamp do export, registrar como relato verbal (com hora que ele informar) no diário do caso e dizer que o export não cobre — nunca "inventar" mensagens para completar a lacuna nem tratar relato verbal como linha do export.

## PITFALL Nº4 — IDENTIDADE AMBÍGUA EM ÁUDIO
- Transcrições podem omitir nomes ou conter referências ambíguas. Não associe uma pessoa a alguém conhecido apenas pelo contexto; confirme a identidade com Igor quando ela mudar a análise.
- Ao receber uma correção, propague-a por todas as menções e conclusões afetadas e registre a origem da confirmação.
- Em pronomes ou referências ambíguas, explicite quem é o referente somente quando houver confirmação; caso contrário, marque a incerteza.

## Regras do domínio (contexto Igor)
- Contato da parceira salvo como "A" ou "Adrielly" — mapear A→Adrielly sem alterar o arquivo original
- Análise de relacionamento é do Rafael (perfil relationship-senior): separar fatos vs hipóteses, não julgar, recomendação prática
- Salvar em ~/MEGA/Documentos/relacionamentos/<caso>/ + atualizar DIARIO quando existir
- Se export vier "com mídia": áudios .ogg/.opus podem ser transcritos (faster-whisper/whisperx) — oferecer. Salvar UM .txt por áudio em /tmp/transcripts/ com o MESMO nome-base do arquivo original (ex: PTT-20261004-WA0207.opus → PTT-20261004-WA0207.txt), para cruzar com as linhas do export por nome de arquivo.
