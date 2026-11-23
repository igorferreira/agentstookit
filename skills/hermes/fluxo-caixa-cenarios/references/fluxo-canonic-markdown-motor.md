# Fluxo de Caixa — Markdown CANÔNICO + motor que gera o XLSX espelho

> Escopo: referência histórica do motor 2026–2030. Os exemplos, nomes de arquivo e
> âncoras numéricas abaixo não são inputs atuais. Para a família 2026–2036, seguir o
> gerador canônico indicado em `atualizar-controles`; use este arquivo apenas para
> entender o motor legado.

## Por que mudou
O ciclo anterior (Excel canônico) custava caro todo recálculo: abrir/editar via openpyxl,
recalcular no LibreOffice headless, caçar `#NAME?` (intervalos nomeados não definidos,
referências a planilha com espaço sem aspas simples), re-verificar os Checks. Tudo isso
só para validar uma curva de ~16 linhas. O Markdown lê instantâneo, é o meio nativo dos
demais controles do Usuário e reduz o custo de toque em ~80%.

## Arquitetura

```
FLUXO-CAIXA-2026-2030.md        (CANÔNICO — fonte da verdade)
   │  premissas em bloco ```yaml``` + tabelas calculadas
   ▼
fluxo_caixa/engine/fluxo.py     (MOTOR Python)
   │  lê o MD → recalcula CDB → reescreve as seções calculadas do próprio MD
   ▼
FLUXO-CAIXA-2026-2030.xlsx      (ESPELHO — gerado, NUNCA editado à mão)
```

**Regra de ouro:** se MD e XLSX divergirem, o **MD vence**; o XLSX é apenas regenerado.
Nunca editar o XLSX à mão.

## Root algorithm (fluxo.py)
- `saldo = CLT + VALLO + Diego + extra_renda − (cartões + HE + outros + imprevisto + extra_despesa + estouro)`
- `CDB = MAX(0, prev × (1+yield) + saldo)` — nunca compõe saldo negativo.
- Aplicar o aumento líquido somente no primeiro mês após a última parcela retida em folha; confirmar a competência da última dedução nas fontes vigentes e nunca descontar o consignado duas vezes.
- 13º + VALLO extra aplicam em Nov e Dez de CADA ano (Nov/26 `8178`, Dez/26 `3758`; idem Nov/27/Dez/27).

## Benchmark de validação (X36)
Motor deve reproduzir EXATAMENTE:
- Base com Diego: min **R$ 13.182,73** (Out/26), final Dez/27 **R$ 92.700,44**, não zera
- Sem Diego desde Out/26: min R$ 6.260,73 (Jan/27)
- Sem Diego desde Set/26: min R$ 4.179,52 (Jan/27)
- Stress (sem Diego Set + estouro R$1.000/mês Set–Jan): **zera em Jan/27**

## Pitfalls desta arquitetura
1. **Gastos ≠ renda:** `extra_despesa` (consulta pontual) e `estouro` são DESPESA. Tratá-los
   como renda foi um erro de verificação manual que falsamente "não zerava" o stress.
2. **13º precisa estar no YAML de CADA ano.** Esquecer o 13º de 2027 divergiu o final em
   −R$12.018 versus o X36 até ser corrigido no YAML. O motor expõe erro de DADOS, não de fórmula.
3. **`#NAME?` no LibreOffice:** ao modelar fórmulas com openpyxl, definir TODOS os intervalos
   nomeados referenciados e usar aspas simples em referências a planilhas com espaço
   (`='Premissas Mensais'!B3`), senão o recalculo devolve `#NAME?`.
4. **Checks que apontam para a célula errada parecem falha:** ex. check "VALLO cobre HE"
   lendo a coluna "faturas+HE+outros" (que não é só o HE) deu 0. Apontar o check para a
   grandeza que realmente valida (ex. comparar VALLO ao valor da parcela HE do app).

## Fluxo de atualização
1. Editar SÓ o YAML do `.md` (nova fatura → mudar linha `mensais`; novo cenário → linha `cenarios`).
2. `python3.12 fluxo_caixa/engine/fluxo.py` — recalcula + reescreve tabelas + regera XLSX.
3. Sincronizar MD + XLSX + fluxo.py ao Google Drive (Insync) e conferir SHA-256.
4. Diagnósticos pontuais (stress, T0–T3) vão em `_Analises/cenarios/<data>_<NOME>.{md,json,xlsx}`.