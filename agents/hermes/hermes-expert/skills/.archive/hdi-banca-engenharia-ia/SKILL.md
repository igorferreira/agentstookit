---
name: hdi-banca-engenharia-ia
description: "Use para apoiar a elaboração, governança e execução de arquitetura de software, APIs e IA generativa na HDI Seguros com os 7 especialistas da banca multidisciplinar de engenharia."
---

# Banca Multidisciplinar de Engenharia de Software — HDI Seguros

## Overview

Skill de apoio corporativo para governança, modernização de arquitetura de software, APIs REST e adoção de IA na HDI Seguros com os 7 perfis especialistas de engenharia.

## 🏛️ Especialistas da Banca de Engenharia (Perfis Hermes)

1. **Arquiteto Corporativo de Soluções:** `solution-architect` (Arquitetura macro, padrões MACH, governança).
2. **Arquiteto de Software (APIs & Integrações):** `java-architect` e `dotnet-architect` (OpenAPI, Java/Spring Boot, Python, .NET C#).
3. **Arquiteto de IA Generativa:** `ai-solution-architect` (Orquestração, MCP, Skills Hub, roteamento de LLMs).
4. **Especialista em DevEx & Platform Engineering:** `devex-platform-senior` (CLI, extensões IDE, templates de scaffolding, catálogo).
5. **Especialista em DevSecOps, Segurança & LGPD:** `devsecops-governance-senior` (SAST/DAST, proteção de segredos, isolamento de tenant, SUSEP).
6. **Especialista no Domínio de Seguros:** `insurance-domain-senior` (Auto, Residencial, Rural, Vida, catálogo de APIs InsureMO).
7. **Consultor Executivo de Transformação Digital:** `digital-transformation-exec` (C-Level, métricas DORA, ROI, adoção incremental).

## 📁 Pastas e Artefatos Canônicos

* Raiz dos documentos de arquitetura HDI: `~/projetos/hdi/Arquitetura/`
* Referências e estudos: `~/projetos/hdi/Arquitetura/referencias/` e `~/MEGA/Documentos/educacao_leitura/estudos/`
* Portal HDI Developers: `https://developers.hdi.com.br` (`llms.txt` e referência de APIs)
* InsureMO: `https://insuremo.com` (PaaS MACH com 2.500+ APIs atômicas e iComposer)

## 🔄 Método de Produção Incremental por Etapas

1. **Etapa 1 — Descoberta:** Fontes primárias, fatos confirmados vs hipóteses vs alegações comerciais, 12 perguntas de alto impacto.
2. **Etapa 2 — Estrutura:** Sumário detalhado (Executivo vs Técnico).
3. **Etapa 3 — Diagnóstico:** Matriz de problemas, causas, impactos e oportunidades.
4. **Etapa 4 — Visão e Arquitetura:** 6 camadas conceituais (Harness & Loop Engineering).
5. **Etapa 5 — Roadmap & Piloto:** Piloto controlado Onda 1 ➔ Expansão Onda 2 ➔ Industrialização.
6. **Etapa 6 — Documento-Base:** Consolidação final estruturada.
7. **Etapa 7 — Apresentação Executiva:** Slides com visual e talking points para C-Level.

## ⚠️ Pitfalls
* **Segregação Estrita de Bancas:** Nunca misturar a Banca de Engenharia HDI com a Banca de Saúde pessoal.
* **Harness & Loop Engineering:** Não defender IA como gerador isolado de código; vincular sempre a um Harness determinístico com testes automatizados (`mvn test`, `pytest`, `dotnet test`) e guardrails de segurança.
* **Estudos de Referência (2026):** Incorporar lições de Boris Cherny (criador do Claude Code — Context Window Optimization, prompts em 5 passos), Hux (@huxlab — Harness & Loop Engineering), Anthropic AI Engineering (Prompt Caching, Prefill, XML tags) e Google AI Engineering (Graph Engineering, LangGraph StateGraphs, Topologia Supervisor/Router) na fundamentação das Camadas 2, 4 e 5.
* **Modelos de Custo de Inferência:** Registrar alternativas como gateways/proxies (ex.: Cheaper Inference/Keak) para ambientes de desenvolvimento/estudo pessoal, ressalvando que ambientes corporativos regulados (HDI) exigem tenant isolado (Azure OpenAI / AWS Bedrock) por compliance e LGPD.
