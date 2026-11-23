# Criação de Planilha de Cenários Financeiros com openpyxl

Quando o usuário pedir para criar uma planilha Excel com múltiplos cenários financeiros comparativos.

## Estrutura da planilha

### Abas
- Uma aba por cenário (`Cenário A`, `Cenário B`, etc.)
- Uma aba `Comparativo` com tabelão lado a lado

### Conteúdo de cada aba de cenário

Seções em ordem, cada uma com cabeçalho escuro (`1F2937`):

1. **💰 RECURSOS** — fontes de dinheiro (CDB, renda, créditos extras, pedaladas), com coluna Tipo (Caixa / Pedalada)
2. **⬜ PAGAMENTOS — CDB** — lista de cartões/contas pagos do CDB em 01/08
3. **🦶 PAGAMENTOS — Pix crédito** — pedaladas que não saem do caixa
4. **💵 PAGAMENTOS — Renda** — cartões pagos com a renda ao longo do mês
5. **📦 FLUXO DE CAIXA** — CDB inicial → fixos → déficit → CDB final
6. **❌ NÃO PAGOS** — cartões que vão pra negociação (fundo vermelho claro)
7. **📆 SETEMBRO+** — projeção de renda, C6, parcela extra, folga
8. **📊 RESUMO** — pagos, não pagos, zerados, CDB final, parcela

### Aba Comparativo

Tabela com colunas por cenário e linhas:
- Crédito extra, Pix 18×, Pagos, CDB final, Não pagos (qtd e R$), Parcela extra, Folga set+

Seções extras: Caixa vs Valor a Pagar (com e sem crédito extra), Ranking.

## Cores por cenário

```python
colors = {
    'A': '2563EB',  # azul
    'B': 'EA580C',  # laranja
    'C': '16A34A',  # verde
    'D': 'CA8A04',  # amarelo
    'E': 'DC2626',  # vermelho
    'G': '7C3AED',  # roxo
    'H': '0891B2',  # ciano
}
```

Cada cenário tem `fill` (escuro, para cabeçalhos) e `light` (claro, para totais e destaques).

## Dados que variam entre cenários

A base fixa é igual em todos:
- **CDB fixos:** Paulo Guerra, Nubank, Amazon, Itaú Signature, PAN Buscapé
- **Pix pedalada:** Itaú Passaí (Pix Nubank)
- **Renda:** 9 cartões (Méliuz, Carrefour, PicPay, Luiza, Digio, Porto, C&A, Atacadão, BrasilCard)
- **Déficit:** `16733.62 - renda_disponivel`

O que varia:
- `extra`: True/False (crédito extra de R$ 5.200)
- `pix_18x`: True/False (Pix crédito RecargaPay 18×)
- `cdb_fixos`: qual cartão extra entra (Casas Bahia, Inter, ou nenhum)
- `nao_pagos`: lista resultante
- `cdb_final`: calculado

## Atualização quando a renda muda

Seguir [`atualizacao-planilha-cenarios.md`](atualizacao-planilha-cenarios.md). O delta de renda afeta déficit, CDB final e total caixa em TODAS as abas.

## Pitfalls

### Sempre recalcular CDB final, não somar delta cegamente
Se um novo cenário foi adicionado com CDB zero (abate parcial), o CDB final não é `anterior + delta` — é zero por definição. Atualizar o abate e o saldo negociado.

### openpyxl requer python3.12
No ambiente do Igor, `python3` é 3.11 sem openpyxl. Usar `python3.12` explicitamente.

### Não usar execute_code para openpyxl
O sandbox do execute_code não tem openpyxl. Escrever o script em `/tmp/` e rodar com `python3.12 /tmp/script.py` no terminal.
