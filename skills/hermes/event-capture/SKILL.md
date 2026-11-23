---
name: event-capture
description: "Capture live events into dual docs with OCR extraction."
metadata:
  version: 1.0.0
  author: hermes
  license: MIT
  tags: [event, capture, documentation, OCR, live-event]
  related_skills: [transcript-synthesis, second-brain, ocr-and-documents]
---

# Event Capture — Live Event Documentation

## When to Use

Use this skill when:
- Capturing information from a **live event** (hackathon, conference, meeting, workshop)
- The user wants **absolute capture** of everything said/shown/sent ("não perde nada")
- You need to process **multiple input types** (audio, text, images) incrementally
- The user wants **dual documentation** (structured report + raw chronological log)
- You need to **extract structured data from images** (schedules, tables, charts) via OCR

Do NOT use this skill for:
- Post-event knowledge management (use `second-brain`)
- Cleaning messy transcripts (use `transcript-synthesis`)
- Simple note-taking (no dual-doc architecture needed)

---

# Event Capture — Live Event Documentation

Capture everything said, shown, and sent during a live event (hackathon, conference, meeting) into two synchronized documents: one formal/structured, one raw/incremental. Nothing is lost.

## Mental Model

```
ANOTACOES.md   →   PEDIDOS.md
(formal)          (raw incremental)
structured        chronological
versioned         source-indexed
```

- **ANOTACOES.md** — Formal document: sections, tables, structured data, versioned. The "report."
- **PEDIDOS.md** — Raw capture: everything the user says, indexed by source number, chronological. The "catch-all."

Both documents stay synchronized. When information is added to one, mirror it to the other (in the appropriate format).

## Step 1 — Initialize the Dual Documents

1. **Create the working directory**: `~/MEGA/Documentos/<event-slug>/`
2. **Create ANOTACOES.md** with the template structure (see `references/dual-doc-template.md`). Key sections:
   - Header (event name, dates, location)
   - Contexto/Escopo (volume, business context)
   - Cronologia (chronological events)
   - Estrutura (groups, teams, people)
   - Deliverables
   - Participantes/Suporte (table)
   - Insights
   - Fontes (source index)
3. **Create PEDIDOS.md** with the template structure. Key sections:
   - Regras de Registro (rules — absolute capture, chronological indexing)
   - Participantes (same table as ANOTACOES)
   - Contexto e Escopo
   - Cronologia (raw, with source numbers)
   - Fontes (source list with timestamps)
   - Pendentes (what's still missing)

> **Pitfall:** Read the full file before patching. The patch tool requires an exact `old_string` match. If you've only read a portion, the patch will fail with "Could not find a match." Always `read_file` the target section before patching.

## Step 2 — Process Each Input Incrementally

> **CRITICAL PRE-STEP:** If an input arrives with a `TimedOut` error, STOP all capture work. Inform the user and wait. Never hallucinate or skip missing audio.

As the user sends inputs (audio, text, images), process them in this order:

### Audio Inputs
1. Transcribe the audio (use `audio-transcription` skill or manual transcription from context)
2. Add to **PEDIDOS.md** under the current day's section with source number (e.g., `Áudio 1: 09:49 — ...`)
3. Extract key facts and add to **ANOTACOES.md** in the appropriate section
4. Update the **Fontes** list in both documents

### Text Inputs
1. Add to **PEDIDOS.md** with source number and timestamp (e.g., `Texto 4: 09:54 — ...`)
2. If the text contains structured information (names, dates, volumes), add to **ANOTACOES.md** in the appropriate section
3. Update **Fontes** list

### Image Inputs
1. **Save the image** to the working directory with a descriptive name (e.g., `img_052f812b7c4d.jpg`)
2. **Run vision_analyze** to extract content:
   - For structured data (tables, schedules, charts): extract the data and add to **ANOTACOES.md** as a table
   - For descriptive content (logos, designs, screenshots): add a description to **ANOTACOES.md**
3. Add to **PEDIDOS.md** under **Fontes** with source number and file path
4. Update the **Arquivos de Imagem** table in **ANOTACOES.md** (if applicable)

> **Pitfall — OCR extraction:** `vision_analyze` can extract text from images with good accuracy. For tables/schedules, extract the data and format it as a Markdown table in **ANOTACOES.md**. Don't just paste the raw OCR text — structure it.

> **Pitfall — Image paths:** The image path from the user's message (e.g., `/home/igorferreira/.hermes/cache/images/img_052f812b7c4d.jpg`) is the canonical path. Save a copy to the working directory with a descriptive name for long-term reference.

## Step 3 — Synchronize and Verify

After processing each input:

1. **Check both documents** for consistency:
   - Source numbers match between PEDIDOS.md and ANOTACOES.md
   - Dates/times are consistent
   - Names/spelling are consistent
2. **Update the Pendentes list** in PEDIDOS.md:
   - Mark completed items with `[x]`
   - Add new pending items as `[ ]`
3. **Report to the user** what was captured and where:
   - "Cronograma extraído e salvo em ANOTACOES.md + PEDIDOS.md"
   - "Imagem salva em `~/MEGA/Documentos/<event>/img_XXX.jpg`"

## Step 4 — Final Synthesis and Post-Event Archive

After the event ends:

1. **Review ANOTACOES.md** — ensure sections are complete and distinguish recorded observations from interpretation.
2. **Review PEDIDOS.md** — reconcile its source index with ANOTACOES.md; mark unresolved items as unavailable rather than filling gaps by inference.
3. **If the user asks to locate and consolidate materials across multiple folders, follow `references/post-event-archive.md`.** Treat this as a provenance-preserving research/archive task, not just a compression step.
4. **Archive non-destructively:** copy the source directory into the archive; do not move, rename, or overwrite original materials. Keep copied source filenames as-is; use lowercase for newly generated folder and report names.
5. **Report verified counts, destination, missing sources, search coverage, exclusions, and whether cloud synchronization was actually confirmed.** Do not infer upload completion merely because a sync client is running.

## Pitfalls and Standing Evidence Rules

- **Preserve originals:** Keep the original input and its provenance; never move or overwrite a source when creating an archive copy.
- **Do not claim media is saved from a note alone:** A reference to an audio/image in ANOTACOES.md or PEDIDOS.md is not proof the file exists. Locate and verify the actual file; otherwise report it as referenced but not found within the searched locations.
- **Separate evidence from inference:** Cite the source path and line/page/timestamp for factual claims; distinguish contemporaneous records, later summaries, proposals, and unverified self-reported metrics. Preserve contradictions and state search limits instead of silently choosing a version.
- **Security before copying:** Never copy or expose passwords, tokens, keys, credentials, or connection strings. Scan candidate material first; create sanitized copies with secret values replaced by `[REDACTED]`, or exclude an unsafe binary and report the omission without revealing the value.
- **New names are lowercase:** Use lowercase for generated folder and report names; preserve source filenames exactly when copying them.
- **Absolute capture:** The user's rule is "não perde nada" (nothing is lost). Every input — audio, text, image — gets a source number and is indexed. Don't skip anything.
- **Chronological indexing:** PEDIDOS.md is chronological. Source numbers increment with each input (Áudio 1, Texto 2, Imagem 3, etc.). Don't renumber.
- **Patch before write:** Always `read_file` the target section before patching. The patch tool requires an exact `old_string` match. If you've only read a portion of the file, the patch will fail.
- **OCR > manual entry:** When an image contains structured data (tables, schedules), extract it via `vision_analyze` and format as a Markdown table. Don't manually type it — OCR is faster and more accurate.
- **Image preservation:** Save all images to the working directory with descriptive names. Reference them in both documents. Don't rely on the cache path alone.
- **Synchronization:** Both documents must stay in sync. When you add to one, mirror to the other (in the appropriate format). Don't let them drift.
- **Timeout Protocol:** If a voice message returns `TimedOut`, stop capturing immediately. Output a visible status marker (`⏳ TimedOut — aguardando envio`). Do not assume the content, do not skip it, and never hallucinate fillers. Wait for the retry or ask the user to send text.
- **Name Disambiguation:** Events frequently feature multiple participants with the same name (e.g., two different "Carlos" in separate groups). Immediately tag the first mention with a unique qualifier (e.g., `Carlos [G3 - Dados]`, `Carlos [G4 - Deparação]`) in both documents. Add a note if a new name appears that conflicts with a prior one.
- **File Patch Safety (Pagination Gotcha):** When inserting content via `patch`, always ensure the `old_string` boundary is fully loaded in context. Reading a file with `read_file(offset=X, limit=Y)` leaves you with only a partial view. If the patch fails due to a mismatch, re-read the target section with wider margins or use `search_files` to locate the exact insertion anchor before trying again.
- **Chronological Anchoring:** Always use the time provided by the runtime (`[Agora: ...]` in the system prompt). Running `date` on the host machine risks timezone drift or stale cache if the VM clock differs from the Telegram client. Treat the injected block as the absolute source of truth.
- **Structural Consistency:** New rows added during live capture must strictly match the header syntax (bold keys, consistent delimiters) of the tables already present in ANOTACOES.md/PEDIDOS.md. Forcing new column structures mid-pitch breaks downstream parsing or dashboard integrations.

- `transcript-synthesis` — for cleaning messy audio transcripts before capture
- `second-brain` — for archiving the final event documentation into the wiki (post-event)
- `ocr-and-documents` — for advanced OCR on complex documents (receipts, forms)

## References

- [`references/dual-doc-template.md`](references/dual-doc-template.md) — Template structure for ANOTACOES.md and PEDIDOS.md
