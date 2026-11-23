# QA pass: full-project check of a generated dashboard

Run in this order; each stage can find the bug that invalidates the next.

## 1. Suite + official build

- Run the full pytest suite from the project root with the user-level binary (`~/.local/bin/pytest -q`) — the host's default `python3` may resolve to a venv without pytest and fail with ModuleNotFoundError, which is tooling, not a test result; record the count.
- After a merge or branch switch, run the official build BEFORE the suite: published artifacts are gitignored and 100% derived, so the freshly checked-out tree lacks (or holds stale) `publicacao/` and every test that reads it errors with FileNotFoundError en masse — that reads like a broken merge but only means the derived output is missing.
- Regenerate with the official generator and require exit 0 plus the generator's own veredito line. A clean pass with unchanged published files is itself a check (published trees are gitignored and 100% derived — do not version them).
- Re-run the suite after the build: a generator that mutates shared state can break a test that passed before.

## 2. Static sweep over every published page (one script, not page-by-page)

Sweep ALL `*.html` in `publicacao/` for: inline `<script>` without `src` and inline `on*=` handlers (CSP); internal `href`/`src` targets that do not exist on disk (split off `?query`/`#hash` first); duplicate `id` attributes; missing viewport, charset, or title; JSON files that fail to parse. Make attribute-presence patterns case-insensitive (`(?i)charset=["']utf-8`): generated pages commonly emit `charset="UTF-8"`, and a case-sensitive sweep reports a healthy page as a finding. Then `node --check` every published `.js` and run the header-sync checker. Expected result on a healthy build is all-zero — any single hit is a finding worth reporting. Diagnose a MASS header-sync failure by regenerating first: derived pages left on disk from an older build or branch fail the checker spuriously; only a failure that survives a fresh official build is a real menu bug.

## 3. Browser pass (error collector + interactions)

- After each navigation, install a fresh collector (window `error`/`unhandledrejection` listeners plus a wrapping `console.error`) BEFORE interacting; read it after each interaction. Navigating wipes globals, so reinstall per page.
- Interact with the real controls: change each `<select>` (dispatch a real `change` event), click each filter button and count the visible items before vs after, submit the search with text and assert the visible-link list narrows. Counting rendered rows/cards is the assertion — a filter that changes nothing visible is a bug even with zero console errors.
- Render-then-assert: a page that renders via JS needs a settle wait before you count elements, or you measure the skeleton and call the feature broken (or miss it working).
- Dispatch synthetic events on the TARGET element, not on `document`: listeners attached to an inner element (the `<details>` wrapper) never see a KeyboardEvent dispatched at the document root, so a working Esc-close reads as broken. Locate where each behavior is actually wired first (in generated menus, Esc-on-the-search-input only clears + blurs; the drawer close lives on the `<details>` itself) — and to open a menu shortcut test, focus the element or dispatch on it directly rather than simulating the key at the root.
- Check `<details>`-based menus for how dropdowns actually open (hover? click? native) before assuming a missing burger button is a bug — and remember native `<details>` opens without JS, so navigation working proves nothing about the menu's JS features (search shortcuts, Esc/click-outside close, active-link fallback).
- Gate the active-page marker: every published page carries EXACTLY ONE `aria-current="page"`, pointing at itself (or at its menu-parent entry for detail pages). Count the tags with a regex that doesn't assume attribute order (`<a\b[^>]*aria-current="page"[^>]*>` then extract `href` from each) — generated HTML often puts `href` BEFORE `aria-current`, and an order-assuming regex silently matches zero and reports every page broken (or, worse, a presence-only check validates nothing). The same marker often appears twice because the nav block is emitted twice (desktop cascade + mobile drawer): the a11y attribute belongs only on the desktop copy, the drawer keeps just the visual class.
- Gate menu coverage: every published page must be reachable from the menu (an orphan page is invisible to the search datalist and unmarked) — detail pages count via their parent entry. In the search filter, open the parent `<details>` group of any match and close groups when the query empties; a display-only filter leaves matches hidden inside closed groups and Enter then navigates to a link the user never saw.
- Test the marker-attribute extraction order too: when a generated page renders the attribute AFTER the href, a test regex that requires `aria-current=...href=` finds nothing even though the page is correct — extract tags first, attributes second.

## 4. Mobile sweep

- Emulate a narrow viewport (`Emulation.setDeviceMetricsOverride`, width 375) and assert `scrollWidth <= innerWidth` (no horizontal overflow) on every key page; clear the override after.
- At narrow width a header often shows only top-level groups — that is the design, not a bug. Verify the hamburger/drawer opens and its link list matches the desktop groups instead of counting total links.
- Test keyboard shortcuts and drawer features at BOTH widths. A feature living only inside the mobile drawer (display:none on desktop) makes its shortcut a silent no-op on desktop — the JS fires, the element stays invisible, no error. Clear the override and re-run the same shortcut on desktop; if the drawer must open there, give the open state its own floating-panel CSS (the JS `open` alone shows nothing inside a display:none parent).

## 5. Data anchors vs the canonical plan

- Spot-check the published JSON and the rendered page values against the canonical plan file — but read the plan's own Divergências/notes section FIRST: motor-rule vs official-anchor differences (including cent-level rounding) that the plan documents are not findings. Report only undocumented divergence.
- An empty catalog feeding an otherwise-working page (e.g. zero registered entries) is an honest empty state, not a data bug — verify the page renders the empty state rather than assuming the data pipeline failed.
- Check history JSONs for dates in the future and rows with cost but no usage (and vice versa).

### Numeric audit (when the ask is "revise os números e fórmulas")

- Parse the canonical plan's monthly table first: BRL cells can be negative ANYWHERE in the cell (`R$ -1.234,56` — a startswith('-') check misses it), bold-wrapped, and em-dash cells (`—`) mean "not decomposed" — treat them as missing, don't crash or coerce to 0.
- Reconstitute the whole series with the DOCUMENTED rules (read the doc's rules/divergências sections first): saldo = renda − despesa per line; CDB/interest series per the stated floor + rate; payment schedules from the agreement docs. Compare every published anchor and page value; cent-level drift after 100+ compounding months is rounding accumulation, not a bug, when the doc documents it.
- When several engines compute the SAME named scenario (base plan, stress variants, a "pay everything" variant), pages must read the canonical engine's live computation — never hardcoded values from a superseded engine. A variant that only some pages simulate keeps the variant's label AND an `estimate` flag, never the canonical scenario's name.
- When the SAME formula exists in two implementations (the canonical engine AND a dashboard-local reimplementation, e.g. a copied `simulate()`), the copy drifts silently: rules added to the canonical engine (a floor, a locked-reserve term) never reach the copy, and every page fed by the copy renders the old math. Diff the copy's published series against the canonical engine's output LINE BY LINE (≤ 1 cent per row), not just the display cards — then either make the build call the canonical engine directly or re-align the copy, and land a published-JSON parity test that fails the build on any row divergence. Also reuse one engine's outputs for both the detail cards and the scenario list: recomputing the same quantity twice (once per engine, once in a builder loop) splits it into two values one cent apart.
- Before editing a shared constant, grep for engines that import it — one engine's constants often serve as parity-tolerance references in another; changing the value changes the second engine's gates (keep test comparisons on explicit `approx(..., abs=)` tolerances).
- A verbally stated balance from the user is ground truth for LABELS: reconcile it against the canonical triple (total / locked / available) and confirm which one each displayed number carries — plan one-liners, summary tables and card labels can cite the locked component as the whole reserve while the engines and published JSON are all correct.
- Cross-check page amounts against source documents by grep: each fatura/oferta/parcela value on a scenario page should exist verbatim in a source doc (fatura, oferta, controle). A total that only exists in the generator is a finding.

## 6. Report and close

- Write the report to the project's reports directory with: scope, per-stage results (tests, build, static sweep counts, browser pages, mobile pages), findings sorted by severity with root cause and suggested fix, and what was NOT tested.
- File findings as gates, not one-off fixes: every bug that escaped the existing checks implies a new gate in the test suite (e.g. a script-inclusion gate for every page carrying the shared header).
- Close the Kanban task with a result line that names the concrete bug and the report path, and mirror the pedido in the user's queue file.
