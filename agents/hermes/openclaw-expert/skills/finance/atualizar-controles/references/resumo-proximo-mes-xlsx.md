# Resumo do Próximo Mês no XLSX

Use este padrão quando Usuário pedir uma versão simplificada da planilha ou quiser ver o próximo mês primeiro.

## Decisão de arquitetura

Não criar uma segunda planilha independente. Adicionar `Resumo Próximo Mês` como **primeira aba** do workbook canônico, mantendo as abas detalhadas como fonte de cálculo. Isso evita duas fontes de verdade.

Se a alteração for somente estrutural/visual, criar a próxima versão do cenário e declarar explicitamente: **sem mudança numérica**.

## Conteúdo mínimo da primeira aba

1. Entradas previstas, separadas por fonte.
2. Faturas conhecidas/documentadas por cartão.
3. Provisão para cartões sem fatura fechada.
4. Total conservador de faturas usado no fluxo.
5. Home Equity, outros compromissos e imprevistos.
6. Saídas totais.
7. Déficit ou superávit do mês.
8. Uso planejado do CDB, sempre exibido como valor positivo.
9. CDB no fechamento do mês anterior, rendimento estimado, CDB após o mês, mínimo projetado e saldo final do horizonte.
10. Lista explícita do que falta confirmar.

## Regra: confirmado versus provisionado

Nunca apresentar como confirmado o valor que é apenas estimativa.

```text
Faturas conhecidas = soma das faturas individualizadas no controle mensal
Provisão pendente = total conservador do Fluxo Mensal − faturas conhecidas
Total modelado = faturas conhecidas + provisão pendente
```

A provisão deve indicar nominalmente os cartões pendentes e ser substituída quando as faturas fecharem. Faturas abertas devem ter aviso de que podem variar.

## Fórmulas e cores

- Valores documentados por cartão: inputs azuis, com comentário de fonte/data.
- Totais e cálculos: fórmulas pretas.
- Referências a outras abas: fórmulas verdes.
- O resumo deve apontar para `Fluxo Mensal` e `Inputs`; não duplicar hardcodes derivados.
- Exibir `Uso planejado do CDB = -Saldo_mês` quando o saldo for negativo, para o painel mostrar uma necessidade positiva e intuitiva.

## Ponte do CDB

A reconciliação deve ser visível:

```text
CDB após mês = CDB fechamento anterior × (1 + yield) − uso planejado do CDB
```

Adicionar check automático garantindo diferença zero entre essa ponte e o saldo calculado em `Fluxo Mensal`.

## Checks adicionais obrigatórios

Além dos checks existentes, incluir:

1. Entradas do resumo = entradas do mês em `Fluxo Mensal`.
2. Total de faturas do resumo = faturas do mês em `Fluxo Mensal`.
3. Ponte do CDB = zero após reconciliação.

Recalcular no LibreOffice e validar com `data_only=True`. Todos os checks antigos e novos devem permanecer `✅ OK`.

## Entregáveis sincronizados

Após atualizar o XLSX:

- salvar o arquivo canônico na raiz;
- preservar a versão em `fluxo_caixa/cenario_atual/X<n>_atual.xlsx`;
- atualizar MD, PDF e CSV correspondentes;
- comparar hashes ou bytes das cópias que devem ser idênticas;
- registrar o delta da versão no Markdown e em `AVISOS.md`.

## Auditoria visual do PDF

Não considerar o PDF concluído apenas porque foi gerado.

1. Renderizar todas as páginas como imagens.
2. Auditar cortes, sobreposições, barras de rolagem, tabelas estreitas, títulos órfãos e páginas quase vazias.
3. Para tabelas mensais largas, preferir A4 paisagem com CSS de impressão próprio.
4. Usar `thead { display: table-header-group; }` e `tr { page-break-inside: avoid; }`.
5. Regenerar e revisar novamente se houver qualquer defeito.

Uma página final parcialmente ocupada é aceitável se evita reduzir demais a legibilidade; cortes ou sobreposições nunca são aceitáveis.
