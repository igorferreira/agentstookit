# Usuário 2026-06: OpenClaw and Hermes coexistence setup

This is a compact worked example from a real session. Use it as a pattern, not as a universal default.

## User intent

- Analyze `/home/usuario/.openclaw/openclaw.json`.
- Recreate the same OpenClaw agents in Hermes.
- Keep OpenClaw and Hermes both running; do not perform a cutover.
- Start Hermes Gateway without stealing OpenClaw's bot/channel.
- Give the finance specialist full operational permission over `/home/usuario/MEGA/Comprovantes`.
- Document the outcome in `/home/usuario/.hermes/docs`.

## OpenClaw agents recreated as Hermes profiles

Created profiles with matching names:

- `main`
- `hr-tech-senior`
- `product-senior`
- `java-senior`
- `python-senior`
- `finance-senior`
- `relationship-senior`
- `pickup-senior`
- `health-performance-board`

Each profile got a short `SOUL.md` under `~/.hermes/profiles/<name>/SOUL.md` describing role, Portuguese default response style, and relevant safety boundaries.

Validation commands:

```bash
hermes profile list
hermes kanban assignees
```

## Gateway coexistence pattern

Before starting Hermes Gateway, check that OpenClaw is still expected to run and avoid token contention.

Useful checks:

```bash
hermes gateway status
systemctl --user is-active openclaw-gateway.service || true
pgrep -af 'openclaw|hermes.*gateway'
```

Validate Telegram without printing tokens:

- Print token presence/fingerprints only, or
- call Telegram `getMe` for the Hermes token and report username/id only.

In this session Hermes used bot username `@milyhermes_bot`, while OpenClaw remained running separately.

Hermes Gateway service setup:

```bash
printf 'Y\nY\n' | hermes gateway install --force
hermes gateway status
hermes gateway list
```

If Hermes `.env` contains deprecated `MESSAGING_CWD`, move it to config:

```bash
hermes config set terminal.cwd /home/usuario/clawd
# remove MESSAGING_CWD=... from ~/.hermes/.env
hermes gateway restart
```

## Finance profile permissions pattern

For `finance-senior`, the user explicitly granted full permission inside:

`/home/usuario/MEGA/Comprovantes`

Applied profile-scoped config:

```bash
hermes --profile finance-senior config set terminal.cwd /home/usuario/MEGA/Comprovantes
hermes --profile finance-senior config set approvals.mode off
hermes --profile finance-senior config set security.allow_private_urls true
```

Then verify/patch YAML if necessary:

```yaml
approvals:
  mode: 'off'
gateway:
  media_delivery_allow_dirs:
    - /home/usuario/MEGA/Comprovantes
```

Filesystem permission reinforcement:

```bash
chmod -R u+rwX /home/usuario/MEGA/Comprovantes
stat -c '%A %U %G %a %n' /home/usuario/MEGA/Comprovantes
```

Update `~/.hermes/profiles/finance-senior/SOUL.md` to state the user-granted scope and boundary.

Verification: run the profile and perform a harmless create/read/delete test in the target directory, then confirm the test file no longer exists.

## Local documentation structure created

Directory:

`/home/usuario/.hermes/docs`

Recommended files by context:

- `INDEX.md`
- `00-resumo-executivo.md`
- `01-openclaw-config-analisado.md`
- `02-perfis-hermes-criados.md`
- `03-gateway-hermes-e-openclaw-paralelos.md`
- `04-finance-senior-comprovantes-permissoes.md`
- `05-comandos-operacionais.md`
- `06-decisoes-e-cuidados.md`

Do not include tokens, API keys, raw auth-state, or sensitive session dumps in these docs.
