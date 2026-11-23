---
name: linkedin-poster
description: Publish a post to the user's personal LinkedIn profile via LinkedIn's official REST API (never via automated browser sessions). Includes a one-time OAuth setup script and a publish script that defaults to a safe dry-run mode. Use when the user has approved final post text (and optionally an image) and wants it actually published to LinkedIn.
license: MIT
version: 1.0.0
---

# LinkedIn Poster

Publishes to LinkedIn for real, via the official REST API (`w_member_social`, personal profile
only) — never via an automated/logged-in browser session (that violates LinkedIn's Terms of
Service and risks account suspension).

## One-time setup (only if `.credentials.json` doesn't exist yet or has expired)

Requires Usuário to have created a LinkedIn Developer app with the "Share on LinkedIn" product
added (self-serve, no partner approval needed for posting to one's own profile —
https://www.linkedin.com/developers/apps). Then:

```
python3 /home/usuario/.claude/skills/linkedin-poster/scripts/linkedin_oauth_setup.py \
  --client-id <CLIENT_ID> --client-secret <CLIENT_SECRET>
```

This opens a browser for Usuário to log in and approve access, then writes
`.credentials.json` (permission 600) next to the scripts. Tokens last up to 60 days; rerun this
when `publish_linkedin_post.py` reports an expired token.

## Publishing a post

**Always dry-run first** and show Usuário the exact payload before publishing for real:

```
python3 /home/usuario/.claude/skills/linkedin-poster/scripts/publish_linkedin_post.py \
  --text "<final approved text>" [--image /path/to/photo.jpg]
```

Only after Usuário has explicitly confirmed the exact text (and image, if any) shown in the
dry-run output, re-run with `--publish`:

```
python3 /home/usuario/.claude/skills/linkedin-poster/scripts/publish_linkedin_post.py \
  --text "<final approved text>" [--image /path/to/photo.jpg] --publish
```

**Never pass `--publish` without that explicit confirmation in the current turn.**

## Related

- Agent: `linkedin-post-specialist` (drafts the post from a theme or a photo, then uses this
  skill to publish once the text is approved).
