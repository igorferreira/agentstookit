---
name: agente-video-transcricao
description: Use for audiovisual transcription.
---
# Transcrição

Use faster-whisper, preserve a transcrição bruta e faça segunda passagem para nomes, números, marcas e termos técnicos. Gere timestamps, capítulos e incertezas.

## Procedimento validado

1. Extrair áudio (16 kHz mono, WAV) — o modelo aceita direto, sem passada extra:

```bash
ffmpeg -y -v error -i video.mp4 -vn -ac 1 -ar 16000 /tmp/audio.wav
```

2. Transcrever com faster-whisper (disponível no python do Hermes e no venv hermes-agent): `WhisperModel("small", device="cpu", compute_type="int8")`, `transcribe(path, language="pt")`; reel ~50s roda em ~25s. Formato por segmento: `[<start>-<end>] <texto>` com 1 casa decimal.
3. Gravar a transcrição BRUTA em arquivo (`/tmp/..._transcricao_raw.txt`) antes de revisar — a revisão (passada 2) corrige nomes, números, marcas e termos técnicos SEM alterar o que foi falado ("Cloud Code" do reel = Claude Code; corrigir com nota, não apagar).
4. Anexar a transcrição ao MD de metadata do post quando existir (regra do snapinsta-downloader: o .md fica junto do vídeo).

## Saída
Transcript raw, transcript revisado, termos incertos e timestamps.

## Limites
Não invente falas, não transforme alegação em fato e preserve o original.