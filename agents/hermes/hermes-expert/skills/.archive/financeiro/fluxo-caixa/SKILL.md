---
name: fluxo-caixa
description: "Use when consulting, updating, or modifying Igor's cash flow projections (~/MEGA/Comprovantes/FLUXO-CAIXA-*.md and *.xlsx), including CDB balance, Home Equity SAC schedule, monthly budget, and long-term scenarios."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [financeiro, fluxo-caixa, projecao, cdb, home-equity, orcamento]
    related_skills: [financeiro-comprovantes]
---

# Fluxo de Caixa — Consulta e Alterações

Sempre que o usuário pedir para consultar, atualizar ou modificar o fluxo de caixa (projeções, cenários, orçamento, CDB, Home Equity, faturas, renda), siga este procedimento.

## Arquivos canônicos

| Arquivo | Finalidade |
|---|---|
| `~/MEGA/Comprovantes/FLUXO-CAIXA-2026-2030.md` | Fluxo completo mês a mês (Markdown) |
| `~/MEGA/Comprovantes/FLUXO-CAIXA-2026-2030.xlsx` | Planilha com 4 abas (Fluxo, Resumo, Métricas, Contracheque) |
| `~/MEGA/Comprovantes/CONTRACHEQUE.md` | Projeção salarial + VALLO + dissídios |
| `~/MEGA/Comprovantes/HOME-EQUITY.md` | Tabela SAC do CCB 004505 (50 parcelas) |
| `~/MEGA/Comprovantes/FLUXO-CAIXA-RESCISAO.md` | Cenários de rescisão (3 cenários, sem seguro-desemprego) |
| `~/MEGA/Comprovantes/ORCAMENTO.md` | 🆕 Plano mestre de orçamento: categorias, limites, regras de aprovação |
| `~/MEGA/Comprovantes/ORCAMENTO_SISTEMA_APROVACAO.md` | 🆕 Checklist de 5 perguntas + template de resposta para compras grandes |
| `~/MEGA/Comprovantes/CONTROLE_FATURAS_MANTIDOS.md` | 🆕 Visão mensal agregada de todos os cartões ativos |
| `~/MEGA/Comprovantes/FICHA_CARTAO_<NOME>_<FINAL>.md` | 🆕 Ficha individual por cartão com histórico mês a mês |
| `~/MEGA/Comprovantes/YYYY/YYYY_MM_MES/ORCAMENTO.md` | 🆕 Realizado mensal vs planejado |
| `~/MEGA/Comprovantes/CONTROLES.md` | Índice vivo de todos os controles ativos e status por cartão — ler primeiro quando não tiver certeza de quais arquivos existem hoje |
| `~/MEGA/Comprovantes/ENDIVIDAMENTO.md` | Camada estratégica: classificação mantidos/negociação vigente, propostas recebidas, monitoramento de negativação. Consultar antes de assumir qualquer contagem de cartões mantidos/negociação. |

## 🛑 Aprovação de compras grandes

Quando Igor perguntar "posso comprar X?", siga o checklist:

1. **Classificar:** Qual categoria do orçamento? (L1–L5, N1–N5)
2. **Verificar limite:** Já estourou o teto da categoria neste mês? → ler `ORCAMENTO.md` do mês
3. **Checar CDB:** Saldo atual permite? Vai precisar sacar?
4. **Projetar impacto:** Isso afeta os próximos 3 meses do fluxo de caixa?
5. **Priorizar:** É necessidade ou desejo? Dá pra esperar 13º/dissídio?

Responda SEMPRE com um dos 4:
- 🟢 **Aprovado** — cabe no orçamento, sem impacto
- 🟡 **Aprovado com ressalva** — cabe mas pressiona mês seguinte
- 🔴 **Não recomendado** — estoura categoria ou afeta reserva
- ⏸️ **Adiar** — esperar próximo mês / 13º / dissídio

## Regras de ouro

1. **Markdown é canônico.** Toda alteração começa no `.md`. O `.xlsx` é derivado.
2. **Atualize ambos.** Se mexeu no `.md`, regenere o `.xlsx` com `python3.12` + `openpyxl`.
3. **Consulte os arquivos-fonte:** CONTRACHEQUE.md (renda), HOME-EQUITY.md (parcela exata do HE), dados-contrato.json (FGTS).
4. **Não invente números.** Use os valores exatos do HOME-EQUITY.md para a parcela SAC de cada mês.
5. **Mantenha a data de atualização** no cabeçalho do `.md`.
6. **CDB é o termômetro.** O saldo do CDB mês a mês é a métrica principal.
7. **QUANDO FOR FINANCEIRO, QUEBRE EM TAREFAS.** Use `todo` com 3+ itens para qualquer pedido complexo. Sempre.
8. **COMPRAS GRANDES (>R$ 300 fora do orçamento).** Siga o checklist do `ORCAMENTO.md` raiz: categoria, CDB, fluxo, projeção, prioridade. Responda com 🟢/🟡/🔴.

## Premissas fixas (atualize aqui se mudarem)

| Premissa | Valor |
|---|---|
| Custo de vida cartões (pós-Jul/2027) | R$ 4.421/mês |
| VALLO BENEFÍCIOS mensal | R$ 4.420 (reajusta com dissídio ~4%/ano) |
| Dissídio FEAAC | ~4% ao ano, data-base 1º/agosto, reflexo novembro |
| CDB atual | **Não hardcodar aqui** — muda a cada pagamento/absorção. Ler o saldo em `FLUXO-CAIXA-2026-2030.md` (linha "CDB inicial"/tabela mensal) no momento da consulta. |
| Home Equity | SAC 50 parcelas, 1ª em Set/2026, última Out/2030 |
| Seguro-desemprego | Igor NÃO é elegível — nunca incluir |

> ⚠️ **Pitfall recorrente:** premissas com valor de CDB hardcoded nesta tabela já ficaram desatualizadas mais de uma vez (ex.: "R$ 21.131" e "mínimo R$ 13.141" — o CDB já mudou de cenário para Cenário X6 e esses números não valem mais). Trate qualquer número de CDB citado num SKILL.md como suspeito até confirmar contra o `FLUXO-CAIXA-2026-2030.md` atual.

## Fluxo de trabalho

### Consulta
```
1. Ler FLUXO-CAIXA-2026-2030.md (visão geral)
2. Se precisar de detalhe, ler CONTRACHEQUE.md ou HOME-EQUITY.md
3. Apresentar os números relevantes em tabela Markdown
```

### Alteração
```
1. Ler os arquivos atuais para entender o estado
2. Fazer as contas em Python (execute_code ou terminal) — nunca de cabeça
3. Atualizar o .md com patch ou write_file
4. Atualizar a data de atualização no cabeçalho
5. Regerar o .xlsx com python3.12 + openpyxl
6. Confirmar as alterações para o usuário
```

### Reconciliação com pagamentos reais
```
1. Levantar comprovantes de pagamento da pasta do mês (find *COMPROVANTE*) + meses adjacentes
2. Cruzar com o CONTROLE_PAGAMENTOS.md — o que tem comprovante → ✅ Pago
3. Atualizar ORCAMENTO.md do mês com valores realizados (planejado vs real)
4. Atualizar CDB tracking com saques executados e saldo atual
5. Verificar se o CDB real bate com o CDB projetado no fluxo — se divergir >R$100, recalcular
6. Atualizar status no CONTROLE_PAGAMENTOS.md: ✅ Pago / 🔴 Negociação / ⬜ Em aberto
```

### Geração do Excel
```bash
python3.12 << 'PYEOF'
# Usar openpyxl para gerar planilha com abas: Fluxo de Caixa, Resumo Anual, Métricas, Contracheque
# Dados extraídos do .md atualizado
PYEOF
```

## Pitfalls

- A parcela do HE muda TODO MÊS (SAC decrescente ~R$ 40/mês). Use o valor exato do HOME-EQUITY.md.
- O dissídio só reflete em Novembro (3 meses após data-base de agosto).
- Após Jul/2027, os parcelamentos zeram e as faturas caem para R$ 4.421 fixo.
- O CDB NUNCA zerou em nenhum cenário até hoje — mas o valor mínimo histórico específico muda a cada recálculo (não citar um número fixo aqui; conferir o mínimo atual em `FLUXO-CAIXA-2026-2030.md`).
- O HE é quitado em Ago/2030 — Nov/2030 e Dez/2030 têm HE = R$ 0.
- **💀 Absorções por cartão de negociação:** cada pagamento feito com Inter/Dígio aumenta a dívida de negociação e preserva o CDB. Ver [`references/rastreamento-absorcoes-negociacao.md`](references/rastreamento-absorcoes-negociacao.md).
- **Atualização do CDB por DELTA:** quando o CDB melhora por absorções (ex: +R$ 7.869), aplicar o delta via script Python que percorre todos os valores em negrito no arquivo `.md`, soma o delta, e corrige manualmente valores que não são CDB (renda, faturas, HE). Rodar `python3.12` com `re.sub(r"\*\*([\\d,]+)\*\*", shift, content)` e depois aplicar fixes nos valores que não deveriam ser alterados. Também atualizar o `.xlsx` com `openpyxl` percorrendo as células da coluna CDB.

## Referências

- [`references/rastreamento-absorcoes-negociacao.md`](references/rastreamento-absorcoes-negociacao.md) — padrão de rastreamento de absorções por cartões de negociação (Inter/Dígio)
- **Nomes de arquivos de sistema na raiz** (ORCAMENTO, FLUXO, CONTRACHEQUE) usam underscore `_` como separador, NÃO hífen. Ex: `ORCAMENTO_SISTEMA_APROVACAO.md`, não `ORCAMENTO-SISTEMA-APROVACAO.md`. Arquivos financeiros datados (comprovantes, faturas) continuam usando hífen por compatibilidade com o padrão existente.
- **Reconciliação de CDB:** ao revisar pagamentos, sempre cruzar o CDB real (comprovantes de resgate) com o CDB projetado no fluxo. Divergência > R$ 100 requer recalcular o fluxo.
- **Comprovantes podem estar em meses adjacentes:** pagamentos de fatura de Agosto processados em 31/07 ficam na pasta Julho. Buscar com `find ~/MEGA/Comprovantes/2026/ -name "*COMPROVANTE*"` para não perder nenhum.

## Rescisão — Cruzamento com CARREIRA

Quando o usuário pedir cenários de rescisão ou "e se eu for demitido":
1. Ler o relatório mais recente em `~/MEGA/Documentos/CARREIRA/rescisao-clt/relatorios/`
2. Cruzar os valores de rescisão (líquido imediato) com o fluxo de caixa atual (HE, custo de vida)
3. Calcular: `meses de cobertura = rescisão ÷ (HE + custo_vida)`
4. Gerar/atualizar `FLUXO-CAIXA-RESCISAO.md` com mês a mês de cada cenário
5. Sempre lembrar: Igor NÃO é elegível para seguro-desemprego

## 💀 Uso estratégico de cartões de negociação

Quando o usuário quiser usar limite de um cartão que vai pra negociação para pagar outro:
- Seguir [`references/uso-estrategico-cartoes-negociacao.md`](references/uso-estrategico-cartoes-negociacao.md)
- Calcular limite disponível REAL (total − fatura − parcelamentos)
- Mostrar cenário: o que o Inter/Dígio absorve vs o que o CDB cobre
- Destaque: **preservação do CDB** como métrica principal
## O que NÃO fazer

- ❌ Alterar só o .xlsx e deixar o .md desatualizado
- ❌ Usar números aproximados para a parcela HE — consulte HOME-EQUITY.md
- ❌ Incluir seguro-desemprego em qualquer cenário
- ❌ Tratar VALLO como parte da rescisão
- ❌ Ignorar o dissídio de agosto nos meses de Nov/Dez
- ❌ Fazer contas de cabeça — use Python

## Gatilhos e apelidos

- "financeiro" e "financerio" (typo comum) ativam o domínio financeiro
- "fluxo de caixa", "orcamento", "CDB", "projeção" → consultar FLUXO-CAIXA-2026-2030.md
- "posso comprar X?" → seguir checklist do ORCAMENTO_SISTEMA_APROVACAO.md

## Referências

- [`references/uso-estrategico-cartoes-negociacao.md`](references/uso-estrategico-cartoes-negociacao.md) — Padrão 💀: usar limite de cartões de negociação para pagar essenciais, preservando CDB
- [`references/reconciliacao-pagamentos.md`](references/reconciliacao-pagamentos.md) — Fluxo completo: comprovantes → controles → orçamento → CDB → fluxo
- [`references/controle-faturas-mantidos.md`](references/controle-faturas-mantidos.md) — Sistema de fichas individuais + controle mensal de faturas dos cartões ativos
- [`references/playbook-negociacao-email.md`](references/playbook-negociacao-email.md) — Atualizar playbook com ebook do Dr. Israel + enviar por email
