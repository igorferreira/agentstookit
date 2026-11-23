# Auditoria de inventário de cartões e provisões futuras

Use este procedimento quando o usuário pedir para descobrir quantos cartões possui, verificar faturas de um mês, calcular a dívida mínima documentada ou provisionar parcelas futuras.

## 1. Escopo temporal

1. Defina o período histórico de varredura — normalmente os seis meses completos ou correntes anteriores.
2. Examine também a pasta do mês-alvo e documentos do mês anterior que mencionem vencimento futuro.
3. Leia inventários antigos, fichas individuais, controles mensais, arquivos de dívida e registros de pagamentos cruzados.

## 2. Contagem deduplicada

Conte **contas/produtos de cartão**, não todos os plásticos ou números encontrados.

- Cartão físico e virtual da mesma conta = uma conta.
- Finais diferentes vinculados explicitamente à mesma conta = uma conta.
- Produtos distintos do mesmo banco ou da mesma marca = contas separadas quando possuem faturas próprias.
- Empréstimos, contas bancárias e linhas de crédito sem cartão devem ser excluídos.
- Não trate nome semelhante como duplicidade sem emissor, final ou evidência relacional.

Apresente pelo menos:

- fichas cadastrais encontradas;
- itens excluídos e motivo;
- cartões/contas deduplicados;
- quantidade com evidência transacional no período;
- quantidade apenas cadastrada, sem fatura direta.

## 3. Matriz de cobertura do mês-alvo

Classifique cada cartão em uma destas categorias:

1. **Fatura completa/agregada localizada**;
2. **Obrigação parcial ou provisionada, sem fatura completa**;
3. **Nenhum valor do mês localizado**.

Regras:

- “Fatura não localizada” não significa saldo zero.
- Não invente fatura, taxa ou vencimento.
- Pagamentos cruzados devem aparecer como obrigação futura no cartão usado como fonte.
- Uma fatura agregada com cartão físico e virtual deve ser contada uma única vez.
- Informe quantos cartões permanecem sem fatura completa.

## 4. Total mínimo documentado

Calcule separadamente:

```text
subtotal de faturas completas/agregadas
+ subtotal de obrigações parciais/provisionadas
= dívida mínima documentada
```

Chame o resultado de **piso documental** quando ainda houver faturas ausentes ou abertas. Nunca apresente como total final definitivo.

## 5. Captura aberta substituída por fatura fechada

Quando chegar uma imagem mais recente:

1. Preserve a captura anterior como histórico.
2. Marque o Markdown antigo como `REGISTRO SUPERADO`, com link para a nova fatura.
3. Salve imagem original, PDF da imagem e Markdown da fatura fechada.
4. Atualize valor, vencimento, status e referência em dívida, checklist, índice e resumo anual.
5. Recalcule o delta entre captura aberta e fechamento e explique a decomposição do total.
6. Não marque como pago sem comprovante com sufixo `COMPROVANTE-PAGAMENTO`.

## 6. Valor bruto do aplicativo × ajuste informado pelo usuário

Se o aplicativo exibir um valor bruto que o usuário afirma conter uma competência anterior:

- preserve o valor bruto como evidência;
- registre separadamente o desconto determinado pelo usuário;
- calcule o valor líquido de planejamento;
- declare que a inclusão da competência anterior é informação do usuário quando a imagem não a comprovar;
- mantenha a fatura como aberta/provisória até o fechamento.

Exemplo de registro:

```text
valor bruto exibido
(-) competência anterior que será paga
= projeção líquida da nova competência
```

## 7. Identificação de parcela recorrente por conciliação

Uma diferença pode ser tratada como parcela recorrente somente quando:

1. a aritmética fecha exatamente entre projeção líquida e transações visíveis; e
2. o usuário confirma a natureza recorrente e o mês final.

Se qualquer uma dessas condições faltar, marque como `A confirmar` e não projete.

Mesmo com confirmação:

- não invente o número formal da parcela;
- registre o valor mensal, competências remanescentes, total remanescente e mês final;
- use datas de vencimento como referência quando não confirmadas;
- guarde a conciliação em um registro mestre sob `_Controle_Anual/`.

## 8. Provisões que atravessam o ano

Para cada competência futura:

1. atualizar `AAAA-MM_00_DIVIDA.md`;
2. atualizar `AAAA-MM_00_CONTROLE_PAGAMENTOS.md`;
3. atualizar `INDEX.md` do mês;
4. recalcular o total mensal a partir das linhas, não por substituição cega;
5. atualizar o resumo anual e `CONTRATADO_FUTURO`;
6. criar a estrutura do ano seguinte quando a obrigação atravessar dezembro;
7. incluir outras parcelas já contratadas no novo mês, sem limitar o controle à obrigação recém-informada.

Se o usuário disser que novas fotos não são necessárias para uma parcela fixa, registre essa regra no documento mestre. Ainda assim, solicitar nova evidência quando houver compra, estorno, tarifa, alteração de valor ou fechamento divergente.

## 9. Auditoria final

Verifique programaticamente:

- soma das linhas de cada mês = total do resumo;
- links relativos existentes;
- valor bruto, ajuste e líquido presentes nos documentos;
- PDFs contendo valores-chave e sem caracteres corrompidos;
- imagem copiada com hash idêntico ao original quando aplicável.

Verifique visualmente todas as páginas:

- sem linhas de tabela divididas;
- sem títulos órfãos;
- sem listas isoladas em outra página;
- sem páginas quase vazias;
- contraste e margens adequados.

Quando o mecanismo de PDF ignorar `break-inside`, divida a tabela manualmente no Markdown, insira quebra explícita e repita título e cabeçalho. Escolha o ponto de quebra pelo equilíbrio visual das páginas, não apenas pelo fato de a tabela caber.
