# Multi-page dashboard screens (index + one page per record)

Shape the user asks for: one **index page** listing every record with a **filter that selects it**, and each record also reachable as **its own page**. Used for financial scenario screens, per-card analyses, per-month views.

## Files and generation

- Index: `src/<nome>_template.html` → copied to `publicacao/<nome>.html` by the generator (the `_template` suffix is the only rename rule).
- Record pages: plain `src/<nome>-<n>-<slug>.html` files, copied verbatim — thin shells, no duplicated content.
- Shared assets: `src/<nome>.css` + `src/<nome>.js`. The JS has two modes and picks one from markup, never from an inline script:

```html
<body data-alvo="slug-do-registro">   <!-- record page -->
<body>                                 <!-- index page -->
```

```js
const ALVO = document.body.dataset.alvo || null;
if (ALVO) modoDetalhe(ALVO); else modoIndex();
```

- All numbers come from the model: the builder computes and formats them in Python, the JS only renders. Currency formatting (`1.234,56`), sign colouring, and percentages belong in the builder or one `fmt()` helper, not scattered in templates.
- Every record page shows the canonical file **name** it came from; the absolute directory lives in one shared field (e.g. `fonte_path`) rendered once in the footer.
- Slug ↔ file name is derived, not stored twice: `'<nome>-' + ordem + '-' + slug + '.html'` in both the generator loop and the JS, so prev/next navigation always resolves.

## Accents in pt-BR screens

Slugs and file names stay ASCII; the visible text carries accents. Rather than hand-typing accents into every string, run a display pass in the builder:

1. A phrase list first for cases a word rule cannot decide (`'Nao e plano' → 'Não é plano'`, `'e a base de' → 'é a base de'`) — the verb `é` versus the conjunction `e` is not recoverable word-by-word.
2. Then a whole-word map with word boundaries (`(?<![A-Za-zÀ-ÿ])(?:...)(?![A-Za-zÀ-ÿ-])`), longest key first, applied recursively to display fields only.
3. Exclude keys that must stay machine-readable: `slug`, `fonte`, `fonte_path`, and any file name.
4. Assert afterwards that slugs and file names are unchanged in the regenerated JSON.

## Verification loop that catches real breakage

1. `python3 gerar_dashboard.py | tail -1` then `pytest testes/ -q` — full suite, no partial runs.
2. `curl` each new route on the local server for HTTP 200, including the JSON, both assets, the index, one record page, and the last record page.
3. Browser pass over the tunnel: assert the index reports the expected card count and filter option count, drive the filter (`select.value = ...; dispatchEvent(new Event('change'))`) and assert exactly one card stays visible, then open a record page and assert its title, section row counts and verdict text.
4. Assert `document.title` on each probe — a probe that lands on another tab reports the previous page's DOM and looks like a rendering failure.
5. Cache-bust tunnel probes with a `?v=N` query when a page was regenerated.

## Scenario screens for financial decisions

- Build the list in the order the user dictates (he describes the cascade himself); do not re-sort by size or urgency. The scenario he names first is the first card.
- Every scenario carries: levers (what it uses), what it covers, costs and risks, and a verdict — plus an `ESTIMATIVA` tag on any figure that is a premise (discount rates, FGTS balance, savings estimate) rather than a line read from the canonical cash-flow file.
- Recompute every total in Python from canonical rows and show the arithmetic result; never restate a screen value.
- When the canonical plan counts an item the user has already decided not to pay, show both holes (plan vs real) in a banner and repeat the reasoning on each affected page.
- Close the delivery with the kanban board link, the task id in the board, and the mirror entry in the project queue file.
