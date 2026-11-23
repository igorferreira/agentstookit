---
name: registro-comida-rua
description: "Use ao registrar restaurante, lanchonete ou delivery."
version: 0.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [restaurante, delivery, ifood, alimentação]
    related_skills: [reconciliacao-gastos]
---

# Registro de comida na rua

## Fonte canônica
`~/MEGA/Documentos/financas_bancos/GASTOS-COMIDA-RUA.md`

## Categorias
Restaurante, lanchonete, iFood/delivery, refeição durante trabalho/deslocamento e refeição paga para terceiros.

## Fluxo
1. Extrair data, estabelecimento, tipo, valor, companhia e pagamento.
2. Preservar nota, print ou comprovante.
3. Usar `Não informado` nos campos ausentes.
4. Acrescentar linha sem apagar histórico.
5. Relacionar fatura/comprovante e sinalizar duplicidade.
6. Atualizar resumo mensal apenas com valores confirmados ou explicitamente informados.
7. Regenerar dashboard e executar testes.

Comida na rua não entra na lista de compras ou estoque. Não inferir companhia ou data relativa sem âncora. Não executar pedidos ou pagamentos.

## Saída
Informar lançamento, data, valor, classificação, fonte, duplicidade, total mensal e pendências.
