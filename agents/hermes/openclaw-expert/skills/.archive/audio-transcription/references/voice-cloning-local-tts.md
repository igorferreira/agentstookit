# Local TTS & Zero-Shot Voice Cloning Patterns

This document covers proven local TTS configurations and zero-shot voice cloning workflows discovered under Hermes Agent.

## 1. Piper TTS (Fast, Free, Local pt-BR Engine)

Piper provides lightweight on-device neural TTS with zero token/API cost.

### Configuration
```bash
# Install package
uv pip install piper-tts

# Download pt-BR voices
python3 -c "
from pathlib import Path
import piper.download_voices as pdv
dest = Path('~/.hermes/cache/piper-voices').expanduser()
dest.mkdir(parents=True, exist_ok=True)
pdv.download_voice('pt_BR-faber-medium', dest)
pdv.download_voice('pt_BR-cadu-medium', dest)
"

# Set Hermes provider
hermes config set tts.provider piper
hermes config set tts.piper.voice pt_BR-faber-medium
```

---

## 2. Voice Extraction & Quality Analysis for Cloning

### Step 1: Pre-processing Audio
Extract a 24 kHz Mono 16-bit PCM WAV from incoming voice messages:
```bash
ffmpeg -y -i input.ogg -ar 24000 -ac 1 output.wav
```

### Step 2: Accurate Transcription
Transcribe via `faster-whisper` to provide exact phonetic matching for reference conditioning:
```python
from faster_whisper import WhisperModel
model = WhisperModel('small', device='cpu', compute_type='int8')
segs, _ = model.transcribe('output.wav', language='pt')
text = ' '.join([s.text.strip() for s in segs]).strip()
```

### Step 3: Acoustic Purity & SNR Assessment
Compute RMS and SNR (signal-to-noise ratio) across 50ms frames to determine if an audio is suitable for voice cloning:
- **Clean studio/home audio (SNR > 22 dB):** Ideal for base timbre representation.
- **Ambient/reverberant audio (SNR > 25 dB with background noise):** High dynamic range but has room noise. Best used as an auxiliary sample alongside a clean sample in multi-sample cloning engines (e.g. ElevenLabs).

---

## 3. NeuTTS & Hugging Face Gated Models

- **Requirement:** `torchao<0.8.0`, `llama-cpp-python`, `torchaudio`.
- **Hugging Face Authentication:** Fine-grained tokens must have global read permissions; otherwise gated repositories like `neuphonic/neutts-air-q4-gguf` return `HTTP 401/403` despite user web acceptance.
