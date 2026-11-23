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

## Benefícios não salariais (VALLO e similares)

Quando o usuário mencionar depósitos de pacotes de benefícios como VALLO BENEFÍCIOS:

- **Nunca incorporar ao salário, rescisão, FGTS, aviso-prévio, férias ou 13º** — nem o depósito habitual nem o depósito recebido junto ao 13º.
- Registrar exclusivamente como **rendimento/recurso disponível do período** em que o depósito ocorrer.
- Não projetar o valor para meses futuros sem confirmar data e recorrência documentalmente.
- Se o usuário afirmar que o benefício "não entra na rescisão", registrar isso como regra fixa no `dados-contrato.json` com campo `user_confirmed_exclusion_from_termination: true` e nunca revisitar sem solicitação explícita.

## Fluxo: fatura em aberto (não comprovante)

Quando o usuário enviar o print de uma **fatura ainda não fechada** (e.g. fatura de cartão em andamento):

1. Criar `.md` descritivo com o valor acumulado até aquele momento, vencimento provável, cartões vinculados e limite disponível.
2. Nomear sem sufixo `COMPROVANTE-PAGAMENTO` — usar sufixo descritivo como `FATURA-CARTAO-X-AGOSTO-RABERTO`.
3. Adicionar à seção "Em aberto" de `AAAA-MM_00_DIVIDA.md` com status ⬜ e nota de que o valor pode crescer.
4. Quando houver antecipações já aplicadas a essa fatura (pedaladas anteriores), registrá-las explicitamente no arquivo e descontá-las do saldo disponível, mas **não** subtrair do valor em aberto (que é o que o app exibe).
5. Comprovante de pagamento da fatura será um arquivo separado quando ocorrer.

## Pedaladas e pagamentos cruzados

Quando um pagamento for feito com limite de **outro cartão** (via RecargaPay, outro cartão, intermediário):

- Registrar em `AAAA-MM_00_PAGAMENTOS_CRUZADOS.md`: obrigação quitada, valor, instrumento usado, onde vai reaparecer e link do comprovante.
- A obrigação original some do credor, mas **reaparece na próxima fatura do instrumento usado** — rastrear explicitamente.
- Nunca marcar como "quitado sem rastro" — sempre registrar o "onde vai aparecer depois".
- Atualizar a seção "Próximo passo" no arquivo de pedaladas com `[ ]` pendentes para conferência quando as faturas posteriores fecharem.
- Para diagnóstico de endividamento: listar pedaladas ativas separadamente do total em aberto, pois representam dívida que mudou de endereço mas não foi amortizada.

## Mapa de custo de vida

Usuário mantém um **mapa canônico de custo de vida** em dois lugares idênticos (sincronizar ambos ao atualizar):

- `~/MEGA/Comprovantes/MAPA-CUSTO-VIDA.md` ← pasta financeiro
- `~/MEGA/Documentos/carreira/MAPA-CUSTO-VIDA.md` ← pasta carreira

Quando o usuário perguntar "qual meu custo de vida?" ou "quanto gasto por mês?":
1. Ler o arquivo acima — não recalcular do zero.
2. Apresentar: fixas mapeadas + custo declarado + gap variável.
3. Se houver nova despesa informada, atualizar ambos os arquivos.

**Valores atuais (corrigidos em 25/07/2026):**
- Fixas mapeadas e somadas: R$ 3.916,61/mês
- Teto de custo de vida confirmado por Usuário: R$ 4.000/mês
- Folga dentro do teto: R$ 83,39
- Parcelamentos e faturas de cartão pertencem ao plano de dívidas, não ao custo fixo

**Composição das fixas:**
| Categoria | Itens | Total |
|---|---|---:|
| Moradia | Condomínio | R$ 1.019,73 |
| Energia | Light (média 12m) | R$ 1.197,95 |
| Gás | Naturgy | R$ 121,32 |
| Telefone | Claro + Vivo | R$ 430,90 |
| Academia | Smartfit + Karatê + Crossfit | R$ 439,00 |
| IA (4 assinaturas) | ChatGPT + Gemini + Claude + Manus | R$ 407,69 |
| Transporte | Combustível | R$ 300,00 |
| Alimentação | VR/VA R$650 — cobre o custo | R$ 0,00 |

**Assinaturas de IA (todos planos básicos/pro entry, em USD):**
- ChatGPT Plus: $20/mês
- Gemini Advanced (Google One AI Premium): $19,99/mês
- Claude Pro: $20/mês
- Manus Pro Entry: $20/mês
- Total: ~$79,99/mês (converter pela cotação atual ao atualizar o mapa)

## Diagnóstico e estratégia de dívida

### Fonte obrigatória de salário, benefícios e custo de vida

Antes de calcular qualquer plano de dívida para Usuário:

1. Ler o **contracheque mensal normal mais recente** em `CARREIRA/rescisao-clt/contracheques/`; evitar férias, 13º, complemento CCT e eventos extraordinários como referência recorrente.
2. Separar explicitamente:
   - salário-base;
   - parcela fixa/CCT;
   - remuneração CLT bruta;
   - INSS, IRRF e empréstimo em folha;
   - salário CLT líquido em conta;
   - VALLO e outros benefícios como recursos separados, nunca como salário ou verba rescisória.
3. Ler o mapa canônico `~/MEGA/Comprovantes/MAPA-CUSTO-VIDA.md` e seu espelho em CARREIRA.
4. **Recalcular a soma das linhas** do mapa; não confiar cegamente no total escrito. Se houver divergência, corrigir os dois espelhos e registrar a data.
5. Usar o teto de custo confirmado pelo usuário uma única vez no fluxo. Se os fixos forem menores que o teto, mostrá-los como informação “incluída no teto”, sem subtrair fixos e teto cumulativamente.
6. Parcelamentos e faturas de cartão pertencem ao plano de dívida; não inflar o custo de vida somando-os novamente.
7. Quando renda ou custo forem corrigidos, recalcular todos os cenários, home equity e a própria qualificação de superendividamento. Não preservar uma conclusão jurídica produzida por premissas antigas.
8. Distinguir **meta negocial** de **teto absoluto**: a meta preserva folga e busca desconto; o teto é a prestação máxima matemática antes de exigir nova revisão.

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

### Cálculo do custo total CLT (para análise de margem de consultoria)

`custo_total_clt = salario_bruto × 1.65`

Fator 1.65 inclui: FGTS 8% + provisão 13º (~8.3%) + provisão férias + 1/3 (~11.1%) + INSS patronal + RAT + sistema S (~27–32%). Usar como estimativa conservadora para BPO/consultoria brasileira.

## Relatórios financeiros em PDF — paginação obrigatória

Para pareceres, planos financeiros e relatórios com muitas tabelas, Usuário prefere uma diagramação limpa: **a tabela inteira deve ir para a página seguinte quando não couber no espaço restante**, em vez de ser dividida.

1. No CSS de impressão, aplicar `page-break-inside: avoid !important` e `break-inside: avoid-page !important` em `table`, `thead`, `tbody` e `tr`.
2. Manter título/subtítulo junto da tabela ou bloco seguinte. Não confiar apenas em `page-break-after: avoid` do wkhtmltopdf; quando necessário, inserir quebra explícita antes da seção no Markdown.
3. Depois de cada alteração de paginação, renderizar **todas as páginas** em contact sheet e reinspecionar o documento inteiro, pois mover uma tabela altera todas as páginas seguintes.
4. Corrigir também títulos órfãos, uma única linha de checklist isolada, páginas quase vazias, cortes, sobreposição e contraste.
5. Só entregar depois de validar o texto extraído, caracteres quebrados, valores-chave e a última página.
6. Usar [`references/negociacao-dividas-superendividamento.md`](references/negociacao-dividas-superendividamento.md), seção “Geração de Markdown e PDF”, para o procedimento detalhado.

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

## Home equity / refinanciamento imobiliário — impacto no fluxo mensal

Quando o usuário mencionar recebimento de home equity com parcelas mensais:

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
2. **Padrão FEAAC (Usuário)**: data-base 1º de agosto, mas o reajuste historicamente reflete no contracheque de **outubro ou novembro** (1–3 meses de atraso). Não assumir que agosto = mês do contracheque com reajuste.
3. **O VALLO BENEFÍCIOS também reajusta junto com o dissídio** (confirmado por Usuário) — ao projetar novo salário pós-dissídio, projetar o VALLO proporcionalmente com o mesmo percentual.
4. **Salvar projeção** em `CARREIRA/rescisao-clt/analise/HISTORICO-DISSIDIOS-PROJECAO.md` com: histórico de reajustes (competência, salário anterior, novo salário, %), projeção do próximo dissídio por cenário (IPCA 4%/5%/6%), impacto no fluxo mensal com e sem parcela HE.
5. **Atualizar `dados-contrato.json`** quando o contracheque com o reajuste chegar — campo `base_salary`, `monthly_salary`, `latest_payroll_period` e `last_updated`.

## Pitfalls

### Cache de imagens do Telegram / Hermes
Imagens enviadas via Telegram ficam em `~/.hermes/image_cache/img_<hash>.jpg`. O path é válido apenas na sessão em que a imagem foi recebida — em sessões posteriores o arquivo pode não existir mais. Antes de tentar usar `vision_analyze` ou `cp` com um path de cache antigo, verificar se o arquivo existe com `ls -la <path>`. Se não existir, pedir ao usuário para reenviar a imagem.

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

### VALLO BENEFÍCIOS (Usuário)
Por determinação expressa de Usuário: depósitos da VALLO BENEFÍCIOS **nunca entram na rescisão**, inclusive o depósito recebido junto ao 13º salário. A VALLO conta apenas como rendimento/recurso disponível do período em que for recebida. Não revisitar essa classificação nem sugerir reclassificação mesmo quando o pagamento coincidir com um evento remuneratório (13º, férias, etc.).
- Quando fizer melhoria em agentes ou fluxo financeiro, registre em `/home/usuario/.hermes/docs/CHANGELOG.md`.

## Verificação antes de finalizar

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

- [`references/card-payment-proof-workflow.md`](references/card-payment-proof-workflow.md) — checklist para comprovantes de pagamento de cartão.
- [`references/endividamento-renegociacao.md`](references/endividamento-renegociacao.md) — estrutura de diagnóstico de endividamento e renegociação, pedaladas, priorização e eventos de liquidez.
- [`references/negociacao-dividas-superendividamento.md`](references/negociacao-dividas-superendividamento.md) — metodologia jurídica e financeira para planos de 24 meses, atraso planejado, Lei do Superendividamento, home equity, modelos de negociação e geração verificada de Markdown/PDF.
