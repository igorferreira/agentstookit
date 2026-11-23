# Blogwatcher — RSS/Atom Feed Monitoring

Track blog and RSS/Atom feed updates via `blogwatcher-cli`. Supports auto-discovery, HTML scraping fallback, OPML import, and read/unread tracking.

## Installation (pick one)

```bash
# Go
go install github.com/JulienTant/blogwatcher-cli/cmd/blogwatcher-cli@latest

# Binary (Linux amd64)
curl -sL https://github.com/JulienTant/blogwatcher-cli/releases/latest/download/blogwatcher-cli_linux_amd64.tar.gz | tar xz -C /usr/local/bin blogwatcher-cli

# Binary (macOS Apple Silicon)
curl -sL https://github.com/JulienTant/blogwatcher-cli/releases/latest/download/blogwatcher-cli_darwin_arm64.tar.gz | tar xz -C /usr/local/bin blogwatcher-cli

# Docker (with persistent storage)
docker run --rm -v blogwatcher-cli:/data -e BLOGWATCHER_DB=/data/blogwatcher-cli.db ghcr.io/julientant/blogwatcher-cli scan
```

> **Migrating from original blogwatcher:** `mv ~/.blogwatcher/blogwatcher.db ~/.blogwatcher-cli/blogwatcher-cli.db`

## Managing Feeds

```bash
# Add a blog (auto-discovers RSS/Atom)
blogwatcher-cli add "My Blog" https://example.com

# Add with explicit feed URL
blogwatcher-cli add "My Blog" https://example.com --feed-url https://example.com/feed.xml

# Add with HTML scraping fallback
blogwatcher-cli add "My Blog" https://example.com --scrape-selector "article h2 a"

# List tracked blogs
blogwatcher-cli blogs

# Remove a blog
blogwatcher-cli remove "My Blog" --yes

# Import from OPML (Feedly, Inoreader, NewsBlur export)
blogwatcher-cli import subscriptions.opml
```

## Scanning and Reading

```bash
blogwatcher-cli scan                          # Scan all blogs
blogwatcher-cli scan "My Blog"               # Scan one blog
blogwatcher-cli articles                     # List unread articles
blogwatcher-cli articles --all               # List all articles
blogwatcher-cli articles --blog "My Blog"   # Filter by blog
blogwatcher-cli articles --category "Engineering"
blogwatcher-cli read 1                       # Mark article 1 as read
blogwatcher-cli read-all                     # Mark all read
blogwatcher-cli read-all --blog "My Blog" --yes
```

## Environment Variables

| Variable | Description |
|---|---|
| `BLOGWATCHER_DB` | SQLite database path |
| `BLOGWATCHER_WORKERS` | Concurrent scan workers (default: 8) |
| `BLOGWATCHER_SILENT` | Only output "scan done" |
| `BLOGWATCHER_YES` | Skip confirmation prompts |
| `BLOGWATCHER_CATEGORY` | Default article category filter |

## Notes

- Auto-discovers RSS/Atom from blog homepage when no `--feed-url` given
- Falls back to HTML scraping when `--scrape-selector` is configured
- Database: `~/.blogwatcher-cli/blogwatcher-cli.db` (override with `--db` or `BLOGWATCHER_DB`)

## Resources
- GitHub: https://github.com/JulienTant/blogwatcher-cli
- All releases: https://github.com/JulienTant/blogwatcher-cli/releases
