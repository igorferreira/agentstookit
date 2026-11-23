---
name: github-workflow
description: "Use when working across the GitHub lifecycle: authentication, repo setup, issues, pull requests, reviews, releases, and repository inspection. This is the umbrella for GitHub automation and day-to-day repo operations."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [GitHub, git, gh-cli, issues, pull-requests, repositories, releases, auth]
    related_skills: []
---

# GitHub Workflow

A class-level GitHub skill covering the common lifecycle: authenticate, inspect a repo, manage issues, open and review pull requests, handle releases, and keep the repository state tidy.

## When to Use

Use this skill when the user asks you to:
- authenticate to GitHub with `gh`, PATs, or SSH
- clone, fork, create, or configure repositories
- inspect repo size / language mix / codebase composition
- create, triage, label, assign, or close issues
- open, monitor, review, and merge pull requests
- post PR comments or formal reviews
- manage releases, tags, workflow runs, and secrets

If the task is specifically only about one narrow GitHub operation, still load this umbrella so you have the broader workflow in view.

## Core workflow

1. Detect auth state first.
2. Detect repo context and default branch.
3. Prefer `gh` when available; fall back to `git` + `curl` when needed.
4. Keep PRs small and reviewable; use conventional commit and PR body templates.
5. Verify with real commands and, when relevant, CI status or local tests.

## Authentication

Use this when the user has not yet authenticated or asks why GitHub access is failing.

- Check whether `gh auth status` works.
- If `gh` is available, prefer browser or token-based login through `gh auth login`.
- If not, use git credential helpers or SSH keys.
- Keep token handling out of chat output and docs.

See the moved support file for environment setup details and shell snippets.

## Repository management

Use this for cloning, creating, forking, syncing, and configuring repositories.

Common actions include:
- clone or fork a repository
- create a new repo from a local directory
- update repo settings and branch protection
- manage secrets and releases
- inspect repository metadata and language composition

## Issues

Use this for issue triage and tracking.

Typical flow:
- list open or untriaged issues
- read the issue body and labels
- assign an owner or add a triage label
- comment with investigation notes
- close or reopen when done

## Pull requests and reviews

Use this for the PR lifecycle and review work.

Typical flow:
- branch from a clean base
- commit with a conventional message
- create or update the PR
- check CI / workflow status
- leave inline and summary review comments
- merge when checks are green

## Code review style

When reviewing code, stay concrete:
- cite file and line numbers
- separate correctness from style suggestions
- call out security and test coverage issues clearly
- prefer short, actionable comments

## Repository inspection

Use this when you need a quick sense of what a repo contains before editing it.

Good questions:
- how large is the codebase?
- what languages dominate?
- are there huge generated/vendor directories?
- is the repo mostly code, docs, or config?

## Support files

- `scripts/gh-env.sh` — shell bootstrap and auth helpers
- `references/github-api-cheatsheet.md` — API-oriented reminders and endpoints
- `references/review-output-template.md` — structured review output format
- `references/conventional-commits.md` — commit message conventions
- `references/ci-troubleshooting.md` — CI failure triage notes
- `templates/bug-report.md` — issue template starter
- `templates/feature-request.md` — issue template starter
- `templates/pr-body-feature.md` — PR body starter
- `templates/pr-body-bugfix.md` — PR body starter

## Verification

Before reporting success:
- confirm auth works
- confirm the intended repo / branch / PR / issue exists
- confirm the desired server-side change or local git state actually changed
- verify CI or local checks if the workflow depends on them
