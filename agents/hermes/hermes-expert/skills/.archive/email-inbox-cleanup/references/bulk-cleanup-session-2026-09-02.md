# Worked recipe — purge 505 + reorganize 362 (Gmail pt-BR, 2026-09-02)

Real session: Igor asked to descadastrar & delete all promos/newsletters and
reorganize the 362 preserved emails. Verified commands below.

## Enumeration (himalaya, JSON)
```bash
# paginate with --page (NOT --offset; --offset returns empty). size 500.
himalaya envelope list --page-size 500 --output json --page 1
```
Parse with Python `json.loads`; each element: `{id, subject, from:{name,addr}, date}`.

## Classification
- Build `PROTECT_WORDS` (subject-side) + `PROTECT_DOMAINS` (from.addr). Example domains:
  `@nubank @99pay @itau @bradesco @digio @mercadopago @revolut @recargapay @light @claro @vivo
  @tuya @totalpass @veroneze @cencosud @dasa @conexa @mevosaude @trabalho-...`
- Classify each email by `subject + from.name + from.addr`; if any protect keyword/domain
  matches → preserve. Else → delete list. Then AUDIT delete list again for
  `nfe|nota fiscal|fatura|boleto|comprovante|recibo|pagamento` and move those to preserve.
- This caught 4 Linx "Emissão de Nota Fiscal Eletrônica" emails that a first pass had
  wrongly binned as Notícias. Result: 505 delete / 362 preserve, 0 finance leaked.

## Purge
```bash
himalaya message delete --folder INBOX <id>...   # batches of ~100
```
- First batch silently failed (`No folder [Gmail]/Trash`) until
  `~/.config/himalaya/config.toml` had `folder.aliases.trash = "[Gmail]/Lixeira"` (pt-BR).
- Verify: re-list INBOX, assert 0 deleted ids remain. Don't trust the first loop.
- Backup IDs first: `json.dump({"apagar":[ids],"preservar":[ids]}, open(...))`.

## Label reorganization
```bash
himalaya folder add "@Banco_Financeiro/Financas"     # slash = Gmail nested label
himalaya message move --folder "INBOX" "@Banco_Financeiro/Financas" <id>...
```
- Right after `folder add`, the first `move` may return transient `System Error` — retry once
  (propagation race). Confirmed working on retry.
- Groups used: `@Banco_Financeiro/{Financas,Compras,Contas}`, `@Pessoa_Saude/Saude`,
  `@Trabalho_Carreira/Trabalho`, `@Info_Daily/{Alertas,Noticias}`.
- Delete empty old flat labels with `himalaya folder delete -y <name>` (`-y` REQUIRED in
  non-TTY; else `cannot prompt boolean / input device is not a TTY`).
- Confirm old labels empty BEFORE delete (0 envelopes) so no mail is lost.

## Timeout lesson
One-by-one `message move` loop for ~360 ids exceeded the 300s script cap and was killed.
Fix: run the moving loop in a background terminal with a log file, then derive
"ids still in INBOX" and resume. Group ids ~20/call to cut round-trips.