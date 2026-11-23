# LIS vs PIX on Credit: Break-Even and Recording

## Cost formulas

For principal `P`, monthly overdraft rate `i_lis`, PIX-credit percentage `i_pix`, days `d`, fixed fee `F`, and taxes/IOF `T`:

```text
approx_lis_cost(d) = P × i_lis × d / 30 + T_lis
pix_credit_cost = P × i_pix + F + T_pix
break_even_days = 30 × (i_pix + (F + T_pix - T_lis)/P) / i_lis
```

These are screening formulas. Use the bank's CET or app simulation when available. Compound daily accrual if the contract requires it.

## Interest-free windows

- Count from the first day the account became negative through the date funds will settle.
- Confirm whether the benefit counts calendar or business days.
- Confirm remaining free days in the app; prior use in the same month may have consumed them.
- Interest-free does not necessarily mean tax-free; label IOF separately.
- If the certain inflow arrives inside the window, a new one-month credit charge is normally unnecessary.

## Same-card warning

A PIX funded by the same card whose statement is due creates a new card transaction. It does not reduce the closed statement. Do not model:

```text
statement payment = cash paid + PIX funded by the same card
```

Instead model:

```text
current statement payment = external cash actually paid
future card debt = PIX principal + fees + IOF
```

Pay the current statement first, wait for limit release, then simulate the new transaction.

## Limit coverage

Use the actual cash/withdrawal limit, not total card limit:

```text
residual_negative_balance = max(0, negative_account_balance - net_pix_received)
```

Show the residual explicitly.

## Reserve comparison

Reserve withdrawal opportunity cost for `d` days:

```text
reserve_opportunity_cost ≈ P × monthly_yield × d / 30
```

State both conclusions when they differ:

- mathematical cheapest option;
- user's preferred liquidity-preserving option.

## Cash-flow recording

1. Current-period completed payments belong in actuals.
2. If an item is already inside the base budget, do not add it again to monthly outflows.
3. Add only unbudgeted deltas and new future recurring costs.
4. For a R$ X purchase every N months:

```text
monthly_budget_provision = X / N
```

Record the actual R$ X cash payment only in purchase months. Label the provision as budget smoothing, not an additional payment.
5. Recalculate reserve trajectory when recurring cost changes.
