---
name: kanban-system
description: "Kanban multi-agent orchestration system — orchestrator decomposition playbook (task planning, routing, dependency management) and worker execution guide (lifecycle, pitfalls, handoffs, heartbeats, retries). Use when the user wants to decompose work into Kanban tasks, or when dispatched as a worker."
version: 3.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [kanban, multi-agent, orchestration, routing, worker, task-management]
    related_skills: []
---

# Kanban Multi-Agent System

This umbrella skill covers both sides of the Hermes Kanban multi-agent workflow:

- **§ Orchestrator** — the decomposition playbook for routing work through Kanban: task planning, profile discovery, dependency graphs, anti-temptation rules, fan-out patterns, and recovering stuck workers.
- **§ Worker** — the execution guide for dispatched workers: lifecycle, good handoff shapes, heartbeats, retry diagnostics, workspace handling, and edge cases.

The core worker lifecycle (the `kanban_create` fan-out pattern and the "decompose, don't execute" rule for orchestrators; the 6-step lifecycle — orient → work → heartbeat → block/complete — for workers) is auto-injected into every kanban process via the `KANBAN_GUIDANCE` system-prompt block. This skill provides the deeper detail beyond that injection.

---

## § Orchestrator — Decomposition Playbook

### Profiles are user-configured — not a fixed roster

Hermes setups vary widely. Some users run a single profile that does everything; some run a small fleet (`docker-worker`, `cron-worker`); some run a curated specialist team they've named themselves. There is **no default specialist roster** — the orchestrator skill does not know what profiles exist on this machine.

Before fanning out, you must ground the decomposition in the profiles that actually exist. The dispatcher silently fails to spawn unknown assignee names — it doesn't autocorrect, doesn't suggest, doesn't fall back. So a card assigned to `researcher` on a setup that only has `docker-worker` just sits in `ready` forever.

**Step 0: discover available profiles before planning.**

Use one of these:

- `hermes profile list` — prints the table of profiles configured on this machine. Run it through your terminal tool if you have one; otherwise ask the user. When the roster or warning output is large, filter to candidate profiles and their relevant warnings; dumping every profile warning can obscure the actual assignee and queue state.
- `kanban_list(assignee="<some-name>")` — sanity-check a single name. Returns an empty list (rather than an error) for an unknown assignee, so this only confirms a name you're already considering.
- **Just ask the user.** "What profiles do you have set up?" is a fine first turn when the goal needs more than one specialist.

Cache the result in your working memory for the rest of the conversation. Re-asking every turn wastes a tool call.

### When to use the board (vs. just doing the work)

Create Kanban tasks when any of these are true:

1. **Multiple specialists are needed.** Research + analysis + writing is three profiles.
2. **The work should survive a crash or restart.** Long-running, recurring, or important.
3. **The user might want to interject.** Human-in-the-loop at any step.
4. **Multiple subtasks can run in parallel.** Fan-out for speed.
5. **Review / iteration is expected.** A reviewer profile loops on drafter output.
6. **The audit trail matters.** Board rows persist in SQLite forever.

If *none* of those apply — it's a small one-shot reasoning task — use `delegate_task` instead or answer the user directly.

### Chronological queue mirrors and concurrent updates

When a Kanban workflow is mirrored in a chronological queue file:

- Re-read the current mirror immediately before adding an item; earlier conversation context may be stale because another request can be recorded concurrently.
- Insert by the request's received time and renumber affected entries, rather than blindly appending after the last number seen.
- After writing, re-read the affected range and inspect the exact Kanban task ID; confirm the mirror and card agree on title, order, destination/acceptance details, and non-dispatchable queued status.
- Treat a follow-up that clarifies a queued task's destination or acceptance as an update to the existing card and mirror, not a duplicate task. Bind “this post” to the latest relevant URL in the same thread; if multiple candidates remain plausible, clarify before changing the target. Keep it non-dispatchable with empty start/end fields until execution is authorized.
- After starting/completing work, read each card back and source its start/end time from that card's persisted lifecycle timestamps (`started_at`/`completed_at`), converting epoch values in the correct timezone. Do not use the request's [Agora] time or one shared batch time as a later completion time. Confirm the board's actual terminal status value rather than assuming a label such as `completed`; update each mirrored row from its own card and re-read the affected range.
- A request to enqueue is not authorization to begin execution. Keep start/end fields empty until work actually starts and finishes, and use the local queue protocol's non-dispatchable state for future work.
- Before sending a Kanban link in a status or completion reply, resolve the current authoritative web/local URL and verify that it serves the board. If a public URL is stale, do not repeat it; provide a verified local route and state that the public route is unavailable. Do not start or expose a new tunnel just to supply a link.
- Before inventorying or dispatching an existing queue, read the current board list and account for every status. Tally all nonterminal cards by status (`ready`, `todo`, `blocked`, `running`, and any other live state), verify the subtotals equal the nonterminal total, and retain the exact IDs in each group. Never infer the queue by filtering only `ready` rows or one status icon. If machine-readable output cannot be parsed, fall back to the plain list and verify ambiguous records with `show`; do not silently drop rows. Capture the baseline before creating a coordination/meta card so it does not distort the work count.
- A later explicit user authorization to run a clearly defined set of queued/blocked cards in parallel—including “all currently pending/executable cards” on the designated board after inventory—overrides older wait text only for that set. Treat broad scope as a point-in-time snapshot: cards created after the authorization are outside it unless the user explicitly includes future items or names those cards. Do not ask the user to repeat the IDs when the set is unambiguous. Record the authorization and exact card set in each card's comments; assign, unblock, and dispatch only those IDs, leaving unrelated queue entries unchanged. Keep genuine prerequisites blocked, and preserve dependency links: never parallelize a child that needs a parent's output.
- Re-inventory immediately before EVERY board mutation after any context gap (compaction, interrupted turn, or hours elapsed) — an inventory from a previous turn can be a day stale, even within the same session. Check each target card's live status right before `complete`/`unblock`: a refusal like `cannot complete (unknown id or terminal state)` means the card is already terminal — read the newest run's `summary` and confirm the work independently (commits, tests, artifacts) instead of retrying; if the evidence is real, your closure is redundant and you must NOT re-execute or re-close it as if it were fresh work.
- Assume a SECOND orchestrator session can mutate the same board concurrently (same machine, multiple Hermes sessions share one SQLite board). Between reading a card's status and acting on it, another actor can claim, complete, or unblock it — a mutation refused with `(not blocked/scheduled?)` usually means someone won the race seconds earlier. Re-read the card, verify the other actor's run, and never spawn duplicate work for a card in `running`; report the other actor's verified results instead of redoing them.

### The anti-temptation rules

Your job description says "route, don't execute." The rules that enforce that:

- **Do not implement specialist work yourself, but do not merely park it.** If Igor explicitly asks for execution, create or reuse the task and dispatch the actual worker(s) through the approved Kanban path; a card being created, assigned, commented on, or left `ready` is tracking, not execution. Verify a real run/spawn and inspect the outputs/tests before reporting progress or completion. If an external prerequisite (credential, human login, approval) blocks a lane, keep that lane blocked, continue independent authorized lanes, and name the exact next step; never substitute fake credentials or bypass authentication.
- **For any concrete task, create a Kanban task and assign it.** Every single time.
- **Split multi-lane requests before creating cards.** A user prompt can contain several independent workstreams. Extract those lanes first, then create one card per lane instead of bundling unrelated work into a single implementer card.
- **Run independent lanes in parallel.** If two cards do not need each other's output, leave them unlinked so the dispatcher can fan them out. Link only true data dependencies.
- **Never create dependent work as independent ready cards.** If a card must wait for another card, pass `parents=[...]` in the original `kanban_create` call. Do not create it first and link it later, and do not rely on prose like "wait for T1" inside the body.
- **If no specialist fits the available profiles, ask the user which profile to create or which existing profile to use.** Do not invent profile names; the dispatcher will silently drop unknown assignees.
- **Match the action to the request.** For a plan/queue request, decompose and leave work non-dispatchable; for an explicit execute request, decompose, dispatch, verify, and report the concrete result.

### Decomposition playbook

#### Step 1 — Understand the goal

Ask only when the goal or scope is genuinely ambiguous in a way that changes which work will run. If the user clearly authorizes all pending work, enumerate the designated board and dispatch the eligible independent subset; do not ask them to restate that scope or let real blockers hold up unrelated ready work. Keep items requiring credentials, data, approval, physical action, or unresolved dependencies blocked, and report those exceptions.

#### Step 2 — Sketch the task graph

Before creating anything, draft the graph out loud (in your response to the user). Treat every concrete workstream as a candidate card:

1. Extract the lanes from the request.
2. Map each lane to one of the profiles you discovered in Step 0. If a lane doesn't fit any existing profile, ask the user which to use or create.
3. Decide whether each lane is independent or gated by another lane.
4. Create independent lanes as parallel cards with no parent links.
5. Create synthesis/review/integration cards with parent links to the lanes they depend on. A child created with unfinished parents starts in `todo`; the dispatcher promotes it to `ready` only after every parent is done.

Examples of prompts that should fan out (using placeholder profile names — substitute whatever exists on the user's setup):

- "Build an app" → one card to a design-oriented profile for product/UI direction, one or two cards to engineering profiles for implementation, plus a later integration/review card if the user has a reviewer profile.
- "Fix blockers and check model variants" → one implementation card for the blocker fixes plus one discovery/research card for config/source verification. A final reviewer card can depend on both.
- "Research docs and implement" → a docs-research card can run in parallel with a codebase-discovery card; implementation waits only if it truly needs those findings.
- "Analyze this screenshot and find the related code" → one card to a vision-capable profile for the visual analysis while another searches the codebase.

Words like "also," "finally," or "and" do not automatically imply a dependency. They often mean "make sure this is covered before reporting back." Only link tasks when one card cannot start until another card's output exists.

Show the graph to the user before creating cards. Let them correct it — including which actual profile name should own each lane.

#### Step 3 — Create tasks and link

Use the profile names from Step 0. The example below uses placeholders `<profile-A>`, `<profile-B>`, `<profile-C>` — replace them with what the user actually has.

```python
t1 = kanban_create(
    title="research: Postgres cost vs current",
    assignee="<profile-A>",  # whichever profile handles research on this setup
    body="Compare estimated infrastructure costs, migration costs, and ongoing ops costs over a 3-year window. Sources: AWS/GCP pricing, team time estimates, current Postgres bills from peers.",
    tenant=os.environ.get("HERMES_TENANT"),
)["task_id"]

t2 = kanban_create(
    title="research: Postgres performance vs current",
    assignee="<profile-A>",  # same profile, run in parallel
    body="Compare query latency, throughput, and scaling characteristics at our expected data volume (~500GB, 10k QPS peak). Sources: benchmark papers, public case studies, pgbench results if easy.",
)["task_id"]

t3 = kanban_create(
    title="synthesize migration recommendation",
    assignee="<profile-B>",  # whichever profile does synthesis/analysis
    body="Read the findings from T1 (cost) and T2 (performance). Produce a 1-page recommendation with explicit trade-offs and a go/no-go call.",
    parents=[t1, t2],
)["task_id"]

t4 = kanban_create(
    title="draft decision memo",
    assignee="<profile-C>",  # whichever profile drafts user-facing prose
    body="Turn the analyst's recommendation into a 2-page memo for the CTO. Match the tone of previous decision memos in the team's knowledge base.",
    parents=[t3],
)["task_id"]
```

`parents=[...]` gates promotion — children stay in `todo` until every parent reaches `done`, then auto-promote to `ready`. No manual coordination needed; the dispatcher and dependency engine handle it.

If the task graph has dependencies, create the parent cards first, capture their returned ids, and include those ids in the child card's `parents` list during the child `kanban_create` call. Avoid creating all cards in parallel and linking them afterward; that creates a window where the dispatcher can claim a child before its inputs exist.

#### Step 4 — Complete your own task

If you were spawned as a task yourself (e.g. a planner profile was assigned `T0: "investigate Postgres migration"`), mark it done with a summary of what you created:

```python
kanban_complete(
    summary="decomposed into T1-T4: 2 research lanes in parallel, 1 synthesis on their outputs, 1 prose draft on the recommendation",
    metadata={
        "task_graph": {
            "T1": {"assignee": "<profile-A>", "parents": []},
            "T2": {"assignee": "<profile-A>", "parents": []},
            "T3": {"assignee": "<profile-B>", "parents": ["T1", "T2"]},
            "T4": {"assignee": "<profile-C>", "parents": ["T3"]},
        },
    },
)
```

#### Step 5 — Report back to the user

Tell them what you created in plain prose, naming the actual profiles you used:

> I've queued 4 tasks:
> - **T1** (`<profile-A>`): cost comparison
> - **T2** (`<profile-A>`): performance comparison, in parallel with T1
> - **T3** (`<profile-B>`): synthesizes T1 + T2 into a recommendation
> - **T4** (`<profile-C>`): turns T3 into a CTO memo
>
> The dispatcher will pick up T1 and T2 now. T3 starts when both finish. You'll get a gateway ping when T4 completes. Use the dashboard or `hermes kanban tail <id>` to follow along.

### Common orchestration patterns

**Fan-out + fan-in (research → synthesize):** N research-style cards with no parents, one synthesis card with all of them as parents.

**Parallel implementation + validation:** one implementer card makes the change while one explorer/researcher card verifies config, docs, or source mapping. A reviewer card can depend on both. Do not make the implementer own unrelated verification just because the user mentioned both in one sentence.

**Pipeline with gates:** `planner → implementer → reviewer`. Each stage's `parents=[previous_task]`. Reviewer blocks or completes; if reviewer blocks, the operator unblocks with feedback and respawns.

**Same-profile queue:** N independent tasks assigned to the same profile are eligible for parallel dispatch only up to that profile's configured concurrency cap. Inspect the dispatch dry-run's selected/capped tasks; do not assume either serialization or parallelism. After actual dispatch, verify each card's run separately.

**Human-in-the-loop:** Any task can `kanban_block()` to wait for input. Dispatcher respawns after `/unblock`. The comment thread carries the full context.

### Goal-mode cards (persistent workers)

By default a dispatched worker gets **one shot** at its card: it does its work, calls `kanban_complete`/`kanban_block`, and exits. For open-ended cards where one turn rarely finishes the job, pass `goal_mode=True` to wrap that worker in a Ralph-style goal loop — the same engine behind the `/goal` slash command:

```python
kanban_create(
    title="Translate the full docs site to French",
    body="Acceptance: every page translated, no English left, links intact.",
    assignee="<translator-profile>",
    goal_mode=True,        # judge re-checks the card after each turn
    goal_max_turns=15,     # optional budget (default 20)
)["task_id"]
```

How it behaves:
- After each worker turn, an auxiliary judge evaluates the worker's response against the card's **title + body** (treated as the acceptance criteria).
- Not done + budget remains → the worker keeps going **in the same session** (full context retained — not a fresh respawn).
- Worker calls `kanban_complete`/`kanban_block` itself → loop stops, normal lifecycle.
- Budget exhausted without completion → the card is **blocked** for human review (sticky), never a silent exit.

When to use it: long, multi-step, or "keep going until X is true" cards. When NOT to: cheap one-shot cards (translation of a single string, a quick lookup) — the judge overhead isn't worth it, and the dispatcher's existing retry/circuit-breaker already handles transient worker failures.

Write the body as **explicit acceptance criteria** — the judge is only as good as the goal text. "Translate the README" is weaker than "Translate every section of the README to French; no English sentences remain."

### Recovering stuck workers

When a worker profile keeps crashing, hallucinating, or getting blocked by its own mistakes (usually: wrong model, missing skill, broken credential), the kanban dashboard flags the task with a ⚠ badge and opens a **Recovery** section in the drawer.

**Verify actual startup before reporting progress or switching paths.** Treat a `dispatch --dry-run` selection as a preview only; it never proves a worker started. After dispatch or any `unblock`/`reassign`, inspect each authorized target with `hermes kanban --board default show <id> --json`: check `task.status`, `task.last_failure_error`, the newest `runs` (`status`, `outcome`, `worker_pid`), and relevant `events`; confirm the worker PID is live before reporting progress. If the `--json` output comes back unreadable in your tool results (truncated to one line / opaque), re-run plain `hermes kanban show <id>` WITHOUT `--json` — the human-readable view prints status, diagnostics, comments and events in full and is enough to confirm state; do not spend rounds re-attempting the JSON route or alternate transports to confirm something the plain view already answers. A claim or running-state transition alone is not proof. The gateway may claim a newly eligible card before a manual dispatch command runs: reread the task immediately before dispatch, and do not dispatch again if it already has a live run. If it remains `ready`, use a dry-run to confirm only authorized IDs would be selected, then dispatch and verify again. If invocation fails before substantive work, inspect its log and exact failure, then stop retrying that path. Reassign the same card to a known, compatible profile that is currently launchable (verify the candidate with `hermes profile list`), preserving its body, skills, parent links, and mirror; do not create a duplicate card or change credentials/configuration just to force a spawn. If no compatible launchable profile is available, keep the card blocked and record the precise next step. When an already-authorized fallback runs outside the dispatcher (for example, an isolated `delegate_task` session), keep the original card blocked to suppress a duplicate dispatcher spawn, comment the fallback's ownership and scope on that card, and update the required task mirror. Identify the fallback honestly: a subagent using a specialist's method or persona is not the named Hermes profile; never report it as that profile's work. If the card's acceptance criteria require the named profile, a fallback is partial delivery and does not satisfy that criterion: keep the card blocked, do not use `--force` or lower the criterion implicitly after a judge rejection, and report the remaining decision to the user. The parent must verify the fallback's artifacts and tests before applying the parent-owned closure rule below; do not create a duplicate card for the fallback.

If a dependency-gated child is still `todo` and the board refuses to block it, do not rely on a comment to hold it: a failed state transition may leave the comment but still allow automatic promotion to `ready` when its final parent completes. Before completing that parent, verify the child's assignee and dispatch path and prepare a fallback or reassignment. After parent completion, reread the child state and active runs before starting another worker, so a just-promoted task is not duplicated.

Three primary actions:

1. **Reclaim** (or `hermes kanban reclaim <task_id>`) — abort the running worker immediately and reset the task to `ready`. The existing claim TTL is ~15 min; this is the fast path out.
2. **Reassign** (or `hermes kanban reassign <task_id> <new-profile> --reclaim`) — switch the task to a different profile (one that exists on this setup) and let the dispatcher pick it up with a fresh worker.
3. **Change profile model** — the dashboard prints a copy-paste hint for `hermes -p <profile> model` since profile config lives on disk; edit it in a terminal, then Reclaim to retry with the new model.

Hallucination warnings appear on tasks where a worker's `kanban_complete(created_cards=[...])` claim included card ids that don't exist or weren't created by the worker's profile (the gate blocks the completion), or where the free-form summary references `t_<hex>` ids that don't resolve (advisory prose scan, non-blocking). Both produce audit events that persist even after recovery actions — the trail stays for debugging.

### Orchestrator pitfalls

**Inventing profile names that don't exist.** The dispatcher silently fails to spawn unknown assignees — the card just sits in `ready` forever. Always assign to a profile from your Step 0 discovery; ask the user if you're unsure.

**Bundling independent lanes into one card.** If the user asks for two independent outcomes, create two cards. Example: "fix blockers and check model variants" is not one fixer task; create a fixer/engineer card for the fixes and an explorer/researcher card for the variant check, then optionally gate review on both.

**Over-linking because of wording.** "Finally check X" may still be parallel with implementation if X is static config, docs, or source discovery. Link it after implementation only when the check depends on the implementation result.

**Forgetting dependency links.** If the task graph says `research -> implement -> review`, do not create all tasks as independent ready cards. Use parent links so implement/review cannot run before their inputs exist.

**Reassignment vs. new task.** If a reviewer blocks with "needs changes," create a NEW task linked from the reviewer's task — don't re-run the same task with a stern look. The new task is assigned to the original implementer profile.

**Ready without assignee = invisible to the dispatcher.** The dispatcher only claims `ready` cards that HAVE an assignee; `ready` + assignee NULL sits forever (confirmed on a board where 24 such cards stalled 5 days). Dependency-gated children are often created without assignee, so EVERY promotion from the `todo` chain re-produces a stalled card. Fix: pre-assign `default` to the whole `todo` chain up front (proven safe), so promotions become dispatchable instantly.

**Spawn-failure circuit breaker ≠ real blocker.** A card `blocked` with `gave_up` events (`failures: 2, effective_limit: 2`) and error `platform token can serve only one gateway...` is NOT a human prerequisite — it's a profile that can't spawn (Telegram token conflict: one platform token serves one gateway, so only one profile claiming the token wins). Classify blocked cards by their events before treating them as Igor-inputs: real `needs_input`/`capability` block events (money moves, physical signature, OAuth creds, irreversible actions, past events) stay blocked; crash-circuit-breaker cards get requeued. Requeue recipe (when CLI mutation is blocked, see next pitfall): sqlite `UPDATE tasks SET status='ready', assignee='default', consecutive_failures=0, last_failure_error=NULL, worker_pid=NULL, claim_lock=NULL, claim_expires=NULL` + INSERT a matching `task_events` row (kind='assigned', payload json with from/by) for the audit trail. Always `.backup` the DB first.

**The `hermes kanban` CLI can be fully blocked in worker/delegate-child contexts** — even READ verbs (`list`) fail with `kanban: delegate_task child contexts cannot mutate Kanban tasks or boards`, while the `kanban_*` tools (show/comment/heartbeat/complete) still work. When you must touch assignee/status/failures from such a context, go through sqlite on `~/.hermes/kanban.db` (tables: `tasks`, `task_events`, `task_links` — no `board` column; WAL mode, so do `sqlite3 .backup` not `cp` if the `-wal` file is non-empty). The dispatcher polls `ready`+assignee continuously; assigning is enough to trigger dispatch, no manual spawn needed.

**Verify the pump, then get out.** An orchestrator's closure criterion for "liberate the queue" is: every non-done card is either (a) `ready`/`running` with assignee default and fresh heartbeats, (b) `todo` with assignee already set and satisfied-by-design parents, or (c) `blocked` with a real documented prerequisite. Once (a)-(c) hold, the dispatcher drains the queue autonomously — do not babysit; complete your meta-card with the handoff inventory.

**Child runs cannot close board cards.** A subagent spawned via delegation (child context) cannot complete a Kanban task — when the work lands, the PARENT verifies it (`git log`, tests, `git status`) and runs `hermes kanban --board default complete <id> --result "..."` itself. When re-dispatching a task whose goal includes closing the card, strip the closure from the child's goal and reserve it for the parent, or the card stays `ready` forever after the work is done. (Fallback that worked from inside a child: a PATCH against the dashboard HTTP API for the task.)

**Queue-gate parent links must be removed before completing a card executed out-of-band.** If a card was gated with N parents purely as a chronological queue gate (no data dependency) and the user later authorizes direct execution, `unlink <parent> <card>` for every parent first — `complete` fails on "unsatisfied parent dependencies" otherwise. After unlinking, the dispatcher can promote and claim the card within seconds; if a duplicate worker is already running it when you go to close it, use `complete <id> --force` to close its run and complete anyway (the direct session did the real work — a redundant worker spawn must not block closure, but comment on the card that its run was superseded).

**Argument order for links.** `kanban_link(parent_id=..., child_id=...)` — parent first. Mixing them up demotes the wrong task to `todo`.

**Don't pre-create the whole graph if the shape depends on intermediate findings.** If T3's structure depends on what T1 and T2 find, let T3 exist as a "synthesize findings" task whose own first step is to read parent handoffs and plan the rest. Orchestrators can spawn orchestrators.

**Tenant inheritance.** If `HERMES_TENANT` is set in your env, pass `tenant=os.environ.get("HERMES_TENANT")` on every `kanban_create` call so child tasks stay in the same namespace.

---

## § Worker — Execution Guide

> You're dispatched as a worker. The **lifecycle** (6 steps: orient → work → heartbeat → block/complete) also lives in the `KANBAN_GUIDANCE` block that's auto-injected into your system prompt. This section is the deeper detail: good handoff shapes, retry diagnostics, edge cases.

### Workspace handling

Your workspace kind determines how you should behave inside `$HERMES_KANBAN_WORKSPACE`:

| Kind | What it is | How to work |
|---|---|---|
| `scratch` | Fresh tmp dir, yours alone | Read/write freely; it gets GC'd when the task is archived. |
| `dir:<path>` | Shared persistent directory | Other runs will read what you write. Treat it like long-lived state. Path is guaranteed absolute (the kernel rejects relative paths). |
| `worktree` | Git worktree at the resolved path | If `.git` doesn't exist, run `git worktree add <path> ${HERMES_KANBAN_BRANCH:-wt/$HERMES_KANBAN_TASK}` from the main repo first, then cd and work normally. Commit work here. |

### Tenant isolation

If `$HERMES_TENANT` is set, the task belongs to a tenant namespace. When reading or writing persistent memory, prefix memory entries with the tenant so context doesn't leak across tenants:

- Good: `business-a: Acme is our biggest customer`
- Bad (leaks): `Acme is our biggest customer`

### Good summary + metadata shapes

The `kanban_complete(summary=..., metadata=...)` handoff is how downstream workers read what you did.

**Coding task:**
```python
kanban_complete(
    summary="shipped rate limiter — token bucket, keys on user_id with IP fallback, 14 tests pass",
    metadata={
        "changed_files": ["rate_limiter.py", "tests/test_rate_limiter.py"],
        "tests_run": 14,
        "tests_passed": 14,
        "decisions": ["user_id primary, IP fallback for unauthenticated requests"],
    },
)
```

**Coding task that needs human review (review-required):**

For most code-changing tasks, the work isn't truly *done* until a human reviewer has eyes on it. Block instead of complete, with `reason` prefixed `review-required: ` so the dashboard surfaces the row as needing review. Drop the structured metadata into a comment first.

```python
import json
kanban_comment(
    body="review-required handoff:\n" + json.dumps({
        "changed_files": ["rate_limiter.py", "tests/test_rate_limiter.py"],
        "tests_run": 14,
        "tests_passed": 14,
        "diff_path": "/path/to/worktree",
        "decisions": ["user_id primary, IP fallback for unauthenticated requests"],
    }, indent=2),
)
kanban_block(
    reason="review-required: rate limiter shipped, 14/14 tests pass — needs eyes on the user_id/IP fallback choice before merging",
)
```

Use `kanban_complete` only when the task is genuinely terminal — e.g. a one-line typo fix, a docs change with no functional consequences, or a research task where the artifact IS the writeup itself.

**Research task:**
```python
kanban_complete(
    summary="3 competing libraries reviewed; vLLM wins on throughput, SGLang on latency, Tensorrt-LLM on memory efficiency",
    metadata={
        "sources_read": 12,
        "recommendation": "vLLM",
        "benchmarks": {"vllm": 1.0, "sglang": 0.87, "trtllm": 0.72},
    },
)
```

**Review task:**
```python
kanban_complete(
    summary="reviewed PR #123; 2 blocking issues found (SQL injection in /search, missing CSRF on /settings)",
    metadata={
        "pr_number": 123,
        "findings": [
            {"severity": "critical", "file": "api/search.py", "line": 42, "issue": "raw SQL concat"},
            {"severity": "high", "file": "api/settings.py", "issue": "missing CSRF middleware"},
        ],
        "approved": False,
    },
)
```

Shape `metadata` so downstream parsers (reviewers, aggregators, schedulers) can use it without re-reading your prose.

### Claiming cards you actually created

If your run produced new kanban tasks (via `kanban_create`), pass the ids in `created_cards` on `kanban_complete`. The kernel verifies each id exists and was created by your profile; any phantom id blocks the completion with an error.

```python
# GOOD — capture return values, then claim them.
c1 = kanban_create(title="remediate SQL injection", assignee="security-worker")
c2 = kanban_create(title="fix CSRF middleware", assignee="web-worker")

kanban_complete(
    summary="Review done; spawned remediations for both findings.",
    metadata={"pr_number": 123, "approved": False},
    created_cards=[c1["task_id"], c2["task_id"]],
)
```

```python
# BAD — claiming ids you don't have captured return values for.
kanban_complete(
    summary="Created remediation cards t_a1b2c3d4, t_deadbeef",  # hallucinated
    created_cards=["t_a1b2c3d4", "t_deadbeef"],                   # → gate rejects
)
```

If a `kanban_create` call fails, the card was NOT created — do not include a phantom id for it. Retry the create, or omit the id and mention the failure in your summary.

### Block reasons that get answered fast

Bad: `"stuck"` — the human has no context.

Good: one sentence naming the specific decision you need.

```python
kanban_comment(
    task_id=os.environ["HERMES_KANBAN_TASK"],
    body="Full context: I have user IPs from Cloudflare headers but some users are behind NATs with thousands of peers.",
)
kanban_block(reason="Rate limit key choice: IP (simple, NAT-unsafe) or user_id (requires auth, skips anonymous endpoints)?")
```

The block message is what appears in the dashboard / gateway notifier. The comment is the deeper context a human reads when they open the task.

### Heartbeats worth sending

Good heartbeats name progress: `"epoch 12/50, loss 0.31"`, `"scanned 1.2M/2.4M rows"`, `"uploaded 47/120 videos"`.

Bad heartbeats: `"still working"`, empty notes, sub-second intervals. Every few minutes max; skip entirely for tasks under ~2 minutes.

### Retry scenarios

If you open the task and `kanban_show` returns `runs: [...]` with one or more closed runs, you're a retry. The prior runs' `outcome` / `summary` / `error` tell you what didn't work. Don't repeat that path. Typical retry diagnostics:

- `outcome: "timed_out"` — the previous attempt hit `max_runtime_seconds`. You may need to chunk the work or shorten it.
- `outcome: "crashed"` — OOM or segfault. Reduce memory footprint.
- `outcome: "spawn_failed"` + `error: "..."` — no worker started. Diagnose the failure before retrying; do not mistake a claim/status transition for execution. If the user has already authorized continuation and an isolated fallback can safely remain tied to the same card, use the blocked-card recovery procedure above; otherwise block with the exact missing setup or decision via `kanban_block`. Do not repeat the same failed dispatch path blindly.
- `outcome: "reclaimed"` + `summary: "task archived..."` — operator archived the task out from under the previous run; you probably shouldn't be running at all, check status carefully.
- `outcome: "blocked"` — a previous attempt blocked; the unblock comment should be in the thread by now.

### Notification routing

You can configure the gateway to receive cross-profile Kanban task notifications by adding `notification_sources` to `~/.hermes/config.yaml`.
- `notification_sources: ['*']` accepts subscriptions from all profiles.
- `notification_sources: ['default', 'zilor-ppt']` or `"default,zilor-ppt"` restricts subscriptions to specified profiles.
- Omitting the key keeps the default behavior (profile isolation).

### Worker DO NOTs

- Do not use `delegate_task` instead of creating/tracking new Kanban work; `delegate_task` is for short reasoning subtasks inside YOUR run, while `kanban_create` tracks cross-agent handoffs that outlive one API loop. Existing-card recovery is different: only the parent/orchestrator may use an already-authorized isolated fallback after a pre-start dispatch failure, following the recovery procedure above and preserving the same card and mirror. Workers must not self-delegate.
- Call `clarify` to ask the human a question. You are running headless — there is no live user to answer. The call will time out (default ~120s) and the task will sit silently in `running` with no signal that it needs input. Use `kanban_comment` (context) + `kanban_block(reason=...)` (decision needed) instead.
- Modify files outside `$HERMES_KANBAN_WORKSPACE` unless the task body says to.
- Create follow-up tasks assigned to yourself — assign to the right specialist.
- Complete a task you didn't actually finish. Block it instead.

### Worker pitfalls

**Task state can change between dispatch and your startup.** Between when the dispatcher claimed and when your process actually booted, the task may have been blocked, reassigned, or archived. Always `kanban_show` first. If it reports `blocked` or `archived`, stop — you shouldn't be running.

**Workspace may have stale artifacts.** Especially `dir:` and `worktree` workspaces can have files from previous runs. Read the comment thread — it usually explains why you're running again and what state the workspace is in.

**Don't rely on the CLI when the guidance is available.** The `kanban_*` tools work across all terminal backends (Docker, Modal, SSH). `hermes kanban <verb>` from your terminal tool will fail in containerized backends because the CLI isn't installed there. When in doubt, use the tool.

### CLI fallback (for scripting)

Every tool has a CLI equivalent for human operators and scripts:
- `kanban_show` ↔ `hermes kanban show <id> --json`
- `kanban_complete` ↔ `hermes kanban complete <id> --summary "..." --metadata '{...}'`
- `kanban_block` ↔ `hermes kanban block <id> --kind needs_input|capability "reason"` — the kind tag separates real human-input blockers from capability gaps in the events trail; `unblock` takes `--reason "..."` instead — NEVER a bare positional: a trailing quoted string after the task id is parsed as another task id, so the refusal echoes your reason text as the target (`cannot unblock <your reason> (not blocked/scheduled?)`) and the real card was never touched.
- `kanban_create` ↔ `hermes kanban create "title" --assignee <profile> [--parent <id>]`
- `kanban_comment` ↔ `hermes kanban comment <id> "text"`
- etc.

CLI verbs are strict: task creation is `create` — `hermes kanban add` is not a verb and exits 2 (easy to type by analogy with "add to board"). Appending context to a card is `comment` — `hermes kanban note` is not a verb either; check `--help` before guessing a verb by analogy.

Use the tools from inside an agent; the CLI exists for the human at the terminal.
