# Endividamento e renegociação — referência

Use este documento quando o usuário pedir diagnóstico de endividamento, análise de renegociação ou consolidação de dívidas.

## Estrutura do diagnóstico

Produzir um `.md` com as seguintes seções, nesta ordem:

1. **Resumo executivo** — total em aberto, total pago no mês, renda líquida, relação dívida/renda, deficit mensal.
2. **Dívidas em aberto** — tabela por prioridade: vencimento, credor, valor, status (⬜/✅/⏳), referência.
3. **Auditoria de pagamentos** — tabela de tudo que foi pago no mês com comprovante.
4. **Pedaladas/pagamentos cruzados ativos** — o que foi quitado com outro limite e onde vai reaparecer.
5. **Cartões e limites** — mapa de todos os cartões com final, banco, limite total, utilizado e disponível.
6. **Análise para renegociação** — pontos críticos e tabela de prioridade por credor com argumento de renegociação.
7. **Recursos potenciais para amortização** — VALLO, home equity, rescisão, 13º, salário.
8. **Próximos passos** — lista `[ ]` acionável.

## Prioridade de renegociação

Usar esta ordem como padrão, ajustando pelo contexto do usuário:

1. Maior valor individual em aberto sem amortização visível.
2. Itens com juros correndo (cheque especial, cartão rotativo) — parar o sangramento primeiro.
3. Pedaladas ativas com instrumento de alto custo.
4. Parcelas fixas de menor valor — impacto menor por item mas relevante no agregado.

## Regras de totalização

- **Total em aberto** = soma das dívidas com status ⬜ ou ⏳ na seção 2.
- **Total pago no mês** = soma de todos os itens com comprovante na seção 3.
- Pedaladas ativas **não somam ao total em aberto** separadamente — estão dentro dos cartões credores que as absorveram; listar à parte para clareza.
- FGTS só entra como caixa de rescisão quando a modalidade e a hipótese legal permitirem. Em saque-aniversário, não inferir saque imediato pela simples diferença entre saldo total e bloqueado; separar multa rescisória, conta atual e contas antigas.
- VALLO nunca entra em nenhuma verba rescisória (ver regra na skill principal).

## Dívida declarada vs dívida mapeada

Quando o usuário declarar um total (e.g., R$ 150.000) que supera os documentos disponíveis:

- Registrar `dívidas_mapeadas` (itens com comprovante/extrato) separadamente de `dívidas_não_mapeadas` (saldo declarado − mapeado).
- Ao simular um evento de liquidez (e.g., home equity de R$ 100.000):
  1. Quitar todo o mapeado na ordem de prioridade.
  2. Aplicar o saldo remanescente do evento às não mapeadas.
  3. O que sobrar de dívida não mapeada = dívida residual do plano.
- Nunca simular como se o HE cobrisse apenas o mapeado e ignorasse o restante.
- Sempre pedir ao usuário para mapear gradualmente as dívidas não documentadas — listar todos os credores, valores e taxas.

## Simulação de home equity

Home equity converte dívida de consumo sem garantia em obrigação garantida pelo imóvel. Não executar algoritmo de quitação automaticamente.

Antes de considerar:

1. Calcular `margem_pós_HE = renda_disponível - custo_vida - parcela_HE` e exigir fluxo positivo com contingência.
2. Obter acordos globais escritos; não usar HE para pagar apenas a parcela mapeada e deixar cartões residuais.
3. Preservar reserva compatível com o risco do usuário.
4. Exigir revisão jurídica de CET, garantia/alienação fiduciária, mora, vencimento antecipado e execução.
5. Explicar que cartões podem ser quitados, mas a dívida total foi refinanciada e continua garantida pelo imóvel.
6. Tratar carência somente como janela temporária, nunca como solução do fluxo recorrente.

Para plano jurídico-financeiro, atraso negociado, descontos e superendividamento, seguir [`negociacao-dividas-superendividamento.md`](negociacao-dividas-superendividamento.md).

## Arquivo de saída

Salvar como:

```
AAAA-MM-DD_DIAGNOSTICO-ENDIVIDAMENTO.md
```

Na pasta mensal corrente. Atualizar quando novos itens forem informados pelo usuário.

## Pitfalls comuns

- Usuário pode informar valor total de empréstimo pessoal superior ao que aparece nos comprovantes de uso — usar o valor declarado pelo usuário como total da dívida.
- Fatura de cartão ainda aberta pode ter antecipações já aplicadas que não reduzem o valor exibido no app — registrar ambos.
- "Pago com cartão X" não significa dívida zerada — significa que mudou para o cartão X. Rastrear.
- Nunca tratar o diagnóstico como definitivo sem confirmar: saldo FGTS, cheque especial real, limites de todos os cartões pedalados.
- **Dívida emocional**: Usuário mencionou que o tema de dívidas é emocionalmente difícil. Aceitar informações graduais sem pressionar pela visão completa imediatamente. Integrar cada novo dado e mostrar como muda o plano, sempre com foco na saída possível.
