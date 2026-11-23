---
name: email-attachment-archiver
description: "Watcher to auto-fetch invoices/PDFs from IMAP via Himalaya."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [email, imap, himalaya, attachments, archive, cron, invoices, faturas]
    related_skills: [himalaya, financeiro-comprovantes]
---

# Email Attachment Archiver

Reusable pattern for a **cron-style watcher** that scans an IMAP inbox for invoices/attachments (faturas, boletos, contas, PDFs), downloads them, and archives them to a filesystem with a canonical naming + dedup rule — without a human in the loop.

This captures the transferable Himalaya/JSON quirks learned while building a daily invoice watcher (2026-09-01). The user-specific finance workflow that consumes it lives in the `financeiro-comprovantes` skill (user-owned); this is the tooling-level class.

## Architecture

- **Cron job `no_agent=True`** that runs a script; empty stdout = silent; non-empty stdout = delivered as the message. Perfect for a "watchdog that reports only when new".
- **Dedup state**: keep a JSON list of already-processed message IDs (`~/.hermes/scripts/<name>-state.json`), capped (e.g. last 200).
- **Name canonical**: `DATA_FATURA-EMISSOR.{ext}` + a `<name>.md` sidecar with sender/subject/date/message-ID.

## Himalaya quirks (learned the hard way)

### 1. Parse envelopes with `--output json`
```bash
himalaya --output json envelope list --account NAME --page-size 60
```
→ returns a JSON array of `{id, from:{name,addr}, subject, date, has_attachment}`. Far more reliable than grepping the ASCII table. Note the `--output json` flag goes BEFORE `envelope list`.

### 2. `has_attachment` is NOT reliable
It returned `false` on an email that demonstrably had a PDF attachment. **Never branch on it.** Always attempt `attachment download` and inspect whether anything landed; treat "no file" as the true negative.

### 3. `attachment download` needs `--downloads-dir`
Without it, himalaya tries to write to the **attachment's original server path**, which doesn't exist locally → fails with `No such file or directory`. Always:
```bash
himalaya attachment download --account NAME --downloads-dir "$DEST" <MSG_ID>
```

> ⚠️ The community `himalaya` skill documents this as the `--dir` flag; on the tested build the working flag is `--downloads-dir`. Verify with `himalaya attachment download --help` on your version, but start from `--downloads-dir`.

### 4. Reusing the account from scripts
Scripts must pass `--account NAME` explicitly. Headless download works via the configured auth command (e.g. `secret-tool` / keyring) with no live session — verified working.

## Dedup rules (user requirement: never overwrite, never duplicate)

- Track processed message IDs in state JSON.
- Before saving, check whether the target folder already has a file with the same **emissor** in the name; if so, mark the ID processed and `continue` (skip) — do not re-save.
- Clean up any stray temp dir (`/tmp/<name>`) between runs so a prior extraction doesn't leak.

## Sender-matching pitfalls

- `from <term>` returns nothing for several providers (e.g. Light, Naturgy). Maintain a small mapping of real senders + subject tokens; broaden with generic lookup AND message-ID scan of recent envelopes when a provider is missing.
- Filter false positives: subjects containing "aviso de manutenção" (maintenance notice from a utility) or "problema com o pagamento" (payment-failure notice) are NOT invoices — exclude them. A "problema com o pagamento" notice still records a real charge for a service the user consumed; when the receipt class is spend tracking (not payment proof), keep the value but mark it as cobrança pendente instead of dropping it.

## Identifier-first sender discovery (user names the service in a voice message)

STT garbles brand names in Portuguese voice messages; resolve the real sender from the mailbox BEFORE asking the user to spell it:

1. Derive 2–4 phonetic candidates from what was heard and search mail directly by identifier: keyring-authenticated imaplib (`secret-tool lookup service hermes-gmail account <email>` with `DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus` exported), X-GM-RAW searches `from:<candidate>` and `subject:<service-keyword>` (estacionamento, fatura, boleto). Hit counts per candidate reveal the real sender in one round.
2. If subject/from searches all miss, profile the mailbox: fetch FROM headers in 200-id batches over all mail and keyword-filter the unique sender list. The real service shows up as a sender with dozens of messages; a same-keyword newsletter shows up with 1–2 and is eliminated by count.
3. Open 1–2 sample bodies and confirm the extracted fields before building any file, script, or cron.
4. Only then involve the user — ask them to CONFIRM the resolved name, not to identify the company from scratch.

Keep X-GM-RAW search terms ASCII-only: a non-ASCII token inside the search crashes imaplib with UnicodeEncodeError — search `patio`, not `pátio`, or pick another ASCII keyword from the subject.

## Deduping extracted receipts

Dedupe by the extracted data tuple (date + place + amount), not by message ID alone — the same comprovante can arrive twice seconds apart as separate e-mails, and ID-based dedup will double-count it. Before writing the register, assert the written row count equals the expected count from the parsed source list; a mismatch means a parsing or dedup bug, not fewer receipts.

## Manual test loop (no waiting for cron)

```bash
rm -f ~/.hermes/scripts/<name>-state.json   # to force reprocessing
python3 ~/.hermes/scripts/<name>.py
```
Empty output = nothing new. After scheduling, verify `last_status` on the cron job — an auth/keyring failure should surface as an error, not silence.

## Verification checklist

- [ ] A new invoice saves to the correct month folder with a stable canonical name.
- [ ] Re-running the script does NOT create a duplicate (dedupe works).
- [ ] The `.md` sidecar records sender, subject, date, and message ID.
- [ ] Author schema/flag (`--downloads-dir`) matches the installed himalaya version.