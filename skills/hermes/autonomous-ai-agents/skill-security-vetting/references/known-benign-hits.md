# Known benign hits in skill security scans

Recurring findings from static audits (grep-based and `skills-guard-v1`) that are almost always false positives. Confirmed against a real full-library audit of ~151 installed skills (Aug 2026). Still eyeball the actual line before dismissing — this is a prior, not a rubber stamp.

## `curl | bash` / `wget | sh`
Benign when it's a documented official installer command inside a skill's own setup instructions (e.g. the skill's own upstream project's install script: Nous Research, ntn.dev/Notion CLI, X Platform's xurl). Risky if it appears inside a script that *runs automatically* rather than being a copy-paste instruction for the human, or if the domain isn't the skill's own documented upstream.

## `rm -rf` with a fixed `/tmp/...` path
Benign when it's cleanup of a specific, hardcoded scratch directory the skill created itself (e.g. `rm -rf /tmp/recalc_in /tmp/recalc_out` before a LibreOffice headless recalc pass). Risky if the path includes a variable, `$HOME`, `~`, or a bare `/`.

## `/etc/passwd`, `/etc/shadow`, `.ssh`, `.aws/credentials` mentioned in test files
Benign when found inside a `test_*.py` validating a `safe_path_join`/path-traversal-guard function — the test asserts the function *rejects* that path. Read the surrounding assert/pytest.raises to confirm it's defensive testing, not an access attempt.

## "exfiltration" as a plain-English word in review checklists
Benign when it's a code-review or security-review skill listing "data exfiltration" as one of many auto-FAIL criteria graders should look for in *other* code — i.e. descriptive prose, not an instruction to exfiltrate anything.

## Security-auditor skills flagged DANGEROUS by the install-time guard
The install guard (`skills-guard-v1`) is a naive pattern matcher. A skill whose whole job is detecting `sudo`, `os.environ[`, `chmod 777`, `setuid`, prompt-injection phrases, etc. will itself contain those strings — in a rules table, a YAML ruleset, or a docstring — and gets flagged as if it executed them. Distinguish by checking whether the surrounding code actually *calls* the dangerous primitive vs. merely *lists/matches against* it. See the parent skill's "install-time guard" section for the full decision procedure. Note: `--force` never overrides a DANGEROUS verdict even when you're confident it's a false positive — the guard is a hard block, not a warning at that level.

## Genuinely risky pattern seen (not benign)
A "skill security checker" (v3.3.0, ClawHub) shipped real sandboxing code: `os.environ.__class__.__getitem__` monkey-patching to intercept env reads, `subprocess.Popen`/`docker_backend.py`, and a dynamic execution sandbox — 47 scanner findings, many in *actually executing* code paths, not just detection-rule text. This one was correctly left uninstalled; don't treat "it's a security-auditor skill" as automatic grounds to dismiss its own findings — check whether the code paths are live or descriptive.
