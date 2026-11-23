---
name: vigias-email
description: "Vigia por e-mail parou de captar ou vai criar um. IMAP/cron."
category: finance
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
tags: [email, vigia, cron, comprovantes, imapan]
---

# Vigias por e-mail (captação automática de comprovantes)

## Quando usar

Manutenção, depuração ou criação de vigias que leem comprovantes do Gmail via IMAP e escrevem em arquivo canônico Markdown (estacionamento, faturas por e-mail, comprovantes de banco, notas). Padrão do Igor: cron `no_agent=True` diário, stdout vazio = silêncio, stdout não vazio = mensagem no Telegram. Arquivos vigiados vivem em `~/MEGA/Documentos/financas_bancos/` ou `~/MEGA/Comprovantes/`.

## Regra de ouro: silêncio recente = suspeite de migração de remetente

Quando um arquivo canônico mantido por vigia parar de receber registros (ou o usuário notar um período faltando), **a causa mais provável é o remetente ter mudado**, não um bug do parser — empresas grandes emitem comprovantes de subdomínios de marketing/notificação distintos do remetente transacional antigo.

1. **Sondar antes de mexer** (read-only, sem tocar o state): via IMAP `X-GM-RAW`, contar os e-mails do remetente configurado POR ANO (`from:X`). Se o ano corrente sumir da contagem, procurar em TODOS os remetentes do domínio/marca e por termos de assunto, sem restrição de remetente (ex.: `'"palavra-chave" newer_than:930d'`).
   - **Atalho: exemplar do usuário vale mais que sondagem** — se o Igor encaminhar/colar um exemplo do e-mail novo ("olha esse email também"), extraia remetente + corpo INTEGRAL dele primeiro; isso substitui boa parte da varredura de domínio e já entrega a variante de layout para o parser.
2. **Extrair o corpo integral de um e-mail do formato novo** antes de escrever código: o layout HTML muda junto com o remetente, e o MESMO fornecedor pode ter 2-3 variantes de layout vigentes ao mesmo tempo (por ano, por campanha, por campo).
3. **Pegue o ano dos headers do e-mail, nunca do texto**: datas no corpo costumam vir sem ano (`Data: 28/09`) — derive o ano de `parsedate_to_datetime(msg["DATE"])`, com ajuste de virada de ano (mês 12 do corpo em e-mail de janeiro → ano-1; mês 1 em dezembro → ano+1).

## Parser resistente a migração

- **Cadastre TODOS os remetentes conhecidos em uma lista** e construa a consulta como `OR from:a OR from:b` — o vigia continua pegando o formato antigo enquanto o novo entra.
- **Parser unificado por âncoras de dados**: se achou o campo de valor do formato novo, siga os campos do novo; senão caia no antigo. Cada campo tolerante (`re.search(...) or re.search(...)`) cobre uma variante de layout conhecida.
- **Não confie em acentuação/emoji do corpo**: e-mails de marketing chegam com caracteres degradados (`Hor rio`, `Saida`). Regex deve tolerar `[ií]` e espaços perdidos.
- **Dedupe por tupla das colunas de dados** (nunca pela coluna de observação nem pelo ID IMAP: o mesmo evento pode chegar por 2 remetentes/e-mails).

## Backfill: reconstrua, não remende

Ao integrar um período que faltou, **re-parseie TODOS os e-mails (de todos os remetentes) e REESCREVA o arquivo canônico inteiro** a partir das linhas dedupeadas — não dê append nas linhas faltantes sobre a tabela existente. Linhas parcialmente parseadas (com `—`) ficam gravadas e viram basura de dedup; o rebuild idempotente elimina isso de uma vez.

- **Rebuild reusa o parser do vigia, nunca o duplica**: carregue o script do vigia no script one-shot de rebuild com `importlib.util.spec_from_file_location(...)` e chame as funções de parse dele. Reescrever as regex no rebuild gera uma segunda lógica que diverge — o rebuild conserta a tabela e quebra na próxima varredura do vigia.

Depois do rebuild:

- valide 0 duplicatas por chave completa;
- valide que resumo anual/mensal bate com a soma recalculada das linhas;
- liste as linhas que ainda têm campo ausente e volte ao corpo do e-mail original para decidir: variante de layout nova (adicionar ao parser) ou dado realmente ausente (deixar `—`).

## Estrutura do arquivo canônico (padrão)

Header com empresa/criado/última atualização (data E hora) + 3 tabelas: resumo anual, resumo mensal (com média por evento) e registros individuais. Ao mudar o formato do cabeçalho da tabela de registros, o vigia precisa ler as linhas existentes com regex do header, não string exata.

## Pitfalls

- **Não escreva no state antes de parsear com sucesso**: o state (IDs IMAP) só registra IDs efetivamente tentados — senão uma falha de parse come o e-mail para sempre.
- **`M.search` X-GM-RAW com OR múltiplo exige a query inteira entre aspas duplas**: construa em Python e teste com um termo simples antes.
- **`M.fetch` em lote perde a associação id→mensagem**: prefira fetch individual por ID no loop (desempenho é irrelevante para dezenas de e-mails).
- **`BODY.PEEK[]` para sondar** header/corpo sem marcar como lida; `RFC822` marca como lida.
- **Credencial via keyring**: `secret-tool lookup service hermes-gmail account <email>` com `DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus` — nunca imprimir a senha nem gravá-la em arquivo.
- **Truncamento de tabela no Obsidian**: quando datas/valores quebram de linha em células estreitas, habilitar snippet CSS com `white-space: nowrap` em `td`/`th` (`.obsidian/snippets/` + `enabledCssSnippets` no `appearance.json`) — o Obsidian quebra no espaço/hífen quando a coluna fica menor que o conteúdo.

## Light/Equel (fatura energia): PDFs protegidos por senha

As faturas da Light (equel.com.br) chegam como **PDFs protegidos por senha**, mesmo sem OCR ou texto selecionável. O padrão do himalaya é falhar com "Incorrect password" ao usar `pdftotext`. Tratamento especial necessário:

- **Caminho IMAP comum**: pasta `Financeiro/Contas/Luz` (pode variar — sempre verificar primeiro).
- **Download via himalaya**: `himalaya attachment download <envelope-id> -f 'Pasta' --downloads-dir /tmp/destino` (NUNCA `himalaya attachment fetch` — esse subcomando não existe).
- **Senhas típicas de PDF Light**: CPF do titular, número do contrato, número do medidor — tentar essas 3 variações antes de considerar outras abordagens.
- **Quando nenhuma senha funciona**: o PDF pode ser apenas uma imagem escaneada protegida — nesse caso, usar extração por OCR (`ocr-and-documents` skill) convertendo página → imagem → texto.
- **Armazenamento pós-extração**: salvar análise canônica em formato Markdown na estrutura `MEGA/Comprovantes/YYYY/YYYY_MM_MES/` seguindo template de fatura existente.
