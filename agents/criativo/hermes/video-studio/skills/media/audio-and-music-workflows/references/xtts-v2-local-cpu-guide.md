# Coqui XTTS-v2 Local CPU Deployment & Python Compatibility Guide

This reference documents the exact implementation details, critical patches, and pitfalls encountered when running Coqui XTTS-v2 zero-shot voice cloning fully local on modern Linux / CPU environments (PyTorch 2.6+, Python 3.11, Ryzen 5 5600G).

---

## 1. Environment & Dependency Pinning

Coqui TTS (`TTS==0.22.0`) depends on specific legacy behaviors in PyTorch, Torchaudio, and Hugging Face Transformers.

```bash
# Recommended installation via uv inside isolated venv (.venv-xtts)
uv venv .venv-xtts --python python3.11
uv pip install --python .venv-xtts/bin/python TTS torch torchaudio soundfile psutil --extra-index-url https://download.pytorch.org/whl/cpu

# CRITICAL PIN 1: Transformers compatibility
# Transformers >= 4.44.0 removed BeamSearchScorer from top-level transformers namespace
uv pip install --python .venv-xtts/bin/python "transformers>=4.33.0,<4.44.0"
```

---

## 2. Mandatory Runtime Patches in Python

When executing XTTS-v2 under modern PyTorch versions (PyTorch 2.6+):

### Patch A: PyTorch 2.6+ `weights_only=True` Default
PyTorch 2.6+ changed `torch.load` default to `weights_only=True`, which breaks unpickling of Coqui checkpoint configurations (`XttsConfig` unpickler error).

### Patch B: Torchaudio / TorchCodec Missing Dependency
Modern `torchaudio.load()` defaults to `load_with_torchcodec`, raising `ModuleNotFoundError: No module named 'torchcodec'`. Monkey-patching `torchaudio.load` using `soundfile` avoids installing heavy non-standard build dependencies.

### Standard Script Boilerplate (`clone_voice_xtts.py`):
```python
#!/usr/bin/env python3
import os
import sys
import psutil
import soundfile as sf
import torch
import torchaudio

os.environ["COQUI_TOS_AGREED"] = "1"

# 1. Patch torch.load for Coqui checkpoints
_orig_torch_load = torch.load
def _patched_torch_load(*args, **kwargs):
    if "weights_only" not in kwargs:
        kwargs["weights_only"] = False
    return _orig_torch_load(*args, **kwargs)
torch.load = _patched_torch_load

# 2. Patch torchaudio.load to use soundfile
def _patched_torchaudio_load(filepath, *args, **kwargs):
    data, sr = sf.read(str(filepath))
    tensor = torch.from_numpy(data).float()
    if tensor.ndim == 1:
        tensor = tensor.unsqueeze(0)
    else:
        tensor = tensor.transpose(0, 1)
    return tensor, sr

torchaudio.load = _patched_torchaudio_load

from TTS.api import TTS

def synthesize(text: str, reference_wav: str, output_wav: str, language: str = "pt", threads: int = 12):
    torch.set_num_threads(threads)
    tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False, gpu=False)
    tts.tts_to_file(
        text=text,
        speaker_wav=reference_wav,
        language=language,
        file_path=output_wav,
        split_sentences=True,
    )
```

---

## 3. Benchmarks on AMD Ryzen 5 5600G (6C / 12T)

- **Model Load Time:** ~12.5s – 13.5s
- **RAM Peak:** ~2.8 GB – 3.0 GB (extremely light footprint on 62 GB systems)
- **Real-Time Factor (RTF):** ~5.7x to 6.4x on CPU (e.g. 13s of audio synthesizes in ~81s)
- **Inteligibility Audit:** 100% transcript recovery via `faster-whisper` (`small` / `int8` CPU).
