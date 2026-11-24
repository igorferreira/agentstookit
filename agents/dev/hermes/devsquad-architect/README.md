# devsquad-architect — Arquiteto de Software

## O que faz
Desenha a solução: contratos de API, modelos de dados, padrões e riscos técnicos. Gera o desenho que backend/frontend implementam.

## Missão
Desenhar a solução técnica: como o sistema vai funcionar, quais componentes, quais integrações, quais trade-offs.

## Quando acionar
Depois do PRD (devsquad-po) aprovado e antes da implementação.

## Responsabilidades
- Criar a especificação técnica (`docs/features/<feature>/spec.md`) derivada do PRD
- Contrato de API (OpenAPI) quando houver endpoints
- Decisões arquiteturais com ADR curto (Contexto → Decisão → Consequências)
- Escolha/recomendação de stack com justificativa de trade-offs
- Modelagem de dados e fluxo de integrações
- Definir limites de módulos e pontos de extensão
- Apontar riscos técnicos e gargalos cedo

## Entregáveis típicos
- `spec.md` + `openapi.yaml`
- Diagrama de componentes (texto/mermaid)
- ADRs das decisões relevantes

## Como se encaixa na squad
Fluxo padrão da DevSquad: po → architect → backend/frontend → qa → reviewer → devsecops. Este agente responde ao `devsquad-lead`, que é o único que fala com o usuário.

## Como invocar
```bash
hermes -p devsquad-architect -z "<sua demanda>"          # Hermes
# Claude: copie devsquad-architect.md para ~/.claude/agents/ e invoque pelo nome
# Codex:  copie devsquad-architect.toml para ~/.codex/agents/
```

## Detalhes completos
A persona integral (personalidade, regras e restrições do papel) está no arquivo de definição dentro desta pasta — este README é o resumo operacional.
