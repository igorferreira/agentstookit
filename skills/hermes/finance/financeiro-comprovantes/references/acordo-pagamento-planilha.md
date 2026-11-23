# Acordo de Pagamento — Planilha + Compartilhamento

## Quando usar

Quando Igor fecha um acordo de pagamento parcelado (amigo, familiar, credor informal) e precisa de:

1. Planilha de controle formatada (xlsx)
2. Compartilhamento via Google Drive
3. Registro no controle financeiro local

## Fluxo

### 1. Criar a planilha

Usar `openpyxl` com formatação profissional:

- **Título:** "Acordo <Nome Credor> × Igor Ferreira"
- **Cabeçalho:** # | Vencimento | Valor | Status | Comprovante
- **Cores:** azul escuro no cabeçalho, verde claro na entrada, cinza alternado nas parcelas
- **Totais:** linha de TOTAL em destaque
- **Rodapé:** "Sem juros. Sem multa. Combinado entre amigos. 🤝"
- **Moeda:** `R$ #,##0.00`

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
# title_font = Font(size=14, bold=True, color='1F4E79')
# header_fill = PatternFill(start_color='1F4E79', fgColor='1F4E79', fill_type='solid')
# green_fill = PatternFill(start_color='D9F2D9', fgColor='D9F2D9', fill_type='solid')
# money_format = 'R$ #,##0.00'
```

### 2. Salvar em dois locais

```bash
# Local (MEGA — backup)
~/MEGA/Comprovantes/YYYY/YYYY_MM_MES/AAAA-MM-DD_NOME-ACORDO.xlsx

# Google Drive (Insync — compartilhamento)
~/Insync/GoogleDrive/igorferreirabr/Divida/AAAA-MM-DD_NOME-ACORDO.xlsx
```

O Insync sincroniza automaticamente → Igor gera link de compartilhamento → envia por email.

### 3. Criar controle Markdown

Arquivo `.md` no MEGA com:

- Tabela de cronograma (# | Vencimento | Valor | Status)
- Seção de pagamentos realizados (Data | Valor | Origem | Comprovante)
- Total e condições do acordo

### 4. Atualizar controles

- `_saldos/SALDO_<BANCO>.md` — débito da conta usada
- `_controles/CONTROLE_SALDO_CONTAS.md` — se afetar projeção
- `ORCAMENTO-AREAS.md` — se afetar consolidação mensal

### 5. Resposta amigável

Se for amigo próximo, usar tom pessoal e quente:

- Nome, tempo de amizade
- Confirmar valores sem formalidade
- Oferecer planilha como "pra gente controlar bonitinho"
- Emojis leves (🤝, 🙏, 😄)
- Sem juridiquês

## Exemplo: Paulo Guerra (10/08/2026)

- Valor: R$ 10.000 → R$ 5.000 entrada + 5× R$ 1.000
- Origem pagamento: Resgate CDB C6 → Itaú
- Planilha: `2026-08-10_PAULO-GUERRA-ACORDO.xlsx`
- Controle: `2026-08-10_PAULO-GUERRA-CONTROLE-PAGAMENTO.md`
- Amizade: 10 anos
