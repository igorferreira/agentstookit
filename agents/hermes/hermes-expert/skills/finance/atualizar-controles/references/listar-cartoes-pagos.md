# Listar cartões pagos — reconciliação por competência

Use quando Igor pedir “cartões pagos”, “total pago em cartões” ou equivalente.

## 1. Fixar escopo antes da soma

Declare no resultado:

- **competência** da fatura (ex.: agosto/2026);
- **data de corte** do levantamento;
- se o número representa **faturas liquidadas**, **dívida eliminada** ou **histórico acumulado**.

Por padrão, interpretar como **faturas da competência mais recente com pagamento documentado**, não como todo o histórico do cartão.

## 2. Hierarquia de evidências

Use nesta ordem:

1. comprovante de pagamento/transferência visível;
2. controle mensal `AAAA-MM_00_CONTROLE_PAGAMENTOS.md` com link para comprovante;
3. ficha individual do cartão;
4. `CONTROLE_FATURAS_MANTIDOS.md`;
5. `ENDIVIDAMENTO.md`, dossiês e playbooks antigos apenas como apoio.

Se as fontes divergirem, não escolher silenciosamente. Reconcilie cartão por cartão e registre a diferença.

## 3. Classificação obrigatória

### A. Mantidos com fatura paga

Cartões ativos/mantidos cuja fatura daquela competência foi liquidada. Parcelamentos futuros podem continuar.

### B. Pagos por cross-payment / absorvidos

A obrigação do cartão de origem foi liquidada, mas a dívida migrou para o cartão-fonte. Mostrar separadamente e identificar o destino da dívida.

### C. Zerados/cancelados sem pagamento no período

Não entram no valor pago. Um cartão com saldo R$ 0,00 não prova desembolso na competência.

### D. Abertos, futuros ou em negociação

Não entram como pagos, mesmo que apareçam em fichas ou projeções.

## 4. Regras de inclusão

- Um cartão aparece **uma única vez** por competência.
- Use o **valor efetivamente pago**, não o valor aberto atual nem o saldo total utilizado.
- Não incluir dívida pessoal, conta fixa, empréstimo ou transferência entre contas.
- Não somar cartão absorvido duas vezes: uma vez como origem quitada e novamente como aumento da fonte.
- Se uma operação quitou apenas parte da fatura, classificar como **pagamento parcial**, não como cartão pago integralmente.
- PicPay/absorções sem comprovante mensal explícito podem ser listados somente como “absorvido conforme ficha/playbook”, com nível de evidência declarado; não apresentá-los como desembolso bancário comprovado.

## 5. Verificação numérica

Calcule mecanicamente:

```text
subtotal_mantidos = soma dos valores pagos do grupo A
subtotal_absorvidos = soma dos valores liquidados no grupo B
total_faturas_liquidadas = subtotal_mantidos + subtotal_absorvidos
```

Depois valide:

- quantidade de linhas = quantidade declarada;
- soma das linhas = subtotal de cada grupo;
- subtotais = total geral;
- o total do controle antigo foi recalculado se um cartão pago estava omitido (ex.: cartão reativado ou fatura pequena).

## 6. Formato de resposta

1. título com competência e data de corte;
2. tabela “Mantidos pagos”;
3. tabela “Pagos/absorvidos”;
4. resumo com quantidade e três totais;
5. aviso curto: **fatura liquidada não é necessariamente dívida eliminada**;
6. lista de valores abertos/futuros excluídos, quando houver risco de confusão.

## 7. Pitfalls observados

- Um snapshot de ativos pode omitir cartão com fatura pequena já paga; recalcular pelas linhas e não confiar no total escrito.
- “Quitado” pode significar cartão zerado, enquanto parcelamentos continuam em outro cartão.
- Uma captura de fatura aberta da competência seguinte nunca entra no total pago da competência anterior.
- Cross-payment melhora o status do credor de origem, mas não reduz o endividamento agregado na mesma proporção.
