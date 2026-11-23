# Deleted Audio Forensics — Smoking Gun Pattern

When someone deletes WhatsApp/Telegram voice messages in a live conversation, those deleted audios often contain the **truth they didn't mean to share**. Treat deleted audios as high-priority evidence.

## Pattern

1. **Detect deletion** — User says "ela apagou", "esse áudio sumiu", "ela mandou e apagou"
2. **Find the original** — Locate in `~/.hermes/audio_cache/` by timestamp match with the conversation
3. **Transcribe aggressively** — Use `small` model (not `base`) with `word_timestamps=True` and domain `initial_prompt`. The audio is likely noisy (street, party, emotional state)
4. **Flag every low-confidence word** — Words below 0.4 probability should be flagged for the user
5. **Present as forensic evidence** — Mark clearly: `❌ APAGADO POR ELA/ELE` in the output
6. **Cross-reference with conversation context** — What was said before the deletion? What was said after? The deletion itself is evidence of guilt/regret

## Why it works

People delete audios when they realize they:
- Confessed something (being with someone, using drugs, lying)
- Revealed their true feelings (anger, resentment)
- Showed their hand in a manipulation
- Were recorded without filtering

The act of deletion is an admission that the content is real and damning.

## Presentation format

```
🎙️ [Speaker] | [duration]s | ❌ APAGADO

> "[transcribed text]"

### 🔍 Tradução/Interpretação
[What was really said, decoded from slang/noise]

### Por que apagou
[Analysis of why this specific content triggered deletion]
```

## Real example (Igor/Adrielly, 09/08/2026)

Three deleted audios from Adrielly, in chronological order:

| # | Dur | Conteúdo real | Por que apagou |
|---|---|---|---|
| 1 | 7s | *"Não é isso? Liga aqui pra gente."* — falando COM outro cara, pedindo pra ele entrar na vídeochamada pra "provar" que era só amigo | Provou a encenação premeditada |
| 2 | 37s | *"O mano que eu tava na onda... meu amigo saiu agora aqui... tem uma valora moral"* — confessou que tinha um cara e que se sentia culpada | Se entregou completamente |
| 3 | 16s | *"É um saco ficar provando as coisas pras pessoas"* — revelou raiva e ressentimento | Mostrou o que realmente pensa sobre prestar contas |

The second audio was the "smoking gun" — the confession she never intended to keep.
