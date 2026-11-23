# Atualização de orçamento, reconciliação e PDF auditável

Use quando uma mesma solicitação mistura nova fatura, saldo de conta, gastos realizados, novo custo recorrente e recálculo do fluxo.

## 1. Classifique antes de lançar

Separe cada dado em uma destas classes:

1. **Valor documentado que substitui provisão** — trocar o status/proveniência, sem somar novamente.
2. **Realizado pontual** — afeta somente a competência em que ocorreu.
3. **Custo recorrente novo** — afeta a competência inicial definida e todos os meses seguintes.
4. **Status operacional sem valor** — por exemplo, cartão bloqueado; não inferir cancelamento, quitação ou fatura zero.
5. **Saldo observado** — prevalece como posição atual, mas exige reconciliação com o saldo anterior e movimentos conhecidos.

## 2. Regras contra invenção e dupla contagem

- Se uma fatura já estava provisionada pelo mesmo valor, converter `provisionado → documentado`; delta financeiro = zero.
- Se dois pagamentos foram informados juntos, mas o rateio por categoria não foi informado, registrar o bloco combinado e marcar `rateio a confirmar`.
- Não inferir beneficiário, causa de bloqueio, final do cartão, CET ou forma de pagamento.
- Se a competência inicial de um novo recorrente não for explícita, adotar a próxima competência ainda não realizada e declarar a premissa. Não duplicar o realizado do mês corrente.

## 3. Reconciliação de saldo observado

Calcule:

```text
saldo esperado = saldo anterior + entradas conhecidas − saídas conhecidas
diferença não conciliada = saldo observado atual − saldo esperado
```

- O saldo atual confirmado pelo usuário prevalece para a posição corrente.
- Registre a diferença como **não detalhada**; nunca crie uma operação de ajuste fictícia.
- Preserve os movimentos informados individualmente e o ponto de observação atual.

## 4. Cascata mínima de atualização

1. Preservar a evidência original; gerar OCR bruto e Markdown normalizado.
2. Atualizar pasta mensal, controle de pagamentos e dívida mensal.
3. Atualizar ficha do cartão/conta e índices.
4. Atualizar orçamento realizado, orçamento recorrente e mapa de custo de vida.
5. Criar cenário X(n+1), mantendo o anterior.
6. Recalcular XLSX com LibreOffice em diretórios separados.
7. Regenerar CSV, Markdown e PDF a partir do XLSX recalculado.
8. Atualizar `AVISOS.md`, `CONTROLE_INDICE.md`, `PEDIDOS.md` e qualquer cópia legada ainda consumida por skills.
9. Auditar fórmulas, checks, totais, hashes e PDF visualmente.

## 5. PDF financeiro apresentável

Não confiar apenas em `pdfinfo` ou `pdftotext`. Renderize todas as páginas em imagens e faça auditoria visual.

### Problemas que obrigam regeneração

- título ou subtítulo órfão no fim da página;
- tabela quebrada sem repetir cabeçalho;
- colunas fora das margens;
- página vazia/quase vazia;
- fundo escuro ou transparência que prejudica notas e rodapés;
- sobreposição, cortes ou fonte ilegível.

### Padrão robusto

Para relatórios longos, prefira HTML com paginação controlada:

- página 1: resumo executivo + indicadores + evidências;
- páginas intermediárias: fluxo mensal em blocos, cada tabela com `<thead>` próprio;
- última página: checks e rastreabilidade;
- CSS com `@page { size: A4 landscape; }` e `html, body, section { background: #fff !important; }`;
- usar `wkhtmltopdf --background`; não usar `--no-background` quando o CSS depende de fundo branco e preenchimentos claros.

Depois:

1. `pdfinfo` confirma tamanho e páginas;
2. `pdftotext -layout` confirma conteúdo-chave;
3. renderizar páginas (`pdftoppm`) e montar folha de contato;
4. auditar visualmente página por página;
5. só entregar após status **APROVADO**.

## 6. Checks mínimos do modelo

- todas as linhas derivadas continuam fórmulas;
- todos os checks retornam OK/TRUE;
- novo recorrente aparece como named range/input com comentário de fonte;
- fatura convertida de provisão não alterou o total;
- CDB após o próximo mês, mínimo projetado e saldo final reconciliam;
- cópias canônicas e legadas intencionalmente mantidas estão sincronizadas.