---
name: reconciliacao-gastos
description: "Use ao conciliar gastos operacionais com faturas."
version: 0.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [conciliação, faturas, duplicidade, finanças]
    related_skills: [registro-supermercado, registro-comida-rua]
---

# Reconciliação de gastos

## Objetivo
Relacionar lançamentos operacionais a faturas, comprovantes e controles sem dupla contagem.

## Fluxo
1. Carregar combustíveis, supermercado, comida na rua e fontes financeiras disponíveis.
2. Normalizar datas, valores e descrições sem alterar originais.
3. Procurar candidatos por valor, data, estabelecimento, cartão e descrição.
4. Classificar como `conciliado`, `possível correspondência`, `possível duplicidade`, `aguardando fatura/detalhamento` ou `divergência`.
5. Igualdade de valor isolada nunca é prova suficiente.
6. Não apagar, marcar pago ou alterar lançamento sem evidência.
7. Produzir relatório com fontes, data e pendências.
8. Regenerar dashboard e executar testes.

Somente leitura sobre dados financeiros. Não executar pagamentos, transferências ou cancelamentos. Não expor credenciais ou identificadores completos.

## Saída
Informar analisados, conciliados, duplicidades, aguardando fatura, divergências, fontes e confirmações necessárias.
