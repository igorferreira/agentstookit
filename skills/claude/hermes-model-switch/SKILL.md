---
name: hermes-model-switch
description: Use whenever Igor asks to change/switch/troca the model or provider that Hermes uses (primary model, fallback chain, or both), or asks to check which model Hermes is on, whether a provider is rate-limited, or why Hermes is failing/erroring on every message. Triggers on "troca o hermes para X", "muda o modelo do hermes", "coloca [provider] como fallback", "por que o hermes ta dando erro", "reinicia o hermes", "hermes travado". Encodes the exact CLI commands and known gotchas discovered through repeated trial and error, so this doesn't need to be re-derived from scratch each time.
metadata:
  version: 1.0.0
---

# hermes-model-switch — change Hermes's model/provider fast, without re-deriving the process

## Step 0 — Diagnose first, don't just switch blindly

Before changing anything, check what's actually happening — "switch to X" often doesn't fix the
real problem if X is already active or also broken:

```bash
hermes config get model              # current primary provider/model
hermes fallback list                 # current fallback chain (in try-order)
hermes auth list                     # per-provider credential status — look for
                                      # "rate-limited" / "usage_limit_reached" / time remaining
```

Also check recent real errors before assuming config is the problem:
```bash
tail -n 60 ~/.hermes/logs/errors.log
grep "Fallback activated\|API call #" ~/.hermes/logs/agent.log | tail -20
```

Common root causes seen in practice, in order of frequency:
- **Provider rate-limited** (`hermes auth list` shows `rate-limited` with a countdown). Switching
  the primary to that same already-rate-limited provider does nothing. **`openai-codex` (ChatGPT login) is
  unusable**: `usage_limit_reached` until ~2026-10-17 AND `HTTP 400 "gpt-5.6-sol is not supported when
  using Codex with a ChatGPT account"`. Do not use it as primary or fallback.
- **OpenRouter credits depleted** (`HTTP 402` in errors.log, "can only afford N tokens"). Check the balance
  without printing the key: `K=$(grep -E '^OPENROUTER_API_KEY=' ~/.hermes/.env | cut -d= -f2-); curl -s -H "Authorization: Bearer $K" https://openrouter.ai/api/v1/credits`
  (balance = total_credits - total_usage). Igor tops it up himself. If it hits zero, chat AND crons AND most profiles
  fail together (Igor accepted this single point of failure on 2026-09-18; there is no independent fallback).
- **Anthropic is blocked for Hermes/OpenClaw** (confirmed by Igor 2026-09-18): `HTTP 400 - "Third-party apps
  now draw from your extra usage, not your plan limits"`. **Never use provider `anthropic` (Claude Sonnet/
  Haiku/Opus) in Hermes** — not as primary, fallback, cron model or profile model. Its credentials were removed
  from the pool and the `ANTHROPIC_*` lines in `~/.hermes/.env` commented out on 2026-09-18.

## Step 1 — Change the primary model/provider

```bash
hermes config set model.provider <provider>   # e.g. openrouter, gemini, deepseek
hermes config set model.default <model>       # e.g. openai/gpt-5.6-luna, z-ai/glm-5.3-flash
```

This is safe to run directly — no known bugs on these two scalar keys.

### Where each thing is configured (change in ONE place per surface)
- **Chat (default profile):** `~/.hermes/config.yaml` -> `model.default` / `model.provider` (+ `fallback_providers`).
- **Crons:** `~/.hermes/config.yaml` -> `cron.model` / `cron.model_provider`. Jobs with no pin follow it (verified);
  a job only keeps its own model if pinned with `hermes cron edit <id> --model M --provider P`; clear a pin with
  `--model "" --provider ""`. Without `cron.model`, a global model change makes unpinned jobs skip (`drift_skip`).
- **Profiles (~113 folders, isolated config + `.env`):** `~/.hermes/models.yaml` (tiers + fallbacks + profile->tier)
  and `python3 ~/.hermes/scripts/sync-profile-models.py` (dry-run by default, `--apply`, backup per profile).
  `python3 ~/.hermes/scripts/provision-openrouter-profiles.py` copies the OpenRouter key into profile `.env` files.
  A profile only works with a provider whose key is in ITS `.env`.

## Step 2 — Change the fallback chain (DO NOT use `hermes config set fallback_providers[N].model`)

That CLI form is broken: it creates a **bad literal top-level key** named
`fallback_providers[N]` instead of editing the array element, and can also trigger a YAML
aliasing bug that silently collapses multiple identical-looking entries into one node (so
`hermes fallback list` shows fewer entries than expected, though the underlying data may still be
correct — always verify with `grep -A2 "^fallback_providers" ~/.hermes/config.yaml` after any
edit, not just `hermes fallback list`).

Instead, always edit the array directly with `ruamel.yaml`, and build each entry as a **fresh,
independent `CommentedMap`** (never reuse/copy a dict reference across entries — that's what
causes the aliasing collapse):

```python
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap
yaml = YAML()
yaml.preserve_quotes = True
yaml.width = 4096

path = "/home/usuario/.hermes/config.yaml"
with open(path) as f:
    data = yaml.safe_load(f)

data["fallback_providers"] = [
    CommentedMap([("provider", "openrouter"), ("model", "z-ai/glm-5.3-flash")]),
    CommentedMap([("provider", "openrouter"), ("model", "deepseek/deepseek-v4.1-flash")]),
]

with open(path, "w") as f:
    yaml.dump(data, f)
```

Verify with `hermes fallback list` AND a raw `grep -A6 "^fallback_providers" ~/.hermes/config.yaml`.

### Known-good model picks (as of 2026-09-18; see ~/.hermes/docs/modelos-openrouter-2026-09.md)
Value = Artificial Analysis Intelligence Index vs cost per typical Hermes call (110k input, 87% cached). All have tool calling.
- **Primary / premium:** `openrouter` / `openai/gpt-5.6-luna` (index 51.2, 1.05M window, ~US$ 5 per 1000 calls) — current chat primary.
- **Cheap workhorse (crons, econ profiles):** `openrouter` / `z-ai/glm-5.3-flash` (41.9, 1.31M, ~US$ 3 per 1000 calls). More tool-call
  rounds than a frontier model on scraping jobs (42 calls vs 6 in one test) but ~9x cheaper per run.
- **Highest quality if needed:** `openrouter` / `deepseek/deepseek-v4-pro-0813` (53.2, ~US$ 10.5 per 1000 calls).
- **2nd fallback:** `openrouter` / `deepseek/deepseek-v4.1-flash` (index 39.5, ~US$ 2.6 per 1000 calls). Igor chose to keep EVERYTHING on OpenRouter (2026-09-18): chat, crons, profiles, vision (`openai/gpt-5.6-luna`) and compression summary (`z-ai/glm-5.3-flash`). Consequence: a zero OpenRouter balance takes everything down at once; check the balance first when all surfaces fail.
- Avoid: `openai-codex/*` (blocked), any `anthropic/*` (blocked), `minimax/minimax-m3` and `google/gemini-3.7-flash` on OpenRouter
  (dominated: costlier and lower index than glm-5.3-flash).
- Fetch live OpenRouter pricing anytime with: `curl -s https://openrouter.ai/api/v1/models | python3 -m json.tool` (filter by `id`/`pricing.prompt`/`pricing.completion`)

## Step 3 — Restart to apply

Try the normal path first:
```bash
hermes gateway restart
```

If it hangs in `deactivating (final-sigkill)` for more than ~30s (check with `hermes gateway
status`), the systemd cgroup is likely stuck on **orphaned headless Chrome/Playwright processes
in D-state** (uninterruptible kernel sleep on `drm_open` — a GPU/DRM driver issue, accumulates
from browse/QA/audit sessions that didn't close their browser). These **cannot be killed by any
signal**, not even `SIGKILL` — don't waste time retrying kill. Diagnose with:
```bash
ps -o pid,stat,cmd -p <pids from `systemctl --user status hermes-gateway` CGroup section>
# STAT column showing "D" confirms uninterruptible sleep — unfixable short of a reboot
```

Workaround: run Hermes manually, outside the stuck systemd unit, until Igor is ready for a full
machine reboot (only real fix for the D-state processes):
```bash
nohup hermes gateway run --replace > /tmp/hermes_manual_run.log 2>&1 &
disown
```
`--replace` is needed if a previous manual instance is still holding the lock (`❌ Gateway
already running (PID ...)`).

**Gotcha:** launching this nohup'd process in the *same* Bash call as a preceding `kill`/`pkill`
sometimes returns a bogus non-zero exit code (seen as `144`) and the backgrounded process doesn't
actually survive. If that happens, just re-run the `nohup ... & disown` line alone in a fresh,
separate command — don't chain it after a kill in one shot. Always verify aftewards with:
```bash
ps -p <PID> -o pid,etime,cmd   # or: pgrep -af "hermes_cli.main gateway run"
tail -n 15 /tmp/hermes_manual_run.log
```

## Step 4 — Report back

Always tell Igor: what changed (old → new for primary and each fallback slot), whether the
gateway is running via systemd or the manual workaround (and that the manual one won't survive a
reboot/logout on its own), and any rate-limit/credit ceilings discovered in Step 0 that will bite
again soon.
