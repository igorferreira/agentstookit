---
name: x-twitter-fetch
description: "Use when fetching X/Twitter tweets or media by URL."
---

# X/Twitter fetch — free route via fxtwitter API

## The route (validated 2026-09-06)

```
https://api.fxtwitter.com/<user>/status/<id>
```

- Public, free, no key, no login.
- Returns JSON: `tweet.text` (full body), `tweet.author`, `tweet.media.all[]` (direct MP4/JPG URLs on video.twimg.com / pbs.twimg.com), `tweet.replies` count.
- Command: `curl -s "https://api.fxtwitter.com/hanakoxbt/status/2096364160166621318"`

## Media download

```bash
# Get media URL from the JSON payload, then:
curl -sL -A "Mozilla/5.0" "<video.twimg.com url>" -o video.mp4
```

- If the CDN 404s, re-fetch the payload first: the URL carries a `?tag=` version param that changes between payload fetches. Using a stale URL is the most common failure.
- Always pass a browser User-Agent.

## Limits

- Public tweets only (no protected accounts).
- Threads = one API call per status ID (each reply is its own status).
- No engagement counts (views/likes not exposed reliably).
- If fxtwitter is down: instance lists at status.dutton.dev, then paid fallback (ScrapeCreators/Apify).

## What does NOT work (validated 2026-09-06 — do not waste attempts)

| Route | Result |
|---|---|
| nitter.net | HTTP 200 but empty page shell (~12 KB) without session |
| xcancel.com | Cloudflare challenge ("Just a moment...") |
| nitter.poast.org / nitter.privacydev.net | DNS failure |
| nitter.space | 403 |
| x.com direct via curl | login wall, no text |

**Conclusion:** the era of public Nitter mirrors is over. Go fxtwitter first, always.

## Workflow for the user's context (Igor)

When Igor sends an X link for the study archive:
1. Extract via fxtwitter API.
2. If media: download video/images to `~/MEGA/Documentos/educacao_leitura/filmes_aulas_ia/videos/` named `AAAA-MM-DD_<AUTOR>-TEMA.mp4`.
3. Append summary + link + status to `~/MEGA/Documentos/educacao_leitura/filmes_aulas_ia/INDEX.md`.
4. If the full thread matters, fetch replies one call per status ID.

## Relation to social-fetch skill

Detailed per-platform strategy chains live in the `social-fetch` skill (references/strategies.md). That skill's older chain marks X as "low reliability free" and leans on Nitter — this skill supersedes it for X with the validated fxtwitter route. If social-fetch becomes editable, fold this content into its references/strategies.md and retire this skill.
