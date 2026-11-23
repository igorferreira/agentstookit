# Dossiê Master-Detail para Advogado

## Quando usar

Quando o usuário pedir um dossiê simplificado no formato master-detail para o advogado (Dr. Israel), com todas as dívidas ordenadas da maior para menor.

## Estrutura do documento

PDF de 3-5 páginas com:

| Seção | Conteúdo |
|---|---|
| **Página 1 — Resumo Executivo** | Totais por tipo, cartões em atraso, capacidade, reserva, alerta C6 |
| **Página 2 — Tabela MASTER** | Todas as dívidas maior→menor, com Em atraso?, vencimento, dias |
| **Páginas 3-4 — DETAIL** | Ficha resumida de cada dívida |
| **Página final — Capacidade + HE** | Renda, essenciais, C6, capacidade livre, reserva |

## Colunas da tabela MASTER

| # | Coluna | Descrição |
|---|---|---|
| 1 | Credor | Banco, financeira, pessoa física |
| 2 | Dívida / Cartão | Nome do produto |
| 3 | Tipo | Cartão / Empréstimo pessoal / Consignado / Garantia imóvel |
| 4 | Principal | Valor-base identificável |
| 5 | Prestação | Valor mensal atual |
| 6 | Parcelas rest. | Quantidade pendente |
| 7 | Total exposição | Saldo total sem dupla contagem |
| 8 | Ref. | Mês/Ano |
| 9 | Em atraso? | SIM / NÃO / A CONFIRMAR / NÃO SE APLICA |
| 10 | Venc. em aberto | Data da fatura não paga |
| 11 | Dias atraso | Calculado na data-base |
| 12 | Status | Ativo / Negociação / Quitado / Cancelado |

## Regras de ouro

1. **NÃO enviar antes de mapear o valor ATUAL de cada cartão.**
2. Cada valor classificado como CONFIRMADO | PROVISÓRIO | INCONSISTENTE | SUPERADO.
3. Coluna "Em atraso?" é separada de "Status".
4. Home Equity C6 sempre destacado como prioritário (não pode atrasar).
5. NÃO incluir: promessas de desconto, projeções de acordo, "280 dias" como garantia, conjecturas.
6. Anexos no email: exatamente 2 (dossiê PDF + CCB Home Equity).
7. Toda varredura de cartão deve atualizar a ficha em `_fichas/`.

## Fluxo de trabalho

```
METODOLOGIA (definir colunas, data-base, classificação)
    ↓
CONFIRMAR CCB Home Equity
    ↓
VARREDURA CARTÃO A CARTÃO (maior dívida primeiro)
    ↓
RECONCILIAR (evitar dupla contagem)
    ↓
FECHAR DÍVIDAS NÃO-CARTÃO (Paulo Guerra, consignado)
    ↓
CALCULAR CAPACIDADE DE PAGAMENTO
    ↓
GERAR MD → AUDITAR → PDF
    ↓
REVISÃO COM USUÁRIO
    ↓
ENVIO (só após autorização expressa)
```

## T3 — Varredura: ciclo atômico por cartão

Cada cartão da varredura segue o mesmo ciclo de 7 passos. Executar **um cartão por vez**, do maior para o menor.

### Passo a passo

1. **Receber** — o usuário envia PDF, print do app, ou CSV (Nubank)
2. **Extrair** — `pdftotext` para PDFs, `tesseract --psm 6 -l por` para imagens, `csv.DictReader` para CSV (formato português: vírgula decimal, ponto milhar)
3. **Salvar original** — cópia na pasta mensal com nome padronizado:
   `AAAA-MM-DD_TIPO-CARTAO-FINAL-COMPETENCIA-RVALOR.ext`
4. **Criar Markdown** — na mesma pasta mensal, `.md` com:
   - Metadados (fonte, data extração, arquivo)
   - Resumo da fatura (total, vencimento, status)
   - Parcelamentos ativos (tabela: descrição, parcela x/y, restantes, R$/mês)
   - **Projeção de faturas futuras** (mês a mês, só parcelas recorrentes)
   - Lançamentos do mês (se disponíveis)
   - Para cartões que **não serão pagos**: projeção de juros rotativo (ver abaixo)
   - Observações (pedaladas, riscos, particularidades)
5. **Atualizar ficha** — sobrescrever `_fichas/FICHA_CARTAO_BANCO_NOME.md` com:
   - Cabeçalho padronizado (Nome, Banco emissor, Vencimento, Últimos 4 dígitos)
   - Dados da fatura atual
   - Parcelamentos ativos + projeção
   - Histórico de eventos
   - Observações
6. **Atualizar plano** — `patch` no `PLANO-DOSSIE-MASTER-DETAIL.md`:
   - Linha do cartão na tabela T3: `⬜` → `✅ CONFIRMADO (R$ X.XXX, fonte data)`
7. **Resumo** — tabela de progresso com #, cartão, valor real, status + "X/15 confirmados"

### Padrão de nomes para arquivos da varredura

| Tipo | Padrão | Exemplo |
|---|---|---|
| Fatura PDF | `AAAA-MM-DD_FATURA-BANCO-CARTAO-FINAL-COMPETENCIA-RVALOR.pdf` | `2026-08-07_FATURA-PAN-MELIUZ-4863-AGOSTO-R1216449.pdf` |
| Extrato PDF | `AAAA-MM-DD_EXTRATO-BANCO-CARTAO-FINAL-COMPETENCIA-RVALOR.pdf` | `2026-08-07_EXTRATO-AMAZON-3018-SETEMBRO-R187058.pdf` |
| Markdown | mesmo nome base `.md` | `2026-08-07_EXTRATO-AMAZON-3018-SETEMBRO-R187058.md` |

## Projeção para cartões que NÃO serão pagos

Quando o usuário decide que um cartão **não será pago** (negociação), projetar o efeito dos juros rotativo:

### Passos

1. Identificar a taxa de juros rotativo:
   - Se visível na fatura → usar o valor exato (ex.: PAN 20,49% a.m.)
   - Se ausente → estimar por emissor:
     - **Bradescard** (Casas Bahia, Amazon, C&A): ~15% a.m.
     - **PAN**: ~20,49% a.m. (confirmado em fatura)
     - **RecargaPay**: ~8,75% a.m. (confirmado)
     - **Inter**: ~12-15% a.m. (estimativa)

2. Calcular mês a mês:
   ```
   Mês N+1 = (Saldo_N × (1 + juros)) + Multa(2%) + Mora(1%) + Parcelas_recorrentes
   ```

3. Apresentar como **tabela de projeção** com colunas: Mês, Base, +Juros, +Multa, +Mora, +Parcelas, Total

4. **Rotular como ESTIMATIVA** — valores reais dependem de quando o banco interrompe capitalização

5. **Destacar o alerta**: "Em X meses sem pagar: a dívida dobra de R$ Y para ~R$ Z"

### Exemplo (Casas Bahia 6015, Bradescard ~15% a.m.)

| Mês | Base | +Juros | +Multa | +Mora | +Parcelas | Total ~ |
|---|---|---|---|---|---|---|
| Set/26 | 8.628 | — | 73 | — | 909 | R$ 9.536 |
| Out/26 | 9.536 | 1.430 | 191 | 95 | 400 | ~R$ 11.652 |

## Atualização do plano T3

O arquivo `PLANO-DOSSIE-MASTER-DETAIL.md` na pasta `_Analises/` contém a tabela de varredura. Cada confirmação atualiza uma linha:

```
| 4 | PAN Méliuz | 4863 | 💀 Negociação | ✅ CONFIRMADO (R$ 12.164, fatura PDF 07/08) | — | ✅ |
```

**Regra:** usar `patch` com `old_string` contendo a linha completa original para garantir unicidade. Após cada atualização, apresentar tabela de progresso com:
- Cartões já confirmados (✅) com valor real
- Próximo cartão pendente (⬜) destacado como **PRÓXIMO**
- Contador: "X/15 confirmados" + total mapeado em R$

## Pitfalls

### Plano referencia path errado de arquivo
⚠️ O plano pode conter paths desatualizados (ex.: CCB `2. ccb - vnn.PDF.pdf` quando o real é `1. ccb - vn.pdf`). **Antes de executar T1, verificar com `ls` ou `search_files` — não assumir que o path no plano está correto.**

### CCB: Via Negociável ≠ Via Não Negociável
O contrato CCB [REDACTADA] do C6 é Via **Negociável**, não "Não Negociável" como pode constar em anotações. Confirmar no PDF real com `pdftotext` antes de registrar.

### Projeção de juros sem taxa explícita na fatura
Quando a taxa de juros rotativo não aparece no extrato, **declarar a estimativa usada e sua fonte** (ex.: "~15% a.m. — estimativa Bradescard"). Nunca projetar sem explicitar a premissa.

### Cartão pode ter fatura CLARO e pedaladas internas
Faturas de cartões ativos frequentemente contêm pagamentos de contas fixas (Claro, Light) e pedaladas RecargaPay. Isso NÃO altera a classificação do cartão como ativo/negociação — apenas documenta o uso do limite. A contas fixas pagas no cartão aumentam a dívida do cartão correspondentemente.

### Captura parcial vs completa — a primeira imagem pode mostrar só a fatura ABERTA
⚠️ **PITFALL — já ocorreu em 07/08/2026 com BrasilCard 5382:** O usuário enviou 1 imagem que mostrava apenas a fatura ABERTA (R$ 292,20, vencimento 10/Set). Depois enviou mais 4 imagens revelando a fatura FECHADA (R$ 673,65, vencimento 10/Ago). **A primeira imagem isolada subestimou a dívida em R$ 381,45 (130%).**

**Regra:** quando a captura mostrar \"Fatura aberta\" ou \"Em aberto\", SEMPRE perguntar ou buscar ativamente a fatura fechada do mês anterior — especialmente se o vencimento exibido for para o mês SEGUINTE (ex.: vence 10/Set em pleno 07/Ago). Vencimento distante + fatura \"aberta\" = sinal claro de que há uma fatura fechada mais urgente que não foi capturada.
