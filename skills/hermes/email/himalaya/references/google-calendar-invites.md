# Google Calendar invites by e-mail (accept/find via himalaya)

## When to Use
Load when Igor asks to check his e-mail for interview/meeting invites ("convites", "entrevistas"), accept calendar invitations, or report on scheduled meetings received by e-mail.

## How invite e-mails look

External organizers (first contact) arrive as `Convite de remetente desconhecido: <Evento> - <dia>. <data> <HH:MM - HH:MM> (BRT) (SEU-EMAIL@gmail.com)`, sender = the organizer's own address (their calendar sends from them). The subject line already carries the date and time window — match interviews/meetings by parsing it, not by opening every message.

To find them: `himalaya envelope list --folder INBOX --output json` (paged) and filter on `convite` / `entrevista` / `interview` / organizer domain. `message read <ID>` prints the plain-text rendering, which includes the Meet link, phone PIN and organizer — enough for a report.

## RSVP link anatomy (in the HTML part)

The HTML part carries one RSVP link per response:

    https://calendar.google.com/calendar/event?action=RESPOND&eid=<base64>&rst=<N>&tok=<token>&ctz=...&hl=pt_BR&es=1

- `rst=1` = Sim (accept) · `rst=2` = Não · `rst=3` = Talvez
- `action=VIEW` links only open the event view; they do NOT respond.
- `marksenderasknown` links ("Adicionar à agenda") only mark the sender as known so FUTURE invites skip the unknown-sender notice — not an RSVP.

`himalaya message read` text output does NOT reliably include the RSVP links. To extract them, fetch the raw message over IMAP in Python and regex the HTML part for `https://calendar\.google\.com/calendar/event\?action=RESPOND[^"<>]*rst=1[^"<>]*`, then `replace('&amp;','&')`. IMAP credentials: `secret-tool lookup service hermes-gmail account <email>` (same credential works for SMTP).

## Accepting: what works

- **E-mail reply to the organizer (himalaya native path).** Build a raw .eml with `In-Reply-To`/`References` = the invite's Message-ID (format in the SKILL.md threading pitfall) and a short confirmation naming the date/time; send via `himalaya message send < reply.eml`; verify both replies exist in the locale Sent folder (`[Gmail]/E-mails enviados`). This is what the user counts as "aceitar" — but it does NOT flip the RSVP status inside Google Calendar.
- **True calendar RSVP (status Sim in Agenda).** The RESPOND link requires a logged-in Google session. The harness browser has no Google login. The local machine's CDP Chrome (`linkedin-cdp-profile`, port 9224) IS logged into Google Agenda — open the link in a tab there via CDP and confirm the event shows the accept state. Use only when the user wants the calendar status, not just a reply.
- The invite notification also appears with "Este evento ainda não está na sua agenda" — the event is not on the user's calendar until accepted via a logged-in RSVP (or manual "Adicionar à agenda").

## Report format the user expects

Per invite: date/weekday + exact time window (BRT), organizer name + address, Meet link, phone PIN, and confirmation that the reply was sent (with the Sent-folder evidence). Flag the calendar-RSVP gap as a one-line offer, not a blocker.
