# Dossiê do Advogado — Consolidated Card Table

Use when the user asks for a comprehensive single-table deliverable for the lawyer (or external advisor), with every card's full profile in one view.

## Trigger

- `"dossiê do advogado"`, `"documento para o advogado"`, `"preciso de um resumo de todos os cartões pra negociação"`, or any request to "consolidate everything about my cards into one document for the lawyer".

## Table Schema

The table must have exactly these columns, in this order:

| # | Cartão | Final | Emissor | Vencimento | Fechamento | Limite total | Disponível | Dívida agosto | Dívida futura (parcelas) | Status | Obs. |

Legend:

| Ícone | Status |
|:---:|---|
| 🟢 | Pago / saldo zero |
| 🟡 | Em aberto (dentro do prazo) |
| 🔴 | Em atraso |
| ⬜ | Fatura completa ausente — valor parcial |
| ❓ | Sem informação de agosto |

## Data Sources (merge priority)

1. **Fatura fechada / captura do app** → primary for amount, vencimento, status
2. **User declaration** → supplement for future use, bloqueio state, missing faturas
3. **Inventário de cartões** (`INVENTARIO-CARTOES.md`) → final, emissor, historical evidence
4. **Controle de pagamentos** (`CONTROLE_PAGAMENTOS.md`) → payment status cross-check

## Sectioning (canonical structure — updated 30/07/2026)

The dossier follows a fixed structure, consolidated after extensive use:

| Order | Section | Contains |
|---|---:|---|
| 1 | Resumo executivo | Total cards, active debt, documented debt, deficit, **Como chegamos aqui** (narrative context for good-faith debtor defense), **Documentação disponível** (evidence list), **⚠️ Risco do imóvel** (alienação fiduciária highlight) |
| 2 | Situação financeira | Renda mensal (CLT + VALLO), Reserva (CDB), Dívida total (cards + pessoal), Dívida Paulo detail, Empréstimo C6 detail |
| 3 | Tabela completa — todos os cartões (26 no dossiê original de 30/07; ver `CONTROLES.md` para a contagem atual) | All cards with full schema, split into: ativos (by vencimento), adiados (next month), 🟢 sem dívida. Plus Resumo Cartão × Banco Emissor × Valor |
| 4 | Análise crítica | RecargaPay detail, cartões estourados/bloqueados, vencimentos por data, faturas abertas (⚠️ podem aumentar) |
| 5 | Base legal — Metodologia dos 280 dias | Reference to lawyer's own methodology, risks, bank-by-bank process risk, legal protections (framed respectfully as "developed by Dr. Israel", not teaching) |
| 6 | Proposta de ação | **Premissa crítica** (C6 parcel impact), Fase 1 (CDB), Fase 2 (renda agosto), Fase 3 (280 dias), Estratégia complementar (Nubank→Passaí), Resumo do plano |
| 7 | Próximos passos | **Explicit call to action**: what the lawyer should do (numbered list), meeting request |

### Narrative principles for legal dossiês

The document must tell a story the lawyer can act on. Before delivering, verify:

1. **Contexto de boa-fé**: how did the debtor get here? (rolling cards, interest compounding, attempted consolidation). This helps the lawyer argue "good faith debtor" under CDC Art. 54-A.
2. **Pedido explícito**: the dossier must end with "what we need from you, Dr. X" — a numbered list of specific asks.
3. **Risco do ativo**: if any debt is secured by real estate (alienação fiduciária), it must be highlighted in the executive summary as the #1 risk.
4. **Premissa de fluxo de caixa**: if a loan installment starts mid-plan, recalculate available income and flag the impact on future phases.
5. **Tom com o advogado**: when referencing the lawyer's own published methodology, frame as "based on the methodology developed by Dr. X" — never as instruction.
6. **Evidência documental**: list exactly what documents back each number (prints, PDFs, contracts).

## Update Rules (living document)

The dossier is **not one-shot** — update it every time new data arrives:

- New fatura received → update row, recalc totals
- Card state changes (blocked→unblocked, zeroed→new charge) → update row, status, observations
- Limit data arrives → fill in the previously ❓ columns
- New card surfaces → add row, update totals

## Cascata de atualização (após cada nova fatura ou mudança de status)

When a new fatura is registered or a card status changes, update **all** of these in the dossier:

### Para fatura nova recebida

1. **Resumo executivo** — recalcular:
   - `Com dívida ativa` (+1 se antes estava sem info)
   - `Cartões sem informação` (-1 se antes estava sem info)
   - `Dívida mínima documentada` (somar o valor novo)
   - `Déficit estrutural estimado` (total - capacidade)
2. **Tabela completa** — atualizar linha do cartão: valor, status (`🟡`), obs (`📄 fatura fechada, OCR <data>`)
3. **Faturas com vencimento iminente** — se vencer até dia 05, adicionar linha e recalcular total
4. **Cronograma de vencimentos** — substituir `❓` pelo valor
5. **Projeção de endividamento** — `Faturas completas` (+1), `Total conhecido` (novo total), `Cartões sem informação` (novo count)
6. **Déficit** — recalcular `Agosto/2026`, `Déficit`, `Meses para quitar`
7. **Pendências documentais** — remover cartão da lista de `Faturas ausentes`
8. **Alerta de superendividamento** — atualizar valor e múltiplo (ex: `6,5x`)

### Para cartão reportado como zerado/cancelado

1. **Resumo executivo** — `Saldo zerado/cancelado` (+1), `Cartões sem informação` (-1)
2. **Tabela completa** — atualizar linha: valor `R$ 0,00`, status `🟢`, obs
3. **Cronograma** — remover linha (se estava listado com `❓`)
4. **Projeção** — `Cartões sem informação` (novo count)
5. **Pendências** — remover da lista de `Faturas ausentes`
6. **Total financeiro** — NÃO altera (zerado não contribuía para o total)

### Sincronização com outros arquivos

Paralelamente, atualizar:
- `AAAA-MM_00_DIVIDA.md` → total do resumo + linha na tabela de dívidas em aberto
- Criar arquivo de evidência `.md` na pasta mensal com dados do OCR
- `DIAGNOSTICO-CARTOES-FATURAS-AGOSTO.md` → se existir para o mês, atualizar counts de resumo

## Pitfalls

- **Limits are rarely on the fatura screen** — most app screenshots show only the bill. Limits need the app's "card management" or "limits" screen. If the user sends a fatura screenshot, mark limit as ❓ and ask for a separate screenshot.
- **Future debt (parcelas)** — most faturas don't itemize future installments. If the user's screenshot shows the installment breakdown (`x/y`), extract it; otherwise mark ❓.
- **Card blocked ≠ zero balance** — they are independent facts. Blocked card can have debt (if frozen mid-cycle) and unblocked card can be zero.
- **Liquidated bank** — if the issuer was liquidated by BCB (e.g. Will Bank), the card is effectively zeroed/cancelled. Add a note and reference the BCB official notice. The card cannot generate new charges.
- **Total never goes down when adding data** — the dossier shows documented debt MINIMUM. Adding a new card always increases or keeps the total, never decreases it. If you think the total should go down, you're probably removing a provisional value that was replaced by a confirmed one — recalc carefully.
- **Payment amount ≠ fatura amount** — when OCR shows both a fatura subtotal (e.g. R$ 1.049,90) and a payment (e.g. R$ 3.245,04), the *fatura value* is the spending amount, not the payment. The payment may cover previous balances too. Always ask the user to confirm which number is the actual fatura when both appear.

## Batch session workflow (high-velocity update sessions)

When updating the dossier multiple times in a single session (e.g., user sends 5+ card screenshots back-to-back), use this efficient pattern:

1. **OCR first, register later** — extract all screenshots with tesseract sweep first, then batch the updates.
2. **`patch` tool, not full rewrites** — use `patch` with targeted `old_string/new_string` for each field that changes. Avoid rewriting the entire file for a single-line change.
3. **Update order**: evidence `.md` → dossiê row → resumo executivo → cronograma → projeção → déficit → pendências → alerta.
4. **Recount totals programmatically** — when possible, verify the new total by summing the table rows rather than adding incrementally (catches off-by-one errors).
5. **One `patch` per logical unit** — group related changes (e.g., total + déficit + alerta value all in one resumo block) into a single patch call with enough context lines to be unique.
6. **After the batch, regenerate the PDF** — use `pandoc → html → wkhtmltopdf` with the custom CSS template from [`references/geracao-pdf-relatorios.md`](references/geracao-pdf-relatorios.md). Full workflow is documented there.

```bash
pandoc DOSSIE-ADVOGADO-CARTOES.md -t html | sed 's/<table>/<table style="width:100%">/g' > /tmp/body.html && \
python3 -c "... inject into CSS template ..." && \
wkhtmltopdf --encoding UTF-8 --no-background /tmp/final.html DOSSIE-ADVOGADO-CARTOES.pdf
```

### PDF quality review (mandatory before delivery)

Igor expects clean, professional PDFs. Before marking the dossier as ready:

1. **No orphaned titles** — every h2/h3 must have content immediately below it. If a header would land at the bottom of a page with its table on the next page, insert a manual page break before the header.
2. **No broken tables** — tables must not split mid-row across pages.
3. **White background** — confirm no dark theme inheritance (`--no-background` + explicit CSS `background: #fff`).
4. **Clean spacing** — sections must have breathing room. No double separators (`---\n\n---`).
5. **No duplicate data** — same income/debt numbers should not appear in 3 different sections. Consolidate before generating.
6. **Last page not empty** — if the last page has only a footer or 1-2 lines, tighten the layout.

Regenerate the PDF after ANY structural change and re-check all 6 points.

Real session example (28/07/2026): ~20 dossier updates in one session — Casas Bahia, Amazon, C&A Pay, Signature, C6 paid, Latam Pass zeroed, South Blackcard zeroed, Porto Seguro (5,7× surprise), PAN Méliuz (5× surprise), BrasilCard (vencimento shifted to September), Digio, Itaú Vivo zeroed — all via incremental `patch` calls. Finished with a complete rewrite for the final version sent to the lawyer.

Para o ciclo completo de reconciliação → dossiê → PDF → email, ver [`references/ciclo-dossie-advogado.md`](references/ciclo-dossie-advogado.md).

## Optional section: estratégia de negociação (280 dias)

When the dossier is for a lawyer specialized in debt negotiation, add a \"Sugestão de negociação\" section after the financial projections. Base it on the lawyer's own methodology (if available as ebook/reference) and cross-reference each card's bank/issuer against the known risk profiles:

- **Nubank**: raramente processa abaixo de R$ 30 mil
- **Itaú**: dívida pode chegar a R$ 1M antes de processar
- **Bradesco**: adiciona seguros/tarifas sem aviso claro
- **Santander**: geralmente processa acima de R$ 30 mil
- **Banco PAN**: ❓ não listado no material de referência — pesquisar política de cobrança
- **RecargaPay**: não é banco, tratamento jurídico diferente

Classificar cartões em tiers: candidatos ideais para estratégia dos 280 dias (baixo risco de processo), candidatos com cautela (risco moderado), e prioridade de pagamento (NÃO atrasar). Incluir seção \"O que os bancos NÃO podem fazer\" (penhora única casa, desconto salário, bloqueio de conta sem ordem judicial) conforme Lei 8.009/1990 e CPC art. 833.
