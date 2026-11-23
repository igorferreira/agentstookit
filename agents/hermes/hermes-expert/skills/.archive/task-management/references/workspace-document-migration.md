# Migração segura de documentos do workspace

Use este procedimento quando documentos pessoais produzidos em `~/clawd/` precisarem ser organizados no MEGA sem tocar no runtime de Hermes/OpenClaw.

## Auditoria prévia

1. Inventarie arquivos individualmente; não classifique o diretório inteiro como pessoal.
2. Proteja explicitamente identidade, memória, tarefas operacionais, skills, planos e repositório: arquivos Markdown de agente, `memory/`, `.hermes/`, `.git/` e `canvas/`.
3. Para cada candidato, confira:
   - tipo real/magic bytes (extensão pode mentir);
   - assunto e finalidade;
   - presença de chaves, tokens, senhas, `.env`, providers, gateway ou configuração;
   - duplicata ou documento canônico já existente no MEGA;
   - referências recebidas de outros documentos.
4. Itens ambíguos ficam no lugar. Não apagar temporários automaticamente.

## Roteamento por classe

- Relações pessoais → `MEGA/Documentos/relacionamentos/<pessoa>/`
- Carreira/estudos/LinkedIn/conversas → subpastas em `MEGA/Documentos/carreira/`
- Finanças e análises jurídicas → `MEGA/Documentos/financas_bancos/`
- Compras/pesquisas pessoais → `MEGA/Documentos/lazer_interesses/compras/`
- Comprovantes, notas e regulamentos de cartões → `MEGA/Comprovantes/`
- Registro diário de produção → `MEGA/Documentos/diario/`

Use nomes datados e descritivos. Se um arquivo mistura dois domínios, divida em documentos independentes e preserve o original integral em `MEGA/Documentos/registros_manutencao/originais_clawd/`.

## Execução e referências

1. Crie somente as pastas pessoais necessárias.
2. Mova os candidatos aprovados.
3. Atualize links relativos no `TAREFAS.md` e em fichas/documentos associados.
4. Não edite `PEDIDOS.md`, memória, identidade ou configuração para registrar a migração.

## Verificação obrigatória

- Todos os destinos existem, têm tamanho maior que zero e tipo esperado.
- As fontes antigas aprovadas para migração não existem mais.
- Links atualizados resolvem para arquivos existentes.
- Não restaram referências aos nomes antigos.
- Arquivos protegidos estão idênticos; em escopo sensível, gere hashes antes e valide depois.
- Considere locale: `sha256sum -c` pode imprimir `SUCESSO` em vez de `OK`; use o código de saída ou aceite ambos ao contar.

## Pitfalls observados

- Um `.pdf` pode ser apenas HTML de “Access Denied”; valide com `file` ou magic bytes.
- Uma imagem aparentemente redundante pode ser evidência complementar; se o usuário não autorizou descarte, preserve-a junto ao documento canônico e registre o link.
- Não confundir menções textuais a Hermes/OpenClaw num diário pessoal com configuração operacional; a classificação depende da função do arquivo, não apenas de palavras-chave.
- Um patch multiarquivo atômico pode falhar inteiro por um único hunk. Prefira substituições pequenas e independentes para referências/documentação.
