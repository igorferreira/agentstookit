# Faster-Whisper Transcription Commands

Quick-reference for the multi-pass transcription approach used in the Aline Cunha case.

## Installation

```bash
pip3 install faster-whisper
```

Models auto-download on first use. Sizes: base (~145MB), small (~500MB), large-v3-turbo (~1.6GB).

## Multi-pass pipeline (Portuguese audio)

```python
from faster_whisper import WhisperModel

# Pass 1 — fast sanity check
model = WhisperModel("base", device="cpu", compute_type="int8")
segments, info = model.transcribe("audio.mp3", language="pt", beam_size=5)

# Pass 2 — improved accuracy
model = WhisperModel("small", device="cpu", compute_type="int8")
segments, info = model.transcribe("audio.mp3", language="pt", beam_size=5)

# Pass 3 — final/consequential
model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")
segments, info = model.transcribe("audio.mp3", language="pt", beam_size=5)

for seg in segments:
    print(f"[{seg.start:.1f}s - {seg.end:.1f}s] {seg.text.strip()}")
```

## Typical performance (CPU)

| Model | Speed | Quality |
|---:|---:|---:|
| base | ~15x realtime | OK for gist |
| small | ~6x realtime | Good |
| large-v3-turbo | ~0.5x realtime | Best for legal/consequential |

## File format support

`.ogg`, `.mp3`, `.m4a`, `.wav`, `.flac` all work. No conversion needed.

## Multi-audio case batches

When processing 5+ audios from the same case:
1. Use `base` for all first to get gists quickly
2. Only escalate to `large-v3-turbo` for audios containing legal terms, names, numbers, or allegations
3. Mark uncertain terms with `[inaudível]`, `[termo incerto: ...]`, or `[palavra provável?]`

## Domain vocabulary for slang-heavy audio

For noisy street audio with colloquial speech, use `initial_prompt` with likely slang terms:

```python
segments, info = model.transcribe(
    "audio.ogg",
    language="pt",
    beam_size=5,
    word_timestamps=True,
    vad_filter=True,
    initial_prompt="flor, maconha, bec, beck, fumar, fumaça, onda, brisa, rua, viela, boca"
)
```

This dramatically improves accuracy by disambiguating phonetically similar words (e.g. "lindando" → "lidando", "devava" → "devia", "begora" → "Beck agora").

Slang vocabulary bank: [`references/vocabulario-girias.md`](vocabulario-girias.md)

## Pitfall — model download hangs

If the model download hangs, interrupt and try again. Models cache to `~/.cache/huggingface/hub/`.
