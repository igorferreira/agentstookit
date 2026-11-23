---
name: email-inbox-cleanup
description: "Bulk inbox cleanup: delete promos, keep finance, relabel."
version: 1.0.0
platforms: [linux, macos, windows]
---

# Email Inbox Cleanup (descadastro + purge + label reorganize)

Class of task: "descadastra newsletters", "apaga promoções", "organiza meus labels/emails",
"limpa minha caixa". Operates on Gmail (and IMAP generally) via the `himalaya` CLI.

Always load the `himalaya` skill for CLI basics; this skill covers the *bulk cleanup workflow*
and its safety rules. Never invent outlook-wide commands — confirm each destructive step.

## GUARDRAILS (these override "just do it")

1. **Never touch financial/important mail.** Preserve, by subject+domain keyword: fatura,
   boleto, pix, recibo, comprovante, NF-e/nota fiscal, conta (luz/gás/condomínio/Claro/Vivo),
   seguro, banco (Nubank/99Pay/Mercado Pago/Itaú/Bradesco/C6/Inter/Digio/Revolut/RecargaPay),
   benefício (TotalPass/SmartFit), gov.br, contracheque/holerite, RH/Noorden, consulta crédito (Serasa/SCPC/Boa Vista).
2. **"Confirmação de entrega" / "compra chegou" is DELETEABLE** — the user explicitly authorizes it (Lojas: Mercado Livre, Shopee, Amazon).
3. **Move emails before deleting labels.** When reorganizing, confirm the old labels are EMPTY
   before `folder delete`; a non-empty delete destroys mail permanently.
4. **Get an explicit "PODE APAGAR" before bulk delete.** Show the counts (delete vs preserve)
   and the category breakdown first. The user is financially sensitive — respect the rhythm.
5. **Back up the ID lists first** (persist a deletes log) — harmless and aids recovery/audit.

## Reliable enumeration + classification

- **Use `--output json`**, not awk on the table (column widths shift). Paginate with
  `--page N` (NOT `--offset`; `--offset` returns empty). Batch `--page-size 500`.
- Envelope JSON: `id`, `subject`, `from.{name,addr}`, `date`.
- Classify **per-email** (subject + from.name + from.addr concatenated), not per-sender —
  a single sender often mixes promo and financial mail. Match preserve-keywords FIRST,
  then delete. Fallback: classify unknown into a "Notícias/leitura" folder, never delete.
- **Audit the would-delete list** for misclassified financial mail (NF-e, nota fiscal,
  fatura, boleto, "pagamento") before executing; silently relabel to Compras/Financas.

## Executing the purge (to Trash, not expunge)

- `himalaya message delete --folder INBOX <id>...` marks-as-deleted / moves to the configured
  trash alias. Batch ids in groups (~100) so no single shell arg line explodes. Verify after:
  re-list INBOX and assert none of the deleted ids remain.
- **Trash locale pitfall:** on non-English Gmail the delete FAILS with
  `No folder [Gmail]/Trash` unless `folder.aliases.trash` in
  `~/.config/himalaya/config.toml` matches the real Gmail name (PT-BR → `[Gmail]/Lixeira`).
  Fix the alias, then retry. The email does NOT delete until this matches — re-check, don't
  assume success from the first (silently failing) loop.
- Do NOT prompt-confirm in non-TTY; pass positional ids directly (non-interactive).

## Label (re)organization

- Create a hierarchy with slash in the name: `himalaya folder add "@Banco_Financeiro/Financas"`.
  Parent must exist/be created. Gmail renders slash-labels as nested folders.
- Move mail with `himalaya message move --folder "INBOX" "<dest>/<Sub>" <id>...`.
  Transient `System Error` right after folder creation is a propagation race — retry once
  before assuming a real failure.
- Delete an EMPTY old label with `himalaya folder delete -y` (the `-y`/`--yes` flag is
  REQUIRED in non-TTY; without it you get `cannot prompt boolean / input device is not a TTY`).
- Prefer a small set of clear top-level groups (e.g. `@Banco_Financeiro/{Financas,Compras,Contas}`
  `@Pessoa_Saude/Saude`, `@Trabalho_Carreira/Trabalho`, `@Info_Daily/{Alertas,Noticias}`)
  and nest the user's net-new labels under them rather than piling flat labels on the root.

## Pitfalls

- `message move` destination name must exactly match the created folder incl. slash case.
- Long one-by-one `move` loops can exceed a 300s script timeout — run in background with a log
  file, and re-derive "still in INBOX" ids to resume where it stopped.
- Deleting a label that Gmail treats as a category (`[Gmail]/...`) won't work / is not intended.

## Support files

- `references/bulk-cleanup-session-2026-09-02.md` — worked recipe from a real purge+reorg.