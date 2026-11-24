# Configure tab — Campos, limites e capabilities (Agent Builder no Copilot Chat)

Fonte: learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agent-builder-build-agents (2026-08-19)

## Como chegar

Microsoft 365 Copilot (microsoft365.com/chat, office.com/chat, Teams desktop/web)
→ **New agent** → três caminhos:

1. **Describe** (recomendado): linguagem natural; o builder gera nome, descrição,
   instructions, knowledge e starters conversacionalmente.
2. **Skip to configure**: aba Configure manual.
3. **Start with a template**: templates com descrição/instructions/prompts pré-configurados.

## Campos

| Campo | Limite / opções | Diretriz |
|---|---|---|
| Name | ≤30 caracteres | Descritivo e único |
| Icon | PNG, 192x192, ≤1MB, fundo transparente | Gerar (IA), biblioteca ou upload |
| Model (default response mode) | Auto (default) / Quick response / Think deeper | Usuário pode sobrescrever em runtime; Think deeper para tarefas complexas |
| Description | ≤1.000 caracteres | Ajuda o LLM de roteamento a saber quando usar o agente; curta, precisa, simples |
| Instructions | ≤8.000 caracteres | Direciona tarefas e como executá-las; geradas na aba Describe, sempre revisar |
| Knowledge | ≤20 fontes | SharePoint (sites, pastas, arquivos), sites públicos; Teams/Outlook e connectors exigem add-on M365 Copilot |
| Capabilities | 2 toggles | Code interpreter = "Create documents, charts, and code"; Image generator = "Create images" |
| Starter prompts | sem mínimo | Nome + descrição cada; comunicam os cenários suportados |

## Capabilities

- **Code interpreter** — resolve problemas matemáticos complexos, analisa dados, gera visualizações. Toggle: "Create documents, charts, and code".
- **Image generator** — gera imagens a partir de prompts. Toggle: "Create images".

## Disponibilidade por licença

A disponibilidade de knowledge sources e capabilities varia com a licença do
usuário ("Agent capabilities and licensing models"). Sem add-on M365 Copilot:
não há grounding em dados pessoais de trabalho (Teams/Outlook) nem connectors pré-criados.

## Aba Try it

- Ativa após name + description + instructions preenchidos.
- Comporta-se como agente publicado (responde queries complexas dentro do knowledge configurado).
- Atualiza a cada turno conforme você refina (Describe ou Configure).
- Limitações no Try it: sem share de prompts, sem feedback, sem @mention de outros agentes.

## O que NÃO existe no Agent Builder (fronteiras com Copilot Studio)

- Actions custom (APIs externas autenticadas) → Copilot Studio
- Flows de Power Automate com lógica complexa/agendamento → Copilot Studio
- Canais fora do M365 → Copilot Studio
- Agents criados no Agent Builder NÃO funcionam em Teams Chat (apenas nos apps M365 Copilot)
- Toggle de "discourage model knowledge" (só existe no manifest pro-code 1.7): no
  Agent Builder, obtenha o efeito via instrução — "Responda SOMENTE das knowledge
  sources configuradas; se não estiver nelas, diga e pare."
