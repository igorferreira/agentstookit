# Graphify command reference & integration notes

Status verified on Igor's machine (02/09/2026): `graphify 0.9.53`, installed via `uv tool install graphifyy`.

## Key facts
- PyPI package: **`graphifyy`** (double-y). Other `graphify*` PyPI packages are NOT affiliated.
- CLI command: `graphify` (same name regardless of package).
- Official repo: `Graphify-Labs/graphify` (active dev branch `v8`).
- License Apache-2.0; homepage graphify.com.

## Scan behavior observed on a legal-case folder (docs/papers/images)
`graphify .` reported: `found 0 code, 23 docs, 41 papers, 2 images` and listed
"file(s) not classified (no supported extension or shebang), skipped" for `.gddoc`,
`_DESCONHECIDO_*` without recognized extensions, etc. So:
- `.gddoc` / unknown-extension files are skipped silently.
- Docs/papers/images are classified separately from code.
- On a doc-heavy corpus it immediately requested an LLM key (semantic extraction).

## Platforms (register the skill)
`graphify install` + per-platform wiring:
- Claude Code: `graphify claude install` (writes CLAUDE.md + PreToolUse hook)
- Codex / OpenCode / Aider / Copilot: write AGENTS.md section
- Cursor: `.cursor/rules/graphify.mdc`
- Gemini CLI: GEMINI.md + BeforeTool hook
- OpenClaw: `graphify claw install` (AGENTS.md)
- Hermes: `graphify hermes install` → `~/.hermes/skills/graphify/`
- Generic cross-framework: `graphify install --platform agents` (→ `~/.agents/skills/`)
- Uninstall all: `graphify uninstall [--purge]` (also removes `graphify-out/`)

## Graph lifecycle
- `graphify <path>` (bare) → `extract`. Output under `<path>/graphify-out/` (graph.json + graph.html).
- `graphify path "A" "B"` — shortest path between two nodes in graph.json.
- `graphify explain "X"` — plain-language explanation of a node + neighbors.
- `graphify update <path> [--force]` — incremental re-extract (no LLM). Use `--force` after refactors that delete code, or `GRAPHIFY_FORCE=1`.
- `graphify watch <path>` — rebuild on change.
- `graphify clone <url>` / `graphify merge-graphs <g1> <g2> --out`.
- `graphify diagnose multigraph` — detect same-endpoint edge collapse risk.
- `graphify check-update <path>` — cron-safe "needs_update" check.

## QA feedback loop
- `graphify save-result` → `graphify-out/memory/`
- `graphify reflect` → aggregates into `graphify-out/reflections/LESSONS.md`

## Mirror/hygiene pattern
Run offline/isolated before touching a synced tree: copy to /tmp excluding `graphify-out`,
build there, promote only what's wanted. Keeps synced dirs (MEGA + Dr. Diogo + GDrive) clean of
`graphify-out/`.

## Credential boundary recap
Doc-heavy indexing needs a backend key. When absent, DO NOT scrape the environment/`.env`/
config files for a key — ask the user which key to supply, or run `--code-only` only if code is
the actual corpus.