---
name: short-term-liquidity-management
description: Use for overdraft, Pix-credit, and reserve cash gaps.
version: 1.0.0
---

# Short-Term Liquidity Management

Use this class-level skill for temporary negative balances, overdraft/LIS decisions, PIX on credit, reserve withdrawals, salary-timing bridges, and debt migration between instruments.

## Core principle

Compare financing by the **actual number of days the cash gap will exist**, not by monthly rates alone. A flat one-month fee can be more expensive than a higher-rate overdraft used for only a few days, especially when the bank grants interest-free days.

## Mandatory inputs

1. Current negative balance — label it confirmed or derived.
2. First day the overdraft/LIS was used.
3. Exact date and certainty of the next cash inflow.
4. Remaining interest-free days, verified in the banking app.
5. Overdraft rate, IOF and other charges.
6. PIX-credit net amount, fee, IOF, CET and billing date.
7. Actual withdrawal limit, distinct from the card's total limit.
8. Reserve balance, yield and the user's liquidity preference.

Never recommend a transfer from a derived balance without asking the user to confirm the exact app balance before execution.

## Decision workflow

1. Build the calendar from first use through the next certain inflow.
2. Check whether the gap fits inside a valid free-interest window.
3. Calculate pro-rata overdraft cost and flat PIX-credit cost.
4. Show reserve withdrawal as the mathematical baseline, including opportunity cost.
5. Separate the cheapest option from the option that best preserves liquidity.
6. Define a contingency if the inflow is delayed or the free window expires.
7. Give an executable sequence with dates, app, exact amount and post-action balance.

See [`references/lis-pix-credit-break-even.md`](references/lis-pix-credit-break-even.md) for formulas, same-card pitfalls and recording rules.

## Same-card PIX-credit rule

PIX on credit is a **new purchase/advance**. It does not pay or reduce the current closed statement of the source card.

Correct sequence when reusing the same card:

1. Pay the closed statement through the proper payment channel.
2. Wait for posting and limit release.
3. Simulate PIX on credit in the app.
4. Verify net amount, fee, IOF, CET and which future statement receives the charge.
5. Record it as migrated/deferred debt, never as debt elimination.

If the available withdrawal limit is smaller than the negative account balance, calculate the remaining uncovered amount explicitly.

## Budget and cash-flow integration

- Record completed transactions in the current period's actuals.
- Do not add expenses already included in the base budget a second time.
- Add only genuinely new current-period deltas and future recurring costs.
- For bimonthly or quarterly purchases, show both actual cash timing in purchase months and monthly provision for budgeting.
- Make the distinction explicit so the provision and cash payment are not double-counted.
- Recalculate linked cash-flow artifacts when the new recurring expense changes the structural budget.
- Finish financial outputs with current, minimum projected and horizon-end reserve/CDB balances.

## Output format

Provide a clear verdict first, short option comparison, break-even horizon, execution plan, contingency and reserve/CDB status. Avoid presenting a debt migration as a payment or savings event.

## Verification

- Exact balance marked confirmed/derived.
- Dates and day count checked.
- Free-day rule confirmed or clearly conditional.
- Fees and IOF labeled known/unknown.
- Current statement not confused with the new PIX-credit charge.
- Cash-flow deltas not double-counted.
- Reserve trajectory reconciles.
