---
name: safe-codebase-modification
version: 1.0.0
author: hermes-agent
license: MIT
category: engineering-workflow
tags: [subagent, codebase, locked-ui, validation, docker]
related_skills: [browser-use, interactive-html-demos, demos-html-interativas]
description: Use when editing shared codebases with concurrent subagents.
---

# Safe Codebase Modification

## When to Use

Load this skill whenever you are about to modify a shared codebase where other agents, subagents, or background processes may be writing concurrently. Specifically:

- You are delegating work to subagents and need to verify their output didn't mutate unrelated files
- You are creating a new component (office, dashboard, demo) inside an existing repo that already has working components
- The project has a LOCKED UI contract or similar interface preservation rule
- A Docker compose build is in progress and you need to rebuild without cache pollution
- You receive a subagent completion report that mentions file modifications outside your task scope

If any of these conditions apply, load this skill FIRST and follow the protocol before touching any files.

## Scope

Covers:

- Delegation to subagents that may overwrite unrelated files
- Concurrent Docker builds / Git branches
- Multi-office demos where one change affects another
- Any codebase with an existing LOCKED UI or similar contract

## Protocol

### Step 0 — Pre-flight Lock Check

When resuming an in-flight codebase task after context compression, reload every task-relevant skill marked as pruned before any mutation, build, or test; a preserved todo records scope but may omit the governing procedures.

BEFORE writing ANYTHING:
```bash
git diff --stat           # current uncommitted changes
git status --short        # list of modified files
ls -la <target-dir>/      # verify target exists and is clean
```

If any files show `M ` in unexpected paths → PAUSE. Verify who/what modified them.

### Step 1 — Document Locked UI Before Diverging

If the codebase has an existing interface that must NOT change (CSS classes, HTML IDs, JS function signatures):

1. Copy the EXACT current state of the relevant section(s) to `_locked_snapshots/` in the project root
2. Write a `LOCKED_UI_CONTRACT.md` describing: which selectors, functions, and behaviors cannot change
3. Create a QA script that asserts these invariants before accepting any change

Example QA assertion:
```python
html = Path('app.html').read_text()
assert 'id="zoomOut"' in html          # zoom button preserved
assert 'id="rolePanel"' in html        # role panel preserved
assert 'initState()' in html            # entry function exists
```

### Step 2 — Validate Subagent Output IMMEDIATELY After Completion

When a subagent reports completion:

1. **List ALL modified files**: `git status --short`
2. **Diff each modified file against HEAD** for UNEXPECTED changes (outside the task scope)
3. **Re-validate exports** using a script that imports each module and checks required symbols exist
4. **Roll back out-of-scope changes** immediately

```bash
# Quick audit after subagent returns
git diff --name-only | while read f; do
    echo "=== $f ==="
    git diff "$f" | head -30
done
```

For each unexpected modification → revert with `git checkout -- $f` or restore from snapshot.

### Step 3 — Gate Before Merge / Commit

Before committing or pushing:

1. Run QA suite for the ENTIRE project (not just changed files)
2. Verify cross-dependencies: does Module A still export what Module B imports?
3. Run syntax checker on EVERY changed JavaScript file
4. Test in browser/container if possible (curl localhost:port/page → HTTP 200)

### Step 4 — Atomic Commits Per Component

Never commit mixed changes from different components:
```bash
# GOOD: separate commits per office
git add demos/clientes/banca_saude/js/*
git commit -m "fix: Banca Saude responsive layout"

git add demos/clientes/faculdade/
git commit -m "feat: new Faculdade office with aws-tutor agent"
```

## Pitfalls

- **PITFALL: Subagent silent mutations.** Subagents often modify files they shouldn't touch (e.g., rewriting auth tokens in sse.js when asked to create a new office). ALWAYS diff-and-revert after delegation completes.
- **PITFALL: Missing exported symbol breaks entire app.** If one module drops an export (`initRolePanel`), the importing module fails silently. Always validate `grep -r 'export function'` across all modules before testing.
- **PITFALL: Browser cache masks errors.** After Docker rebuild, hard-refresh (`Ctrl+Shift+R`) before debugging. The container may serve stale bundles.
- **PITFALL: Docker COPY uses cached layers.** `docker compose up --build` may use cached COPY layer even when source changed. Use `--no-cache` for critical rebuilds.
- **PITFALL: Committing build artifacts with `git add -A`.** A repo living inside a synced tree (e.g. MEGA) makes `-A` sweep unrelated files into the commit — always `git add` explicit paths. Keep generated/published dirs and local secret files (auth files) in `.gitignore`, and verify a secret never entered ANY commit (`git log --all --oneline -- <file>`) before pushing.
- **PITFALL: Attributing another agent's draft to yourself.** While subagents work in parallel on the same repo, the full test suite will fail on THEIR in-progress draft files (e.g., a generated page not yet registered in shared gates/menus). Before "fixing" a new gate failure, check whether the failing files belong to another agent's assigned prefix — the parent runs central integration (menu/build/gates) only AFTER all children finish; do not touch their files or "repair" the mid-flight state.
- **PITFALL: Broad staging during parallel waves.** While children are mid-flight, stage only build-canonical files you own by explicit path — a wide `git add` sweeps half-written draft artifacts into your commit.

## Dispatching subagents without truncation

Subagents that explore-then-edit routinely die on their iteration cap AFTER writing code but BEFORE committing — leaving uncommitted work in the tree and items pending. To make one dispatch survive:

1. **Embed the full execution map in the dispatch context**, not pointers to it: file:line of each edit, the exact old/new snippet or patch spec, precomputed values, and the commit grouping. Never make the child re-derive what you already know.
2. **Instruct mechanically**: at most ONE read per file (to confirm the anchor line), apply patches directly, commit incrementally every 2–3 items with explicit paths, run the test suite at the end of each group — zero reconnaissance commands, no re-reading for "context".
3. **Expect ~10 items per dispatch**, not 25. Bigger scopes hit the cap; split into sequential waves instead.
4. **When a child truncates**: verify the tree yourself (`git status`, run the suite), commit the completed-but-uncommitted work with explicit paths, then either finish the small remaining items yourself or re-dispatch ONLY the remainder with the map. Never re-dispatch the whole task — the tree already holds half of it.

## Audit-then-fix waves

For a rigorous bug-hunt over a repo: fan out READ-ONLY auditors in parallel (one per area, distinct lens), require every finding to carry executed evidence (a probe that actually reproduced it, in `/tmp` or a sandbox — never suspicion), then consolidate into a numbered inventory and fix in severity-ordered sequential waves (same repo ⇒ waves cannot run in parallel). Each fix wave: regression test failing first → fix → test green → commit per item → full suite → push. Authorize numeric changes explicitly: a fix may alter a published number only when the label/number was wrong against the canonical source — never as a side effect of parsing changes.

## Recovery Pattern

If a subagent corrupts files:
1. Restore from git: `git checkout -- path/to/corrupted/file`
2. Restore from snapshot if git doesn't help
3. Record what went wrong in `_postmortem_<date>.md`
4. Patch this skill's pitfalls section
