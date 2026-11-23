# PhD em Matemática Financeira — Equações e Fórmulas Canônicas

> **Referência de:** `planejamento-financeiro/SKILL.md` (Modo PhD)
> **Skill relacionada:** `phd-financas-pessoais` (referência de domínio, mais extensa)

## 1. Rescisão CLT (Brasil — Lei 12.506/2011)

### 1.1 Aviso prévio (dias)
```
aviso_prévio(anos) = 30 + min(60, ⌊anos_completos⌋ × 3)
```
| Anos completos | Dias aviso |
|---:|---:|
| 0 (menos de 1) | 30 |
| 1 | 33 |
| 2 | 36 |
| 3 | 39 |
| 4 | 42 |
| 5 | 45 |
| 6 | 48 |
| 7+ | 51 |

### 1.2 FGTS acumulado
```
FGTS(t) = base × (1 + taxa_mensal)^n + salário × 0.08 × n − saques_aniversário
```
- `base` = saldo oficial do extrato Caixa
- `taxa_mensal` ≈ 0,3% (~3,6% a.a. TR + remuneração)
- `salário × 0,08` = depósito mensal (8% FGTS)
- `saques_aniversário` = COD 60 já sacados (set/24, set/25...)

### 1.3 Multa 40% (só dispensa sem justa causa)
```
multa_40% = 0,40 × FGTS_total
```
**Saque-aniversário**: multa 40% BLOQUEADA em condições normais; LIBERA integralmente na dispensa sem justa causa (junto com saldo bloqueado).

### 1.4 13º proporcional
```
13°(mês, com_aviso) = (m + AP/30) / 12 × bruto
```
Limitado a 12/12. Se `com_aviso=True` (dispensa), soma a projeção do aviso.

### 1.5 Férias proporcionais + 1/3 constitucional
```
férias_prop = meses_PA / 12 × bruto × 4/3
```
Período aquisitivo: 22/05 a 21/05 (aniversário de admissão). Cap em 12/12.

### 1.6 INSS + IRRF (tabela 2026)
```
INSS = min(bruto × 0,10, 815,06)
IRRF = max(0, (bruto − INSS) × 0,15 − 354,80)   # dedução simplificada
```

### 1.7 Caixa imediato (consolidado)
```
DISPENSA:
  caixa_imediato = líquido_empregador + multa_40% + saldo_bloqueado_saque_aniv
  onde:
    líquido_empregador = bruto_emp − INSS − IRRF
    saldo_bloqueado_saque_aniv = FGTS − multa_40%   # LIBERA na dispensa

PEDIDO DEMISSÃO (sem multa, sem saldo bloqueado):
  se aviso_dispensado:
    caixa = líquido_empregador
  se aviso_descontado:
    caixa = líquido_empregador − (salário − empréstimo_folha)
```

## 2. Janela ótima para sair

**Problema:** encontrar a data `t*` em que `caixa_imediato(t*) ≥ alvo(t*)`.

```
alvo(t) = Σ_cartões_em_negociação + BrasilCard + HE_saldo(t)
HE_saldo(t) = max(0, HE_principal − HE_amortização × meses_HE_pagos(t))
```

**Implementação:** simular para datas discretas (Ago/26, Mai/27, Ago/27, Mai/28, Ago/28, ...) e reportar a primeira data em que `caixa ≥ alvo`.

**Resultado típico para Igor:**
- Quitar só 6 cartões: HOJE (margem R$ 21k)
- Quitar tudo incluindo HE: **Ago/2028** (5a3m)
- Margem confortável: Ago/2030 (7a3m, sobra R$ 171k)

## 3. Estratégia de quitação de dívidas

| Estratégia | Regra | Vantagem | Quando usar |
|---|---|---|---|
| **Snowball** | Quitar menor saldo primeiro | Psicológica (motivação) | Múltiplas dívidas pequenas, quer vencer rápido |
| **Avalanche** | Quitar maior juros primeiro | Matemática (otimiza $ pago) | Quer minimizar custo total |
| **Oportunidade** | Só quita se `taxa_dívida > yield_disponível` | Financeira | CDB rende mais que a dívida custa |

**Regra de decisão:**
```
quitar_se = taxa_dívida > yield_alternativa + buffer_risco
   ex: quitar cartão a 15% se CDB rende 12%? NÃO. Quitar cartão a 18%? SIM.
```

## 4. Reserva de emergência

| Métrica | Valor |
|---|---|
| Mínimo absoluto | 3 meses de despesas |
| Confortável | 6 meses de despesas |
| Ideal com dependentes | 9-12 meses |

**Regra dos 4% (Trinity Study):**
```
patrimônio_aposentadoria = 25 × despesas_anuais
```

## 5. Rendimento e valor presente

```
VPL(cf, r) = Σ cf_t / (1 + r)^t
TIR: VPL(cf, TIR) = 0
Sharpe = (retorno_esperado − taxa_livre) / desvio_padrão
Drawdown = (pico − vale) / pico
```

## 6. Custos de crédito no Brasil (referência 2026)

| Produto | Taxa a.m. | Taxa a.a. |
|---|---:|---:|
| CDB (pós-fixado CDI 100%) | ~0,87% | ~11% |
| CDB (pós-fixado CDI 120%) | ~1,04% | ~13% |
| PIX no crédito Carrefour | 4,99% | ~79% |
| Cheque especial Nubank | ~8% | ~152% |
| Rotativo cartão | ~15% | ~435% |
| Empréstimo pessoal | ~3-7% | ~42-125% |

**Regra de ouro:** reserve de emergência vence qualquer investimento arriscado.

## 7. Cron job ativo (Modo PhD)

```
job_id: e247555646ba
schedule: "0 9 1 * *"        # 1º de cada mês, 09:00 BRT
script: python3.12 ~/MEGA/Comprovantes/fluxo_caixa/calculos_auxiliares/calcular_rescisao.py
output: ~/MEGA/Comprovantes/fluxo_caixa/cenario_demissao/rescisao_YYYY-MM.{md,json}
```

## 8. Janela ótima — saída rápida (1-página)

```
                              Dispensa    Pedido (disp)   Cobre TUDO?
Hoje (Ago/26)                 R$ 85.929    R$ 39.170       ❌ (HE alto)
Mai/27 (4 anos)               R$ 87.261    R$ 28.233       ❌
Ago/27 (4a3m, dissídio)       R$ 104.877   R$ 40.191       ❌
Mai/28 (5 anos)               R$ 106.302   R$ 28.782       ❌
⭐ Ago/28 (5a3m, dissídio + 5a) R$ 125.348 R$ 41.256      ✅ JANELA ÓTIMA
Mai/29 (6 anos)               R$ 126.782   R$ 29.354       ✅ (margem +5,2m)
Ago/29 (6a3m)                 R$ 147.346   R$ 42.367       ✅ (margem +11,5m)
Mai/30 (7 anos)               R$ 148.834   R$ 29.951       ✅ (margem +16,1m)
Ago/30 (7a3m, HE quitado)     R$ 171.011   R$ 43.526       ✅ (margem +22,7m)
```

## 9. Scripts em `calculos_auxiliares/`

| Script | Função |
|---|---|
| `calcular_rescisao.py` | Calcula rescisão em uma data (atualiza mensalmente via cron) |
| `calcular_janela_otima.py` | Encontra primeira data em que dispensa cobre todas as dívidas |
| `calcular_cenarios_saida.py` | Gera 9 cenários comparativos (dispensa vs pedido demissão) |

Todos usam as funções matemáticas acima. Manter atualizados quando premissas mudarem (dissídio, salário, datas).

## 10. Outputs padrão (sempre entregar 5)

| # | Formato | Ferramenta |
|---|---|---|
| 1 | PDF | `pandoc + wkhtmltopdf --no-background` |
| 2 | XLSX | `openpyxl` (skill excel-author) |
| 3 | MD | Derivado do XLSX ou escrito direto |
| 4 | JSON | `json.dump(..., indent=2)` |
| 5 | Script Python | Em `calculos_auxiliares/` — reutilizável |