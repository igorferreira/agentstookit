# Short-form video: audio + on-screen text

Use this when a Reel, TikTok, X clip, or similar short video contains both spoken instructions and progressive text/formulas.

## Validated workflow

1. Preserve the downloaded original and probe it with `ffprobe` (duration, codecs, dimensions, size).
2. Transcribe audio with forced language and domain vocabulary. For nutrition clips, an effective narrow prompt is: `calorias, proteína, gordura, fibras, carboidratos, déficit calórico`.
3. Extract frames at a fixed cadence. For a clip around one minute, start at one frame every 2 seconds.
4. Run OCR only as a locator. Stylized captions, outlines, moving subjects, and compressed video often produce nonsense even when the text is visually obvious.
5. Build chronological contact sheets (for example, 8 frames each) and inspect them visually. This is the reliable layer for progressive numbered lists and formulas.
6. Cross-check every visible number against the audio transcript. Keep these layers separate in the output:
   - literal revised transcript;
   - exact on-screen text/formula;
   - personalized or derived calculation.
7. Preserve discrepancies. Example: the spoken rule may yield 54 g while the screen rounds to 50 g; report both instead of silently choosing one.
8. For health content, treat social-media formulas as educational references, not prescriptions. Compare against basal metabolism, activity level, existing plan, clinical context, and minimum protein/fiber targets before adopting.
9. Generate a separate WhatsApp derivative when requested and record technical metadata plus SHA-256 for original and derivative.

## Instagram retrieval boundary

This reference starts after a valid MP4 exists. Retrieval logic belongs to the social/video download skill. As of the validated September 2026 flow, Instagram embed helpers can vary response by User-Agent; always verify the downloaded payload with `file` and `ffprobe` before assuming an `.mp4` extension means media.
