# Padrão: Geração de Excel + Markdown do Fluxo de Caixa

Script Python (`python3.12`) que gera simultaneamente:
- Excel com 5 abas (Visão Geral, Fluxo de Caixa, Resumo, Parcelamentos, Premissas)
- Markdown com orçamento, projeção e métricas

## Estrutura do modelo de dados

```python
# RENDA
clt_base = 8913.00       # CLT líquido recorrente (com triênio, sem pontuais)
vallo_base = 4420.00     # VALLO BENEFÍCIOS mensal
dissidio = 1.04          # ~4% ao ano, efeito novembro

# HOME EQUITY (extrair da CCB real com pdftotext)
he_principal = 108719.73
he_amort = 2343.98       # SAC: amortização constante
he_taxa = 0.017          # 1.7% a.m.
he_seguros = 68.47       # MIP + DFI
he_schedule = {}         # dict[YYYY-MM] = parcela_total

# GASTOS MENSAIS
lazer = 1970             # Claro 330 + Karatê 100 + TotalPass 240 + Combust. 300 + Livres 1000
nao_lazer = 2451         # Condomínio 1020 + Vivo 105 + IA 408 + Light 778 + Gás 140
gasto_mensal = lazer + nao_lazer  # 4421

# C6 EMPRÉSTIMO
c6_start = 4389.00
c6_amort = 88.00         # SAC ~R$88/mês de redução

# PARCELAMENTOS (extrair das faturas reais)
card_data = {
    "Nubank": {"2026-09": 5160.86, ...},
    "Passaí": {"2026-09": 961.62, ...},
    ...
}
```

## Loop mensal

```python
for year in range(2026, 2029):
    for month in range(start_month, 13):
        key = f"{year}-{month:02d}"
        
        # Renda com dissídio
        mult = calcular_mult(year, month)
        clt = round(clt_base * mult, 2)
        vallo = round(vallo_base * mult, 2)
        
        # VALLO → Home Equity
        he = he_schedule.get(key, 0)
        vallo_surplus = round(vallo - he, 2)
        
        # 13º
        extra = 0
        if month == 11: extra = round(gross * 0.50, 2)
        elif month == 12: extra = round(gross * 0.39, 2)
        
        # Disponível = CLT + sobra VALLO + 13º
        available = round(clt + vallo_surplus + extra, 2)
        
        # Faturas = parcelamentos fixos + gastos novos do mês anterior
        inst = instalments_by_month.get(key, 0)
        prev = gasto_mensal  # gasto do mês anterior aparece nesta fatura
        bills = round(inst + prev, 2)
        
        # C6 SAC
        c6 = round(max(0, c6_start - c6_amort * months_elapsed), 2)
        
        net = round(available - bills - c6, 2)
```

## Estrutura do Excel (openpyxl)

### Aba 1: Visão Geral
- Orçamento mensal com categorias (ENTRADA, LAZER, FIXO, SAÍDA, SALDO)
- Ajustes já considerados (com antes/depois)
- Métricas KPIs (reserva inicial, pior momento, Dez/2028, crescimento)
- Color coding: verde=entrada, amarelo=saldo, azul=lazer, vermelho=déficit

### Aba 2: Fluxo de Caixa
- Colunas: Mês, CLT, VALLO, Home Equity, Sobra VALLO, 13º, Disponível, Parcelamentos, Novos Gastos, Faturas, C6, Saldo, Reserva, Evento
- 29 linhas (Ago/26 a Dez/28)
- Eventos: 13º(1)+Diss, 13º(2), DISSÍDIO
- Linhas alternadas em azul claro
- Saldo negativo em vermelho

### Aba 3: Resumo
- Cartões mantidos (7)
- Cartões negociação (12)
- Recursos CDB

### Aba 4: Parcelamentos
- Matriz: Mês × Cartão com totais

### Aba 5: Premissas
- Renda, Home Equity, Gastos, C6, Cenário X2

## Estilos padrão

```python
hfont = Font(name='Calibri', size=11, bold=True, color='FFFFFF')
hfill = PatternFill(start_color='2F5496', end_color='2F5496', fill_type='solid')
tfont = Font(name='Calibri', size=16, bold=True, color='1F3864')
sfont = Font(name='Calibri', size=13, bold=True, color='2F5496')
mfmt = '#,##0'
afill = PatternFill(start_color='F2F7FC', end_color='F2F7FC', fill_type='solid')  # alternado
efill = PatternFill(start_color='D6E4F0', end_color='D6E4F0', fill_type='solid')  # evento
gfill = PatternFill(start_color='E2EFDA', end_color='E2EFDA', fill_type='solid')  # entrada
yfill = PatternFill(start_color='FFF2CC', end_color='FFF2CC', fill_type='solid')  # saldo
```

## Arquivos gerados

- `~/MEGA/Comprovantes/FLUXO-CAIXA-2026-2030.xlsx`
- `~/MEGA/Comprovantes/FLUXO-CAIXA-2026-2030.md`

> Conferir com `ls ~/MEGA/Comprovantes/FLUXO-CAIXA-*.md` antes de gerar — o intervalo de anos no nome já mudou de versão uma vez (2026-2028 → 2026-2030, 03/08/2026) e o arquivo antigo foi apagado.

## Recálculo

Quando premissas mudarem (novo gasto, TotalPass, etc.), regenerar ambos os arquivos com o script completo. Não tentar editar o Excel manualmente — a estrutura é complexa e propensa a erros de merged cells.
