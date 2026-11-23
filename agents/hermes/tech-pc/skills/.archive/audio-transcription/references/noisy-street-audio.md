# Noisy Street Audio with Slang — Playbook

Lessons from transcribing WhatsApp/Telegram voice messages recorded outdoors (street, parties, boca de fumo) with heavy slang and drug-context vocabulary.

## When to use this playbook

- Audio recorded outdoors (wind, traffic, music, voices in background)
- Speaker using gírias (street slang, drug terms, regional expressions)
- Auto-transcript from gateway is garbled or nonsensical
- Consequential content (relationship, legal, safety)

## Strategy

### 1. Progressive model escalation

Base model is often insufficient for noisy street audio. Plan for two passes:

```python
# Pass 1: base (fast, cheap)
model = WhisperModel("base", device="cpu", compute_type="int8")

# Pass 2: small (significantly better for noisy Portuguese)
model = WhisperModel("small", device="cpu", compute_type="int8")
```

For critical phrases (names, amounts, accusations), use `word_timestamps=True` and check `word.probability`. Words below 0.4 should be flagged as `[incerto]`.

### 2. Domain vocabulary priming

`initial_prompt` with domain terms helps the model disambiguate:

```python
initial_prompt="flor, maconha, beck, boca, Uber, moto, táxi, rua"
```

List likely terms but do NOT script full sentences — that biases the model toward hearing what you expect.

### 3. Confidence checking

After transcription, flag segments with low-confidence words:

```python
for seg in segments:
    if seg.words:
        low_conf = [(w.word, round(w.probability, 2)) for w in seg.words if w.probability < 0.4]
        if low_conf:
            print(f"  ⚠️ Baixa confiança: {low_conf}")
```

### 4. Context interpretation

When the audio is too degraded for reliable transcription, combine:
- What the model heard (even garbled)
- The conversation context (what was said before/after)
- The speaker's known patterns

Always label interpretation as interpretation: "Provavelmente: ..."

## Known slang (Igor/Adrielly context)

| Term | Meaning |
|---|---|
| flor 🌿 | Maconha |
| beck / beque | Cigarro de maconha |
| copão | Cerveja grande / drink |
| onda | Efeito/brisa de droga |
| boca / boca de fumo | Ponto de venda de drogas |
| CDD | Cidade de Deus (favela no Rio) |
| moto táxi | Transporte informal por moto |
