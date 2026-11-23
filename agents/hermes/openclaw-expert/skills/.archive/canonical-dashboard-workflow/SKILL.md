---
name: canonical-dashboard-workflow
description: Use when updating canonical dashboards.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [dashboard, canonical-data, markdown, generators, verification]
---

# Canonical Dashboard Workflow

Use this skill for dashboards whose visible data is generated from Markdown/YAML registries, control files, or per-item detail sheets. Keep canonical files authoritative and treat `publicacao/` as derived output.

## Procedure

1. **Register the request and define acceptance criteria.** Record the request in the project queue and internal task summary before editing. State the source of truth, affected routes, expected groups/counts, and required local/public verification.
2. **Inspect sources before editing UI.** Locate the canonical registry and detail files. Decide which fields are authoritative, which may be enriched, and what must remain unknown.
3. **Map records by stable identifiers.** Prefer card/account final digits or IDs; use normalized names only as fallback. Preserve original display values.
4. **Parse fields by key cells.** Match the requested table key and its value cell, not a word anywhere in the line. Normalize Markdown decoration for lookup while preserving currency strings, names, statuses, and identifiers exactly.
5. **Enrich conservatively.** Fill only explicit missing sentinels such as `Não informado`, em dash, or empty. Never overwrite a populated canonical value with a stale or ambiguous detail value. Do not publish full private detail files.
6. **Render from the model.** Derive grouping and counts from the parsed model; do not duplicate business lists in HTML and JavaScript. Show missing data honestly.
7. **Test the behavior.** Cover a stable-identifier match, an extracted field, an intentionally missing field, a non-match/conflict, and group/count totals. Run the full suite and syntax checks.
8. **Regenerate officially.** Never hand-edit derived HTML or JSON. Run the generator, inspect representative JSON values/counts, and verify affected local routes return HTTP 200. When a dedicated `servidor_local.py` exists (e.g. serving `publicacao/` on a specific port), always run it instead of a generic `http.server` to preserve custom MIME, CORS, and root fallback routes.
9. **Verify public output.** Query the active tunnel API (`http://127.0.0.1:4040/api/tunnels`) for the current URL, then request every affected public route and assert HTTP status plus a distinctive change marker. On ngrok tunnels, always pass the header `-H "ngrok-skip-browser-warning: 1"` in automated curl probes to bypass the interstitial warning page and inspect the actual payload. Never reuse a stale free-tier URL.
10. **Close with evidence.** Update task records with real counts, route results, current public URL, and remaining visual-review limitations.

For multi-page screens (an index plus one page per record, a filter that selects the page), the sources-and-pages recipe, the accent pass, and the browser verification loop are in `references/multi-page-dashboards.md`.

## Always-on rules

- Markdown/YAML canonical sources are the source of truth; generated pages are views.
- Whole-line matches are not field extraction evidence; headers and narrative rows can contain the same words.
- Never infer limits, dates, or statuses from unrelated text.
- Prefer one shared parser/model over page-specific copies.
- Public artifacts contain only the minimum fields required by the screen.
- If a correction changes a semantic category, update parser/model and tests, not only the label.
- A passing local server does not prove the tunnel serves the new build.
- New `build_*` functions follow the existing convention: same module as the other builders, own `src/<nome>_template.html` + `src/<nome>.js` (template becomes `<nome>.html` on copy), state exposed under a new top-level JSON key, page renders it. Do not invent a second pipeline.
- Page parameters (which record/section to open) travel in markup, never in an inline `<script>`. The ngrok-free tunnel injects a CSP that blocks inline scripts AND inline `<style>` blocks: `window.X = '...'` never runs (page silently falls back to its default view), and inline styles are dropped so the page loads unstyled through the tunnel while looking fine on `127.0.0.1` — an easy trap when QA is local-only. Keep parameters in `<body data-alvo="slug">` (read `document.body.dataset.alvo` in the shared JS) and keep every CSS rule in external files. When a CSS change ships, bump every stylesheet URL with a build version (`href="x.css?v=<build-id>"`) or the user's browser cache serves the old stylesheet and the fix looks not applied.
- Parsed canonical rows may hold `Decimal`; wrap row values in `float()` before arithmetic in a new builder, or the first subtraction raises `TypeError: unsupported operand type(s) for -: 'decimal.Decimal' and 'float'`.
- Dashboard display text is pt-BR **with accents**; slugs and file names stay ASCII (`demissao`, `contas-cartoes`). Keep slugs, `fonte` and `fonte_path` out of any accent-rewriting pass.
- Source identification on the page: the body shows only the canonical file **name**; the absolute directory appears exactly once, in a single shared field rendered in the footer.

## Common pitfalls

- **Whole-line regex extraction:** can capture `Valor` from a table header or `Valor utilizado` instead of the requested available limit. Match the first cell as the field key and the second as its value.
- **Identifier normalization leakage:** can alter names or currency strings. Normalize only for matching and retain source strings for display.
- **Canonical overwrite:** can replace a current registry value with an older detail value. Enrich only explicit missing sentinels.
- **Stale tunnel verification:** can return an unrelated application or old HTML. Query the tunnel endpoint and assert a page-specific marker. Pass `-H "ngrok-skip-browser-warning: 1"` to prevent false assertions against the free-tier interstitial page.
- **Subset-only sync gate:** a menu/header sync check that validates only the pages it was written for reports OK while the rest of the site keeps the old shell, and the user sees the inconsistency that the gate missed. Enumerate EVERY published page, fail on missing header, and derive expected counts from the generator's page registry (never hardcode them — the count changes with each new page).
- **Shared shell applied per-template:** when one template gets the shared header but the generator also writes other pages by different code paths, only post-processed templates update. Apply the shell through a build-time post-processor (replaces old nav, injects header + stylesheet link, extracts inline `<style>` to external CSS) that runs LAST in the generator, after every write, and is idempotent (`ja-mg`/already-done status) so re-runs are no-ops.
- **Generator/template drift after menu changes:** run the template-menu updater BEFORE the main generator (it only rewrites templates, never built pages), and on divergence between regenerated pages and templates clear `__pycache__` and regenerate — stale bytecode makes builds diverge with no code change.
- **Serving root vs publicacao directory:** running a generic HTTP server at the project root instead of pointing to `publicacao/` (or using the project's `servidor_local.py`) causes 404/500 errors on routes expected by client-side assets and relative links.
- **Derived-output drift:** can make a manual HTML fix disappear on regeneration. Change parser/template/source and regenerate.
- **Bulk rewrite that silently no-ops:** replacing a template string that still holds its `{placeholder}` (or a `\u`-escaped sequence) against the concrete generated files matches nothing and reports success. After any scripted multi-file edit, assert the new marker is present in every file (`assert 'data-alvo=' in t`) and grep the copied output in `publicacao/` — never trust the loop's own print.
- **Truncated code payload:** appending a very large builder through `execute_code` in one shot can arrive cut off (`SyntaxError: unterminated triple-quoted string`). Write in chunks of a few thousand characters, appending each to the module and running `py_compile` between chunks, and keep the arithmetic in Python rather than in the page JS.
- **DOM read from the wrong tab:** after navigating, a `js()` probe can evaluate in a previously opened tab, so a page that renders correctly looks broken (its `<title>` is right but the DOM reads as the old page). Assert `document.title` first, call `ensure_real_tab()` when tabs disagree, and treat DOM assertions — not screenshots — as the evidence when the screenshot capture times out.
- **Plausible page, wrong number:** the canonical plan may count an item the user has decided not to pay as a paid expense. Show both figures side by side (the plan's hole and the real hole) with the one-line explanation, instead of publishing the plan's number as the current situation.

## Verification checklist

- [ ] Request registered before implementation
- [ ] Canonical and detail sources identified
- [ ] Stable-identifier matching tested
- [ ] Missing-field behavior tested
- [ ] Group/count totals tested
- [ ] Official generator run
- [ ] Full tests and syntax checks passed
- [ ] Affected local routes returned HTTP 200
- [ ] Affected public routes returned HTTP 200 and contained a change marker
- [ ] Task records updated with evidence
