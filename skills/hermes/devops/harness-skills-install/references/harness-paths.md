# Paths e instaladores por harness

| Harness | Skills globais | Skills de projeto | Comando de validação | Instalador nativo |
|---|---|---|---|---|
| Hermes Agent | `~/.hermes/skills/<cat>/<name>/` | — | `hermes skills` / skill_view | `hermes skills install`; guard `skills-guard-v1` faz scan em skills community |
| OpenCode | `~/.config/opencode/skills/<name>/SKILL.md` | `.opencode/skills/` | `opencode debug skill` (conta entradas por frontmatter `name`) | `plugin` array no `~/.config/opencode/opencode.jsonc` (ex.: `["nome@git+https://github.com/org/repo.git"]`); auto-carrega TAMBÉM `~/.claude/skills/` e `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/<name>/SKILL.md` | `.claude/skills/` | sessão do claude | — |
| Codex | `~/.codex/skills/` | — | — | — |
| OpenClaw | `~/.openclaw/` (skills + registro `hermes-agents/<id>/`) | — | gateway/clawdbot registry | — |

## Notas OpenCode
- Frontmatter `name` é o ID registrado (lowercase, hífen, ≤64 chars, deve ser único); pasta com prefixo de coleção é permitida enquanto o `name` não colida.
- Skill sem `description` no frontmatter é descartado silenciosamente pela listagem.
- Config: `~/.config/opencode/opencode.jsonc` (não `~/.opencode/`); binary em `~/.opencode/bin` (PATH).
- `graphify install` (do pacote `graphifyy`, via `uv tool install`) escreve em `~/.claude/skills/graphify/` — copiar para o skills do OpenCode depois.
- OpenCode recém-instalado fica sem provedor: `opencode auth login` (ou `opencode providers`) é passo pendente do usuário — registrar no relatório.

## Instalador universal `npx skills add`

- `npx -y skills add <org>/<repo> -g` (skills.sh) instala em `~/.agents/skills/<name>/` e cria SYMLINKS em `~/.claude/skills/` e nos dirs de dezenas de outros harnesses — é a via oficial quando o repo não tem instalador próprio. OpenCode enxerga via auto-load de `~/.agents/skills/`.
- Falhas parciais são esperadas e benignas: algum harness da lista pode recusar (ex.: "PromptScript does not support global skill installation") — o resto instala; conferir os alvos que importam e seguir.
- Para repos com múltiplos skills, filtrar com `--skill <nome>`. Os symlinks apontam para `~/.agents/skills/` (uma fonte canônica) — não copiar conteúdo por cima do symlink duplicando o skill.
