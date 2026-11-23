---
name: price-watch-cron
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [cron, price-watch, vigia, watchdog, telegram]
    related_skills: [hermes-agent]
description: Create a product price monitor (vigia) cron job.
---

# Price Watch (Vigia de Preço) via Hermes cron

## When to Use

- Igor asks to "monitorar preço" of any product, "me avise quando cair", "vigia", or any new product purchase waiting for a discount window (Black Friday etc.).
- Any task needing a recurring silent watchdog script delivered via Hermes cron.

Standing setup for Igor: watch scripts live in `~/.hermes/scripts/vigia-<produto>.py`; state/history files in the product's canonical dir under `~/MEGA/Documentos/` (e.g. `hardware/placas-video/`, `hardware/celulares/`); alert delivered to Telegram. Use the existing `vigia-iphone17.py` as the template — read it before writing a new one.

## Procedure

1. **Template first:** read `~/.hermes/scripts/vigia-iphone17.py` (fetch + extract + state JSON + append CSV history + silent-if-no-change output). Copy its shape; only product URLs, target band, and alert text change.
2. **Write script** to `~/.hermes/scripts/vigia-<produto>.py`. Behavior contract:
   - stdout empty = silence (watchdog pattern); text = alert delivered verbatim by cron.
   - State file (`~/.hermes/cache/` or product dir) holds last seen price; append each reading to a CSV history.
   - Alert only when price crosses a target OR drops ≥ R$ 100 in one reading — never on every check. For products with a régua de preço from review sites, prefer **3 tiers** (bom / ótimo / PEGA JÁ) over one target, and dedupe alerts with a `state["alerted"][<produto>]` key storing the last alerted price: only re-alert when Pix < last-alerted. Alerting on every daily check at the same price trains Igor to ignore the channel.
   - **Compare the target against the price the user actually pays, not the scraped token.** Amazon BR applies ~9% off the buybox at checkout via Pix — scrape the buybox, then threshold on `pix = buybox × 0.91`, and state the régua/alerts in Pix terms (validate the factor once against a price confirmed by real navigation before trusting it).
3. **Create the cron job** (correct syntax):
   ```
   hermes cron create "0 9 * * *" --name vigia-<produto> --script vigia-<produto>.py --no-agent --deliver telegram
   ```
   Schedule is POSITIONAL (`hermes cron create "0 9 * * *" ...`), not a flag; `--board` does not exist. Other flags: `--repeat` (count; default ∞), `--failure-deliver local` to suppress failure spam.
   Alternative that also works: the `cronjob_manage` TOOL with `action=create, schedule="0 10 * * *", script="vigia-<produto>.py", no_agent=true, deliver="origin"` — returns the job_id immediately and resolves the script path under `~/.hermes/scripts/` the same way.
4. **Verify end-to-end:** run the script directly (`python3 ...`), then `hermes cron run <name>` and check `hermes cron list` shows `Last run ... ok`. A script that only "should work" is not deployed.
5. **Record** the watch in the canonical vigia registry: `~/MEGA/Documentos/desejos_precos/HISTORICO-<CATEGORIA>-<PRODUTO>.md` (headers = targets/régua + script path + cron id; rows = dated append-only coletas stated in the price condition the user pays, e.g. Pix), and add ONE row to `desejos_precos/INDEX.md` (product | arquivo | gatilho) so future sessions discover the watch without reading every file.

## Pitfalls

- **Constrain price extraction to a realistic band for the specific product** (e.g. R$ 1.500–3.500 for a mid-range GPU). A generic `R$ ...` regex on comparison/agggregator pages (Zoom, Buscapé, gpuprix) matches accessories and other products, producing fake "lowest price ever" alerts on the first run. Run once, inspect values, tighten the band, delete the state file, re-run.
- **Changing extraction units, price basis (cheio→Pix) or state schema invalidates the old state file** — delete it and re-baseline, and default every state key inside `load_state()` (a key added later crashes with KeyError on an existing state JSON saved by a previous version of the script).
- **Regex vs JSON price tokens:** pages expose prices both as `R$ X.XXX,XX` text and as `"priceValue":NNN.NN` — match both, dedupe, take the min, and sanity-filter the range.
- **Comparison-site prices are offers, not purchase prices** — say so to the user; validate the real price at the store before any buy decision.
- **Silence must be real silence:** if collection fails entirely (network/timeout), return nothing rather than an error dump — a broken collector should not spam Telegram.
- **Content-change vigias: seed the baseline BEFORE the first cron run.** Run the script 2× in a row at deploy time — the 1st run records the current state as baseline, the 2nd must exit silent. If state starts empty, the first cron run delivers the CURRENT state as "novidade" and trains Igor to ignore the channel.
- **Multi-source keyword vigias need per-alvo include/exclude lists, not a single grep:** when the script searches several portal pages and matches any of several alvos, generic keywords ("TI", "concursos") match hundreds of unrelated snippets. Give each alvo its own `gatilhos` (ex.: "TRF-2", "TRF 2", "Tribunal Regional Federal da 2") and `excluir` (ex.: "TRF-1", "TRF-3"...) lists, and keep the alvo list + portal URLs at the top of the script so adding a new alvo is a one-dict edit.
- **When the alvo set changes (new alvo added, one descarted), re-run the script 2× again** to re-baseline with the new keyword lists — otherwise the next run reports the re-scoped results as novidade.
- **Agent cron with no new findings:** tell the collector to keep the reference prices and log the search as "sem resultado novo" in the Histórico row instead of failing — a week with no change is still a coleta, not an error.

## Variant: agent-cron vigia (multi-source research, not a script)

Use this when each check requires *search and judgment* across several stores/sources (weekly BF tracking, "melhores pechinchas"), not a single fixed URL a script can regex.

1. Keep the canonical product list in a Markdown canônico (e.g. `~/MEGA/Documentos/<area>/INDEX.md` with per-product store table, meta BF, and an append-only "Histórico de Coletas" section) and a machine copy in `~/.hermes/cache/<slug>/`.
2. Create the job with the `cronjob_manage` TOOL (not the CLI): `action=create, name, prompt, schedule="every monday 9am", deliver="telegram:<chat_id>"`. The prompt must instruct: read the INDEX, run a web_search per product, append a dated row to the Histórico section, and reply with a short Telegram summary (days-to-event, what got cheaper, what hit target, best links).
3. Verify end-to-end with `cronjob_manage action=run` for the job — the run report shows delivery target and next scheduled run; the output file lands in `~/.hermes/cron/output/<job_id>/`.
- **Transport pitfall:** a prompt with long accented/multi-line text can fail `tool_call` JSON parsing repeatedly. Keep the cron prompt SHORT, single-line, accent-free where possible, and put the detailed instructions in the canonical INDEX.md the prompt only points to.
- **Script vigia vs agent cron:** silent single-URL watchdog → script + `--no-agent` (silence pattern); multi-store weekly survey → agent cron (always answers, never silent). Don't force one pattern into the other.

## Delivery & delivery targets

- `--deliver telegram` sends stdout to Igor's home channel; `--deliver local` writes to `~/.hermes/cron/output/`. For alert-type vigias use telegram; for audit/report jobs, local.
- `--no-agent` = script IS the job (stdout delivered verbatim, no LLM). Without it, stdout is injected into an agent prompt instead — wrong for pure watchdogs.
