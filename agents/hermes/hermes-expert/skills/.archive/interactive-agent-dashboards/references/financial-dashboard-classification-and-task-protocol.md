# Financial dashboard classification and task protocol

Use this reference for incremental personal-finance dashboard work.

## Queue and task records

1. Register the request in the single general queue: `~/clawd/PEDIDOS.md`.
2. Keep the project's `dashboard/TASKS.md` as an internal summary/status only; never treat it as a second general queue.
3. Create `dashboard/tasks/NNN_<snake_case>.md` with sources, scope, decisions, tests, evidence, caveats, and final status.
4. Update all three records after implementation and verification.

## Source classification

Before UI work, read the canonical Markdown sources and separate:

- card cadastro: issuer, final, limits, due/closing dates;
- monthly recurring costs;
- subscriptions;
- observed per-operation fees;
- budget limits/provisions;
- invoices, debt, installments, payments, and negotiations.

Never classify an observed per-operation fee as a monthly recurring cost. Never mix invoices/debt into recurring expenses. Missing fields must render `Não informado`; do not infer them.

Subscriptions with explicit evidence should use the type `Assinatura`, not generic fixed cost. Test both subscription count and derived monthly total. Derived totals must be calculated from classified rows and checked against the canonical source.

For daily-budget screens without a canonical realized-expense ledger, show only a clearly labeled calculated limit and state that realized spending is unavailable.

## Verification sequence

After each feature:

- add parser/model fields before rendering;
- append the page to every shared navigation template;
- regenerate JSON/HTML;
- run parser/reconciliation tests;
- run `node --check` for every generated JavaScript;
- request-test every generated route;
- record exact counts, totals, hashes, and caveats in the review report.

Maintain the honest distinction between a running server/tunnel and implementation work in progress.
