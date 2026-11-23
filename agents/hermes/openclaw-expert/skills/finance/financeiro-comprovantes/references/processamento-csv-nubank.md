# Processamento de CSV de Extrato Nubank

## Formato

O Nubank exporta extrato de transações em CSV com 3 colunas:

```
date,title,amount
2026-08-05,Mercado*Mercadolivre - Parcela 1/3,"42,33"
2026-07-31,Pagamento recebido,"- 5.660,52"
```

## Armadilhas de parsing

1. **Formato numérico português**: ponto como milhar, vírgula como decimal. Ex: `"5.660,52"` = 5660.52
2. **Valores negativos**: prefixados com `"- "` (hífen + espaço). Ex: `"- 5.660,52"`
3. **Parcelas no título**: formato `Parcela X/Y` dentro do campo title
4. **Sem total fechado**: o CSV lista transações, não o valor da fatura fechada. O total do período é a soma de todas as transações (exceto pagamentos).

## Pipeline Python

```python
import csv
from collections import defaultdict

def parse_amount(s):
    s = s.strip().replace(' ', '')
    sign = -1 if s.startswith('-') else 1
    if sign < 0:
        s = s[1:]
    s = s.replace('.', '').replace(',', '.')
    return sign * float(s)

# Classificar transações
parcelas = []   # (data, desc, parcela_atual, total, valor)
avulsas = []    # (data, desc, valor)
pagamentos = [] # (data, desc, valor) — negativo

for row in reader:
    title = row['title']
    amount = parse_amount(row['amount'])
    
    if amount < 0 or 'Pagamento' in title:
        pagamentos.append((row['date'], title, amount))
    elif 'Parcela' in title:
        cur, tot = extract_xy(title)  # regex: Parcela (\d+)/(\d+)
        parcelas.append((row['date'], title, cur, tot, amount))
    else:
        avulsas.append((row['date'], title, amount))
```

## Projeção de parcelas futuras

Para cada parcela `X/Y`, as parcelas restantes = `Y - X`. Projetar mês a mês:

- Agrupar por mês: `monthly[+N_meses] += valor`
- Marcar parcelas que terminam: `if Y - X == 1: ending_next_month.append(...)`
- Se `X == 1` e data é do mês atual → NOVO parcelamento

## Pitfalls

- O CSV é extrato de transações, NÃO fatura fechada. O total real pode ser diferente do que o CSV mostra.
- A fatura do Nubank fecha por volta do dia 5. Transações entre fechamento e vencimento aparecem em CSV futuro.
- `Pagamento recebido` aparece como valor negativo — não somar ao total do período.
- Parcelas `Y/Y` (última) NÃO projetam para o próximo mês.
