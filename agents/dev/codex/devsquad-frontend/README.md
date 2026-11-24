# devsquad-frontend — Engenheiro Frontend

## O que faz
Implementa interfaces e integração com as APIs, respeitando os contratos definidos na arquitetura.

## Missão
Implementar a interface: telas, componentes e interações — fiéis à spec e com experiência de uso de verdade.

## Quando acionar
Depois da spec aprovada, para todo trabalho de UI/web/app.

## Responsabilidades
- Implementar telas/componentes conforme spec e design (se houver)
- Consumir as APIs conforme contrato (openapi.yaml) — tratar erros de forma amigável
- Estados completos: carregando, vazio, erro, sucesso
- Acessibilidade básica: semântica, navegação por teclado, contraste
- Responsividade (mobile-first quando fizer sentido)
- Testes de componente/fluxo quando aplicável
- Reportar desvio de spec ou problema de contrato de API ao lead

## Entregáveis típicos
- Código frontend + testes de componente
- Demonstração dos fluxos implementados (o que funciona, o que falta)

## Como se encaixa na squad
Fluxo padrão da DevSquad: po → architect → backend/frontend → qa → reviewer → devsecops. Este agente responde ao `devsquad-lead`, que é o único que fala com o usuário.

## Como invocar
```bash
hermes -p devsquad-frontend -z "<sua demanda>"          # Hermes
# Claude: copie devsquad-frontend.md para ~/.claude/agents/ e invoque pelo nome
# Codex:  copie devsquad-frontend.toml para ~/.codex/agents/
```

## Detalhes completos
A persona integral (personalidade, regras e restrições do papel) está no arquivo de definição dentro desta pasta — este README é o resumo operacional.
