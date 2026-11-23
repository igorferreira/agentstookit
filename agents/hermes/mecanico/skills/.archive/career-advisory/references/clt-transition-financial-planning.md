# CLT Transition Financial Planning (Brazil)

Use this reference when career advice includes preparing for resignation, dismissal, or a job change under Brazilian CLT rules. It is a planning workflow, not legal/accounting advice and not a substitute for the employer's TRCT.

## Scenario set

Always separate at least:

1. **Resignation with notice worked or waived without deduction**
2. **Resignation without notice, with possible notice deduction**
3. **Dismissal without cause**
4. **Mutual agreement under CLT art. 484-A**, only when useful

Do not merge employer-paid termination amounts with FGTS, unemployment insurance, or blocked/conditional assets.

## Core components

- Salary balance: monthly remuneration / 30 × eligible days, capped at the monthly remuneration for a full month.
- Proportional 13th salary: remuneration × eligible twelfths / 12; a month normally counts when at least 15 days are computable.
- Accrued/acquired vacation: remuneration + constitutional one-third.
- Proportional vacation: remuneration × eligible twelfths / 12 + one-third.
- Vacation outside the concessive period may require double payment; validate dates before applying.
- Employer dismissal notice: check Lei 12.506/2011, service length, CCT, and current interpretation; project indemnified notice into service time when applicable.
- Resignation notice: show both worked/waived and possible deduction; do not automatically apply proportional employer-benefit notice against the employee.
- FGTS: use the app/extract's **base for termination purposes** when calculating the penalty, not merely the visible balance.
- Distinguish FGTS current balance, termination base, withdrawal mode, and actually withdrawable amount. Saque-aniversário and advances may block the balance.

## Output layers

Present five separate totals:

1. Employer-paid gross termination amounts
2. Estimated taxes and authorized deductions
3. Employer-paid estimated net amount
4. FGTS balance/penalty and accessibility
5. Immediately accessible conservative total

Then compute financial runway:

`runway_months = immediately_accessible_conservative_total / monthly_net_cost_of_living`

Keep a conservative view that excludes blocked FGTS, unapproved unemployment insurance, disputed amounts, and unguaranteed bonus/PLR.

## Minimum intake

Do not calculate real values until these are known or explicitly treated as assumptions:

- exact admission date;
- current gross salary and habitual variable remuneration;
- hypothetical termination/reference date;
- vacation periods acquired, taken, or overdue;
- 13th advances;
- FGTS current balance and termination base;
- saque-rescisão versus saque-aniversário and any advance loan;
- dependents and authorized deductions;
- applicable collective bargaining agreement.

For recurring monthly reports, derive the hypothetical termination date consistently (for example, the last day of each analyzed month) instead of asking the user for it every month.

## Employment-history normalization

When admission or role-change evidence contains multiple dates or pay figures, normalize the chronology before calculating:

1. Preserve the **originally communicated start date** as historical context.
2. Use the **formally amended/effective start date** for service time only when the evidence or user clearly says it superseded the earlier date.
3. Record the source date, subject/title, and evidence status separately; distinguish an original email/PDF from a user-provided consolidation or transcription.
4. Store **initial/proposed salary** separately from **current gross salary**. Never populate the current-salary input from an old offer or admission message.
5. Preserve admission role, current role, legal employer, client assignment, work mode, and internal department as distinct fields; leave the department unknown rather than inferring it from the client or job title.
6. If the current salary or vacation/FGTS facts remain unknown, update the historical record but keep the real termination calculation blocked.

A useful audit record includes: effective date, replaced date, change-confirmation date, source description, evidence status, admission role, initial salary, current salary, employer, client, and unresolved fields.

## Payroll evidence from email or document archives

Payslips can often resolve current gross salary, salary evolution, habitual variable pay, INSS/IRRF deductions, dependents, 13th advances, and recurring payroll deductions. They do **not** reliably replace FGTS statements, vacation history, or the applicable collective bargaining agreement.

When the user says payslips are in Gmail or another mailbox:

1. Save the mailbox/document source and the unresolved questionnaire before attempting access, so the task remains resumable.
2. Check authentication with the relevant email/Workspace skill before claiming access. Treat missing authorization as a setup state, not as evidence that the mailbox or tools are unavailable.
3. Do not configure credentials, request broad scopes, install account access, or search the mailbox unless the user explicitly chooses to proceed.
4. Prefer the narrowest access needed for locating and downloading payroll documents. Do not send, delete, move, label, or otherwise modify messages during evidence collection.
5. Search by employer/sender, terms such as `contracheque`, `holerite`, `demonstrativo de pagamento`, attachment type, and date range; preserve message date, sender, subject, attachment filename, and local archive path as provenance.
6. Process documents chronologically and distinguish observed payroll fields from inferred values. Never promote an admission offer or old payslip to `current gross salary` when a newer payslip may exist.
7. Record access state explicitly: source known, authorization pending, documents located, documents downloaded, or extraction verified.
8. After extraction, update the structured contract data and missing-data checklist, while leaving unrelated unresolved fields null.

## Non-salary benefits versus personal income

Keep two independent ledgers whenever the worker receives meal/flexible-benefit cards, allowances, reimbursements, benefit-platform credits, or cash deposits described as benefits:

1. **Employment-law remuneration:** amounts proven to compose salary or habitual variable remuneration and therefore potentially affecting notice, vacation, 13th salary, FGTS, and termination calculations.
2. **Personal disposable resources:** salary net cash plus benefits or credits actually available for living expenses in the relevant period.

Do not move a benefit from the second ledger into the first merely because it is regular or deposited in an account. Conversely, do not accept a non-salary label as a definitive legal classification without evidence. Record:

- provider and full bank/payroll description;
- payment date and competence;
- amount;
- one-time, monthly, annual, or unknown recurrence;
- cash-free versus category-restricted use;
- policy, collective agreement, benefit regulation, or reimbursement basis;
- whether it appears on the payslip and how it is taxed;
- evidence status: user statement, bank proof, benefit-platform statement, payroll record, or regulation.

Operational rules:

- If the user explicitly defines a benefit as excluded from termination for their planning model, preserve that as a stable scenario rule: keep it out of salary, notice, vacation, 13th salary, FGTS, penalty, and every termination total. Record the source as `user-confirmed planning treatment`. Do not repeatedly re-open or weaken that instruction with speculative legal caveats; mention any evidence limitation once, only when material, without changing the requested calculation.
- A benefit paid again when 13th salary is paid remains a separate non-salary resource unless the user or documentary evidence explicitly reclassifies it. Record the event linkage, amount, timing, and recurrence separately; never assume the extra benefit equals the ordinary benefit amount.
- Include a one-time or unconfirmed benefit only in the period actually received; never project it into future monthly income.
- Add a recurring benefit to ongoing disposable-income analysis only after recurrence is evidenced.
- Keep benefit totals visibly separate from gross salary and from the termination base.
- Do not add future employer-funded benefits to post-termination runway unless continuation after termination is proven.
- An already received, unused cash balance may be shown as a separate personal reserve, not as TRCT.
- If money is freely deposited and paid habitually without a documented benefit/reimbursement structure, flag possible employment-law and tax reclassification for professional review rather than deciding it silently.

A useful report has three rows: `salary/remuneration used for termination`, `non-salary resources received in the period`, and `combined disposable resources`. State explicitly whether the termination estimate changed.

## Automation pattern

- Store stable contract data in a JSON input file.
- Keep monthly/reference fields distinct from stable facts.
- Generate one report per month with a stable filename.
- If required data is missing, output a concise missing-data checklist and stop; never fill null fields with invented amounts.
- Revalidate INSS and IRRF tables when the year changes or official pages are updated.
- Test the deterministic calculator with synthetic fixtures before using personal data.
- Verify a complete-month salary-balance edge case in 31-day months; cap full-month salary balance at the monthly remuneration.

## Official sources to re-check

- CLT compiled: https://www.planalto.gov.br/ccivil_03/decreto-lei/del5452compilado.htm
- FGTS Law 8.036/1990: https://www.planalto.gov.br/ccivil_03/leis/l8036consol.htm
- Notice Law 12.506/2011: https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/lei/l12506.htm
- INSS contribution table: https://www.gov.br/inss/pt-br/direitos-e-deveres/inscricao-e-contribuicao/tabela-de-contribuicao-mensal
- Receita Federal annual tax tables: https://www.gov.br/receitafederal/pt-br/assuntos/meu-imposto-de-renda/tabelas/
- Formal unemployment insurance: https://www.gov.br/trabalho-e-emprego/pt-br/servicos/trabalhador/seguro-desemprego/seguro-desemprego-formal

## Final-report checklist

- [ ] Scenarios are separate and comparable
- [ ] Employer cash and FGTS are not conflated
- [ ] Non-salary benefits are separated from employment-law remuneration and post-termination runway
- [ ] Benefit date, recurrence, restrictions, payroll treatment, and evidence status are explicit when applicable
- [ ] Notice assumptions are explicit
- [ ] Vacation periods and dates are validated
- [ ] Current official tax tables are cited
- [ ] Immediate versus conditional access is explicit
- [ ] Financial runway is calculated from the user's stated net monthly cost
- [ ] Hypotheses, missing data, files changed, and next action are reported
