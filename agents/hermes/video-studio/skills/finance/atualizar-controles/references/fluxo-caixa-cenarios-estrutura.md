# Fluxo de Caixa — Estrutura `fluxo_caixa/` (X23)

> **Criado:** 13/08/2026
> **Skill:** `fluxo-caixa-cenarios`

## 📁 Estrutura obrigatória

```
~/MEGA/Comprovantes/fluxo_caixa/
├── cenario_atual/                          # continuar na [EMPRESA]
│   ├── X23_atual.xlsx                      # XLSX canônico (8 sheets)
│   ├── X23_atual.md                        # derivado
│   ├── X23_atual.pdf                       # apresentação
│   └── X23_atual.csv                       # export Excel
│
├── cenario_demissao/                       # dispensa sem justa causa
│   ├── rescisao_YYYY-MM.md                 # atualizado mensalmente via cron
│   ├── rescisao_YYYY-MM.json
│   ├── janela_otima_demissao.md            # análise PhD da janela
│   └── janela_otima_demissao.json
│
├── cenario_pedido_demissao/                # pedido demissão
│   ├── comparativo_cenarios_saida.md        # tabela 9 cenários
│   ├── comparativo_cenarios_saida.json
│   └── comparativo_cenarios_saida.pdf
│
├── calculos_auxiliares/                    # scripts Python reutilizáveis
│   ├── calcular_rescisao.py
│   ├── calcular_janela_otima.py
│   └── calcular_cenarios_saida.py
│
├── historico/                              # versões antigas (X19, X20, X21, X22)
│
└── README.md
```

## 🔢 Premissas críticas (atualizadas 13/08/2026)

### Admissão e salário
- Admissão: **22/05/2023**
- Salário bruto base: **R$ [REDACTADO]** (triênio incluso)
- Dissídio anual: **4,32%** (FEAAC ago/26)

### Rendimentos mensais
- **VALLO: R$ 4.420/mês (FIRME, nunca atrasa)** — confirmado por Usuário em 13/08/2026
- Aluguel Diego: R$ 2.000/mês

### Custo de vida e reservas
- Custo de vida Set+: **R$ 4.421**
- Imprevistos: **R$ 1.000/mês** (decisão 13/08/2026)
- 13º salário:
  - Nov/26: R$ 6.950 (50% bruto)
  - Dez/26: R$ 5.400 (~39% líquido)
  - 2027+: +5% (1º ano) ou +10% (anos seguintes)

### CDB e HE
- CDB Inicial: **R$ 29.167,14** (app C6 ~R$ 29.155,70)
- CDB yield: 1% a.m.
- HE principal: **R$ [REDACTADO]** (CCB [REDACTADA])
- HE início 1ª parcela completa: **10/Out/2026**
- HE fim: **10/Set/2030** (50 meses)

### 6 cartões em negociação (R$ 62.744)

| Cartão | Valor |
|---|---:|
| RecargaPay | R$ 14.254 |
| PAN Méliuz 4863 | R$ 12.159 |
| PAN Buscapé 5014 | R$ 9.758 |
| Casas Bahia 6015 | R$ 8.628 |
| Inter 1982 | R$ 12.717 |
| Digio | R$ 5.228 |
| **TOTAL** | **R$ 62.744** |

**BrasilCard R$ 647** foi REMOVIDO da negociação em 13/08/2026 — Usuário vai pagar mensalmente.

### Estratégia
- Só pagar os 6 cartões quando **CDB = R$ 150k** (atinge em Fev/28 no X23)
- CDB final Dez/30 projetado: R$ 608.485 (X23) ou R$ 577.550 (X20)

### Cenário Demissão (Lei 12.506/2011)
- Aviso prévio: `30 + min(60, ⌊anos⌋ × 3)` dias
- Dispensa sem justa causa em 13/08/2026:
  - **Líquido empregador**: R$ 52.746,92
  - **Multa 40% FGTS**: R$ 17.086,15 (saque-aniversário retém)
  - **Saldo bloqueado (libera)**: R$ 39.495,35
  - **TOTAL CAIXA IMEDIATO**: R$ 94.956,24
  - Cobertura: 21,48 meses a R$ 4.421/mês
- **Seguro-desemprego**: NÃO elegível (Usuário confirmou 27/07/2026)
- **VALLO NUNCA entra na rescisão** (decisão Usuário 23/07/2026)

## ⏰ Cron jobs ativos

| Job ID | Schedule | Função |
|---|---|---|
| `e247555646ba` | `0 9 1 * *` | Recalcula rescisão todo dia 1º às 09:00 |
| `5e02d98f0186` | `0 23 * * *` | Resumo diário de conversas (todo dia 23:00) |

## 🎯 Janela ótima para demissão (X23)

| Target | Data | Tempo de casa | Margem |
|---|---|---|---|
| 🟢 Mínimo (6 cartões + BrasilCard) | Ago/26 | 3,3 anos | R$ 21.094 |
| 🟡 Médio (+ HE saldo) | **Ago/28** | 5,3 anos | 0,6 meses |
| 🔴 Completo (+ 24m vida) | Set/30 | 7,3 anos | 22,7 meses |

**Por que Ago/2028:** três alavancas simultâneas — dissídio Ago/28, 5 anos completos (aviso +3 dias), HE saldo cai para R$ 59.570.

## 📋 9 cenários comparativos (X23)

| Data | Anos | Aviso | Dispensa | Pedido disp | Pedido desc | Cobre TUDO? |
|---|---:|---:|---:|---:|---:|:---:|
| Ago/26 | 3,28 | 39 | R$ 85.929 | R$ 39.170 | R$ 25.781 | ❌ |
| Mai/27 | 4,00 | 42 | R$ 87.261 | R$ 28.233 | R$ 14.844 | ❌ |
| Ago/27 | 4,28 | 42 | R$ 104.877 | R$ 40.191 | R$ 26.802 | ❌ |
| Mai/28 | 5,00 | 45 | R$ 106.302 | R$ 28.782 | R$ 15.393 | ❌ |
| **Ago/28** | **5,28** | **45** | **R$ 125.348** | R$ 41.256 | R$ 27.867 | **✅** |
| Mai/29 | 6,00 | 48 | R$ 126.782 | R$ 29.354 | R$ 15.965 | ✅ |
| Ago/29 | 6,28 | 48 | R$ 147.346 | R$ 42.367 | R$ 28.978 | ✅ |
| Mai/30 | 7,00 | 51 | R$ 148.834 | R$ 29.951 | R$ 16.562 | ✅ |
| Ago/30 | 7,28 | 51 | R$ 171.011 | R$ 43.526 | R$ 30.137 | ✅ |

## 🚨 Pitfalls críticos (X23)

### 1. BrasilCard removido
Atualizar lista para **6 cartões** (não 7) — total R$ 62.744 (não R$ 63.391)

### 2. CDB_Inicial mudou
Usar `R$ 29.167,14` (não R$ 22.168 da estimativa antiga)

### 3. 13º anual projetado
Incluir Nov/Dez de CADA ANO (2026, 2027, 2028, 2029, 2030)
- Usar `mes.startswith('Nov')` (NÃO `endswith`)
- Multiplicador: ×1.05 (2027) ou ×1.10 (2028+)

### 4. Imprevistos R$ 1.000/mês
Linha separada, não dentro de Outros
- Gera 3 meses de déficit (Set/26, Out/26, Jan/27) em vez de 2

### 5. VALLO nunca atrasa
Pode ser tratado como receita garantida

### 6. XLSX agora tem 8 sheets
(antigo era 7)
1. Inputs
2. Fluxo Mensal
3. CDB Evolução
4. Cenário Desemprego
5. Estratégia Negociação
6. Sensitivity
7. Checks
8. **Cenários Saída** (novo no X23)

## 📂 Scripts prontos (não modificar sem aviso)

- `calculos_auxiliares/calcular_rescisao.py` — gera rescisao_YYYY-MM.md/json
- `calculos_auxiliares/calcular_janela_otima.py` — gera janela_otima_demissao.md/json
- `calculos_auxiliares/calcular_cenarios_saida.py` — gera comparativo_cenarios_saida.{md,json,pdf}

Todos idempotentes — podem rodar várias vezes sem corromper dados.