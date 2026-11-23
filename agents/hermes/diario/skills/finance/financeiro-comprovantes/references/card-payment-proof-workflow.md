# Card payment proof workflow

Use this checklist when the user sends a card payment receipt image/PDF and expects the financial archive to be updated.

## What to extract

- payment date and time
- amount paid
- beneficiary / favorecido
- destination bank
- due date shown on the receipt
- payer name
- origin bank / agency / account
- transaction ID / auth / NSU when present
- barcode / linha digitável when present

## What to create

- Save the original file in the month folder
- Create a matching `.md` with structured metadata
- Use a filename that includes the actual paid amount in centavos, e.g. `R163885`
- Link the receipt to the corresponding control/debt item

## What to update

- `AAAA-MM_00_CONTROLE_PAGAMENTOS.md`: mark the item as paid and link the comprovante
- `AAAA-MM_00_DIVIDA.md`: also mark the debt entry as paid when that file tracks the same obligation

## Practical pitfalls

- If the receipt and the control file disagree, trust the receipt for fields it visibly proves and update the ledger to match it.
- Attribute each field to its source. A card name/final supplied by the user but absent from the receipt must be labeled as user-provided; a bank beneficiary alone does not prove the specific card.
- When editing large monthly markdown files, re-read the current file before patching; partial views can lead to malformed table rows.
- `read_file` renders output as `LINE_NUM|CONTENT`; for a Markdown row whose content starts with `|`, the display naturally shows adjacent pipes. Do not “repair” table delimiters based only on that visual prefix—inspect/search the actual content.
- Do not update aggregate totals by blindly adding the new receipt amount. First identify the total’s meaning (gross monthly obligations, paid-in-month audit, or outstanding debt), then recompute from the authoritative rows using the file’s existing inclusion rules.
- A paid receipt may belong in both the monthly payment audit and a debt ledger, but its effect on an **outstanding debt** total may be zero or negative rather than additive.
- After saving, verify the original and `.md` exist, the new entry appears in each applicable ledger, links resolve, table column counts remain consistent, and any aggregate total reconciles with its definition.
