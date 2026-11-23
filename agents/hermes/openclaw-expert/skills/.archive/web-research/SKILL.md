---
name: web-research
description: "Web search, content extraction, SPA fallback."
tags: []
---

# Web Research & Content Extraction

## Trigger

Usar para qualquer tarefa que envolva buscar na internet, extrair conteúdo de páginas web, validar técnicas de automação web, scraping, ou análise de conteúdo técnico encontrado online. Também coberto: tarefas de benchmarking comparativo entre sites.

## Workflow

### Fase 1 — Pesquisa Inicial

- Sempre usar `web_search(query)` primeiro para contexto amplo antes de extração detalhada
- Usar operadores avançados quando relevante: `site:`, `filetype:pdf`, `"exato"`, `-termo indesejado`
- Para comparações entre 3+ opções, pesquisar cada opção separada

### Fase 2 — Extração de Conteúdo Web

- Preferir `web_extract(urls=[...])` para páginas HTTP simples com conteúdo no HTML
- Se `web_extract` retorna página vazia sem conteúdo textível → sinal de SPA com renderização client-side JS
- Neste caso, NÃO tentar automatizar scroll/clique/browser para apenas LEITURA — isso desperdiça tokens
- Fallback seguro: baixar os arquivos `.js` da SPA e grep por strings-pt-BR alvo (ver `references/spa-extraction-pattern.md`)
- Se conteúdo está embutido em JSON/data attributes do HTML fonte (ex: `initialState`, `<script type="application/json">`), extrair direto via terminal

### Fase 3 — Validação Técnica

- Para verificar implementações (CSS, JS, HTML) de terceiros, ler arquivos-fonte diretamente via terminal (`curl` + `grep`, `cat`)
- Comparar resultados com especificações oficiais quando houver risco de informação desatualizada
- Validar claims técnicos contra documentação oficial verificável

### Fase 4 — Entrega

- Respostas sempre incluir data/hora atual (`date` no terminal) para ancoragem temporal
- Links verificáveis com status code HTTP (se relevante)
- Citar fonte específica, não generalizar "a internet diz"

### Fase 5 — Registro canônico do Igor

- Salvar toda pesquisa solicitada também no MEGA, em Markdown canônico na pasta da área correspondente; o arquivo de pesquisa interno não substitui esse registro.
- Incluir no Markdown: data da consulta, pergunta/escopo, conclusão, fontes com URLs, nível de confiança e limitações.
- Usar nomes com data compacta `YYYYMMDD` e snake_case na pasta; verificar a pasta canônica da área antes de criar uma nova.
- Informar na resposta o caminho absoluto do arquivo salvo no MEGA.

## Pitfalls

- `web_extract` falha silenciosamente em SPAs (retorna HTML vazio mas HTTP 200) — verificar tamanho do retorno antes de confiar
- Resultados de busca podem estar desatualizados — sempre checar data/cronologia
- Operadores de busca funcionam diferente em backends diferentes (Exa, DDGS, Brave) — não assumir comportamento universal
- Não transformar links longos em "clique aqui" — mostrar URLs completas para verificabilidade
- NUNCA usar terminologia abstrata para detectar elementos HTML em auditorias (ex: procurar "feed" ao invés de `id=painelStatus`). Buscar SEMPRE IDs/classes/CSS selectors CONCRETOS existentes no DOM. False-negativos de regex são o erro #1 em QA de HTML.
