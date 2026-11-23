# Payroll Evidence Extraction and Audit

Use this reference when a career-transition or CLT analysis must reconstruct remuneration, vacation history, deductions, and FGTS from a mailbox or a folder of payslips.

## Evidence collection

1. Obtain explicit authorization before accessing the mailbox.
2. Use read-only behavior: list/search/read/download only. Do not send, move, label, delete, or mark messages unless separately requested.
3. Search the all-mail/archive folder, not only Inbox. Combine employer sender/domain, payroll terms (`contracheque`, `holerite`, `recibo de pagamento`), and the employment date range.
4. Keep a manifest with message ID, date, sender, subject, attachment name, and local path.
5. Exclude replies/forwards and documents from prior employment periods unless continuity is proven.
6. Download attachments into an auditable folder and validate every PDF before extraction.

## Deterministic extraction

Prefer local text extraction such as `pdftotext -layout` for digital PDFs. Use OCR only for image-only documents.

For each document, capture:

- payroll type: monthly, 13th first/second installment, vacation, CCT/dissídio complement, or collective instrument;
- competence/month;
- salary base;
- recurring fixed CCT component;
- total earnings, deductions, net, INSS, IRRF, FGTS, and recurring loan deduction;
- source filename and extraction errors.

Write both JSON and CSV. Verify:

- expected document count;
- chronological continuity of monthly competences;
- first and last competence;
- zero parse errors or an explicit exception list;
- sampled values against the original PDF;
- every generated report link resolves.

## Salary normalization

Do not equate total earnings in an unusual month with recurring salary. Vacation, 13th, abono, retroactive CCT, and dissídio can inflate gross totals.

Use a regular full-month payslip to determine:

`recurring remuneration = salary base + recurring salary-nature fixed components`

Keep separately:

- initial/proposed salary;
- current salary base;
- recurring fixed CCT component;
- current recurring remuneration;
- variable-pay average supported by multiple documents.

## Vacation reconstruction

Payroll events can reconstruct periods even when there is no standalone vacation receipt:

- `DIAS FÉRIAS` identifies days taken;
- `DIAS ABONO PECUNIÁRIO` identifies days sold;
- `1/3 DAS FÉRIAS` and `1/3 DO ABONO` corroborate treatment;
- `ADIANTAMENTO DE FÉRIAS` prevents double counting cash across monthly payroll and vacation payment.

Aggregate split events across months by acquisition period. A pattern of 20 days taken plus 10 sold usually liquidates one 30-day entitlement. Still ask the user to confirm that no off-cycle receipt is missing.

## CCT audit

Extract and inspect the current collective instrument, not only payroll lines. Search for:

- validity and date-base;
- salary adjustment and fixed parcels;
- notice-proportional rules;
- seniority/tenure additions;
- special allowance or PLR/PPR exemption;
- age/service indemnities;
- termination-document requirements and normative penalties.

Treat a CCT right absent from the latest payslip as a **possible pending right**, not automatically as proven remuneration. Show a separate sensitivity and request HR/union confirmation.

If indemnified notice projects the employment past the date-base, flag that the next CCT adjustment may require recalculation. Check current TST guidance before adding any one-salary pre-date-base indemnity; do not double count both outcomes.

## FGTS reconstruction

Summing `FGTS do mês` across monthly and extra payroll documents is useful for a documentary estimate and deposit-regularity check. It is not the official current balance or termination base because it can omit:

- monetary correction;
- withdrawals;
- blocked balances;
- missing or late deposits;
- account consolidation effects.

Always preserve three distinct fields:

1. documentary sum of deposits;
2. app/extract current balance;
3. app/extract base for termination purposes.

Run accessibility branches separately for `saque-rescisão`, `saque-aniversário`, and unknown mode.

## Scenario separation

Do not merge these resignation cases:

1. immediate exit with employer waiver and no notice deduction;
2. immediate exit with 30-day notice deduction;
3. 30-day notice actually worked.

The worked-notice case has a later termination date and may change 13th and vacation twelfths. Ordinary salary paid before the final month should be described separately from the TRCT.

For dismissal without cause, project the full statutory/CCT notice and then recalculate 13th and vacation twelfths at the projected end date.

## Conditional deductions and benefits

- A payroll installment proves only the installment amount, not the outstanding loan balance. Do not deduct the whole loan without a payoff statement or contract rule.
- Show unemployment insurance separately from immediate cash because it is conditional and paid over time.
- Keep disputed CCT amounts, unapproved insurance, blocked FGTS, bonus, PLR/PPR, and unknown loan balances outside the conservative core total.

## Repository and automation relocation

When the user moves the career repository:

1. finish and verify active reports before moving when possible;
2. confirm the destination exists and the old source is absent;
3. update scheduled-job workdirs and any absolute paths in prompts/scripts;
4. list the cron job and verify its next run after the move;
5. rerun JSON/PDF/report/link validation from the destination.
