# 📊 Padrão XLSX do Fluxo de Caixa com Gráfico de CDB

> **Atualizado:** 13/08/2026 (X21 → validação do padrão banker-grade com `excel-author`)
> **Autor da primeira versão:** Igor + Hermes Agent

Quando gerar `FLUXO-CAIXA-2026-2030.xlsx`, seguir este padrão. Estrutura validada para que o gráfico de evolução do CDB funcione em Excel/LibreOffice sem dependências externas.

## ⚙️ Setup

```bash
pip install "openpyxl>=3.0"
```

Estrutura validada em 13/08/2026 — usar skill `excel-author` (oficial Nous Research) como referência para convenções banker-grade.

## 🏛️ Estrutura de abas (5 sheets — padrão completo)

Para XLSX significativo (X20+), usar a estrutura completa de 5 sheets:

| # | Nome | Conteúdo | Convenção excel-author |
|---|---|---|---|
| 1 | `Inputs` | Todos os parâmetros (renda, custo vida, HE, parcelas, CDB inicial) | **Blue cells** com comments |
| 2 | `Fluxo Mensal` | Cálculos derivados (Renda, Saldo, CDB) | **Black formulas** referenciando Inputs via named ranges |
| 3 | `CDB Evolução` | Tabela mês-a-mês + **gráfico de linha** + marcos anotados | Links verdes para Fluxo Mensal |
| 4 | `Sensitivity` | Tabela 5×5 (eixo Y = Δ custo vida, eixo X = Δ VALLO) | Blue inputs (Δ), Black formulas (resultado) |
| 5 | `Checks` | TRUE/FALSE automático: CDB nunca zera, déficit = 2, soma Paulo = 5.000, etc. | **Black formulas** (MIN, COUNTIF, ABS) com resultado em IF |

Para XLSX simples (apenas a tabela + gráfico), usar a versão 3 sheets:
| # | Nome | Conteúdo |
|---|---|---|
| 1 | `Fluxo Mensal` | Tabela mês-a-mês com 8 colunas: Mês, Renda, Faturas, HE, Outros, Saldo, CDB usou, CDB saldo |
| 2 | `CDB Evolução` | Tabela mês-a-mês + **gráfico de linha** mostrando CDB saldo + marcadores em eventos-chave |
| 3 | `Resumo Anual` | Totais anuais (Renda, Faturas, HE, Outros, Saldo) |

## 🎨 Convenção banker-grade (excel-author)

| Cor | Uso | Quando |
|---|---|---|
| **Blue** `Font(color="0000FF")` | Hardcoded input | Inputs, dados históricos, drivers que o usuário vai flexar |
| **Black** `Font(color="000000")` (default) | Fórmula | Toda célula derivada de outras células |
| **Green** `Font(color="006100")` | Link entre sheets | Cross-sheet references, links para outras abas |

**Regra absoluta:** "If you catch yourself computing a value in Python and writing the result, stop." — Use fórmulas Excel sempre.

**Named ranges:** definir para qualquer figura referenciada entre sheets. Padrão:
```python
wb.defined_names["CDB_Inicial"] = DefinedName(
    "CDB_Inicial", attr_text="Inputs!$B$27"
)
```

## 💻 Implementação completa (5 sheets)

Usar `python3.12` + `openpyxl`. Cuidado: `execute_code` é bloqueado pelo Hermes (segurança contra subprocess não aprovado) — **usar sempre `terminal` com script em `/tmp/`** ou inline.

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.chart import LineChart, BarChart, Reference
from openpyxl.chart.marker import Marker
from openpyxl.utils import get_column_letter

# Convenção de cores
BLUE = Font(color="0000FF")
BLACK = Font(color="000000")
GREEN = Font(color="006100")
BOLD = Font(bold=True)
HEADER_FILL = PatternFill("solid", fgColor="1F4E78")
HEADER_FONT = Font(color="FFFFFF", bold=True, size=12)
SUBHEADER_FILL = PatternFill("solid", fgColor="D9E1F2")
GREEN_FILL = PatternFill("solid", fgColor="C6EFCE")
RED_FILL = PatternFill("solid", fgColor="FFC7CE")
YELLOW_FILL = PatternFill("solid", fgColor="FFEB9C")
CENTER_FILL = PatternFill("solid", fgColor="BDD7EE")
border = Border(
    left=Side(style='thin'), right=Side(style='thin'),
    top=Side(style='thin'), bottom=Side(style='thin')
)
center = Alignment(horizontal='center', vertical='center')

# 1. Criar workbook
wb = Workbook()
wb.remove(wb.active)

# 2. Sheet "Inputs" — todos os parâmetros como blue cells com comments
inp = wb.create_sheet("Inputs")
inp["A1"] = "FLUXO DE CAIXA — INPUTS"
inp["A1"].font = HEADER_FONT
inp["A1"].fill = HEADER_FILL
inp.merge_cells("A1:D1")

# Cada input: label, valor, vigencia, fonte
inputs_data = [
    ("Parâmetro", 7995.07, "Ago-Dez/26", "CONTRACHEQUE.md. Triênio incluso."),
    # ... outros inputs
]
for i, (label, val, vigencia, fonte) in enumerate(inputs_data):
    r = 5 + i
    inp.cell(row=r, column=1, value=label).border = border
    inp.cell(row=r, column=2, value=val).font = BLUE  # INPUT
    inp.cell(row=r, column=2).number_format = '#,##0.00'
    inp.cell(row=r, column=2).border = border
    inp.cell(row=r, column=2).comment = Comment(fonte, "model")  # OBRIGATÓRIO
    inp.cell(row=r, column=3, value=vigencia).border = border
    inp.cell(row=r, column=4, value=fonte).border = border
```

**Pitfall crítico:** off-by-one em named ranges. Quando a estrutura é:
- Linha N: section header (`inp["A{N}"] = "CUSTO DE VIDA"`)
- Linha N+1, N+2, ...: dados

O named range deve apontar para `Inputs!$B$(N+1)` em diante, NÃO `Inputs!$B$(N+2)`. Sempre validar com um check.

```python
# CERTO (header na linha 11, dados nas linhas 12-13)
wb.defined_names["Custo_Vida"] = DefinedName("Custo_Vida", attr_text="Inputs!$B$12")
wb.defined_names["Custo_Vida_Ago"] = DefinedName("Custo_Vida_Ago", attr_text="Inputs!$B$13")
```

## 3. Sheet "Fluxo Mensal" — todas as células derivadas como fórmulas

```python
fluxo = wb.create_sheet("Fluxo Mensal")

# Headers
for col, h in enumerate(["Mês", "Renda", "Faturas", "HE", "Outros", "Saldo", "CDB usou", "CDB saldo"], 1):
    cell = fluxo.cell(row=3, column=col, value=h)
    cell.font = HEADER_FONT
    cell.fill = HEADER_FILL
    cell.alignment = center
    cell.border = border

for i, mes in enumerate(MESES):
    row = 4 + i
    
    # A: Mês (texto)
    fluxo.cell(row=row, column=1, value=mes).border = border
    
    # B: Renda (FÓRMULA preta)
    if mes == 'Ago/26':
        renda_f = "=Renda_CLT_2026+VALLO+Aluguel_Diego"
    elif mes == 'Nov/26':
        renda_f = "=Renda_CLT_2026+VALLO+Aluguel_Diego+Decimo_1"
    # ... outros meses
    fluxo.cell(row=row, column=2, value=renda_f).font = BLACK
    fluxo.cell(row=row, column=2).number_format = '#,##0.00'
    fluxo.cell(row=row, column=2).border = border
    
    # C: Faturas (BLUE input — valor do X21)
    fluxo.cell(row=row, column=3, value=FATURAS[i]).font = BLUE
    fluxo.cell(row=row, column=3).number_format = '#,##0.00'
    fluxo.cell(row=row, column=3).border = border
    
    # D: HE (BLUE input — valores SAC do HOME-EQUITY.md)
    fluxo.cell(row=row, column=4, value=HE_VALUES[i]).font = BLUE
    fluxo.cell(row=row, column=4).number_format = '#,##0.00'
    fluxo.cell(row=row, column=4).border = border
    
    # E: Outros (BLUE input)
    fluxo.cell(row=row, column=5, value=OUTROS[i]).font = BLUE
    fluxo.cell(row=row, column=5).number_format = '#,##0.00'
    fluxo.cell(row=row, column=5).border = border
    
    # F: Saldo (FÓRMULA preta)
    fluxo.cell(row=row, column=6, value=f"=B{row}-C{row}-D{row}-E{row}").font = BLACK
    fluxo.cell(row=row, column=6).number_format = '#,##0.00;[Red]-#,##0.00'
    fluxo.cell(row=row, column=6).border = border
    
    # G: CDB usou (FÓRMULA preta)
    if i == 0:
        fluxo.cell(row=row, column=7, value=0).font = BLACK
    else:
        fluxo.cell(row=row, column=7, value=f"=IF(F{row}<0,F{row},0)").font = BLACK
    
    # H: CDB saldo (FÓRMULA preta — COM CAP EM 0!)
    if i == 0:
        fluxo.cell(row=row, column=8, value="=CDB_Inicial").font = BLACK
    else:
        prev = row - 1
        # CRÍTICO: MAX(0, ...) para nunca compor saldo negativo
        fluxo.cell(row=row, column=8, value=f"=MAX(0,H{prev}*(1+CDB_Yield)+F{row})").font = BLACK
    fluxo.cell(row=row, column=8).number_format = '#,##0.00'
    fluxo.cell(row=row, column=8).border = border
    
    # Colorir saldo
    if FATURAS[i] > 14000:
        fluxo.cell(row=row, column=6).fill = RED_FILL
    else:
        fluxo.cell(row=row, column=6).fill = GREEN_FILL

# Marcar Out/26 como mínimo
fluxo.cell(row=6, column=8).fill = YELLOW_FILL  # linha 6 = Out/26
```

## 4. Sheet "CDB Evolução" — links verdes + gráfico

```python
cdb = wb.create_sheet("CDB Evolução")

# Dados via link (green) para Fluxo Mensal
for i, mes in enumerate(MESES):
    row = 4 + i
    cdb.cell(row=row, column=1, value=f"='Fluxo Mensal'!A{4+i}").font = GREEN  # LINK
    cdb.cell(row=row, column=2, value=f"='Fluxo Mensal'!H{4+i}").font = GREEN
    cdb.cell(row=row, column=2).number_format = '#,##0.00'
    if i > 0:
        cdb.cell(row=row, column=3, value=f"=B{row}-B{row-1}").font = BLACK  # Δ mensal

# Gráfico
chart = LineChart()
chart.title = "Evolução do CDB C6 (Cenário X<n>)"
chart.style = 13
chart.y_axis.title = "CDB saldo (R$)"
chart.x_axis.title = "Mês"
chart.height = 14
chart.width = 28

data = Reference(cdb, min_col=2, min_row=3, max_row=N+3, max_col=2)
cats = Reference(cdb, min_col=1, min_row=4, max_row=N+3)
chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)
chart.series[0].marker = Marker(symbol='circle', size=4)

cdb.add_chart(chart, "F3")
```

## 5. Sheet "Sensitivity" — tabela 5×5

```python
sens = wb.create_sheet("Sensitivity")

# Eixos (blue inputs)
valho_axis = [-300, -150, 0, 150, 300]  # Δ VALLO
cvida_axis = [-300, -150, 0, 150, 300]  # Δ Custo Vida

# Header eixo X
for j, v in enumerate(valho_axis):
    cell = sens.cell(row=6, column=2+j, value=f"=VALLO+{v}")
    cell.font = BLUE  # INPUT
    cell.number_format = '#,##0'

# Header eixo Y
for i, c_delta in enumerate(cvida_axis):
    cell = sens.cell(row=7+i, column=1, value=f"=Custo_Vida+{c_delta}")
    cell.font = BLUE  # INPUT

# Matriz 5x5: center cell (i=2, j=2) = cenário base
for i, c_delta in enumerate(cvida_axis):
    for j, v_delta in enumerate(valho_axis):
        formula = f"=CDB_Final_Base+({v_delta})*49-({c_delta})*49"
        cell = sens.cell(row=7+i, column=2+j, value=formula)
        cell.font = BLACK  # FORMULA
        cell.number_format = '#,##0.00'
        if i == 2 and j == 2:
            cell.fill = CENTER_FILL
            cell.font = BOLD
            cell.value = "=CDB_Final_Base"
```

## 6. Sheet "Checks" — TRUE/FALSE automático

```python
chk = wb.create_sheet("Checks")

checks = [
    ("CDB nunca zera (todos os meses)",
     "=MIN('Fluxo Mensal'!H4:H56)",
     "=MIN('Fluxo Mensal'!H4:H56)",
     '=IF(C4>0,"✅ OK","❌ FALHA")'),
    ("Saldo Out/26 ≈ -R$ 9.227,79",
     "=ROUND('Fluxo Mensal'!F6,2)",
     "=ROUND('Fluxo Mensal'!F6,2)",
     '=IF(ABS(C5-(-9227.79))<1,"✅ OK","❌ FALHA")'),
    ("Soma parcelas Paulo = R$ 5.000",
     "=Paulo_1+Paulo_2+Paulo_3+Paulo_4+Paulo_5",
     "=Paulo_1+Paulo_2+Paulo_3+Paulo_4+Paulo_5",
     '=IF(C8=5000,"✅ OK","❌ FALHA")'),
    ("Meses com déficit = 2 (Set+Out/26)",
     "=COUNTIF('Fluxo Mensal'!F4:F56,\"<0\")",
     "=COUNTIF('Fluxo Mensal'!F4:F56,\"<0\")",
     '=IF(C9=2,"✅ OK","⚠️ DIVERGE")'),
]
for i, (label, formula, result, status) in enumerate(checks):
    r = 4 + i
    chk.cell(row=r, column=1, value=label).border = border
    chk.cell(row=r, column=2, value=formula).font = GREEN  # LINK
    chk.cell(row=r, column=3, value=result).font = BOLD
    chk.cell(row=r, column=4, value=status).font = BOLD
    chk.cell(row=r, column=4).alignment = center
```

## 7. Salvar + Recalcular

```python
out_path = '/home/igorferreira/MEGA/Comprovantes/FLUXO-CAIXA-2026-2030.xlsx'
wb.save(out_path)

# openpyxl escreve fórmulas como string — precisa recalcular!
# Use LibreOffice com diretórios SEPARADOS (input/output)
import shutil, subprocess
shutil.rmtree('/tmp/recalc_in', ignore_errors=True)
shutil.rmtree('/tmp/recalc_out', ignore_errors=True)
subprocess.run(['mkdir', '-p', '/tmp/recalc_in', '/tmp/recalc_out'])
shutil.copy(out_path, '/tmp/recalc_in/model.xlsx')
subprocess.run(['libreoffice', '--headless', '--calc', '--convert-to', 'xlsx',
                '/tmp/recalc_in/model.xlsx', '--outdir', '/tmp/recalc_out'],
               check=True, capture_output=True)
shutil.copy('/tmp/recalc_out/model.xlsx', out_path)
```

## 🎨 Estilos visuais

```python
header_font = Font(bold=True, color='FFFFFF', size=11)
header_fill = PatternFill('solid', fgColor='1F4E78')  # azul escuro
green_fill = PatternFill('solid', fgColor='C6EFCE')   # verde claro
red_fill = PatternFill('solid', fgColor='FFC7CE')     # vermelho claro
yellow_fill = PatternFill('solid', fgColor='FFEB9C')  # amarelo (mínimo)
border = Border(left=Side('thin'), right=Side('thin'), top=Side('thin'), bottom=Side('thin'))
```

## 📊 Colunas CSV (espelho do .md e .xlsx)

```csv
Mês,Renda,Faturas,HE,Outros,Saldo,CDB usou,CDB saldo
Ago/26,14415.07,0.00,67.90,4409.65,9937.52,0.00,39104.66
...
```

## 🏁 Marcos do gráfico de CDB

| Mês | Marco |
|---|---|
| Ago/26 | ← Início |
| Set/26 | 🔴 CDB começa a ser usado |
| **Out/26** | 🔴 **MÍNIMO** — pintar célula de amarelo |
| Nov/26 | 🟢 CDB volta a crescer |
| Nov/27 | 🟢 +R$ 1.000/mês (consignado Noorden acaba) |
| Dez/30 | ⭐ Final — pintar de amarelo |

## ⚠️ Pitfalls (todos aprendidos em sessão real)

1. **`execute_code` é bloqueado** — Hermes Agent bloqueia execução de código que possa chamar subprocess. Sempre use `terminal` com `python3.12 /tmp/script.py` ou inline `python3.12 -c "..."`.
2. **Chart precisa de `Marker`** — sem marker, a linha fica invisível em alguns visualizadores (LibreOffice mobile, Numbers iOS).
3. **`Reference` deve apontar para `max_row=N+1` se o header está na linha 1** — fácil errar e o gráfico fica vazio.
4. **CSV sem aspas** — usar vírgula como separador, sem aspas (Excel BR entende direto).
5. **Não usar `execute_code`** mesmo quando parece conveniente — vai ser bloqueado pelo guard.
6. **CDB com yield SEM cap=0 → números astronômicos** — fórmula `=H{prev}*(1+CDB_Yield)+F{row}` sem MAX gera valores tipo 10⁸⁵. SEMPRE usar `=MAX(0, H{prev}*(1+CDB_Yield)+F{row})`.
7. **Off-by-one em named ranges** — quando a estrutura tem section header na linha N e dados na N+1, o named range DEVE apontar para N+1 (dados), não N+2.
8. **`libreoffice --convert-to xlsx` falha se input e output são mesmo dir** — sempre usar `/tmp/recalc_in/` e `/tmp/recalc_out/` separados.
9. **Chart precisa ser referenciado após add_chart** — `chart = LineChart()` antes de qualquer `add_data` / `add_chart`.

## 🧪 Validação completa (13/08/2026)

Resultado do X21 com 5 sheets + checks:

```
=== CHECKS (TRUE/FALSE) ===
  R$ 16,659.98 | ✅ OK | CDB nunca zera (todos os meses)
  R$ -9,227.79  | ✅ OK | Saldo Out/26 ≈ -R$ 9.227,79
  R$ 16,659.98 | ✅ OK | CDB Out/26 (mínimo) > R$ 0 (nunca zera)
  R$ 577,550.00 | ✅ OK | CDB Dez/30 > R$ 500.000 (com yield 1% a.m.)
  R$ 5,000.00  | ✅ OK | Soma parcelas Paulo = R$ 5.000
  R$ 2.00     | ✅ OK | Meses com déficit = 2 (Set+Out/26)
  R$ 0.00     | ✅ OK | Nov/26 em diante = saldo positivo
  R$ 16,659.98 | ✅ OK | CDB nunca zera (incluindo yield composto)
```

8/8 checks passaram.

## Histórico

- **13/08/2026 (X19)** — Primeira versão, 3 sheets, sem checks.
- **13/08/2026 (X21)** — Versão banker-grade completa: 5 sheets, 8 checks TRUE/FALSE, gráfico CDB com marcadores, sensitivity 5×5, named ranges, blue/black/green, MAX(0,...) cap no CDB.
