---
name: coding-agent-clis
description: Use when delegating implementation, refactoring, or PR work to external coding agent CLIs such as Claude Code, Codex, or OpenCode. Choose the CLI by task shape, auth state, and whether you need print mode or an interactive TUI.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [coding-agents, cli, delegation, automation, pr, refactoring, review]
    related_skills: [hermes-agent]
---

# Coding Agent CLIs

Use this skill when you want an external coding agent CLI to do the work while Hermes orchestrates the session, files, and verification.

## When to Use

Use for:
- feature implementation
- refactoring and cleanup
- PR review / batch review
- issue fixing in worktrees or scratch repos
- long-running autonomous coding sessions

Do not use for tiny edits that Hermes can do directly; the extra process only helps when the task benefits from a separate agent boundary.

## Core decision: which CLI?

| CLI | Best for | Notes |
|---|---|---|
| Claude Code | multi-turn interactive coding, review, repo work | strong print mode and TUI workflows |
| Codex | OpenAI-native coding, PR review, batch tasks | requires PTY for interactive sessions |
| OpenCode | provider-agnostic coding worker, iterative tasks | run mode for one-shots, TUI for long sessions |

Choose the CLI that best matches the user's auth, model preference, and whether the task is one-shot or interactive.

## Shared workflow

1. Confirm the repo and workdir.
2. Check auth / binary availability.
3. Prefer one-shot / print modes for bounded work.
4. Use background PTY sessions only when iteration is needed.
5. Monitor output and intervene only when the agent asks or gets stuck.
6. Verify changed files and tests before reporting success.

## Claude Code

Use when you need a polished coding agent with print mode or a rich interactive TUI.

Highlights:
- `claude -p` for non-interactive tasks
- `claude --bare` when you want minimal startup overhead
- `claude -w` / `--tmux` for longer sessions with worktrees
- good fit for PR review and iterative refactors

Pitfalls:
- interactive mode needs tmux for reliable orchestration
- `--dangerously-skip-permissions` defaults to the wrong choice on first launch dialog
- `--max-turns` only applies in print mode

## Codex

Use when OpenAI Codex CLI is available and you want OpenAI-native coding behavior.

Highlights:
- `codex exec` for one-shot tasks
- `--full-auto` for autonomous workspace edits
- background PTY sessions for long tasks
- works well for feature work, refactors, and batch fixes

Pitfalls:
- always run in a git repository
- requires `pty=true` for interactive use
- may need `--sandbox danger-full-access` in Hermes gateway contexts if sandboxing fails

## OpenCode

Use when you want a provider-agnostic coding CLI that can run in short or long sessions.

Highlights:
- `opencode run` for bounded tasks
- interactive TUI for iterative work
- explicit session IDs make resuming simple
- good for parallel issue-fix work in separate workdirs

Pitfalls:
- TUI needs PTY
- do not use `/exit` in OpenCode; use Ctrl+C or kill the process
- keep each session scoped to one repo or worktree

## Verification checklist

- [ ] The right CLI matches the task shape
- [ ] Auth / binary availability checked before launch
- [ ] Workdir is explicit and isolated
- [ ] Output was monitored or the one-shot result was read back
- [ ] Changed files and tests were verified before claiming success
