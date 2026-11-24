---
name: dashboard-integration
description: Criar páginas ao dashboard financeiro
version: "1.0"
author: hermes-agent
license: MIT
---

# Dashboard Integration

Add new pages to the financial dashboard project (`~/MEGA/Comprovantes/fluxo_caixa/dashboard/`). Covers template creation, styling, data sourcing, data generation, publishing, and commit.

## When to Use

- Need to create a new page/view in the financial dashboard SPA
- Adding HTML templates, CSS styles, JS controllers, or data files to the dashboard
- Integrating dynamic data (from scripts or static JSON) into dashboard pages
- Updating the build pipeline (`gerar_dashboard.py`) for a new page's data source
- Publishing dashboard pages and registering them in the menu system

# Dashboard Integration

Add new pages to the financial dashboard project (`~/MEGA/Comprovantes/fluxo_caixa/dashboard/`). Covers template creation, styling, data sourcing, data generation, publishing, and commit.

## Pipeline Overview

```
template.html  →  publication/
css            →  publication/
js           →  publication/
data.json    →  publication/
gen_build.py   runs → publishes everything + rebuilds menu
```

Each page owns source files under `src/` ending up copied to `publicacao/`. Build script `gerar_dashboard.py` orchestrates final publish.

## Steps

### 0. Choose rendering strategy first

Pick ONE of three patterns based on the page's data needs:

| Pattern | When to use | Files needed |
|---------|-------------|---------------|
| **Static HTML (direct publish)** | Standalone reference/comparison pages with fixed values. Data never changes mid-session. No build script involvement. | One file: `publicacao/<pagename>.html`. That's it. |
| **Static inline HTML** | Reference tables, comparison cards, informational pages embedded in the normal build pipeline. | `src/<pagename>_template.html`. No JS, no JSON. Built via gerar_dashboard.py. |
| **JS controller + external JSON** | Pages driven by periodically-refreshed data from scripts or APIs. Most dashboards, charts, lists. | `src/<pagename>_template.html` + `src/<pagename>.js` (async loader) + `src/<pagename>_data.json`. |
| **Python-generated HTML** | Heavy computational pages (e.g., projeções financeiras com loops de meses) where Jinja templates are regenerated from Python engine output. | `src/<pagename>.py` (engine) + `src/<pagename>_template.html`. |

**Default choice:** Static HTML direct publish unless the page needs to be rebuilt by `gerar_dashboard.py` or share data with other pages.

**Static HTML (direct publish) — full procedure:**
Write one complete HTML file directly to `publicacao/<pagename>.html`. Include ALL resources inline or via absolute CDN / relative path links — no build pipeline dependency. Structure mirrors any existing published page: `<!DOCTYPE html>`, `<meta viewport>`, title tag, shared CSS imports (`dashboard.css`, `menu_global.css`), page-specific `.css` if any, skip-link, header with `.mg-topo` nav shell, `<main id="app">` content, footer, `defer` script tag for menu. End every pair of companion pages with cross-links in their respective nav menus (e.g., Nov page links to Dez page and vice versa).

For JS-rendered pages: include `<body data-pagina="<pagename>">`, import shared CSS (`cenarios.css`, `menu_global.css`) plus page-specific `.css`, link `menu_global.js`, add skip-link, load page-specific JS. Set `data-<pagename>="<pagename>_data.json"` on `<body>` so the JS controller knows where to fetch data.

**CRITICAL:** Never `patch` a complex large HTML template. Incremental diffs on >100 line HTML consistently corrupt DOM nesting. Always use `write_file` with complete replacement. If the file exists, `git checkout` first, then `write_file`.

Embed only a minimal placeholder structure in the template; real data comes from the JSON file.

### 2. Style the page

Create `src/<pagename>.css` with component styles. Import shared base styles from `cenarios.css` separately — don't duplicate reset/breakpoint logic. Use semantic class prefixes (e.g. `av-`, `cf-`) to avoid collisions with other pages.

Include responsive breakpoints at 768px and 480px minimum. Test grid layouts visually.

### 3. Write the JS controller

Create `src/<pagename>.js` as async loader: reads `data-<pagename>` attribute from `<body>`, fetches JSON via `fetch()`, parses, renders into containers. Wrap in IIFE `(function(){ ... })()` to avoid global namespace pollution.

Handle errors gracefully: network failure shows fallback message, parse errors show clear indicator. JSON lives next to HTML in `publicacao/`.

### 4. Generate or source the data

If data comes from another system's script, call it via `subprocess.run()`:

```python
import subprocess
result = subprocess.run(
    ["python3", "/home/usuario/.hermes/scripts/<script_name>.py",
     "--flags"],
    capture_output=True, text=True, timeout=120
)
if result.returncode != 0:
    print(f"Data gen warning: {result.stderr}")
```

Check `output.strip()` is non-empty to confirm success. Verify the output JSON file exists and is valid after execution.

If no external script exists, write static JSON in `src/<pagename>_data.json` following the schema expected by the JS controller. Validate required keys before proceeding.

**CRITICAL for ngrok-free tunnels:** Do NOT embed JSON in inline `<script>` blocks. The ngrok FREE tier applies strict CSP that blocks ALL inline scripts. Data MUST come from external `.json` files fetched via `fetch()`. Use the `<body data-<key>="<file>.json">` pattern. In `noscript` fallbacks, render static content as plain HTML.

### 5. Publish

Copy all `src/` files for the page to `publicacao/`. If the build script works end-to-end, trust it. If it fails (unrelated legacy Markdown/YAML errors can block it), fall back to direct copy:

#### External JSON updates: manual sync required
When you only modified a `_data.json` file (e.g., new fatura parsed via OCR, updated cartão status), **do NOT run `gerar_dashboard.py`** — it may hang on unrelated files or overwrite your JSON with stale data. Instead:

```bash
cp src/<pagename>_data.json publicacao/<pagename>_data.json
```
Then verify by reading the public file:
```bash
head -5 publicacao/<pagename>_data.json
```
The JS controller will pick up the new data on next browser refresh. No rebuild needed.

If the local server isn't running, start it then immediately stop it after confirming the JSON is served:

```python
import shutil
shutil.copy2("src/<pagename>_template.html", "publicacao/<pagename>.html")
shutil.copy2("src/<pagename>.css", "publicacao/<pagename>.css")
shutil.copy2("src/<pagename>.js", "publicacao/<pagename>.js")
```

Then run `python3 gerar_dashboard.py` alone if you suspect a pipeline issue.

### 6. Update the menu

Register the page in `menu_rebuild.py` — **TWO hooks must be updated together**:

1. **PAGINAS list** — add tuple: `('pagename.html', 'Display Name', 'Group Label')`. Insert alphabetically by group.
2. **CATEGORIA_POR_SLUG dict** — add `'slug-pagename': 'category-slug'` ONLY for scenario detail pages (`cenario-*.html`). Non-scenario pages (salarial, hoje, etc.) have no entry; `categoria_de()` falls back to 'outros' safely.

After updating `PAGINAS`, run `python3 gerar_dashboard.py` — it chains `menu_rebuild.main([])` BEFORE `migrar_menus`, which rewrites the hardcoded nav header on ALL published pages and templates. Do NOT hand-inject `<li>` links into published pages: the migrator is the single source of header regeneration and hand edits are overwritten on the next build. Verify after: `grep -rl 'data-mg-chave="<new-page>"' publicacao/ | wc -l` must equal the page count.

Benign build-output lines (not failures): `MENU_SYNC_FALHOU headers divergentes` (aviso não-fatal de header legado), `DIVERGENTES sem-header:...` (listagem informativa), `MENU_MIGRADO {...}`. The real gate is `VEREDITO APROVADO PELO GERADOR` + pytest.

### 7. Commit
`publicacao/` is **gitignored** — the published tree is build output; commit ONLY `src/` changes. Use explicit file paths for `git add` — NEVER `git add -A` (the repo lives inside `~/MEGA` and `-A` sweeps untracked non-dashboard files). Stage exactly:

```bash
git add src/<pagename>.py src/<pagename>_template.html src/menu_rebuild.py
git add $(git status --short -- src/ | awk '{print $2}' | tr '\n' ' ')
```

(the second `git add` picks up templates whose headers were regenerated by the migrator — commit them too, the paridade test compares src templates against published output.)

Commit with a descriptive message referencing what changed and why.

### 8. Push

Always push via SSH: `git push origin main`. Remote is `git@github.com:usuario/dashboard-financeiro-pessoal.git`. HTTPS/gh CLI tokens expire — SSH never does.

## Static Python-generated pages (the salarial pattern)

For a fixed-values report page (historical analysis, comparison, story-with-numbers): write `src/<page>.py` modeled on `src/salarial_evolucao.py`. Its `gerar()` must: (1) take the header from `menu_rebuild.nav('<page>.html')` with the `?v=` cache-bust read from `respostas_template.html`; (2) compute all values with `Decimal` (never float literals for money); (3) write `src/<page>_template.html` AND `publicacao/<page>.html` with **byte-identical content** — the suíte's `test_template_publicado_bate_com_src` enforces this and the default python3 lacks pytest, so run the suite via `~/.local/bin/pytest -q`.

Reuse `salarial_style.css` classes (`sal-kpi`, `sal-tabela`, `sal-veredito`, `sal-nota`, `sal-lista`) plus `cenarios.css` before creating a page-specific CSS — report-style pages rarely need their own.

Register the page in `menu_rebuild.py` `PAGINAS` under the right group, run `python3 gerar_dashboard.py` to propagate the menu, pytest, commit src only, push via SSH, and verify `curl -s -o /dev/null -w '%{http_code}' http://localhost:8766/<page>.html`.

## Pitfalls

| Trap | Why | Fix |
|------|-----|-----|
| Patching large HTML templates | DOM nesting breaks silently on line-shifts; next diff targets wrong byte range | `git checkout` + `write_file` every time |
| Embedding data in inline scripts | ngrok FREE CSP kills ALL inline scripts → blank page | External `.json` + `fetch()` + `data-*` attribute |
| `git add -A` in MEGA root repo | Sweeps unrelated Insync-synced files → massive noisy commits | Explicit paths only |
| Relying on build script blindly | Unrelated legacy Markdown/YAML errors block the whole pipeline | Run target page's generation independently |
| Forgetting noscript fallback | Screen readers and strict CSP see a blank page | Include visible content inside `<noscript>` |
| Skipping mobile breakpoint test | Drawer/dropdown misaligns without fixed-position fixes | Check viewport width behavior explicitly |
| Cron scripts outside ~/.hermes/scripts/ | `hermes cron create --script` requires filename relative to `~/.hermes/scripts/`, not absolute paths; creates empty job if given raw Python file path | Use wrapper shell file in `~/.hermes/scripts/` that `exec`s the real script, then point cron at the wrapper name. Never use symlinks.
| Updating JSON but seeing old data in browser | `publicacao/_data.json` wasn't synced after edit; browser cache also masks changes | Always `cp` JSON to `publicacao/` AND clear browser cache or hard-refresh (`Ctrl+Shift+R`)

### Cron wrappers for external scripts
When the dashboard needs cron-driven data from scripts stored in MEGA or elsewhere:

```bash
#!/bin/bash
# ~/.hermes/scripts/wrapper-rescisao.sh
exec python3 /home/usuario/MEGA/Documentos/carreira/rescisao/calcular-rescisao.py "$@"
```

Then create cron with just the wrapper name:
```bash
hermes cron create "0 9 * * *" --script wrapper-rescisao.sh --no-agent
```

Always delete the old cron job (`hermes cron delete <id>`) before recreating with the new target.

## Updating an Existing Page (Banner/Section Addition)

When adding a new UI element (banner, card, section) to a page that already exists:

1. **Update the JSON data** — append the new fields at the same level as existing data objects (`meta`, `rescisao_clt`, etc.) in the `_data.json` file. Use flat key names matching JS variable expectations.
2. **Add the render function** in the page's `.js` — define a standalone function (e.g. `renderMeta(data)`), then call it inside the main `renderAll()` loop where it should appear visually. Name conventions: `render<Noun><Type>()` (e.g., `renderMeta()`, `renderAlertas()`).
3. **Add CSS** to the page's `.css` — use semantic prefix matching the section name (`.av-meta`, `.av-box-info`). Ensure gradient backgrounds don't conflict with header z-index.
4. **Manual copy fallback** — if `gerar_dashboard.py` fails due to unrelated errors (YAML parsing, markdown files), manually copy the three assets: `.html` stays untouched (it doesn't embed JS/CSS inline), copy `.css` and `.js` from `src/` to `publicacao/`, copy updated `_data.json` too. The nginx served static files pick up immediately.
5. **Verify via curl** — `curl -s http://localhost:8766/<page>.html | grep -c "<new-class>"` must return >0. If server not running, check `publicacao/<file>.js` contains the new function name.

## Quick Reference

- Repo root: `/home/usuario/MEGA/Comprovantes/fluxo_caixa/dashboard/`
- External data generator: `/home/usuario/.hermes/scripts/generar_avisos_data.py`
- Build script: `gerar_dashboard.py` (root level)
- Menu registry: `menu_rebuild.py` → `PAGINAS` list
- Git remote: SSH-only `git@github.com:usuario/dashboard-financeiro-pessoal.git`
- Local serve: `http://localhost:8766/` (systemd service `dash-serve.service`)