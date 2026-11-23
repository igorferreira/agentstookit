# Inbox cleanup — must-save check & classification refinements (session 03/09/2026)

Worked in a real purge pass over a Gmail INBOX (146 emails). Two rules proved essential and both
cost real back-and-forth when skipped.

## 1. Verify the user's cited "critical" email BEFORE deleting anything

The user named a specific contract/assignment notice (E-CPF / Proposta 578102 / Contrato 004505)
as the thing that MUST stay. It was NOT in the enumerated INBOX.

- Enumerate the whole account, not just INBOX:
  `himalaya envelope list --folder "[Gmail]/Todos os e-mails" --page-size 500 --page N` (paginate;
  each page caps at 500, so an INBOX of 146 had pages of All Mail to walk).
- A page that returns empty / JSON-parse-fails on page 2 means "no more data" — don't loop forever.
- **The email may also live in a different Gmail account than the one himalaya has configured.**
  `himalaya account list` showed only `gmail-igor` (igorferreirabr@gmail.com); the E-CPF email was
  not found there. Igor has a second account, `igorferreira08@gmail.com`, which himalaya does NOT
  cover. Do NOT conclude "email lost" — flag that it may be on the other account and ask the user
  before deleting promos.

## 2. Security alerts & payment receipts are PRESERVE, not promo

A keyword/domain classifier put these in the delete bucket; all must be hand-reclassified to preserve:
- Google: "critical security", "account recovered", "account deleted", "conclua a configuração"
- OpenAI / Anthropic: "New sign-in", "payment unsuccessful/unsuccessful"
- Instagram: "New login" (any device)
- Revolut: "confirm your data"
- Amazon: "security code", "[Action Required] Verify your account"
- GitHub: "Payment Receipt"
- Jusbrasil: process-alert emails (legal case handling → preserve)

Audit the would-delete list for security/2FA/payment context and move them to preserve before purge.

## Worked output shape (before approving a purge)
Show the user three buckets with counts: PRESERVAR (faturas/bolos/PIX/RH/gov/banco/segurança),
PROMO (newsletters + marketing), CONFIRMAÇÃO DE ENTREGA (deleteable). Then wait for explicit
"PODE APAGAR" before any destructive op.