---
name: audio-and-music-workflows
description: "Use when composing songs, engineering prompts for AI music systems, generating music or sound, or analyzing audio with spectrograms and feature views. Route between creative direction, generation engines, and technical analysis."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [audio, music, songwriting, generation, spectrogram, analysis]
---

# Audio and Music Workflows

## Overview

This umbrella covers the lifecycle from song concept and lyrics through AI-generation prompts to technical inspection of rendered audio.

## Workflow Router

- **Song structure, lyrics, rhyme, meter, emotional arc, parody, and Suno-style prompt engineering:** read `references/songwriting-and-ai-music.md`.
- **Spectrograms and audio features such as mel, chroma, and MFCC:** read `references/songsee.md`.
- **Local MusicGen/AudioGen generation (Meta AudioCraft):** read `references/audiocraft.md`; advanced usage and fine-tuning in `references/audiocraft/advanced-usage.md`; troubleshooting in `references/audiocraft/troubleshooting.md`.
- **Text-to-Speech (TTS) & Voice Cloning (Piper, NeuTTS, ElevenLabs):** read `references/tts-voice-cloning-workflow.md` — covers Piper TTS pt-BR local setup, reference audio slicing/transcription, and local few-shot voice cloning vs ElevenLabs.
- **Coqui XTTS-v2 Local CPU Deployment:** read `references/xtts-v2-local-cpu-guide.md` — implementation guide, dependency pinning (`transformers<4.44.0`), PyTorch 2.6+ `weights_only` patch, and torchaudio `soundfile` fallback for CPU cloning.
- **HeartMuLa (open-source Suno alternative):** read `references/heartmula.md` — covers installation, required source patches, model download, and generation commands.

## Integrated Workflow

1. Define purpose, genre, emotional arc, structure, duration, and vocal/instrumental constraints.
2. Draft lyrics and generation metadata separately so each can be iterated.
3. Render with the selected engine and retain the exact prompt, model, seed, and settings where available.
4. Listen to the artifact and inspect technical features when diagnosis or comparison is needed.
5. Iterate one variable at a time and preserve the best artifact rather than overwriting it.

## Verification Checklist

- [ ] Creative brief and delivery format are explicit
- [ ] Prompt/lyrics fit the selected engine
- [ ] Audio artifact was generated or analyzed with real tool output
- [ ] Final file opens and duration/sample characteristics are plausible
