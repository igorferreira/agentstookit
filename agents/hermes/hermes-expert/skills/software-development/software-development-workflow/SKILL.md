---
name: software-development-workflow
description: "Use for the full software change lifecycle: validate uncertain approaches with spikes, debug root causes, implement with test-driven development, and run pre-commit code and security review. Route to the relevant phase and preserve evidence at each gate."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [software-development, spike, debugging, tdd, code-review, verification]
---

# Software Development Workflow

## Overview

A class-level playbook for moving from uncertainty to a verified change. Use only the phases the task needs, but do not skip a gate merely because implementation appears obvious.

## Phase Router

1. **Uncertain feasibility or competing technologies — Spike.** Build a disposable experiment, collect real output, and issue a validated/partial/invalidated verdict. See `references/spike.md`.
2. **Unexpected behavior — Systematic debugging.** Reproduce, gather evidence, identify root cause, then fix. See `references/systematic-debugging.md`.
3. **Behavioral implementation — TDD.** Write and observe a failing test, make the minimum change, pass the focused and full suites, then refactor. See `references/test-driven-development.md`.
4. **Before commit or handoff — Review.** Inspect the diff, scan security hazards, run quality gates, and report unresolved risks. See `references/requesting-code-review.md`.
5. **Agent & Prompt Design — Agentic Patterns.** Use the 5-step prompt formula, context window optimization, and MCP toolchains for deterministic coding agents. See `references/agentic-prompt-engineering-patterns.md`.

## Integrated Sequence

- Establish acceptance criteria and the current baseline.
- Spike only the unknowns that could invalidate the design.
- When a defect exists, find the root cause before editing production code.
- Encode expected behavior in a test and observe RED.
- Implement minimally, observe GREEN, then refactor without changing behavior.
- Review the final diff and run the repository's real lint, test, type, and security checks.
- Report exact commands and outcomes; never fabricate passing output.

## Verification Checklist

- [ ] Baseline and acceptance criteria recorded
- [ ] Unknowns validated with evidence where needed
- [ ] Root cause identified for defects
- [ ] RED and GREEN observed for behavioral changes
- [ ] Full regression suite run
- [ ] Final diff and security-sensitive surfaces reviewed
