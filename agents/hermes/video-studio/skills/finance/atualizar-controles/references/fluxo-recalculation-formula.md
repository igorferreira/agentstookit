# Fórmula de Recalculo do Fluxo de Caixa

## Fontes de dados

| Dado | Arquivo fonte | Campo |
|---|---|---|
| Renda mensal | `CONTRACHEQUE.md` | Líquido Est. + VALLO (+ 13º em nov/dez) |
| Faturas cartão | `CONTROLE_FATURAS_MANTIDOS.md` | Soma de todos os cartões ativos + parcelamentos |
| Home Equity | `HOME-EQUITY.md` | Cronograma SAC — coluna "Parcela" |
| CDB inicial | Contexto da sessão | R$ 29.000 (após pagamento Paulo) |

## Algoritmo Python

```python
cdb = <CDB_INICIAL>  # ex: 29000.00 ou 22041.00 após saque

for mes in meses_ordenados:
    renda = renda_dict[mes]        # CONTRACHEQUE.md
    faturas = faturas_dict[mes]    # 4421 base + parcelamentos + extras
    he = he_schedule[mes]          # HOME-EQUITY.md SAC
    
    saldo = renda - faturas - he
    
    if saldo < 0:
        # Déficit: saca do CDB
        cdb += saldo  # saldo é negativo
    else:
        # Superávit: aporta no CDB
        cdb += saldo
```

## Estrutura dos dicionários

### renda_dict
```python
# Meses normais: CLT líquido + VALLO
renda["Set/26"] = 7995.07 + 4420.00  # = 12415.07

# Novembro: + 13º 1ª parcela (50% do bruto)
renda["Nov/26"] = 8354.88 + 4596.80 + 6981.25  # = 19932.93

# Dezembro: + 13º 2ª parcela (~39% do bruto após descontos)
renda["Dez/26"] = 8354.88 + 4596.80 + 5445.38  # = 18397.06
```

### faturas_dict
```python
# Base: custo de vida = R$ 4.421 (lazer + não-lazer)
# Parcelamentos se extinguem ao longo do tempo
faturas = {
    "Ago/26": 0,
    "Set/26": 14892,   # pico de parcelamentos
    ...
    "Jul/27": 5259,    # últimos parcelamentos quitando
    "Ago/27": 4421,    # só custo base daqui pra frente
}

# Extras: adicionar conforme novos parcelamentos
atacadao = {"Set/26": 323.08, "Out/26": 323.08}
porto = {"Set/26": 1195.77, "Out/26": 695.15, ...}

# Combinar:
f = faturas_base.get(mes, 4421) + atacadao.get(mes, 0) + porto.get(mes, 0)
```

### he_schedule
Extraído DIRETAMENTE da tabela SAC do `HOME-EQUITY.md`, coluna "Parcela":
```python
he = {
    "Set/26": 4260.69, "Out/26": 4220.84, ...
    "Out/30": 2308.15, "Nov/30": 0, "Dez/30": 0,
}
```

## ⚠️ Erros que já aconteceram

1. **Renda errada**: fluxo usava ~R$9.000 quando o real era ~R$12.415 → **SEMPRE extrair do CONTRACHEQUE.md**
2. **HE errado**: fluxo usava valores ~R$130 acima do SAC real → **SEMPRE extrair do HOME-EQUITY.md**
3. **Esquecer 13º**: novembro e dezembro têm renda muito maior → incluir as parcelas
4. **Esquecer dissídio**: a partir de nov/26 a renda sobe ~4%/ano → usar projeção do CONTRACHEQUE.md
5. **Excel desatualizado**: gerar .xlsx com `python3.12` + openpyxl após cada alteração no .md
