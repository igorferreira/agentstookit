# Text-to-Speech (TTS) & Voice Cloning Workflow

This reference documents proven patterns, setup steps, and pitfalls for TTS configuration and voice cloning under Hermes Agent.

## 1. Piper TTS (Local, Free, pt-BR)

Hermes supports Piper TTS natively for zero-cost, on-device text-to-speech.

### Installation & Voice Setup
```bash
# 1. Install piper-tts in the runtime environment
uv pip install piper-tts

# 2. Download high quality pt-BR voices
python3 -c "
from pathlib import Path
import piper.download_voices as pdv
dest = Path('~/.hermes/cache/piper-voices').expanduser()
dest.mkdir(parents=True, exist_ok=True)
pdv.download_voice('pt_BR-faber-medium', dest)
pdv.download_voice('pt_BR-cadu-medium', dest)
"

# 3. Configure Hermes config.yaml
hermes config set tts.provider piper
hermes config set tts.piper.voice pt_BR-faber-medium
hermes config set tts.edge.voice pt-BR-AntonioNeural
```

---

## 2. Voice Sample Preparation for Cloning

When preparing voice samples from voice messages or audio clips:

### Extraction & Formatting
1. Convert input audio to 24 kHz Mono 16-bit PCM WAV:
   ```bash
   ffmpeg -y -i input.ogg -ar 24000 -ac 1 ~/.hermes/voice_clone/ref_sample.wav
   ```
2. Generate exact phonetic transcription via `faster-whisper`:
   ```python
   from faster_whisper import WhisperModel
   model = WhisperModel('small', device='cpu', compute_type='int8')
   segments, _ = model.transcribe('~/.hermes/voice_clone/ref_sample.wav', language='pt')
   text = ' '.join([s.text.strip() for s in segments]).strip()
   Path('~/.hermes/voice_clone/ref_sample.txt').write_text(text, encoding='utf-8')
   ```

### Audio Quality & Acoustic Analysis
- **SNR (Signal-to-Noise Ratio):** Calculate frame-level energy and noise floor using `soundfile` and `numpy`.
- **Pure Reference (>20 dB SNR without background reverberation):** Best for fundamental timbre extraction.
- **Dynamic Conversational Sample:** Useful for natural cadence and prosody.
- **ElevenLabs Best Practice:** Combine a clean, isolated studio/home sample (20–30s) with a conversational sample (30–60s) for optimal timbre and naturalness.

---

## 3. Local Voice Cloning Engines Evaluation for PT-BR (CPU Only / Ryzen 5600G)

When deploying fully local, zero-cost, private voice cloning in environments without NVIDIA GPUs:

### Engine Comparison Matrix
1. **Chatterbox Multilingual (`ChatterboxMultilingualTTS`):**
   - *Limitation:* Trained predominantly on English; PT-BR support has strong robotic/anglo accent artifacts and poor capture of low/warm vocal formants. Not recommended when high speaker similarity is required.
2. **XTTS-v2 (`coqui-tts` / `TTS`):**
   - *Best Balance for CPU:* Outstanding native zero-shot cloning in PT-BR, capturing natural prosody, breathing, and accent/cadence.
   - *Performance on Ryzen 5 5600G (6C/12T):* Stable execution (~15–35s generation for 5–10s audio), ~4–8 GB RAM.
   - *Critical Dependency Constraint:* Coqui TTS imports `BeamSearchScorer` from `transformers`. In newer `transformers>=4.44.0` (and `5.x`), this class was removed/relocated, throwing `ImportError: cannot import name 'BeamSearchScorer' from 'transformers'`. Always pin:
     ```bash
     uv pip install "transformers>=4.33.0,<4.44.0"
     ```
3. **F5-TTS (Diffusion-based):**
   - *Limitation on CPU:* Diffusion step solver is too compute-intensive for CPU-only (takes minutes per short sentence). Requires CUDA/GPU for viable throughput.
4. **OpenVoice v2:**
   - Fast on CPU, but acts as a tone-color converter on top of a base TTS; retains the mechanical cadence of the base model.

### Biometric Privacy & Deployment Protocol
- **Strict Isolation:** Store biometric voice samples in directories with `0700` permissions and files with `0600` (`chmod 700 <dir>`, `chmod 600 <file>`).
- **Non-Destructive Backups:** Always backup existing voice setup (`local-voice/`) before migrating models.
- **Explicit User Consent:** Never enable automated voice synthesis in chat/messaging gateways without explicit user approval of the quality and triggering rules.
- **Intelligibility Validation:** Validate synthesized audio by passing it through local `faster-whisper` (WER/transcription check) and export in both 24 kHz WAV PCM and OGG/Opus (48 kHz / 48 kbps).

---

## 4. Local Neural Cloning (NeuTTS / Hugging Face Gated Models)

### NeuTTS Setup Requirements
- Packages: `neutts[all]`, `torch`, `torchaudio`, `llama-cpp-python`, `torchao<0.8.0`.
- System dependency: `espeak-ng`.
- **Hugging Face Gated Model Pitfall:**
  - Repositories like `neuphonic/neutts-air-q4-gguf` require manual web approval on Hugging Face.
  - Fine-grained tokens must explicitly have global read permissions or be classic Read/Write tokens, otherwise downloading the GGUF backbone fails with HTTP 401/403.
