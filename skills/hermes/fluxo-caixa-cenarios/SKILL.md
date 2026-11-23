---
name: fluxo-caixa-cenarios
description: Gera e mantém a pasta fluxo_caixa/ com cenários de saída (atual, demissão, pedido demissão). Inclui scripts Python para janela ótima, comparativo de 9 cenários, e rescisão dinâmica mensal via cron job. Use sempre que Usuário mencionar cenários de saída, demissão, pedido demissão, ou "como fico se for mandado embora".
version: 1.0.0
author: Hermes Agent (13/08/2026)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [fluxo-caixa, rescisao, demissao, janela-otima, cenarios, python]
    related_skills: [atualizar-controles, phd-financas-pessoais, auditoria-consistencia-financeira, financeiro-comprovantes]
---

# Fluxo de Caixa — Cenários de Saída

Skill class-level para gerenciar a pasta `~/MEGA/Comprovantes/fluxo_caixa/` com sub-cenários.

**Escopo atual:** a família canônica 2026–2036 é gerada pelo procedimento em `atualizar-controles`. Nomes de arquivos, scripts, âncoras e valores 2026–2030 descritos adiante são referências históricas; não os reutilizar como dados atuais sem reconciliação com as fontes vigentes.

## 📁 Estrutura obrigatória

```
~/MEGA/Comprovantes/fluxo_caixa/
├── FLUXO-CAIXA-2026-2030.md        # Fonte canônica (Markdown)
├── FLUXO-CAIXA-2026-2030.xlsx      # Espelho gerado automaticamente
├── engine/                         # Motor de cálculo canônico
│   └── fluxo.py                    # Recalcula tabelas do MD e regera XLSX
├── dashboard/                      # Dashboard financeiro visual
│   ├── gerar_dashboard.py          # Script de compilação dos artefatos web
│   ├── servidor_local.py           # Servidor HTTP dedicado na porta 8766 (serve publicacao/)
│   ├── src/                        # Modelos e templates (modelo_dashboard.py)
│   └── publicacao/                 # Artefatos finais (dashboard.html, dados_dashboard.json)
├── cenario_atual/                  # X<n>_atual.{xlsx,md,pdf,csv} — continuar na [EMPRESA]
├── cenario_demissao/               # dispensa sem justa causa
│   ├── rescisao_YYYY-MM.{md,json}  # atualizado via cron
│   ├── janela_otima_demissao.{md,json}
├── cenario_pedido_demissao/        # pedido demissão
│   ├── comparativo_cenarios_saida.{md,json,pdf}
├── calculos_auxiliares/            # scripts Python reutilizáveis
│   ├── calcular_rescisao.py
│   ├── calcular_janela_otima.py
│   └── calcular_cenarios_saida.py
├── historico/                      # versões antigas (X19, X20, ...)
└── README.md
```

## 🔢 Scripts canônicos (matemática PhD)

### `calcular_rescisao.py` (cron mensal)

Gera `rescisao_YYYY-MM.md` com base em:
- `ADMISSAO = 22/05/2023`
- `SALARIO_BRUTO_BASE = [REDACTADO]` (triênio incluso)
- Lei 12.506/2011: aviso prévio = `30 + min(60, ⌊anos⌋ × 3)` dias
- FGTS: `42.715 × (1,003)^n + salario × 0,08 × n − 16.000` (saques aniversário)
- HE: `max(0, 108.720 − 2.174 × meses_pagos)` (SAC)
- INSS 10% (faixa 2) + IRRF 15% com dedução R$ 354,80
- Cenários: pedido demissão (aviso dispensado/descontado) + dispensa sem justa causa

**Output:** JSON com `data_referencia`, `anos_completos`, `aviso_previo_dias`, `fgts_acumulado`, `dispensa_sem_justa_causa.caixa_imediato`, `cartoes_negociacao_total` (R$ 62.744 — 6 cartões, BrasilCard removido em 13/08/2026)

### `calcular_janela_otima.py` (sob demanda)

Calcula quando dispensa cobre TUDO (6 cartões + BrasilCard + HE saldo):
- Projeção mês-a-mês (53 meses, Ago/26 → Dez/30)
- 3 targets:
  - 🟢 Mínimo (R$ 63.391): atinge em Ago/26
  - 🟡 Médio (+ HE saldo): atinge em **Ago/2028** (5a3m)
  - 🔴 Completo (+ 24m vida): atinge em Set/2030 (7a3m)
- **Ago/2028 é a janela ótima** — três alavancas se cruzam:
  - Dissídio anual Ago/28 → +R$ 615 no bruto
  - Aviso prévio 5 anos completos (Mai/28) → +3 dias = +R$ 1.341
  - HE já pago 22 meses → saldo cai para R$ 59.570

### `calcular_cenarios_saida.py` (sob demanda)

9 cenários comparativos: Ago/26, Mai/27, Ago/27, Mai/28, Ago/28, Mai/29, Ago/29, Mai/30, Ago/30
- Para cada data: salário bruto (com dissídio Ago de cada ano), aviso prévio, dispensa + 2 versões de pedido demissão
- Gera `comparativo_cenarios_saida.{md,json,pdf}`
- Planilha XLSX: nova aba `Cenários Saída` (dados + gráfico de barras + 10 funções matemáticas)

## ⏰ Cron jobs ativos

| Job ID | Schedule | Comando | Função |
|---|---|---|---|
| `e247555646ba` | `0 9 1 * *` | `python3.12 ~/MEGA/Comprovantes/fluxo_caixa/calculos_auxiliares/calcular_rescisao.py` | Recalcula rescisão todo dia 1º às 09:00 |

## 🌐 Dashboard Financeiro e Exposição Externa

Para atualizar e expor o dashboard do fluxo de caixa:
1. **Regenerar o modelo canônico:** Executar `python3.12 ~/MEGA/Comprovantes/fluxo_caixa/engine/fluxo.py`.
2. **Compilar os artefatos do dashboard:** Executar `python3.12 ~/MEGA/Comprovantes/fluxo_caixa/dashboard/gerar_dashboard.py`.
3. **Subir o servidor local dedicado (background):** Executar `python3.12 ~/MEGA/Comprovantes/fluxo_caixa/dashboard/servidor_local.py` (porta 8766).
4. **Subir túnel ngrok (background):** Executar `/usr/local/bin/ngrok http 8766`.
5. **Capturar a URL pública:** Consultar `curl -s http://127.0.0.1:4040/api/tunnels`.
6. **Validar rotas com bypass ngrok:** `curl -s -I -H "ngrok-skip-browser-warning: 1" <URL_NGROK>/dashboard.html`.

### Pitfall 8: Servir dashboard na pasta errada ou com http.server genérico
Nunca rodar `python3 -m http.server 8766` dentro de `fluxo_caixa/` ou `fluxo_caixa/dashboard/`. Os arquivos gerados residem em `dashboard/publicacao/`. Usar sempre `dashboard/servidor_local.py`, que já faz o bind correto, configura CORS e resolve a rota `/` diretamente para `dashboard.html`.

### Pitfall 9: Status de pagamento não reconhecido no dashboard
O parser `modelo_dashboard.py` extrai pagamentos de `2026-XX_00_CONTROLE_PAGAMENTOS.md` checando a coluna Status ou Comprovante. Para que um item conste como pago no dashboard (`pago: True`), o texto deve conter explicitamente `✅`, `pago` ou `COMPROVANTE-PAGAMENTO`. Lançamentos como "A definir" ou sem emoji/palavra-chave permanecem como em aberto.

## 📋 Atualização do XLSX principal

Quando gerar/atualizar cenário:
1. **Cenário atual**: copiar `FLUXO-CAIXA-2026-2030.{xlsx,md,pdf,csv}` para `cenario_atual/X<n>_atual.*`
2. **Planilha raiz**: manter em `~/MEGA/Comprovantes/FLUXO-CAIXA-2026-2030.{xlsx,md,pdf,csv}` (canônico)
3. **NOVA aba no XLSX**: `Cenários Saída` (a partir do X23) com:
   - Tabela 9 cenários × 12 colunas
   - Gráfico de barras (caixa dispensa vs pedido)
   - 10 funções matemáticas aplicadas (Courier New font)
   - Recomendações com emojis (🟢🟡🔴)

## Premissas financeiras — fontes dinâmicas

Os valores e âncoras numéricas dos exemplos deste skill são históricos, não inputs atuais. Antes de cada simulação, reconciliar as fontes vigentes de salário, parcelas, CDB e dívidas (`CONTRACHEQUE.md`, `HOME-EQUITY.md`, `_saldos/SALDO_C6.md`, comprovantes datados, `ENDIVIDAMENTO.md` e fichas relevantes). Distinguir saldo de abertura do horizonte e último saldo confirmado, sempre com data; saldo bloqueado não é caixa disponível. Separar valores comprovados de estimativas e não inferir líquido a partir de bruto. Se faltarem dados para uma verba rescisória ou outra entrada, excluir ou bloquear somente o componente dependente em vez de inventar valor. Para o procedimento de prova e validação, seguir `atualizar-controles`.

## 🚨 Pitfalls críticos

### Pitfall 1: `'Nov/27'.endswith('Nov')` retorna False
A string `'Nov/27'` termina com `'27'`, NÃO com `'Nov'`. Para detectar meses em qualquer ano:
```python
# ERRADO
if mes.endswith('Nov') or mes.endswith('Dez'):
# CERTO
if mes.startswith('Nov') or mes.startswith('Dez'):
```

### Pitfall 2: Nunca hardcodar a dívida dos cartões em negociação
A posição muda com novas operações, encargos e acordos. Antes de gerar cada cenário:
1. Ler `~/MEGA/Comprovantes/ENDIVIDAMENTO.md`.
2. Reconciliar cada valor com a ficha do cartão.
3. Usar o total mínimo documentado e separar tarifas/IOF/juros ainda pendentes.
4. No X28 (14/08/2026), a posição mínima dos 6 cartões é **R$ 78.659,77**; o Digio está em pelo menos R$ 3.065,30 após a operação prevista de R$900 para o 99Pay.

### Pitfall 3: não confundir saldo de abertura com saldo atual do CDB
Nunca herdar automaticamente o saldo inicial do cenário anterior nem usar o saldo atual para substituir a abertura de um horizonte histórico. Reconciliar o saldo de abertura com a evidência válida na data inicial do modelo; registrar separadamente o último saldo real confirmado, sua data e eventual bloqueio. Consultar `_saldos/SALDO_C6.md` e o comprovante/extrato correspondente. Saldo bloqueado não é caixa disponível; sem evidência posterior, não presumir saldo ou data de liberação.

### Pitfall 4: 13º só inclui 2026 se usar `Decimo_1/Decimo_2`
Para Nov/26 e Dez/26, usar `Decimo_1` (R$ 6.950) e `Decimo_2` (R$ 5.400) hardcoded.
Para Nov/Dez 2027+, usar `Decimo_Anual_Nov × 1.05` (1º ano) ou `× 1.10` (anos seguintes).

### Pitfall 5: VALLO NUNCA entra na rescisão
Usuário declarou em 23/07/2026 que VALLO é rendimento disponível MAS **NÃO entra em cálculo rescisório** (incluindo o depósito extra do 13º). Respeitar SEMPRE.

### Pitfall 6: PDF aprovado exige auditoria visual após cada alteração
Recalcular o XLSX no LibreOffice, exportar MD/CSV/JSON e só então gerar o PDF. Renderizar todas as páginas e verificar:
- títulos órfãos;
- tabelas separadas do título ou sem cabeçalho;
- páginas vazias/quase vazias;
- cortes e sobreposições.

Para tabelas longas, dividi-las manualmente com cabeçalho repetido. Colocar a quebra de página **antes da seção inteira**, não depois de uma tabela que possa ser empurrada pelo motor do PDF.

### Pitfall 7: `cenario_atual/` deve conter somente a versão vigente
Mover X anteriores para `fluxo_caixa/historico/X<n>/`. Na raiz, manter cópias byte a byte idênticas do cenário vigente em `FLUXO-CAIXA-2026-2030.{md,xlsx,csv,pdf}`. Evitar cópias paralelas em `_controles/`; manter apenas um ponteiro para os arquivos canônicos.

## 📚 Referências

| Arquivo | Conteúdo |
|---|---|
| `references/calculos_rescisao_formulas.md` | Fórmulas matemáticas detalhadas (Lei 12.506/2011, FGTS, HE SAC, INSS/IRRF) |
| `references/janela_otima_explicacao.md` | Por que Ago/2028 é a janela ótima (3 alavancas) |
| `references/cenarios_saida_9_datas.md` | Tabela histórica com cenários comparativos |
| `references/fluxo-canonic-markdown-motor.md` | Referência do motor legado 2026–2030; não usar suas âncoras numéricas como inputs atuais |
| `scripts/calcular_rescisao.py` | Script principal de rescisão dinâmica |
| `scripts/calcular_janela_otima.py` | Script de janela ótima |
| `scripts/calcular_cenarios_saida.py` | Script dos 9 cenários comparativos |

## Versão

- **v1.1** (14/08/2026): reconciliação obrigatória do CDB real, dívida dinâmica via ENDIVIDAMENTO, auditoria visual de PDF e limpeza de `cenario_atual/`
- **v1.0** (13/08/2026): criação inicial consolidando todos os cenários de saída