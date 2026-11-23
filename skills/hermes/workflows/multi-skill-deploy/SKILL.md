---
name: multi-skill-deploy
description: >
  Identify, fetch, verify, and deploy skills from external sources (social media posts, curated lists, GitHub repos) across all local agent runtimes. Triggers when the user asks to install, extract, or distribute skills from a linked list, reel, post, or any external URL. Covers sourcing, repo cloning, security scanning, cross-runtime deployment, and verification.
---

# /multi-skill-deploy — Install skills from external sources across all runtimes

Deploy a batch of skills from an external source (Instagram reel, curated post, GitHub repo) into every local runtime agent.

## Step 1 — Extract skill list from source

Parse the source URL/post for skill names or repo paths. Common formats:

- **Structured table** → parse each row's name column
- **Numbered/bulleted list** → extract names between bullets/numbers
- **Repo paths** (e.g., `obra/superpowers`) → resolve to individual skill directory names
- **Implied mentions** → if author references a well-known pack (Superpowers, Matt Pocock TDD), enumerate members from public source

If the source is a social media post (Instagram, X/Twitter, LinkedIn):
1. Use `web_extract` on the URL; if it fails or returns insufficient data, use `web_search` with the exact post title + "skills" as query terms.
2. Cross-reference against known external skill repos for completeness.
3. Always include **indirectly mentioned** skills (referenced in author comments, descriptions, or related links).

### Pitfall: Repo identifier accuracy
Repository names often have subtle variants (plural vs singular, case sensitivity). `superpowers-skills` ≠ `superpowers-skill`. Verify the exact identifier from the GitHub repo root before searching — one character off means zero results. When in doubt, clone the repo and inspect its structure.

## Step 2 — Clone source repos

For skills hosted in GitHub repos:

```bash
git clone --depth 1 <repo-url> /tmp/deploy-source-<slug>/
```

Use `--depth 1` for speed. Keep in `/tmp/` — clean up after.

### Pitfall: GitHub API rate limiting
If listing repo contents via API hits rate limits, fall back to direct curl against `raw.githubusercontent.com`:

```bash
curl -sL https://raw.githubusercontent.com/<owner>/<repo>/main/<path-to-SKILL.md> > target.md
```

Do NOT retry the same API endpoint — switch to raw URLs for subsequent skills.

## Step 3 — Security scan each skill

Before installing ANY skill, run the built-in security scan:

```bash
hermes skill scan <path-to-skill-dir>
# OR for a cloned repo:
for sdir in /tmp/deploy-source-*/skills/*/; do
    echo "=== $sdir ===" && head -5 "$sdir/SKILL.md"
done
```

Gate rules:
- **SAFE** → proceed
- **CAUTION** → surface risk, ask user before installing
- **DANGEROUS** → block install, explain the reason to the user

Some external repos ship skills marked DANGEROUS for good reason (destructive shell commands in SKILL.md body, unvetted network access). Do NOT override a DANGEROUS verdict without explicit user confirmation and understanding of the risk.

Document blocked skills in the final report with reason.

## Step 4 — Create destination directories

Each target runtime has its own skills directory:

| Runtime | Path |
|---|---|
| Hermes | `~/.hermes/skills/` |
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.codex/skills/` |
| OpenCode | `~/.opencode/skills/` |
| OpenClaw | `~/.openclaw/skills/` |

For each approved skill, create the destination dir:

```bash
mkdir -p ~/.{runtime}/skills/{skill-name}
```

## Step 5 — Copy skills to all runtimes

Batch copy all approved skills to all 5 runtimes. Use Python's `os.path` for verification (more reliable than shell globbing across many dirs):

```python
import os
from hermes_tools import terminal

runtimes = {
    "Hermes": "~/.hermes/skills",
    "Claude": "~/.claude/skills",
    "Codex": "~/.codex/skills",
    "OpenCode": "~/.opencode/skills",
    "OpenClaw": "~/.openclaw/skills"
}

for rt_name, base in runtimes.items():
    for skill in approved_skills:
        dest = os.path.expanduser(f"{base}/{skill}")
        # Copy from source temp dir
        terminal(f"cp -r {src_dir}/{skill} {dest}")
```

## Step 6 — Verify installation

Check every runtime for every skill:

```python
import os
for rt_name, base in runtimes.items():
    found = []
    missing = []
    for skill in approved_skills:
        p = os.path.expanduser(f"{base}/{skill}")
        if os.path.isdir(p):
            found.append(skill)
        else:
            missing.append(skill)
    status = f"✅ {len(found)}/{len(approved_skills)}" if not missing else f"⚠️ {status}"
    print(f"{rt_name}: {status}" + (f"\n  Missing: {', '.join(missing)}" if missing else ""))
```

## Step 7 — Document the deployment

Save a record of what was installed where:

- `~/MEGA/Documentos/instagram/posts/post-<source>-YYYY-MM-DD.md` for social media sources
- `~/MEGA/Documentos/agentes_hermes/SKILLS-DEPLOYED/YYYY-MM-DD-report.md` for internal deployments
- Update `~/MEGA/Documentos/instagram/posts/INDEX.md` if social source

Record: skill names, source repo, security verdict per skill, which runtimes received them, any blocks/denials.

## Quick reference: common external skill packs

| Pack | Author/Source | Key skills | Known IDs |
|---|---|---|---|
| Superpowers | obra/superpowers + obra/superpowers-skills | brainstorming, executing-plans, dispatching-parallel-agents, defense-in-depth-validation, etc. | `superpowers-skills` (plural!) |
| Superpowers Lab | obra/superpowers-lab | finding-duplicate-functions, mcp-cli | lab branch |
| TDD | mattpocock/skills | tdd | Skills shipped independently |
| Gemini Deep Research | Google | deep-research | Usually bundled |
