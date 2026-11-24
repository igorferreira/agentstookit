# agentstookit

Coleção de **370 agentes** e dezenas de skills prontas para as plataformas **Hermes**, **Codex** e **Claude** — organizados por **domínio de conhecimento**, com um diretório autocontido por agente.

> Exemplos de prompts prontos para cada domínio: **[PROMPTS.md](PROMPTS.md)**

## Os 9 domínios

| Domínio | O que tem | Quando usar |
|---|---|---|
| **[juridico](agents/juridico/_INDEX.md)** | Banca jurídica com 55 especialidades do Direito brasileiro (juris-tributario, juris-penal, juris-lgpd, juris-ia, juris-master...) | Análise técnica de questão jurídica, minuta de peça, parecer, segunda opinião de tese. Use `juris-master` para orquestrar a banca ou chame a especialidade direto |
| **[dev](agents/dev/_INDEX.md)** | Squads completas (devsquad-*: lead, po, architect, backend, frontend, qa, devsecops, reviewer), arquitetos (solution, java, dotnet), seniores (java, python, dotnet), Linux/Ubuntu, segurança de código | Construir feature end-to-end, revisar arquitetura, code review, diagnóstico de infra, capacitação (aws-tutor) |
| **[saude](agents/saude/_INDEX.md)** | Banca multidisciplinar: clínico geral, cardiologista, endocrinologista, nutrólogo, ortopedista, psiquiatra, preparador físico, fisioterapeuta + `saude-master` | Interpretar exames, plano de treino/dieta, segunda opinião médica antes de consulta. **Não substitui profissional da saúde** |
| **[finance](agents/finance/_INDEX.md)** | Orçamento, quitação de dívidas, FinOps de IA, CFO pessoal | Controlar gastos, planejar pagamento de dívidas, auditar custo de LLM/agentes |
| **[negocios](agents/negocios/_INDEX.md)** | Carreira e RH (hr-tech-senior, salarios-glassdoor), produto, transformação digital, operações (sindico-virtual, viagem corporativa) | Negociação salarial, dossiê de empresa antes de entrevista, plano de produto, rotina de condomínio |
| **[agentic](agents/agentic/_INDEX.md)** | Meta-agentes: construção de agentes (copilot-agent-builder), operação de ecossistemas (hermes-expert, openclaw-expert, hermes-town-expert) | Criar um agente novo do zero, depurar gateway/configuração, governança de frota de agentes |
| **[pesquisas](agents/pesquisas/_INDEX.md)** | Comparadores e dossiês: celular, notebook, perfume, hotel, placa de veículo, cursos gratuitos, dossiê de Instagram | Compra planejada ("qual celular vale mais a pena?"), dossiê antes de decidir, monitoramento de preço |
| **[pessoais](agents/pessoais/_INDEX.md)** | Agenda diária, casa inteligente, diário, conselheiro de relacionamento, espiritualidade, horóscopo | Rotina pessoal, organização de dia, reflexão guiada |
| **[criativo](agents/criativo/_INDEX.md)** | Conteúdo para LinkedIn, estúdio de vídeo | Escrever post com autoridade técnica, produzir vídeo-aula |

## Como usar

Cada pasta de agente é **autocontida** — o contexto (persona, regras, conhecimento) mora dentro dela:

- **Hermes**: copie a pasta do agente para `~/.hermes/profiles/<nome>/` e rode `hermes -p <nome> -z "seu prompt"`. As chaves de API ficam em `.env` — crie o seu (o repositório não contém credenciais).
- **Claude**: copie a definição `.md` para `~/.claude/agents/` e invoque via Task/`@agente`.
- **Codex**: copie a definição `.toml` para `~/.codex/agents/`.

**Dicas de uso:**
- Comece pelo `_INDEX.md` do domínio: cada linha traz o agente, a plataforma e o que ele faz em 1 frase.
- Para decisões grandes, use o padrão **banca**: chame o agente `-master` do domínio (juris-master, saude-master) para coordenar múltiplas especialidades e consolidar veredito.
- Padrões de prompt prontos (por domínio) estão em **[PROMPTS.md](PROMPTS.md)**.

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
