---
name: audio-transcription
description: "Use for literal or edited transcription of voice messages, meetings, interviews, and forwarded audio; preserve originals, resolve uncertain terms with multi-pass STT, and deliver verified Markdown/PDF artifacts."
version: 1.0.0
created_by: agent
metadata:
  hermes:
    tags: [audio, transcription, speech-to-text, whatsapp, telegram, whisper, markdown, pdf]
---

# Audio Transcription

**Setup:** instale `pip3 install faster-whisper` antes de usar (veja seção Setup para detalhes).

## Setup / Pré-requisitos

Antes de usar, instalar o `faster-whisper`:

```bash
pip3 install faster-whisper
```

Verificar instalação:
```bash
python3 -c "from faster_whisper import WhisperModel; print('OK')"
```

O modelo base (~1.5 GB) é baixado automaticamente na primeira execução. Modelos maiores (`small`, `large-v3-turbo`) também são baixados sob demanda.

Para comandos exatos de transcrição multi-passo e multi-modelo, veja [`references/faster-whisper-commands.md`](references/faster-whisper-commands.md).

## Trigger

Use this skill when the user sends or references an audio/voice message and asks to:

- transcribe literally or produce a cleaned transcript;
- preserve timestamps, speakers, pauses, hesitations, or inaudible markers;
- extract names, legal/technical terms, dates, values, tasks, or decisions;
- save the original audio and transcription;
- generate Markdown and PDF versions;
- generate a consolidated document joining multiple related audios;
- create an analysis document (legal, technical) alongside the transcripts;
- format the transcription for WhatsApp delivery.

Do not treat creative music generation or spectrogram work as transcription; route those to `audio-and-music-workflows`.

### 0. Rapid-fire real-time transcription (conversational context)

When the user sends multiple audios in rapid succession (live chat/conversation thread), skip the full artifact pipeline (Markdown/PDF). Instead:

1. **Find the most recent audio** files by timestamp: `ls -lt ~/.hermes/audio_cache/*.ogg | head -N`
2. **Batch transcribe** all pending audios in a single Python loop to avoid per-file overhead:
   ```python
   files = [("audio_xxx.ogg", "Quem"), ...]
   for fname, quem in files:
       segs, info = model.transcribe(str(base/fname), language="pt", beam_size=5, vad_filter=True)
       print(f"🎙️ {quem} | {info.duration:.0f}s")
       for s in segs: print(f"  [{s.start:.0f}s] {s.text.strip()}")
   ```
3. **Deliver inline** with a compact table (speaker, duration, transcript snippet) — no Markdown file unless the user explicitly requests it.
4. **Tag the speaker** explicitly (e.g. "🎙️ Adrielly" vs "🎙️ Igor") using what the user told you, not inference from sender metadata.
5. **For noisy street audio**, escalate progressively: `base` first pass, then `small` with `initial_prompt` containing known slang. If `base` gives gibberish, don't trust it — go to `small` immediately.
6. **Pair with analysis** (if the user has a relationship/situational agent like Rafael) — deliver raw transcript then interpretation in a single response.

## User-specific defaults

For Igor:

- store transcription artifacts under `/home/igorferreira/MEGA/Documentos/Transcricoes/`, normally grouped by year;
- preserve the original audio beside the Markdown/PDF;
- default to a **literal revised transcript**: retain oral phrasing, repetitions, pauses, and slang while adding punctuation and correcting only unmistakable recognition errors;
- when Igor asks only for transcription, show it for review before saving; when he explicitly asks to generate/save Markdown or PDF, create the artifacts immediately;
- distinguish the person who forwarded/sent the file from the person speaking; never infer speaker identity from the Telegram/WhatsApp sender label alone.

## Workflow

### 1. Discover and preserve the source

1. Use the explicit attachment path when present.
2. If the gateway gives only an auto-transcript, locate the corresponding recent audio in the Hermes audio cache and verify duration/mtime.
3. Copy the original into the destination before processing.
4. Verify the copy by size and checksum; never replace the original with a converted derivative.
5. Record source platform, receipt timestamp, duration, codec, and speaker identity status.

### 2. Define the transcription mode

- **Literal:** preserve exact wording, repetitions, incomplete constructions, fillers, slang, and relevant non-speech events.
- **Literal revised (Igor default):** same fidelity, with punctuation and correction of unequivocal STT mistakes; disclose every inferred word.
- **Cleaned:** improve grammar and remove repetitions only when explicitly requested.
- **Summary/minutes:** produce after the transcript, not instead of it, unless the user says otherwise.

### 3. Never trust one STT pass for consequential audio

The gateway transcript is a hypothesis, not evidence. For names, legal issues, money, health, allegations, or technical terminology:

1. run the configured/default STT pass;
2. rerun with forced language and a stronger model;
3. use short segments and timestamps when wording remains uncertain;
4. add a narrowly factual context prompt containing likely domain terms, without scripting full sentences that could bias the model;
5. compare passes and word confidence;
6. mark unresolved wording as `[inaudível]`, `[termo incerto: ...]`, or `[palavra provável?]` rather than inventing.

**Domain vocabulary:** for informal/colloquial audio, consult [`references/vocabulario-girias.md`](references/vocabulario-girias.md) for slang terms to include in `initial_prompt`. Including likely slang (e.g. "flor, bec, beck, fumar, brisa") in the prompt dramatically improves accuracy on noisy street audio by disambiguating phonetically similar words.

Recommended local escalation:

- quick pass: Whisper `base`;
- improved pass: `small`, forced language, beam search, timestamps;
- consequential/final pass: `large-v3-turbo`, forced language, word timestamps, domain vocabulary.

See [`references/literal-transcription-workflow.md`](references/literal-transcription-workflow.md) for commands and comparison details.  
For working copy-pasteable Python snippets, see [`references/faster-whisper-commands.md`](references/faster-whisper-commands.md).
For noisy street audio with slang/drug context, see [`references/noisy-street-audio.md`](references/noisy-street-audio.md).
For deleted audio recovery and forensic analysis, see [`references/deleted-audio-forensics.md`](references/deleted-audio-forensics.md).
For identifying drug comedown in follow-up text messages after transcribed audios, see [`references/cocaina-crash-pattern.md`](references/cocaina-crash-pattern.md).

### 4. Editorial rules

- Add punctuation for readability but do not silently rewrite content.
- Preserve unusual but confidently heard wording and flag it in a notes section.
- Normalize an obvious legal/technical recognition error only when multiple cues support it; disclose the normalization.
- Do not convert allegations in audio into factual claims.
- Do not infer a named speaker from voice gender, chat sender, filename, or forwarding metadata.
- If speakers cannot be distinguished reliably, use `Pessoa não identificada` instead of fabricated labels.
- Use timestamps at meaningful paragraph/speaker boundaries; dense word-level timestamps are for the technical sidecar, not the reader-facing transcript.

### 5. Markdown artifact

Use [`templates/transcricao-literal.md`](templates/transcricao-literal.md) as the starting structure.

Minimum sections:

1. title;
2. identification/metadata table;
3. fidelity note;
4. timestamped transcript;
5. uncertain passages requiring human confirmation;
6. content disclaimer for unverified allegations when applicable;
7. transcription method and model passes.

Use descriptive filenames:

`YYYY-MM-DD_AUDIO-COMPARTILHADO-POR-<NOME>-<ASSUNTO>-TRANSCRICAO.md`

Store the original with the same stem minus `-TRANSCRICAO`.

### 6. PDF generation and visual QA

Markdown is the canonical source. Generate PDF only after Markdown is final.

PDF requirements:

- A4, explicit white background, dark readable text, and sufficient margins;
- use `pagetitle` rather than Pandoc `title` when the Markdown already has an H1, to avoid duplicate titles;
- keep metadata tables intact;
- keep headings with following content;
- do not leave a section heading at the bottom of one page with its list/text on the next;
- rebalance pages if a final page is mostly empty by moving a meaningful transcript continuation to it, not by shrinking text excessively;
- verify all pages visually after every pagination change;
- extract PDF text to check missing terms and replacement characters.

A successful PDF check confirms:

- no dark-mode background leakage;
- no duplicate title;
- no orphan heading;
- no split table or isolated list item;
- no blank/almost-empty page when content can be balanced;
- no clipping, overlap, or broken Unicode.

### 7. Multi-audio case organization

When multiple audio transcriptions relate to the same topic, person, or investigation (e.g. 3 audios about "Caso Aline Cunha"):

1. **Detect the relationship** — look for recurring names, places, or references across transcriptions. The user may explicitly say "esse é o 3º da sequência" or refer to a case name.
2. **Create a case folder** — `~/MEGA/Documentos/Transcricoes/CASO_<NOME>/` with uppercase snake_case.
3. **Move all related files** into the folder (original audios, transcription `.md`, and `.pdf`).
4. **Create `INDEX.md`** inside the folder with:
   - File list table (filename, date, brief content summary)
   - Case summary table (key facts, people involved, values, dates, next steps)
   - "Last updated" date
5. **Keep future transcriptions for the same case** in the same folder.
6. **Clean up** — remove empty source subdirectories after moving files.

### 8. Forensic chain of custody (for legal cases)

When the transcriptions are destined for legal use (lawyer, MP, court), record **criminal evidence metadata** for every audio file:

1. **Extract SHA-256 hash** of every original audio file:
   ```bash
   cd CASO_FOLDER && sha256sum *.ogg *.mp3 *.m4a
   ```
2. **Extract technical metadata** (codec, duration, bitrate, sample rate) with ffprobe:
   ```bash
   for f in *.ogg *.mp3 *.m4a; do
     echo "--- $f ---"
     ffprobe -v quiet -show_entries format=duration,size,bit_rate \
       -show_entries stream=codec_name,sample_rate,channels -of csv=p=0 "$f"
   done
   ```
3. **Create `INDICE-PROVAS.md`** listing:
   - Filename, SHA-256 (full), duration, codec, file size, bitrate
   - Chain-of-custody log (who collected, who preserved, who transcribed)
   - Index of related documents (transcripts, analyses)
4. **Generate `INDICE-PROVAS.pdf`** alongside the consolidated transcript.
5. **Purpose:** If anyone edits even 1 byte of any audio, the SHA-256 mismatch immediately invalidates the evidence chain. This satisfies Art. 158-A to 158-F of the CPP (Lei 13.964/2019 — Pacote Anticrime).

For automated extraction, run [`scripts/extract-audio-hashes.py`](scripts/extract-audio-hashes.py) from the case folder.

### 9. Legal analysis from transcripts

When the user asks for a legal analysis of transcribed audios (e.g. "analisa como advogado criminalista"):

1. **Re-read all transcripts** before writing — base every claim on actual transcribed content.
2. **Cite the literal text of the law**, not just article numbers. Use blockquotes for the legal text.
3. **Structure:** (a) facts summary, (b) criminal typification with full articles, (c) improbidade administrativa if applicable, (d) licitações if applicable, (e) nepotism/constitutional violations, (f) chain of custody for digital evidence, (g) competency/forum, (h) individual responsibility analysis, (i) procedural recommendations with deadlines, (j) conclusion.
4. **Add legal references table** at the end listing every diploma cited.
5. **Deliver as both Markdown and PDF** via pandoc + wkhtmltopdf.
6. If the user mentions the analysis is for an **advogado**, also offer to create a **minuta de notícia-crime** — a template for filing with the Ministério Público (Arts. 5º, II and 27 CPP). Include: (a) qualificação, (b) dos fatos with numbered sub-sections, (c) do direito with article citations, (d) dos pedidos, (e) das provas/annexes list, (f) signature blocks.

### 10. Consolidated document (multiple related audios)

When the user sends several audios in a sequence about the same case and asks for a single deliverable:

1. **Create one markdown file** that joins all transcriptions in chronological order, using `<div style="page-break-before: always;"></div>` between each.
2. **Add an index/table of contents** at the top listing all audios with titles.
3. **Generate PDF** with pandoc:
   ```bash
   pandoc CONSOLIDADO.md -o CONSOLIDADO.pdf --pdf-engine=wkhtmltopdf \
     --metadata title="CASO - Título" \
     -V margin-top=2cm -V margin-bottom=2cm -V margin-left=2cm -V margin-right=2cm
   ```
4. **Add optional analysis document** if requested (e.g. legal analysis, case summary) and convert to PDF the same way.

See `templates/consolidado-transcricoes.md` for the template.

### 11. WhatsApp-formatted delivery

When the user asks for text formatted for WhatsApp:

- **No markdown tables** — use bullet lists or plain text instead
- **Bold with asterisks** (`*texto*`) — WhatsApp supports markdown-style bold
- **No headers** (`#`, `##`) — use emoji separators or dashes (━━━)
- **No code blocks with triple backticks** — use inline or indented text
- **Line breaks for readability** — keep paragraphs short

Example WhatsApp format:

```
🎵 *Nº ÁUDIO — TÍTULO*

Texto da transcrição aqui...

━━━
📁 PASTA
🎧 ~59s
```

### 12. PDF generation for any markdown

For any markdown that needs PDF delivery:

```bash
pandoc arquivo.md -o arquivo.pdf --pdf-engine=wkhtmltopdf \\
  --metadata title="TÍTULO" \\
  -V margin-top=2cm -V margin-bottom=2cm \\
  -V margin-left=2cm -V margin-right=2cm
```

Pre-requisites: `pandoc` and `wkhtmltopdf` must be installed. Verify with `which wkhtmltopdf`.

### 13. Delivery

- [ ] Original audio copied and checksum/size verified
- [ ] Duration and source metadata recorded
- [ ] Sender and speaker identity kept separate
- [ ] Consequential terms checked with more than one STT pass
- [ ] Uncertain words visibly marked
- [ ] No allegation presented as verified fact
- [ ] Markdown saved as canonical source
- [ ] PDF text extraction passed
- [ ] Every PDF page visually inspected
- [ ] Markdown/PDF paths delivered

## Pitfalls

- **Using only the gateway transcript:** short legal names and money amounts are often wrong; rerun on the original.
- **Over-correcting literal speech:** punctuation is allowed, paraphrase is not.
- **Prompt contamination:** context prompts should list domain vocabulary, not dictate the expected sentence.
- **Sender = speaker assumption:** forwarded WhatsApp audio can be voiced by someone else.
- **Deleted audio = smoking gun:** when the user says an audio was deleted by the sender, prioritize re-transcribing it with a strong model (`small` or better). Deleted audios often contain confessions, true feelings, or evidence the sender didn't mean to share. See [`references/deleted-audio-forensics.md`](references/deleted-audio-forensics.md).
- **Post-audio crash texts:** if transcribed audios reveal drug/alcohol use and the user later shares follow-up texts, check for cocaine crash symptoms (vazio, sem forças, desesperada, não consigo chorar). These are chemical, not emotional — do not make relationship decisions during the crash window. See [`references/cocaina-crash-pattern.md`](references/cocaina-crash-pattern.md).
- **Unreviewed PDF:** correct text can still produce dark backgrounds, duplicate headings, orphan titles, or poorly balanced pages.
- **Rapid-fire conversation audios:** gateway auto-transcripts of live chat audio are particularly unreliable due to street noise, music, and overlapping voices. Always run a local Whisper pass; the `base` model is fast enough for real-time delivery. For audios under 10s with heavy noise, skip `base` entirely and go directly to `small` with `initial_prompt` containing known slang.
- **Batch mode for conversation threads:** transcribing 8+ short audios one at a time wastes cycles. Use a single Python script that loops over files — the model stays warm in memory and throughput is 3-4× faster than individual calls.
