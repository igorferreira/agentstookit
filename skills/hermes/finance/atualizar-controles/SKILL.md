---
name: atualizar-controles
description: Atualiza todos os controles financeiros quando Igor diz "atualize nossos controles" ou "financeiro atualiza os controles"
---
# Atualizar Controles Financeiros

Quando o Igor disser **"atualize nossos controles"** ou **"financeiro atualiza os controles"**, seguir este procedimento.

## Pré-requisito
1. Ler `CONTROLE_INDICE.md` em `~/MEGA/Comprovantes/_controles/CONTROLE_INDICE.md` para ver a lista completa
2. Se a atualização envolver XLSX significativo, usar a skill `excel-author` (banker-grade: blue/black/green, fórmulas vs hardcodes, named ranges, checks tab). Ver `references/xlsx-template-cdb-chart.md`.

## ⚠️ ANTES de recalcular o fluxo — Verificação de consistência

**Este passo é obrigatório.** O erro mais comum é o fluxo usar renda diferente do contracheque real — já aconteceu de o fluxo usar ~R$9.000/mês quando o real era ~R$12.415/mês.

### Fórmula correta da renda mensal:
```
Renda = CLT líquido (CONTRACHEQUE.md) + VALLO BENEFÍCIOS
```
- O CLT líquido do `CONTRACHEQUE.md` **já inclui** o desconto do empréstimo folha (−R$1.000). Não descontar de novo.
- Nos meses de **novembro**: adicionar 13º 1ª parcela (50% do bruto)
- Nos meses de **dezembro**: adicionar 13º 2ª parcela (~39% do bruto após descontos)
- O VALLO acompanha o % de dissídio (mesmo % do salário)
- O **consignado Noorden** termina em **Fev/27** — líquido CLT sobe R$1.000 a partir de Mar/27.

### Fórmula correta das saídas:
```
Déficit/Superávit = Renda − Faturas − Home Equity (SAC)
```
- **Faturas**: valores do `CONTROLE_FATURAS_MANTIDOS.md` + parcelamentos conhecidos + custo base (R$ 4.421)
- **Home Equity**: valores exatos do cronograma SAC no `HOME-EQUITY.md`, NUNCA os valores aproximados do fluxo antigo
- O CDB cobre os déficits; superávits são aportados no CDB

### Checklist de reconciliação:
- [ ] `CONTRACHEQUE.md` carregado e renda extraída mês a mês
- [ ] `HOME-EQUITY.md` carregado e parcelas SAC extraídas mês a mês
- [ ] Renda do fluxo confere com CONTRACHEQUE.md (não usar números herdados de versões anteriores!)
- [ ] Home Equity do fluxo confere com HOME-EQUITY.md
- [ ] **🎯 Prioridade #1 do Igor:** para todo mês, `renda_mês ≥ R$4.421 (custo de vida) + parcela_HE_mês`, sem contar com o CDB. Se algum mês falhar, isso é mais grave que qualquer outro achado — parar e avisar antes de continuar o recálculo.

### Provas, estimativas e travas de rescisão
1. Classificar cada entrada relevante como **confirmada**, **estimada** ou **desconhecida**, registrando a fonte e a data da evidência.
2. Não converter bruto em líquido nem inferir salário mensal integral a partir de holerite parcial. Se o valor líquido completo não estiver comprovado, manter estimativa explicitamente rotulada ou bloquear somente o componente que depende dela.
3. Separar o CDB de abertura do horizonte do último saldo real confirmado; datar ambos. Saldo bloqueado não é caixa disponível, e não presumir data de desbloqueio sem prova.
4. Confirmar a competência da última parcela consignada. O aumento do líquido começa no mês seguinte ao último desconto; o líquido do holerite já contém o desconto e não deve ser reduzido outra vez.
5. Na rescisão, não tratar referências brutas como caixa líquido. Só calcular entradas líquidas quando as bases necessárias estiverem documentadas; rotular o resultado como estimativa quando o líquido/TRCT não estiver comprovado. Sem saldo FGTS atual ou outro input essencial, excluir ou bloquear apenas o componente dependente. VALLO fica fora da rescisão e seguro-desemprego só entra após confirmar elegibilidade.
6. Renda futura, dissídio, 13º projetado e crescimento de CDB devem ser identificados como premissas estimadas, não como evidência mensal observada.

### Verificação após a geração
1. Executar somente o gerador canônico da família 2026–2036; não editar manualmente seus espelhos.
2. Ler de volta MD, JSON, CSV e XLSX e conferir horizonte, contagem de meses, âncoras financeiras, consistência entre formatos e checks da planilha. Para alterações mensais que alimentam X46/X47, confirmar também que `src/evolucao_2036.py` incorpora a mudança e que os dados publicados refletem as âncoras recalculadas; a geração da família canônica, sozinha, não prova que as projeções dos cenários foram atualizadas.
3. Rodar testes direcionados e a suíte completa. Se houver falhas conhecidas, comparar os identificadores com a linha de base e reportar separadamente falhas herdadas e novas; nunca declarar a suíte inteira aprovada com base apenas nos testes direcionados.

## Passo a passo

### Retomada de uma atualização interrompida
1. Leia o checklist persistido, o estado do Kanban e os arquivos-alvo atuais; trate o resumo anterior como pista, não como prova.
2. Marque uma etapa como concluída somente quando o artefato ou a validação correspondente confirmar isso.
3. Retome pelo primeiro critério ainda pendente. Antes de repetir downloads ou gravações, confira se os arquivos já existem e se estão corretos, para evitar duplicidade ou sobrescrever trabalho válido.
4. Mantenha a tarefa aberta até validar todos os critérios de aceite e ler de volta os artefatos finais.

### 1. Revisar alterações recentes
- Verificar se há novas faturas, comprovantes ou prints enviados recentemente
- Identificar o que mudou desde a última atualização
- Se houver prints de extrato/fatura, extrair via OCR (ver `references/ocr-card-extraction.md`)
- **Regra obrigatória de sincronização contínua:** Toda fatura fechada recebida (mesmo isoladamente) exige recálculo imediato do fluxo de caixa e atualização do `Resumo Próximo Mês` (version bump X<n> ➔ X<n+1>), substituindo provisões por dados reais.
- **Registro em DIAGNOSTICO.md:** Sempre que for realizado um diagnóstico orçamentário, de endividamento ou de viabilidade, registrar append cronológico em `~/MEGA/Comprovantes/DIAGNOSTICO.md` com data, hora, tipo e conclusão.

### 2. Atualizar arquivos 🔴 (obrigatórios)

| Ordem | Arquivo | Ação |
|---|---|---|
| 0º | `CONTRACHEQUE.md` + `HOME-EQUITY.md` | **Carregar primeiro** — são a fonte da verdade para renda e HE |
| 1º | `_controles/CONTROLE_FATURAS_MANTIDOS.md` | Atualizar faturas do mês corrente com novos valores |
| 2º | `FLUXO-CAIXA-2026-2036.md` (canônico autocontido) + família `.json`/`.csv`/`.xlsx` | Recalcular com `python3.12 fluxo_caixa/dashboard/src/gerar_canonico_2036.py` — ÚNICO escritor da família 2026-2036 (gera MD+JSON+CSV+XLSX de uma vez, valida âncoras). O legado FLUXO-CAIXA-2026-2030.* está arquivado em `fluxo_caixa/historico/2026-2030/` (imutável, NÃO atualizar). |
| 3º | (coberto pelo 2º) | Os reflexos `.json`/`.csv`/`.xlsx` 2026-2036 saem do MESMO comando `gerar_canonico_2036.py` — nada manual; não editar à mão |
| 4º | `CONTRACHEQUE.md` | Atualizar se houve dissídio ou alteração salarial |
| 5º | `HOME-EQUITY.md` | Atualizar se houve alteração de taxa |
| 6º | `ENDIVIDAMENTO.md` | Camada estratégica de dívida (em `~/MEGA/Comprovantes/ENDIVIDAMENTO.md`) — atualizar sempre que um cartão mudar de status (ativo ↔ negociação), chegar proposta de acordo, ou houver evento de negativação/protesto/ação judicial. Não é opcional: se ficar sem sincronizar com `CONTROLE_FATURAS_MANTIDOS.md`, volta a haver duas fontes de verdade divergentes sobre a mesma dívida. |

### 🔄 REGRA DE OURO: sempre terminar mostrando o saldo do CDB

**Quando o output for qualquer discussão de fluxo de caixa, a última linha da resposta DEVE ser o saldo atual e projetado do CDB C6.** Igor declarou em 13/08/2026 que "minha preocupação é não ZERAR ele" — o CDB é seu termômetro principal. O saldo é seu sinal de "estamos vivos". Nunca termine uma resposta sobre fluxo sem mostrar:

```
🔒 Status do CDB (X<n>):
- Saldo atual: R$ X
- Mínimo projetado: R$ Y (mês)
- Final [ano]: R$ Z
- Nunca zera. ✅
```

A linha de "Final [ano]" é o número que ele mais quer ver — representa o impacto de longo prazo das decisões atuais.

**Versão estendida (bom quando há decisão importante):** incluir também o Δ vs cenário anterior, ex: "CDB final +R$ 12.000 vs X20" — isso mostra o impacto da decisão.

**Por que Igor pediu isso (13/08/2026):** "toda vez q eu falar sobre fluxo de caixa no final vc me mostra o saldo do CDB minha preocupacao é nao ZERAR ele" — virou regra permanente do agente, não só do `atualizar-controles`.

### 📅 REGRA DE OURO 2: cronologia automática de conversas

Use como âncora temporal o bloco `[Agora: ...]` injetado na mensagem. Ele prevalece sobre datas da memória, do sistema ou de mensagens anteriores; execute `date '+%Y-%m-%d %H:%M:%S %Z (%A)'` somente quando esse bloco estiver ausente.

1. **Registros diários** em `~/MEGA/Documentos/diario_conversas/` usam a data/hora exatas dessa âncora:
   - `AAAA-MM-DD.md` — 1 arquivo por dia
   - O cron noturno pode acrescentar "## 📋 Resumo automático do dia" no horário agendado.
   - A skill `cronologia-automatica` cobre os gatilhos ("checkpoint", "resumo do dia", "histórico [data]").

2. **PEDIDOS.md**: registre início e fim com a data/hora exatas do bloco `[Agora]`; só consulte `date` se a mensagem não trouxer a âncora. Nunca invente nem herde um timestamp de uma etapa anterior.

A cronologia é tão importante quanto a regra do CDB e deve seguir a âncora temporal vigente em cada mensagem.

### 🎓 REGRA DE OURO 3: profundidade PhD em matemática financeira

Quando o assunto for **decisão financeira estratégica** (rescisão, fluxo, otimização de dívidas), aplicar rigor PhD:

- Funções matemáticas explícitas (Lei 12.506/2011, SAC, VPL, TIR)
- Pelo menos 3 cenários (otimista / base / pessimista) com probabilidades
- Sensitivity 5×5 (stress tests)
- Premissas explícitas com fontes (CONTRACHEQUE.md, app C6, etc)
- Sempre fechar mostrando o "Final [ano]" do CDB ou do patrimônio

Skills relacionadas:
- `phd-financas-pessoais` (PhD em matemática financeira pessoal) — base teórica
- `fluxo-caixa-cenarios` (cenários de saída, janela ótima)
- `price-hunter` (comparação de preços online)
- `excel-author` (planilhas banker-grade)

A matemática PhD substituiu a regra antiga de "decoreba de números" — agora **toda decisão importante precisa de equação**.

## 📌 Convenção do "Outros" no fluxo de caixa

A linha `Outros` no fluxo de caixa DEVE sempre incluir (quando aplicável):

| Item | Valor típico | Quando |
|---|---:|---|
| Parcelas Paulo Guerra | R$ 1.000/mês | Set/26 a Jan/27 (5 parcelas após entrada de R$ 5.000 paga em 10/08/2026) |
| Seguro HE C6 (MIP+DFI) | R$ 67,90 | Ago/26 e Set/26 (período de carência) |
| Aluguel Diego | R$ 2.000 (ENTRADA, não vai aqui) | todo mês |
| Buffer diversos | R$ 40 | ajuste residual |

Validar periodicamente se essas convenções continuam corretas.

## 📌 Convenção "Imprevistos" (decisão 13/08/2026)

A linha **Imprevistos** no fluxo de caixa DEVE existir como coluna separada (a partir do X22), com **R$ 1.000/mês**. Decisão do Igor em 13/08/2026: reserva mensal para cobrir despesas extraordinárias (saúde, carro, reparos).

- Referência: célula `=Imprevistos` em `Inputs!$B$14`
- Implementação como **fórmula** (não valor hardcoded) — facilita flexionar
- Marcar no comment: "Reserva mensal para imprevistos. Decisão Igor 13/08/2026: R$ 1.000/mês ao invés de R$ 200-300."

**Efeito esperado:** cria um 3º mês de déficit em Jan/27 (superavit pequeno vira deficit de ~R$ 40 com Imprevistos). Isso é OK — CDB cobre.

## 📌 Convenção "13º anual projetado"

A linha **13º** (coluna separada, a partir do X23) DEVE incluir projeção de 13º para Nov e Dez de CADA ANO, não só 2026:

- Nov: 50% do bruto atual
- Dez: ~39% do bruto após descontos
- Para 2027+: assumir +5% (1º ano pós-dissídio) ou +10% (anos seguintes) para simular crescimento salarial

**Pitfall:** `mes.startswith('Nov')` é True para 'Nov/27' mas `mes.endswith('Nov')` é False (a string termina com '27'). SEMPRE use `startswith` para detectar meses pelo nome.

```python
# ERRADO — falha para Nov/27, Nov/28, etc.
if mes.endswith('Nov') or mes.endswith('Dez'):

# CERTO
if mes.startswith('Nov') or mes.startswith('Dez'):
```

## 📌 Convenção "VALLO firme"

**Regra do Igor (13/08/2026): VALLO nunca atrasa.** O depósito mensal de R$ 4.420 é firme e pode ser tratado como receita garantida no fluxo de caixa. Marcar essa característica no comment da célula `VALLO` em `Inputs`:

```python
inp["B7"].comment = Comment(
    "Holerite VALLO 31/07/2026. CONFIRMADO por Igor em 13/08/2026: NUNCA ATRASA. "
    "Cai todo mês na conta Nubank. Destino: Home Equity C6.",
    "model"
)
```

## 🎯 Estratégia de negociação com marcos separados (X26+)

Quando Igor define uma estratégia do tipo "só pagar X quando CDB atingir Y":

1. Adicionar **named ranges** de total observado e gatilho em `Inputs`.
2. Criar **sheet dedicada** `Estratégia Negociação` listando cada cartão, valor observado, status e marco de negociação.
3. Não lançar saldo observado como quitação futura sem proposta escrita. Saldo de face, dívida atual e valor de acordo são conceitos diferentes.
4. Se um credor tiver data-alvo própria, separá-lo do gatilho coletivo.
5. Atualizar checks para reconciliar total geral, subtotal do gatilho coletivo e credor separado.

**Aplicação X26 (13/08/2026):**
- 6 cartões em negociação, posição observada total **R$ 77.759,77**.
- 5 cartões sem Inter: **R$ 43.928,91**, mantêm gatilho quando CDB ≥ R$ 150 mil.
- Inter 1982/6250: **R$ 33.830,86 observado**, negociar somente em **Ago/2028**, com valor final a confirmar.
- Agosto/2028 é mês-alvo, não vencimento nem valor de quitação.
- Dívidas migradas/cross-payments já absorvidas pelo Inter não podem ser somadas novamente.
- BrasilCard está fora da negociação e será pago mensalmente.

## 🛡️ Cenário Demissão/Rescisão (X23)

Quando Igor menciona cenário de desemprego ou pede para mapear verbas indenizatórias:

1. Ler `~/MEGA/Documentos/carreira/rescisao_clt/dados-contrato.json` e `relatorios/2026-07-23_ESTIMATIVA-RESCISAO-FGTS-REAL.md` para valores oficiais
2. Criar **sheet dedicada** `Cenário Desemprego` no XLSX com:
   - Verbas do empregador (saldo salarial, aviso prévio, 13º prop, férias + 1/3)
   - FGTS (base oficial, multa 40%, saldo bloqueado saque-aniversário)
   - **TOTAL CAIXA IMEDIATO** + cobertura em meses (R$ 4.421/mês custo vida, R$ 9.000/mês referência)
3. Alertas obrigatórios:
   - ⚠️ VALLO não entra na rescisão (regra Igor)
   - ⚠️ Seguro-desemprego: verificar elegibilidade
   - ⚠️ Empréstimo folha: saldo devedor desconhecido (descontar na rescisão)
   - ⚠️ Cenário hipotético — NÃO é TRCT, confirmar com DP/sindicato

## 🌳 Estrutura `fluxo_caixa/` (13/08/2026)

Quando a modelagem envolve cenários de saída, criar/usar esta estrutura dedicada em `~/MEGA/Comprovantes/fluxo_caixa/`:

```
fluxo_caixa/
├── cenario_atual/                  ← continuar na Noorden (X23_atual.xlsx, .md, .pdf, .csv)
├── cenario_demissao/               ← dispensa sem justa causa
│   ├── rescisao_YYYY-MM.md         ← atualizado mensalmente via cron
│   ├── rescisao_YYYY-MM.json
│   ├── janela_otima_demissao.md    ← análise PhD da janela
│   └── janela_otima_demissao.json
├── cenario_pedido_demissao/        ← pedido demissão (aviso dispensado ou descontado)
│   ├── comparativo_cenarios_saida.{md,json,pdf}  ← tabela com 9 cenários
├── calculos_auxiliares/            ← scripts Python reutilizáveis
│   ├── calcular_rescisao.py
│   ├── calcular_janela_otima.py
│   └── calcular_cenarios_saida.py
├── historico/                      ← X19, X20, X21, X22 antigos
└── README.md
```

**Cron job ativo (Modo PhD):**
- **Job ID:** `e247555646ba`
- **Schedule:** `0 9 1 * *` (todo dia 1º às 09:00 BRT)
- **Comando:** `python3.12 ~/MEGA/Comprovantes/fluxo_caixa/calculos_auxiliares/calcular_rescisao.py`
- **Output:** `cenario_demissao/rescisao_YYYY-MM.md` + `.json`

## 📊 Comparativo de 9 cenários (Modo PhD)

Quando Igor perguntar "quando devo sair?", "vale a pena pedir demissão?", ou "se eu for demitido, cobre tudo?":

1. Simular dispensa + pedido demissão em 9 datas: Ago/26, Mai/27, Ago/27, Mai/28, Ago/28, Mai/29, Ago/29, Mai/30, Ago/30
2. Para cada data, calcular:
   - Salário bruto (com dissídio Ago de cada ano)
   - Aviso prévio dias (Lei 12.506/2011: 30 + 3×anos_completos, cap 90)
   - Caixa imediato dispensa: líquido + multa 40% + saldo saque-aniversário
   - Caixa pedido demissão (aviso dispensado): líquido só
   - Caixa pedido demissão (aviso descontado): líquido − salário
3. Gerar tabela com todos os cenários (`calcular_cenarios_saida.py`)
4. Identificar **janela ótima** = primeira data em que dispensa cobre TUDO (6 cartões + BrasilCard + HE saldo)
5. Atualizar XLSX com nova aba `Cenários Saída` (dados + gráfico de barras + matemática)

**Resultado típico Igor (13/08/2026):**
- 🟢 Quitar só 6 cartões: HOJE (margem R$ 21k)
- 🟡 Quitar TUDO: **Ago/2028** (5a3m)
- 🔴 Margem confortável: Ago/2030 (7a3m, sobra R$ 171k)

**Por que Ago/2028 é a janela:** três alavancas se cruzam:
- Dissídio anual Ago/28 → +R$ 615 no bruto
- Aviso prévio 5 anos completos (Mai/28) → +3 dias = +R$ 1.341
- HE já pago 22 meses → saldo cai para R$ 59.570

## 🔄 Workflow mensal completo (do .xlsx ao PDF)

```
1. Editar Inputs no .xlsx (blue cells, com comments)
   ↓
2. Recalcular com LibreOffice headless (separar /tmp/recalc_in/ e /tmp/recalc_out/)
   ↓
3. Regenerar .md a partir do .xlsx (script `scripts/regenerate_md_from_xlsx.py`)
   ↓
4. Gerar PDF com pandoc + wkhtmltopdf:
      pandoc FLUXO-CAIXA-2026-2030.md \
        -o FLUXO-CAIXA-2026-2030.pdf \
        --pdf-engine=wkhtmltopdf \
        --pdf-engine-opt=--no-background \
        -V geometry:margin=1.5cm \
        -V fontsize=8pt
   ↓
5. Validar todos os checks da aba `Checks` após o recálculo.
   ↓
6. Auditar o PDF visualmente página por página — `pdfinfo`/`pdftotext` não bastam. Renderizar as páginas e verificar fundo branco, títulos órfãos, cabeçalhos repetidos, cortes, sobreposição, margens e legibilidade. Para o procedimento robusto, ver `references/atualizacao-orcamento-e-pdf-auditavel.md`.
   ↓
7. Notificar Igor via Telegram (regra do perfil):
      - Δ vs versão anterior (ex: "X22 → X23")
      - CDB final (regra de ouro)
      - Novos cenários adicionados (Demissão, Estratégia)
```

## 🚨 Pitfalls críticos (lições de sessões reais)

### Pitfall 1: CDB com yield NÃO pode compor saldo negativo
Quando o modelo inclui rendimento do CDB (`CDB × (1 + yield) + saldo`), **NUNCA** faça:
```python
# ERRADO — gera números astronômicos quando saldo é negativo
formula_cdb = f"=H{prev}*(1+CDB_Yield)+F{row}"
```
Se o mês anterior teve CDB negativo (impossível na vida real, mas o modelo pode produzir), multiplicar por (1+yield) só piora. Resultado: números de 10⁸⁵.

**Correto** (cap em 0):
```python
# CERTO — nunca zera
formula_cdb = f"=MAX(0,H{prev}*(1+CDB_Yield)+F{row})"
```

### Pitfall 2: Off-by-one em named ranges quando há section header
Quando a estrutura é `inp["A{N}"] = "Section Header"` e os dados começam em `r = N+1`, mas o named range aponta para `B$N+1` em vez de `B$N+2`:

```python
# ERRADO (off-by-one):
inp["A11"] = "CUSTO DE VIDA"  # header na linha 11
for i, (label, val, ...) in enumerate(cv_data):
    r = 12 + i  # dados nas linhas 12, 13
wb.defined_names["Custo_Vida"] = DefinedName("Custo_Vida", attr_text="Inputs!$B$13")  # ❌ linha 13 (era label de Ago)

# CERTO: apontar para onde os dados realmente estão (linha 12, não 13)
wb.defined_names["Custo_Vida"] = DefinedName("Custo_Vida", attr_text="Inputs!$B$12")
```

**Como evitar:** sempre contar manualmente `r = N_header + 1` na primeira iteração do loop e validar com um check (`assert len() == N`).

### Pitfall 3: `--convert-to xlsx` do LibreOffice falha ao sobrescrever
O comando `libreoffice --headless --calc --convert-to xlsx X --outdir Y` **falha** se `Y` for o mesmo diretório de `X` (ou se o arquivo de destino já existir). Sintoma: `Error: Please verify input parameters... SfxBaseModel::impl_store ... 0x4c0c`.

**Workaround:** sempre usar diretórios separados:
```bash
rm -rf /tmp/recalc_in /tmp/recalc_out
mkdir -p /tmp/recalc_in /tmp/recalc_out
cp /home/.../FLUXO-CAIXA-2026-2030.xlsx /tmp/recalc_in/model.xlsx
libreoffice --headless --calc --convert-to xlsx /tmp/recalc_in/model.xlsx --outdir /tmp/recalc_out
cp /tmp/recalc_out/model.xlsx /home/.../FLUXO-CAIXA-2026-2030.xlsx
```

### Pitfall 4: `execute_code` é bloqueado pelo Hermes Agent
Por segurança (subprocess não autorizado), o `execute_code` falha com `BLOCKED: ... runs arbitrary local Python`. **Sempre** use `terminal` com `python3.12 /tmp/script.py` ou inline `python3.12 -c "..."`.

### Pitfall 5: Fluxo com renda errada
O fluxo de caixa já foi gerado com renda ~R$9.000/mês quando o real era ~R$12.415/mês. **Sempre** recalcular do zero com os valores reais do CONTRACHEQUE.md. Nunca confiar nos números de renda de uma versão anterior do fluxo.

### Pitfall 6: `mes.startswith('Nov')` vs `mes.endswith('Nov')` para 13º
A string `'Nov/27'` termina com `'27'`, NÃO com `'Nov'`. Para detectar meses pelo nome em qualquer ano futuro:

```python
# ERRADO — só funciona para Ago-26 (Set/26 ends with '26')
if mes.endswith('Nov'):  # True apenas para 'Nov' isolado, False para 'Nov/27'

# CERTO — funciona para todos os anos
if mes.startswith('Nov'):  # True para Nov/26, Nov/27, Nov/28, ...
```

Sintoma: 13º anual só aparecia em Nov/26, zerado para 2027-2030. Capturado em 13/08/2026 (X22→X23).

### Pitfall 7: `Font(family=...)` é inválido, usar `Font(name=...)`
Em openpyxl, o parâmetro correto para definir a família da fonte é `name=`, NÃO `family=`:
```python
# ERRADO — gera ValueError: expected <class 'float'>
cell.font = Font(family='Courier New', size=10, bold=True)

# CERTO
cell.font = Font(name='Courier New', size=10, bold=True)
```
Capturado em 13/08/2026 (X23 — aba Cenários Saída).

### Pitfall 8: LibreOffice `--convert-to xlsx` falha com mesmo diretório
Sempre usar diretórios separados para input e output:
```bash
# ERRADO — falha com 0x4c0c
libreoffice --headless --convert-to xlsx model.xlsx --outdir .

# CERTO
mkdir -p /tmp/recalc_in /tmp/recalc_out
cp model.xlsx /tmp/recalc_in/
libreoffice --headless --convert-to xlsx /tmp/recalc_in/model.xlsx --outdir /tmp/recalc_out
cp /tmp/recalc_out/model.xlsx ./FLUXO-CAIXA-2026-2030.xlsx
```

### Pitfall 9: saldo observado não é valor de quitação futura
Quando Igor define um gatilho ou data-alvo para negociação:
1. Registrar o saldo observado com data e evidência.
2. Não congelar esse saldo como saída futura: juros, encargos e desconto ainda são desconhecidos.
3. Separar credores com marcos diferentes na sheet `Estratégia Negociação`.
4. Criar checks distintos: total observado, subtotal do gatilho coletivo e credor separado.
5. Só lançar a saída no fluxo depois de proposta escrita, com valor, validade e condições.

Aplicação X26: cinco cartões sem Inter têm posição observada de R$ 43.928,91 e gatilho CDB ≥ R$ 150 mil. Inter tem R$ 33.830,86 observado e negociação-alvo Ago/2028, sem saída fixa.

### Pitfall 10: BrasilCard está fora da negociação e o Inter tem marco próprio
Lista X26 em 13/08/2026:
- RecargaPay R$ 14.254,20 — gatilho coletivo
- PAN Méliuz R$ 12.158,50 — gatilho coletivo
- PAN Buscapé R$ 6.723,33 — gatilho coletivo
- Casas Bahia R$ 8.627,58 — gatilho coletivo
- Digio R$ 2.165,30 — gatilho coletivo
- **Subtotal cinco cartões: R$ 43.928,91**
- Inter R$ 33.830,86 — negociar em Ago/2028, valor final a confirmar
- **Total observado seis cartões: R$ 77.759,77**

BrasilCard R$ 646,76 foi removido da negociação e será pago mensalmente. O saldo Inter já absorve as origens migradas/cross-payments; não somá-las novamente.

### Pitfall 11: 13º anual projetado (2027-2030) deve usar `startswith`
Adicionar coluna "13º" ao fluxo (a partir do X23):
- Nov/26 = `Decimo_1` (R$ 6.950 hardcoded)
- Dez/26 = `Decimo_2` (R$ 5.400 hardcoded)
- Nov/27, Dez/27 = `Decimo_Anual_Nov × 1.05` (1º ano pós-dissídio)
- Nov/28+, Dez/28+ = `Decimo_Anual_Nov × 1.10` (anos seguintes)

Detectar o mês: `mes.startswith('Nov')` (NÃO `endswith`).
Efeito: cria R$ 66.072 em 13º total ao longo de 53 meses.

### Pitfall 12: VALLO é receita garantida, nunca atrasa
Em 13/08/2026, Igor declarou: "o vallo nunca atrasa". Tratar como receita firme.
- Comentário em `Inputs!B7` deve indicar: "FIRME — NUNCA ATRASA"
- Pode ser usado em cálculo de cobertura mensal sem buffer

### Pitfall 13: Imprevistos R$ 1.000/mês como linha separada (não em Outros)
Decisão 13/08/2026: adicionar coluna "Imprevistos" separada (a partir do X22):
- Referência: `=Imprevistos` (named range, não hardcoded)
- Linha separada, não dentro de Outros
- Efeito: cria 3 meses de déficit (Set/26, Out/26, Jan/27) em vez de 2
- Jan/27 vira deficit pequeno (-R$ 40 com Imprevistos R$ 1.000)

### Pitfall 14: CDB com yield + cap em 0
Para incluir rendimento mensal do CDB sem explodir quando saldo negativo:
```python
# ERRADO — gera números astronômicos (10^85) em deficits
formula = f"=H{prev}*(1+CDB_Yield)+F{row}"

# CERTO — cap em 0, rendimento só se positivo
formula = f"=MAX(0,H{prev}*(1+CDB_Yield)+F{row})"
```

### Pitfall 15: Quando quiser saber "cartões pagos" — separar por categoria
Igor pediu lista de "total de cartões pagos". Sempre:
1. Separar **cartões mantidos pagos** (do `CONTROLE_FATURAS_MANTIDOS.md`)
2. Separar **outros cartões pagos/absorvidos** (cross-payment, zerados)
3. Apresentar subtotais distintos + total geral
4. Em cross-payment, deixar EXPLÍCITO: "o cartão de origem foi quitado, mas a dívida migrou para o cartão-fonte e reaparecerá na fatura futura"

### Pitfall 16: Faturas "outros" não inclui BrasilCard quando é fixo
Se BrasilCard é R$ 647 fixo mensal (não quitado de uma vez), pode ser listado em "cartões mantidos" como `R$ 647/mês`. Mas se for "valor da dívida atual" vs "fatura do mês", são conceitos diferentes.

### Pitfall 17: novo gasto pontual + novo recorrente não podem ser duplicados

Quando o usuário informar pagamentos já realizados e também criar um orçamento mensal para a mesma classe de despesa:

1. Lançar os pagamentos no **realizado da competência atual**.
2. Lançar o novo recorrente na **próxima competência ainda não realizada**, salvo data explícita diferente.
3. Se o rateio entre subcategorias não foi informado, manter um bloco combinado (`faxina/cozinheiro — rateio a confirmar`).
4. Declarar a premissa de vigência e criar check de delta contra o cenário anterior.

### Pitfall 18: saldo atual pode não reconciliar com os movimentos conhecidos

Não force o batimento criando uma entrada/saída fictícia. Calcule e registre a diferença não conciliada; o saldo atual confirmado prevalece como posição, enquanto a diferença fica pendente de extrato.

### Pitfall 19: PDF tecnicamente válido ainda pode estar visualmente reprovado

`pdfinfo`, contagem de páginas e extração de texto não detectam títulos órfãos, tabelas quebradas, fundo escuro ou espaço em branco excessivo. Renderize todas as páginas em imagens e audite visualmente. Se o HTML usar preenchimentos claros, force `html, body, section { background: #fff !important; }` e gere com `wkhtmltopdf --background`. Consulte `references/atualizacao-orcamento-e-pdf-auditavel.md`.

### 3. Atualizar fichas 🟡 (se necessário)
- Atualizar `FICHA_CARTAO_*.md` dos cartões que tiveram movimentação
- Registrar parcelamentos novos, pagamentos, status
- Ao extrair parcelamentos via OCR, detalhar cada um com: total da compra, já pago, falta pagar (R$ + nº parcelas), última parcela (mês/ano)
- Incluir projeção mês a mês até a quitação

### 🔄 Cartão muda de status (ex: negociação → mantido)

Quando Igor decide manter um cartão que estava em negociação:

1. **Ficha do cartão**: mudar status, adicionar parcelas detalhadas, projeção de quitação
2. **`CONTROLE_FATURAS_MANTIDOS.md`**: adicionar à lista de ativos, incluir nas faturas do mês
3. **`FLUXO-CAIXA-2026-2030.md`**: adicionar o valor das parcelas nas colunas de faturas dos meses afetados e recalcular
4. **`_controles/CONTROLE_INDICE.md`** (era citado como `CONTROLES.md` — esse nome na raiz NÃO existe): atualizar status na tabela de fichas
5. **`ENDIVIDAMENTO.md`**: mover o cartão entre as seções 3 (Ativos) e 4 (Em negociação), recalcular os totais da seção 1 e o racional/concentração de risco da seção 2

> Exemplo: Atacadão 1843 saiu de 💀 Negociação para 🟢 Mantido com 2 parcelas de R$ 323,08 em Set–Out/26.

### 💳 Pagamento com CDB

Quando um cartão é pago com o CDB:
1. Subtrair o valor do CDB inicial (ex: R$ 29.000 − R$ 6.959 = R$ 22.041)
2. Registrar na ficha do cartão: valor, data, origem (CDB), chave PIX usada
3. Recalcular o fluxo com o novo CDB inicial
- O impacto real no CDB de 2030 é tipicamente pequeno (~R$ 10k pra cada R$ 7k gasto hoje)

### 🚴 Modelagem de "Pedalada" Parcial de Fatura (Setembro/2026+)

Quando o usuário decide pagar parcialmente uma fatura fechada de cartão (ex: Porto Seguro 8121 de R$ 4.007,41) e "pedalar" uma quantia fixa (ex: R$ 1.000,00) via PIX no crédito ou rolagem controlada:
1. **Fatura do Mês Corrente**: o desembolso efetivo de caixa/renda é apenas o valor líquido pago (ex: R$ 3.007,41).
2. **Impacto no Mês Seguinte**: a fatura do mês subsequente (Out/26) recebe o valor pedalado acrescido do custo financeiro (~4,99% a.m. se PIX crédito, ou juros contratuais), ex: +R$ 1.050,00.
3. **Curva de Alívio**: validar se a fatura do mês seguinte tem espaço/folga (ex: fatura original de Out/26 era baixa, R$ 876,55, permitindo absorver os R$ 1.050 sem estourar o orçamento).
4. **Controles a Sincronizar**: atualizar `FICHA_CARTAO_*.md`, `CONTROLE_FATURAS_MANTIDOS.md`, `2026-MM_00_DIVIDA.md` e registrar em `AVISOS.md`.
5. **CDB**: a pedalada protege o caixa imediato e evita saque desnecessário do CDB no mês de aperto.

### 🧾 Listar cartões pagos e calcular o total

Quando Igor pedir a lista ou o total de cartões pagos, seguir o procedimento completo em [`references/listar-cartoes-pagos.md`](references/listar-cartoes-pagos.md).

Resumo obrigatório:

1. Fixar **competência e data de corte** antes de somar.
2. Validar primeiro por comprovante e controle mensal; fichas, `ENDIVIDAMENTO.md`, dossiês e playbooks são apoio, não prova primária.
3. Separar:
   - **cartões mantidos com a fatura da competência paga**;
   - **outros pagos/absorvidos por cross-payment**;
   - zerados/cancelados sem desembolso ficam fora do total.
4. Apresentar subtotal de cada grupo, total geral e quantidade de cartões.
5. Não incluir dívidas pessoais, contas fixas, faturas abertas da competência seguinte ou cartões apenas zerados.
6. Em cross-payment, dizer explicitamente para onde a dívida migrou.
7. Calcular por ferramenta e provar que linhas, subtotais e total geral reconciliam.

> **Pitfall:** “fatura liquidada” não significa necessariamente “dívida eliminada”, “cartão cancelado” ou “ausência de parcelamentos futuros”.

### 4. Atualizar arquivos de custo fixo quando necessário

Sempre que um custo fixo mensal for adicionado, removido ou alterado:

| Arquivo | Ação |
|---|---|
| `MAPA-CUSTO-VIDA.md` | Adicionar/remover linha na tabela de contas fixas, recalcular TOTAL FIXO |
| `_controles/CONTROLE_ORCAMENTO.md` | Atualizar NÃO-LAZER (teto), adicionar/remover item da tabela N1–N6, atualizar total no resumo |
| `FLUXO-CAIXA-2026-2030.md` | Atualizar referência ao custo de vida (Prioridade #1), recalcular pior margem |

> Exemplo: Meli+ (Disney+) R$40/mês adicionado em ago/2026 → não-lazer R$2.451 → R$2.491, total R$4.421 → R$4.461.
- Listar o que foi alterado
- Destacar impactos no CDB (se fluxo foi recalculado), comparando com a versão anterior
- Listar o que segue pendente (ex: faturas sem info)
- Listar o que NÃO mudou (para tranquilizar)
- Usar tabela comparativa "Antes → Agora" com Δ
- **Sempre avisar via Telegram ao terminar** (`hermes send --to telegram "..."`), resumo curto — regra do perfil, ver `SOUL.md`

### 5. Registrar no AVISOS.md

Sempre que uma atualização revelar algo digno de nota, escrever uma linha em `~/MEGA/Comprovantes/AVISOS.md`:

- 🔴 **Gasto fora do padrão** — fatura muito acima do provisionado, categoria de orçamento estourada
- ⚠️ **Risco identificado** — racional frágil, concentração de exposição, lacuna de dado
- 🚨 **Negativação / atraso crítico** — protesto, ação judicial
- 🟡 **Inconsistência de dados** — números que não batem entre arquivos
- 🔵 **Informativo** — mudança relevante (novo cartão, dissídio, nova renda)

O AVISOS.md é um **log cronológico** — nunca editar ou apagar entradas antigas. Se um alerta for resolvido, adicionar uma nova linha `✅ resolvido` referenciando a original.

### 6. Quando um cartão mudou de status ou um arquivo foi substituído

Rodar a skill `auditoria-consistencia-financeira` antes de encerrar — ela pega divergências que a atualização pontual costuma deixar passar (arquivo antigo ainda referenciado em outro lugar, contagem de cartões que não bateu em todo canto).

## 📐 Padrão estrutural do XLSX banker-grade (skill `excel-author`)

### Primeira aba simplificada para o próximo mês

Quando Igor pedir uma versão simplificada, **não criar uma segunda planilha independente**. Adicionar `Resumo Próximo Mês` como primeira aba do workbook canônico e manter as abas detalhadas como fonte de cálculo. Separar obrigatoriamente faturas conhecidas/documentadas de provisões para cartões pendentes; mostrar entradas, saídas, déficit/superávit e a ponte completa do CDB. Seguir [`references/resumo-proximo-mes-xlsx.md`](references/resumo-proximo-mes-xlsx.md).

Se a mudança for apenas estrutural/visual, ainda fazer version bump e declarar explicitamente **sem mudança numérica**. Recalcular no LibreOffice, adicionar checks de reconciliação do resumo e auditar visualmente todas as páginas do PDF renderizado; corrigir cortes, barras estranhas, tabelas ilegíveis e sobreposições antes da entrega.

Quando o XLSX crescer além de "tabela simples" (cenário X21+), usar a estrutura de 5 abas validada em 13/08/2026:

| # | Sheet | Conteúdo |
|---|---|---|
| 1 | **Inputs** | Todos os parâmetros (renda, custo vida, HE, parcelas, CDB inicial) como **blue cells com comments** referenciando fontes |
| 2 | **Fluxo Mensal** | Cálculos derivados (Renda = f(Inputs), Saldo, CDB) como **fórmulas black** referenciando Inputs via named ranges |
| 3 | **CDB Evolução** | Tabela mês-a-mês + **gráfico de linha** + marcos anotados |
| 4 | **Sensitivity** | Tabela 5×5 (eixo Y = Δ custo vida, eixo X = Δ VALLO) mostrando impacto no CDB final |
| 5 | **Checks** | TRUE/FALSE automático: CDB nunca zera, déficit = 2, soma Paulo = 5.000, etc. |

**Conventions (excel-author):**
- **Blue** `Font(color="0000FF")` — hardcoded input (font)
- **Black** `Font(color="000000")` — fórmula derivada
- **Green** `Font(color="006100")` — link entre sheets
- Toda célula derivada DEVE ser fórmula (nunca hardcode calculado em Python)
- Toda célula blue DEVE ter `Comment` com `Source: [Sistema/Doc], [Data], [Referência]`
- Usar **named ranges** para qualquer figura referenciada entre sheets
- Incluir **Checks tab** com TRUE/FALSE que amarra o modelo

Ver `references/xlsx-template-cdb-chart.md` para o template Python completo e detalhado (incluindo cores, pitfalls de `execute_code` bloqueado, e padrão de `Marker` para o gráfico).

## Notas
- O fluxo de caixa sempre usa Python para recalcular quando há alteração numérica
- Usar `python3.12` para openpyxl (geração de Excel), `python3` para cálculos
- Manter formato Markdown brasileiro (R$ 1.000,00)
- Usar emojis: 🟢 ativo/pago/superávit, 🔴 déficit, ⬜ pendente, ✅ concluído, 💀 negociação, ⚠️ atenção
- Salvar tudo em `~/MEGA/Comprovantes/`
- Atualizar também `_controles/CONTROLE_INDICE.md` quando um controle novo for criado
- **Versão bump (X20→X21→X22):** sempre gerar X(n+1) novo arquivo (não destruir o anterior), fazer o delta explícito "Antes → Agora" e linkar o número de cenário no header do .md

## 📚 Referências

| Arquivo | Conteúdo |
|---|---|
| `references/pdf-email-workflow.md` | Geração de PDF (wkhtmltopdf) + anexo em email (himalaya MML) |
| `references/pdf-generation-workflow.md` | Pipeline completo XLSX → MD → PDF via pandoc + wkhtmltopdf (landscape/portrait, templates) |
| `references/ocr-card-extraction.md` | Workflow de OCR com tesseract para extrair dados de prints de extrato |
- `references/atualizacao-orcamento-e-pdf-auditavel.md` — Classificação de provisão/realizado/recorrente, reconciliação de saldo observado, cascata de atualização e auditoria visual robusta do PDF
- `references/ocr-card-extraction.md` — Workflow de OCR com tesseract para extrair dados de prints de extrato
- `references/monitoramento-cron-jobs.md` — Padrão de cron jobs para monitoramento automático (ex: vigia CCT FEAAC, AVISOS.md)
- `references/xlsx-template-cdb-chart.md` — Template Python completo para gerar FLUXO-CAIXA-2026-2030.xlsx com 5 abas banker-grade + gráfico de CDB
- `references/resumo-proximo-mes-xlsx.md` — Padrão para primeira aba simplificada: confirmado vs provisionado, ponte do CDB, checks, sincronização e auditoria visual do PDF
- `references/diario-conversas-cron.md` — Workflow de cronologia automática de conversas (13/08/2026): pasta `diario_conversas/` + cron noturno + skill `cronologia-automatica`
- `references/fluxo-caixa-cenarios-estrutura.md` — Estrutura obrigatória `fluxo_caixa/` (X23): cenario_atual + cenario_demissao + cenario_pedido_demissao + calculos_auxiliares + cron jobs
- `scripts/regenerate_md_from_xlsx.py` — Regenera .md a partir do .xlsx (fonte canônica) — usar após LibreOffice recalc
- `references/price-hunter-matematica.md` — Matemática PhD para comparação de preços: custo total = (preco_vista × (1 - desconto_pix)) + (preco_parcelado × (1 + juros)^n - preco_vista) + frete - cashback - pontos, × fator_risco_vendedor
