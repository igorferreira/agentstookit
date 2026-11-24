# Manual de instalação

Como montar qualquer agente deste repositório nas 3 plataformas. O contexto do agente vive **dentro da pasta dele** — copiou, funciona.

```
escolha o agente em agents/<dominio>/_INDEX.md
        │
        ├── Hermes  → copie a pasta inteira → ~/.hermes/profiles/<nome>/
        ├── Claude  → copie o <nome>.md     → ~/.claude/agents/
        └── Codex   → copie o <nome>.toml   → ~/.codex/agents/
```

---

## Hermes

1. **Copie a pasta do agente** (autocontida: `SOUL.md` + `skills/` do perfil):
   ```bash
   cp -r agents/juridico/hermes/juris-tributario ~/.hermes/profiles/juris-tributario
   ```

2. **Crie o `.env` do perfil** com a chave do seu provedor (o repo **não** contém credenciais):
   ```bash
   cat > ~/.hermes/profiles/juris-tributario/.env
   # adicione a variável do seu provedor, ex.:
   # OPENROUTER_API_KEY=sk-or-v1-...
   chmod 600 ~/.hermes/profiles/juris-tributario/.env
   ```

3. **Ajuste o `config.yaml`** do perfil com modelo e provedor:
   ```yaml
   model:
     default: <modelo-do-seu-provedor>
     provider: <openrouter|anthropic|openai|...>
   ```

4. **Teste:**
   ```bash
   hermes -p juris-tributario -z "Em uma frase: qual sua especialidade?"
   ```

> O agente responde **na persona** do SOUL.md. Skills dentro da pasta do perfil são carregadas automaticamente.

---

## Claude (Claude Code)

1. **Copie a definição:**
   ```bash
   cp agents/juridico/claude/juris-tributario/juris-tributario.md ~/.claude/agents/
   ```

2. A definição é um `.md` com frontmatter (`name`, `description`, `tools`). O `description` é o que o Claude usa para delegar automaticamente — ajuste se quiser mudar quando ele entra em cena.

3. **Teste:** no Claude Code, peça uma tarefa da especialidade ou invoque direto o agente pelo nome.

> Skills do repo podem ir para `~/.claude/skills/` (uma pasta por skill, com `SKILL.md`).

---

## Codex

1. **Copie a definição:**
   ```bash
   cp agents/juridico/codex/juris-tributario/juris-tributario.toml ~/.codex/agents/
   ```

2. A definição é TOML (`name`, `description`, `prompt`). O campo `description` determina quando o Codex delega para ele.

3. **Teste:** rode o Codex CLI e invoque o agente pela especialidade.

---

## Skills (opcional, em qualquer plataforma)

```
skills/hermes/<categoria>/<skill>/  → ~/.hermes/skills/<categoria>/<skill>/
skills/claude/<skill>/              → ~/.claude/skills/<skill>/
skills/codex/<skill>/               → ~/.codex/skills/<skill>/
```

Skills são bibliotecas de procedimento que qualquer agente pode usar — instale só as que fizerem sentido para o seu uso.

---

## Verificação e problemas comuns

| Sintoma | Causa provável | Correção |
|---|---|---|
| `No LLM provider configured` | `.env` do perfil ausente ou sem chave | crie o `.env` (passo 2 do Hermes) |
| `No models provided` (HTTP 400) | `config.yaml` do perfil sem `model.default`/`provider` | preencha o passo 3 |
| Agente responde fora da persona | SOUL.md não carregado (pasta copiada parcialmente) | copie a pasta **inteira** |
| Aviso de credencial compartilhada com o perfil default | perfil nomeado herda token de Telegram | inofensivo para uso local via `-p` (sem bot próprio) |
| Skill não aparece para o agente | pasta fora do nível esperado | confira o caminho exato por plataforma acima |

---

## Boas práticas

- **Comece pelos `-master`** dos domínios com banca (juridico, saude): eles orquestram as especialidades e consolidam veredito.
- **Um agente por especialidade** escala melhor que um agente genérico com prompt gigante.
- **Exemplos de prompts**: [PROMPTS.md](PROMPTS.md) — copie e adapte.
- Não versiona `.env`, chaves ou dados pessoais nos seus forks — veja o `.gitignore` do repo como referência.
