# Atualização Programática da Planilha de Cenários

A planilha `CENARIOS-PAGAMENTOS.xlsx` tem uma aba por cenário (A, B, C, D, E, G, H) e precisa ser atualizada quando a renda líquida, o déficit ou os valores de fatura mudam.

## Estrutura de cada aba

Cada aba de cenário tem seções fixas:
- **💰 RECURSOS** — "Renda agosto (CLT + VALLO)" e "Total caixa"
- **⬜ PAGAMENTOS — CDB** — valores fixos do CDB
- **💵 PAGAMENTOS — Renda** — valores de fatura pagos pela renda
- **📦 FLUXO DE CAIXA** — "Déficit da renda" e "CDB final"
- **📆 SETEMBRO+** — "Folga mensal"
- **📊 RESUMO** — "CDB final", "Folga setembro+"

## Quando a renda muda (ex.: novo contracheque)

Quando o líquido CLT sobe (ex.: triênio, dissídio), afeta todas as abas:

1. **Renda agosto** em Recursos: novo valor
2. **Déficit da renda** no Fluxo de Caixa: `16733.62 - nova_renda`
3. **CDB final**: sobe em `nova_renda - renda_antiga` (delta positivo)
4. **Total caixa**: sobe pelo mesmo delta
5. **Folga setembro+**: sobe pelo mesmo delta
6. **Comparativo**: CDB final e Caixa total para todos os cenários

## Script de atualização

Usar openpyxl para atualizar programaticamente. A abordagem é "find and update" — procurar strings-chave nas células e atualizar o valor na coluna ao lado:

```python
import openpyxl
wb = openpyxl.load_workbook('CENARIOS-PAGAMENTOS.xlsx')

DELTA = nova_renda - renda_antiga
NEW_RENDA = nova_renda
NEW_DEFICIT = 16733.62 - nova_renda

for sheet_name in ['A', 'B', 'C', 'D', 'E', 'G', 'H']:
    ws = wb[f'Cenário {sheet_name}']
    # Percorrer células procurando textos-chave:
    # - "Renda agosto" → atualizar coluna ao lado
    # - "Déficit da renda" → atualizar coluna ao lado
    # - "CDB final" → adicionar DELTA
    # - "Total caixa" → adicionar DELTA

wb.save('CENARIOS-PAGAMENTOS.xlsx')
```

## Pitfall: Cenário H tem CDB zero com abate parcial

O Cenário H zera o CDB com abate parcial no Inter. Quando a renda sobe, o CDB "sobra" também sobe, o que aumenta o valor do abate no Inter e reduz o saldo a negociar. Atualizar manualmente:
- Célula "Abatimento com sobra CDB" (negativo)
- Célula "Saldo Inter a negociar" (8317.01 - novo_abate)
- Célula "Total a negociar" (saldo_inter + PAN_Meliuz)
