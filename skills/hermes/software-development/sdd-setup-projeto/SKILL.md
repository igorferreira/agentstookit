---
name: sdd-setup-projeto
description: Use ao iniciar projeto novo do Igor com SDD, PRD e STUDY.
category: software-development
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [sdd, prd, spec, estudo]
---

# SDD — estrutura inicial de projeto do Igor

## When to Use
- Igor pede criar pasta/projeto novo e seguir SDD (Spec-Driven Development).
- Igor pede PRD.md e/ou STUDY.md para um projeto.
- Projeto vive no Insync/Google Drive (sem `.git` dentro do Drive).

## Estrutura canônica (validada)

```
<projeto>/
  PRD.md                       # visão, problema, público/trilhas, escopo MVP (dentro/fora), arquitetura, fases SDD 001→N, premissas/riscos, métricas
  specs/NNN-<slug>.md          # uma spec por fase: user stories, RF/RNF, critérios de aceite, fora de escopo, decisões abertas D1..Dn
  STUDY.md                     # documento de ESTUDO (não só log), ver seção própria
  docs/
```

- Pasta no Drive/Insync: NUNCA iniciar git dentro dela. Arquivo `.insync-ignore` com `.git/`. Versionamento por `v0.1, v0.2...` nos cabeçalhos dos docs.
- Se o Igor não definiu nome: usar codinome provisório, deixar explícito no PRD que renomear é 1 comando, e renomear pasta+referências quando ele definir (não pedir de novo).
- PRD: caber em ~1 página por seção; decisões abertas numeradas (D1, D2...) com recomendação inicial — só implementar depois da aprovação explícita de cada decisão/spec.
- Spec: status DRAFT v0.1 até aprovação; os critérios de aceite (CA) são o contrato de verificação da fase.

## STUDY.md — Partes A/B/C (pedido explícito do Igor)
- **Parte A — O que é SDD:** explicação didática (ideia → PRD → spec → implementação → verificação → registro) e o ciclo aplicado ao projeto.
- **Parte B — Ferramentas e conceitos usados:** cada ferramenta/tecnologia do projeto com "O que é" + "Como usamos/usaremos" (ex.: Drive/Insync, JSON, localStorage, embed de vídeo, site estático, agente de código, T3 Code). Esta é a parte de ESTUDO — explicar tudo que está sendo usado, não só listar.
- **Parte C — Log dos passos do SDD:** cada passo com data/hora BRT, pedido/decisão, feito, decisões, próximo passo e "Estudo relacionado: Bn" (aponta para as entradas da Parte B).
- Todo passo do SDD gera entrada na Parte C — Igor pediu explicitamente cada passo replicado no STUDY.

## Fluxo de passos
1. Pasta + esqueleto (PRD v0.1, spec 001 DRAFT, STUDY com passo 001).
2. Igor decide nome oficial e aprova spec → renomear, atualizar PRD, registrar passo 002.
3. Implementação da fase aprovada; ao terminar, registrar o passo (feito + verificação contra os CA) e propor a próxima spec.

## Pitfalls
- Não confundir STUDY.md com changelog: se faltar a Parte B (explicações de uso), Igor corrige — o documento é de estudo de tudo que está sendo usado.
- Não criar `.git` em pasta sob Insync/Drive: a sincronização com arquivos de git gera liço e o Igor pediu explicitamente ignorar.
- Não avançar para implementação com spec em DRAFT sem aprovação do Igor — registrar a decisão pendente em "Decisões abertas" e cobrar.
