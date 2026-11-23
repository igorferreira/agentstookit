---
name: faturas-email-cartoes
description: "Use when Igor asks to fetch card bills from his Gmail."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [financeiro, faturas, email, gmail, comprovantes, cartoes]
---

# Faturas de cartão no e-mail — varredura e arquivamento

## Overview

Classe de tarefa: o Igor pede "busca no meu email as faturas de cartões e baixa para o lugar padrão no MEGA/Comprovantes" para uma janela de meses. Este skill cobre a coleta: detecção nos e-mails, download, descriptografia, dedupe e salvamento no padrão MEGA. O ciclo posterior (fluxo de caixa, fichas, cascata) segue o skill `financeiro-comprovantes` — até que ele seja adotado pelo curador, este skill é a fonte do passo de varredura, que ele ainda não documenta.

Conta IMAP himalaya: `gmail-igor` (igorferreirabr@gmail.com).

## Regras sempre-vivas

- **Inventário local ANTES de baixar:** tudo que já existe em `~/MEGA/Comprovantes/AAAA/YYYY_MM_MES/` (grep `FATURA`) não baixa de novo.
- **Nunca imprimir ou persistir credenciais:** obtenha CPF/CEP/senha apenas em memória via keyring quando indispensável; nunca coloque os valores em logs, Markdown, nomes de arquivo ou mensagens. Use `secret-tool lookup service hermes-identity account igor-cpf` (e `igor-cep`) em variável de shell; `secret-tool search` vaza o segredo na saída — nunca rode sem filtro.
- **Fatura em pasta do mês do VENCIMENTO**, não do e-mail (e-mail de 29/09 com venc 06/10 → pasta Outubro).
- Sempre gravar o PDF protegido original E a cópia `-SEM-SENHA.pdf` descriptografada.
- Fatura fechada oficial substitui captura em aberto anterior; registrar o delta e, se >20%, linha em `AVISOS.md`.
- Não classificar valor idêntico mês a mês como duplicata sem conferir "Parcelas futuras" da competência anterior (parcela fixa chega com o mesmo valor todo mês).
- Metadados mínimos no `.md` (tabela): cartão+final, emissor, competência, vencimento, valor, data do e-mail, pasta Gmail de origem, status, nomes dos arquivos e evidência de validação. Nunca registre a senha do PDF, CPF ou CEP; se necessário, anote apenas a regra/fonte de abertura, sem o valor secreto.

## Procedimento

1. **Inventarie e deduplique antes de baixar:** examine `~/MEGA/Comprovantes/AAAA/YYYY_MM_MES/` por `FATURA`, final, competência e valor. O anexo mais recente/fechado substitui uma captura aberta anterior; preserve o histórico, mas não conte duas vezes.
2. **Varra o All Mail, não apenas a INBOX:** o Gmail já pode ter arquivado as mensagens nos labels Financeiro. Se `himalaya envelope list --output json` vier vazio ou inválido, conecte ao IMAP usando o keyring, selecione `"[Gmail]/Todos os e-mails"`, pesquise apenas `SINCE <data>` e filtre remetente/assunto no cliente. Não use uma consulta Gmail complexa com chaves/parenteses sem validar: o servidor pode responder `Could not parse command`.
3. **Colete em lote:** busque cabeçalhos primeiro; depois faça uma única leitura MIME por candidato e extraia anexos, corpo, data, emissor, final, valor e vencimento. Use o corpo como fonte quando o PDF não tiver texto ou quando o e-mail trouxer o valor de um PIX copia-e-cola.
4. **Classifique o estado financeiro antes de registrar:** `✅ Pago` exige comprovante liquidado ou e-mail oficial de pagamento realizado; `🟡 A vencer` é fatura fechada sem quitação; `🔴 Negociação` não deve ser marcada como a pagar normal; débito automático apenas agendado não é quitação. Separe três fatos: o pagamento ocorreu, qual fatura foi quitada e qual foi a fonte/método de financiamento. Uma confirmação oficial pode provar o pagamento sem identificar o destino ou a origem. Associe-o a uma fatura somente quando identificadores independentes (emissor/beneficiário, final do cartão, competência/vencimento e valor) apontarem unicamente para ela e não houver informação explícita conflitante; valor exato isolado não resolve conflito. Se a transação estiver confirmada, mas o destino estiver em conflito, registre a transação e mantenha as faturas candidatas em `Revisão` até esclarecimento — não dê baixa em uma fatura específica. Se a origem não estiver documentada, registre `não identificada` e não classifique o movimento no fluxo como saída de caixa ou pagamento cruzado até comprovar o método/fonte.
5. **Baixe os anexos e preserve as duas versões:** salve o PDF protegido original e gere `-SEM-SENHA.pdf` validando `pdfinfo` (`Encrypted: no`). Para extração, use `pdftotext -upw` (senha de USUÁRIO — a flag `-opw` responde `Incorrect password` mesmo com a senha correta); para regravar sem senha, use `pdftocairo -upw ... -pdf` ou outra ferramenta que produza um PDF válido. Nunca entregue uma saída vazia/corrompida só porque o comando terminou sem erro.
6. **Nomeie e documente no padrão:** `AAAA-MM-DD_FATURA-CARTAO-<NOME>-<FINAL>-<MES>-R<centavos>.pdf`, o correspondente `.md` e, quando aplicável, `-SEM-SENHA.pdf`. A data é a do e-mail/recebimento; a pasta é a do vencimento. O `.md` deve conter UID/origem, emissor, final, competência, vencimento, valor, status, arquivos e evidência de pagamento.
7. **Atualize todas as fontes relacionadas:** ficha do cartão, `INDEX.md`, `CONTROLE_PAGAMENTOS.md` e o delta do fluxo de caixa. Ao descobrir uma fatura fechada que substitui uma aberta, atualize o valor vigente e registre o delta; recalcule os subtotais com aritmética externa antes de gravá-los.
8. **Verifique a entrega:** confirme existência/tamanho dos arquivos, `pdfinfo` sem criptografia nas cópias abertas, links relativos válidos e que o total pago + a vencer + negociação reconcilia com os itens listados. Nunca declare a caixa/controle concluído com subtotais antigos visíveis sem uma seção de atualização explícita.
9. Seguir o ciclo do fluxo de caixa/fichas conforme `financeiro-comprovantes`.

## Pitfalls

- ⚠️ **`after` + `before` combinados retornam 0 no himalaya** (bug dos filtros de data). Use só `after` e filtre datas no cliente, ou use IMAP `SINCE`.
- ⚠️ **Não confie em JSON vazio do Himalaya:** uma pasta arquivada ou uma saída sem newline pode parecer sem mensagens. Confirme a pasta especial `[Gmail]/Todos os e-mails` via IMAP e faça o fallback MIME antes de concluir que não há faturas.
- ⚠️ **Não conte o anexo pelo nome do arquivo:** emissores reutilizam `Fatura.pdf` e enviam várias versões. Use UID + data + emissor + final + valor para a chave de deduplicação.
- ⚠️ **Se o anexo tiver CAMINHO absoluto como filename** (o remailer do BradesCard embute o caminho de origem em `filename="/home/.../FATURA MENSAL.pdf"`), o `himalaya attachment download` tenta salvar nesse caminho e falha com `No such file or directory` — não crie a árvore de pastas; exporte a mensagem (`himalaya message export <ID> --full > msg.eml`) e extraia a parte `application/*` com o módulo `email` do Python (validando magic bytes `%PDF-`).
- ⚠️ **A fatura do mês costuma estar na INBOX, não no label do cartão:** os labels `Financeiro/Cartoes/*` podem estar defasados (última fatura arquivada lá é de meses atrás). Varra as páginas recentes da INBOX filtrando assunto `fatura|venc|fechou` antes de concluir que a fatura não chegou.
- ⚠️ **Não reconstrua lançamentos linha a linha a partir de pdftotext de fatura em 2+ colunas** — a extração embaralha valores e datas e a soma nunca fecha. Registre na ficha só os campos unívocos (total, vencimento, fechamento, limites, parcelas futuras, resumo de crédito) e anexe o `.txt` extraído como evidência; o detalhe linha a linha fica pendente de conferência visual.
- ⚠️ Flags (`--page-size`, `--folder`, `--output`) sempre **ANTES** dos filtros posicionais no himalaya.
- ⚠️ O lookup do keyring pode vir formatado (pontuação) — remova não dígitos antes de fatiar; fatiar o formato pontuado gera senha errada silenciosamente.
- ⚠️ **Valide a cópia sem senha:** `pdftotext` pode extrair texto com a senha, mas uma conversão que falha pode deixar um PDF vazio. Rode `pdfinfo` e exija `Encrypted: no` antes de registrar o arquivo como entregue.
- ⚠️ **Leia o corpo para a senha do emissor antes de tentar variantes:** Porto, por exemplo, informa no próprio e-mail a composição CPF4+CEP5. Se o PDF continuar fechado, preserve o original protegido e registre claramente a pendência; não invente senha nem marque a cópia aberta como concluída.
- ⚠️ `pypdf` às vezes aceita a senha mas lança `FileNotDecryptedError` ao paginar — use `pdftocairo -upw` ou pikepdf como alternativa validada.
- ⚠️ O CEP pode não estar no keyring — derive do endereço atual e confirme qualquer mudança de endereço antes de usá-lo.

## Referências

- [references/senhas-pdf-emissores.md](references/senhas-pdf-emissores.md) — tabela de senha por emissor + extração de valor do PIX EMV (tag 54) para faturas sem PDF.
