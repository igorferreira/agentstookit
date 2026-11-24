---
name: public-preview
description: "Spin up a quick public URL for any static web app with working social media previews — Cloudflare tunnel, OG tag patching, and container hot-update."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [deployment, demo, social-previews, cloudflare, docker, og-tags]
---

# Quick Public Preview

Spin up a publicly-accessible URL for any local static web build with working social media link previews (WhatsApp, Telegram, etc.). Three-step pipeline: provision tunnel → update OG metadata → validate. For Dockerised frontends, hot-inject via `docker cp` to avoid rebuild downtime.

## Prerequisites

Check tool availability before starting:

```bash
which cloudflared   # quick-tunnel method (preferred, no login required)
which ngrok         # fallback if cloudflared unavailable
pgrep -af 'docker'  # containers running
ss -tlnp | grep ':90[89][0-9]'  # expected frontend ports
```

If neither tunnel binary is available, suggest:
- Cloudflare: `sudo apt install cloudflared` (Linux) or `brew install cloudflare/cloudflared/cloudflared` (macOS)
- Ngrok: download from ngrok.com/dashboard

## Step 1: Verify the local build

Confirm the static output directory exists and serves HTTP 200 locally:

```bash
curl -s -o /dev/null -w '%{http_code}' http://localhost:<port>/
```

If running inside Docker:

```bash
docker ps --filter name=<container-name>
docker exec <container> cat /etc/nginx/conf.d/default.conf  # verify root path
```

**GOTCHA:** Containers may serve from different root paths depending on how NGINX is configured (`/usr/share/nginx/html/`, `/var/www/html/`, etc.). Always verify with `docker exec <container> find '/usr/share/nginx' -name index.html` or the actual nginx config.

## Step 2: Patch OG metadata (if needed)

Before exposing the URL, ensure every `index.html` carries Open Graph + Twitter Card meta tags pointing to consistent `og:image` assets.

### Bulk-patch all HTML files

Use a Python script or `sed` to replace any existing base URL with the new public URL:

```python
import re, pathlib

old_base = "https://SEU-TUNNEL.ngrok-free.app"
new_base = "https://the-new-url.trycloudflare.com"
dist_root = pathlib.Path("apps/web/dist")

for html in dist_root.rglob("index.html"):
    text = html.read_text()
    # Replace old domain in all og/twitter meta tags
    text = re.sub(r'https://[^"\']+\.(?:ngrok|trycloudflare)\.com', new_base, text)
    # Ensure og:image points to correct asset
    text = re.sub(r'og:image.*?content="[^"]*/og/[^"]*\.png"', f'og:image content="{new_base}/og/morador.png"', text)
    text = re.sub(r'twitter:image.*?content="[^"]*/og/[^"]*\.png"', f'twitter:image content="{new_base}/og/morador.png"', text)
    html.write_text(text)
```

**Rules for OG image paths:**
- One canonical image per page type: `/og/morador.png`, `/og/admin.png`, etc.
- Serve images at the exact same path prefix as referenced in meta tags.
- Images must respond to HTTP GET returning 200 + valid PNG/JPG body > 1 KB.

### Validate OG tags post-patch

```bash
page=$(curl -s https://your-public-url/)
echo "$page" | grep -E '(og:title|og:description|og:image|twitter:card|twitter:image)'
```

Every page type served by your app should have `og:title`, `og:description`, and `og:image` populated.

## Step 3: Provision the tunnel

### Cloudflare (preferred — free, no account needed)

```bash
cloudflared tunnel --url http://localhost:<port> > /tmp/cloudflare_tunnel.log 2>&1 &
sleep 10
cat /tmp/cloudflare_tunnel.log | head -5  # first line contains the URL
```

The first line output looks like:
```
$Your tunnel token expires: ...
Your quick tunnel: https://abc-def-xyz.trycloudflare.com
```

Save it immediately:

```bash
grep '^Your quick tunnel:' /tmp/cloudflare_tunnel.log | awk '{print $4}' > .CLOUDFLARE_URL.txt
```

### Ngrok (fallback)

```bash
ngrok http http://localhost:<port> --log=/tmp/ngrok.log &
sleep 5
grep 'forwarding' /tmp/ngrok.log | sed -n 's|.*https://\([^ ]*\).*|\1|p'
```

**GOTCHA — CSP blocking inline scripts:** Quick tunnels (both Cloudflare and ngrok) apply Content Security Policy headers that **block `<script>` with `inline`**. Never embed data via `<script>window.X='...'</script>` or `data-*` attributes set via JS. Pass parameters via HTML attributes or query strings instead. If you hit blank pages, inspect browser devtools — CSP violations are the usual cause.

### Tunnel lifecycle

- **Quick tunnels expire** after ~24h or on process termination. They are suitable for demos, not production.
- Save the URL in version control (e.g., `.gitignore` the file, but share it explicitly).
- To keep the tunnel alive, either start it via `nohup` or run it in a `tmux` session.
- If the tunnel dies (user sees 404 via public URL but localhost still works): restart the tunnel process and update the saved URL everywhere.

## Step 4: Hot-inject into running containers (Docker)

If the frontend runs behind Docker/Nginx, patch the source files then copy them in — **no rebuild needed**.

1. Discover the real paths inside the container:

```bash
docker ps --format '{{.ID}} {{.Names}}'
docker exec <container-id> find '/usr/share/nginx/html/' -name index.html
```

2. Copy each patched file into the container:

```bash
docker cp apps/web/dist/index.html <container-id>:/usr/share/nginx/html/index.html
docker cp apps/web/dist/entrar/index.html <container-id>:/usr/share/nginx/html/entrar/index.html
docker cp apps/web/dist/admin/index.html <container-id>:/usr/share/nginx/html/admin/index.html
```

**GOTCHA — Container ID stability:** Use the full container ID from `docker ps`, not the name. Names can change between compose cycles. The short ID is usually sufficient.

**GOTCHA — Multiple subdirectories:** A single-page app often generates separate `index.html` files per route (`/entrar`, `/cadastro`, `/admin`). Every one of them needs OG tags patched and copied. Missing even one will break social previews for that route.

## Step 5: End-to-end validation

Verify both tunnel reachability AND OG completeness:

```bash
TUNNEL_URL="$(cat .CLOUDFLARE_URL.txt)"

# Check main page + OG presence
curl -s "$TUNNEL_URL/" | grep -c 'og:image'
curl -s "$TUNNEL_URL/entrar" | grep -c 'og:image'
curl -s "$TUNNEL_URL/admin" | grep -c 'og:image'

# Check image assets return 200
for img in /og/morador.png /og/admin.png; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "${TUNNEL_URL}${img}")
  echo "${img} → ${code}"
done
```

If any route returns 0 matches for `og:image`, that page is missing metadata. Re-patch and re-copy.

## Common pitfalls

| Pitfall | Mechanism | Fix |
|---------|-----------|-----|
| CSP blocks JS that sets meta tags | Tunnel proxy adds strict CSP header | Put all meta tags as static HTML, never generated by client-side JS |
| `docker cp` fails silently | Wrong target path inside container vs actual NGINX root | Run `docker exec <id> find` BEFORE copying; always match the nginx config's `root` directive |
| Old ngrok URL persists in some HTMLs | Regex only matched known domain string | Search for ALL `ngrok`, `trycloudflare`, and `loca.lt` patterns; bulk-check with `grep -rl 'ngrok' dist/` |
| Social preview shows blank/stale | Caches on WhatsApp/Telegram cache for hours | Use their debug tools: `https://developers.facebook.com/tools/debug/` (Facebook), paste the URL directly into WhatsApp to force refresh |
| `cloudflared` exits immediately | Port not reachable from host (firewall/container network) | Verify with `curl http://localhost:<port>` first; use port mapping flags: `--url http://host.docker.internal:<port>` |

## Reference files

See the `references/` directory for detailed guides:

- `references/cloudflare-quick-tunnel.md` — Full cloudflared quick-tunnel workflow, auth tunnels, and credential management
- `references/og-tag-template.md` — Canonical OG + Twitter Card meta tag template for web pages
- `references/docker-hot-update.md` — Docker `cp` injection patterns, NGINX config discovery, and reload strategies
