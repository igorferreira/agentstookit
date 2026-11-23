# Accent removal + orphan-label cleanup (session 2026-09-02, Gmail pt-BR)

Follow-up to the purge/reorg recipe. Two new durable techniques from the same account.

## 1. Remove accents from ALL labels (Igor requires accent-free label names)

Real case: 19 labels had diacritics (`@Pessoal/Finanças`, `@Pessoal/Segurança`,
`@Pessoal/Eleições`, `@Pessoal/Parabéns`, `Eleições/2022`, `Endereços`,
`@Dev/.../ImersãoFullStack&&FullCycle`, `Atualizações automáticas`, `Fóruns`, ...).

himalaya has NO rename/move-folder command (`himalaya folder rename` → "unrecognized subcommand").
To rename a label you must move its content to a new label:

1. `himalaya folder add "<accent-free-name>"` (e.g. `@Pessoal/Financas`)
2. list + move envelopes: `himalaya message move --folder "<old>" "<new>" <id>...`
3. verify old is empty: `himalaya envelope list --folder "<old>" --output json` → `[]`
4. `himalaya folder delete -y "<old>"  # -y is REQUIRED in non-TTY`

Detecting accents in Python:
```python
import unicodedata
def has_accent(s):
    return any(unicodedata.combining(c) for c in unicodedata.normalize('NFD', s))
def remove_accent(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c))
```

Pitfall observed: empty labels report "0 movidos" — that's fine (they're orphans, still get
deleted). A `folder delete` can transiently fail with `cannot build IMAP client ('c...')` right
after a crash under load — just re-run that single label. Confirm final state: `folder list`
should show 0 labels with combining chars.

Important Gmail behavior: deleting the old label name when a new label is created removes the
label (the message stays even if the label object was empty; never delete a label with mail in it).

## 2. Orphan (empty) label cleanup at scale

Big accounts accumulate hundreds of EMPTY labels (old setups). They're the label-bloat source
and are safe to delete once confirmed empty.

- Enumerate all labels under a group, then scan each with
  `himalaya envelope list --folder "<L>" --page-size 1000 --output json` and count `len(arr)`.
- This is **I/O-bound and slow** (one Gmail round-trip per label × 700+ labels ≈ 20-30+ min).
  Run it as a background terminal process writing a log, with `notify_on_complete=true`.
- **Sort labels by depth descending** (`x.count('/')`) so child labels are deleted before
  parents — a non-leaf label with remaining children fails to delete with a Gmail error.
- Only `folder delete -y` labels with 0 envelopes. If a delete reports an error, it usually
  means the label still has children (handled in a later pass) — not a data-loss condition.
- Verify at the end: re-list and confirm no empty labels remain under the scanned group.

## Consolidation-first strategy

Rather than scan everything up front, prefer: (a) create bucket labels, (b) move mail from
sparse/old labels into buckets, (c) the source labels that become empty ARE the orphans —
delete them. This folds "reorganize" and "orphan cleanup" into one pass and never deletes mail.