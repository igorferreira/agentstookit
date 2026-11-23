"""
Gerador de XLSX para Fluxo de Caixa — 3 abas (Fluxo Mensal + Resumo Anual + Custos Fixos).

Uso:
    python3 gerar-xlsx-fluxo.py <fluxo_x11.json>

O JSON de entrada deve ter:
{
    "cdb_inicial": float,
    "cdb_min": float,
    "cdb_min_mes": "Out/26",
    "cdb_final": float,
    "cdb_zerou": bool,
    "meses_deficit": int,
    "resultados": [
        {"mes": "Ago/26", "renda": ..., "faturas": ..., "he": ..., "outros": ..., "saldo": ..., "cdb_usou": ..., "cdb_saldo": ...},
        ...
    ]
}
"""

import json, sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


def gerar_xlsx(json_path: str, output_path: str):
    with open(json_path) as f:
        data = json.load(f)

    res = data['resultados']
    wb = Workbook()

    # --- Estilos ---
    header_font = Font(bold=True, size=11, color="FFFFFF")
    header_fill = PatternFill(start_color="2F5496", end_color="2F5496", fill_type="solid")
    green_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    red_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
    yellow_fill = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")
    thin_border = Border(
        left=Side(style='thin'), right=Side(style='thin'),
        top=Side(style='thin'), bottom=Side(style='thin')
    )
    money_fmt = '#,##0.00'

    def style_header(ws, headers, row=1):
        for col, h in enumerate(headers, 1):
            cell = ws.cell(row=row, column=col, value=h)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal='center')
            cell.border = thin_border

    # ============================================================
    # Aba 1: Fluxo Mensal
    # ============================================================
    ws1 = wb.active
    ws1.title = "Fluxo Mensal"

    headers1 = ['Mês', 'Renda', 'Faturas', 'HE', 'Outros', 'Saldo', 'CDB usou', 'CDB saldo']
    style_header(ws1, headers1)

    for i, r in enumerate(res, 2):
        ws1.cell(row=i, column=1, value=r['mes']).border = thin_border
        for j, key in enumerate(['renda', 'faturas', 'he', 'outros', 'saldo', 'cdb_usou', 'cdb_saldo'], 2):
            cell = ws1.cell(row=i, column=j, value=r[key])
            cell.number_format = money_fmt
            cell.border = thin_border

        # Colorir saldo
        saldo_cell = ws1.cell(row=i, column=6)
        saldo_cell.fill = red_fill if r['saldo'] < 0 else green_fill

        # Colorir CDB saldo (amarelo se próximo do mínimo)
        cdb_cell = ws1.cell(row=i, column=8)
        if r['cdb_saldo'] < data['cdb_min'] * 1.05:
            cdb_cell.fill = yellow_fill
        else:
            cdb_cell.fill = green_fill

    for col in range(1, 9):
        ws1.column_dimensions[get_column_letter(col)].width = 14
    ws1.freeze_panes = 'A2'

    # ============================================================
    # Aba 2: Resumo Anual
    # ============================================================
    ws2 = wb.create_sheet("Resumo Anual")
    headers2 = ['Ano', 'CDB Início', 'CDB Fim', 'Variação', 'Meses Déficit', 'CDB Mínimo']
    style_header(ws2, headers2)

    # Agrupar por ano
    anos = {'2026': [], '2027': [], '2028': [], '2029': [], '2030': []}
    for r in res:
        ano = '20' + r['mes'].split('/')[1]
        anos[ano].append(r)

    row = 2
    for ano in ['2026', '2027', '2028', '2029', '2030']:
        meses = anos[ano]
        if not meses:
            continue
        if ano == '2026':
            cdb_ini = data['cdb_inicial']
        else:
            # CDB início = CDB saldo do último mês do ano anterior - saldo daquele mês
            ano_ant = str(int(ano) - 1)
            ultimo_mes_ant = anos[ano_ant][-1]
            cdb_ini = ultimo_mes_ant['cdb_saldo']

        cdb_fim = meses[-1]['cdb_saldo']
        cdb_min_ano = min(m['cdb_saldo'] for m in meses)
        deficits = sum(1 for m in meses if m['saldo'] < 0)
        variacao = cdb_fim - cdb_ini

        for col, val in enumerate([ano, cdb_ini, cdb_fim, variacao, deficits, cdb_min_ano], 1):
            cell = ws2.cell(row=row, column=col, value=val)
            cell.border = thin_border
            if col >= 2:
                cell.number_format = money_fmt

        ws2.cell(row=row, column=4).fill = red_fill if variacao < 0 else green_fill
        row += 1

    for col in range(1, 7):
        ws2.column_dimensions[get_column_letter(col)].width = 16

    # ============================================================
    # Aba 3: Custos Fixos
    # ============================================================
    ws3 = wb.create_sheet("Custos Fixos")
    headers3 = ['Item', 'Categoria', 'Valor/mês', 'Período']
    style_header(ws3, headers3)

    custos = [
        ('Condomínio', 'Moradia', 1019.73, 'Recorrente'),
        ('Light (média)', 'Energia', 1197.95, 'Recorrente'),
        ('Naturgy (Gás)', 'Gás', 121.32, 'Recorrente'),
        ('Claro', 'Telefone', 325.77, 'Recorrente'),
        ('Vivo', 'Telefone', 105.13, 'Recorrente'),
        ('Smartfit', 'Academia', 139.00, 'Recorrente'),
        ('Karatê', 'Academia', 100.00, 'Recorrente'),
        ('Crossfit', 'Academia', 200.00, 'Recorrente'),
        ('ChatGPT Plus', 'IA', 101.94, 'Recorrente'),
        ('Gemini Advanced', 'IA', 101.89, 'Recorrente'),
        ('Claude Pro', 'IA', 101.94, 'Recorrente'),
        ('Manus Pro Entry', 'IA', 101.94, 'Recorrente'),
        ('Meli+ (Disney+)', 'Streaming', 40.00, 'Recorrente'),
        ('Seguro de Vida Itaú', 'Seguro', 137.85, 'Ago-Set/26'),
        ('Combustível', 'Transporte', 300.00, 'Recorrente'),
        ('Gastos livres', 'Lazer', 1000.00, 'Recorrente (reduzido 31/07)'),
    ]

    for i, (item, cat, valor, periodo) in enumerate(custos, 2):
        for col, val in enumerate([item, cat, valor, periodo], 1):
            cell = ws3.cell(row=i, column=col, value=val)
            cell.border = thin_border
            if col == 3:
                cell.number_format = money_fmt

    total_row = len(custos) + 2
    ws3.cell(row=total_row, column=1, value="TOTAL FIXO").font = Font(bold=True)
    ws3.cell(row=total_row, column=1).border = thin_border
    ws3.cell(row=total_row, column=3, value=sum(c[2] for c in custos)).number_format = money_fmt
    ws3.cell(row=total_row, column=3).font = Font(bold=True)
    ws3.cell(row=total_row, column=3).border = thin_border

    # Teto
    tr = total_row + 1
    ws3.cell(row=tr, column=1, value="TETO (Igor)").font = Font(bold=True)
    ws3.cell(row=tr, column=1).border = thin_border
    ws3.cell(row=tr, column=3, value=4000.00).number_format = money_fmt
    ws3.cell(row=tr, column=3).font = Font(bold=True, color="FF0000")
    ws3.cell(row=tr, column=3).border = thin_border
    ws3.cell(row=tr, column=4, value="⚠️ Estourado Ago-Set (R$4.094)").border = thin_border

    for col in range(1, 5):
        ws3.column_dimensions[get_column_letter(col)].width = 20

    wb.save(output_path)
    print(f"✅ XLSX gerado: {output_path}")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Uso: {sys.argv[0]} <fluxo.json> <output.xlsx>")
        sys.exit(1)
    gerar_xlsx(sys.argv[1], sys.argv[2])
