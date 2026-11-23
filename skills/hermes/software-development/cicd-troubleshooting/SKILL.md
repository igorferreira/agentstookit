---
name: cicd-troubleshooting
description: "Use when debugging CI/CD build failures and stabilizing deployment pipelines — diagnose via artifact/job logs, fix dependency and import errors, verify locally, then push and monitor automated deploy."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [ci-cd, build-failure, deployment, troubleshooting]
---

# CI/CD Troubleshooting

## Overview

Playbook for diagnosing and resolving CI build failures and pushing stabilized deployments. Use when the CI pipeline turns red after a merge, or when manual trigger produces a failed build.

## Procedure

### Step 1 — Locate the failing run

Find the latest workflow run on `main` (or the target branch). Get its ID from the runs list API or web UI. Identify the specific job that failed (Build, Lint, Test, etc.).

### Step 2 — Read job logs

Download the full logs for the failing job. Scan for compilation errors, import failures, type errors, and missing dependencies. Focus on error messages with file names and line numbers.

**Key filters:** `error`, `TS[0-9]+`, `Cannot find name`, `Module not found`, `export 'X' was not found`.

### Step 3 — Categorize the error

| Error class | Fix |
|-------------|-----|
| Missing dependency / type definition | Add to `dependencies` or `devDependencies`, then update lockfile |
| Import path wrong | Fix path or verify barrel export (`index.ts`) |
| Component expects props/context | Provide placeholder/stub, or add guard with login redirect |
| Type mismatch in generic | Check type parameter order and expected shape |

### Step 4 — Patch and verify locally

1. Apply the fix to the source file(s)
2. Run the type checker (`tsc --noEmit`) against the affected tsconfig
3. Install deps to regenerate lockfile (do NOT skip this)
4. Commit ONLY changed files explicitly (`git add <path>`) — never `git add -A` inside synced monorepos
5. Push to trigger CI rebuild

### Step 5 — Monitor and validate deployment

After push, monitor the next workflow run until completion. When successful:
- Verify via browser or HTTP scrape that the deployed page contains expected elements
- Check that navigation/chips/buttons render correctly on mobile viewport

## Pitfalls

- **Lockfile discipline**: Adding a dependency to `package.json` is not enough — the CI uses the lockfile. Must run `pnpm install` (equivalent for npm/yarn) and commit the updated lockfile alongside the code change, or CI fails with `ERR_PNPM_OUTDATED_LOCKFILE`.
- **Auth-dependent components**: Components that require authentication context, backend hooks, or unready APIs will throw at render/import time even in stub implementations. Replace with explicit placeholder sections that describe the required action ("faz login para usar esta funcionalidade"), never leave blank `<section>` wrappers.
- **Build vs dev divergence**: Code that passes `vite dev` may still fail in CI due to stricter settings, different Node versions, or plugins disabled in development. Always run type-checker in production-like mode before pushing.
- **Vercel cache stale**: After fixing a build, if the deployed URL still shows old content, wait 60–90 seconds for CDN propagation. Verify via fresh browser tab or `curl -I` for ETag change.

## Related References

See `references/ci-fix-patterns.md` for detailed fix recipes by error type.
