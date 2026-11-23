---
name: registro-supermercado
description: "Use ao registrar compras e preços de supermercado."
version: 0.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [supermercado, compras, preços, alimentos]
    related_skills: [registro-estoque-alimentos, reconciliacao-gastos]
---

# Registro de supermercado

## Fonte canônica
`~/MEGA/Documentos/financas_bancos/PRECO-SUPERMERCADO-REGISTRO.md`

## Fluxo
1. Preservar nota, foto, print ou mensagem original.
2. Extrair data, item, quantidade, unidade, preço, local e marca.
3. Separar alimentos da lista padrão, itens extras, limpeza e higiene.
4. Registrar apenas dados comprovados; ausências ficam como `Não informado`.
5. Acrescentar registros sem apagar histórico.
6. Atualizar histórico mensal e preço unitário quando possível.
7. Relacionar comprovante/fatura e sinalizar possível duplicidade.
8. Regenerar o dashboard e executar os testes.

## Lista padrão
- 6 kg peito de frango
- 4 kg patinho moído
- 30 ovos
- 6 kg arroz integral
- 4 kg feijão
- manteiga
- 1 kg açúcar
- 1 kg sal
- 1 garrafa de azeite

Compra de supermercado não é comida na rua nem consumo imediato do estoque. Não executar pagamentos.

## Saída
Informar arquivo, itens, total confirmado, campos ausentes, duplicidades, testes e pendências.
