---
name: financeiro-comprovantes
description: "Use when handling Igor's financial documents and controls."
version: 1.14.0
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

Use esta skill para qualquer tarefa financeira envolvendo boletos, faturas, contas, comprovantes de pagamento, transferências, controles mensais e auditoria da pasta de comprovantes do Igor.

## Proteção de identificadores

Não transcreva em respostas, tabelas, blocos de código, OCR ou novos arquivos Markdown CPF/CNPJ completos, agência/conta, linha digitável, código de barras, autenticação/NSU ou ID completo de transação, Pix end-to-end, QR/Pix nem credenciais. Verifique esses dados diretamente no original quando a conciliação exigir; preserve o original e masque tais trechos antes de incluir OCR em arquivos derivados. Se indispensável distinguir registros, use somente sufixo mascarado ou `[REDACTED]`. Para pagamento, indique o caminho do original em vez de retransmitir o código.

## Gate de conclusão para pedidos com várias etapas

Trate a captura ou preparação do documento como uma etapa, não como conclusão de um pedido financeiro mais amplo. Para toda fatura ou comprovante recebido, extraia e confira os dados diretamente no documento original antes de classificá-lo; em comprovante de pagamento, confirme no próprio comprovante valor, data, beneficiário e indicação de liquidação. Um boleto ou recibo do condomínio com selo/carimbo “PAGO” registra o status indicado pelo emissor, mas não substitui comprovante ou extrato bancário de liquidação; não dê baixa nem altere saldos com base apenas em declaração do usuário, selo “PAGO”, nome de arquivo, busca textual ou agendamento. Se o usuário informar pagamento sem prova bancária, registre “pagamento informado; conciliação pendente” e mantenha a baixa financeira pendente. Classifique status por estado semântico, não por substring: reconheça formas flexionadas de quitação (`Pago/Paga`, `Quitado/Quitada`, `Liquidado/Liquidada`), mas não marque como pago textos negativos (`Não pago`) ou pendentes (`Pagamento em revisão`, `Em processamento`); confirme a frase completa e cubra casos positivos, negativos e de revisão em testes quando o status for calculado por código. Concilie com a obrigação exata usando final do cartão e vencimento quando constarem no comprovante. Se faltarem identificadores, associe somente quando a combinação de beneficiário/CNPJ, valor exato e referências disponíveis identificar uma única obrigação; registre quais dados foram conciliados, mas não aparecem no comprovante. Se houver ambiguidade, mantenha `Revisar` em vez de marcar `Pago`, preserve as evidências e não altere a obrigação nem o fluxo por inferência. Quando houver vários comprovantes, processe cada um de forma independente: a ambiguidade de um não deve bloquear a conciliação dos demais identificados com unicidade; deixe apenas o item ambíguo pendente e informe qual campo falta para resolvê-lo. Arquive o comprovante no mês do desembolso e atualize os controles do mês do pagamento e do mês da obrigação quando forem diferentes; atualize também o registro da fatura e a ficha correspondente. Em seguida, atualize os índices, projeções ou dashboards pedidos e recalcule totais afetados. Verifique os artefatos finais e reconcilie contagens e valores antes de declarar concluído. Se um arquivo esperado não existir, procure a estrutura canônica real em vez de presumir o nome; mantenha explícitas como pendentes as etapas não realizadas. Um bloqueio ou falha em uma consulta/ferramenta não encerra o pedido inteiro: não repita uma chamada idêntica já bloqueada; retome do estado legível, prossiga nas etapas independentes por um método efetivamente suportado e registre apenas resultados verificáveis. Se nenhuma rota disponível produzir evidência legível, deixe essa etapa explicitamente pendente e peça o insumo necessário — não declare todo o trabalho interrompido nem infira dados financeiros.

Pasta base autorizada:

`/home/igorferreira/MEGA/Comprovantes`

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
- pendências abertas ou comprovantes faltantes;
- **atualização completa do plano** ("atualiza todo o nosso plano" / "atualiza tudo") após múltiplos pagamentos e resgates na mesma sessão.

Para **atualização completa do plano** (cascata de 14+ arquivos após múltiplas transações), seguir [`references/atualizacao-plano-completo.md`](references/atualizacao-plano-completo.md).

Para tarefas de **fluxo de caixa, projeções de CDB, orçamento e atualização do fluxo**, seguir primeiro [`references/fluxo-caixa-source-of-truth.md`](references/fluxo-caixa-source-of-truth.md), que define a fonte vigente, o escritor oficial, a geração do dashboard e os gates de reconciliação. Não assumir horizonte, nome de arquivo, motor ou formatos de saída pela memória; conferir o canônico e o escritor atuais antes de editar. `references/fluxo-caixa-excel-markdown.md` é material legado, não o procedimento de produção.

Para **análise de pedaladas** (usar limite de cartão para cobrir déficits), seguir [`references/analise-pedaladas.md`](references/analise-pedaladas.md).

Não use para:

- alterar arquivos fora de `/home/igorferreira/MEGA/Comprovantes` sem autorização explícita;
- apagar documentos financeiros originais em caso de dúvida;
- inferir valores/datas sem evidência no arquivo, OCR ou contexto do usuário.

## Estrutura do diretório

A raiz `~/MEGA/Comprovantes/` segue esta organização:

```
~/MEGA/Comprovantes/
├── 📄 CONTRACHEQUE.md              ← canônicos (raiz)
├── 📄 ENTRADAS.md                  ← renda canônica (CLT, VALLO, aluguel, 13º, etc.)
├── 📄 HOME-EQUITY.md
├── 📄 MAPA-CUSTO-VIDA.md
├── 📄 ENDIVIDAMENTO.md
├── 📄 DIAGNOSTICO.md               ← fonte da verdade cronológica de diagnósticos (data/hora, escopo, veredito)
├── 📄 FLUXO-CAIXA-<HORIZONTE-VIGENTE>.md
├── 📄 FLUXO-CAIXA-<HORIZONTE-VIGENTE>.csv
├── 📄 FLUXO-CAIXA-<HORIZONTE-VIGENTE>.xlsx
├── 📄 AVISOS.md
│
├── 📁 _controles/                  ← prefixo CONTROLE_ obrigatório
│   ├── CONTROLE_INDICE.md
│   ├── CONTROLE_FATURAS_MANTIDOS.md
│   ├── CONTROLE_CHAVES_PIX.md
│   ├── CONTROLE_ORCAMENTO.md
│   └── CONTROLE_ORCAMENTO_SISTEMA_APROVACAO.md
│
├── 📁 _saldos/                     ← um arquivo SALDO_BANCO.md por conta
│   ├── INDEX.md                    ← visão geral de todos os saldos
│   ├── SALDO_99PAY.md
│   ├── SALDO_NUBANK.md
│   ├── SALDO_INTER.md
│   ├── SALDO_C6.md
│   ├── SALDO_ITAU.md
│   └── SALDO_BRASILCARD.md
│
├── 📁 _fichas/                     ← prefixo FICHA_CARTAO_BANCO_ obrigatório
│   ├── FICHA_CARTAO_NUBANK_3033.md
│   ├── FICHA_CARTAO_ITAU_PASSAI_6698.md
│   └── ... (26 fichas, todas com banco no nome)
│
├── 📁 _Analises/                   ← cenários, planos, análises
│   ├── INDEX-CENARIOS.md
│   ├── PLANO-DOSSIE-MASTER-DETAIL.md
│   └── cenarios/
│
└── 📁 2026/ ... 2025/ ...          ← comprovantes históricos por ano
```

Regras:
- **Raiz**: apenas arquivos canônicos (~10). AVISOS.md fica na raiz.
- **`_controles/`**: todos os arquivos com prefixo `CONTROLE_`.
- **`_fichas/`**: todos com prefixo `FICHA_CARTAO_BANCO_`. Incluir banco emissor no nome. Cartões zerados/cancelados também têm ficha.
- **`_Analises/`**: tracking de cenários, planos, análises de pedalada.
- Ao atualizar uma ficha durante a varredura, salvar em `_fichas/`.
- Links no `ENDIVIDAMENTO.md` devem apontar para `./_fichas/` e `./_controles/`.

### Cabeçalho padronizado de ficha de cartão

Toda ficha em `_fichas/` deve abrir com uma tabela de identificação de 4 campos:

```markdown
# 🟢 Ficha — Nome Cartão Final

| | |
|---|---:|
| **Nome** | Nome do cartão |
| **Banco emissor** | Emissor jurídico (com fonte) |
| **Vencimento** | Dia XX ou — (zerado/cancelado) |
| **Últimos 4 dígitos** | XXXX ou — |
```

**Regras:**
- Nome do arquivo: `FICHA_CARTAO_BANCO_NOME_FINAL.md`
- O banco emissor deve ser pesquisado na internet (contratos, páginas oficiais, BCB) — nunca usar `❓` sem tentativa documentada. Ver `references/pesquisa-emissores-cartoes.md`.
- Cartões zerados/cancelados também têm ficha e cabeçalho.
- Para atualização em lote de múltiplas fichas, usar script Python com `pathlib` + `re` — não editar uma a uma.
- O campo "Vencimento" usa "Dia XX" para cartões ativos, e "— (motivo)" para zerados/cancelados/liquidados.

## Estrutura esperada (comprovantes mensais)

A estrutura de comprovantes usa ano e mês:

```text
/home/igorferreira/MEGA/Comprovantes/
└── 2026/
    ├── 2026_01_JANEIRO/
    ├── 2026_02_FEVEREIRO/
    ├── ...
    └── _Controle_Anual/
```

Dentro de cada mês, os arquivos principais tendem a seguir:

- `INDEX.md`
- `AAAA-MM_00_CONTROLE_PAGAMENTOS.md`
- `AAAA-MM_00_DIVIDA.md`
- `AAAA-MM_CONTAS_FATURAS.md` — padrão legado, só existe em `2026_01_JANEIRO` e `2026_02_FEVEREIRO`, não esperar em meses mais recentes
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
- Identificadores necessários à conciliação: confira-os no original sem transcrevê-los; se indispensável, registre somente sufixo mascarado ou `[REDACTED]`.

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
2. Salvar o original com sufixo `COMPROVANTE-PAGAMENTO` ou `COMPROVANTE-TRANSFERENCIA` na raiz da pasta do mês em que o dinheiro efetivamente saiu.
3. Criar `.md` correspondente com OCR/texto e metadados.
4. Procurar a origem relacionada no mês de vencimento/competência e nos meses próximos; não presumir que pagamento e obrigação pertencem ao mesmo mês.
5. Se o pagamento e a fatura caírem em meses diferentes:
   - manter a fatura original no mês da obrigação e arquivar o comprovante no mês do desembolso — nunca guardar o comprovante apenas na subpasta da fatura por ela vencer no mês seguinte;
   - registrar a saída de caixa e atualizar controle e `INDEX.md` do mês do pagamento;
   - no mês da obrigação, marcar a fatura como paga, atualizar controle/dívida/agenda e `INDEX.md` conforme existirem, com link para o comprovante arquivado no mês do pagamento;
   - excluir o valor quitado da necessidade de desembolso pendente do mês da obrigação, sem apagar sua linha de auditoria e sem contar a saída de caixa duas vezes.
6. Atualizar o controle da obrigação:
   - status `Pago`;
   - link `Comprovante`;
   - manter link `Origem` quando existir.
7. Se a origem não for encontrada ou a associação não for única, registrar como item `Revisar`; não marcar como pago por aproximação.


## Procedimento padrão: conta/fatura + comprovante com OCR/Markdown

Quando o usuário enviar conta, fatura, boleto ou comprovante financeiro por imagem/PDF e pedir para salvar:

1. Salvar o arquivo original na **raiz da pasta mensal** correspondente, não em subpasta, salvo instrução explícita em contrário.
2. Usar o padrão local de nomenclatura com data, tipo, entidade, valor quando útil e sufixo adequado:
   - conta/fatura/boleto: `AAAA-MM-DD_CONTA-ENTIDADE...` ou `AAAA-MM-DD_FATURA-ENTIDADE...`;
   - comprovante pago: `AAAA-MM-DD_TIPO-ENTIDADE-RVALOR-COMPROVANTE-PAGAMENTO.ext`.
3. Sempre extrair texto do documento:
   - PDF pesquisável: use extração de texto (`pdftotext -layout` — o `-layout` preserva as colunas dos boletos/faturas, essencial para reler vencimento/valor/composição sem embaralhar) ou equivalente, salvando a saída em arquivo temporário dentro do diretório de scratch configurado e lendo esse arquivo com `read_file` para inspecionar o conteúdo;
  - confirme que o texto extraído contém os campos relevantes antes de classificar o documento: código de saída, contagem de linhas/bytes e sucesso aparente do comando não provam que o conteúdo foi lido;
  - imagem/PDF escaneado: usar OCR local (`tesseract` ou equivalente) e inspeção visual quando necessário. Para screenshots de apps bancários brasileiros com fontes estilizadas, seguir [`references/ocr-banking-apps.md`](references/ocr-banking-apps.md) — varredura de modos PSM (especialmente 11 e 12) captura melhor que o default. Para **fotos de comprovantes/papel impresso**, aplicar a pipeline de pré-processamento de fotografia (grayscale + resize 200% + contrast-stretch) e usar PSM 3 — ver a seção "Photo de comprovante impresso" na mesma referência.
4. Sempre criar uma versão Markdown (`.md`) para cada documento financeiro relevante, contendo:
   - metadados principais: competência/referência, vencimento, data de pagamento, valor, pagador, recebedor e instituição; identificadores sensíveis devem ser conferidos no original e omitidos ou mascarados no registro derivado;
   - links relativos para o arquivo original;
   - seção `Texto extraído` ou `OCR / Texto extraído` com o conteúdo capturado após mascarar identificadores sensíveis conforme a seção `Proteção de identificadores`;
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

### 📱 Orientação para pagamento de boletos
- Siga a seção `Proteção de identificadores`: não copie a linha digitável, código de barras ou QR/Pix para a resposta ou para novos arquivos.
- Se o usuário precisar pagar, informe o caminho do documento original para que copie o código diretamente dele.

When the user sends a card payment receipt, treat the receipt as the source of truth for the paid amount and update both ledgers when applicable. See [`references/card-payment-proof-workflow.md`](references/card-payment-proof-workflow.md).

1. Extract payment timestamp, amount, beneficiary, destination bank, due date and payer. Consult origin-account details, barcode and transaction IDs only in the original when reconciliation requires them; do not transcribe full identifiers into the response or derived Markdown, and use a masked suffix only if indispensable.
2. Save the original image/PDF in the month folder and create a matching `.md` file.
3. Use the receipt amount in the filename when practical (e.g. `R163885`).
4. Update both `AAAA-MM_00_CONTROLE_PAGAMENTOS.md` **and** `AAAA-MM_00_DIVIDA.md` only when each file actually tracks that obligation; distinguish payment audit rows from outstanding-debt rows.
5. If the control file and receipt differ, prefer the receipt for fields it visibly proves. Label card name/final or context supplied only by the user as user-provided.
6. Never adjust an aggregate total mechanically. Read its definition and recompute using the file's existing inclusion rules; a paid item can increase a gross-obligations total but reduce or leave unchanged an outstanding-debt total.
7. When editing monthly Markdown, re-read the current file before patching. Remember that `read_file` displays `LINE_NUM|CONTENT`, so Markdown table pipes can look duplicated in the rendered output.
8. After the update, verify files, ledger entries, links, table column counts, and reconciliation of any changed total.

## Benefícios não salariais (VALLO e similares)

Quando o usuário mencionar depósitos de pacotes de benefícios como VALLO BENEFÍCIOS:

- **Nunca incorporar ao salário, rescisão, FGTS, aviso-prévio, férias ou 13º** — nem o depósito habitual nem o depósito recebido junto ao 13º.
- Registrar exclusivamente como **rendimento/recurso disponível do período** em que o depósito ocorrer.
- Não projetar o valor para meses futuros sem confirmar data e recorrência documentalmente.
- Se o usuário afirmar que o benefício "não entra na rescisão", registrar isso como regra fixa no `dados-contrato.json` com campo `user_confirmed_exclusion_from_termination: true` e nunca revisitar sem solicitação explícita.

## Fluxo: PDF automático — detectar, extrair, fichar, atualizar plano

⚠️ **CORREÇÃO DO USUÁRIO — 07/08/2026:** Quando Igor envia QUALQUER documento financeiro (PDF, imagem, CSV), não esperar instruções passo a passo. Identificar o tipo imediatamente e executar o ciclo completo.

### Detecção automática

| Evidência | Tipo | Ação |
|---|---|---|
| PDF com "CÉDULA DE CRÉDITO BANCÁRIO" | Contrato CCB | Extrair, salvar cópia limpa na raiz, atualizar HOME-EQUITY.md |
| Imagem com "Pagamento feito com sucesso" | Comprovante de pagamento | Salvar, criar .md, atualizar CONTROLE, linkar origem |
| PDF/CSV com "Lançamentos do cartão" ou colunas date/title/amount | Extrato/fatura de cartão | Salvar, criar .md com projeção, atualizar ficha, atualizar plano T3 e fluxo de caixa |
| PDF com "Fatura de [mês]" e vencimento visível | Fatura de cartão | Salvar, criar .md, atualizar ficha, atualizar plano T3 e fluxo de caixa |
| PDF com nome de conta fixa (Claro, Vivo, Light, etc.) | Conta de consumo | Salvar, criar .md, atualizar controle mensal |

### Ciclo completo (para fatura/extrato de cartão)

1. Extrair texto com `pdftotext` ou `tesseract --psm 6 -l por`
2. Salvar PDF/imagem na pasta mensal com nome padronizado `AAAA-MM-DD_TIPO-EMISSOR-FINAL-MES-RVALOR.ext`
3. Criar `.md` com mesmo nome base contendo: resumo, composição, parcelamentos, projeção, observações
4. Atualizar `_fichas/FICHA_CARTAO_BANCO_NOME_FINAL.md` com dados reais
5. Se o plano master-detail estiver ativo (`_Analises/PLANO-DOSSIE-MASTER-DETAIL.md`), atualizar T3 com status ✅
6. Se a mudança afetar o fluxo, atualize a fonte financeira e o YAML canônico aplicáveis, preservando alterações preexistentes no repositório. Antes de gerar, confira o `git status`/diff e limite as edições ao escopo sustentado por evidência. Execute o escritor oficial da família canônica e, quando a mudança afetar a interface ou os dados publicados, reconstrua o dashboard depois da última edição. Siga [`references/fluxo-caixa-source-of-truth.md`](references/fluxo-caixa-source-of-truth.md); não recalcule nem corrija MD/JSON/CSV/XLSX/HTML derivados manualmente.
   - Atualize `_controles/PAINEL_ACOMPANHAMENTO.xlsx`, `ENDIVIDAMENTO.md`, `AVISOS.md` ou o cadastro de vencimentos somente quando esses artefatos controlarem a obrigação alterada.
   - Espelhe artefatos para outra pasta apenas quando isso fizer parte do fluxo vigente ou do pedido; confirme a cópia após sincronizar.
7. Se um novo diagnóstico de endividamento ou operacional for gerado, registre entrada cronológica com data/hora em `~/MEGA/Comprovantes/DIAGNOSTICO.md`.
8. Reporte os dados financeiros afetados, o saldo atual e as âncoras projetadas no horizonte vigente, além das verificações de build/testes/rotas executadas e das pendências restantes.

Para CSV do Nubank: seguir `references/processamento-csv-nubank.md` (formato português, parcelas x/y, projeção sem total fechado).

### Fluxo: fatura fechada recebida como captura-resumo

Quando a captura do aplicativo mostrar **fatura fechada, valor total e vencimento**, mas não trouxer compras ou parcelamentos, seguir [`references/fatura-fechada-captura-resumo.md`](references/fatura-fechada-captura-resumo.md).

Regras centrais:

- separar dados visíveis, associação proveniente do inventário local e confirmação do titular;
- contabilizar o total fechado como cobertura mensal da conta, registrando que a auditoria por item está indisponível;
- manter a obrigação em aberto até existir comprovante de pagamento;
- não projetar meses futuros sem linhas `x/y`, documento relacionado ou confirmação explícita;
- atualizar em cascata dívida, controle de pagamentos, índice, diagnóstico, inventário e resumo anual;
- preservar original, OCR, Markdown, PDF da imagem e PDF pesquisável do relatório.

## Fluxo: fatura em aberto (não comprovante)

Quando a origem for imagem/captura de aplicativo, seguir também [`references/faturas-imagem-parcelamentos.md`](references/faturas-imagem-parcelamentos.md) para vinculação correta da imagem, dupla conferência OCR/visual, projeção `x/y`, tratamento de pagamentos/créditos anteriores e cascata de atualização.

Quando o usuário enviar o print de uma **fatura ainda não fechada** (e.g. fatura de cartão em andamento):

1. Criar `.md` descritivo com o valor acumulado até aquele momento, vencimento provável, cartões vinculados e limite disponível.
2. Nomear sem sufixo `COMPROVANTE-PAGAMENTO` — usar sufixo descritivo como `FATURA-CARTAO-X-AGOSTO-RABERTO`. **Não incluir vencimento provável no nome do arquivo quando a captura não o mostrar**; manter a data como `a confirmar` nos metadados.
3. Adicionar à seção "Em aberto" de `AAAA-MM_00_DIVIDA.md` com status ⬜ e nota de que o valor pode crescer.
4. Quando houver antecipações já aplicadas a essa fatura (pedaladas anteriores), registrá-las explicitamente no arquivo e descontá-las do saldo disponível, mas **não** subtrair do valor em aberto (que é o que o app exibe).
5. Comprovante de pagamento da fatura será um arquivo separado quando ocorrer.
6. Se o OCR bruto tiver erros tipográficos, preservar `*.ocr-raw.txt` e criar `*.ocr.txt` revisado, corrigindo apenas o que foi confirmado visualmente e listando campos ausentes.
7. Antes e depois de editar os controles, reler o estado atual e procurar duplicidades por cartão/competência. Em caso de edição concorrente, manter uma única linha financeira e um arquivo canônico; mover conjuntos redundantes para `REVISAR/` ou `_DUPLICADOS-RECONCILIADOS/`, sem apagar originais.
8. Recalcular a soma pelas linhas da tabela, verificar que o cartão aparece uma única vez em dívida/controle/diagnóstico e validar todos os links locais.

### Fluxo: fatura em atraso confirmado + substituição de provisão por fatura completa

Quando a captura mostrar **fatura em atraso** (🔴, com contagem de dias) ou quando uma **fatura completa oficial** substituir uma **provisão parcial** (ex.: parcela conhecida de R$ 537,70 substituída por fatura total de R$ 5.660,52), seguir [`references/fatura-atraso-provisao-substituicao.md`](references/fatura-atraso-provisao-substituicao.md).

Regras centrais:
- fatura em atraso usa status 🔴 e acréscimo de juros/multa documentados
- substituição de provisão: calcular diferença e atualizar total; remover provisão antiga dos controles
- em ambos os casos, atualizar em cascata: DIVIDA, CONTROLE, DIAGNOSTICO, relatório simplificado, dados-vencimentos.json e agendamentos
- registrar estratégias financeiras do usuário (ex.: pagar A, Pix crédito no B, pagar C) como nota, sem alterar totais documentados
- validar não duplicação e soma final

## Auditoria de cartões, faturas mensais e provisões futuras

### Relatório simplificado de cadastro dos cartões

Quando o usuário pedir nome, emissor, finais físico/virtual, vencimento, fechamento e limites de todos os cartões, seguir [`references/relatorio-simplificado-cartoes.md`](references/relatorio-simplificado-cartoes.md).

Quando o emissor estiver ausente, genérico ou conflitante, seguir também [`references/pesquisa-emissores-cartoes.md`](references/pesquisa-emissores-cartoes.md): pesquisar profundamente em contratos/páginas oficiais e Banco Central, separando **marca**, **emissor jurídico**, **financiador do saldo** e **credor atual**. Não agrupar co-brands por marca e não alterar o total financeiro ao apenas reclassificar a entidade credora.

### Agenda de vencimentos

Quando o usuário pedir uma **agenda**, **calendário**, **cronograma** ou **lista geral de contas a pagar** de todos os meses com status de pagamento, seguir [`references/agenda-vencimentos.md`](references/agenda-vencimentos.md). Este relatório consolida cartões, contas fixas recorrentes e obrigações futuras em ordem cronológica, com seção de resumo mensal e cartões sem informação.

**Além da consolidada, criar uma `AGENDA.md` individual dentro da pasta de cada mês** (ex.: `2026_08_AGOSTO/AGENDA.md`) — mais enxuta, visual e de consulta rápida.

**Quando um vencimento estiver errado** (usuário contesta data ou cron job mostra alerta incorreto): buscar a fatura real dos últimos 3 meses, extrair a data verdadeira e atualizar todas as agendas. Ver [`references/correcao-vencimentos-contas-fixas.md`](references/correcao-vencimentos-contas-fixas.md). Comprovante PIX/RecargaPay NÃO informa vencimento — sempre preferir a fatura original.

**Para lembretes automáticos diários**, criar um cron job `no_agent=True` com o script `~/.hermes/scripts/verificar-vencimentos.py` e o cadastro `~/.hermes/scripts/dados-vencimentos.json`. O script verifica os próximos 5 dias e entrega no Telegram às 8h. O cadastro precisa ser mantido em sincronia com os controles mensais — ver [`references/lembrete-diario-vencimentos.md`](references/lembrete-diario-vencimentos.md) para estrutura, manutenção e pitfalls.

Regras centrais:

- contar contas/produtos, deduplicando virtuais vinculados;
- exibir somente os três últimos dígitos solicitados;
- distinguir final físico, virtual e final de tipo não identificado;
- preservar conflitos entre cadastro e fatura em vez de escolher silenciosamente;
- marcar datas históricas e data-base dos limites;
- usar `—` para ausência, sem derivar limite total ou classificar o tipo do cartão por suposição;
- gerar tabela de cobertura e PDF A4 paisagem auditado, inspecionando inclusive palavras isoladas no topo da última página.

Quando o usuário pedir para descobrir quantos cartões possui, verificar a cobertura de faturas de um mês ou provisionar parcelas futuras, seguir [`references/auditoria-inventario-cartoes-provisoes.md`](references/auditoria-inventario-cartoes-provisoes.md).

### Dossiê consolidado para advogado

Quando o usuário pedir um **documento único com todos os cartões para o advogado** (ou para negociação externa), siga [`references/dossie-advogado-cartoes.md`](references/dossie-advogado-cartoes.md).

Quando o pedido for específico para um **dossiê simplificado master-detail** (tabela de todas as dívidas ordenadas da maior para menor, com capacidade de pagamento, Home Equity destacado, e envio por email com 2 anexos), siga [`references/dossie-master-detail.md`](references/dossie-master-detail.md). Este formato foi desenvolvido para o Dr. Israel em 07/08/2026 e é mais enxuto que o dossiê completo.

**Primeiro contato com advogado novo (WhatsApp/email):** quando Igor estiver iniciando conversa com um escritório de advocacia para renegociação, siga [`references/primeiro-contato-advogado-dividas.md`](references/primeiro-contato-advogado-dividas.md). Apresentar **apenas os cartões em negociação** (não pagos), agrupados por banco, com valores, tempo de atraso e status de negativação. Formatar em duas versões: `.md` (registro) e `.txt` (pronto pra colar no WhatsApp).

O dossiê tem uma tabela mestra com colunas específicas (cartão, final, emissor, vencimento, fechamento, limite total, disponível, dívida corrente, dívida futura, status, observações) e seções de resumo executivo, projeção de endividamento e cronograma. É um **documento vivo** — cada nova fatura ou mudança de status deve atualizá-lo.

Não confundir com o `relatorio-simplificado-cartoes` (foco em cadastro auditável com finais físico/virtual e data-base dos limites) nem com a `auditoria-inventario-cartoes-provisoes` (foco em cobertura de faturas e provisões futuras). O dossiê do advogado é mais amplo e voltado à renegociação.

**Antes de entregar o dossiê ao advogado**, revisar a narrativa seguindo [`references/revisao-narrativa-dossie-juridico.md`](references/revisao-narrativa-dossie-juridico.md): 6 pontos de verificação (contexto de boa-fé, pedido explícito, risco do ativo, premissa de fluxo, tom com o advogado, evidência documental).

**Depois da revisão narrativa, executar auditoria cruzada de valores** seguindo [`references/auditoria-cruzada-dossie.md`](references/auditoria-cruzada-dossie.md): soma de pagos + não pagos = dívida total (R$ 0,00 de diferença), cobertura de recursos, consistência de percentuais e pitfalls de estimativas agrupadas.

Quando houver captura explícita de cartão com **R$ 0,00** e confirmação do titular sobre ausência de fatura/parcelamentos, seguir também [`references/cartao-saldo-zero.md`](references/cartao-saldo-zero.md). Tratar `saldo zero confirmado` como categoria própria: não é fatura completa, não é obrigação parcial e não pode permanecer em `nenhuma informação localizada`. Separar sempre o que a imagem comprova do que foi declarado pelo usuário; bloqueio do cartão é status operacional, não dívida. O item pode aparecer no controle mensal com R$ 0,00, mas não altera o total financeiro.

**Variante — liquidação do emissor pelo BC:** se o cartão foi emitido por instituição liquidada pelo Banco Central (ex.: Will Bank), a confirmação independe de captura de app (que não funciona mais). Pesquisar o BCB oficialmente e tratar como `saldo zero confirmado — banco liquidado`. Ver seção 6 do reference para o procedimento completo.

Princípios obrigatórios:

- contar contas/produtos de cartão, deduplicando físico e virtual vinculados;
- excluir empréstimos e outros produtos que não sejam cartão;
- separar `fatura completa`, `obrigação parcial` e `nenhum valor localizado`;
- nunca transformar “fatura não localizada” em “saldo zero”;
- chamar a soma de faturas e provisões de **piso documental** enquanto houver faturas ausentes ou abertas;
- ao receber fatura fechada, preservar a captura aberta como histórico e marcá-la como superada;
- quando houver valor bruto no aplicativo e ajuste informado pelo usuário, registrar os dois e identificar claramente qual informação veio do usuário;
- nunca atribuir um residual aritmético inteiro a um parcelamento sem linha visível, documento relacionado ou confirmação explícita; se evidência posterior corrigir o valor, preservar a conciliação antiga como histórico e classificar o restante como lançamentos não visíveis;
- ao projetar `x/y`, avançar mês a mês até `y/y`, registrar a premissa “sem novas compras, juros, tarifas ou estornos” e não inventar vencimento ausente;
- quando a tela já mostrar `valor atual` separado de `pagamentos/créditos`, não subtrair o crédito anterior novamente sem prova de que o aplicativo ainda não o incorporou;
- para obrigações que atravessam o ano, atualizar controles mensais, resumo anual, contratado futuro e criar a estrutura do ano seguinte;
- recalcular todas as somas e validar links e PDFs antes da entrega.

## Pedaladas e pagamentos cruzados

Quando um pagamento for feito com limite de **outro cartão** (via RecargaPay, outro cartão, intermediário):

- Registrar em `AAAA-MM_00_PAGAMENTOS_CRUZADOS.md`: obrigação quitada, valor, instrumento usado, onde vai reaparecer e link do comprovante.
- A obrigação original some do credor, mas **reaparece na próxima fatura do instrumento usado** — rastrear explicitamente.
- Nunca marcar como "quitado sem rastro" — sempre registrar o "onde vai aparecer depois".
- Atualizar a `FICHA_CARTAO_<INSTRUMENTO>.md` do cartão usado como instrumento: adicionar linha com data, valor e descrição (ex.: `+ PIX Brasilcard 06/08 | + R$ 673,65`). O total da ficha aumenta com cada pedalada.
- Atualizar a seção "Próximo passo" no arquivo de pedaladas com `[ ]` pendentes para conferência quando as faturas posteriores fecharem.
- Para diagnóstico de endividamento: listar pedaladas ativas separadamente do total em aberto, pois representam dívida que mudou de endereço mas não foi amortizada.

### 📱 Captura de dívida total de cartão em negociação

Quando o usuário enviar uma captura de app mostrando o **valor total utilizado** de um cartão em negociação (ex.: Inter, PAN, RecargaPay):

1. Fazer OCR (`tesseract --psm 6 -l por`).
2. Salvar imagem original + criar `.md` com OCR e metadados na pasta mensal.
3. Atualizar `FICHA_CARTAO_*.md` com o valor real (substituir o valor rastreado manualmente).
4. Calcular o **delta** entre o valor rastreado (soma de pedaladas + base) e o valor real do app. Reportar explicitamente: "Delta não mapeado: +R$ X.XXX,XX".
5. Atualizar `ENDIVIDAMENTO.md` — linha da tabela da seção 4 com o valor real + evidência + nota sobre o delta.
6. NÃO recalcular o fluxo de caixa automaticamente para cartões em negociação — a dívida deles não é paga, só renegociada.

### 💀 Uso estratégico de cartões que vão pra negociação

Quando o usuário decidir que um cartão **não será pago** (vai pra negociação), o limite disponível dele pode ser usado para cobrir despesas essenciais ANTES do vencimento. Ver [`references/uso-estrategico-cartoes-negociacao.md`](references/uso-estrategico-cartoes-negociacao.md).

**Padrões principais:**
1. Pagar contas (luz, gás) via RecargaPay com o cartão de negociação → preserva CDB
2. Cobrir cheque especial via PIX crédito do cartão de negociação → evita juros de 8% a.m.
3. Antecipar uso do limite antes do bloqueio pós-atraso

**Regras:** somar ao total "queimado" do cartão, NÃO subtrair do CDB, registrar comprovante com sufixo identificando o cartão (ex.: `COMPROVANTE-DIGIO`).

### ⚠️ Pix crédito via RecargaPay — a dívida fica no CARTÃO, não no RecargaPay

O RecargaPay oferece um serviço de **Pix crédito**: você saca dinheiro usando o **limite de um cartão de crédito**. O RecargaPay é apenas o intermediário/processador — a dívida real aparece na **fatura do cartão utilizado**, não no RecargaPay.

**Exemplo do fluxo (que o Igor usa):**

1. Pagar Nubank → libera o limite do Nubank
2. Pix crédito RecargaPay de R$ 5.000 usando o **limite do Nubank** → o RecargaPay só processa
3. Pagar Passaí com o dinheiro do Pix
4. Resultado: a dívida de R$ 5.000 vai para a **fatura de setembro do Nubank**, não para o RecargaPay

**Regras para registrar:**
- A dívida do Pix crédito vai para o **cartão cujo limite foi usado**, não para o intermediário (RecargaPay etc.)
- Atualizar `PAGAMENTOS_CRUZADOS.md` com: quem pagou (intermediário), qual cartão foi usado como fonte, onde a dívida reaparece
- No controle mensal: a obrigação original some do credor antigo, mas a nova despesa entra na fatura futura do cartão fonte
- No diagnóstico: listar como pedalada ativa — dívida que mudou de credor, não foi amortizada
- Não somar ao saldo do RecargaPay — a dívida não é deles

## Mapa de custo de vida

Igor mantém um **mapa canônico de custo de vida** em dois lugares idênticos (sincronizar ambos ao atualizar):

- `~/MEGA/Comprovantes/MAPA-CUSTO-VIDA.md` ← pasta financeiro
- `~/MEGA/Documentos/carreira/MAPA-CUSTO-VIDA.md` ← pasta carreira

### Arquivos canônicos na raiz de Comprovantes

Além do mapa de custo de vida, a raiz `~/MEGA/Comprovantes/` contém os seguintes arquivos canônicos (atualizar quando houver mudança de contrato, renda ou premissas):

| Arquivo | Conteúdo | Atualizar quando |
|---|---|---|
| `ENTRADAS.md` | Renda recorrente + pontual + resumo anual | Mudar salário, VALLO, aluguel, 13º, dissídio |
| `MAPA-CUSTO-VIDA.md` | Fixas mensais, renda, teto, assinaturas | Mudar custo fixo ou renda |
| `HOME-EQUITY.md` | CCB completa com cronograma SAC 50 parcelas | Novo contrato ou amortização extraordinária |
| `CONTRACHEQUE.md` | Último real + projeção até dez/ano+2 | Novo contracheque ou dissídio |
| `DIAGNOSTICO.md` | Fonte da verdade cronológica de diagnósticos financeiros, operacionais e de dívida com data/hora exata | Novo diagnóstico, varredura de cartões, auditoria de fatura/pedalada ou fechamento relevante |
| `FLUXO-CAIXA-<HORIZONTE-VIGENTE>.md` | Projeção de fluxo de caixa completo | Mudança de premissas (gastos, renda, dívidas) — identificar o canônico e o horizonte pelo estado atual do diretório e do próprio arquivo |
| `CONTROLES.md` | Índice vivo de todos os controles financeiros ativos, com status por cartão | Sempre que um controle novo for criado ou um cartão mudar de status |
| `ENDIVIDAMENTO.md` | Camada estratégica: cartões mantidos/negociação, propostas de acordo recebidas, monitoramento de negativação/protesto/ação judicial | Cartão muda de status, proposta chega, evento de negativação/protesto — ver seção "Diagnóstico e estratégia de dívida" abaixo |

**Regras de ouro do modelo de orçamento (corrigidas em 31/07/2026):**
- 💰 **CLT líquido** paga: fixas + livres + Light + Gás + faturas de cartão + C6
- 💜 **VALLO BENEFÍCIOS** paga: Home Equity. Sobra do VALLO (crescente com SAC) vai pra reserva
- 🔒 **Assinaturas IA** (ChatGPT, Gemini, Claude, Manus) = ferramentas de trabalho, **NUNCA cortar**
- ✂️ Únicos cortes possíveis: telefonia (portabilidade) e academias excedentes

Quando o usuário perguntar "qual meu custo de vida?" ou "quanto gasto por mês?":
1. Ler o arquivo acima — não recalcular do zero.
2. Apresentar: fixas mapeadas + custo declarado + gap variável.
3. Se houver nova despesa informada, atualizar ambos os arquivos.

**Valores atuais (corrigidos em 25/07/2026):**
- Fixas mapeadas e somadas: R$ 3.916,61/mês
- Teto de custo de vida confirmado por Igor: R$ 4.000/mês
- Folga dentro do teto: R$ 83,39
- Parcelamentos e faturas de cartão pertencem ao plano de dívidas, não ao custo fixo

**Composição das fixas (atualizado 31/07/2026):**

O modelo separa **LAZER** (R$ 1.970) e **NÃO-LAZER** (R$ 2.451) = total R$ 4.421 (Set/26+ com TotalPass):

| Categoria | Item | Valor | Nota |
|---|---|---|---|
| 🍺 LAZER | Claro | R$ 330 | 🔒 Futebol em casa — economiza bar. NÃO cortar |
| 🍺 LAZER | Karatê | R$ 100 | Saúde |
| 🍺 LAZER | TotalPass | R$ 240 | 🆕 SmartFit + Crossfit (Set/26+). Ago/26: R$ 339 separados |
| 🍺 LAZER | Combustível | R$ 300 | |
| 🍺 LAZER | Livres | R$ 1.000 | Reduzido de R$ 2.000 em 31/07/2026 |
| 🏠 NÃO-LAZER | Condomínio | R$ 1.020 | Estrutural |
| 🏠 NÃO-LAZER | Vivo | R$ 105 | |
| 🏠 NÃO-LAZER | IA (4) | R$ 408 | 🔒 Trabalho — ChatGPT, Gemini, Claude, Manus |
| 🏠 NÃO-LAZER | Light | R$ 778 | Jul/26 real: 454 kWh |
| 🏠 NÃO-LAZER | Gás | R$ 140 | Média histórica |

**Ajustes já aplicados (não sugerir novamente):**
- 🏋️ TotalPass: SmartFit R$ 139 + Crossfit R$ 199 → R$ 240 (economia R$ 99/mês, Set/26+)
- 🍺 Livres: R$ 2.000 → R$ 1.000 (economia R$ 1.000/mês)
- 📱 Claro: mantido. Assistir futebol em casa economiza idas ao bar
- 🤖 IA (4): mantidas. Ferramentas de trabalho como Arquiteto de IA na HDI

**Assinaturas de IA (todos planos básicos/pro entry, em USD):**
- ChatGPT Plus: $20/mês | Gemini Advanced: $19,99/mês | Claude Pro: $20/mês | Manus Pro Entry: $20/mês
- Total: ~$79,99/mês (~R$ 408 pela cotação de jul/2026)

> 🔒 As 4 assinaturas são **ferramentas de trabalho**. NUNCA sugerir cortá-las. O único corte possível já foi feito (TotalPass em Set/26).

## Diagnóstico e estratégia de dívida

### Fonte obrigatória de salário, benefícios e custo de vida

> ⚠️ **PITFALL CRÍTICO — já ocorreu múltiplas vezes:** Subtrair o custo de vida da renda ANTES de calcular capacidade de pagamento. Correto: usar renda líquida TOTAL (CLT + VALLO) como disponível integral, porque as despesas de custo de vida são pagas COM CARTÃO DE CRÉDITO e já estão embutidas nas faturas listadas na tabela de cartões. Subtrair o custo de vida novamente duplica o desconto — a capacidade real é ~R$ 13.281, não ~R$ 9.281.

Antes de calcular qualquer plano de dívida para Igor:

1. Ler o **contracheque mensal normal mais recente** em `CARREIRA/rescisao-clt/contracheques/`; evitar férias, 13º, complemento CCT e eventos extraordinários como referência recorrente.
2. Separar explicitamente:
   - salário-base;
   - parcela fixa/CCT;
   - remuneração CLT bruta;
   - INSS, IRRF e empréstimo em folha;
   - salário CLT líquido em conta;
   - VALLO e outros benefícios como recursos separados, nunca como salário ou verba rescisória.
3. **NÃO subtrair o custo de vida da renda ao calcular a capacidade de pagamento.** Igor paga o custo de vida (~R$ 4.000) integralmente nos cartões de crédito — essas despesas já estão embutidas nas faturas listadas na Seção 3 do dossiê. Subtrair novamente duplicaria o desconto. Usar a renda líquida total (CLT + VALLO) como disponível integral.
4. Ler o mapa canônico `~/MEGA/Comprovantes/MAPA-CUSTO-VIDA.md` e seu espelho em CARREIRA.
5. **Recalcular a soma das linhas** do mapa; não confiar cegamente no total escrito. Se houver divergência, corrigir os dois espelhos e registrar a data.
6. Usar o teto de custo confirmado pelo usuário uma única vez no fluxo. Se os fixos forem menores que o teto, mostrá-los como informação "incluída no teto", sem subtrair fixos e teto cumulativamente.
7. Parcelamentos e faturas de cartão pertencem ao plano de dívida; não inflar o custo de vida somando-os novamente.
8. Quando renda ou custo forem corrigidos, recalcular todos os cenários, home equity e a própria qualificação de superendividamento. Não preservar uma conclusão jurídica produzida por premissas antigas.
9. Distinguir **meta negocial** de **teto absoluto**: a meta preserva folga e busca desconto; o teto é a prestação máxima matemática antes de exigir nova revisão.

Quando o usuário apresentar uma dívida total elevada e pedir estratégia de pagamento:

1. **Calcular viabilidade** com margem mensal pura: `prazo = dívida ÷ margem`. Se > 24 meses → declarar "inviável sem evento de liquidez".
2. **Mapear eventos de liquidez disponíveis**: home equity, aumento de salário, 13º, rescisão — quantificar cada um e o que sobra de dívida após cada evento.
3. **Ordem de ataque por custo de juros**:
   - Cheque especial (12–15%/mês) → prioridade máxima
   - Rotativo de cartão / RecargaPay → urgente
   - Parcelado fixo com taxa → manter em dia
   - Dívida pessoal sem juros (amigo/familiar) → após eventos de liquidez
4. **Cenários de renegociação**: simular múltiplos descontos (por exemplo 30%, 40% e 50%) e calcular a parcela total, sem tratar nenhum percentual como “realista” ou garantido sem proposta atual e documentada do credor. O teto deve preservar custo de vida e contingência mensal.
5. **Pedaladas ativas**: listar separadamente do total em aberto — representam dívida que mudou de credor mas existe.
6. **Planos jurídicos e superendividamento**: para atraso planejado, negociação em 24 meses, Consumidor.gov.br, Procon/CEJUSC ou home equity, seguir [`references/negociacao-dividas-superendividamento.md`](references/negociacao-dividas-superendividamento.md).
7. Salvar diagnóstico em `AAAA-MM-DD_DIAGNOSTICO-ENDIVIDAMENTO.md` na pasta mensal de comprovantes e/ou em `CARREIRA/mercado-salarial/evolucao/` se combinar com análise de carreira.

### Proposta de acordo recebida ou evento de negativação/protesto

Quando o Dr. Israel (ou qualquer credor) trouxer uma **proposta de acordo** para um cartão em negociação, ou quando surgir um evento de **negativação, protesto ou ação judicial**:

1. Não gerar um novo documento avulso — registrar direto em `~/MEGA/Comprovantes/ENDIVIDAMENTO.md`:
   - Proposta de acordo → seção 5 (tabela de propostas). Calcular **os dois percentuais de desconto**: sobre o saldo apresentado pelo credor (nominal) e sobre o valor de face original ago/26 (real, coluna "Valor ago/26" da seção 4). Nunca reportar só um dos dois.
   - Negativação/protesto/ação judicial → seção 6 (tabela de monitoramento).
2. Anexar/linkar o documento da proposta (nunca aceitar proposta verbal sem registro escrito).
3. Se a proposta for aceita ou o cartão for quitado, mover a linha da seção 4 para a 4.1 (quitados/absorvidos) e recalcular os totais da seção 1.
4. Atualizar `CONTROLES.md` se o status do cartão mudar.

### Cálculo do custo total CLT (para análise de margem de consultoria)

`custo_total_clt = salario_bruto × 1.65`

Fator 1.65 inclui: FGTS 8% + provisão 13º (~8.3%) + provisão férias + 1/3 (~11.1%) + INSS patronal + RAT + sistema S (~27–32%). Usar como estimativa conservadora para BPO/consultoria brasileira.

## Relatórios financeiros em PDF — paginação obrigatória

Para pareceres, planos financeiros e relatórios com muitas tabelas, Igor prefere uma diagramação limpa: **a tabela inteira deve ir para a página seguinte quando não couber no espaço restante**, em vez de ser dividida.

O fluxo completo de geração (pandoc → HTML → wkhtmltopdf com template CSS) e o template estão documentados em [`references/geracao-pdf-relatorios.md`](references/geracao-pdf-relatorios.md).

Checklist de qualidade antes da entrega:

1. No CSS de impressão, aplicar `page-break-inside: avoid !important` e `break-inside: avoid-page !important` em `table`, `thead`, `tbody` e `tr`.
2. Manter título/subtítulo junto da tabela ou bloco seguinte. Não confiar apenas em `page-break-after: avoid` do wkhtmltopdf; quando necessário, inserir quebra explícita antes da seção no Markdown.
3. Se mover a tabela inteira criar página quase vazia ou distribuição desequilibrada, dividir a tabela manualmente em um ponto lógico, inserir título de continuação e repetir o cabeçalho. O objetivo é preservar linhas inteiras **e** equilibrar visualmente as páginas.
4. Depois de cada alteração de paginação, renderizar **todas as páginas** em contact sheet e reinspecionar o documento inteiro, pois mover uma tabela altera todas as páginas seguintes.
5. Corrigir também títulos órfãos, uma única linha de checklist isolada, páginas quase vazias, cortes, sobreposição e contraste.
6. Só entregar depois de validar o texto extraído, caracteres quebrados, valores-chave e a última página.
7. Usar [`references/negociacao-dividas-superendividamento.md`](references/negociacao-dividas-superendividamento.md), seção “Geração de Markdown e PDF”, para o procedimento detalhado.

## Fluxo: fechamento mensal

1. Ler `INDEX.md` do mês, se existir.
2. Ler `AAAA-MM_00_CONTROLE_PAGAMENTOS.md` e `AAAA-MM_00_DIVIDA.md` — essa é a convenção vigente (documentada em `~/MEGA/Comprovantes/CLAUDE.md`), os dois devem ficar sincronizados: tudo em aberto na DIVIDA aparece no CONTROLE, tudo pago tem link de comprovante.
3. `AAAA-MM_CONTAS_FATURAS.md` é um padrão **legado**, usado só em `2026_01_JANEIRO` e `2026_02_FEVEREIRO` — não esperar esse arquivo em meses mais recentes; só ler se existir.
4. Rodar script de auditoria, quando disponível.
5. Listar pendências abertas.
6. Listar comprovantes sem origem.
7. Listar documentos sem `.md` correspondente.
8. Gerar resumo com totais e pontos de atenção.
9. Não marcar como concluído se houver pendência sem justificativa.

## Projeção de Negociação e Desconto Real para Cartões em Negociação

Quando o usuário solicitar projeção de **quando negociar** e **qual desconto vale a pena** para os cartões não pagos:

1. **Parâmetros Base:** Mapear o **Valor de Face Original** (o saldo real utilizado no momento do default, ex: Ago/2026), a taxa contratual de rotativo (ex: 18% a 21% a.m.) e o saldo contábil inflado.
2. **Ciclo PDD e Janelas Temporais:**
   - *0 a 90 dias:* Cobrança call center e bloqueio de limite. **Não negociar** (descontos ilusórios de 10% a 20%).
   - *120 a 180 dias:* Ofertas de parcelamento com juros embutidos. **Recusar**.
   - *280 a 360 dias (Janela de Ouro):* Provisão para Devedores Duvidosos (PDD) regulatória no BC. A instituição oferece quitação via Serasa Limpa Nome / Consumidor.gov.br com **80% a 92% de desconto nominal**.
   - *24 meses (Caso Inter):* Janela de liquidação estendida (ex: Agosto/2028), com quitação por fração mínima do CDB acumulado.
3. **Métrica de Desconto Real sobre Valor de Face:**
   - $\text{Desconto Real} = 1 - \frac{\text{Valor Final do Acordo}}{\text{Valor de Face Original}}$
   - **Regra de Ouro da Banca:** Nunca aceitar propostas cujo desconto nominal resulte em valor final acima do saldo de face original (desconto real negativo). A meta mínima aceitável é **Desconto Real > 40% a 60% sobre o dinheiro originalmente utilizado**.
4. **Atualizar Fichas:** Inserir a seção `## 🎯 Projeção de Negociação e Acordo com Desconto Real` com a matriz de 4 cenários (Desfavorável, Aceitável, Ótimo e Excelente) nas fichas individuais sob `_fichas/`.

## Cuidados operacionais

- Não apague originais financeiros em caso de dúvida.
- Para itens suspeitos/duplicados, prefira mover para pasta `REVISAR/` dentro do mês.
- Não registre tokens, senhas ou chaves em Markdown.
- Não invente OCR, IDs, datas ou valores.
- Sempre cite caminhos dos arquivos alterados.
- Quando fizer melhoria em agentes ou fluxo financeiro, registre em `/home/igorferreira/.hermes/docs/CHANGELOG.md`.

## Home equity / refinanciamento imobiliário — impacto no fluxo mensal

Quando o usuário mencionar recebimento de home equity com parcelas mensais:

1. **Antes de atualizar qualquer dossiê, localizar e extrair o contrato assinado** (CCB, Cédula de Crédito Bancário) — seguir [`references/extracao-ccb-contrato.md`](references/extracao-ccb-contrato.md) para técnica de extração e campos críticos.

1. **Calcular o fluxo pós-parcela imediatamente**: `margem_pós_HE = renda_disponível - custo_vida - parcela_HE`. Se negativo ou sem contingência adequada, declarar a operação insustentável antes de qualquer plano de quitação.
2. **Grace period**: se houver carência, tratá-la somente como janela temporária; não usar os meses sem parcela para mascarar a inviabilidade recorrente.
3. **Não converter risco sem garantia em risco sobre o imóvel para pagamento parcial**: o home equity só pode ser considerado depois de obter acordos globais escritos que encerrem as dívidas caras, preservem reserva e deixem fluxo mensal positivo.
4. **Revisão jurídica**: antes de recomendar contratação, exigir análise do CET, mora, alienação fiduciária/garantia, execução extrajudicial, seguros e hipóteses de vencimento antecipado por advogado habilitado.
5. **Distinguir quitação de refinanciamento**: pagar cartões com home equity quita os cartões, mas mantém dívida de longo prazo garantida pelo imóvel; não chamar isso de “ficar sem dívidas”.
6. **Impacto na rescisão**: o HE não aparece no TRCT, mas sua parcela reduz a cobertura pós-desligamento. Recalcular meses de sobrevivência com a parcela deduzida.
7. **Dívida declarada vs mapeada**: registrar ambos e nunca projetar uso do HE apenas sobre a parcela já documentada.

## Dissídio coletivo / CCT — registro e projeção

Quando o usuário mencionar dissídio anual:

1. **Verificar data-base da CCT nos contracheques extraídos** — procurar em `CARREIRA/rescisao-clt/analise/contracheques-extraidos.json` pelos registros mensais e identificar em qual competência o salário subiu em cada ano.
2. **Padrão FEAAC (Igor)**: data-base 1º de agosto, mas o reajuste historicamente reflete no contracheque de **outubro ou novembro** (1–3 meses de atraso). Não assumir que agosto = mês do contracheque com reajuste.
3. **O VALLO BENEFÍCIOS também reajusta junto com o dissídio** (confirmado por Igor) — ao projetar novo salário pós-dissídio, projetar o VALLO proporcionalmente com o mesmo percentual.
4. **Salvar projeção** em `CARREIRA/rescisao-clt/analise/HISTORICO-DISSIDIOS-PROJECAO.md` com: histórico de reajustes (competência, salário anterior, novo salário, %), projeção do próximo dissídio por cenário (IPCA 4%/5%/6%), impacto no fluxo mensal com e sem parcela HE.
5. **Atualizar `dados-contrato.json`** quando o contracheque com o reajuste chegar — campo `base_salary`, `monthly_salary`, `latest_payroll_period` e `last_updated`.

## Contratos de crédito — verificação contra documento assinado

Quando o usuário informar parâmetros de empréstimo/contrato verbalmente (home equity, CCB, financiamento):

1. **Nunca aceitar apenas a informação verbal para o dossiê.** Procurar ativamente o contrato assinado:
   - `~/MEGA/Documentos/Emprestimo/` — contratos, CCBs, simulações
   - `~/MEGA/Comprovantes/2026/_Emprestimos/` — registros de empréstimos consignados
   - Buscar por `*contrato*`, `*ccb*`, `*credito*` e extensões `.pdf` nos diretórios acima

2. **Extrair dados do contrato com `pdftotext`**: campos críticos são Principal, Valor Líquido, Prazo, Sistema de Amortização, Taxa de Juros (a.m./a.a.), Parcela Estimada (amortização + juros + seguros), Data da 1ª Parcela, Vencimento Final, CET.

3. **Confrontar com a informação verbal e reportar divergências explicitamente** — o contrato assinado prevalece. As discrepâncias comuns: principal (verbal inclui taxas financiadas vs. contrato que as detalha separadamente), número de parcelas, valor da parcela (verbal frequentemente omite seguros MIP/DFI), carência.

4. **Atualizar o dossiê com os dados do contrato**, não com a informação verbal não verificada.

## Relação VALLO × Home Equity (CCB 004505 — dados reais)

Dados extraídos do contrato assinado em 31/07/2026:

| | |
|---|---|
| 💜 VALLO BENEFÍCIOS | R$ 4.420/mês (recorrente, confirmado) |
| 🏠 Home Equity C6 (CCB 004505) | ⏳ Ago–Set/26: só seguro R$67,90 | Out/26: 1ª parcela completa ~R$4.334 (SAC 50m) |
| 💵 Sobra VALLO (início) | R$ 30,56 após seguro. A partir de Out/26 a sobra cresce com SAC |
| 📈 Crescimento da sobra | ~R$ 40/mês (SAC reduz a parcela) |

**Contrato**: Principal R$ 108.719,73 / Líquido R$ 100.000 / SAC 50m / 1,7% a.m. / Seguros R$ 68,47/mês.

**Regra**: VALLO paga Home Equity. CLT paga o resto. **Nunca somar CLT+VALLO como renda disponível única** — superestima em ~R$ 4.000/mês.

⚠️ **Confirmado em 05/08/2026:** O contrato (CCB 004505) tem carência de Ago–Set/26 (só seguro R$67,90) e 1ª parcela real em Out/26 (~R$4.334). Os valores do contrato são estimativas (cláusula 2.3). Sempre confrontar com o app do banco — ver `references/ccb-contrato-vs-app.md`.

Para o cronograma SAC completo de 50 parcelas, ver arquivo canônico `HOME-EQUITY.md` na raiz de `~/MEGA/Comprovantes/`.

## Análises financeiras (cenários, pedaladas, comparativos)

Quando o usuário pedir análise de cenários (ex.: "vale a pena pedalar?", "compara opção A vs B"), seguir [`references/analise-cenarios-pedaladas.md`](references/analise-cenarios-pedaladas.md).

Toda análise concluída deve ser salva em `~/MEGA/Comprovantes/YYYY/_Analises/AAAA-MM-DD_ANALISES-<TOPICO>.md` + PDF com a data no nome. Esta pasta é o histórico de decisões financeiras — permite consultar análises passadas sem refazê-las.

## Pitfalls

### PDF de fatura de banco brasileiro protegido por senha
Faturas de bancos como Bradescard (Amazon, Casas Bahia), Itaú e outros frequentemente chegam criptografadas com senha (ex: primeiros dígitos do CPF do titular).
- **Extração de Texto Direta:** Usar `pdftotext -upw <senha> -layout <input.pdf> <output.txt>`.
- **Descriptografia e Salvamento de Cópia Limpa:** Usar Python com `pypdf` no ambiente venv ativo (`python3.12 -c "import pypdf; ..."`):
  ```python
  import pypdf
  reader = pypdf.PdfReader('fatura_protegida.pdf')
  if reader.is_encrypted:
      reader.decrypt('SENHA')
  writer = pypdf.PdfWriter()
  for p in reader.pages:
      writer.add_page(p)
  with open('fatura_limpa.pdf', 'wb') as f:
      writer.write(f)
  ```
- Sempre salvar o PDF descriptografado na pasta mensal canônica para permitir leitura e geração de relatórios subsequentes sem bloqueio.

### Contracheque pode estar no INBOX com assunto com espaço, não na pasta dedicada
O e-mail do contracheque Noorden usa assunto "Noorden - Contra cheque - julho 2026" (com espaço em "Contra cheque"), e pode cair direto no INBOX em vez da pasta `@Pessoal/Negocios/Clientes/Noorden/Contra-Cheque`. Ao buscar, usar termos com e sem espaço (`contracheque`, `contra cheque`, `holerite`) e verificar tanto INBOX quanto a pasta dedicada.

### Painel/planilha XLSX editada com openpyxl: fórmulas perdem cache e células mescladas rejeitam escrita
⚠️ **PITFALL — já ocorreu em 11/11/2026:** ao editar um XLSX (ex.: `PAINEL_ACOMPANHAMENTO.xlsx`) com openpyxl:
- Fazer backup (`cp -n`) antes da primeira escrita da sessão.
- `wb.save()` descarta o cache de fórmulas; leitura posterior com `data_only=True` devolve `None`, e um teste que leia o valor calculado falha como se o dado tivesse sumido. Gravar VALORES diretos (painel vira estático) ou recalcular no LibreOffice antes de rodar o teste.
- Célula mesclada só aceita escrita na âncora da mescla (`m.min_row`/`m.min_col` do range); escrever em qualquer outra coordenada do range falha.

### Orçamento mensal: CLT paga contas, VALLO paga Home Equity
⚠️ **PITFALL — já ocorreu em 31/07/2026:** Somar CLT + VALLO como renda disponível única e usar o total para pagar tudo. O modelo correto, confirmado por Igor:
- **CLT líquido** (~R$ 9.300) → fixas + livres + cartões + C6
- **VALLO** (R$ 4.420) → Home Equity C6 (R$ 4.389, decrescente). Sobra ~R$ 31 no início, crescendo ~R$ 40/mês (SAC)
- Misturar os dois superestima a capacidade de pagamento em ~R$ 4.000/mês

### Informação verbal de contrato diverge do documento assinado
A memória do titular sobre parâmetros de contrato é frequentemente imprecisa. Exemplo real (CCB C6 nº 004505): verbal → principal R$ 120.000 / 58 parcelas / R$ 4.200 / carência 2 meses. Contrato → principal R$ 108.719,73 / 50 parcelas / R$ 4.389,44 (com seguros) / 1ª parcela 10/Set/2026. **Sempre buscar e extrair o contrato assinado antes de atualizar o dossiê.**

### App de cartão — \"fatura atual\" ≠ \"fatura fechada\" (BrasilCard e similares)

⚠️ **PITFALL — já ocorreu em 07/08/2026:** O app BrasilCard mostra simultaneamente uma \"Fatura fechada\" (R$ 673,65, vence 10/08) e uma \"Fatura atual\" (R$ 292,20, ainda aberta). A \"fatura atual\" é o período EM ANDAMENTO — não é a obrigação vincenda. A \"fatura fechada\" é a que realmente precisa ser paga.

Em apps que mostram ambas (BrasilCard, PAN, Bradescard, etc.):
- **Fatura fechada**: valor total, fechamento e vencimento já definidos → esta é a dívida real
- **Fatura atual/aberta**: lançamentos do ciclo atual, sujeito a alteração → NÃO usar como valor da dívida
- Sempre priorizar a fatura FECHADA. Se só existir a aberta, marcar como \"⬜ Em aberto — valor parcial\" e estimar o fechamento com base no ciclo anterior.

### CSV de extrato Nubank — formato português, sem total fechado
⚠️ **PITFALL — já ocorreu em 07/08/2026:** O Nubank exporta extrato como CSV com 3 colunas (date, title, amount) usando formato numérico português (ponto=milhar, vírgula=decimal, negativo com "- "). O CSV lista transações, NÃO é fatura fechada — o total do período é a soma das linhas. Parcelas vêm como `Parcela X/Y` no campo title. Para projetar: `restantes = Y - X`; `Y/Y` = última, não projeta. Pipeline completo em `references/processamento-csv-nubank.md`.

### Plano pode referenciar caminho de arquivo errado
⚠️ **PITFALL — já ocorreu em 07/08/2026:** O `PLANO-DOSSIE-MASTER-DETAIL.md` referenciava o arquivo CCB como `2. ccb - vnn.PDF.pdf` (Via Não Negociável). O arquivo real é `1. ccb - vn.pdf` (Via **Negociável**). Planos e dossiês são documentos vivos que podem conter paths desatualizados. **Antes de executar T1 de qualquer plano, verificar se o arquivo referenciado existe com `ls` ou `search_files` — não assumir que o path no plano está correto.**

### Informação verbal de valor de dívida pessoal pode estar errada
⚠️ **PITFALL — já ocorreu em 07/08/2026:** O valor da dívida pessoal com Paulo Guerra foi rastreado como R$ 3.175,46 por várias sessões até Igor corrigir: o valor real é R$ 10.000,00. O valor menor era uma estimativa de um pagamento parcial ou parcela, não a dívida total. **Sempre confirmar explicitamente o valor total de dívidas pessoais com o Igor**, especialmente quando o número não veio de um documento escrito (contrato, mensagem, comprovante).

### Valor verbal do usuário vs documento anexado — o documento prevalece no preenchimento
Quando Igor declara verbalmente um valor (ex.: reembolso, comprovante lido de foto) e o documento que ele anexou mostra outro (mesmo poucos centavos), usar o valor do DOCUMENTO no preenchimento da planilha/ficha e sinalizar a divergência na resposta antes de registrar — o documento é o que o destinatário (empresa, credor, RH) vai conferir. Registrado no arquivo/SESSION a divergência, nunca corrigir "por cima" do verbal em silêncio nem aceitar o verbal contra o recibo. Se ele insistir no verbal depois do aviso, registrar como user-provided.

### Fatura de cartão ativo pode revelar parcelamentos futuros não mapeados
⚠️ **PITFALL — já ocorreu em 07/08/2026:** A fatura do Itaú Signature (Set/26) revelou R$ 2.399,75 no mês + parcelamentos de R$ 233/190/160 em Out–Dez/26 que não estavam no fluxo de caixa. Cartões "pagos no mês" podem ter parcelamentos residuais que só aparecem na captura de "próximas faturas". **Ao receber a captura de qualquer fatura de cartão ativo, SEMPRE verificar o gráfico de próximas faturas na imagem e extrair TODOS os meses, não apenas o valor do mês corrente.**

### Atualização incremental do fluxo
Quando só uma ou duas faturas mudarem, calcule o delta para identificar os meses e cenários afetados, mas aplique-o às fontes/modelos vigentes e regenere pelo escritor oficial. Não use JSON intermediário ou saída antiga como fonte de produção, nem atualize projeções publicadas à mão. Confira as outras séries afetadas e as âncoras finais conforme [`references/fluxo-caixa-source-of-truth.md`](references/fluxo-caixa-source-of-truth.md).

### Empréstimo consignado com data de fim — recalcular projeções
⚠️ **PITFALL — já ocorreu em 05/08/2026:** Quando o usuário mencionar que um empréstimo consignado (folha de pagamento) tem data de término, **recalcular imediatamente o fluxo de caixa e as projeções do CONTRACHEQUE.md**. O impacto é +R$ X/mês a partir da data de fim, e isso pode estar ausente das projeções existentes.

- Conferir o horizonte vigente no arquivo canônico e verificar se a data de término está dentro dele.
- Recalcular a renda líquida a partir do mês seguinte ao término, adicionando a parcela que deixou de ser descontada.
- Atualizar a fonte de renda e os controles que realmente acompanham essa alteração; depois, gerar novamente a família e o dashboard pelos escritores oficiais aplicáveis.
- Reconciliar as âncoras afetadas e documentar a premissa, sem reutilizar valores projetados de versões antigas.

### Cache de imagens do Telegram / Hermes
Imagens enviadas via Telegram ficam em `~/.hermes/cache/images/img_<hash>.jpg` (uma cópia pode existir sob `~/.hermes/cache/documents/native-inputs/<sha256>/`). Este é o caminho vigente — se buscas por um caminho de cache antigo (`image_cache`, `media/inbound`) falharem, busque em `cache/images` antes de pedir reenvio. A primeira entrega de uma foto pode falhar por timeout; pedir reenvio em vez de prosseguir sem a imagem. O path é válido apenas na sessão em que a imagem foi recebida — em sessões posteriores o arquivo pode não existir mais. Antes de tentar usar `vision_analyze` ou copiar um path de cache antigo, verificar se o arquivo existe. Se não existir, pedir ao usuário para reenviar a imagem.

Quando houver várias imagens na mesma conversa, **não escolher apenas o arquivo mais recente do cache**. Prefira o caminho explícito anexado à mensagem ou ao bloco `Replied-to image ... saved at:` e mantenha cada captura vinculada à mensagem que a originou. Se descrição e pixels divergirem, não misture cartões/documentos: registre a divergência e peça confirmação.

### Himalaya (email CLI) — search syntax v1.2.0+

⚠️ **PITFALL — já ocorreu em 10/08/2026:** O himalaya v1.2.0+ usa uma sintaxe de busca posicional, não de flags. Os filtros (`from`, `subject`, `date`, `body`, `before`, `after`) são argumentos posicionais do QUERY, e as flags (`--page-size`, `--folder`) PRECISAM vir ANTES:

```bash
# ✅ CORRETO: flags primeiro, depois os filtros de busca
himalaya envelope list --page-size 10 subject keyword
himalaya envelope list --page-size 10 from noorden

# ❌ ERRADO: nunca usar dois-pontos — himalaya espera espaço após o filtro
himalaya envelope list "subject:keyword" --page-size 10

# ❌ ERRADO: nunca colocar --flags depois dos filtros — o parser trata como parte do query
himalaya envelope list subject keyword --page-size 10
```

Ao buscar emails da Noorden (contracheque, timesheet, comunicados), usar `from noorden` ou `subject planilha` com as flags antes.

### Due diligence de advogado para dívidas

Quando Igor estiver avaliando um novo escritório de advocacia para renegociação de dívidas, seguir o ciclo completo em [`references/due-diligence-advogado-dividas.md`](references/due-diligence-advogado-dividas.md):
- Fase 1: Coleta (OAB, Escavador, Jusbrasil, Reclame Aqui, CNPJ, mídia)
- Fase 2: Análise de honorários e projeção de custo
- Fase 3: Verificação de casos de sucesso (OCR dos PDFs)
- Fase 4: Tabela comparativa entre advogados
- Fase 5: Recomendação com checklist de segurança

### Extrato FGTS — modalidade saque-aniversário
Quando o extrato da Caixa mostrar lançamentos `SAQUE JAM - COD 60` ou `SAQUE DEP - COD 60`, há evidência de saques-aniversário no histórico; confirmar a modalidade atual antes de concluir.
- Na dispensa sem justa causa, quem permanece no saque-aniversário em regra saca a multa rescisória, não o saldo integral por motivo rescisório.
- `saldo total - saldo bloqueado` é apenas **saldo não bloqueado por diferença aritmética**; não chamar automaticamente de “saldo disponível para saque imediato”. A liberação depende da modalidade e hipótese legal.
- Calcular a multa de 40% pela base rescisória oficial da conta do empregador atual, não pelo total consolidado de contas antigas.
- Conta de empregador anterior integra o patrimônio FGTS, mas não a base da multa devida pelo empregador atual.
- Mudança para saque-rescisão, carência e liberações extraordinárias podem mudar; verificar a regra oficial vigente na data da análise.
- Nunca igualar “saldo FGTS” a “caixa recebido na demissão” sem separar multa, conta atual, contas antigas, bloqueio e modalidade.

### Pedaladas financeiras — não some com a dívida
Quando uma fatura é paga com outro cartão (RecargaPay, Digio, etc.), a dívida não desaparece — apenas muda de credor. Registrar sempre em `AAAA-MM_00_PAGAMENTOS_CRUZADOS.md` com: obrigação quitada, valor, como foi pago, onde vai reaparecer, comprovante.

### Conta fixa pode emitir DUAS faturas no mesmo mês — não tratar o vencimento como absoluto
⚠️ **PITFALL — ocorreu em 14/08/2026:** A Vivo gerou duas faturas no mesmo número de conta no mês de 08/2026 — venc **10/08** (R$ 102,23) e venc **21/08** (R$ 38,71) — mesmo com o vencimento padrão registrado como "dia 10 de todo mês". Ao receber contas fixas recorrentes (Vivo, Claro, Light, Naturgy):

- **Sempre olhar o vencimento na PRÓPRIA fatura/PDF**, não confiar no vencimento cadastrado — o provedor pode faturar duas competências no mesmo mês (ex.: 2ª via, reajuste, correção de ciclo, encargos).
- Tratar as faturas como **itens separados** no controle mensal (uma linha cada), com vencimento próprio e fonte de pagamento própria — podem ter sido pagas por meios diferentes (aqui: 99Pay e RecargaPay/Digio).
- Verificar se a 2ª via não indica cobrança duplicada/encargos; registrar para conferência com a operadora quando a ocorrência for atípica.
- Nomear arquivos com o vencimento real de cada fatura (ex.: `2026-08-10_FATURA-VIVO-R10223.pdf` e `2026-08-21_FATURA-VIVO-R3871.pdf`).

### Pagamento com cartão-em-negociação via intermediário — papel do cartão-fonte
⚠️ **PITFALL — ocorreu em 14/08/2026:** A 2ª fatura Vivo (R$ 38,71) foi paga via **RecargaPay** (Pix QR), mas o usuário informou que a fonte de crédito era o **cartão Digio**, que está em negociação (não será pago). O OCR/comprovante só mostra o intermediário (RecargaPay), não o cartão-fonte.

Regras:
- **Nunca atribuir a dívida ao intermediário** que aparece no comprovante — quando o usuário diz "paguei com o cartão X", a dívida vai para o cartão X (ver também a seção "Pix crédito via RecargaPay").
- O pagamento feito com um cartão-em-negociação **aumenta a posição daquele cartão** na ficha (`FICHA_CARTAO_DIGIO.md`), no `ENDIVIDAMENTO.md` e na soma dos cartões em negociação — é dívida que cresce, **não** renda nem caixa livre.
- Registrar o comprovante com sufixo identificando a fonte (ex.: `COMPROVANTE-RECARGAPAY`) e documentar no `.md` que a fonte de crédito é o cartão, conforme informado pelo usuário (dado user-provided, não provado pelo OCR).
- Recalcular em cascata: ficha do cartão-fonte → ENDIVIDAMENTO (totais de negociação) → AVISOS → controle mensal.

### Saldo confirmado pelo usuário prevalece sobre projeção derivada — sinalizar a divergência
Quando o usuário informa o saldo real de uma conta (ex.: 99Pay **R$ 520,19**) e ele diverge de uma projeção que você calculou (ex.: 10,40 + 900 − 102,23 = **R$ 808,17**):
- Usar o valor **confirmado** como fonte da verdade no `_saldos/SALDO_<BANCO>.md` — nunca "forçar a reconciliação" inventando origens para a diferença.
- Registrar a divergência explicitamente (valor, diferença em R$, "não detalhada; saldo real prevalece") e adicionar uma linha em `AVISOS.md` se a diferença for material (aqui, R$ 287,98).
- Oferecer olhar o extrato do app para reconciliar, mas não bloquear a atualização por causa da divergência.

### Nunca escreva somas, subtotais ou percentuais calculados de cabeça em documentos financeiros
Ao gerar qualquer documento financeiro com análise numérica (base factual, ficha, dossiê, análise de demonstrativo), calcular TODA soma, subtotal, percentual e divergência com código (`Decimal`), nunca de cabeça. Em demonstrativos com dezenas de linhas, o total mental erra por milhares de reais e o erro passa despercebido na releitura — o documento fica contaminado como se fosse auditoria. Ao final, conferir a soma das rubricas discriminadas contra o total declarado do documento-fonte e registrar qualquer divergência como **lacuna a esclarecer** (não como economia identificada nem como erro presumido da administradora) — a conferência é o detector, o código é a garantia.

### Valores provisionados são piso, não teto — sempre subestimam
Quando um cartão está listado como ⬜ \"obrigação parcial\" porque só se conhece o **principal de um pagamento** (ex.: \"R$ 1.176,11 do pagamento da Inter feito via Porto Seguro\"), esse valor é quase sempre **muito menor** que a fatura real. A fatura completa frequentemente inclui:
- saldo anterior não documentado (pode ser 3-5× o valor provisionado);
- taxas, encargos, parcelamentos ativos não mapeados;
- novas compras desde o último registro.

**Exemplos reais (28/07/2026):**
- Porto Seguro: provisionado R$ 1.176,11 → real R$ 6.791,92 (5,7×)
- PAN Méliuz: provisionado R$ 2.441,60 → real R$ 12.158,50 (5,0×)
- Digio: provisionado R$ 524,74 → real R$ 1.117,97 (2,1×)

**Regra:** nunca trate valor provisionado como \"já coberto\". Mantenha status ⬜ e priorize obter a fatura completa. Ao atualizar o dossiê com o valor real, recalcule imediatamente totais, déficit e projeções — o impacto pode ser de milhares de reais. **Se a diferença entre provisionado e real for maior que ~20%, registrar uma linha em `~/MEGA/Comprovantes/AVISOS.md`** (tipo 🔴 gasto fora do padrão) — é exatamente o tipo de evento que esse log existe para capturar.

### "Pagou o cartão X?" — sempre especificar o mês da fatura
⚠️ **PITFALL — já ocorreu em 07/08/2026:** Perguntar "pagou o Nubank?" sem o mês gerou confusão. O usuário respondeu "só paguei o que vencia em agosto" — a fatura de setembro (~R$ 5.025) não venceu ainda. Cartões ativos têm faturas mensais contínuas. Sempre listar mês a mês com vencimento: "Nubank ago (~05/08, R$ 5.865) — pagou? E Nubank set (~05/09, R$ 5.025) — futuro, não pago."

### Vencimento registrado pode estar errado — confirme na fatura real
O vencimento cadastrado no inventário/dossiê é **histórico e pode não corresponder ao ciclo atual**. Exemplos:
- Itaú Signature: cadastrado como 15/08, fatura real mostrou 03/08;
- BrasilCard: cadastrado como 10/08, fatura real mostrou vencimento 10/09 (ciclo seguinte).

**Regra:** ao receber a fatura real, o vencimento exibido no app **sempre prevalece** sobre o cadastro. Atualizar imediatamente dossiê, cronograma e projeções — especialmente se o vencimento real for **mais cedo** que o esperado (impacto no grupo de \"vencimento iminente\").

### VALLO BENEFÍCIOS (Igor)
Por determinação expressa de Igor: depósitos da VALLO BENEFÍCIOS **nunca entram na rescisão**, inclusive o depósito recebido junto ao 13º salário. A VALLO conta apenas como rendimento/recurso disponível do período em que for recebida. Não revisitar essa classificação nem sugerir reclassificação mesmo quando o pagamento coincidir com um evento remuneratório (13º, férias, etc.).
- Quando fizer melhoria em agentes ou fluxo financeiro, registre em `/home/igorferreira/.hermes/docs/CHANGELOG.md`.

### Transparência sobre estimativas no fluxo de caixa

⚠️ **PITFALL — já ocorreu em 05/08/2026:** Quando o usuário perguntar se o fluxo de caixa tem "todos os valores reais" ou demonstrar medo/preocupação com a confiabilidade das projeções, **nunca responder apenas com o número agregado**. Separar explicitamente:

- **CONFIRMADO (valor exato mês a mês):** cartões cujo cronograma de parcelamento foi extraído de ficha/OCR
- **ESTIMADO (só pico conhecido, cronograma real NÃO mapeado):** cartões onde só se sabe o valor máximo mas não o decaimento mensal

Apresentar como tabela com 3 colunas: Cartão, Pico, Meses afetados, Status. Se houver subestimação potencial conhecida, **declará-la com valor em reais e mês afetado** — o próprio fluxo de caixa deve conter um aviso sobre isso.

- O fluxo de caixa e os artefatos derivados vigentes (por exemplo, MD, JSON, CSV, XLSX e dashboard) incorporam os melhores números disponíveis. O problema é de **comunicação**: o usuário precisa saber o que é fato vs estimativa para dormir tranquilo (ou agir — pedindo os prints que faltam).

### Cenários de pagamento e playbook de execução

### Planilha de cenários

Quando o usuário pedir para comparar múltiplos cenários financeiros (ex.: "com e sem Pix 18×", "com e sem crédito extra"), criar uma planilha Excel com uma aba por cenário e uma aba Comparativo. Seguir [`references/criacao-planilha-cenarios.md`](references/criacao-planilha-cenarios.md) para a estrutura completa e o código openpyxl.

Quando a renda mudar (novo contracheque, VALLO com valor diferente), atualizar TODAS as abas programaticamente seguindo [`references/atualizacao-planilha-cenarios.md`](references/atualizacao-planilha-cenarios.md).

### Evolução do saldo (running balance)

Quando o usuário quiser visualizar o impacto de cada pagamento no saldo,
criar documento com tabela sequencial mostrando o saldo após cada débito,
com gráfico ASCII de barras. Incluir:

- Saldo inicial confirmado (conta corrente + CDB já transferido)
- Cada pagamento com: #, data, cartão/conta, app, débito, saldo resultante
- Gráfico de barras ASCII mostrando a curva de queda
- Saldo final e reserva livre

Seguir [`references/evolucao-saldo-running-balance.md`](references/evolucao-saldo-running-balance.md).

### Matriz de parcelamentos futuros (cartão a cartão)

⚠️ **PITFALL CRÍTICO — já ocorreu em 31/07/2026:** Assumir que as faturas atuais são tudo. Cada cartão pago hoje pode ter dezenas de parcelamentos futuros invisíveis que só aparecem no gráfico de "próximas faturas" do app. Se não forem mapeados, o orçamento estoura — o Cenário P foi inviabilizado por causa disso.

Antes de travar qualquer cenário, verificar se TODOS os cartões que serão
pagos têm seus parcelamentos futuros mapeados. Parcelamentos invisíveis na
fatura atual podem inviabilizar o orçamento dos meses seguintes.

**Regra:** para cada cartão ativo, solicitar print do gráfico de próximas faturas. Montar matriz mensal cruzada e cruzar com a projeção ANTES de travar.

Seguir [`references/matriz-parcelamentos-futuros.md`](references/matriz-parcelamentos-futuros.md): solicitar prints ao usuário um a um, extrair via OCR,
montar matriz mensal cruzada e cruzar com a projeção de folga.

### Cheque especial — modelar em projeções com saldo negativo

⚠️ **PITFALL — já ocorreu em 31/07/2026:** Projetar saldo negativo sem modelar o cheque especial. Quando o fluxo ficar negativo, o cheque especial do Nubank (~8% a.m.) entra automaticamente e os juros são capitalizados.

**Regra:** em toda projeção onde o fluxo ficar negativo, adicionar colunas "OD acumulado" e "Juros OD" (8% a.m. sobre o acumulado). O efeito composto é devastador — um déficit de R$ 10.000 vira R$ 15.000+ em 6 meses só de juros.

Quando o usuário pedir um "passo a passo", "como eu faço" ou "guia pra executar", criar um documento prático com:

- Saldo real confirmado (o que já está na conta vs. o que precisa transferir)
- Passo 0 HOJE (resgate CDB, concentração no Nubank)
- Blocos por data com tabela: #, Cartão, App, Valor
- Pedaladas em bloco separado com aviso de ordem
- Resultado final e seção de contingência

### Projeção de longo prazo (12-24 meses)

Quando o usuário estiver preocupado com a viabilidade de um compromisso financeiro ao longo do tempo, criar projeção mês a mês por 12-24 meses seguindo [`references/projecao-orcamento-24-meses.md`](references/projecao-orcamento-24-meses.md). Incluir redução SAC, dissídios anuais, início/fim de compromissos e gráfico de folga.

Quando o objetivo for acumular dinheiro para quitar dívidas negociadas (após 280 dias), seguir [`references/projecao-limpar-nome.md`](references/projecao-limpar-nome.md). Estender até dezembro do ano seguinte, simular quitação com desconto e mostrar o saldo pós-acordo.

### Tracking de cenários e análises

Quando forem gerados cenários comparativos (pedaladas, what-if), seguir [`references/analises-cenarios.md`](references/analises-cenarios.md) e o mecanismo de histórico já vigente no projeto. Não criar JSONs por versão nem tratar arquivos intermediários como fonte canônica sem confirmar que o fluxo atual os usa. A versão de produção só avança com dado confirmado, fonte canônica atualizada e geração pelo escritor oficial; ver [`references/fluxo-caixa-source-of-truth.md`](references/fluxo-caixa-source-of-truth.md).

### Cenário de pagamento — só essenciais (por banco)

Quando os parcelamentos futuros inviabilizarem o cenário de "pagar todos", o usuário pode optar por manter ativos apenas cartões de bancos estratégicos. Seguir [`references/cenario-essenciais-por-banco.md`](references/cenario-essenciais-por-banco.md). Identificar bancos essenciais, calcular reserva, projetar apenas os parcelamentos dos ativos e mostrar o impacto de jogar o restante para negociação.

### Negociação com credor pessoa física (amigo/familiar)

Quando o usuário tiver dívida com amigo e quiser propor parcelamento, seguir [`references/negociacao-parcelamento-amigo.md`](references/negociacao-parcelamento-amigo.md): calcular TIR real do parcelamento e demonstrar que a proposta é melhor para o credor que receber à vista e aplicar em 100% CDI. Incluir mensagem pronta para WhatsApp e respostas para objeções.

- [ ] O arquivo original foi salvo no mês correto.
- [ ] Existe `.md` correspondente quando aplicável.
- [ ] Metadados mínimos foram preenchidos ou marcados como `A confirmar`.
- [ ] Controle mensal foi atualizado quando necessário.
- [ ] Origem e comprovante foram linkados quando ambos existem.
- [ ] Nenhum arquivo real foi apagado sem autorização explícita.
- [ ] A resposta final cita os caminhos principais alterados.

## Templates disponíveis

- [`templates/extrato-fgts.md`](templates/extrato-fgts.md) — estrutura para documentar extrato FGTS com dados críticos rescisórios, histórico completo e alertas de modalidade.
- [`templates/diagnostico-endividamento.md`](templates/diagnostico-endividamento.md) — diagnóstico completo de endividamento para renegociação: resumo executivo, dívidas em aberto, auditoria de pagamentos, pedaladas ativas, limites de cartões e próximos passos.

## Referências

- [`references/relatorio-simplificado-cartoes.md`](references/relatorio-simplificado-cartoes.md) — cadastro auditável de cartões com três últimos dígitos, físico/virtual, datas, limites com data-base, cobertura, conflitos e paginação A4 paisagem.
- [`references/pesquisa-emissores-cartoes.md`](references/pesquisa-emissores-cartoes.md) — pesquisa oficial de emissores ausentes/conflitantes, separando marca, emissor jurídico, financiador do saldo e credor atual para negociação.
- [`references/fatura-fechada-captura-resumo.md`](references/fatura-fechada-captura-resumo.md) — tratamento de fatura fechada recebida apenas como tela-resumo: proveniência dos dados, contabilização, cascata de controles, proibição de projeção sem detalhamento e auditoria final.
- [`references/faturas-imagem-parcelamentos.md`](references/faturas-imagem-parcelamentos.md) — vinculação correta de múltiplas imagens, OCR + inspeção visual, correção de leitura `x/y`, pagamento/crédito anterior, projeções e cascata de atualização/auditoria.
- [`references/cartao-saldo-zero.md`](references/cartao-saldo-zero.md) — registro de cartão com saldo zero confirmado, separação entre evidência visual e declaração do titular, classificação no inventário e atualização dos controles sem alterar o total.
- [`references/auditoria-inventario-cartoes-provisoes.md`](references/auditoria-inventario-cartoes-provisoes.md) — inventário deduplicado de cartões, cobertura de faturas, piso documental, substituição de captura aberta, ajustes bruto/líquido e provisões que atravessam o ano.
- [`references/card-payment-proof-workflow.md`](references/card-payment-proof-workflow.md) — checklist para comprovantes de pagamento de cartão.
- [`references/endividamento-renegociacao.md`](references/endividamento-renegociacao.md) — estrutura de diagnóstico de endividamento e renegociação, pedaladas, priorização e eventos de liquidez.
- [`references/uso-estrategico-cartoes-negociacao.md`](references/uso-estrategico-cartoes-negociacao.md) — padrão de uso de limite de cartões de negociação para cobrir despesas essenciais e cheque especial antes do default.
- [`references/negociacao-dividas-superendividamento.md`](references/negociacao-dividas-superendividamento.md) — metodologia jurídica e financeira para planos de 24 meses, atraso planejado, Lei do Superendividamento, home equity, modelos de negociação e geração verificada de Markdown/PDF.
- [`references/lembrete-diario-vencimentos.md`](references/lembrete-diario-vencimentos.md) — estrutura e manutenção do lembrete automático diário no Telegram (script Python + JSON + cron no_agent).
- [`references/fatura-atraso-provisao-substituicao.md`](references/fatura-atraso-provisao-substituicao.md) — tratamento de fatura em atraso confirmado (🔴) e substituição de provisão parcial por fatura completa oficial, com cascata de atualização nos controles e validação.
- [`references/revisao-narrativa-dossie-juridico.md`](references/revisao-narrativa-dossie-juridico.md) — checklist de 6 pontos para revisão narrativa de dossiês jurídico-financeiros: contexto de boa-fé, pedido explícito, risco do ativo, premissa de fluxo, tom com o advogado, evidência documental.
- [`references/geracao-pdf-relatorios.md`](references/geracao-pdf-relatorios.md) — geração de PDF profissional com pandoc + wkhtmltopdf + CSS externo: regras anti-órfãos, detecção automatizada, encoding, ajuste de margem para página vazia.
- [`references/dossie-advogado-cartoes.md`](references/dossie-advogado-cartoes.md) — dossiê consolidado para advogado/negociação: tabela única de todos os cartões (ver `CONTROLES.md` para a contagem atual) com emissor, vencimento, fechamento, limite, dívida corrente e futura, status e cronograma. Documento vivo — atualizar conforme novos dados chegam.
- [`references/ocr-banking-apps.md`](references/ocr-banking-apps.md) — técnicas de OCR para screenshots de apps bancários brasileiros: varredura de PSM modes, estimativa por pagamento mínimo e pitfalls comuns.
- [`references/auditoria-cruzada-dossie.md`](references/auditoria-cruzada-dossie.md) — auditoria numérica cruzada: soma de pagos + não pagos = dívida total, cobertura de recursos, consistência de percentuais, pitfalls de estimativas agrupadas.
- [`references/controle-completo-cartoes-3-blocos.md`](references/controle-completo-cartoes-3-blocos.md) — controle visual de TODOS os cartões em 3 blocos (✅ a pagar / ❌ não pagos / 🟢 zerados) com coluna Origem do recurso, resumo de caixa e pitfalls de substring "PAGO".
- [`references/cenarios-financeiros-ab.md`](references/cenarios-financeiros-ab.md) — documento de comparação entre duas estratégias financeiras mutuamente exclusivas, com seções de itens comuns, comparativo final e indicadores-chave para decisão.
- [`references/criacao-planilha-cenarios.md`](references/criacao-planilha-cenarios.md) — criação de planilha Excel multi-abas com openpyxl para cenários financeiros: estrutura de cada aba, cores, variações entre cenários, pitfalls de ambiente.
- [`references/playbook-pagamentos.md`](references/playbook-pagamentos.md) — guia prático de execução de pagamentos com passo a passo por data, app e valor, ordem de pedaladas, checklist de preparação e seção de contingência.
- [`references/registro-lote-faturas.md`](references/registro-lote-faturas.md) — padrão para maratona de registro de múltiplas faturas na mesma sessão: ciclo atômico OCR → evidência → dossiê → controle → resumo, ordem de prioridade e pitfalls de fadiga de patch.
- [`references/pdf-encrypted-brazilian-banks.md`](references/pdf-encrypted-brazilian-banks.md) — decriptação de PDFs de fatura de bancos brasileiros (senha = 5 dígitos do CPF) usando pypdf/qpdf/pikepdf como fallback.
- [`references/atualizacao-planilha-cenarios.md`](references/atualizacao-planilha-cenarios.md) — atualização programática da planilha Excel de cenários financeiros com openpyxl quando renda ou valores de fatura mudam.
- [`references/projecao-limpar-nome.md`](references/projecao-limpar-nome.md) — projeção de longo prazo (até dez/ano+1) para acumular reserva e quitar acordos de dívidas negociadas após 280 dias.
- [`references/cenario-essenciais-por-banco.md`](references/cenario-essenciais-por-banco.md) — cenário de pagamento com redução a bancos estratégicos quando parcelamentos futuros inviabilizam pagar todos os cartões.
- [`references/negociacao-parcelamento-amigo.md`](references/negociacao-parcelamento-amigo.md) — proposta de parcelamento para credor pessoa física: cálculo TIR vs CDI, mensagem WhatsApp, objeções.
- [`references/fluxo-caixa-excel-markdown.md`](references/fluxo-caixa-excel-markdown.md) — nota de legado: não usar o método manual antigo para produção; aponta para o workflow canônico vigente em `fluxo-caixa-source-of-truth.md`.
- [`references/fluxo-caixa-source-of-truth.md`](references/fluxo-caixa-source-of-truth.md) — fonte da verdade em Markdown/YAML, procedimento do escritor oficial, regeneração do dashboard e verificação de artefatos/rotas.
- [`references/analise-risco-fluxo.md`](references/analise-risco-fluxo.md) — análise estruturada de risco do fluxo de caixa: 3 níveis (ALTO/MÉDIO/BAIXO), stress test, mitigações e ações imediatas. Usar quando o usuário perguntar "tem risco de não cumprir?" ou demonstrar preocupação.
- [`references/playbook-negociacao-cartoes.md`](references/playbook-negociacao-cartoes.md) — guia completo de negociação de cartões não pagos: agrupamento por emissor, canais de contato pesquisados, cronograma de 4 fases, simulação de acordos com desconto, checklist de segurança.
- [`references/cdb-ponte-deficit.md`](references/cdb-ponte-deficit.md) — padrão de exibição de meses com déficit cobertos pela reserva do CDB: tabela com colunas "CDB usou" e "CDB saldo", seção de alerta no topo, timeline visual ASCII. Usar em toda projeção de fluxo de caixa com meses negativos.
- [`references/controle-saldo-contas.md`](references/controle-saldo-contas.md) — estrutura `_saldos/` com um arquivo por conta bancária, OCR de prints de app, pitfalls de CDB vs conta corrente.
- [`references/fluxo-caixa-rescisao.md`](references/fluxo-caixa-rescisao.md) — fluxo de caixa preventivo pós-rescisão: cruza dados da CARREIRA (rescisão CLT) com o fluxo mensal (HE + custo de vida) para mostrar mês a mês quanto tempo cada cenário cobre e quando o dinheiro acaba.
- [`references/registro-gasto-restaurante-lazer.md`](references/registro-gasto-restaurante-lazer.md) — ciclo completo de gasto avulso em restaurante/lazer: OCR da notinha → cadastro do restaurante em Documentos/Restaurantes → comprovante no mês da fatura → atualização da ficha do cartão → cascata no orçamento (Pote 3 → CDB).
- [`references/auditoria-extrato-cartao-orcamento.md`](references/auditoria-extrato-cartao-orcamento.md) — procedimento completo para auditar extratos de lançamentos de cartão de crédito via OCR, segregação de parcelas antigas vs. novos gastos correntes, classificação orçamentária (Lazer L5 vs. Não-Lazer), cálculo de % de atingimento de metas e atualização de catálogo de restaurantes.
- [`references/varredura-completa-plano.md`](references/varredura-completa-plano.md) — 🆕 sequência de 14+ arquivos quando Igor disser "atualiza todo o plano". Ordem: saldos → controles mensais → canônicos → índices → fluxo de caixa.
- [`references/acordo-pagamento-planilha.md`](references/acordo-pagamento-planilha.md) — acordo de pagamento parcelado com amigo/credor informal: planilha xlsx formatada, compartilhamento via Insync/Google Drive, controle Markdown, tom de resposta amigável.
- [`references/projecao-acordos-desconto-real.md`](references/projecao-acordos-desconto-real.md) — metodologia completa de matemática financeira para projeção de acordos PDD (Res. BCB 4.966), cálculo de desconto real sobre o valor de face original e playbook de negociação via Serasa/Consumidor.gov.br.
- [`references/atualizacao-plano-completo.md`](references/atualizacao-plano-completo.md) — cascata de atualização de 14+ arquivos após múltiplas transações: ordem, checklist, pitfalls (pipes duplos em tabelas).
