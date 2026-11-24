# Engenharia de Prompts e Arquitetura de Agentes (Padrão Boris Cherny / Claude Code)

Padrões arquiteturais práticos para construção de agentes de software determinísticos e governados (baseado no framework oficial da Anthropic / Boris Cherny - *"Mastering Claude Code in 30 Minutes"*):

## 1. Otimização de Janela de Contexto (Context Window)
* **Anti-pattern:** Carregar árvores inteiras de repositório, múltiplos arquivos de código ou documentação exaustiva de uma vez.
* **Best Practice:** Manter arquivos de orientação concisos (`CLAUDE.md`, `AGENTS.md`, `SOUL.md`) que funcionam como roteadores e índices semânticos. Deixar o agente localizar e inspecionar arquivos sob demanda via busca rápida (`search_files`, `ripgrep`, MCP).

## 2. Fórmula de 5 Etapas para Prompts de Agentes de Código
1. **Persona & Guardrails Estritos:** Definir quem é o agente e o que ele **NÃO** deve fazer (ex.: não inventar regras de negócio, não tocar em arquivos fora do escopo, não commitar segredos).
2. **Fontes Primárias & Contratos Canônicos:** Apontar caminhos exatos de especificações OpenAPI, ADRs ou repositórios homologados.
3. **Escopo Atômico:** Uma tarefa isolada e mensurável por ciclo.
4. **Critério de Aceite Determinístico:** O agente só declara a tarefa concluída após execução real e sucesso de testes locais (`mvn test`, `pytest`, `dotnet test`, status 0).
5. **Formato Estruturado de Entrega:** Diffs claros, relatórios de verificação e evidências de execução.

## 3. Agentic Toolchain & MCP (Model Context Protocol)
* **Skills Reutilizáveis:** Encapsular fluxos e receitas corporativas em skills versionadas.
* **Protocolos Abertos (MCP):** Conectar ferramentas, APIs e bancos de dados através de servidores MCP padronizados.
* **Human-in-the-Loop:** A IA atua como copiloto e executora técnica; a responsabilidade de merge, homologação e deploy em produção permanece humana.
