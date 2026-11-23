#!/usr/bin/env python3
"""Regenera FLUXO-CAIXA-2026-2030.md a partir do XLSX (após recalc do LibreOffice).

Uso:
    python3.12 /tmp/regenerate_md_from_xlsx.py

Lê:
    ~/MEGA/Comprovantes/FLUXO-CAIXA-2026-2030.xlsx

Escreve:
    ~/MEGA/Comprovantes/FLUXO-CAIXA-2026-2030.md

Por que regenerar do XLSX (não do Python):
    - O .md é a versão derivada, não a fonte canônica
    - O .xlsx é o que tem as fórmulas validadas pelo LibreOffice
    - Mudanças nos Inputs propagam automaticamente após recalc
"""

from openpyxl import load_workbook
from pathlib import Path
from datetime import datetime

wb = load_workbook('/home/usuario/MEGA/Comprovantes/FLUXO-CAIXA-2026-2030.xlsx', data_only=True)
fl = wb['Fluxo Mensal']
chk = wb['Checks']

meses = []
for i in range(53):
    row = i + 4
    meses.append({
        'mes': fl.cell(row=row, column=1).value,
        'renda': fl.cell(row=row, column=2).value or 0,
        'faturas': fl.cell(row=row, column=3).value or 0,
        'he': fl.cell(row=row, column=4).value or 0,
        'outros': fl.cell(row=row, column=5).value or 0,
        'imprevistos': fl.cell(row=row, column=6).value or 0,
        # Estrutura atual da aba Fluxo Mensal:
        # G=13º, H=Saldo mensal, I=CDB usou, J=CDB saldo.
        # Pitfall: versões antigas do script liam H como CDB e corrompiam o MD.
        'decimo': fl.cell(row=row, column=7).value or 0,
        'saldo': fl.cell(row=row, column=8).value or 0,
        'cdb_usou': fl.cell(row=row, column=9).value or 0,
        'cdb_saldo': fl.cell(row=row, column=10).value or 0,
    })

check_results = []
for r in range(4, 12):
    check_results.append({
        'label': chk.cell(row=r, column=1).value,
        'valor': chk.cell(row=r, column=3).value,
        'status': chk.cell(row=r, column=4).value,
    })

min_cdb = min(meses, key=lambda m: m['cdb_saldo'])
cdb_final = meses[-1]['cdb_saldo']

md = f"""# Fluxo de Caixa — auto-gerado do XLSX (regenerado {datetime.now().strftime('%Y-%m-%d %H:%M')})

> **Fonte canônica:** `FLUXO-CAIXA-2026-2030.xlsx` (após recalc LibreOffice)
> **Cobertura:** Ago/26 a Dez/30 (53 meses)

## 🎯 Indicadores-chave

| Indicador | Valor |
|---|---|
| CDB mínimo | **R$ {min_cdb['cdb_saldo']:,.2f}** ({min_cdb['mes']}) |
| CDB final (Dez/30) | **R$ {cdb_final:,.2f}** |

### 2026

| Mês | Renda | Faturas | HE | Outros | Imprevistos | Saldo | CDB saldo |
|---|---:|---:|---:|---:|---:|---:|---:|
"""

for m in meses[:5]:
    s = '🔴' if m['saldo'] < 0 else '🟢'
    md += f"| {m['mes']} | {m['renda']:,.2f} | {m['faturas']:,.2f} | {m['he']:,.2f} | {m['outros']:,.2f} | {m['imprevistos']:,.2f} | {s} {m['saldo']:+,.2f} | {m['cdb_saldo']:,.2f} |\n"

md += "\n### 2027\n\n| Mês | Renda | Faturas | HE | Outros | Imprevistos | Saldo | CDB saldo |\n|---|---:|---:|---:|---:|---:|---:|---:|\n"
for m in meses[5:17]:
    s = '🔴' if m['saldo'] < 0 else '🟢'
    md += f"| {m['mes']} | {m['renda']:,.2f} | {m['faturas']:,.2f} | {m['he']:,.2f} | {m['outros']:,.2f} | {m['imprevistos']:,.2f} | {s} {m['saldo']:+,.2f} | {m['cdb_saldo']:,.2f} |\n"

md += "\n### 2028\n\n| Mês | Renda | Faturas | HE | Outros | Imprevistos | Saldo | CDB saldo |\n|---|---:|---:|---:|---:|---:|---:|---:|\n"
for m in meses[17:29]:
    s = '🔴' if m['saldo'] < 0 else '🟢'
    md += f"| {m['mes']} | {m['renda']:,.2f} | {m['faturas']:,.2f} | {m['he']:,.2f} | {m['outros']:,.2f} | {m['imprevistos']:,.2f} | {s} {m['saldo']:+,.2f} | {m['cdb_saldo']:,.2f} |\n"

md += "\n### 2029\n\n| Mês | Renda | Faturas | HE | Outros | Imprevistos | Saldo | CDB saldo |\n|---|---:|---:|---:|---:|---:|---:|---:|\n"
for m in meses[29:41]:
    s = '🔴' if m['saldo'] < 0 else '🟢'
    md += f"| {m['mes']} | {m['renda']:,.2f} | {m['faturas']:,.2f} | {m['he']:,.2f} | {m['outros']:,.2f} | {m['imprevistos']:,.2f} | {s} {m['saldo']:+,.2f} | {m['cdb_saldo']:,.2f} |\n"

md += "\n### 2030\n\n| Mês | Renda | Faturas | HE | Outros | Imprevistos | Saldo | CDB saldo |\n|---|---:|---:|---:|---:|---:|---:|---:|\n"
for m in meses[41:]:
    s = '🔴' if m['saldo'] < 0 else '🟢'
    md += f"| {m['mes']} | {m['renda']:,.2f} | {m['faturas']:,.2f} | {m['he']:,.2f} | {m['outros']:,.2f} | {m['imprevistos']:,.2f} | {s} {m['saldo']:+,.2f} | {m['cdb_saldo']:,.2f} |\n"

md += """
---

## ✅ Auditoria (checks automáticos)

| Check | Status |
|---|---|
"""

for c in check_results:
    v = f'R$ {c["valor"]:,.2f}' if isinstance(c['valor'], (int, float)) else str(c['valor'])
    md += f"| {c['label']} | {c['status']} ({v}) |\n"

md += """
---

## 📂 Arquivos relacionados

- **Planilha:** `~/MEGA/Comprovantes/FLUXO-CAIXA-2026-2030.xlsx`
- **CSV:** `~/MEGA/Comprovantes/FLUXO-CAIXA-2026-2030.csv`
- **PDF:** `~/MEGA/Comprovantes/FLUXO-CAIXA-2026-2030.pdf`
"""

out = Path('/home/usuario/MEGA/Comprovantes/FLUXO-CAIXA-2026-2030.md')
out.write_text(md)
print(f'✅ MD regenerado: {out}')
print(f'   Linhas: {md.count(chr(10))}')
print(f'   CDB Out/26 mínimo: {min_cdb["cdb_saldo"]:,.2f}')
print(f'   CDB Dez/30 final: {cdb_final:,.2f}')