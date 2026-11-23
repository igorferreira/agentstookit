---
name: financeiro-comprovantes
description: "Use when handling Usuário's financial receipts, boletos, invoices, card bills, payment proofs, monthly controls, and audits under ~/MEGA/Comprovantes."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [financeiro, comprovantes, faturas, boletos, auditoria, brasil]
    related_skills: [ocr-and-documents]
---

# Financeiro: Comprovantes

## Overview

Use esta skill para qualquer tarefa financeira envolvendo boletos, faturas, contas, comprovantes de pagamento, transferências, controles mensais e auditoria da pasta de comprovantes do Usuário.

Pasta base autorizada:

`/home/usuario/MEGA/Comprovantes`

Perfil recomendado:

`finance-senior`

## When to Use

Use quando o usuário enviar ou mencionar:

- boleto;
- fatura de cartão;
- conta de consumo;
- comprovante de PIX, boleto, cartão, TED, DOC ou transferência;
- necessidade de organizar arquivos financeiros;
- atualização de controle mensal;
- fechamento mensal;
- auditoria de comprovantes;
- pendências abertas ou comprovantes faltantes.

Não use para:

- alterar arquivos fora de `/home/usuario/MEGA/Comprovantes` sem autorização explícita;
- apagar documentos financeiros originais em caso de dúvida;
- inferir valores/datas sem evidência no arquivo, OCR ou contexto do usuário.

## Estrutura esperada

A estrutura principal usa ano e mês:

```text
/home/usuario/MEGA/Comprovantes/
└── 2026/
    ├── 2026_01_JANEIRO/
    ├── 2026_02_FEVEREIRO/
    ├── ...
    └── _Controle_Anual/
```

Dentro de cada mês, os arquivos principais tendem a seguir:

- `INDEX.md`
- `AAAA-MM_00_CONTROLE_PAGAMENTOS.md`
- `AAAA-MM_CONTAS_FATURAS.md`
- arquivos individuais `.md` por documento/transação;
- arquivos originais `.pdf`, `.jpg`, `.png`, etc.

## Padrão de nomes

Use nomes sem espaços quando criar novos arquivos.

Formato geral:

`AAAA-MM-DD_TIPO-ENTIDADE-DESCRICAO-RVALOR-SUFX.ext`

Exemplos:

- `2026-06-15_PIX_CONDOMINIO-PJBANK-R104177-COMPROVANTE-PAGAMENTO.pdf`
- `2026-06-02_FATURA-CARTAO-NUBANK.md`
- `2026-05-10_BOLETO-COND-FREGUESIA-COMPROVANTE-PAGAMENTO.pdf`

Convenções:

- valores em centavos no nome quando já houver padrão local, por exemplo `R104177` para R$ 1.041,77;
- sufixo `COMPROVANTE-PAGAMENTO` para pagamento confirmado;
- sufixo `COMPROVANTE-TRANSFERENCIA` para transferência;
- sufixo `FATURA`, `BOLETO`, `CONTA`, `DIVIDA` conforme o tipo.

## Metadados mínimos por arquivo `.md`

Todo documento financeiro deve tentar registrar:

- Data do documento;
- Data de pagamento, se houver;
- Tipo: fatura, boleto, conta, comprovante, transferência, dívida;
- Valor;
- Pagador;
- Recebedor/beneficiário;
- Banco/instituição, se aplicável;
- Status: Aberto, Pago, Pendente, Revisar;
- Arquivo original;
- Origem relacionada;
- Comprovante relacionado;
- IDs relevantes: linha digitável, código de barras, autenticação, NSU, ID transação, Pix end-to-end, protocolo.

Quando um dado não estiver disponível, use `Não identificado` ou `A confirmar`; não invente.

## Fluxo: boleto, conta ou fatura recebida

1. Identificar ano e mês de vencimento ou competência.
2. Salvar o arquivo original na pasta mensal correta.
3. Criar `.md` com o mesmo nome base do arquivo original.
4. Extrair texto/OCR quando possível.
5. Preencher metadados mínimos.
6. Atualizar `INDEX.md` do mês, se existir.
7. Atualizar `AAAA-MM_00_CONTROLE_PAGAMENTOS.md` como `Aberto` ou `Pendente`, com link em `Origem`.
8. Se já houver comprovante, relacionar `Comprovante` e marcar `Pago`.

## Fluxo: comprovante de pagamento recebido

1. Identificar data do pagamento e valor.
2. Salvar o original com sufixo `COMPROVANTE-PAGAMENTO` ou `COMPROVANTE-TRANSFERENCIA`.
3. Criar `.md` correspondente com OCR/texto e metadados.
4. Procurar origem relacionada no mês e meses próximos.
5. Atualizar controle mensal:
   - status `Pago`;
   - link `Comprovante`;
   - manter link `Origem` quando existir.
6. Se a origem não for encontrada, registrar como item a revisar.


## Procedimento padrão: conta/fatura + comprovante com OCR/Markdown

Quando o usuário enviar conta, fatura, boleto ou comprovante financeiro por imagem/PDF e pedir para salvar:

1. Salvar o arquivo original na **raiz da pasta mensal** correspondente, não em subpasta, salvo instrução explícita em contrário.
2. Usar o padrão local de nomenclatura com data, tipo, entidade, valor quando útil e sufixo adequado:
   - conta/fatura/boleto: `AAAA-MM-DD_CONTA-ENTIDADE...` ou `AAAA-MM-DD_FATURA-ENTIDADE...`;
   - comprovante pago: `AAAA-MM-DD_TIPO-ENTIDADE-RVALOR-COMPROVANTE-PAGAMENTO.ext`.
3. Sempre extrair texto do documento:
   - PDF pesquisável: usar extração de texto (`pdftotext` ou equivalente);
   - imagem/PDF escaneado: usar OCR local (`tesseract` ou equivalente) e inspeção visual quando necessário.
4. Sempre criar uma versão Markdown (`.md`) para cada documento financeiro relevante, contendo:
   - metadados principais: competência/referência, vencimento, data de pagamento, valor, pagador, recebedor, instituição, IDs, linha digitável/código de barras quando houver;
   - links relativos para o arquivo original;
   - seção `Texto extraído` ou `OCR / Texto extraído` com o conteúdo capturado;
   - observações de conferência quando algum dado vier do usuário ou estiver ambíguo.
5. Quando houver conta/fatura e comprovante do mesmo item, vincular os dois nos respectivos `.md`:
   - Markdown da conta/fatura aponta para o comprovante;
   - Markdown do comprovante aponta para a conta/fatura.
6. Atualizar o controle mensal `AAAA-MM_00_CONTROLE_PAGAMENTOS.md`:
   - status `Pago` quando houver comprovante;
   - valor e vencimento conferidos;
   - fonte pagadora quando identificada;
   - origem indicando `OCR`, `PDF`, `Telegram` ou combinação aplicável.
7. Se a origem já existir, substituir/atualizar pelo arquivo oficial recebido e regenerar o Markdown com base nele.
8. Não inventar dados ausentes: usar `Não identificado`, `A confirmar` ou registrar que a informação foi fornecida pelo usuário.
9. Antes de responder, verificar com `ls`, `grep`, extração/OCR ou leitura do Markdown que os arquivos foram criados/atualizados e que o controle mensal contém a linha correta.

## Card payment proofs: reconciliation checklist

When the user sends a card payment receipt, treat the receipt as the source of truth for the paid amount and update both ledgers when applicable. See [`references/card-payment-proof-workflow.md`](references/card-payment-proof-workflow.md).

1. Extract payment timestamp, amount, beneficiary, destination bank, due date, payer, origin bank/account, barcode, transaction IDs.
2. Save the original image/PDF in the month folder and create a matching `.md` file.
3. Use the receipt amount in the filename when practical (e.g. `R163885`).
4. Update both `AAAA-MM_00_CONTROLE_PAGAMENTOS.md` **and** `AAAA-MM_00_DIVIDA.md` only when each file actually tracks that obligation; distinguish payment audit rows from outstanding-debt rows.
5. If the control file and receipt differ, prefer the receipt for fields it visibly proves. Label card name/final or context supplied only by the user as user-provided.
6. Never adjust an aggregate total mechanically. Read its definition and recompute using the file's existing inclusion rules; a paid item can increase a gross-obligations total but reduce or leave unchanged an outstanding-debt total.
7. When editing monthly Markdown, re-read the current file before patching. Remember that `read_file` displays `LINE_NUM|CONTENT`, so Markdown table pipes can look duplicated in the rendered output.
8. After the update, verify files, ledger entries, links, table column counts, and reconciliation of any changed total.

## Fluxo: fechamento mensal

1. Ler `INDEX.md` do mês, se existir.
2. Ler `AAAA-MM_00_CONTROLE_PAGAMENTOS.md`, se existir.
3. Ler `AAAA-MM_CONTAS_FATURAS.md`, se existir.
4. Rodar script de auditoria, quando disponível.
5. Listar pendências abertas.
6. Listar comprovantes sem origem.
7. Listar documentos sem `.md` correspondente.
8. Gerar resumo com totais e pontos de atenção.
9. Não marcar como concluído se houver pendência sem justificativa.

## Cuidados operacionais

- Não apague originais financeiros em caso de dúvida.
- Para itens suspeitos/duplicados, prefira mover para pasta `REVISAR/` dentro do mês.
- Não registre tokens, senhas ou chaves em Markdown.
- Não invente OCR, IDs, datas ou valores.
- Sempre cite caminhos dos arquivos alterados.
- Quando fizer melhoria em agentes ou fluxo financeiro, registre em `/home/usuario/.hermes/docs/CHANGELOG.md`.

## Verificação antes de finalizar

- [ ] O arquivo original foi salvo no mês correto.
- [ ] Existe `.md` correspondente quando aplicável.
- [ ] Metadados mínimos foram preenchidos ou marcados como `A confirmar`.
- [ ] Controle mensal foi atualizado quando necessário.
- [ ] Origem e comprovante foram linkados quando ambos existem.
- [ ] Nenhum arquivo real foi apagado sem autorização explícita.
- [ ] A resposta final cita os caminhos principais alterados.
