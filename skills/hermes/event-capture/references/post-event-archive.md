---
name: post-event-archive
description: Reusable workflow for provenance-preserving event archives and evidence reviews.
version: 1.0.0
author: hermes
license: MIT
metadata:
  hermes:
    tags: [event, archive, provenance, evidence, security]
    related_skills: [event-capture, second-brain, ocr-and-documents]
---

# Post-Event Archive and Evidence Review

Use this reference when a user asks to find, inventory, consolidate, or deeply analyze event materials spread across folders, drives, or capture systems. It complements the live dual-document workflow; it does not replace or rewrite the source records. Its scope ends at a verified source archive and evidence-led report; use `second-brain` separately if the user wants those conclusions compiled into a personal knowledge wiki.

## Procedure

1. **Set scope.** Identify the requested destination and plausible source roots from the event records and filenames. Search both filenames and contents. Record each root searched, excluded, or unavailable; do not call a search exhaustive without defining its boundary.
2. **Inventory before copying.** Create a structured manifest with exact source path, relative destination path, file type, size, filesystem timestamp, SHA-256, role, and copy/sanitization status. Persist the manifest and summarize it programmatically; do not rely on clipped, compressed, or one-line command output for counts or findings.
3. **Classify by provenance.** Separate contemporaneous records and user-supplied originals from later summaries, OCR/transcriptions, proposals, scripts, and ancillary logistics. Treat agendas as planned schedules, not proof of what happened; treat later summaries as secondary evidence. Label reported metrics as self-reported unless independently verified.
4. **Check security before copying.** Inspect text and extractable content from PDFs, office documents, archives, and source code for credentials, keys, tokens, passwords, and connection strings without printing matched values. Write only sanitized copies with secret values replaced by `[REDACTED]`. If a binary cannot be sanitized reliably, exclude it from the destination and list the omission using metadata only. Never modify the original.
5. **Copy without collisions.** Preserve the source tree under separate, lowercase source-root namespaces so equal filenames cannot overwrite one another. Keep source filenames unchanged. Do not move or delete originals. If the destination already has a conflicting file, preserve both under distinct namespaces or stop and report the conflict; never overwrite silently.
6. **Record duplicates, do not erase provenance.** Compare SHA-256 hashes. Mark identical files as duplicates in the manifest, but keep each source path represented; only omit a duplicate copy when the user has asked for deduplication or space-saving.
7. **Write an evidence-led analysis.** Put generated `index.md` and `analysis.md` in lowercase. Separate sourced facts, interpretations, contradictions, unknowns, and recommendations. Cite source path plus page/line/timestamp wherever available. An audio mention in a note does not establish that the original recording was saved; verify the file and metadata before claiming it was found.
8. **Verify the result.** Recount the inventory and destination files, compare hashes for unmodified copies, verify sanitized copies contain `[REDACTED]` and no original secret, and confirm no existing file was overwritten. Report local copy verification separately from cloud-sync verification; a running sync process alone is not proof that upload finished.

## Reporting checklist

- Source roots searched and meaningful exclusions
- Counts by source root and file type, backed by the saved manifest
- Files copied, sanitized, skipped, or unavailable
- Duplicate hashes and retained provenance
- Facts vs interpretations; contradictions and evidence quality
- Missing originals, especially audio/images referenced by notes
- Destination verification and explicit cloud-sync status
