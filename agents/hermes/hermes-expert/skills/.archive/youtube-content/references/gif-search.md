# GIF Search via Tenor API

Search and download GIFs from Tenor using curl. No extra tools — just curl + jq + `TENOR_API_KEY`.

## Setup

```bash
# Get free API key at https://developers.google.com/tenor/guides/quickstart
# Add to ~/.hermes/.env:
TENOR_API_KEY=your_key_here
```

## Search and Fetch

```bash
# Get GIF URLs from search
curl -s "https://tenor.googleapis.com/v2/search?q=thumbs+up&limit=5&key=${TENOR_API_KEY}" | jq -r '.results[].media_formats.gif.url'

# Small/preview versions
curl -s "https://tenor.googleapis.com/v2/search?q=celebration&limit=3&key=${TENOR_API_KEY}" | jq -r '.results[].media_formats.tinygif.url'

# Download top result
URL=$(curl -s "https://tenor.googleapis.com/v2/search?q=celebration&limit=1&key=${TENOR_API_KEY}" | jq -r '.results[0].media_formats.gif.url')
curl -sL "$URL" -o celebration.gif

# Full metadata
curl -s "https://tenor.googleapis.com/v2/search?q=cat&limit=3&key=${TENOR_API_KEY}" | jq '.results[] | {title: .title, url: .media_formats.gif.url, preview: .media_formats.tinygif.url}'
```

## API Parameters

| Parameter | Description |
|-----------|-------------|
| `q` | Search query (URL-encode spaces as `+`) |
| `limit` | Max results (1–50, default 20) |
| `key` | API key from `$TENOR_API_KEY` |
| `media_filter` | Filter: `gif`, `tinygif`, `mp4`, `tinymp4`, `webm` |
| `contentfilter` | Safety: `off`, `low`, `medium`, `high` |
| `locale` | Language: `en_US`, `es`, `fr`, etc. |

## Media Formats

| Format | Use case |
|--------|----------|
| `gif` | Full quality GIF |
| `tinygif` | Small preview GIF |
| `mp4` | Smaller file size video |
| `nanogif` | Tiny thumbnail |

## Notes
- `tinygif` URLs are lighter weight for chat delivery
- GIF URLs work directly in markdown: `![alt](url)`
- Requires: `TENOR_API_KEY`, `curl`, `jq`
