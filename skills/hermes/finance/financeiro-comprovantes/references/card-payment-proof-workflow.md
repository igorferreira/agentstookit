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
- whether a transaction reference or payment code is present; do not copy the full value into derived records, and retain only a masked suffix if it is indispensable for reconciliation

## Intermediary receipts and card-funding source

1. Separate fields visible in the receipt from context supplied by Igor. An intermediary receipt that says `Cartão` proves the method, not the issuer, brand, or final digits. If Igor identifies the source card, record it explicitly as user-provided and do not imply that OCR or the receipt confirms it.
2. Reconcile the receipt to the original bill and the payment/control records for both the obligation month and payment month. Compare beneficiary/CNPJ and any reference directly in the originals without reproducing full identifiers in derived records; compare invoice period, due date, amount and transaction status, and search nearby months for an existing payment of the same obligation.
3. Do not link or mark an obligation `Pago` when the beneficiary is masked, a prior row may already have paid the bill, or the records conflict. Keep it `Revisar` until a unique match is established; an amount difference alone neither proves a second bill nor proves a duplicate.
4. If the user confirms that a credit card funded the intermediary payment, track both sides: the matched utility obligation and the new liability on the source card. Follow the main skill's `Pedaladas e pagamentos cruzados` workflow so the card charge is not lost or double-counted as cash.

## What to create

- Save the original file in the month folder
- Create a matching `.md` with structured metadata
- Use a filename that includes the actual paid amount in centavos, e.g. `R163885`
- Link the receipt to the corresponding control/debt item

## What to update

- In `AAAA-MM_00_CONTROLE_PAGAMENTOS.md`, mark an obligation as paid and link the receipt only after it is uniquely matched to the original bill. If the receipt proves a title was settled but does not identify the specific obligation, record the confirmed cash outflow as an unmatched payment-audit item and keep the candidate obligation `Revisar`, outside reconciled obligations/debt totals until a unique match is established.
- Update `AAAA-MM_00_DIVIDA.md` only when it tracks that specifically matched obligation; never reduce a card or debt based on amount or beneficiary resemblance alone.
- Do not alter outstanding-debt totals or projections for an unmatched payment.

## Practical pitfalls

- If the receipt and the control file disagree, trust the receipt for fields it visibly proves and update the ledger to match it.
- Attribute each field to its source. A card name/final supplied by the user but absent from the receipt must be labeled as user-provided; a bank beneficiary alone does not prove the specific card.
- When editing large monthly markdown files, re-read the current file before patching; partial views can lead to malformed table rows.
- `read_file` renders output as `LINE_NUM|CONTENT`; for a Markdown row whose content starts with `|`, the display naturally shows adjacent pipes. Do not “repair” table delimiters based only on that visual prefix—inspect/search the actual content.
- Do not update aggregate totals by blindly adding the new receipt amount. First identify the total’s meaning (gross monthly obligations, paid-in-month audit, or outstanding debt), then recompute from the authoritative rows using the file’s existing inclusion rules.
- A paid receipt may belong in both the monthly payment audit and a debt ledger, but its effect on an **outstanding debt** total may be zero or negative rather than additive.
- After saving, verify the original and `.md` exist, the new entry appears in each applicable ledger, links resolve, table column counts remain consistent, and any aggregate total reconciles with its definition.
