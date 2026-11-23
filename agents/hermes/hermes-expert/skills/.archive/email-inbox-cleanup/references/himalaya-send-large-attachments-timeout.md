# himalaya message send — large multi-attachment sends time out SMTP

Real event (2026-09-02): sending an email to a lawyer with **15 PDF attachments / ~7 MB**
via `himalaya message send --account gmail-igor` FAILED with
`cannot send message: request timed out`, after the Gmail SMTP ACKed several parts
with `250 OK` (the payload was streaming up in pieces, then the send window died).

## Why
`himalaya message send` takes raw MIME via stdin and uploads synchronously over the one
SMTP connection. A big payload (~7 MB, many parts) exceeds the effective timeout before the
final `DATA` completes → the connection drops and himalaya reports `request timed out`.

## Fix (reliably validated)
1. **Split into smaller emails.** Group the PDFs into chunks of ~5 attachments each
   (or keep total well under ~3–4 MB). one email per chunk。 This is the dependable fix and matches
   how the Gmail web/Jira-style mailers behave.
2. **Run the send in background** with `notify_on_complete=true` and a log file
   (`himalaya message send --account <acct> < /tmp/raw.eml > /tmp/send.out 2>&1`) so a
   multi-minute upload isn't killed by a foreground tool timeout. Combined with smaller
   payloads this is belt-and-suspenders.

## Build-ahead
- Assemble the full MIME email (email.mime.multipart MIMEMultipart + MIMEApplication per
  PDF) into `/tmp/raw_N.eml` first, verify the envelope (`From/To/Subject`, `len(attachments)`)
  from the on-disk bytes, then send each chunk. Do NOT sprint repeat-send the giant blob —
  it will keep dyinguntil split smaller.


## General rule for this class of task
Sending documents outward (lawyers, Procuradoria, third-party helpers) is common after
a cleanup/case-file job. Prefer document packets as a **small set of purpose-built PDFs**
rather than forwarding dozens of source files in one email.