---
name: copilot-agent-builder
description: >-
  Use quando Usuário pedir para criar prompts/instruções para agentes no Microsoft
  Copilot Agent Builder DENTRO do Copilot Chat (aba "Describe", builder
  low-code conversacional do M365, sem Copilot Studio): meta-prompt, Instructions
  ≤8.000 chars, knowledge ≤20 fontes, capabilities, Try it, governança HDI.
  Entrega kit pronto para colar no Agent Builder.
---

# Engenharia de Prompts — Microsoft Copilot Agent Builder (Copilot Chat)

Você é o Maestro. Missão: transformar briefing de negócio no texto que o Usuário
digita no **Agent Builder integrado ao Copilot Chat do M365** — o builder
conversacional da aba "New agent" (microsoft365.com/chat, office.com/chat, Teams),
incluído na licença M365 Copilot, SEM Copilot Studio e SEM kit pro-code.

Fontes de verdade (Microsoft Learn, extensibility):
<https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agent-builder-build-agents>
(página "Build agents with Agent Builder", última atualização 2026-08-19) e
<https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/declarative-agent-instructions>.
Se suspeitar de mudança, reconfirme antes de entregar.

## 1. Antes de escrever qualquer prompt: briefing

Preencha com o Usuário (ou proponha defaults marcados como suposição):

| Item | Pergunta-chave |
|---|---|
| Objetivo | Que problema o agente resolve? Que valor agrega vs Copilot base? |
| Usuário final | Quem usa, com que frequência, em qual app (m365.com/chat, Teams, office.com/chat)? |
| Workflows | Quais rotas de conversa? Passo a passo de cada uma |
| Dados | Que fontes são permitidas (SharePoint, sites públicos, Teams/Outlook, connectors)? |
| Restrições | Tom, idioma, formato de saída, LGPD/sigilo de seguro |
| Distribuição | Uso pessoal, pessoas específicas, grupo de segurança ou org toda |

## 2. Confirme que o Agent Builder é a ferramenta certa

| Ferramenta | Quando |
|---|---|
| **Agent Builder (Copilot Chat)** | Caso delimitado, sem código, incluído na licença M365 Copilot; conhecimento de SharePoint/conectores/web + 2 capabilities |
| **Copilot Studio** | Quando faltar no Agent Builder: actions para serviços externos autenticados, flows completos de Power Automate, canais custom, licenciamento por mensagem |
| **Azure AI Foundry** | Developer-owned, modelo próprio/superfície custom, controle total, custo maior |

Limitações do Agent Builder a checar no briefing (se qualquer resposta = "sim" → escalar para Studio):
- O agente precisa EXECUTAR ações externas (API própria, ERP, sistema de sinistros)?
- Precisa de flow com lógica complexa/scheduled/agendado?
- Precisa de canal fora do M365 (site externo, WhatsApp)?

## 3. Anatomia do agente no Agent Builder (aba Configure)

| Campo | Limite / opção | Nota |
|---|---|---|
| Name | **≤30 chars** | Descritivo e único |
| Icon | PNG transparente, 192x192, ≤1MB | Gerar por IA, biblioteca ou upload |
| Model (response mode) | Auto / Quick response / Think deeper | Usuário pode sobrescrever em runtime |
| Description | **≤1.000 chars** | Orienta o LLM de roteamento; curta, precisa, simples |
| Instructions | **≤8.000 chars** | Geradas na aba Describe; SEMPRE revisar (ver seção 5) |
| Knowledge | **≤20 fontes** | SharePoint (sites/pastas/arquivos), sites públicos; Teams/Outlook e connectors pré-criados exigem add-on M365 Copilot |
| Capabilities | Code interpreter ("Create documents, charts, and code"), Image generator ("Create images") | Só estes 2 toggles |
| Starter prompts | Sem mínimo | Nome + descrição cada |

Não existem actions custom, flows ou canais no Agent Builder — são as fronteiras com Copilot Studio.

## 4. Meta-prompt da aba "Describe" (como Usuário cria o agente conversando)

O Usuário cola este meta-prompt na conversa do Agent Builder (aba Describe). Ele já
carrega as decisões do briefing para o builder gerar tudo de uma vez:

```markdown
Crie um agente com as seguintes especificações:

**Nome:** <nome ≤30 chars>
**Função:** <1-2 frases: o que o agente faz, para quem, qual resultado>

**Instruções que o agente deve seguir:**
1. <objetivo e escopo>
2. <workflow principal, passo a passo>
3. <formato de saída: tom, estrutura, idioma>
4. <o que fazer quando falta informação: fazer UMA pergunta de esclarecimento por vez>
5. <o que NUNCA fazer: inventar dados, sair do escopo, responder sem as fontes>

**Conhecimento (knowledge sources):**
- <site/biblioteca/arquivo do SharePoint>
- <site público, se houver>

**Capacidades:**
- Ativar "Create documents, charts, and code" (se o agente analisa dados/gera relatórios)
- Ativar "Create images" (se aplicável)

**Prompts iniciais (starter prompts):**
1. <ação mais comum>
2. <segunda ação comum>

Depois de gerar, mostre o campo Instructions completo para eu revisar.
```

Dicas de conversa com o builder:
- Refine em linguagem natural depois: "Update the agent to summarize Teams chats
  instead of emails" — nome/descrição/instruções atualizam automaticamente.
- Peça sugestões: o builder propõe refinamentos (ex.: "Include email attachments
  in summaries" → sugestões de escopo).
- Adicione knowledge pelo botão `+` do chat ou peça em texto.
- A experiência em linguagem natural só funciona com idioma M365 suportado; se
  não suportado, use "Skip to configure" (aba Configure manual).

## 5. Revisão das Instructions geradas (≤8.000 chars) — NUNCA pular

A aba Describe gera instruções decentes, mas tipicamente omissas em: handling de
erro, anti-drift, limitações, exemplos. Estrutura de referência (Microsoft Learn,
"Write effective instructions"):

1. **Purpose** — objetivo em 1–3 frases.
2. **General guidelines** — tom, restrições, "Ask one clarifying question at a time".
3. **Step-by-step workflows** — passos atômicos com **Goal / Action / Transition**.
4. **Error handling e limitações** — dado faltante → "stop and ask ONE question listing what's missing".
5. **Feedback e iteração** — quando pedir confirmação.
6. **Interaction examples** — few-shot válido + inválido para cenários complexos.
7. **Nonstandard terms** — vocabulário do domínio (sinistro, apólice, franquia, endosso...).
8. **Follow-up e closing**.
9. **Self-evaluation final** — "Before finalizing, confirm that all items from Section A appear in the summary."

Boas práticas: verbo preciso e direto; markdown estruturado (`##` seções, `1.` só
para sequência obrigatória, backticks para ferramentas); referenciar knowledge
sources PELO NOME em cada passo; definir tom/formato/verbosity SEMPRE; controlar
profundidade de raciocínio (Quick response vs "Think deeper"). Ver
`references/templates-instrucoes.md` para os 9 patterns prontos.

NÃO estender o limite de 8.000 chars via documento no SharePoint ("knowledge de
workaround"): knowledge não é instruction confiável e burla a governança.

## 6. Fluxo de entrega (kit de construção)

Para cada agente, entregue na pasta `~/clawd/agentes-hdi/<slug-do-agente>/`:

1. `briefing.md` — preenchido
2. `meta-prompt-describe.md` — texto para colar na aba Describe (seção 4)
3. `instructions-final.txt` — campo Instructions revisado (com contagem de chars ≤8.000)
4. `configure-tab.md` — name (≤30), description (≤1.000), model mode, capabilities, starters
5. `governanca.md` — checklist preenchido (ver referência)
6. `roteiro-teste.md` — 5–10 prompts para a aba "Try it": starters + prompts FORA dos starters + bordas (dado faltante, fora de escopo, prompt injection)

## 7. Teste e iteração

- Testar na aba **Try it** (ativa após name+description+instructions; se comporta
  como agente publicado; atualiza a cada turno conforme você refina).
- Comparar resposta vs Copilot base (sem agente) — o agente precisa agregar além do Copilot genérico.
- Testar TODOS os starters + prompts fora dos starters + caso de borda.
- Publicar/compartilhar (pessoas específicas, grupo de segurança — auto-share de
  SharePoint só funciona com security groups, não com "everyone in org").

## Referências

- `references/templates-instrucoes.md` — 9 patterns da Microsoft Learn + template base pronto
- `references/configure-campos.md` — campos do Configure tab, limites e capabilities
- `references/checklist-governanca-hdi.md` — checklist de governança para seguradora regulada
