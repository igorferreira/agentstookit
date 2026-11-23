# Relatório simplificado de cartões

Use quando o usuário pedir uma visão cadastral de todos os cartões com emissor, finais, datas e limites.

## Objetivo

Produzir um relatório simples, auditável e sem exposição desnecessária de números de cartão. A unidade de contagem é a **conta/produto de cartão**; cartões virtuais vinculados não são novas contas.

## Fontes e precedência

1. Inventário anual consolidado.
2. Cadastro histórico de cartões.
3. Faturas e capturas mais recentes.
4. Confirmação explícita do titular.

Dados recentes e diretos prevalecem sobre cadastro histórico, mas conflitos devem ser preservados e explicados; nunca escolha silenciosamente um dos valores.

## Campos

Para cada conta, registrar:

- nome;
- banco/emissor;
- três últimos dígitos do físico/cadastrado;
- três últimos dígitos do virtual;
- dia habitual de vencimento;
- dia habitual de fechamento;
- limite total;
- limite disponível.

Use `—` ou `Não informado` quando não houver evidência. Nunca derive limite total de fatura + disponível sem prova de que essa é a regra da tela.

## Privacidade e tipagem dos finais

- Exiba somente os **três últimos dígitos** solicitados.
- Não classifique um final como físico ou virtual se a fonte não indicar o tipo; use nota de confirmação.
- Se houver troca ou conflito de finais, mostre ambos de forma concisa e explique em observação.
- Deduplicate físico e virtual da mesma conta; preserve produtos diferentes do mesmo emissor separadamente.

## Temporalidade

- Datas de vencimento/fechamento são dias habituais, não garantias para todos os meses.
- Identifique quando uma data vem de cadastro histórico e quando há evidência recente divergente.
- Limites são fotografias: marque a competência/data-base, pois compras, pagamentos e ajustes bancários os alteram.
- Limite disponível não é renda nem saldo em conta.

## Estrutura recomendada

1. título, data e escopo;
2. legenda (`—`, data-base dos limites);
3. tabela de cobertura por campo;
4. tabela principal;
5. observações sobre conflitos/incertezas;
6. fontes principais;
7. prioridades para próxima atualização.

Para inventários grandes, dividir a tabela manualmente em blocos lógicos, repetir cabeçalho e usar A4 paisagem.

## Validação determinística

Antes de entregar:

- conferir número de contas contra o inventário;
- conferir que cada linha tem o mesmo número de colunas;
- contar cobertura e ausências por campo;
- validar todos os links locais;
- extrair texto do PDF e procurar título, seções, quantidade de contas e valores-chave;
- confirmar que nenhum final com quatro ou mais dígitos foi exposto na tabela final.

## Auditoria visual do PDF

- Manter o título da seção junto da tabela com quebra explícita quando necessário.
- Verificar todas as páginas após cada alteração.
- Corrigir título órfão, tabela cortada, página quase vazia e item isolado.
- Inspecionar especialmente a última página: uma única palavra ou continuação curta no topo ainda é quebra ruim. Encurte a observação, mova o bloco inteiro ou insira quebra em ponto lógico.
- Só entregar quando tabelas e notas estiverem legíveis em escala normal.
