---
name: openclaw-update
description: Use ao rodar openclaw update na máquina do Igor.
---

O update roda `openclaw doctor` internamente, que exige **lease exclusivo** dos bancos SQLite (~/.openclaw/state/openclaw.sqlite + um sqlite por agente — 123 escopos). Três causas de falha já confirmadas na prática (24/09/2026, ida 2026.9.5 → 2026.9.6):

1. **Lease preso** → "unsafe recovery (79)" / "Abandoned update detected". Causa: gateway ativo e filhos `codex app-server` (podem ser 20+ processos órfãos).
2. **Heap OOM do Node** → "JavaScript heap out of memory" no doctor. Causa: heap padrão não dá conta de 123 escopos de agente.
3. **SQLite sob escrita concorrente** → "SQLite source did not stabilize after 10 read-only inspection attempts". Causa: update rodando com o gateway ligado.

## Sequência validada

```bash
# 1. Parar gateway e matar filhos codex (padrão com colchete p/ não matar o próprio shell)
systemctl --user stop openclaw-gateway.service
PIDS=$(pgrep -f 'cod[e]x app-server'); [ -n "$PIDS" ] && kill $PIDS

# 2. Rodar o update EM BACKGROUND (demora 15-45min com muitos agentes)
export NODE_OPTIONS="--max-old-space-size=8192"
env OPENCLAW_STATE_DIR=/home/igorferreira/.openclaw \
    OPENCLAW_CONFIG_PATH=/home/igorferreira/.openclaw/clawdbot.json \
    OPENCLAW_WORKSPACE_DIR=/home/igorferreira/.openclaw/workspace \
    openclaw update --yes

# 3. Se sobrar "Abandoned update detected": reconciliar
openclaw update repair   # com as mesmas env vars e NODE_OPTIONS

# 4. Reativar e conferir
systemctl --user start openclaw-gateway.service
openclaw --version
openclaw update status   # deve mostrar "✅ OpenClaw updated to <versão>"
```

## Gotchas

- **Sempre background** (`terminal background=true` ou monitor próprio): o foreground da ferramenta corta em 420s e MATA o update no meio (deixa run órfã → repair depois).
- **As env vars OPENCLAW_STATE_DIR/CONFIG_PATH/WORKSPACE_DIR são obrigatórias**; sem elas o update roda mas pula o service management ("service management skipped: non-default state dir").
- **Não reativar o gateway antes do update terminar** — causa o erro 3 na hora.
- `openclaw update status` mostrando só "requested" sem processo nenhum = run órfã → rodar repair.
- O gateway fica FORA DO AR durante todo o update (~30 min); Telegram via OpenClaw fica mudo nesse período.
- Depois do update, `openclaw doctor --fix` é recomendado pelo próprio tool.
- Aviso conhecido e aceito: gateway bound to loopback (Igor decide quando expor).