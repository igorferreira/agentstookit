# No-label audit sweep + multi-account access

Session-validated 2026-09-09 on the Igor Gmail (~100k emails).

## Sweep: emails with no label

Standing rule: every email must end inside some label. Detect strays:

```python
# over "[Gmail]/Todos os e-mails"
typ, data = M.search(None, "ALL")
sem_label = []
for u in data[0].split():
    typ, d = M.fetch(u, "(X-GM-LABELS)")
    if "X-GM-LABELS ()" in d[0].decode(errors="ignore"):
        sem_label.append(u)
```

- Light FETCH: ~10k emails/min with no sleep. Run as background process, print progress every 5k.
- Then group by sender (fetch `BODY.PEEK[HEADER.FIELDS (FROM SUBJECT)]`, regex `<([^>]+)>`),
  classify with the sender-dict + subject-keyword fallback from SKILL.md, apply labels in
  batches of 100-150, unknown senders → `AAA-Revisar`.
- End state: triage buckets (`Analisar`, `AAA-Revisar`) emptied → then `M.delete()` those labels.

## Adding another Gmail account

- Only accounts in himalaya config.toml (`[accounts.<name>]`) are directly usable.
- Check the keyring FIRST, before asking the user:
  `DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus secret-tool lookup service hermes-gmail account <other@gmail.com>`
  - Empty output = no stored password → ask the user for an **app password**
    (myaccount.google.com → Security → App passwords). Never hunt the environment for
    keys; never echo secret values back.
- Once stored, the same IMAP/batch method from SKILL.md works. Label rules are per-account.
- Corporate Microsoft 365 accounts may require admin/OAuth — flag, don't improvise.
