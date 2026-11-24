# HeartMuLa — Open-Source Suno-like Music Generation

HeartMuLa is a family of Apache-2.0 music foundation models that generates songs conditioned on lyrics + tags, comparable to Suno. Models: HeartMuLa (3B/7B LM), HeartCodec (12.5Hz music codec), HeartTranscriptor (Whisper-based), HeartCLAP.

## When to Use
- Generate full songs from lyrics + tags
- Open-source alternative to Suno/Udio
- Local/offline music generation
- Multilingual song generation

## Hardware Requirements
- Min: 8GB VRAM with `--lazy_load true` (loads/unloads sequentially)
- Recommended: 16GB+ VRAM
- Multi-GPU: `--mula_device cuda:0 --codec_device cuda:1`
- 3B model with lazy_load peaks at ~6.2GB VRAM
- No GPU: run on CPU but expect 30–60+ min per song

## Installation (Python 3.10 required)

```bash
git clone https://github.com/HeartMuLa/heartlib.git
cd heartlib
uv venv --python 3.10 .venv
. .venv/bin/activate
uv pip install -e .

# Fix dependency conflicts (as of Feb 2026)
uv pip install --upgrade datasets transformers
```

## Required Source Patches (for transformers 5.x)

**Patch 1 — RoPE cache fix** in `src/heartlib/heartmula/modeling_heartmula.py`, in the `setup_caches` method, add after the `reset_caches` try/except block:

```python
from torchtune.models.llama3_1._position_embeddings import Llama3ScaledRoPE
for module in self.modules():
    if isinstance(module, Llama3ScaledRoPE) and not module.is_cache_built:
        module.rope_init()
        module.to(device)
```

**Patch 2 — HeartCodec loading fix** in `src/heartlib/pipelines/music_generation.py`:
Add `ignore_mismatched_sizes=True` to ALL `HeartCodec.from_pretrained()` calls (2 total).

## Download Models

```bash
cd heartlib
hf download --local-dir './ckpt' 'HeartMuLa/HeartMuLaGen'
hf download --local-dir './ckpt/HeartMuLa-oss-3B' 'HeartMuLa/HeartMuLa-oss-3B-happy-new-year'
hf download --local-dir './ckpt/HeartCodec-oss' 'HeartMuLa/HeartCodec-oss-20260123'
```

## Usage

```bash
cd heartlib
. .venv/bin/activate
python ./examples/run_music_generation.py \
  --model_path=./ckpt \
  --version="3B" \
  --lyrics="./assets/lyrics.txt" \
  --tags="./assets/tags.txt" \
  --save_path="./assets/output.mp3" \
  --lazy_load true
```

## Input Formats

**Tags** (comma-separated, no spaces):
```
piano,happy,wedding,synthesizer,romantic
```

**Lyrics** (use structural tags):
```
[Intro]
[Verse]
Your lyrics...
[Chorus]
Chorus lyrics...
[Bridge]
[Outro]
```

## Key Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--max_audio_length_ms` | 240000 | 4 min max |
| `--topk` | 50 | Sampling diversity |
| `--temperature` | 1.0 | Creativity |
| `--cfg_scale` | 1.5 | Guidance scale |
| `--lazy_load` | false | VRAM-saving mode |

## Performance
- RTF ≈ 1.0 — 4-minute song takes ~4 minutes to generate on GPU
- Output: MP3, 48kHz stereo, 128kbps

## Pitfalls
1. **Do NOT use bf16 for HeartCodec** — degrades quality. Use fp32 (default).
2. **Tags may be ignored** — known issue (#90). Lyrics dominate.
3. **Triton not available on macOS** — Linux/CUDA only for GPU.
4. **RTX 5080** — incompatibility reported upstream.
5. Dependency conflicts require manual upgrades AND source patches.

## Resources
- Repo: https://github.com/HeartMuLa/heartlib
- Models: https://huggingface.co/HeartMuLa
- Paper: https://arxiv.org/abs/2601.10547
- License: Apache-2.0
