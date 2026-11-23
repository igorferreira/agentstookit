---
name: spa-content-extraction
description: "Use when a SPA page yields little text; mine its JS bundles."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Research, Scraping, SPA, JavaScript, Vite, React, Content]
    related_skills: [blocked-page-recovery]
---

# SPA Content Extraction (JS bundle disassembly)

When the target isn't blocked but is a **React/Vite SPA whose HTML shell is nearly empty**
(`web_extract` returns ~500 chars, plain-text scraping yields only the hero), the content lives
in the JS chunks. No browser needed — download and mine the bundles.

**Validated case (2026-09-04):** `workshop-ia.techleads.club/v3` — React + Vite + lazy routes.
Full curriculum (7 módulos), 7 speaker bios, FAQ, and bonus-material lists recovered from JS alone.
Bios cross-checked via `web_search` (LinkedIn).

## Ladder for SPAs (before reaching for a real browser)

1. `curl -sL <url> -A "<real UA>" -o page.html` — check byte size vs text yield.
   20-30 KB HTML but <1 KB of visible text ⇒ SPA shell.
2. **Find the chunk list.** Vite injects a loader script near `</body>` containing
   `\u003clink rel=modulepreload href=/assets/<Name>-<hash>.js` entries; also grep the main
   bundle for `assets/[A-Za-z0-9_-]*\.js` and `__vite__mapDeps`.
3. **Download the promising chunks.** Heuristics for which hold content:
   - Names matching page sections: `*Section*.js`, `*Speakers*.js`, `*Content*.js`
   - The largest chunks (hero-only bundles are ~15 KB; content chunks 20-40 KB)
   - Route-named bundles (`V3-*.js`, `Index-*.js`) usually only render shells
4. **Extract readable strings** from each chunk (snippet below).
5. **Filter aggressively:** first pass will include carousel/engine libs (Embla etc.) that
   ship inside page chunks — re-filter per-file with stricter stop-patterns.
6. **Structured fields survive minification verbatim** — recover tables with
   `re.finditer(r'(name|title|role|company):\s*"([^"]+)"')`.
7. **Cross-check names with web_search** for bios/verifications (LinkedIn, GitHub, imprensa).

## String-extraction snippet

```python
import re
raw = open(f, encoding="utf-8", errors="ignore").read()
strs = re.findall(r'"((?:[^"\\]|\\.){15,900})"', raw)
for s in strs:
    t = s.encode().decode("unicode_escape", errors="ignore")
    # keep pt-BR-looking text with real words:
    if re.search(r'\b(de|da|do|para|com|que|como|em|um|uma|os|as|no|na|por)\b', t) \
       and not re.search(r'[{};()]', t) \
       and not re.search(r'(className|flex |grid |px-|py-|assets/|http)', t):
        print(t)
```

## Pitfalls

- **Carousel/engine libs ride along** (e.g. Embla) and dump thousands of garbage strings
  (`function wt(e,t,n,r)...`). Filter per-file, not globally: engine code lives in a
  different chunk than the content.
- **unicode_escape decoding mangles UTF-8 accents** — character-class ranges like `Ã-Ã¿`
  crash `re`. Always use `\u00e0-\u00ff` escapes, never literal accented chars, in filter regexes.
- **Some strings are template fragments** (`` `Garantir por apenas R$${r.whole}` ``) — keep
  them; they reveal copy variables useful for landing-page teardowns.
- **Chunk graph is two levels deep:** content chunks import other content chunks
  (`WorkshopSection` → `workshopSpeakers`). Grep each downloaded chunk for more
  `assets/*.js` refs and fetch those too.
- **Don't bother with Wayback for SPAs** — snapshots don't render JS; you get the same
  empty shell. Go straight to bundle disassembly.

## When bundles still aren't enough

If content is fetched from an API at runtime (fetch/axios to `/api/...`), disassembling
JS won't show the data — only the endpoint. Grep bundles for `fetch(` / `axios` / URL
literals and hit those endpoints directly with curl (usually JSON, no WAF).

## Provenance

Strings recovered this way come from the live site's own assets ⇒ provenance `live`.
Note the extraction date; promo/landing pages change (prices, "inscrições encerradas").

## Related
- `blocked-page-recovery` (separate skill) — for genuinely blocked pages (WAF/paywall),
  not SPAs. Its `scripts/recover_page.py` handles 403/WAF/paywall ladders.
