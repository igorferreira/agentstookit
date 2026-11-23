# Análise de export WhatsApp — procedimento específico do caso Igor↔Adrielly

## Convenções de remetente
- Contato da Adrielly salvo como **"A"** na agenda do Igor (não ver nome completo). Em exports, `A` = Adrielly, `igor ferreira` = Igor. Mapear A→Adrielly nas análises SEM alterar o arquivo original.
- Exports vêm com ou sem mídia; quando com imagens, analisar conteúdo visual também.

## Workflow de análise
1. Receba o ZIP como arquivo, preserve o original e extraia cada export em diretório próprio; compare SHA-256 antes de tratar versões com nomes iguais ou trechos sobrepostos.
2. Limpe caracteres bidi invisíveis (`\u200e\u200f\u202a-\u202e\u2066-\u2069`) antes de parsear.
3. Parseie linhas `DD/MM/YYYY, HH:MM - remetente: msg`; associe linhas multilinha à mensagem anterior e normalize o identificador `A` para Adrielly sem alterar a fonte.
4. Calcule contagens por remetente, proporção, latências por bloco, aberturas e pausas, perguntas, emojis, mensagens apagadas e distribuição temporal. Declare a unidade, denominador, janela e exclusões; use o mesmo critério nos dois lados.
5. Pesquise no export cada citação literal e confirme autor e horário. Não atribua texto colado no chat ao export sem localizar a linha original.
6. Salve o relatório na subpasta canônica do caso e atualize o diário correspondente; use nome de arquivo descritivo sem incorporar datas de incidentes ao conteúdo da skill.

## Cuidados de interpretação
- Não invente eventos: se o último timestamp disponível for anterior ao período citado, declare que o export não contém essas mensagens e solicite uma fonte atualizada se necessário.
- Apresente métricas como descrição da amostra, não como argumento para invalidar a percepção de qualquer pessoa.
- Mensagens apagadas comprovam apenas que o export registra uma exclusão; não revelam motivo, conteúdo ou estado emocional.
- Não classifique uma dinâmica como perseguição, afastamento ou abuso a partir de volume, latência ou perguntas; formule hipótese comportamental, mostre evidências a favor e contra e considere alternativas.
