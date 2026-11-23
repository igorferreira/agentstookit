---
name: interactive-agent-dashboards
description: "Use when building responsive agent dashboards in Vanilla JS."
version: 1.0.0
created_by: agent
---

# Interactive Agent Dashboards

Use this skill to build or repair browser-based “living office” dashboards that visualize agents, their roles, live states, tasks, chat interactions, and safety controls. Default to **HTML + CSS + Vanilla JavaScript** unless the user explicitly requests a framework.

## Core outcome

Deliver a real, exercised dashboard—not a mock description—with:

- legible agent identity and role;
- synchronized visual and textual state;
- compact responsive layout;
- mouse and touch interaction;
- persistent user positioning;
- deterministic safety checks where commands can trigger actions;
- Docker/public-link verification when the project uses that deployment model.

For the validated TimeAutomático implementation and exact acceptance evidence, read `references/timeautomatico-living-office.md`.

## 1. Establish the visual contract

Before editing, identify:

1. target viewports (desktop plus named phones/orientations);
2. maximum agents per row;
3. whether roles belong in the scene, a panel, or both;
4. what each animation means;
5. which elements may be dragged independently;
6. what must move as a group;
7. persistence scope (page, user, portrait/landscape);
8. public delivery requirements.

Treat user screenshots and complaints as acceptance-test input. Run OCR and visual analysis when text collision, truncation, or stale rendering is involved.

## 2. Model an agent station as one unit

A station typically contains:

```text
mesa + cadeira + personagem + nome + função + placa de tarefa
```

Even if legacy DOM nodes are siblings, maintain a shared station model:

```js
stations[agent.name] = { desk, x, y };
```

Use one function to apply positions to all linked nodes. Do not update desk, character, and label through unrelated code paths.

## 3. State semantics must be explicit

Define one source of truth per agent:

```js
agent.state = 'working' | 'coffee' | 'idle';
agent.task = '...';
```

Example legend:

- walking/moving = working;
- coffee cup = idle/on break;
- still/desaturated = waiting.

Rules:

- only a working agent may receive movement animation;
- coffee and idle states must be motionless;
- the status panel and scene must read the same state;
- populate the status panel synchronously before randomized timers start;
- use role as fallback when no task is present.

Avoid UI states that are merely random decorations with no semantic meaning.

## 4. Responsive layout

Use deterministic rows, not random positions.

Recommended decision factors:

- width controls columns;
- height controls vertical spacing;
- short landscape screens must be treated as compact even when width is large;
- reserve explicit vertical bands for header, alert, controls, scene, and footer.

Example:

```js
const compact = width < 769 || height < 500;
const cols = width >= 1100 ? 6 : width >= 640 ? 4 : 3;
const baseY = height < 500 ? 90 : 150;
const gapY = compact ? (width < height ? 96 : 78) : 118;
```

Validate at the actual CSS viewport dimensions. For phone QA include both portrait and landscape.

### Mobile text policy

Long role tags often collide in a compact scene. Prefer:

- complete, legible names above characters;
- detailed roles/tasks in an expandable status panel;
- hide free-floating role tags on very small viewports;
- preserve access to role information through the panel.

## 5. Drag with Pointer Events

Use native `PointerEvent` so one implementation supports mouse and touch.

Requirements:

- `touch-action: none` on draggable handles;
- `setPointerCapture` when available;
- ignore pointerdown originating from `button`, `input`, `textarea`, `a`;
- bound positions so controls cannot be lost entirely off-screen;
- move a station as a linked group;
- visually indicate dragging;
- allow a reset to deterministic defaults.

Do not infer touch support from mouse simulation alone. Exercise `Input.dispatchTouchEvent` or a real device.

## 6. Persist positions safely

For small single-page demos, cookies are acceptable when requested.

Recommended key structure:

```text
<app>_<pathname>_<portrait|landscape>
```

Store a compact JSON map:

```json
{"agent:helena":{"x":58,"y":172}}
```

Use:

- one-year `Max-Age` if durable positioning is desired;
- `Path=/`;
- `SameSite=Lax`;
- separate portrait and landscape layouts;
- reset only the current layout key unless the user requests global reset.

Remember cookie size limits. For larger dashboards migrate to `localStorage` or server-side user preferences—but honor an explicit cookie requirement.

Automatic re-layout must not overwrite saved custom positions. Check persistence before applying defaults.

## 7. Zoom and movable controls

Support the interaction modes required by the product:

- plus/minus buttons;
- Ctrl+wheel on desktop;
- pinch on touch devices;
- visible percentage;
- safe min/max scale;
- reset control.

Append zoom controls to a stable visible ancestor (usually `body`), not a panel that may be collapsed. Keep controls outside the footer and header. Make movable controls draggable if the product contract requires it.

## 8. Stale-version prevention

If users repeatedly see fixed bugs, verify the actual served artifact before blaming the source code.

For nginx-hosted rapidly changing demos, consider:

```nginx
add_header Cache-Control "no-store, no-cache, must-revalidate";
add_header Pragma "no-cache";
```

Then verify headers and the public artifact. A correct local file is not proof that the public tunnel serves it.

## 9. Command guardrails

If the dashboard accepts commands, use deterministic pre-dispatch checks for clearly forbidden classes. Do not rely only on agent prompting.

Typical hard blocks:

- filesystem destruction;
- recursive/batch deletion;
- privileged system changes;
- disk formatting;
- destructive SQL;
- remote-code pipelines;
- bulk outbound messaging;
- credential or personal-data exfiltration.

The UI guardrail is only one layer. Production systems need tool allowlists, sandboxing, least privilege, audit logs, and human approval for risky actions.

## 10. Multi-page navigation contract

For a dashboard with multiple HTML routes, define one canonical route manifest and use it to render the same complete menu in every page. Do not let individual page templates keep partial link subsets.

Preserve the active-page marker, add an accessible navigation label, and make the menu wrap cleanly on narrow screens. After generation, parse every page and assert that its link set contains every route in the manifest; then request every route locally and, when public, through the tunnel and require HTTP 200.

**Pitfall:** Checking only the landing page hides incomplete menus and broken generated routes; navigation changes require an all-pages × all-routes matrix check.

## 11. Static financial dashboard classifications

For cadastral or portfolio screens that split records into operational groups, derive the grouping from the canonical Markdown section and preserve the user's exact business label. Do not infer a new category from a nearby status word: for example, a list described by the user as “pagamento posterior” must be rendered and stored as `Pagamento posterior`, not renamed to “negociação” or “quitado”.

Procedure:

1. Parse the canonical source into structured records before changing the UI.
2. Track both the top-level section and the subsection/table schema; identical Markdown row shapes can mean different columns under different headings.
3. Assign an explicit machine-readable group to every active record, such as `Em uso` or `Pagamento posterior`.
4. Keep inactive, cancelled, blocked, or historical records out of the active lists unless the requirement explicitly includes them.
5. Render separate headings, counts, and tables from the groups; never duplicate or hand-maintain a second list in HTML.
6. Add tests for one representative record in each group and assert that every rendered record has exactly one group.

**Pitfall:** Do not classify records using substring checks against unnormalized text; bold Markdown, accents, virtual-card suffixes, and final numbers can cause a record to land in the wrong list. Normalize comparison keys, but preserve the original display value and label.

**Pitfall:** Do not assume one row schema across a Markdown file; a “bank issuer” column in one subsection shifts the final, flag, and due-date columns. Select the parser mapping from the subsection heading and test representative rows from each schema.

## 12. QA sequence

### Syntax

Validate every script block, not just the first:

```js
for (const match of html.matchAll(/<script>([\s\S]*?)<\/script>/g)) {
  new Function(match[1]);
}
```

### Functional checks

Test all of the following:

- page creates expected agent count;
- status panel has one row per agent immediately;
- send button and Enter share the same handler;
- normal command passes;
- dangerous command is blocked;
- mouse drag changes position;
- touch drag changes position;
- linked station nodes retain expected offsets;
- cookie is created on pointerup;
- reload restores exact coordinates;
- portrait and landscape cookies coexist;
- reset removes only intended key and returns to default;
- zoom controls exist and change scale;
- TTS endpoint responds if present.

When testing synthetic touch, place short delays between touchStart, touchMove, and touchEnd; zero-delay events may be coalesced and produce a false failure.

### Visual checks

Capture at least:

- desktop (for example 1400×900);
- target-phone portrait;
- target-phone landscape.

Inspect with vision/OCR for:

- `undefined` text;
- clipped names;
- overlapping role/task labels;
- panels intercepting touch over agents;
- second row hidden by footer;
- controls inside collapsed panels;
- excessive empty space or unreadable scale.

### External verification

After rebuild:

1. local HTML returns 200;
2. health/TTS returns 200;
3. public URL returns 200;
4. public HTML contains a unique marker from the new version;
5. cache headers are correct;
6. tunnel URL is saved;
7. link is delivered to the user.

For a static dashboard served by a local Python process, establish the local server before creating the tunnel, then discover the live URL from ngrok's local API rather than trusting a previously saved link:

```bash
python3 servidor_local.py
curl -m 8 -sS -o /dev/null -w '%{http_code} %{url_effective}\\n' http://127.0.0.1:8766/dashboard.html
ngrok http 8766
curl -m 10 -sS http://127.0.0.1:4040/api/tunnels
curl -L -m 20 -sS -o /tmp/dashboard-public.html -w '%{http_code} %{content_type} %{size_download}\\n' "$BASE/dashboard.html"
```

Extract the `public_url` whose upstream is `http://localhost:8766`, and verify the exact dashboard path through that URL before delivering it. Free-tier ngrok URLs are ephemeral: never treat a stale file or old URL as proof that the current process is reachable. Record the request in the project's queue before starting the server/tunnel and mark it complete only after the public HTTP check passes.

## 12. Frequent failure modes

- **Function defined but listener never attaches:** an earlier runtime exception stopped the script. Capture console exceptions; do not inspect only the handler.
- **`undefined undefined`:** data is an array but renderer uses object properties (or vice versa). Test the rendered alert.
- **Status panel shows zero temporarily:** the list is populated only by delayed randomized state transitions. Populate immediately.
- **Portrait works, landscape fails:** compact detection relies on width only. Include short height.
- **Touch hits a panel instead of the agent:** inspect `document.elementFromPoint()` at the intended touch center.
- **Synthetic touch fails while code is correct:** add realistic delays before concluding failure.
- **Custom positions disappear:** periodic responsive layout overwrites saved coordinates. Saved state must take precedence.
- **Zoom missing:** it was appended inside a hidden/collapsed panel.
- **Source fixed, phone stale:** public container/tunnel or browser cache still serves old HTML.
- **Large legacy CSS regressions:** duplicated selectors override the intended block. Create regression tests before broad cleanup.

## 13. Handoff discipline

Maintain a project Markdown with:

- architecture;
- requirements;
- backlog status;
- completed tests with evidence;
- known issues;
- exact files;
- build/run commands;
- next steps;
- definition of done.

Do not mark an item complete based on code intent. Record it as complete only after the relevant functional or visual proof passes.
