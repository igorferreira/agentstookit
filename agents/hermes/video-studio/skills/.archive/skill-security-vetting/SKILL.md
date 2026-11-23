---
name: skill-security-vetting
description: Use when installing or security-auditing Hermes skills.
---

# Skill Security Vetting

Governs the whole lifecycle of adding third-party skills to a Hermes install safely: search → inspect → scan verdict → install/reject → (optionally) periodic static audit of what's already installed.

## 1. Finding and inspecting a candidate skill

```bash
hermes skills search "<term>"                 # table view
hermes skills search "<term>" --json          # for parsing; gives exact `identifier`
hermes skills inspect "<exact name or id>"     # shows SKILL.md preview, tags, deps
```

Pitfalls:
- `hermes skills list` has **no `--json` flag** (only `search` does).
- Short/ambiguous identifiers (e.g. `skill-security-check`) return a disambiguation list instead of installing — always pass the **exact identifier** from `search --json`, or the exact quoted display name shown in that list.
- Read the full SKILL.md preview before installing: check `metadata.openclaw.requires` for OS/binary requirements. Skills bundling a compiled `.pyd`/`.dll`/`.exe` and declaring "Windows OS 10/11 Required" are incompatible with a Linux host and not worth installing regardless of security verdict.

## 2. The install-time guard (`skills-guard-v1`)

Every `hermes skills install <id>` fetches into quarantine and runs an automatic static scanner **before** the skill ever touches the live skills directory:

- **SAFE** → installed automatically.
- **CAUTION** → blocked by default; `--yes --force` can override it.
- **DANGEROUS** → blocked unconditionally. **`--force` does NOT override a dangerous verdict**, no matter what. Don't waste a retry on it.

```bash
hermes skills install "<exact id>" --yes            # SAFE only
hermes skills install "<exact id>" --yes --force     # to override a CAUTION verdict you've reviewed
```

### Known false-positive pattern

Skills whose *entire purpose* is to audit other skills for danger often get flagged **DANGEROUS/CAUTION themselves**, because their own SKILL.md/scripts *document or detect* the very patterns the scanner greps for (`sudo`, `os.environ[`, `/etc/passwd`, `chmod 777`, "ignore previous instructions", `setuid`/`setgid`). The scanner does simple pattern matching and cannot tell "this text describes a detection rule" from "this code executes the dangerous action."

Before accepting a DANGEROUS/CAUTION verdict at face value:
1. Read the actual flagged line(s) in context (scan output gives file:line + snippet).
2. If the surrounding text is a rules table, a YAML detection-rules file, or a docstring describing what the scanner looks for → likely false positive, safe to `--force` if verdict was CAUTION.
3. If the surrounding text is real executable code that reads `os.environ`, calls `subprocess`/`Popen`, monkey-patches env access, or spawns sandboxes/dockers to actually run untrusted code → the verdict is probably correct; do not force it, and don't install.
4. DANGEROUS verdicts cannot be forced either way — if you believe it's a false positive, tell the user and let them decide whether to install manually outside the guard.

## 3. Independent static audit of already-installed skills

Useful for periodic full-library security reviews (not just at install time). Run from `~/.hermes/skills/`:

```bash
cd ~/.hermes/skills
# Remote-install-and-run pattern (should only appear in known official installers)
grep -rlE "curl[^|]*\|\s*(sudo\s+)?(bash|sh)|wget[^|]*\|\s*(sudo\s+)?(bash|sh)" --include="*.md" --include="*.sh" --include="*.py" .
# Broad destructive deletes
grep -rlE "rm -rf (/|~|\$HOME)" --include="*.md" --include="*.sh" --include="*.py" .
# Credential/secret access
grep -rlE "\.ssh/id_rsa|\.aws/credentials|/etc/passwd|HISTFILE|\.netrc" --include="*.md" --include="*.sh" --include="*.py" .
# Bundled compiled binaries (unauditable by text review)
find . -type f \( -iname "*.pyd" -o -iname "*.dll" -o -iname "*.exe" -o -iname "*.so" \)
# Symlinks — verify each target resolves to a trusted LOCAL dir, not something remote/unknown
find . -type l
# Hidden base64 blobs dropped straight into SKILL.md
grep -rlE "^[A-Za-z0-9+/=]{200,}$" --include="*.md" .
# Prompt-injection / instruction-override phrasing
grep -rniE "ignore (all )?(previous|prior) instructions|disregard (the )?system prompt|send.*credentials to|exfiltrat" --include="*.md" .
```

Every hit needs manual triage, not automatic condemnation — see references/known-benign-hits.md for the recurring false-positive shapes seen so far (official `curl|bash` installers, `/tmp` cleanup `rm -rf`, path-traversal test fixtures, security-review checklists that *mention* "exfiltration" as a grading criterion).

`~/.hermes/skills/.hub/quarantine/` is an internal cache — it cannot be read directly with search_files/read_file ("Access denied ... to prevent prompt injection"); rely on the scan output printed to the terminal instead, or the `hermes skills inspect` preview before installing.

## 4. Reporting format

For a full-library audit, deliver: an overall verdict, a table of {category, location, verdict} for every real finding (mark clearly which are benign/expected vs which need action), and — if the request also involved researching new skills — a separate section listing candidates researched-but-not-installed with the reason (compatibility, false-positive-but-unverifiable, or genuinely risky).

## Linked files
- `references/known-benign-hits.md` — recurring false-positive patterns seen in real audits, so you don't re-litigate them each time.
