# agentstookit

Coleção de agentes e skills prontos para as plataformas **Hermes**, **Codex** e **Claude** — separados por plataforma, um diretório por agente/skill.

## Estrutura

```
agentstookit/
├── agents/         # organizados por DOMÍNIO, cada agente autocontido
│   ├── juridico/   # banca jurídica (40+ especialidades) — veja _INDEX.md
│   ├── dev/        # squads de dev, arquitetura, DevSecOps, Linux
│   ├── saude/      # banca multidisciplinar de saúde
│   ├── finance/    # finanças, dívidas, FinOps de IA
│   ├── negocios/   # carreira, RH, produto, operações
│   ├── agentic/    # meta-agentes (Hermes, OpenClaw, Copilot builder)
│   ├── pesquisas/  # preços, dossiês, comparações
│   ├── pessoais/   # agenda, casa, diário
│   └── criativo/   # conteúdo, vídeo
└── skills/
    ├── hermes/   # skills globais (organizadas por categoria)
    ├── codex/    # skills
    └── claude/   # skills
```

## Como usar

- **Hermes**: copie a pasta do agente para `~/.hermes/profiles/<nome>/` (as chaves de API ficam em `.env` — crie o seu; o repositório não contém credenciais).
- **Codex**: copie a definição para `~/.codex/agents/`.
- **Claude**: copie a definição para `~/.claude/agents/` ou a skill para `~/.claude/skills/`.

## Segurança

Antes da publicação, todo o repositório passou por **três varreduras independentes** de segurança (scanner automatizado + auditoria ofensiva): chaves de API, tokens, JWTs, chaves privadas, credenciais, dados pessoais e financeiros — zero segredos reais, zero dados pessoais. Skills e agentes construídos em torno de contexto pessoal do autor foram removidos (não fazem sentido público).

## Skills e ferramentas de terceiros usados

As skills abaixo **não estão neste repositório** (são públicas nos projetos originais) — são citadas porque são parte do ecossistema usado pelos agentes:

- **gstack** (Garry Tan) — suíte de engenharia (browse, make-pdf, ship...)
- **Skills oficiais Anthropic** (`anthropics/skills`) — docx, pptx, xlsx, pdf, canvas-design, algorithmic-art, theme-factory, webapp-testing, mcp-builder...
- **Superpowers** (Jesse Vincent / obra) — brainstorming, writing-plans, TDD, systematic-debugging...
- **claude-mem** (thedotmack) — memória persistente cross-session
- **daytrader** (jakeschincariol) — suíte de trading (trader-alerts, scanner...)
- **wshobson/agents** — devops-engineer, mobile-developer, python-pro
- **OpenMontage** — suíte de produção de vídeo (ffmpeg, whisperx, color-grading...)
- **Vercel** — web-interface-guidelines, react-best-practices
- **better-auth**, **impeccable** (pbakaus), **last30days**, **osv-ui**, **caveman**, **Archify**, **claude-api**, **humanizer**
- **Built-ins de plataforma**: Hermes (Nous Research), Codex CLI (OpenAI)

## Licença

Uso livre para fins pessoais e educacionais.
