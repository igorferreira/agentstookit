---
name: knowledge-graph-indexing
description: Turn a folder into a queryable knowledge graph via Graphify.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [knowledge-graph, graphify, agent-tools, indexing, docs]
    related_skills: [coding-agent-clis]
---

# Knowledge-Graph Indexing

Turn a working folder into a queryable knowledge graph that AI agents can navigate —
beyond grep, it captures how parts relate. Primary tool: Graphify (open source, 100k+ stars,
Apache-2.0, package `graphifyy` on PyPI, CLI is `graphify`).

## When to use
- Understanding a large/messy codebase before agent work
- Indexing a document-heavy folder (legal case, research, contractor docs) so an agent answers
  "how does X relate to Y" instead of just "where is the word X"
- Building a navigable map of architecture/technical documentation

## Install
```bash
uv tool install graphifyy     # PyPI "graphifyy" (double-y). CLI command is still "graphify".
graphify --version            # verify
```
Alternatives: `pipx install graphifyy`, `pip install graphifyy`.

## Build a graph
`graphify <path>` with a bare path redirects to the `extract` command and creates `graphify-out/`.
```bash
cd /path/to/folder
graphify .                        # scan + extract + build
graphify query "<question>"       # answer via graph traversal
graphify explain "<node>"         # plain-language node explanation
```

## CRITICAL: CODE vs DOCS — LLM key
- **Code-only**: no key (local deterministic AST parsing works offline).
- **Docs/PDF/images corpus** (legal case, docs, papers): requires a semantic-extraction LLM key.
  Fails with "no LLM API key found ... Set GEMINI_API_KEY / ANTHROPIC_API_KEY /
  OPENAI_API_KEY / DEEPSEEK_API_KEY ... or pass --backend".
  - `--code-only` indexes only code (no key) but is useless for doc-heavy folders.
  - Pass a supported backend key to meaningfully index the documents.

## ⚠️ Credential boundary (hard rule)
When the key is missing, DO NOT search the user's environment, `.env`, `.claude/settings.json`,
hermes config, or any credential file to harvest an API key — even masked. The user treats this
as a leak/exposure risk and will veto it. STOP and ask the user which key to use, or abort.

## Avoid polluting synced/mirrored dirs
If the target folder is mirrored (e.g. MEGA + SharePoint + GDrive), run on a /tmp copy so
`graphify-out/` never enters the synced tree:
```bash
rsync -a --exclude=graphify-out SRC/ /tmp/workdir/
cd /tmp/workdir && graphify .
```

## Register the skill with an assistant
```bash
graphify install --platform hermes   # → ~/.hermes/skills/graphify/
graphify install                     # auto-detect
graphify install --project           # project-scoped
```
20+ platforms incl. claude, codex, opencode, gemini, copilot, cursor, claw (OpenClaw), hermes.

## Other commands
`graphify update <path>` (incremental re-extract) · `graphify watch <path>` (rebuild on change)
· `graphify clone <url>` · `graphify merge-graphs` · `graphify path "A" "B"` · `graphify diagnose`
· `graphify save-result` / `reflect` (QA feedback loop → graphify-out/reflections/LESSONS.md).