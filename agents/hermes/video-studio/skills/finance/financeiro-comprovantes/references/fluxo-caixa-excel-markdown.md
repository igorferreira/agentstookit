# Fluxo de Caixa — Recalculo Completo (MD + CSV + XLSX)

> ⚠️ **Atualizado em 18/09/2026:** o fluxo agora é **Markdown canônico + motor** (`~/MEGA/Comprovantes/fluxo_caixa/engine/fluxo.py`). O processo atual está em [`fluxo-caixa-source-of-truth.md`](fluxo-caixa-source-of-truth.md). O restante deste arquivo descreve o método anterior (recálculo em Python + XLSX como referência) e serve só de histórico das premissas.


## Quando usar

Quando o usuário pedir "atualiza o fluxo de caixa", "recalcula o fluxo", "projeta o CDB", ou qualquer mudança em:
- Novas despesas (fixas, one-time, recorrentes)
- Mudança de renda (dissídio, aluguel, benefício)
- Novo empréstimo ou alteração no Home Equity
- Impacto de decisão financeira no longo prazo

## Arquivos canônicos (ler antes de recalcular)

| Arquivo | O que extrair |
|---|---|
| `CONTRACHEQUE.md` | CLT líquido + VALLO mensal, mês a mês, com dissídios e 13º já projetados |
| `HOME-EQUITY.md` | Cronograma SAC completo de 50 parcelas (coluna "Parcela") |
| `MAPA-CUSTO-VIDA.md` | Total fixo atual (somar as linhas, não confiar no total escrito) |
| `FLUXO-CAIXA-2026-2030.md` | Faturas existentes, CDB inicial, cenário anterior (referência) |
| `FLUXO-CAIXA-2026-2030.csv` | Verificar se bate com o MD — frequentemente está desatualizado |

## Fluxo de trabalho

### 1. Extrair parâmetros

```python
from decimal import Decimal, ROUND_HALF_UP
def D(s): return Decimal(str(s)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

# CDB inicial — do MD atual (pós-Porto, pré-renda agosto)
cdb_inicial = D('22041.00')

# Renda mensal = CLT líquido + VALLO + Aluguel + 13º (extrair do CONTRACHEQUE.md)
renda['Ago/26'] = D('7995.07') + D('4420.00') + D('2000.00')  # = 14.415,07
renda['Nov/26'] = D('8354.88') + D('4596.80') + D('2000.00') + D('6981.25')  # +13º1

# Home Equity — extrair cada parcela do cronograma SAC
he['Set/26'] = D('4260.69')
he['Out/26'] = D('4220.84')
# ... 50 parcelas decrescentes

# Faturas — do MD existente
faturas['Set/26'] = D('16411')
faturas['Out/26'] = D('12328')
# Ago/27 em diante: custo de vida baseline (~R$ 4.421 ou R$ 4.461)
```

### 2. Coluna "Outros" — despesas não-cartão, não-HE

Adicionar coluna para débitos em conta que não passam por cartão de crédito nem Home Equity:

```python
outros = {}
for key in meses:
    outros[key] = seguro_vida + meli_plus  # recorrentes: R$ 137.85 + R$ 40.00

# One-time expenses — adicionar só no mês específico
outros['Ago/26'] += juros_cheque_especial  # +R$ 4,231.80
```

**Regra:** se a despesa é paga com cartão de crédito → vai em "Faturas". Se é débito em conta → vai em "Outros". One-time expenses só no mês em que ocorrem.

### 3. Recalcular mês a mês

```python
for mes in meses_ordenados:
    r = renda[mes]
    f = faturas.get(mes, D('4421'))
    h = he.get(mes, D('0'))
    o = outros.get(mes, D('177.85'))
    
    saldo = r - f - h - o
    
    # One-time: Paulo Guerra R$ 3.175,46 do CDB em Set/26
    cdb_usou = D('0')
    if mes == 'Set/26':
        cdb_usou = paulo_guerra_cdb
    
    if saldo < 0:
        cdb_usou += abs(saldo)
        cdb_saldo -= abs(saldo)
    else:
        cdb_saldo += saldo
```

### 4. Gate 0 — verificação obrigatória

Antes de finalizar, verificar que a renda sozinha cobre o essencial em TODO mês:

```python
custo_total = custo_vida + seguro_vida + meli_plus  # ~R$ 4.639
for r in resultados:
    renda_base = r['renda'] - decimo_terceiro  # remover 13º
    margem = renda_base - custo_total - r['he']
    if margem < 0:
        print(f"🚨 {r['mes']}: margem negativa!")
```

### 5. Gerar arquivos

**MD** (`FLUXO-CAIXA-2026-2030.md`):
- Cenário versionado (X8, X9, ...)
- Tabelas por ano com colunas: Mês | Renda | Faturas | HE | Outros | Saldo | CDB usou | CDB saldo
- Seção de métricas (CDB mín, CDB final, meses de déficit, gate 0)
- Notas sobre cada premissa alterada

**CSV** (`FLUXO-CAIXA-2026-2030.csv`):
- Mesmas colunas, valores exatos (sem arredondamento)
- Usar como fonte para openpyxl

**XLSX** (`FLUXO-CAIXA-2026-2030.xlsx`):
- Aba 1: Fluxo Mensal (53 linhas, colorido: verde/vermelho/amarelo)
- Aba 2: Resumo Anual (CDB início/fim/variação por ano)
- Aba 3: Custos Fixos (tabela do MAPA-CUSTO-VIDA + total + alerta de teto)

### 6. Sincronizar arquivos dependentes

```bash
# MAPA-CUSTO-VIDA.md — adicionar nova despesa fixa
# Espelho na CARREIRA
cp MAPA-CUSTO-VIDA.md ~/MEGA/Documentos/carreira/MAPA-CUSTO-VIDA.md
```

## Ambiente Python

- **openpyxl**: instalar com `uv pip install openpyxl` (evita PEP 668)
- **Execução**: `python3 << 'PYEOF'` via terminal. **NÃO usar `execute_code`** — é bloqueado em ambientes sem aprovação interativa (cron, gateway). Prefira `write_file` para salvar o script em `/tmp/` e depois `terminal(command='python3 /tmp/script.py')`.
- **Heredoc Python pode falhar**: `python3 << 'PYEOF'` às vezes retorna \"Could not determine home directory\". Nesse caso, usar `write_file` + `terminal` em dois passos.
- **Decimal**: usar `Decimal` para evitar erros de ponto flutuante em 53 meses

## Colunas do fluxo — evolução

| Cenário | Colunas | Quando |
|---|---|---|
| X6 | Mês, Renda, Faturas, HE, Saldo, CDB saldo | Antes de aluguel Diego |
| X7 | + Aluguel Diego R$ 2.000 na renda, + Paulo Guerra | 03/08/2026 |
| X8 | **+ Outros** (seguro vida + Meli+ + juros cheque especial) | 04/08/2026 |

Sempre que surgir uma nova categoria de despesa que não é cartão nem HE, adicionar à coluna "Outros" em vez de inflar "Faturas" ou criar coluna nova.

## Geração dos 3 arquivos (MD + CSV + XLSX)

Após recalcular os 53 meses em Python, gerar os 3 formatos:

**MD** — usar o template da seção "Parâmetros de exibição" abaixo.
**CSV** — `csv.writer` com 8 colunas (Mês, Renda, Faturas, HE, Outros, Saldo, CDB usou, CDB saldo).
**XLSX** — `openpyxl` com 3 abas:
- **Fluxo Mensal**: todas as linhas, colorido (verde/vermelho/amarelo), header congelado.
- **Resumo Anual**: CDB início/fim/variação por ano + meses de déficit + CDB mínimo.
- **Custos Fixos**: tabela do MAPA-CUSTO-VIDA + total + alerta de teto.

Para o código openpyxl completo, ver o script em `scripts/gerar-xlsx-fluxo.py`.

### Parâmetros de exibição no MD

- Cenário versionado (X10, X11, ...) com descrição das mudanças.
- Tabelas por ano com colunas: Mês | Renda | Faturas | HE | Outros | Saldo | CDB usou | CDB saldo.
- Seção de métricas (CDB mín, CDB final, meses de déficit, gate 0).
- Notas sobre cada premissa alterada.
- Emoji 🟢/🔴 na coluna Saldo.
- Coluna "CDB usou" mostra `—` quando zero e `−R$ X.XXX,XX` quando > 0 (inclui Paulo Guerra).

### Pitfalls

- **Atualização em cascata (X+1, X+2...):** quando múltiplas faturas chegam na mesma sessão, é tentador aplicar deltas ao JSON do cenário anterior. Isso funciona para ajustes pequenos (±R$ 200), mas acumula erros de arredondamento e perde rastreabilidade. Após 3+ ajustes incrementais, prefira regenerar o script completo com os parâmetros atualizados.
- **CSV desatualizado**:
- **MD usa números arredondados**: as tabelas do MD arredondam para exibição. Para recálculo, usar os valores exatos do CONTRACHEQUE.md e HOME-EQUITY.md.
- **openpyxl no ambiente Hermes**: o venv não tem pip. Usar `uv pip install openpyxl` ou `pip install --break-system-packages`.
- **Heredoc Python no terminal pode falhar**: `python3 << 'PYEOF'` às vezes retorna "Could not determine home directory". Prefira escrever o script em `/tmp/fluxo_recalc.py` com `write_file` e depois executar com `python3 /tmp/fluxo_recalc.py`. Isso também facilita debug e reexecução.
- **Deduções do CDB precisam ser EXPLÍCITAS**: o X10 não descontava Paulo Guerra (−R$ 3.175,46) do saldo do CDB em Set/26 — o valor aparecia na coluna "CDB usou" mas o CDB saldo não refletia a saída. No X11+ toda dedução do CDB (Paulo Guerra, pagamentos pontuais) deve reduzir `cdb_saldo` diretamente. Não usar a coluna "CDB usou" como apenas informativa.
- **CDB mínimo real vs operacional**: se o CDB mínimo for logo no início (Ago/26, pós-pagamento de todas as faturas, antes da renda entrar), reportar ambos: o mínimo absoluto e o mínimo operacional (menor ponto após a primeira renda do mês).
- **Custo de vida no fluxo vs MAPA**: o fluxo usa custo de vida (~R$ 4.461) + seguro + Meli+ como saída total. O MAPA lista só as fixas. Não somar os dois.
- **Teto de custo estourado**: se o MAPA-CUSTO-VIDA ultrapassar R$ 4.000, sinalizar com ⚠️ mas não alterar o teto sem o usuário confirmar.
- **One-time vs recorrente**: juros de cheque especial é one-time (mês específico). Seguro de vida é recorrente (todos os meses). Não misturar.
- **Empréstimo consignado com data de fim**: quando o usuário informar que um empréstimo em folha termina em data X (ex.: Fev/2027), adicionar o valor da parcela (+R$ 1.000/mês) à renda líquida a partir do mês seguinte. Verificar se o CONTRACHEQUE.md já reflete isso — frequentemente NÃO reflete. Recalcular o fluxo imediatamente; o impacto no CDB de longo prazo pode ser de +R$ 20.000+.
- **Contrato vs app (Home Equity)**: quando o contrato diz uma data de 1ª parcela (10/Set) mas o app mostra outra (10/Out com carência Ago-Set), o APP prevalece. A cláusula 2.3 do contrato CCB diz que os valores são estimativas e se ajustam na data efetiva de liberação. Ver referência `references/ccb-contrato-vs-app.md`.

## Iterative Scenario Tracking (X10, X11, X12...)

When updating the fluxo multiple times in a session as new faturas come in:

### Save JSON per scenario

```python
import json
with open(f'/tmp/fluxo_x{num:02d}.json', 'w') as f:
    json.dump({'cdb_inicial': ..., 'cdb_min': ..., 'resultados': [...]}, f)
```

### Track in INDEX-CENARIOS.md

```
~/MEGA/Comprovantes/2026/_Analises/
├── INDEX-CENARIOS.md          ← tracking of ALL scenarios
├── cenarios/
│   ├── fluxo_x12.json
│   └── fluxo_x16.json         ← current production
```

Each new scenario gets a line with: #, date, event, CDB mínimo, CDB final, delta vs previous. The production MD/CSV/XLSX always reflects the LATEST scenario.

### Persist JSON beyond /tmp

`/tmp/` is wiped on reboot. After each recalculation batch, copy JSON files to `cenarios/` in `_Analises/` for persistence.

### Also track in INDEX-CENARIOS.md

- Matrix of which cartões have been mapped (8 ativos × 5 months)
- Fixed assumptions across all scenarios
- Pedalada analyses (separate section, marked as "not applied to fluxo")
- **Dívida pessoal — confirmar valor explicitamente**: o valor de dívidas pessoais (ex.: Paulo Guerra) pode estar errado no rastreamento se foi estimado. Confirmar o total com Usuário quando o número não vier de documento escrito.
- **Recálculo por delta (rápido)**: quando apenas 1-2 cartões têm faturas novas, carregar o JSON do cenário anterior, aplicar deltas nas faturas, e recalcular mês a mês. Só regenerar tudo quando há mudança estrutural (renda, HE, novo empréstimo).
- **Dívida pessoal — modelar como "Outros", não como "Faturas"**: acordos com pessoas físicas (Paulo Guerra) e transferências bancárias que não passam por cartão de crédito vão na coluna "Outros". Exemplo: parcelas Paulo Guerra 5× R$ 1.000 (Set/26–Jan/27) → `outros['Set/26'] += 1000`. Isso mantém a distinção: "Faturas" = cartão de crédito, "Outros" = débito em conta / transferência. Ver também [`references/fluxo-caixa-source-of-truth.md`](references/fluxo-caixa-source-of-truth.md) para a fonte da verdade dos cenários.
- **HE SAC — base da 1ª parcela**: usar o valor REAL do app C6 (R$ 4.333,63 em Out/26), não o valor calculado por SAC puro (R$ 4.091). O decremento é `amort × 0.017 ≈ R$ 36,96/mês`. Não usar os valores do contrato (R$ [REDACTADO]) que são estimativas pré-desembolso.
- **Tracking de cenários**: cada novo X(N) deve ter seu JSON salvo em `YYYY/_Analises/cenarios/fluxo_xNN.json` e uma linha adicionada ao `INDEX-CENARIOS.md`. Isso mantém rastreabilidade de qual premissa mudou em cada versão. O JSON permite regenerar MD/CSV/XLSX sem perder o histórico. *(legado: não há JSON depois do X35; hoje a versão vigente é o próprio MD canônico.)*
- **Cenário hipotético vs produção**: um what-if pedido pelo usuário (ex: "e se cair R$5.000 da Caixa?") entra como **nova linha em `cenarios` no YAML do MD canônico**, não como novo X. A versão vigente (Xn) só avança quando os dados são confirmados.
