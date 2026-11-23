# Literal transcription workflow

## Goal

Produce a reader-facing literal transcript that is more reliable than a single gateway STT pass, while preserving uncertainty instead of hallucinating.

## Source checks

```bash
ffprobe -v error \
  -show_entries format=duration,size,bit_rate:stream=codec_name,sample_rate,channels \
  -of default=noprint_wrappers=1 input.ogg
sha256sum input.ogg preserved-copy.ogg
```

A matching checksum proves the preserved audio is byte-identical.

## Baseline Hermes transcription

From the Hermes source checkout or importable environment:

```python
from tools.transcription_tools import transcribe_audio
result = transcribe_audio("/absolute/path/audio.ogg")
print(result)
```

Treat the result as the first hypothesis only.

## Progressive pass strategy

When the gateway transcript is insufficient or uncertain, use a progressive model escalation instead of jumping to the largest model directly. Each pass builds on the previous one, and key disagreements between passes flag terms that need human review.

**1. Quick pass (base model)** — fast, catches obvious structure:

```python
from faster_whisper import WhisperModel
model = WhisperModel("base", device="cpu", compute_type="int8")
segments, info = model.transcribe("/path/audio.ogg", language="pt", beam_size=5)
for seg in segments:
    print(f"[{seg.start:.1f}s - {seg.end:.1f}s] {seg.text.strip()}")
```

~1.4s for a 22s clip on CPU. Good enough for short, clear audio.

**2. Improved pass (small model)** — better accuracy, fixes structural errors:

```python
model = WhisperModel("small", device="cpu", compute_type="int8")
# Same transcribe call...
```

~3.7s for a 22s clip. Typically resolves word-boundary issues from the base pass.

**3. Final pass (large-v3-turbo)** — best accuracy, resolves domain terms:

```python
model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")
```

~20-40s for a 22s clip depending on CPU. Use for legal terms, names, amounts, and allegations.

**When to skip to large directly:** when the user explicitly says the audio is critical (legal, financial, allegations) and accuracy matters more than speed. Otherwise, the progressive approach saves time and the comparison across passes helps identify genuinely uncertain words.

## Higher-accuracy local pass

```python
from faster_whisper import WhisperModel

model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")
segments, info = model.transcribe(
    "/absolute/path/audio.ogg",
    language="pt",
    beam_size=5,
    vad_filter=True,
    word_timestamps=True,
    initial_prompt=(
        "Vocabulário do domínio: TCE, Secretaria de Saúde, "
        "mandado de segurança, exonerado, liminar."
    ),
)

for segment in segments:
    print(f"[{segment.start:06.2f}-{segment.end:06.2f}] {segment.text.strip()}")

**Compare passes systematically:** when the base and small passes disagree on a word, note it; when large-v3-turbo agrees with one of them, that consensus wins. When all three differ, mark the term as uncertain.
```

Use only domain vocabulary in `initial_prompt`. Do not place expected full sentences or uncertain amounts there unless another independent pass already supports them.

## Escalation strategy

1. Compare the gateway/default transcript with `small` or `large-v3-turbo`.
2. Force the known language; auto-detection can distort short clips.
3. Inspect word timestamps/probabilities around disputed terms.
4. Split only the disputed time range when another pass is needed.
5. Prefer agreement across independent passes over one model's confidence.
6. Preserve high-confidence but semantically odd speech literally and explain it in notes.
7. Use brackets for editorial inference: `[ilegal?]`, `[termo incerto: palavra]`, `[inaudível]`.

## Legal names, amounts, and allegations

- Verify acronyms and legal terms against the audio hypotheses, not general knowledge alone.
- A technically obvious phrase such as `mandado de segurança` may correct an STT rendering like `mandato de segurança`, but disclose the correction in the fidelity note.
- An amount needs independent support from at least two passes or must be marked uncertain.
- Add a disclaimer that transcription does not validate allegations.

## Markdown/PDF production

A robust Pandoc invocation when the Markdown already contains its own H1:

```bash
pandoc transcript.md -f gfm -t html5 -s \
  --metadata pagetitle='Transcrição literal revisada' \
  --css=transcript.css -o transcript.html
```

Use `pagetitle`, not `title`, or Pandoc may render a duplicate visible title block.

For wkhtmltopdf, set white backgrounds explicitly:

```css
html, body {
  background: #fff !important;
  color: #20242a !important;
}
p, li, td { color: #20242a !important; }
```

After rendering:

```bash
pdfinfo transcript.pdf
pdftotext transcript.pdf transcript.txt
pdftoppm -png -r 140 transcript.pdf rendered/page
```

Inspect every page. If a heading is orphaned, move the heading and its content together in the Markdown. If the final page is mostly blank, rebalance with a meaningful `Transcrição — continuação` page boundary rather than reducing readability.

## Evidence to retain

Keep:

- original audio;
- canonical Markdown;
- final PDF;
- optional technical JSON with segment/word timestamps when the content is consequential;
- checksums for the original copy and final artifacts when auditability matters.
