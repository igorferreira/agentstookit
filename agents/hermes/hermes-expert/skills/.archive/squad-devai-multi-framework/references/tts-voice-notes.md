# TTS voice-note workflow (Telegram)

Used repeatedly this session for messages Igor forwards to contacts (girlfriend, friends, colleagues).

## Pipeline (validated)
1. Write the message text in pt-BR, warm/friendly tone, naming the recipient ("Fala, X! Aqui é o Hermes, assistente de IA do Igor...").
2. Generate WAV with Piper:
   `echo "<text>" | piper --model ~/.hermes/cache/piper-voices/pt_BR-faber-medium.onnx --output_file /tmp/out.wav`
3. Convert to Telegram voice bubble format:
   `ffmpeg -y -i /tmp/out.wav -c:a libopus -b:a 48k ~/.hermes/audio_cache/tts_YYYYMMDD_<slug>.ogg`
4. Deliver with `MEDIA:<absolute .ogg path>` plus the exact transcript in a fenced code block so Igor can copy-paste it into WhatsApp alongside the audio.

## Notes
- Escape quotes/backticks in the text before shell interpolation (use a Python heredoc + subprocess, not raw echo, when the text contains special chars).
- Keep audios under ~60s; split long content.
- Content pattern that works: greeting → who Hermes is → why Igor asked → 3-5 short informative bullets → warm closing call-to-action.
