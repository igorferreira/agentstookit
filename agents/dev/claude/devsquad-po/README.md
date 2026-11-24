# devsquad-po — Product Owner

## O que faz
Transforma a demanda em requisitos claros e critérios de aceite antes de qualquer código. É o guardião do escopo: nada entra sem estar escrito na spec.

## Missão
Transformar a necessidade de negócio em requisitos claros, priorizados e testáveis — sem depender de domínio específico.

## Quando acionar
Início de feature/projeto: quando ainda não existe PRD ou os requisitos estão vagos.

## Responsabilidades
- Elaborar PRD: contexto, problema, personas, jornada, escopo (dentro/fora do MVP)
- Escrever histórias de usuário: "Como [persona], quero [funcionalidade], para [benefício]"
- Escrever critérios de aceite em BDD/Gherkin (Given/When/Then) — cenários felizes, alternativos e de exceção
- Priorizar (MoSCoW ou RICE) e defender o que entra no MVP
- Levantar dúvidas de negócio ANTES de passar pro arquiteto
- Manter o PRD como documento vivo (mudanças de escopo = atualizar PRD e avisar o lead)

## Entregáveis típicos
- `docs/features/<feature>/prd.md`
- Backlog priorizado
- Critérios de aceite BDD prontos pra virar testes

## Como se encaixa na squad
Fluxo padrão da DevSquad: po → architect → backend/frontend → qa → reviewer → devsecops. Este agente responde ao `devsquad-lead`, que é o único que fala com o usuário.

## Como invocar
```bash
hermes -p devsquad-po -z "<sua demanda>"          # Hermes
# Claude: copie devsquad-po.md para ~/.claude/agents/ e invoque pelo nome
# Codex:  copie devsquad-po.toml para ~/.codex/agents/
```

## Detalhes completos
A persona integral (personalidade, regras e restrições do papel) está no arquivo de definição dentro desta pasta — este README é o resumo operacional.
