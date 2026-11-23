## Recálculo

Quando premissas mudarem (novo gasto, TotalPass, etc.), regenerar ambos os arquivos com o script completo. Não tentar editar o Excel manualmente — a estrutura é complexa e propensa a erros de merged cells.

### ⚠️ PITFALL: Off-by-one em named ranges

Section headers na linha N, dados na linha N+1. Os named ranges devem apontar para a linha dos DADOS (N+1), não do header. Padrão seguro para construir:

```python
inp["A11"] = "CUSTO DE VIDA"        # header na linha 11
cv_data = [("Custo_Vida", 4421.00, ...), ("Custo_Vida_Ago", 4094.46, ...), ...]
for i, (label, val, fonte) in enumerate(cv_data):
    r = 12 + i                     # dados na linha 12+i (12, 13, 14...)
    inp.cell(row=r, column=2, value=val).font = BLUE
# named ranges → SEMPRE apontar para a linha dos dados:
("Custo_Vida", "Inputs!$B$12"),    # ✅ dado, não header
("Custo_Vida_Ago", "Inputs!$B$13"),
```

**Validar antes de assumir que está certo:**
```python
from openpyxl import load_workbook
wb = load_workbook('FLUXO-CAIXA-2026-2030.xlsx', data_only=False)
print('Inputs B12:', wb['Inputs']['B12'].value)   # 4421, não label
print('Inputs B13:', wb['Inputs']['B13'].value)   # 4094.46
```

### ⚠️ PITFALL: CDB com yield — NUNCA componha saldo negativo

```python
# ❌ ERRADO — multiplica juros sobre juros negativos:
fluxo.cell(row=row, column=10, value=f"=H{prev}*(1+CDB_Yield)+F{row}")

# ✅ CORRETO — nunca deixa CDB negativo (cap em 0):
fluxo.cell(row=row, column=10, value=f"=MAX(0, H{prev}*(1+CDB_Yield)+F{row})")
```

Sem o `MAX(0, ...)`, um déficit Out/26 explode o CDB exponencialmente: `(-R$ 5k) × 1.01 × 1.01 × ...` vira valores absurdos em poucos meses.

### ⚠️ PITFALL: LibreOffice headless recalc precisa de diretórios SEPARADOS

`--outdir` falha com erro `0x4c0c` se for o mesmo dir do input. Padrão correto:

```bash
rm -rf /tmp/recalc_in /tmp/recalc_out
mkdir /tmp/recalc_in /tmp/recalc_out
cp FLUXO-CAIXA-2026-2030.xlsx /tmp/recalc_in/model.xlsx
libreoffice --headless --calc --convert-to xlsx /tmp/recalc_in/model.xlsx --outdir /tmp/recalc_out
cp /tmp/recalc_out/model.xlsx FLUXO-CAIXA-2026-2030.xlsx
```

Sem isso, as fórmulas ficam sem valores calculados e `openpyxl(data_only=True)` retorna None.

### Pattern final: gerar XLSX → MD → PDF em sequência

```python
# 1. openpyxl salva XLSX (fórmulas, sem valores calculados)
wb.save('FLUXO-CAIXA-2026-2030.xlsx')

# 2. LibreOffice recalcula (fórmulas → valores)
# [comando bash acima]

# 3. Gerar MD derivado (do XLSX recalculado)
# [seu script de geração de MD aqui]

# 4. Gerar PDF do MD
pandoc FLUXO-CAIXA-2026-2030.md -o FLUXO-CAIXA-2026-2030.pdf \
  --pdf-engine=wkhtmltopdf --pdf-engine-opt=--no-background \
  -V geometry:margin=1.5cm -V fontsize=8pt

# 5. Validar com checks (TRUE/FALSE no Checks tab)
```