# Session addendum (2026-09-09): hyphen-split, inbox routing, empty-label purge, NF-by-issuer

Follow-up techniques from a large real session (907 labels audited; 2.417 emails
dedup-migrated; 1.054 "important" marks stripped; 472 NF emails grouped; 87
INBOX emails routed to zero).

## Hyphen-split rule (user convention)

Leaf labels like `Alimentacao/Delivery-ifood` or `Carros-Fiat-Punto-ELX-KRK2101`
must become directories: `Delivery/ifood`, `Carros/Fiat/Punto/ELX/KRK2101`.
User confirmed: **"quebra TODOS os hífens"** (all hyphens, every level).

```python
folha = antigo.split("/")[-1]
novo = "/".join(antigo.split("/")[:-1] + folha.split("-"))
```

Apply the Technique 3 migration per label. Scale note: 389 labels in one run;
~1s/label plus batch STOREs — schedule as a **background job** with flushed
progress prints, reconnect-retry on `System Error`/`EOF`, and idempotent
`-label:` exclusion queries so reruns are safe.

## Empty-label purge

After the hierarchy audit, labels with 0 emails AND no emails anywhere in their
subtree can be deleted, **deepest-first** (`sorted(vazias, key=lambda x:
-x.count("/"))`). Real numbers: 62 found (mostly `Dev/*` history), 61 deleted.
`[Gmail]/Importante` refuses with `[CANNOT] Internal folder cannot be deleted`
— expected; report as unresolvable, don't loop on it.

## NotaFiscal grouping by issuer

For a catch-all NF/nota-fiscal label:

1. Fetch `BODY.PEEK[HEADER.FIELDS (FROM)]` per UID, extract sender domain.
2. Map known domains → issuer: mercadolivre→MercadoLivre, shopee→Shopee,
   lojanike→Nike, usereserva→Reserva, prefeitura/fazenda/sefaz→SEFAZ family,
   enotas/enotasgw/linxnfe/fiscalflow/sieg→NFe (gateway issuers).
3. Apply `<Label>/<Issuer>` for issuers with ≥3 emails; leave rare ones at the
   label root (avoids a forest of 1-email leaves).
4. Unify duplicate labels first (`Notas Fiscais` w/ space → `NotaFiscal`, 5
   emails moved, duplicate deleted).

Real result: 472 emails → MercadoLivre 122, Prefeitura 97, NFe 27, Vultr 14,
Gmail 11, Mail 8, and 3-4 each for smaller issuers.

## INBOX routing (empty the inbox)

Map each INBOX email's FROM domain → destination label via a domain dict
(amazon→Dev/Vendors_Empresas/Amazon, linkedin→Carreira/LinkedIn,
fatura.portobank→Financeiro/Cartoes/PortoBank, light→Financeiro/Contas_Casa/Luz,
infojobs→Alertas de vagas...). Batch-apply label + archive. **Unmatched senders
go to the user's triage label (`AAA-Revisar`), never deleted.**

Real result: 87/87 routed in one pass. Verify with `X-GM-RAW "label:inbox"`
afterwards — folder SELECT shows phantom counts.

## Syntax trap: archiving per-uid

`-X-GM-LABELS '(\Inbox)'` applied per-uid sometimes writes a **literal**
`\Inbox` label instead of removing the inbox flag (observed: `X-GM-LABELS
("\\Inbox" Dev/...)` — escaped backslashes stored as text). Big batch STOREs
behaved correctly. Always test the exact STORE syntax on one email with
`fetch (X-GM-LABELS)` before bulk-running, and re-verify with
`X-GM-RAW "label:inbox"` afterwards.

## json.dump gotcha

imaplib UIDs and search results are bytes — decode to str before
`json.dump(emissores, ...)`, else `TypeError: keys must be str, not bytes`.
