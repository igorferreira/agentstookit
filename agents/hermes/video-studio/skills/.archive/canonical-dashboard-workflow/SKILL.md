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
8. **Regenerate officially.** Never hand-edit derived HTML or JSON. Run the generator, inspect representative JSON values/counts, and verify affected local routes return HTTP 200.
9. **Verify public output.** Query the active tunnel API for the current URL, then request every affected public route and assert HTTP status plus a distinctive change marker. Never reuse a stale free-tier URL.
10. **Close with evidence.** Update task records with real counts, route results, current public URL, and remaining visual-review limitations.

## Always-on rules

- Markdown/YAML canonical sources are the source of truth; generated pages are views.
- Whole-line matches are not field extraction evidence; headers and narrative rows can contain the same words.
- Never infer limits, dates, or statuses from unrelated text.
- Prefer one shared parser/model over page-specific copies.
- Public artifacts contain only the minimum fields required by the screen.
- If a correction changes a semantic category, update parser/model and tests, not only the label.
- A passing local server does not prove the tunnel serves the new build.

## Common pitfalls

- **Whole-line regex extraction:** can capture `Valor` from a table header or `Valor utilizado` instead of the requested available limit. Match the first cell as the field key and the second as its value.
- **Identifier normalization leakage:** can alter names or currency strings. Normalize only for matching and retain source strings for display.
- **Canonical overwrite:** can replace a current registry value with an older detail value. Enrich only explicit missing sentinels.
- **Stale tunnel verification:** can return an unrelated application or old HTML. Query the tunnel endpoint and assert a page-specific marker.
- **Derived-output drift:** can make a manual HTML fix disappear on regeneration. Change parser/template/source and regenerate.

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
