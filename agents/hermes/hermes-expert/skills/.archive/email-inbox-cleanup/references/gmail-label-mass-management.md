# Gmail Label Mass-Management via Raw IMAP (validated 2026-09-09)

Battle-tested recipe for mass-labeling, reorganizing, and deduplicating Gmail
labels. Executed successfully on a real mailbox (~907 labels, ~2.500 emails
moved in one session). Complements the SKILL.md label section: use **this raw
IMAP technique whenever himalaya's copy/move is too slow or silently fails**.

## The core pitfall: himalaya copy/move SILENTLY fails on newly created Gmail labels

`himalaya message copy/move <new-label> <id>` reports **"successfully copied"**
but the email never appears under the new label — even minutes later. Happens
specifically with labels created via `himalaya folder create` in the same
session. IMAP APPEND to a freshly-created Gmail label is not honored.

**Fix: bypass himalaya for label writes. Use raw IMAP with `X-GM-LABELS`.**

## Technique 1: keyring password retrieval (DBUS is the trap)

```bash
# CRITICAL: gnome-keyring needs the USER's session DBUS bus, not a fresh one
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus
secret-tool lookup service hermes-gmail account user@gmail.com
```

Without this exact address (pointing at the user's real session bus),
`secret-tool` returns nothing; `dbus-launch` starts a NEW empty keyring with
no passwords. Persist the export in `.bashrc` once.

## Technique 2: batch STORE X-GM-LABELS (one connection, 500/batch)

```python
import imaplib, ssl, time
pwd = open('/tmp/.gpw').read().strip()
M = imaplib.IMAP4_SSL("imap.gmail.com", 993, ssl_context=ssl.create_default_context())
M.login("user@gmail.com", pwd)
M.select('"[Gmail]/Todos os e-mails"')   # locale-dependent! discover via M.list()

def batch_label(query, label, batch=500):
    typ, data = M.search(None, f'X-GM-RAW "{query}"')
    ids = data[0].split()
    for i in range(0, len(ids), batch):
        b = b",".join(x for x in ids[i:i+batch])   # message-set "1,2,3" in ONE store
        typ, d = M.store(b, '+X-GM-LABELS', f'("{label}")')
        time.sleep(0.3)
    return len(ids)

batch_label('from:camila subject:"Contra Cheque"', 'Clientes/Noorden/Contracheques')
batch_label('X-GM-RAW "from:mjv -label:Clientes/MJV"', 'Clientes/MJV')  # idempotent
```

- Batches of 500 in a single STORE work — vastly faster than per-email himalaya.
- `X-GM-RAW` accepts Gmail web search syntax incl. `-label:...` exclusions →
  re-runs are idempotent (only unprocessed emails match).
- Remove label: same with `-X-GM-LABELS`. Archive: `-X-GM-LABELS (\Inbox)`.
- Strip "important" everywhere: search `is:important` then `-X-GM-LABELS (\Important)`
  (removed 1.054 in one pass this way).
- **Check before each STORE batch**: `M.fetch(one_id, '(X-GM-LABELS)')` shows the
  exact label tuple — confirm the store syntax took effect before bulk-running.

## Technique 3: migrate a duplicated hierarchy (eco labels)

Example: `Arquivados/Compras/China/China/China-AliExpress` → `.../China/China-AliExpress`.

```python
for antigo, novo in movimentos:
    # find affected emails GLOBALLY (folder SELECT counts are cached/stale)
    typ, data = M.search(None, f'X-GM-RAW "label:{antigo}"')
    ids = data[0].split()
    for i in range(0, len(ids), 100):
        b = b",".join(x for x in ids[i:i+100])
        M.store(b, '+X-GM-LABELS', f'("{novo}")')
        M.store(b, '-X-GM-LABELS', f'("{antigo}")')
        time.sleep(0.2)
```

## Gmail quirks observed (don't rediscover these)

- **Gmail does NOT propagate parent labels to children.** `label:A/B` does not
  match `A/B/C`. Enumerate a subtree by searching each leaf individually.
- **Stale folder counts after relabel**: `SELECT`ing the old label still reports
  the old count for minutes. Ground truth = global `X-GM-RAW label:` search in
  All Mail. Don't re-run migrations because of this.
- **`\Noselect` wrappers**: after emptying a duplicated node, DELETE returns
  `[NONEXISTENT]` and the node stays listed as `(\\HasChildren \\Noselect)`.
  Harmless — invisible in the Gmail web UI. Don't fight it.
- **Locale folders**: PT-BR Gmail = `[Gmail]/Todos os e-mails` (All Mail),
  `[Gmail]/Lixeira` (Trash). Discover with `M.list('""','*')`; never hardcode
  English names.
- **Trash purge via IMAP doesn't stick** (message delete reports success, count
  unchanged). Trash self-purges in 30 days; don't loop on it.
- **Rate limiting**: rapid bulk STORE triggers `IMAP4.abort: System Error` /
  `socket error: EOF`. Pattern: catch → sleep 5-10s → reconnect → retry same
  batch (idempotent via `-label:` exclusions). Long migrations: background
  process with flushed progress prints.
- **Envelope IDs are per-folder UIDs**; re-list before every new operation.
- **Root-label budget**: keep ≤17 root labels (user's rule); `AAA-` prefix pins
  a label to the top of the alphabetical list.
- **Sublabel creation rule (user's convention)**: when creating `A/B/C`, attach
  one email to `A`, `A/B`, and `A/B/C` so every level renders as a directory.

## Hierarchy audit playbook

1. `M.list('""','*')` → inventory → verify every `A/B/C` has parents `A`, `A/B`.
2. Detect eco/dup names (`X/X` or same leaf under different parents); pick the
   right parent by full-path semantics (e.g. `Compras` material goods →
   `Arquivados/Compras`, NOT `Financeiro/Compras`).
3. Migrate with Technique 3; verify globally; expect `\Noselect` residue.
4. Associate ≥1 email to every intermediate level (Technique: take one email
   from any child leaf, `+X-GM-LABELS` with each parent name).
5. Final verify with fresh `M.list` + global searches; report labels fixed /
   created / unresolvable (e.g. system folders like `[Gmail]/Importante`).
