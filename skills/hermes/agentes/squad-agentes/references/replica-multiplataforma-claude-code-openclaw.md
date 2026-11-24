Réplicas multi-plataforma dos agentes Hermes (validado 05/09/2026 com celular-doc, linux-sys, ubuntu-doc, ubuntu-mate-doc).

## Claude Code (subagente)
Criar `~/.claude/agents/<id>.md` — frontmatter YAML + conteúdo do SOUL.md do Hermes como corpo:

```yaml
---
name: "<id>"
description: "(<Apelido>) <gatilhos de uso — o roteador usa isto para invocar automaticamente>"
model: sonnet
permissionMode: default
memory: user
maxTurns: 40
tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
color: cyan
---
```

Notas:
- `description` descreve QUANDO usar (triggers concretos), não quem o agente é.
- Contar total: `ls ~/.claude/agents/ | wc -l` (cresce a cada criação).

## OpenClaw (workspace + registro JSON)
1. Criar `~/.openclaw/workspace-<id>/` e copiar o SOUL.md do Hermes para lá **sem alteração**.
2. Registrar em `~/.openclaw/openclaw.json` → `agents.list[]`:
```json
{"id": "<id>", "name": "<id>", "workspace": "/home/usuario/.openclaw/workspace-<id>", "agentDir": "/home/usuario/.openclaw/agents/<id>/agent"}
```
- O `agentDir` pode não existir fisicamente — o essencial é workspace + SOUL.md.
- Editar o JSON via Python (`json.load` / `json.dump`, ensure_ascii=False, indent=2) — NUNCA por regex/sed.
- Invocável no bot como `@<id>`.
- Contar total: `len(cfg['agents']['list'])`.

## Auditoria pós-réplica
Verificar em todas as 3 plataformas após criar: SOUL.md presente e com conteúdo (não vazio), registro JSON válido, contagens batendo. Padrão do usuário: registrar as réplicas em `~/clawd/AGENTES.md` (seção "Réplicas multi-plataforma") e sincronizar o espelho no Drive (`~/Insync/GoogleDrive/usuariobr/03_Dev_IA/ia_agentes/AGENTES.md`).
