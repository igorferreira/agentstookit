---
name: himalaya
description: "Himalaya CLI: IMAP/SMTP email from terminal."
version: 1.1.0
author: community
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Email, IMAP, SMTP, CLI, Communication]
    homepage: https://github.com/pimalaya/himalaya
prerequisites:
  commands: [himalaya]
---

# Himalaya Email CLI

Himalaya is a CLI email client that lets you manage emails from the terminal using IMAP, SMTP, Notmuch, or Sendmail backends.

This skill is separate from the Hermes Email gateway adapter. The gateway
adapter lets people email the agent and uses Hermes' built-in IMAP/SMTP
adapter; this skill lets the agent operate a mailbox from terminal tools and
requires the external `himalaya` CLI.

## References

- `references/configuration.md` (config file setup + IMAP/SMTP authentication)
- `references/message-composition.md` (MML syntax for composing emails)
- `references/smtp-attachment-fallback.md` (Python SMTP fallback when MML attachments fail)
- `references/google-calendar-invites.md` (finding calendar invite e-mails, RSVP link anatomy, accepting them)

## Prerequisites

1. Himalaya CLI installed (`himalaya --version` to verify)
2. A configuration file at `~/.config/himalaya/config.toml`
3. IMAP/SMTP credentials configured (password stored securely)

### Installation

```bash
# Pre-built binary (Linux/macOS — recommended)
curl -sSL https://raw.githubusercontent.com/pimalaya/himalaya/master/install.sh | PREFIX=~/.local sh

# macOS via Homebrew
brew install himalaya

# Or via cargo (any platform with Rust)
cargo install himalaya --locked
```

## Configuration Setup

Run the interactive wizard to set up an account:

```bash
himalaya account configure
```

Or create `~/.config/himalaya/config.toml` manually:

```toml
[accounts.personal]
email = "you@example.com"
display-name = "Your Name"
default = true

backend.type = "imap"
backend.host = "imap.example.com"
backend.port = 993
backend.encryption.type = "tls"
backend.login = "you@example.com"
backend.auth.type = "password"
backend.auth.cmd = "pass show email/imap"  # or use keyring

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.example.com"
message.send.backend.port = 587
message.send.backend.encryption.type = "start-tls"
message.send.backend.login = "you@example.com"
message.send.backend.auth.type = "password"
message.send.backend.auth.cmd = "pass show email/smtp"

# Folder aliases (himalaya v1.2.0+ syntax). Required whenever the
# server's folder names don't match himalaya's canonical names
# (inbox/sent/drafts/trash). Gmail is the common case — see
# `references/configuration.md` for the `[Gmail]/Sent Mail` mapping.
folder.aliases.inbox = "INBOX"
folder.aliases.sent = "Sent"
folder.aliases.drafts = "Drafts"
folder.aliases.trash = "Trash"
```

> **Heads up on the alias syntax.** Pre-v1.2.0 docs used a
> `[accounts.NAME.folder.alias]` sub-section (singular `alias`).
> v1.2.0 silently ignores that form — TOML parses fine, but the
> alias resolver never reads it, so every lookup falls through to
> the canonical name. On Gmail this means save-to-Sent fails *after*
> SMTP delivery succeeds, and `himalaya message send` exits non-zero.
> Any caller (agent, script, user) that retries on that exit code
> will re-run the entire send — including SMTP — producing duplicate
> emails to recipients. Always use `folder.aliases.X` (plural, dotted
> keys, directly under `[accounts.NAME]`).

## Hermes Integration Notes

- **Standing preference (Igor, Telegram):** when he asks to check, organize, move, or reply to e-mail on this machine, do it through himalaya — do not reach for browser/CDP or ad-hoc IMAP-python sessions unless himalaya genuinely cannot do the step (e.g. parsing HTML parts for RSVP links, bulk folder creation). He corrected an invite-acceptance flow mid-task toward himalaya; default to it first.
- **Reading, listing, searching, moving, deleting** all work directly through the terminal tool
- **Composing/replying/forwarding** — piped input (`cat << EOF | himalaya template send`) is recommended for reliability. Interactive `$EDITOR` mode works with `pty=true` + background + process tool, but requires knowing the editor and its commands
- Use `--output json` for structured output that's easier to parse programmatically
- The `himalaya account configure` wizard requires interactive input — use PTY mode: `terminal(command="himalaya account configure", pty=true)`

## Common Operations

### List Folders

```bash
himalaya folder list
```

### List Emails

List emails in INBOX (default):

```bash
himalaya envelope list
```

List emails in a specific folder:

```bash
himalaya envelope list --folder "Sent"
```

List with pagination:

```bash
himalaya envelope list --page 1 --page-size 20
```

### Search Emails

```bash
himalaya envelope list from john@example.com subject meeting
```

### Read an Email

Read email by ID (shows plain text):

```bash
himalaya message read 42
```

Export raw MIME:

```bash
himalaya message export 42 --full
```

### Reply to an Email

To reply non-interactively from Hermes, read the original message, compose a reply, and pipe it:

```bash
# Get the reply template, edit it, and send
himalaya template reply 42 | sed 's/^$/\nYour reply text here\n/' | himalaya template send
```

Or build the reply manually:

```bash
cat << 'EOF' | himalaya template send
From: you@example.com
To: sender@example.com
Subject: Re: Original Subject
In-Reply-To: <original-message-id>

Your reply here.
EOF
```

Reply-all (interactive — needs $EDITOR, use template approach above instead):

```bash
himalaya message reply 42 --all
```

### Forward an Email

```bash
# Get forward template and pipe with modifications
himalaya template forward 42 | sed 's/^To:.*/To: newrecipient@example.com/' | himalaya template send
```

### Write a New Email

**Non-interactive (use this from Hermes)** — pipe the message via stdin:

```bash
cat << 'EOF' | himalaya template send
From: you@example.com
To: recipient@example.com
Subject: Test Message

Hello from Himalaya!
EOF
```

Or with headers flag:

```bash
himalaya message write -H "To:recipient@example.com" -H "Subject:Test" "Message body here"
```

Note: `himalaya message write` without piped input opens `$EDITOR`. This works with `pty=true` + background mode, but piping is simpler and more reliable.

### Move/Copy Emails

Move to folder (target BEFORE IDs):

```bash
himalaya message move "Archive" 42
# Multiple IDs in one call:
himalaya message move "Archive" 42 43 44 45
```

Copy to folder:

```bash
himalaya message copy "Important" 42
```

### Delete an Email

```bash
himalaya message delete 42
```

### Manage Flags

Add flag:

```bash
himalaya flag add 42 --flag seen
```

Remove flag:

```bash
himalaya flag remove 42 --flag seen
```

## Multiple Accounts

List accounts:

```bash
himalaya account list
```

Use a specific account (global flags go AFTER the subcommand on this binary):

```bash
himalaya envelope list --account work
```

`-a/--account` takes the account NAME key from `config.toml`, never the e-mail address — passing the address itself (e.g. `-a you@example.com`) fails with `cannot find configuration for account ...` even though that is the address the account points at. Run `himalaya account list` to get the exact name.

## Attachments

Save attachments from a message:

```bash
himalaya attachment download 42
```

Save to specific directory:

```bash
himalaya attachment download 42 --dir ~/Downloads
```

## Output Formats

Most commands support `--output` for structured output:

```bash
himalaya envelope list --output json
himalaya envelope list --output plain
```

## Debugging

Enable debug logging:

```bash
RUST_LOG=debug himalaya envelope list
```

Full trace with backtrace:

```bash
RUST_LOG=trace RUST_BACKTRACE=1 himalaya envelope list
```

## Tips

- Use `himalaya --help` or `himalaya <command> --help` for detailed usage.
- Message IDs are relative to the current folder; re-list after folder changes.
- For composing rich emails with attachments, use MML syntax (see `references/message-composition.md`).
- Store passwords securely using `pass`, system keyring, or a command that outputs the password.

## Pitfalls

### Gmail special-folder names vary by locale

Never assume Gmail special folders use English labels. Run `himalaya folder list --account <account> --output json` and use the exact returned folder name; identify all-mail and sent folders by their IMAP attributes, not guessed labels. On Portuguese Gmail, all mail can appear as `[Gmail]/Todos os e-mails` (not `All Mail`) and sent as `[Gmail]/E-mails enviados` (not `[Gmail]/Sent Mail`). The `\Sent` attribute on a folder is the canonical signal; inspect with `himalaya folder list --output json` and grep for `Sent` to find its actual name.

If an assumed folder name is wrong, a search can fail with an unknown-mailbox error or miss archived messages when it targets only the inbox. If the sent alias is wrong, Himalaya may deliver via SMTP and then fail while saving the copy; verify the locale-specific folder name before sending.

### `message send` receives the RAW MESSAGE, never a file path

`himalaya message send < email.eml` (stdin redirect) works; `himalaya message send /path/to/email.eml` does NOT read the file — himalaya treats the path string as the message content and crashes with a mail-parser panic (`index out of bounds: the len is 0 but the index is 0`). Always redirect the .eml via stdin.

### Attachments require MML multipart/mixed

There is no `--attach` flag. Embed attachments directly in the template body using `<#part filename=/absolute/path/to/file.pdf name=nice-name.pdf><#/part>` inside a `<#multipart type=mixed>` block. See `references/message-composition.md` for the full syntax.

**Validated alternative — hand-built raw MIME:** pipe a complete .eml (headers + `multipart/mixed` with text/plain part + `application/pdf` part with `Content-Transfer-Encoding: base64` from `base64 -w0`) straight into `himalaya message send < email.eml`. This bypasses MML parsing entirely and works first-try; use it when MML attachment parsing fails or for programmatic sends. Always close the boundary with `--BOUND--` and send the PDF with `name=` + `Content-Disposition: attachment`.

**⚠️ Fallback:** If MML attachment sending fails (parse error), use Python SMTP directly with `secret-tool` for authentication. See `references/smtp-attachment-fallback.md`.

### Verify delivery before reporting success

`message send` returning "Message successfully sent!" confirms SMTP only. Before telling the user the e-mail arrived, run `himalaya envelope list` on the recipient INBOX and match subject + message ID; if the list is empty, wait a few seconds and re-list — SMTP delivers before the IMAP index refreshes.

When the send carries attachments, also confirm the copy that landed in the Sent folder: `himalaya attachment download -f <sent-folder> -d <dir> <id>` re-downloads the attachments, and comparing the sizes against the originals catches a malformed MIME part that SMTP accepted but that arrives stripped.

When the user says "me envia" without naming a recipient, use the user's own address as both From and To.

### Bulk INBOX triage: classify, group by folder, one move per folder
For "organize my inbox" tasks: (1) page the whole INBOX as JSON (`--page-size 50 --page N` in a loop until a page returns nothing); (2) classify in Python by sender domain + subject substrings — keep a small KEEP list for what stays (human senders, urgent-flagged subjects, CI failures, recurring digests the user reads daily); (3) before executing, grep `himalaya folder list` for each target folder and map to folders that ALREADY exist — this mailbox has 600+ folders, so an existing `Financeiro/Contas/99Pay` usually beats inventing `Financeiro/Contas/Pix_99Pay`, and moving into a non-existent path fails mid-batch; (4) execute one `message move "<folder>" <id...>` per folder with ALL its IDs, re-listing fresh only if a batch errors. Report back as a short table: what stayed in INBOX (each with why) and per-folder move counts.

### Raw sends: template parser can fail — keep raw .eml headers ASCII
Two independent failure modes on the send path of this build:

1. `himalaya template send` / `template save` abort with `cannot parse template` even for a template that `himalaya template write` / `template reply` just generated — the MML parser fails regardless of file content. Don't debug the MML; bypass it with a raw .eml piped to `message send` (reply-header recipe in the threading pitfall above; the same .eml works without reply headers for new mail).
2. A raw .eml piped via stdin must have ASCII-only headers or parsing breaks silently: use the bare address in `To:` (a UTF-8 display name like `Fábio <fabio@x.com>` makes the recipient resolve as empty → `cannot send message without a recipient`), and RFC2047-encode non-ASCII subjects (`Header(subject, 'utf-8').encode()`). UTF-8 in the BODY is fine with `Content-Transfer-Encoding: 8bit`. Passing a file PATH as the `[MESSAGE]` argument instead of stdin causes a mail-parser panic (`index out of bounds`) — always redirect via `< file`.

### Move command: target before IDs, never after

`himalaya message move <TARGET> <ID...>` — the destination folder comes BEFORE the message ID(s). Reversing the order (`himalaya message move 42 "Archive"`) produces an error. This applies identically to `message copy`. Always verify syntax with `himalaya message move --help` if unsure.

### Create folders before moving into them

`himalaya` does NOT auto-create parent folders. Attempting to move into `"Arquivados/Dev/Cursos"` when that path doesn't exist results in an error. Pre-create with `himalaya folder create "Arquivados/Dev/Cursos"` first. To check if a path exists, run `himalaya folder list | grep "<path>"` before attempting the move.

### IMAP message IDs shift between reads

IMAP UID numbers can change between calls due to concurrent mail delivery or folder mutations. When building a batch of moves from an `envelope list`, do one fresh `envelope list` call immediately before executing any `move`, and use those IDs exclusively. Do not cache IDs across separate terminal calls without re-listing first. When a single `move` fails (the ID disappeared mid-loop), skip it and continue with remaining IDs — don't retry the whole batch.

### JSON parsing fails on empty folders

Some queries return zero lines (not `[]`) when a folder has no messages. Guard python parsers with: `himalaya envelope list --folder X --output json 2>/dev/null | python3 -c "..." || echo "$p = 0"`.

### Flag order: subcommand first, global flags after

Put `--account` (and other global flags) AFTER the subcommand: `himalaya envelope list --account NAME ...`. The prefix form (`himalaya --account NAME envelope list`) is rejected with `unexpected argument '--account'` — flag parsing is subcommand-scoped on this binary.

### JSON output mixes WARN log lines into stdout

With `--output json`, runtime `WARN` lines print on stdout around the payload. Filter by dropping lines containing `WARN`, never by stripping the first line — line 1 is usually the JSON opening bracket, and cutting it makes every parse fail with `Expecting value: line 1 column 1`.

### Full-mailbox scans need explicit pagination

Reading a huge folder (All Mail / Todos os e-mails) returns ~10 envelopes by default. Loop `--page-size 250 --page N` until a page returns fewer than 250 rows, accumulate the pages in Python, and only then filter by sender/subject/date keywords — filtering per page misses older matches.

### Download-wrapper emails (2ª via / "clique para baixar")

- Extract the FULL href from the HTML body (up to the closing quote). A truncated click-tracking URL returns HTTP 400 with no Location header; the complete tracking link redirects and serves the file directly.
- Verify magic bytes before naming the result: check the response starts with `%PDF` before writing a `.pdf`; otherwise save as HTML and inspect.
- Copy the exported message and attachments to their canonical destination right after export — scratch directories are pruned after ~24h idle, so a multi-day task that relies on re-reading the scratch loses the artifacts and must re-fetch from IMAP.

### Threading a reply: `template reply` fails on Sent Mail; send with explicit reply headers

`himalaya template reply <ID> --all` rejects IDs whose envelopes himalaya has not indexed — Sent Mail is the common miss, failing with `cannot find message <ID>`. A plain resend with `Re:` in the subject does NOT reliably group into the original Gmail conversation (the user will see two separate emails); Gmail threads on reply headers, not subject prefix alone.

**Validated primary path — raw .eml with reply headers via `himalaya message send` (no SMTP code needed):** get the original Message-ID with `himalaya message read <ID> -f "<pasta>" --header message-id`; build a full .eml whose headers include `Subject: Re: ...`, `In-Reply-To: <id>` AND `References: <id>` (both, with angle brackets); send with `himalaya message send < reply.eml`; verify in `envelope list` that the reply sits adjacent to the original. Works even when the original lives in a locale-named Sent folder.

If Python SMTP is required instead:

1. Fetch the original `Message-ID` over IMAP, selecting the locale-correct sent folder (see the Gmail locale pitfall above): `m.select('[Gmail]/E-mails enviados')`, search by subject, `m.fetch(uid, '(BODY.PEEK[HEADER])')`, read the `Message-ID` header.
2. Build a MIME message with `In-Reply-To` AND `References` set to that Message-ID (both, with angle brackets) plus a unique new `Message-ID` of your own.
3. Send via `smtplib.SMTP('smtp.gmail.com', 587)` + STARTTLS using the password resolved by the exact command in the himalaya config's `backend.auth.cmd` (`secret-tool lookup ...` — run it via subprocess; the same credential works for IMAP and SMTP).
4. Verify by re-listing Sent and confirming the new message sits adjacent to the original before telling the user it's threaded.

### Search query syntax: space-separated operators, ASCII-only terms

`himalaya envelope list "subject:vallo"` fails with `found ':' expected space after 'subject'` — operators take a SPACE, not a colon: `envelope list subject vallo`, `envelope list body vallo`, `envelope list from user@example.com`. Accented search terms (e.g. `subject rescisão`) abort with `cannot search IMAP envelope UIDs / unexpected BAD response: Could not parse command` — search with unaccented ASCII keywords only. For exhaustive sweeps (finding every e-mail of a sender, or keyword in subject across all mail), the paginated envelope dump is more reliable than IMAP search: page the whole folder into a JSON cache (`--page-size 250 --page N` in a Python loop), then filter sender/subject/attachment in Python — IMAP search misses matches and crashes on non-ASCII.

### Tables and formatting: send multipart/alternative with an HTML part (Gmail renders it)

Gmail renders HTML e-mails (tables, colors, inline styles) — it only strips scripts. When the content is a table or anything formatting-sensitive, build a raw `.eml` with `multipart/alternative`: a `text/plain` part in prose (labeled lines, dash bullets — markdown pipes and `**` show as literal characters in plain text) plus a `text/html` part with styles INLINE on each element (external `<style>` blocks are unreliable across clients). Never paste markdown source into either part. Answer to "o Gmail suporta HTML?" is yes.

### Signature-service confirmation mails: only the HTML "finalizado" variant carries the document link
E-mails de assinatura eletrônica (ZapSign, DocuSign, Clicksign) chegam em 3 variantes: "Assinar documento", "Comprovante de assinatura" e "está finalizado". As variantes em TEXTO puro são stubs SEM link nenhum — o link do documento (`app.zapsign.com.br/verificar/<uuid>` ou equivalente) só existe na variante HTML do "está finalizado". Para achar o link: `message read` da variante "está finalizado" (o corpo vem como bloco `<#part type=text/html>` com a URL visível) ou regex `https://app\.zapsign\.com\.br/[a-zA-Z0-9/._-]+` no texto bruto. Não conclua "não há evidência" sem ter testado a variante HTML.

Página de verificação pública: abrir o link `/verificar/<uuid>` mostra SEM LOGIN o nome do documento e a contagem de assinaturas ("Assinaturas 2/2") — o grau mínimo de prova sem ter conta no serviço. O PDF em si exige login, e os e-mails de comprovante NÃO trazem anexo — não varra anexos dessas variantes à toa; "Acessar documentos assinados" leva ao signup, não ao arquivo.

Click-tracking URLs dobradas: `message export --full` mantém o corpo em quoted-printable, e regex sobre o texto bruto captura URLs cortadas na dobra de linha (HTTP 400 sem Location). Decodifique ANTES do regex: `email.message_from_string(raw, policy=policy.default)` → `part.get_content()` da part text/html → regex `https?://url\d+[^"'\s<>]+`.

### Verify the rendered HTML part before reporting a styled e-mail as sent

Render the HTML part in a browser (save the extracted HTML to a file, screenshot it) before telling the user it looks good: a template-generation bug silently duplicated a value across two table columns while the plain-text part stayed correct — both parts must be checked, and generated rows must be built by one clean loop per column (no string-replace hacks on assembled HTML). If a broken version was already delivered, send the corrected one and remove the bad duplicate from the mailbox with `himalaya message delete <ID>` (same folder-relative ID namespace as `envelope list`), telling the user both happened.
