# Gmail Label Audit & Merge — Validated Playbook (igorferreirabr/igorferreira08)

Validated 09-11/09/2026 across ~100k emails, 2 accounts. All commands assume:
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
- **Duplicates REAPPEAR between sessions** (audit 1: 41 dups; audit 2 next day: 5 — Amazon/Condominio/Hotmart/PayPal/Compras). Re-run this audit after any big reorg.
- **Echo side-effect of merges:** a big merge can leave 1-3k emails unlabeled (`has:nouserlabels` > 0). Reclassify them (sender rules + catch-all `Pessoal/Outros`), then verify to 0 twice with sleeps — Gmail IMAP cache refills 1-2 stragglers after each batch.

## Wrapper \Noselect ghost roots

`\Noselect` labels (e.g. "Compras") don't appear in Gmail UI but CAN hold real children with real emails ("Compras/99app" 2.307, "Compras/Uber" 942 — validated 10/09). They show up as phantom "parent missing" in audits. Fix: migrate children (merge or create proper parent path), then delete the child labels. After children move, the wrapper disappears on its own. Audit for children stuck under wrappers, not just missing parents.

## Deletion rules (user-mandated)

- NEVER delete a label that has sublabels even if it holds 0 emails — empty parents support the tree; deleting creates orphans (caused a 16-missing-parent incident).
- Delete only when: no emails AND no sublabels (whole branch empty).
- Before ANY bulk delete: validate individually, show list, require human gate (Gmail label-wipe incident 02/09/2026 deleted 763 labels).

## Debt-collection label tree (Igor, 11/09/2026)

All debt-collection emails live under `Financeiro/Cobrancas_Dividas/<Credor>`:
Asaas, Serasa, SPC, Creditas, Quod, RecargaPay, Itau, Inter, PAN, Digio, CasasBahia, Carrefour + `/Geral` for subject matches (`cobranc|divid|inadimpl|negativad`). Routing new collection senders there is mandatory — Igor uses this tree for negotiations with lawyers. Validated: 2.062 emails labeled in one pass (RecargaPay 1.169, Inter 748, Asaas 70, Serasa 35...).

## Price-watch history naming (related convention)

Price-watch history files: `HISTORICO-<CATEGORIA>-<PRODUTO>.md` under `~/MEGA/Documentos/desejos_precos/` (e.g. `HISTORICO-CELULAR-MOTO-G86.md`, `HISTORICO-BONUS-MILHAS.md`). Igor renamed flat `HISTORICO-MOTO-G86` → category-prefixed on 11/09 — new price watchers must follow this naming.

## Batch-rate pattern for mass relabeling

- Map senders first: `M.fetch(batch, "(BODY.PEEK[HEADER.FIELDS (FROM)])")` in lots of 200, accumulate `uid→sender` dict, save to /tmp JSON (crash-resumable).
- Apply per-sender with rules dict (substring match → target label), then catch-all pass for unknowns (Pessoal/Outros or AAA-Revisar while triage label exists).
- Subjects may be RFC2047-encoded (`=?UTF-8?Q?...?=`) — decode with `quopri.decodestring` before classifying by subject. Some legit senders (Light, NF-e, gov.br) have empty/masked FROM — classify by SUBJECT, not FROM.

## Final-state checklist (both accounts)

1. `has:nouserlabels` returns 0 (3-pass verification)
2. 0 duplicate leaves, 0 missing parents (excluding [Gmail]), 0 echo folders
3. Root count ≤ 17, no \Noselect wrappers with children
4. Every new label level got ≥1 email associated