# Gmail Label Audit & Merge — Validated Playbook (igorferreirabr/igorferreira08)

Validated 09-10/09/2026 across ~100k emails, 2 accounts. All commands assume:
`export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus` (needed for secret-tool keyring).

## Core audit script (labels hierarchy)

```python
import imaplib, ssl, subprocess, re
from collections import defaultdict
pwd = subprocess.run(['secret-tool','lookup','service','hermes-gmail','account',EMAIL], capture_output=True, text=True).stdout.strip()
M = imaplib.IMAP4_SSL("imap.gmail.com", 993, ssl_context=ssl.create_default_context())
M.login(EMAIL, pwd)
typ, L = M.list()
labels = []
for x in L:
    s = x.decode()
    if '\\Noselect' in s: continue          # skip wrapper ghosts for root counting
    m = re.match(r'.*\) "(.*)" (.*)', s)
    if m: labels.append(m.group(2).strip('"'))
labels = sorted(set(labels))
# 1) duplicates: same leaf name under different paths
leaf_count = defaultdict(list)
for l in labels: leaf_count[l.split('/')[-1]].append(l)
dups = {k: v for k, v in leaf_count.items() if len(v) > 1}
# 2) missing parents: every prefix path must exist as a label
paths = set()
for l in labels:
    p = l.split('/')
    for i in range(1, len(p)+1): paths.add('/'.join(p[:i]))
missing = sorted(p for p in paths if p not in labels and p != '[Gmail]')
# 3) echo folders X/X
echo = [l for l in labels if len(l.split('/'))>=2 and l.split('/')[-1]==l.split('/')[-2]]
```

## Checking emails without labels

```python
M.select('"[Gmail]/Todos os e-mails"')   # MANDATORY: SEARCH fails in AUTH state
typ, d = M.search('utf-8', 'X-GM-RAW', '"has:nouserlabels"'.encode('utf-8'))
ids = [x.decode() for x in d[0].split()]
```

- **Pitfall:** `M.search(...)` raises "illegal in state AUTH" unless you `select` a mailbox first.
- **Pitfall:** Gmail IMAP has write-propagation lag. A just-moved email can still appear in `has:nouserlabels` for seconds/minutes. Verify with **3 attempts** (`store` then `sleep(5)` then re-search). Only accept 0 after a clean pass.

## Merging duplicates (absorb extra into canonical)

```python
typ, d = M.search('utf-8', 'X-GM-RAW', f'"label:\\"{extra}\\""'.encode('utf-8'))
ids = [x.decode() for x in d[0].split()]
for i in range(0, len(ids), 150):
    b = ",".join(ids[i:i+150])
    M.store(b, '+X-GM-LABELS', f'("{canonical}")')
    M.store(b, '-X-GM-LABELS', f'("{extra}")')
    time.sleep(0.2)
M.delete(f'"{extra}"')
```

- Batch size **150** for STORE (bigger hangs). Fetch headers in batches of **200**.
- On exception: `time.sleep(15)`, logout, reconnect, retry batch.
- Canonical choice rule: Financeiro paths for financial senders; Arquivados/Compras for retail; Estudos for education. Keep ONE path per leaf.

## Wrapper \Noselect ghost roots

`\Noselect` labels (e.g. "Compras") don't appear in Gmail UI but hold orphaned children ("Compras/99app", "Compras/Uber"). They show up as phantom "parent missing". Fix: migrate children (merge or create proper parent path), then delete wrapper. After children move, the wrapper disappears.

## Deletion rules (user-mandated)

- NEVER delete a label that has sublabels even if it holds 0 emails — empty parents support the tree; deleting creates orphans (caused a 16-missing-parent incident).
- Delete only when: no emails AND no sublabels (whole branch empty).
- Before ANY bulk delete: validate individually, show list, require human gate (Gmail label-wipe incident 02/09/2026 deleted 763 labels).

## Batch-rate pattern for mass relabeling

- Map senders first: `M.fetch(batch, "(BODY.PEEK[HEADER.FIELDS (FROM)])")` in lots of 200, accumulate `uid→sender` dict, save to /tmp JSON (crash-resumable).
- Apply per-sender with rules dict (substring match → target label), then catch-all pass for unknowns (Pessoal/Outros or AAA-Revisar while triage label exists).
- Subjects may be RFC2047-encoded (`=?UTF-8?Q?...?=`) — decode with `quopri.decodestring` before classifying by subject. Some legit senders (Light, NF-e, gov.br) have empty/masked FROM — classify by SUBJECT, not FROM.

## Final-state checklist (both accounts)

1. `has:nouserlabels` returns 0 (3-pass verification)
2. 0 duplicate leaves, 0 missing parents (excluding [Gmail]), 0 echo folders
3. Root count ≤ 17, no \Noselect wrappers with children
4. Every new label level got ≥1 email associated