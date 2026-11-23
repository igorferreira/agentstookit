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

## Fallback routes when fxtwitter fails (validated 2026-09-28)

1. **Twitter syndication JSON** (no login, no key): `https://cdn.syndication.twimg.com/tweet-result?id=<id>&lang=pt&token=a` — returns `text`, author, and `mediaDetails[].video_info.variants[]` with direct mp4/m3u8 URLs. Single tweet only, not replies.
2. **nitter.tiekoetter.com** via curl + browser UA returns 200. Even behind its Anubis anti-bot interstitial, the page's `og:description` meta carries the FULL tweet/thread text — regex the meta content (`content="(.*?)"`), never read the page body.

Direct `curl` of video.twimg.com mp4 URLs returns 0 bytes (CDN needs session): download the m3u8 playlist URL from the syndication JSON instead — `yt-dlp -f "<video-format-id>+<audio-format-id>" --merge-output-format mp4 <m3u8-url>` (list formats first with --list-formats).

## Limits

- Public tweets only (no protected accounts).
- Threads = one API call per status ID (each reply is its own status).
- No engagement counts (views/likes not exposed reliably).
- If fxtwitter is down: instance lists at status.dutton.dev, then paid fallback (ScrapeCreators/Apify).

## What does NOT work (validated 2026-09-06 — do not waste attempts)

| Route | Result |
|---|---|
| nitter.net | HTTP 200 but empty page shell (~12 KB) without session |
| xcancel.com | service suspended (legal proceedings), not a Cloudflare issue |
| threadreaderapp.com | redirects to /authenticate — login wall for unrolls |
| r.jina.ai proxy | Cloudflare turnstile checkbox that automation cannot pass |
| nitter.poast.org / nitter.privacydev.net | DNS failure |
| nitter.space / lightbrd.com | 403 |
| x.com direct (curl or logged-out browser) | 403 denied |
| nitter.net | connection refused |

**Conclusion:** most public Nitter mirrors are dead or gated. Order: fxtwitter → syndication JSON → nitter.tiekoetter.com (via og:description).

## Workflow for the user's context (Usuário)

When Usuário sends an X link for the study archive:
1. For a full post archive (the default in the dedicated X-study thread), follow `extrair-posts-x` for the artifact destination, Markdown, thematic folder, and central index. This skill supplies the retrieval/API and fallback methods; it must not override the specialized archive workflow or an explicit destination Usuário names.
2. Use `~/MEGA/Documentos/educacao_leitura/filmes_aulas_ia/videos/` for a media-only save, unless Usuário specifies another destination; do not route a full post archive there merely because it contains video.
3. Fetch replies one API call per status ID only when the full thread is requested or needed to satisfy the task.

## Relation to social-fetch skill

Detailed per-platform strategy chains live in the `social-fetch` skill (references/strategies.md). That skill's older chain marks X as "low reliability free" and leans on Nitter — this skill supersedes it for X with the validated fxtwitter route. If social-fetch becomes editable, fold this content into its references/strategies.md and retire this skill.
