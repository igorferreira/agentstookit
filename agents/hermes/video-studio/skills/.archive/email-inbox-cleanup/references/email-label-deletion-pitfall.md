# Critical pitfall — label deletion must never trust a script's "empty" self-report

Real event (2026-09-02, Gmail pt-BR): an orphan-cleanup pass ran `himalaya folder delete -y`
over ALL 763 `@Pessoal` labels after its scan reported `com_conteudo_preservados=0` — i.e. it
believed EVERY label was empty and deleted them all, including labels that clearly held mail
(`@Pessoal/Contas`, `@Pessoal/Negocios`, `@Pessoal/Cursos`, `@Pessoal/Bancos`).

## Why it happened
A bulk scan that counts "how many labels have ≥1 envelope" can silently produce a broken
summary line. Common bugs: wrong parse of `--output json` (a WARN on a previous stderr line
corrupts the JSON stream → `[]` for everything), a field-lookup returning empty, or a shared
accumulator being reset. A claim of "0 labels with content across 763" is **statistically
impossible** — that is the tell that the detection is broken, NOT that the job is done.

## Rules (non-negotiable for bulk label deletion)
1. **Never delete based on an aggregated self-report.** The summary line ("X empty", "0 with
   content") is exactly where a bug lies. Trust code you can inspect, not a script's verdict.
2. **Hand-verify a SAMPLE before any bulk delete.** Independently run
   `himalaya envelope list --folder "<L>" --output json` and confirm `[]` on a handful of the
   labels the script says are "empty". If any sample has mail → stop, detection is broken.
3. **Fail loud on suspicious distributions.** If >80% of labels are suddenly "empty", abort
   and report before deleting — a healthy account does not become 80% empty in one pass.
4. **Prefer consolidation-first** (move mail into buckets → source labels empty out by
   construction → delete the ones you just saw empty) over a standalone "scan all, delete all
   empties" pass. Moved-emptied labels are verifiable; inferred-emptied labels are the risk.

## Recovery fact (Gmail) — tell the user, don't panic them
Deleting a label removes the **label**, not the **messages**. The mail remains in
`[Gmail]/Todos os e-mails` (pt-BR Gmail name; "All Mail" in English) and returns to INBOX if
it had no other label. So after a label wipe:
- The MAIL IS SAFE — no messages lost.
- The taxonomy / folder structure is what was lost — that's the real (recoverable-with-effort)
  cost, because Gmail does not retain the email→label association after the label is gone.
Reassure the user their emails are intact; be honest that the labels were removed.

## Operational notes copied from the working scan (for context)
- Enumerate + count with `himalaya envelope list --folder "<L>" --page-size 1000 --output json`,
  `len(arr)` per label. This is I/O-bound and slow (~20-30 min for 700+ labels) — run in
  background with `notify_on_complete=true` and a log file.
- Delete children before parents: sort labels by depth (`x.count('/')`) descending, so leaves go
  first and a parent with remaining children doesn't error.
- `himalaya folder delete -y` (`-y`/`--yes`) is REQUIRED in non-TTY; without it you get a
  "cannot prompt boolean / input device is not a TTY" error.
