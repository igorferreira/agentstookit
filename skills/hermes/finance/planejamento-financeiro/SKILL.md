---
name: planejamento-financeiro
description: "Use when Igor asks about financeiro tasks — modelagem de cenários, projeções, parcelamentos, cheque especial, registro de faturas/comprovantes, cenários de pagamento, matriz de cartões, dossiês para advogado, negociação de dívidas."
version: 1.0.0
---

# Planejamento Financeiro — Cenários e Projeções

Skill para modelagem de cenários financeiros complexos: múltiplos cartões, parcelamentos futuros, CDB, cheque especial, projeções de longo prazo e dossiês para advogados.

## Triggers

- "Financeiro" como prefixo de mensagem
- "cenário", "projeção", "planilha", "orçamento"
- "parcelamento", "parcelas futuras"
- "negociar dívida", "advogado", "dossiê"
- "cheque especial", "estourou a conta"
- "matemática", "PhD", "janela ótima", "cálculo profundo" — usar **Modo PhD** (ver seção abaixo)
- Perguntas sobre rescisão CLT ("quanto recebo se for demitido", "pedir demissão", "quando sair")

## Modo PhD em Matemática Financeira (PREFERENCIAL para Igor)

Quando Igor pedir análise estratégica (rescisão, janela ótima, "vale a pena sair", etc), operar em **Modo PhD** com rigor matemático. Esta é a modalidade preferida desde 13/08/2026 — Igor pediu explicitamente para "atualizar o agente financeiro para ser tb um phd em matemática financeira pessoal e matemática financeira para famílias e pessoas".

### O que o Modo PhD exige

1. **Fórmulas explícitas** — toda projeção tem equação matemática, não número mágico
2. **3 cenários mínimo** — otimista / base / pessimista, com probabilidades
3. **Stress test paramétrico** — tabela 5×5 (2 variáveis ±3 níveis) com center cell destacado
4. **Cronologia exata** — sempre executar `date '+%Y-%m-%d %H:%M:%S %Z (%A)'` antes de responder (regra de Igor: nunca confiar em data de contexto)
5. **Janela ótima** — encontrar a data em que `caixa_imediato ≥ alvo` (dívidas + viver)
6. **Múltiplos cenários de saída** — para cada decisão de rescisão, comparar:
   - **Pedido demissão (aviso dispensado)** — líquido sem multa/saldo bloqueado
   - **Pedido demissão (aviso descontado)** — desconta 1 salário
   - **Dispensa sem justa causa** — caixa máximo (multa 40% + saldo saque-aniversário)
7. **Sempre fechar com CDB saldo** — regra absoluta do Igor: `fluxo_caixa → CDB saldo no final`

### Matemática CLT obrigatória (Lei 12.506/2011)

```
aviso_prévio_dias(anos) = 30 + min(60, ⌊anos⌋ × 3)
   └─ 3 anos → 39 dias, 4 anos → 42, 5 anos → 45, 6 anos → 48
FGTS(t) = base × (1 + taxa_mensal)^n + salário × 0,08 × n − saques_aniversário
multa_40% = 0,40 × FGTS
saldo_bloqueado (saque-aniversário) = FGTS − multa → LIBERA na dispensa
13°_proporcional(mês, com_aviso) = (m + AP/30) / 12 × bruto (cap 12)
férias_prop = meses_PA / 12 × bruto × 4/3 (cap 12, com 1/3 constitucional)
INSS = min(bruto × 0,10, 815,06)            # teto 2026
IRRF = max(0, (bruto−INSS) × 0,15 − 354,80) # dedução simplificada
caixa_dispensa = líquido_emp + multa_40% + saldo_bloqueado
caixa_pedido = líquido_emp (sem multa, sem saldo bloqueado)
```

**REGRA INVARIÁVEL: VALLO BENEFÍCIOS NÃO entra na rescisão** (Igor confirmou). É rendimento enquanto estiver empregado, mas não compõe verbas rescisórias.

### Estrutura obrigatória de pastas `fluxo_caixa/`

Quando a modelagem envolver cenários de saída, criar/organizar esta estrutura:

```
~/MEGA/Comprovantes/fluxo_caixa/
├── README.md                              ← índice da estrutura
├── cenario_atual/                         ← continuar na Noorden (X23_atual.xlsx etc.)
│   ├── X23_atual.xlsx
│   ├── X23_atual.md
│   ├── X23_atual.pdf
│   └── X23_atual.csv
├── cenario_demissao/                      ← dispensa sem justa causa
│   ├── rescisao_YYYY-MM.md                 ← atualizado mensalmente via cron
│   ├── rescisao_YYYY-MM.json
│   ├── janela_otima_demissao.md           ← análise PhD da janela
│   └── janela_otima_demissao.json
├── cenario_pedido_demissao/               ← pedido de demissão (aviso dispensado ou descontado)
│   ├── comparativo_cenarios_saida.md       ← tabela com 9 cenários
│   ├── comparativo_cenarios_saida.json
│   └── comparativo_cenarios_saida.pdf
├── calculos_auxiliares/                   ← scripts Python reutilizáveis
│   ├── calcular_rescisao.py
│   ├── calcular_janela_otima.py
│   └── calcular_cenarios_saida.py
└── historico/                              ← X19, X20, X21, X22 antigos
```

### Cron job ativo

Igor pediu atualização mensal automática da rescisão via cron:
- **Job ID:** `e247555646ba`
- **Schedule:** `0 9 1 * *` (todo dia 1º às 09:00 BRT)
- **Comando:** `python3.12 ~/MEGA/Comprovantes/fluxo_caixa/calculos_auxiliares/calcular_rescisao.py`
- **Output:** `cenario_demissao/rescisao_YYYY-MM.md` e `.json`

### Outputs obrigatórios em Modo PhD

Sempre entregar os 5 formatos:
1. **PDF** (apresentável, via pandoc + wkhtmltopdf --no-background)
2. **XLSX** (planilha viva com fórmulas, via excel-author)
3. **MD** (Markdown derivado, fonte narrativa)
4. **JSON** (machine-readable, para automações futuras)
5. **Script Python** (`calculos_auxiliares/calcular_*.py` — reutilizável)

### Janela ótima — algoritmo

Para "quando devo sair para que a rescisão cubra X":

```
para cada data_em [Ago/26, Mai/27, Ago/27, Mai/28, Ago/28, ...]:
    simular_dispensa(data_em) = calcular verbas + FGTS + multa + saldo_bloqueado
    he_saldo(data_em) = max(0, 108.720 − 2.174 × meses_HE_pagos)
    alvo(data_em) = 6_cartões + BrasilCard + he_saldo(data_em)
    cobertura = caixa_imediato / custo_vida_mensal
    se caixa_imediato ≥ alvo(data_em):
        registrar como janela viável
        # mostrar margem = (caixa − alvo) / custo_vida
retornar primeira_data_viável
```

Tabela canônica de 9 cenários comparativos (gerar sempre):

| Data | Anos | Aviso | Salário | HE saldo | Dispensa | Pedido (disp) | Pedido (desc) | Cobre TUDO? |
|---|---:|---:|---:|---:|---:|---:|---:|:---:|

### Decisão estratégica por objetivo

| Objetivo | Janela |
|---|---|
| Quitar só 6 cartões + BrasilCard | Pode sair HOJE (margem R$ 21k) |
| Quitar TUDO incluindo HE saldo | **Ago/2028** (5 anos 3 meses) |
| Margem confortável após quitar tudo | Ago/2030 (7 anos 3 meses) |

### Por que Ago/2028 cruza a fronteira

Três alavancas se cruzam exatamente nesse mês:
- **Dissídio anual Ago/28** → +R$ 615 no bruto
- **Aviso prévio 5 anos** (completa Mai/28) → +3 dias = +R$ 1.341
- **HE já pago 22 meses** (Out/26 → Ago/28) → saldo cai para R$ 59.570

A conjunção das três = janela ótima.

## Verificação de dados antes de qualquer análise

Quando o usuário menciona um número específico (saldo, dívida, valor de conta) que você não encontra nos arquivos pesquisáveis:

1. **Primeiro — verificar o dashboard:** O motor do dashboard lê diretamente o banco e atualiza saldos em tempo real. Verificar `~/MEGA/Comprovantes/fluxo_caixa/dashboard/publicacao/dados_dashboard.json`:
   - `realismo.saldos` → saldos reais por banco no momento
   - `realismo.outubro` (ou mês corrente) → buraco/gastos/renda do mês
   - `cartoes.cartoes[]` → cada cartão com `total_aberto`
   - `scenarios[]` → projeções já calculadas

2. **Segundo — grep nos arquivos controladores:** `ENDIVIDAMENTO.md`, `_controles/CONTROLE_INDICE.md`, `FLUXO-CAIXA-2026-2036.md`. Procurar tanto pelo nome quanto pelo número exato.

3. **Terceiro — considerar fontes não-textuais:** Prints de app, extratos PDF, capturas de tela — podem conter números que NENHUM arquivo .md referencia. Se nada das etapas 1-2 encontrou o valor, perguntar ao usuário: "onde você viu esse número? Print, app, site?"

4. **Sempre cruzar fonte-textual × fonte-dashboard.** Se valores divergem, a fonte-dashboard é mais recente (gerada automaticamente), mas pode estar desatualizada se ninguém regenerate depois de uma mudança. Anotar qual versão foi consultada e quando.

⚠️ **PITFALL: Não assumir que "não encontrei nos arquivos" = "valor não existe".** O motor financeiro é a fonte primária para saldos correntes; arquivos .md registram cenários/projeções. Um saldo real de −R$ 9k numa conta ItaÚ pode aparecer como parte da coluna `cartões` no fluxo projetado sem nunca ser chamado "lombarda" ou "LIS" em texto explícito.

## Análise de oferta de emprego (salário + benefícios)

Quando Igor recebe uma proposta ("me ofereceram uma vaga de X por R$ Y"):

1. **Criar pasta da empresa** em `~/MEGA/Documentos/oportunidades/<Empresa>/` com `INDEX.md` e um dossiê MD único por empresa.
2. **Pesquisar a empresa em duas camadas**: (a) web — notícias financeiras, IPO/delisting, dívidas, layoffs, donos, receita/prejuízo; (b) Glassdoor logado na conta do Igor — notas por categoria, avaliações literais recentes, salários publicados, benefícios (aba com avaliações individuais), processo de entrevista e vagas abertas.
3. **Calcular a oferta centavo-exato** — INSS progressivo + IRRF progressivo reais, líquido, pacote de caixa mensal (líquido + VA + auxílios), 13º + férias+1/3, ano 1 de caixa, e sobra sobre o custo de vida (R$ 4.000). Ver `references/analise-oferta-salario-clt.md` para as tabelas vigentes e o script.
4. **Comparar com a banda interna da empresa** (percentis dos salários publicados) e com o salário atual/meta do plano de carreira (`~/MEGA/Documentos/carreira/`). Oferita vs mercado: o que importa é onde cai na banda da empresa e vs a meta (14+ salários/ano com PLR consistente).
5. **PLR não é crédito sem histórico de pagamento** — exigir o valor real pago nos últimos 3 ciclos antes de somar ao pacote anual.
6. **Confirmar modelo CLT × PJ antes de qualquer conclusão**: PJ R$ 14k sem 13º/férias/FGTS é pior que CLT — a análise inteira muda de rota. Se PJ, reescrever (PRL, pró-labore, INSS 11%, encargos).
7. **Fechar o dossiê com veredito + lista de perguntas para o recrutador** (modalidade, valor real do VA, PLR paga de fato, estabilidade, stack/gestor).

**Pitfall: nunca aceitar o valor da tela/da vaga como a banda da empresa.** Puxar os salários publicados por cargo no Glassdoor e posicionar a oferta — "topo da banda" e "abaixo do 75º percentil" são os argumentos de negociação que Igor usa.

## Workflow

### Registrar pagamento informado verbalmente (sem comprovante)

Quando Igor diz que já pagou uma parcela/conta e não manda comprovante ("registra que o pagamento já foi feito"):

1. **Localizar a ficha do compromisso** — `grep -rli '<nome do credor>' ~/MEGA/Comprovantes/ ~/MEGA/Documentos/` (excluir `fluxo_caixa/dashboard`). A ficha canônica de um acordo pessoal NÃO fica em `_fichas/` (que é só de cartões) e sim na pasta mensal de origem do acordo (ex.: `2026/2026_08_AGOSTO/<data>_<CREDOR>-CONTROLE-PAGAMENTO.md`).
2. **Atualizar a ficha em 2 lugares**: a coluna de status da parcela no cronograma (`✅ Paga <data> — informado pelo Igor, sem comprovante`) e a tabela de pagamentos do rodapé (nova linha com origem e comprovante `—`).
3. **Adicionar linha no CONTROLE_PAGAMENTOS do mês da competência** (`2026/2026_MM_MES/YYYY-MM_00_CONTROLE_PAGAMENTOS.md`), na seção de provisões/obrigações, com link para a ficha.
4. **Kanban + fila**: `hermes kanban --board default create "..."` → `complete <id> --result "..."` → append no `~/clawd/PEDIDOS.md` com início/fim. ⚠️ O comando `hermes kanban start` NÃO existe — ir direto de `create` para `complete`.
5. **Fluxo canônico 2036 NÃO muda** para confirmação de pagamento já modelado: as parcelas de acordos estão embutidas por COMPETÊNCIA no X47/motor — pagamento confirmado não recalcula a cadeia, só registra a baixa nos controles. Só re-modelar se a competência/valor divergir do modelado.
6. Na resposta, fechar com a situação completa do acordo (tabela parcela a parcela + o que resta) e oferecer arquivamento do comprovante quando Igor o enviar depois.

### Registrar e avaliar propostas de renegociação

Quando o usuário enviar uma oferta de acordo por print, app ou documento:

1. Preserve a evidência original na pasta mensal de `~/MEGA/Comprovantes/2026/AAAA_MM_MES/` e crie um Markdown pareado com data/hora, saldo apresentado, desconto, entrada, parcelas, total exibido, validade e status.
2. Recalcule tudo antes de registrar como fato: `economia = saldo − valor à vista`, `desconto% = economia ÷ saldo × 100`, `total parcelado = entrada + (nº parcelas × valor da parcela)` e `custo adicional = total parcelado − valor à vista`. Compare o total calculado com o total exibido e destaque qualquer divergência, mesmo de centavos.
3. Atualize a ficha individual do cartão, `ENDIVIDAMENTO.md` (seção de propostas), `AVISOS.md` e `DIAGNOSTICO.md`. Marque explicitamente “não aceita” até o usuário confirmar o aceite; não substitua o valor-base da dívida apenas porque o app exibiu uma oferta.
4. Separe sempre três números: saldo apresentado pelo credor, valor de liquidação à vista e custo total parcelado. Um percentual maior não significa proposta melhor se o desembolso total for maior.
5. Não contabilize oferta de consignado, limite pré-aprovado ou empréstimo simulado como renda, caixa ou contratação; só entra no fluxo após aceite formal e crédito efetivo.
6. Para investigar se novas ofertas podem melhorar, combine termos/páginas oficiais do credor com relatos públicos, classificando os relatos como evidência anedótica. Informe “pode acontecer” versus “é garantido” e nunca transforme um desconto de terceiro em expectativa contratual.

**Pitfall:** não copie o total parcelado da tela sem refazer a soma; apps podem exibir entrada, parcelas, encargos ou arredondamentos em campos diferentes, e uma diferença pequena pode alterar o CET e o valor contratual.

### 0. ⚠️ ANTE S de modelar: confirmar lista de mantidos vs negociação

**Este é o passo em que mais se erra.** A lista de cartões muda DURANTE a sessão — o usuário decide manter um que era pra negociar, paga um com limite de outro, absorve cartão novo. Se você modelar com a lista errada, TODO o fluxo de caixa fica errado.

**Antes de QUALQUER projeção:**
- Ler `~/MEGA/Comprovantes/ENDIVIDAMENTO.md` (seções 3 e 4) para a classificação vigente — é a fonte da verdade, criada exatamente para não depender da memória da sessão.
- Confirmar com o usuário só se o `ENDIVIDAMENTO.md` estiver desatualizado (checar a data de "Última atualização" no topo) ou se houver uma mudança recente que ainda não foi registrada lá.
- Tratar 3 categorias separadamente: **ATIVOS/MANTIDOS** (pagar), **NEGOCIAÇÃO** (não pagar), **ZERADOS** (sem dívida — seção 7 do `ENDIVIDAMENTO.md`)
- Se houver cartão com emissor desconhecido (ex: Méliuz), **buscar na internet** antes de classificar
- **Sempre que um cartão mudar de categoria, atualizar `ENDIVIDAMENTO.md` (seções 1, 3, 4) e `CONTROLES.md` junto** — não deixar a mudança só na sessão atual, ou a próxima sessão volta a perguntar do zero.

### 1. Mapear TODOS os compromissos

Antes de qualquer cenário:
- Listar todos os cartões com fatura atual, vencimento e emissor
- **Perguntar sobre parcelamentos futuros de CADA cartão.** Não assumir que a fatura atual é o único custo.
- Parcelamentos ocultos são o maior risco — insistir com o usuário até ter todos mapeados.
- **Saldo em conta corrente é recurso.** Se o usuário tem dinheiro na conta do Itaú, usar para pagar cartões Itaú primeiro — libera o CDB.

### 2. Descobrir parcelamentos futuros

- Pedir prints dos apps de cartão (gráfico de "próximas faturas" ou "parcelamentos")
- Extrair com OCR (pytesseract). Em modo escuro, **inverter a imagem** antes: `ImageOps.invert(img.convert('RGB')).convert('L')`
- Se OCR falhar (comum em apps dark mode), pedir para o usuário ditar os valores
- Montar matriz: linhas = meses, colunas = cartões
- Ver `references/dark-mode-ocr.md` para técnicas de extração

### 3. Modelar cenários

Para cada cenário:
- **Caixa disponível:** CDB + conta corrente + renda mensal
- **Pagamentos imediatos:** faturas do mês atual
- **Parcelamentos futuros:** da matriz
- **Renda recorrente:** CLT líquido + VALLO + outros
- **Compromissos fixos:** empréstimos, custo de vida
- **Eventos sazonais:** 13º (1ª parcela nov, 2ª parcela dez), dissídio (confirmar data-base)

### 4. ⚠️ PITFALL: Cheque especial

**SEMPRE incluir juros do cheque especial em projeções com saldo negativo.**

- Nubank: ~8% a.m. sobre o saldo devedor
- O juro composto do OD transforma um déficit pequeno em bola de neve
- Projetar mês a mês: `OD_acumulado = OD_anterior + déficit_mensal + juros(OD_anterior * 0.08)`
- Mostrar explicitamente: "Sem OD" vs "Com OD" para o usuário ver o impacto

### 5. Projeção de longo prazo

- **NUNCA incluir aumentos de renda não confirmados.** Dissídio só entra na projeção depois de confirmada a data-base e o percentual.
- Ser conservador: usar a renda recorrente comprovada, sem bônus ou pontuais
- Projetar até o marco relevante (ex: fim dos parcelamentos, fim dos 280 dias de negociação)
- Incluir 13º nas datas legais (1ª parcela até 30/nov, 2ª até 20/dez)
- Empréstimos SAC: a parcela diminui ~R$ 40/mês (recalcular amortização × taxa)

### 6. Formato de entrega

Para cada cenário, entregar:
1. **Markdown:** visão completa com tabelas
2. **Excel (openpyxl):** uma aba por cenário + aba comparativo
3. **Passo a passo:** playbook de execução com data, app, valor, saldo após cada pagamento
4. **PDF:** para enviar a terceiros (advogado, contador)

### 7. Dossiê para advogado

**Sempre fazer due diligence ANTES de recomendar qualquer escritório.** Ver `references/due-diligence-advogado.md` para o checklist completo.

**⚠️ PITFALL: Confirmar estrutura COMPLETA de honorários.** Advogados frequentemente mencionam só uma dimensão e "esquecem" as outras. Sempre confirmar as 3:

| Dimensão | Perguntar |
|---|---|
| **Entrada** | Valor à vista? Parcelamento? |
| **Mensalidade** | Cobra valor fixo mensal? Quanto? |
| **Sucesso** | % sobre redução? Tem cap (teto máximo)? |

Projetar custo total por tempo: `Entrada + (Mensalidade × Meses) + (% × Redução)`. Comparar escritórios com projeção de 3/6/12/24 meses.

Formato canônico do dossiê (ver template completo em `references/due-diligence-advogado.md`):
1. Identificação (OAB, CNPJ, endereço)
2. Perfil do advogado (processos, experiência, adversários)
3. Resultados apresentados (com alerta de autodeclaração)
4. Alertas e riscos (Reclame Aqui, OAB, inconsistências)
5. Comparação de honorários (se 2+ escritórios)
6. Perguntas essenciais antes de fechar
7. Proposta de honorários detalhada

Salvar em `~/MEGA/Documentos/Dividas/dossie-NOME-snakecase.md`.

## Fluxo de caixa detalhado com contas de consumo

Quando o usuário pedir projeção de fluxo de caixa incluindo contas de consumo (luz, gás) que serão pagas no crédito:

1. **Identificar contas atrasadas**: verificar último pagamento registrado e meses em aberto. Para Light (~R$ 771/mês) e Naturgy (~R$ 110/mês), usar histórico recente como estimativa quando a fatura não estiver disponível.
2. **Confirmar com o usuário**: quantos meses atrasados e qual cartão (Signature ou Passaí).
3. **Incluir como despesa recorrente no cartão escolhido**: a partir do mês seguinte, adicionar ~R$ 881/mês (luz + gás) na fatura do cartão indicado.
4. **Projetar mês a mês**: renda (CLT + VALLO) → menos faturas dos cartões → menos C6 → saldo. Incluir dissídio e 13º nas datas corretas.
5. **Apresentar tabela com**: Mês, Parcelas, C6, Renda, Fluxo, Reserva.

## Nubank: antecipação de parcelas vs CDB

- **Taxa de antecipação Nubank:** ~10,58% a.a. (0,84% a.m.) — confirmado via pesquisa no site oficial.
- **CDB C6:** ~14% a.a. (1,1% a.m.).
- **Conclusão:** Matematicamente, **NÃO antecipar**. Deixar o dinheiro no CDB rende mais do que o desconto da antecipação. Só antecipar se o alívio de fluxo de caixa for crítico (risco de cheque especial).

## Estrutura do orçamento de Igor

O orçamento mensal se divide em duas categorias:

### 🍺 LAZER (~R$ 1.970)
| Item | Valor | Nota |
|---|---|---|
| Claro | R$ 330 | 🔒 Futebol em casa — NUNCA sugerir cortar |
| Karatê | R$ 100 | Saúde |
| TotalPass | R$ 240 | SmartFit + Crossfit (Set/26+) |
| Combustível | R$ 300 | |
| Livres | R$ 1.000 | Mercado, restaurante, lazer |

### 🏠 NÃO-LAZER (~R$ 2.451)
| Item | Valor | Nota |
|---|---|---|
| Condomínio | R$ 1.020 | Estrutural |
| Vivo | R$ 105 | |
| IA (4 assinaturas) | R$ 408 | 🔒 Ferramentas de trabalho — NUNCA sugerir cortar |
| Light | R$ 778 | Jul/26: 454 kWh |
| Gás | R$ 140 | Média histórica |

> Total gasto mensal: ~R$ 4.421. Aparece na fatura do mês seguinte.

## VALLO BENEFÍCIOS + Home Equity

**⚠️ CRÍTICO: VALLO NÃO é renda livre.** R$ 4.420 de VALLO vai integralmente para o Home Equity C6 (CCB 004505, SAC 50m, 1ª parcela R$ 4.389 em 10/Set/2026). Sobra apenas ~R$ 31/mês no início, crescendo ~R$ 40/mês conforme o SAC reduz a parcela.

**Sempre modelar:**
```
Disponível = CLT líquido + (VALLO − Home Equity) + 13º
```
NUNCA somar CLT + VALLO como renda total sem descontar o Home Equity.

## Estrutura de pastas e nomenclatura

```
~/MEGA/Comprovantes/
├── 📄 CONTRACHEQUE.md              ← canônicos (raiz)
├── 📄 HOME-EQUITY.md
├── 📄 MAPA-CUSTO-VIDA.md
├── 📄 ENDIVIDAMENTO.md
├── 📄 FLUXO-CAIXA-2026-2030.md
├── 📄 AVISOS.md
│
├── 📁 _controles/                  ← prefixo CONTROLE_ obrigatório
│   ├── CONTROLE_INDICE.md
│   ├── CONTROLE_FATURAS_MANTIDOS.md
│   ├── CONTROLE_SALDO_CONTAS.md
│   ├── CONTROLE_ORCAMENTO.md
│   └── ...
│
├── 📁 _fichas/                     ← prefixo FICHA_CARTAO_BANCO_ obrigatório
│   ├── FICHA_CARTAO_NUBANK_3033.md
│   └── ... (26 fichas)
│
├── 📁 _Analises/
├── 📁 2026/YYYY_MM_MES/
│   ├── INDEX.md
│   ├── FATURA-CARTAO-<NOME>-R<VALOR>.pdf
│   └── ...
```

### Padrão de nomenclatura de arquivos

- Fatura: `AAAA-MM-DD_FATURA-CARTAO-<NOME_CARTAO>-R<VALOR>.(pdf|md)`
- Comprovante pagamento: `AAAA-MM-DD_FATURA-CARTAO-<NOME_CARTAO>-R<VALOR>-COMPROVANTE-PAGAMENTO.(jpg|pdf|md)`
- Cenários: `AAAA-MM-DD_CENARIOS-PAGAMENTOS.xlsx`
- Playbook: `AAAA-MM-DD_PASSO-A-PASSO-<CENARIO>.md`
- Projeção: `AAAA-MM-DD_PROJECAO-24-MESES.md`

## Contracheque — fluxo de atualização

1. Buscar email com `himalaya envelope list` procurando "Noorden - Contra Cheque"
2. Email de Camila Lima (camilalima@noorden.com.br) com assunto "Noorden - Contra Cheque - <MÊS> <ANO>"
3. Extrair PDF do email com `himalaya message export` + Python `email` module
4. Extrair texto com `pdftotext -layout`
5. Atualizar `dados-contrato.json` com novos valores
6. Atualizar memória com novo líquido
7. Atualizar planilha de cenários com nova renda

## PDFs de fatura Itaú — senha

Faturas Itaú (Signature, Luiza, Passaí) vêm com PDF criptografado.
- **Senha:** 5 primeiros dígitos do CPF (ex: XXXXX)
- **Decriptar com:** `pypdf.PdfReader.decrypt(password)`

## OCR de prints de app (modo escuro)

Apps como Itaú em dark mode falham no Tesseract direto. Ver `references/dark-mode-ocr.md` para o pipeline completo. Resumo rápido:

```python
from PIL import Image, ImageEnhance, ImageOps
img = ImageOps.invert(img.convert('RGB')).convert('L')
img = ImageEnhance.Contrast(img).enhance(2.0)
img = img.point(lambda x: 0 if x < thresh else 255)  # thresh 70-100
text = pytesseract.image_to_string(img, config='--oem 3 --psm 6 -l por')
```

## Projeção de fluxo de caixa (padrão canônico)

### Arquivos na raiz de Comprovantes

Os arquivos canônicos do fluxo de caixa ficam em `~/MEGA/Comprovantes/`:
- `FLUXO-CAIXA-2026-2030.xlsx` — planilha com abas de fluxo, resumo, métricas e contracheque
- `FLUXO-CAIXA-2026-2030.md` — versão Markdown (fonte da verdade; o `.xlsx` é derivado)
- `HOME-EQUITY.md` — cronograma SAC completo da CCB 004505
- `CONTRACHEQUE.md` — real + projeção até Dez/2028
- `_controles/CONTROLE_INDICE.md` — índice vivo de todos os controles ativos e status por cartão; ler primeiro para saber quais arquivos existem hoje
- `ENDIVIDAMENTO.md` — classificação atual mantidos/negociação, propostas recebidas, monitoramento de negativação — ler ANTES do passo 0 (confirmar lista de mantidos vs negociação) em vez de perguntar do zero ao usuário

> ⚠️ Nomes datados mudam de versão (ex.: `FLUXO-CAIXA-2026-2028` foi substituído por `FLUXO-CAIXA-2026-2030` em 03/08/2026, e o arquivo antigo foi apagado). Confirmar com `ls ~/MEGA/Comprovantes/FLUXO-CAIXA-*.md` antes de citar um nome de arquivo específico de memória.

### Geração com Python

Usar script Python com `openpyxl` para gerar Excel com 5 abas:
1. **Visão Geral** — Orçamento, ajustes, métricas KPIs
2. **Fluxo de Caixa** — 29 meses com CLT, VALLO, HE, parcelamentos, C6, reserva
3. **Resumo** — Cartões mantidos, negociação, recursos CDB
4. **Parcelamentos** — Matriz por cartão mês a mês
5. **Premissas** — Todas as premissas do modelo

Pattern: `python3.12` com script em here-document. Gera Excel + Markdown de uma vez.

### Dados reais, não estimativas

- **SEMPRE extrair CCB do PDF** (`pdftotext`) para valores reais do Home Equity
- **SEMPRE usar contracheque real** para CLT líquido
- **SEMPRE usar faturas reais** para parcelamentos (não estimar)
- Fonte CCB: `~/MEGA/Documentos/Emprestimo/1. ccb - vn.pdf`
- Fonte contracheque: email Camila Lima `camilalima@noorden.com.br`

### "Meses no vermelho"

Quando o usuário disser "não posso ter meses no vermelho", explicar que:
- Déficit mensal coberto por reserva NÃO é "estar no vermelho" de verdade
- A reserva do CDB funciona como ponte até os parcelamentos acabarem
- Mostrar a reserva NUNCA zera — só diminui temporariamente
- Após os parcelamentos (Jul/27), o fluxo fica positivo todo mês

## Pitfalls

- **NUNCA assumir que a fatura atual é o único custo.** Parcelamentos futuros explodem o orçamento.
- **SEMPRE incluir juros do cheque especial** em projeções negativas.
- **NÃO antecipar dissídio** sem confirmação de data e percentual.
- **Separar itens pontuais de recorrentes** na renda (ex: triênio retroativo é pontual, triênio é recorrente).
- **VALIDAR com o usuário** antes de gerar Excel/PDF final — ele revisa os números.
- **Senha de PDF de fatura:** perguntar ao usuário (normalmente CPF parcial). Descriptografar com `pypdf`.
- **OCR do app Nubank — não confundir "fatura atual" com "total das próximas faturas".** São números muito diferentes — R$ 5.660 vs R$ 28.548 no mesmo print. Confirmar qual é qual com inspeção cuidadosa.
- **IA é ferramenta de trabalho — NUNCA sugerir cortar.** ChatGPT, Gemini, Claude e Manus são custo fixo intocável.
- **Claro é lazer, não telefone.** R$ 330/mês = futebol em casa. Economiza bar. NUNCA sugerir cortar.
- **VALLO paga Home Equity.** NUNCA modelar VALLO como renda livre sem descontar a parcela do HE.
- **Usar dados reais da CCB.** Extrair do PDF com `pdftotext`, nunca estimar parcela do HE.
- **Cartão Dígio em negociação = limite "grátis".** Pagar contas (luz, gás) com ele preserva caixa. Ver `references/fluxo-caixa-contas-consumo.md`.
- **Limite de qualquer cartão em negociação é recurso.** Usar PIX crédito do cartão que não será pago para quitar cartões menores. Ex: PAN Buscapé pagou PicPay → PicPay saiu da negociação, PAN absorveu +R$880.
- **"Pagou o cartão X?" — sempre especificar o mês da fatura.** Perguntar "pagou o Nubank?" sem o mês gera confusão — a resposta pode ser "só paguei o que vencia em agosto" enquanto a fatura de setembro ainda está em aberto. Sempre listar mês a mês com vencimento.
- **Saldo em conta corrente paga cartões do mesmo banco.** Dinheiro na conta Itaú → usar para cartões Itaú primeiro. Libera o CDB para outros pagamentos. SEMPRE verificar saldo em conta antes de modelar uso do CDB.
- **Mensalidade de advogado muda tudo.** Um advogado que parece "só cobra se reduzir" pode ter R$ 800/mês de mensalidade que ninguém mencionou. Em 6 meses = R$ 4.800 — mais caro que valor fixo de R$ 4.500. Sempre projetar custo total por tempo (3/6/12/24 meses).
- **Excel/planilhas — off-by-one em named ranges é o bug mais comum.** Section header na linha N, dados na N+1 — mas os named ranges precisam apontar para a linha dos DADOS (N+1), não do header. Sempre validar com `python -c "from openpyxl import load_workbook; wb=load_workbook(...); print(wb['Inputs']['B5'].value)"` antes de assumir.
- **CDB com yield mensal — NUNCA componha saldo negativo.** Fórmula segura: `=MAX(0, H{prev} * (1 + CDB_Yield) + saldo_mês)`. Sem o `MAX(0, ...)` um déficit explode o CDB exponencialmente (multiplica juros sobre juros negativos). Ver `references/geracao-excel-fluxo.md` para o padrão completo.
- **LibreOffice headless recalc precisa de diretórios SEPARADOS para input e output.** `--outdir` falha se for o mesmo dir do input (SfxBaseModel error 0x4c0c). Padrão correto:
  ```bash
  rm -rf /tmp/recalc_in /tmp/recalc_out && mkdir /tmp/recalc_in /tmp/recalc_out
  cp <input.xlsx> /tmp/recalc_in/model.xlsx
  libreoffice --headless --calc --convert-to xlsx /tmp/recalc_in/model.xlsx --outdir /tmp/recalc_out
  cp /tmp/recalc_out/model.xlsx <input.xlsx>
  ```
  Após o recalc, as fórmulas têm valores calculados (importante para o `data_only=True` do openpyxl).
- **CDB saldo no final de CADA mensagem sobre fluxo de caixa.** Regra absoluta do Igor (13/08/2026): toda resposta sobre fluxo de caixa termina mostrando o saldo do CDB. Zerar é o pior cenário possível. Formato: `🔒 Status do CDB (X23): Saldo atual R$ X | Mínimo Out/26 R$ Y | Final Dez/30 R$ Z`.
- **VALLO nunca atrasa** (confirmado 13/08/2026) — Igor explicitamente marcou VALLO como receita garantida. Cai sempre na conta Nubank dia 5 útil.
- **Imprevistos R$ 1.000/mês como linha separada** (não diluído em Outros). Decisão 13/08/2026 — Igor prefere R$ 1.000/mês ao invés de R$ 200-300. Sempre incluir como `Imprevistos` separado no fluxo, com fórmula `=Imprevistos` (named range).
- **Cartões em negociação SÓ são pagos quando CDB ≥ R$ 150k.** Decisão 13/08/2026 — deixar cartões em aberto/parcelando até CDB atingir threshold. BrasilCard R$ 647 foi removido da negociação (Igor vai pagar mensalmente). 6 cartões restantes somam R$ 62.744.
- **Verba indenizatória: VALLO nunca entra na rescisão**, mas **multa 40% + saldo saque-aniversário LIBERA** na dispensa. Caixa imediato na dispensa = líquido_emp + multa_40% + saldo_bloqueado. Total típico R$ 80-100k vs R$ 30-40k em pedido demissão.
- **Seguro-desemprego: Igor NÃO é elegível** (confirmado 27/07/2026) — não incluir em nenhum cenário de rescisão. Cobertura deve vir só da rescisão + CDB + reserva pessoal.
- **Cronologia de mensagens: sempre executar `date '+%Y-%m-%d %H:%M:%S %Z (%A)'` ANTES de qualquer resposta.** Igor exige cronologia exata. Nunca confiar em data de contexto/memória. Cada resposta começa com o timestamp atual implícito.

## Registrar gasto pessoal com a Adrielly (ledger canônico)

Gastos com a Adrielly vivem em `~/MEGA/Documentos/financas_bancos/GASTOS-ADRIELLY.md` — tabela `| Data | Descrição | Valor (R$) | Categoria | Observação |`, categorias padrão: Presente, Saída/Passeio, iFood/Comida, Casa/Miliciano, Uber/Transporte, Saúde, Outros. Cada lançamento: nova linha + recalcular o **Total geral**.

- A página `gastos_adrielly/index.html` lê o `dados.json` irmão — **regenere o `dados.json` a partir do MD a cada lançamento**; ele pode estar desatualizado com dados de exemplo divergentes do canônico (o viewer publica números errados silenciosamente), então nunca confie nele como fonte nem assuma sync.
- Gasto sem finalidade informada: lançar como categoria `Outros` com descrição do meio de pagamento (ex.: `Pix`) — não inventar propósito.
- Compras para a casa dela são registradas em `~/MEGA/Documentos/relacionamentos/adrielly/PENDENCIAS-CASA-ADRIELLY.md` (checkbox marcado = não entra mais no lembrete cron); gasto e pendência são controles separados — registrar em ambos só quando a compra realizada também for custo dele.

## Referências

- `references/dark-mode-ocr.md` — Técnicas para extrair texto de screenshots em modo escuro
- `references/due-diligence-advogado.md` — Checklist completo de due diligence para avaliação de escritório de advocacia (OAB, CNPJ, Jusbrasil, Reclame Aqui, honorários, red flags)
- `references/dossie-template.md` — Template completo do dossiê para advogado (5 seções + geração PDF + envio email)
- `references/fluxo-caixa-contas-consumo.md` — Projeção de fluxo de caixa incluindo contas de consumo (luz/gás) pagas no crédito + estratégia Dígio
- `references/geracao-excel-fluxo.md` — Padrão para gerar Excel + Markdown do fluxo de caixa com openpyxl (inclui pitfalls off-by-one, MAX(0,...) e LibreOffice recalc)
- `references/emissores-cartoes.md` — Mapeamento de emissores de cartões de loja (Atacadão=Carrefour, Méliuz=PAN, C&A=Bradescard, etc.)
- `references/analise-oferta-salario-clt.md` — INSS/IRRF progressivos reais + fórmulas de pacote de caixa para avaliar ofertas de emprego
- `references/phd-matematica-financeira.md` — Equações PhD de matemática financeira pessoal (VPL, TIR, regra dos 4%, janelas ótimas, etc.) — referência da skill `phd-financas-pessoais`
- `references/apresentacoes-pptx.md` — Pipeline completo para pedidos de "análises estatísticas + apresentação" sobre um arquivo canônico: stats em Python → matplotlib PNGs → deck 16:9 python-pptx → verificação visual → entrega via Telegram
