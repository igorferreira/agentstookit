# Fatura fechada recebida como captura-resumo

Use este procedimento quando a imagem do aplicativo comprovar o total fechado e o vencimento, mas não trouxer a lista de compras nem a composição da fatura.

## Classificação da evidência

Separe explicitamente três fontes:

1. **Visível na captura:** valor fechado, vencimento, limite, bandeira, status e nome exibido.
2. **Cadastro/inventário local:** emissor, final já conhecido e deduplicação da conta.
3. **Declaração do titular:** competência, ausência de parcelamentos, associação do print a determinado cartão ou qualquer contexto não visível.

Nunca apresente um dado do inventário ou do usuário como se estivesse nos pixels. Exemplo: `Final exibido: não visível` e `Final associado pelo inventário local: 3825`.

## Arquivos obrigatórios

Preserve, com o mesmo nome-base:

- original `.jpg`, `.png` ou `.pdf`;
- OCR bruto `.ocr.txt`;
- Markdown canônico `.md`;
- PDF da imagem;
- PDF pesquisável derivado do Markdown, com sufixo `-RELATORIO-OCR.pdf` quando o PDF da imagem já ocupar o nome-base.

No Markdown, inclua:

- resumo dos dados comprovados;
- dados não visíveis;
- fonte de cada dado contextual;
- tratamento nos controles;
- OCR bruto, sem apagar os erros originais;
- correções feitas por inspeção visual;
- links relativos para todos os artefatos.

Valores publicitários visíveis na tela não são encargos. Registre a distinção quando o OCR puder confundi-los com a fatura.

## Contabilização mensal

Uma captura que mostre explicitamente **fatura fechada + total + vencimento** pode cobrir o valor mensal da conta no diagnóstico, mesmo sem detalhamento das compras. Registre, porém, a limitação de auditoria por item.

Atualize em cascata:

1. `AAAA-MM_00_DIVIDA.md`;
2. `AAAA-MM_00_CONTROLE_PAGAMENTOS.md`;
3. `INDEX.md`;
4. diagnóstico consolidado do mês;
5. inventário anual de cartões;
6. resumo anual da dívida.

Ao mover a conta de `sem informação localizada` para `fatura fechada localizada`:

- aumente a quantidade de faturas localizadas;
- reduza a quantidade sem informação;
- reduza a quantidade sem posição suficiente;
- atualize subtotal, piso documental e textos narrativos;
- remova o cartão da lista numerada e renumere os itens restantes.

A fatura permanece **em aberto** até existir comprovante de pagamento. Não use o sufixo `COMPROVANTE-PAGAMENTO` para a captura da fatura.

## Projeções futuras

Não projete setembro ou meses seguintes apenas a partir do total fechado. Sem linhas `x/y`, documento relacionado ou confirmação explícita do titular, não há base para separar parcelamentos, compras recorrentes, tarifas ou lançamentos à vista.

## Reconciliação e verificação

1. Releia os arquivos atuais antes de editar; controles podem ter sido modificados por outro fluxo.
2. Recalcule o total a partir das linhas incluídas, não apenas somando ao total escrito.
3. Valide a soma das faturas completas e das obrigações parciais separadamente.
4. Procure totais e contagens antigas em resumo, índice, notas e prioridades documentais.
5. Valide todos os links relativos.
6. Extraia texto dos PDFs e confirme valor, vencimento e identificação.
7. Renderize todas as páginas em contact sheet e corrija tabelas divididas, títulos órfãos, itens isolados e páginas quase vazias.
8. Após qualquer correção textual no relatório, regenere e reinspecione o PDF final.
