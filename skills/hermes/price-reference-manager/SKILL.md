---
name: price-reference-manager
description: "Use when checking if a product price is cheap or expensive." 
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Prices, Comparison, Household, Shopping]
---

# Price Reference Manager

Maintain a structured reference of product prices across sources so you can instantly tell if a new quote is cheap or expensive. Three-file pattern per domain:

1. **LIVRO-RAZAO-PRECOS-<DOMINIO>.md** — append-only chronological ledger (all entries)
2. **CATÁLOGO-PRECOS-<DOMINIO>.md** — macro view by category/product (best costs/liters, ranges)
3. **TABELA-REFERENCIA-BARATO-CARO-<DOMINIO>.md** — decision table with verdict rules + compact faq by product
4. **CATÁLOGO-REFERENCIA-PRECOS.json** — machine-readable stats (min, max, counts per product key)

Always store price files under `~/MEGA/Documentos/financas_bancos/`.

## Naming Convention

All raw registry files MUST use the prefix `REGISTRO-PRECOS-<DOMINIO>.md` where DOMINIO = `LIMPEZA-HIGIENE`, `SUPERMERCADO`, `HORTIFRUTI`, etc. No inverted forms (`PRECO-...-REGISTRO`).

Catalog/master files use `CATÁLOGO-PRECOS-<DOMINIO>.md` (macro read-only). Decision tables use `TABELA-REFERENCIA-BARATO-CARO-<DOMINIO>.md`. Data files use `CATÁLOGO-REFERENCIA-PRECOS.json`.

## Procedure

### 0. Check for existing infrastructure
Before creating anything, search `~/.hermes/skills/`, `~/MEGA/Documentos/financas_bancos/`, and `memory/` for existing registry files, catalogs, or pricing skills related to the domain. If found, extend them; do not create duplicates.

### 1. Parse the inbound message(s)
Extract from user input: brand, product name, volume/quantity, price (total and per-unit), source/platform, conditions (PIX, bulk, installment), link (if present), date.

**Unit normalization**: Always compute cost-per-unit (per liter, per kg, per unit) when applicable. For mixed units, convert to the smallest common denominator (e.g., R$/L for liquids, R$/kg for solids).

For list messages (multiple products from same source): extract all in parallel, not one-by-one.

### 2. Classify the price BEFORE saving
Search the product reference data (catalog JSON or LIVRO-RAZAO for matching product). Compare new price/unit against known min and max.

Classification matrix:

| Veredicto | Condição | Ação |
|-----------|----------|------|
| 🔥 MUITO BARATO | ≤ 90% do mínimo histórico ou novo recorde | COMPRAR AGORA |
| 👍 BARATO | 90–100% do mínimo histórico | Bom momento |
| 😐 NORMAL | Entre mínimos e máximos (+5% tolerância) | Qualquer hora OK |
| ⚠️ CARO | >130% do mínimo | Esperar promoção |
| ❌ MUITO CARO | >150% do mínimo | Não comprar agora |

If only 1 historical record exists: label "⬜ SÓ 1 REGISTRO" — note "Ação: registrar mais fontes para ter baseline". Cannot declare stable/cheap/expensive definitively.

Include the veredict inline in the ledger entry as an observation tag.

### 3. Write to LIVRO-RAZAO (append-only)
Each entry: date-first ordering, full fields (marca, produto, volume, local/plataforma, preço total, preço unitário, custo/unidade, condições, link, observações com veredicto).

Never modify past entries. Only APPEND new rows.

### 4. Update CATÁLOGO (macro view)
Refresh the catalog's best-costs tables and category summaries after appending. Identify updated best prices.

### 5. Regenerate TABELA DE REFERÊNCIA
Rebuild the decision table with current min/max ranges and verdict thresholds per product. Include the product summary section listing which products have ≥2 records vs only 1.

### 6. Update machine-readable catalog (JSON)
Parse LIVRO-RAZAO, group by normalized product key (marca|produto[:50]), compute: min/max cost/unit, count of records, variation percentage, all individual records. Write to `CATÁLOGO-REFERENCIA-PRECOS.json` in the same directory.

Done when the JSON round-trips back to identical stats from the LIVRO-RAZAO.

## Product Key Normalization

Group products by normalized key: `marcalower|produtolower[:50]`

Example keys:
- `topmar|sabonete líquido perolizado frutas vermelhas`
- `urca|desinfetante urca pinho`
- `braslimpo|azulim ação clareadora sem perfume`

Different volumes of the same base product are SEPARATE keys. Same formula in different sizes = different rows but cross-reference in observations.

## Variation Classification

After ≥2 records exist, calculate spread between min and max:

| Spread | Status | Recommendation |
|--------|--------|----------------|
| 0% | ✅ ESTÁVEL | Comprar a qualquer momento |
| <15% | 🟢 Baixa variação | Bom momento em qualquer ponto da faixa |
| 15–40% | 📊 MODERADA | Esperar se preço atual > R$ (min × 1.2)/un |
| >40% | 📉 ALTA VOLATILIDADE | Comprar AGORA se ≤ R$ (min × 1.1)/un |

## Pitfalls

- **Compare unit cost, never total price.** A 5L bottle at R$30 may be cheaper per liter than a 500ml bottle at R$8. Always normalize to R$/L or R$/kg.
- **Single-record products cannot be classified.** "Só 1 registro" means no baseline — report the price but flag that more sources needed for cheap/expensive judgment.
- **Don't force-match similar products.** Same brand, different line (e.g., Vanish gel sachê vs frasco vs profissional) = different products. Don't collapse them into one key.
- **Append only.** Never edit previous entries. The integrity of historical tracking depends on immutable records.
- **Price varies by channel.** Same SKU differs across supermarket, Shopee, distributor, wholesale. Record both product AND source; don't average across vastly different channels without noting the discrepancy.
- **Bulk pricing changes unit economics.** Kit of 12 may have lower unit cost than single, or the seller may inflate bundle price. Verify per-unit math.
- **PIX/discount adjustments:** Some entries show "original" vs "PIX" price. Always use the FINAL price paid for classification. Note the original in observations.

## Verification Checklist

- [ ] Unit cost computed correctly (divide total by volume, handle decimals)
- [ ] Price classified before being saved
- [ ] Entry appended to LIVRO-RAZAO with correct date order
- [ ] CATÁLOGO refreshed with new best prices identified
- [ ] TABELA DE REFERENCIA rebuilt with updated min/max ranges
- [ ] JSON catalog regenerated and round-trip verified
- [ ] All files use REGISTRO-PRECOS-<DOMINIO>.md naming convention
- [ ] No previous entries modified

## References

See `references/price-classification-matrix.md` for extended comparison rules and cross-domain benchmarks.