# advisory-master — Coordenador da Banca Consultiva de Engenharia

## O que faz
Ponto de entrada para questões de engenharia de software em QUALQUER projeto (não específico de HDI). Faz a triagem da demanda e distribui entre os 4 especialistas (platform, qa, security, strategy), depois consolida tudo numa recomendação única e coordenada. Encaminha dúvidas de implementação profunda para os arquitetos de stack (java-architect, dotnet-architect, ai-solution-architect, solution-architect).

## Quando usar
Não sabe em qual especialista cai sua dúvida de engenharia? Comece por ele.

## Como se encaixa na banca
Fluxo: master (triagem) → platform | qa | security | strategy (consolidado pelo master). É a banca consultiva genérica — para o contexto HDI específico, use os correspondentes '-senior' (devex-platform-senior, devsecops-governance-senior, digital-transformation-exec).

## Como invocar
```bash
# Claude: copie advisory-master.md para ~/.claude/agents/ e invoque pelo nome
# Codex:  copie advisory-master.toml para ~/.codex/agents/
```

## Detalhes completos
A persona integral está no arquivo de definição dentro desta pasta — este README é o resumo operacional.
