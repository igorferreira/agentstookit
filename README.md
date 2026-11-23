# agentstookit

Coleção de agentes e skills prontos para as plataformas **Hermes**, **Codex** e **Claude** — separados por plataforma, um diretório por agente/skill.

## Estrutura

```
agentstookit/
├── agents/
│   ├── hermes/   # 135 perfis Hermes (SOUL.md + config.yaml + skills do perfil)
│   ├── codex/    # 115 agentes (definições .toml)
│   └── claude/   # 130 agentes (definições .md)
└── skills/
    ├── hermes/   # 98 skills globais (organizadas por categoria)
    ├── codex/    # 24 skills
    └── claude/   # 139 skills
```

## Como usar

- **Hermes**: copie a pasta do agente para `~/.hermes/profiles/<nome>/` (as chaves de API ficam em `.env` — crie o seu; o repositório não contém credenciais).
- **Codex**: copie a definição para `~/.codex/agents/`.
- **Claude**: copie a definição para `~/.claude/agents/` ou a skill para `~/.claude/skills/`.

## Segurança

Antes da publicação, todo o repositório passou por varredura automatizada de segredos (chaves de API, tokens, JWTs, chaves privadas, credenciais, dados pessoais). Os achados foram triados um a um: todos os padrões detectados são placeholders de documentação ou fixtures de teste — **nenhum segredo real**. Dados pessoais (CPF) foram mascarados.

## Licença

Uso livre para fins pessoais e educacionais.
