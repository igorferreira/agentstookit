---
name: registro-estoque-alimentos
description: "Use ao atualizar o estoque atual de alimentos."
version: 0.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [estoque, alimentos, compras]
    related_skills: [registro-supermercado]
---

# Registro de estoque de alimentos

## Fonte canônica
`~/MEGA/Documentos/financas_bancos/ESTOQUE-ALIMENTOS.md`

## Fluxo
1. Ler foto, mensagem ou conferência fornecida.
2. Registrar somente quantidade e unidade confirmadas.
3. Registrar data da conferência e observações de marca, validade e embalagem.
4. Só calcular suficiente, atenção ou esgotado quando existir estoque mínimo.
5. Sem mínimo, usar `Não informado`.
6. Nunca transformar ausência em zero.
7. Regenerar dashboard e executar testes.

Estoque atual não é compra do mês, preço ou consumo inferido. Não apagar histórico relevante.

## Saída
Informar data, itens atualizados, itens não identificados, níveis calculados, fonte e testes.
