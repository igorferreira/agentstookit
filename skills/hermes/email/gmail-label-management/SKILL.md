---
name: gmail-label-management
description: Use when reorganizing or bulk-managing Gmail labels by IMAP.
---

# Gmail Label Management (bulk, via IMAP)

Class-level skill for tasks of the shape: move hundreds/thousands of emails between Gmail labels, fix label hierarchies, deduplicate label trees, zero the INBOX, or audit which emails are missing labels. Validated on 2026-09-09 reorganizing 900+ labels and ~4.000 emails for Usuário.

## Choose the workflow by volume and user constraints

For large migrations, use **direct IMAP with Gmail extensions**, one connection and batch STORE; do not issue one Himalaya process per message. For a small inbox triage where messages need individual classification—or when the user explicitly requires Himalaya—use the careful single-message workflow below.

**Never treat a `message move` response as proof of state.** Himalaya may report success while a label remains empty, or return `System Error` after Gmail has already moved the message. After either response, re-list the current INBOX and destination; retry only if the message is still in INBOX and absent from the destination.

### Small inbox: classify and move safely with Himalaya

1. Snapshot the INBOX with `himalaya envelope list --folder INBOX --page 1 --page-size 100 --output json`. Record each message’s sender, subject, date, and `Seen` flag before reading bodies or moving anything.
2. Classify each message by its actual sender and full subject. Normalize whitespace (including non-breaking spaces) and case before matching; for recurring newsletters or repeated subjects, use sender plus exact date as well as subject.
3. Before each move, refresh the INBOX list and resolve the message again; IDs can change across folder operations. Move one message, then verify it is present exactly once in the destination and absent from INBOX before proceeding.
4. Preserve the original read state. Avoid `himalaya message read` unless necessary because it can mark mail as seen; if body inspection changes `Seen`, restore it with `himalaya flag add <id> seen --folder <folder>` or `himalaya flag remove <id> seen --folder <folder>`, using the ID freshly listed in that folder.
5. Keep destination listings bounded to a recent page for current mail; use a precise subject/sender/date query when possible. Dumping 1,000-message pages from many labels is needlessly slow and can time out.
6. After the batch, list INBOX again and verify it is empty (or report every message that remains and why). Do not delete mail as a substitute for labeling.

### Large migration: direct IMAP batch STORE

```python
import imaplib, ssl
M = imaplib.IMAP4_SSL("imap.gmail.com", 993, ssl_context=ssl.create_default_context())
M.login(email, pwd)
M.select('[Gmail]/Todos os e-mails')
typ, data = M.search(None, "X-GM-RAW", "from:noorden.com.br")
ids = data[0].split()
for i in range(0, len(ids), 150):
    b = b",".join(x for x in ids[i:i+150])
    M.store(b, '+X-GM-LABELS', '("Clientes/[EMPRESA]/Correspondencia")')
    M.store(b, '-X-GM-LABELS', '("OldLabel")')   # optional removal
    time.sleep(0.15)
M.expunge()
```

- Batch 150-500 UIDs per STORE; >300 req/min can abort the connection (`System Error`/`socket error: EOF`) → catch, reconnect, continue (see pitfalls).
- To archive out of INBOX do NOT try `-X-GM-LABELS '(\\Inbox)'` — see pitfalls.

## Password access

Keyring via `secret-tool lookup service hermes-gmail account <email>` requires
`DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus` (persist in `.bashrc`).

## OPTIMIZED sweep method (validated 09/09, replaces fetch-1-by-1 for huge accounts)

The old sweep (search ALL + fetch X-GM-LABELS one-by-one) takes 40+ min on 100k accounts and Gmail kills long sessions. Use the NATIVE search instead:

```python
# THE FAST WAY — one command, finds ALL unlabeled emails:
typ, d = M.search(None, 'X-GM-RAW', 'has:nouserlabels')
ids = [x.decode() for x in d[0].split()]
```

- `has:nouserlabels` = Gmail's own operator for "no user labels". Instant, complete, no pagination drift.
- Read senders in BATCHES of 200: `M.fetch(",".join(lote), "(BODY.PEEK[HEADER.FIELDS (FROM)])")` — one command per 200 emails (100x faster than 1-by-1).
- Save progress to `/tmp/grupos.json` every batch (json.dump) so kills/reconnects lose nothing.
- Apply labels in batches of 150 per STORE; unknown senders → `AAA-Revisar`.
- **Double verification at the end:** `X-GM-RAW "has:nouserlabels"` must return 0 on every account. That is the mathematical proof no email is unlabeled.
- Onda strategy for 280-email triage buckets: wave 1 sender-dict (40-60 rules), wave 2 remaining senders dict, wave 3 subject/manual review, wave 4 catch-all (`Pessoal/Outros` or `AAA-Revisar`) → delete the bucket label.
- Kill the slow 1-by-1 sweep if it's still running before starting the optimized one (two IMAP writers = label races).

## Usuário's standing label rules (follow without asking)

1. Root labels max **17**.
2. Every label needs ≥1 email. For sublabels: associate an email to EVERY level (root, mid, leaf). One email may serve all levels of the same branch.
3. **NEVER delete a label that has sublabels, even if it has 0 direct emails** (Usuário's rule, 10/09/2026). An empty parent with children sustains the tree — deleting it orphans the children (this caused the 16 missing-parents incident). Only delete a label when it has NO emails AND NO sublabels (whole branch empty). This supersedes the old "empty = deletable" rule for parents.
4. Break hyphens in leaf names into directories: `Carros-Fiat-Punto-ELX` → `Carros/Fiat/Punto/ELX` (ALL hyphens, user-confirmed even when deepening paths like `Carros/Fiat/Punto/ELX/[PLACA-REDACTADA]`).
5. No duplicates; same-named labels in different parents (`Compras`) resolved by full-path hierarchy.
6. Label names without accents.
7. Every email must end inside some label; INBOX ends at 0.

## Canonical root structure (2026-09)

`AAA-Revisar` (triage, prefix keeps it on top), Agendas, Alertas, Arquivados, Carreira, Clientes, Dev, Financeiro, IA, Pessoal, Legal... Companies under `Clientes/<Empresa>/[Contracheques|ControleHoras|Comunicados|Correspondencia]`; money under `Financeiro/{Contas,Cartoes,Contas_Casa,Cobrancas}`; notas fiscais under `Arquivados/Compras/Financeiro_Docs/NotaFiscal[/Emissor]` (unified `NotaFiscal`, broken by issuer: MercadoLivre 122, Prefeitura 97, NFe 27, Vultr 14...).

`AAA-Revisar` = fallback bucket for unmatched senders.

## Classification pattern (bulk triage)

1. Fetch `BODY.PEEK[HEADER.FIELDS (FROM SUBJECT)]` per email, regex `<([^>]+)>` for sender.
2. Map by sender-domain substring → destination label (dict). 40-60 rules cover the tail.
3. Subject-keyword fallback (e.g. `cupom|promo|desconto|black friday` → cupons label).
4. Bulk-apply per destination in batches; leftovers → `AAA-Revisar`.
5. On shared corporate domains (vivo.com.br had old work emails), require finance keywords in subject before labeling.

## Pitfalls (all hit and validated this session)

- **`-X-GM-LABELS '(\\Inbox)'` does NOT remove the Inbox label** — it can even WRITE a literal `"\Inbox"` string label. Removal is inconsistent; safest is a big STORE batch on All Mail, then verify with `X-GM-RAW "label:inbox"`. NEVER trust the STORE OK reply alone.
- **`X-GM-RAW` syntax**: plain queries work (`from:bank.com`); parentheses and `-in:` are rejected (`Could not parse command`). Exclusion = client-side (fetch X-GM-LABELS per email and filter).
- **Gmail IMAP caches label renames**: after migrating emails off a label, `LIST`/`SELECT` on the old label show stale counts for minutes. Ground truth = `X-GM-RAW "label:<path>"` on All Mail.
- **Names with `&`** (C&A, Casa&Video) break `STORE` label args → `BAD Could not parse command`. Handle separately/escaped.
- **Rate limits**: large select+store loops trigger `System Error`/EOF aborts. Pattern: per-item retry (3x) with full reconnect, `time.sleep` between batches, run as background process and poll with `process log`.
- **Gmail folders are labels**: `SELECT` a label path like `"Financeiro/Contas/Nubank/Comprovantes"` works like a folder; `M.delete()` removes the label, not emails (they stay in All Mail).
- **`\Noselect` wrappers** (parent labels with no direct emails) are harmless residue — `M.delete` returns NO; they don't render in the Gmail UI. Leave them.
- **Huge volumes**: 1.000+ email migrations take 10+ min with sleeps. Always `background=true` + `notify_on_complete=true`, report progress.
- **Deleted labels ghost in LIST**: keep appearing until Gmail purges; verify twice with sleep, don't double-delete.
- **`message delete` in `[Gmail]/Lixeira` does not purge** (Gmail Trash is IMAP read-only; auto-purges in 30 days).
- **STORE label arg form (validated 11/2026, t_83bb0253): use PLAIN paren form** `M.uid('STORE', b, '+X-GM-LABELS', '(Path/Label)')` — clean labels with slashes/spaces. The quoted form `'("Path/Label")'` CREATES JUNK labels literally named `(Path/Label)` (with parens in the name) instead of applying the intended label. Junk labels resist `-X-GM-LABELS` removal; delete them with `M.select('"((Name))"')` + `M.delete()` (removes the label, messages stay in All Mail).
- **You cannot remove the label of the mailbox you are currently SELECTed in**: `-X-GM-LABELS '(Parent)'` while SELECTed in `Parent` replies OK and silently does NOTHING. Always run parent-label removals from `[Gmail]/Todos os e-mails` (need the All-Mail UID of each message, not the source-mailbox UID).
- **Batch `-X-GM-LABELS` STORE (comma-joined 100 UIDs) propagates late (up to ~15 min)** and per-message checks right after show the label still present — it does land; re-verify after a sleep. Single-UID STORE minus is immediate and reliable.
- **Batch FETCH responses may come back as plain `bytes`, not tuples** (varies by session/response). Handle both: UID is in item[0] prefix (`b'4280 (X-GM-LABELS (...) UID n)'`), body in item[1]; regex the whole line for `X-GM-LABELS \((.*?)\)(?: UID| FLAGS|$)` — the terminator alternates between FLAGS and UID.
- **FETCH inside a label-mailbox HIDES that label from X-GM-LABELS output** — a message still carrying the selected label may appear "without" it. Full label truth only from All Mail.
- **Gmail rate-limits rapid fetch/STORE loops with `socket error: EOF` / `[ALERT]`**: reconnect + sleep 3-4s per retry; keep batches ≤300 and sleep 0.3-0.5s between commands.

## Verification checklist (end of any label op)

1. Root count ≤ 17.
2. No missing parents (every /-prefix of every label exists).
3. No exact duplicates; no eco labels (`X/X`).
4. Every leaf label ≥1 email; parents with sublabels are KEPT even if empty (rule 3). Whole branch with 0 emails → delete.
5. INBOX = 0 via `X-GM-RAW label:inbox`.
6. "importante"/star markers removed if asked: `X-GM-RAW X:important` → batch `-X-GM-LABELS`.