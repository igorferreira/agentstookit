# AudioCraft (Meta) — MusicGen, AudioGen, EnCodec

Meta's open-source framework for text-to-music and text-to-sound generation.

## When to Use AudioCraft

- Generate music from text descriptions (MusicGen)
- Create sound effects and environmental audio (AudioGen)
- Melody-conditioned generation (musicgen-melody)
- Stereo audio output (musicgen-stereo-*)
- Style transfer from reference audio (musicgen-style)

## Installation

```bash
pip install audiocraft
# or latest from GitHub
pip install git+https://github.com/facebookresearch/audiocraft.git
# or via HuggingFace Transformers
pip install transformers torch torchaudio
```

## Quick Start

```python
import torchaudio
from audiocraft.models import MusicGen

model = MusicGen.get_pretrained('facebook/musicgen-small')
model.set_generation_params(duration=8, top_k=250, temperature=1.0)

wav = model.generate(["happy upbeat electronic dance music with synths"])
torchaudio.save("output.wav", wav[0].cpu(), sample_rate=32000)
```

## Model Variants

| Model | Size | Use Case |
|-------|------|----------|
| `musicgen-small` | 300M | Quick generation, low VRAM |
| `musicgen-medium` | 1.5B | Balanced quality |
| `musicgen-large` | 3.3B | Best quality |
| `musicgen-melody` | 1.5B | Melody conditioning |
| `musicgen-stereo-medium` | 1.5B | Stereo output |
| `musicgen-style` | 1.5B | Style transfer |
| `audiogen-medium` | 1.5B | Sound effects |

## Key Generation Parameters

| Parameter | Default | Effect |
|-----------|---------|--------|
| `duration` | 8.0s | Length (1–30s) |
| `top_k` | 250 | Diversity |
| `temperature` | 1.0 | Creativity |
| `cfg_coef` | 3.0 | Text adherence |

## GPU Memory Requirements

| Model | FP32 | FP16 |
|-------|------|------|
| small | ~4GB | ~2GB |
| medium | ~8GB | ~4GB |
| large | ~16GB | ~8GB |

## Sound Effects (AudioGen)

```python
from audiocraft.models import AudioGen
model = AudioGen.get_pretrained('facebook/audiogen-medium')
model.set_generation_params(duration=5)
wav = model.generate(["thunderstorm with rain and lightning"])
torchaudio.save("sound.wav", wav[0].cpu(), sample_rate=16000)
```

## Prompt Engineering Tips

Structure: `[mood] [genre] with [instruments] at [tempo/style]`

Good: `"upbeat electronic dance music with synthesizer leads and punchy drums at 128 bpm"`
Bad: `"nice music"`

## Common Issues

| Issue | Fix |
|-------|-----|
| CUDA OOM | Use smaller model, reduce duration |
| Poor quality | Increase cfg_coef, better prompts |
| FFmpeg missing | `sudo apt-get install ffmpeg` |
| Sample rate wrong | MusicGen=32kHz, AudioGen=16kHz |

For detailed troubleshooting see `references/audiocraft/troubleshooting.md`.
For fine-tuning, deployment, and advanced patterns see `references/audiocraft/advanced-usage.md`.

## Resources
- GitHub: https://github.com/facebookresearch/audiocraft
- Paper: https://arxiv.org/abs/2306.05284
- HuggingFace: https://huggingface.co/facebook/musicgen-small
