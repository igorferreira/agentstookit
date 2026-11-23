---
name: flight-search
description: "Buscar passagens aéreas com anti-bot e SPAs de preço."
tags: [travel, flights, pricing, booking]
---

# Flight Search & Price Comparison

## Trigger

Usar quando o usuário pedir para buscar passagens aéreas, comparar preços de voos, encontrar a rota mais barata, verificar disponibilidade de voos, ou verificar preços de rotas específicas (ex: SDU↔CGH, GRU↔GIG). Também coberto: tarefas de monitoramento de preços de voos e alertas de queda. Para ÔNIBUS (ex.: RJ↔SP na Buser/ClickBus), seguir `references/onibus-buser-clickbus.md` — a técnica é extrair o estado interno do site, não preencher formulário.

## Workflow

### Fase 1 — Pesquisa Inicial (web_search)

- **SEMPRE começar com `web_search`** para dados de preço cacheados de agregadores (Skyscanner, KAYAK, Decolar, Google Flights)
- Consultas direcionadas: `"[Origem] [Destino] voos baratos [mês/ano] 2026"` ou `"[Cia Aérea] [Origem] [Destino] tarifa [data]"`
- Para rotas BR: incluir `"Brasil"` ou `"BR"` no query para filtrar resultados locais
- **Não tentar extração direta** de agregadores (Skyscanner, KAYAK, Decolar) via `web_extract` — são SPAs com renderização client-side JS
- Capturar preços estimados do web_search (títulos e snippets geralmente contêm faixas de preço)

### Fase 2 — Verificação Manual (Browser)

- Para confirmação de disponibilidade e preço exato, usar `browser_exec` com `browser-use`
- **Navegar diretamente para o site da companhia aérea** (não para agregadores)
- **URLs atualizadas das companhias BR** (ver `references/airline-urls.md`):
  - Azul: `https://www.voeazul.com.br/br/pt/home/reservas`
  - GOL: `https://www.gol.com.br/` (verificar URL atual de busca)
  - LATAM: `https://www.latam.com/pt-br/`
- **Preencher formulário manualmente** via `fill_input` e `click_at_xy` (não via API/automation)
- **Capturar screenshot** após preenchimento para verificar se o formulário carregou corretamente
- **Não tentar automação profunda** (preencher datas, submeter busca) — sites de companhias aéreas bloqueiam com 403 Access Denied

### Fase 3 — Cálculo de Custo Total

- Para rotas urbanas (SDU↔CGH, GRU↔GIG, etc.), **sempre adicionar custo de transporte terrestre**:
  - Uber/Transfer: estimar R$ 115–170 por trecho (Centro→Aeroporto em capitais)
  - Total = Preço da passagem + 2× Custo do transfer (ida + volta)
- Registrar endereços de origem/destino no MEGA (`~/MEGA/Documentos/pessoal/viagens/`) para cálculo preciso
- Exemplo: SDU→CGH com transfer = R$ 395 (passagem) + R$ 115 (Casa→SDU) + R$ 170 (CGH→Casa SP) = **R$ 680 total**

### Fase 4 — Registro e Monitoramento

- Salvar resultados em `~/MEGA/Documentos/pessoal/viagens/` com nome `YYYYMMDD-rotas-precos.md`
- Incluir: data da consulta, rotas, preços estimados, fontes, custo total com transferes
- Para monitoramento semanal: criar cron job que roda `web_search` e alerta se preço cair abaixo do alvo
- Cron sugerido: `semana seg 09h` com query `"[rota] voos baratos [mês] 2026"`

## Pitfalls

- **Sites de companhias aéreas bloqueiam automação** — 403 Access Denied é o padrão (Azul, GOL, LATAM). Não tentar `curl` ou `web_extract` direto; usar `browser_exec` com navegação manual ou aceitar que o preço exato só aparece após preenchimento do formulário.
- **Agregadores são SPAs** — Skyscanner, KAYAK, Decolar, Google Flights não retornam dados via `web_extract`. O web_search retorna snippets com faixas de preço, mas a extração detalhada precisa ser manual.
- **URLs de busca mudam periodicamente** — Azul mudou de `passagens.voeazul.com.br/pt/pesquisa` (404) para `voezazul.com.br/br/pt/home/reservas`. **Sempre verificar URL atual** no web_search antes de navegar.
- **Preços variam com antecedência** — 7+ semanas antes: preços estáveis; 4-5 semanas: pode baixar R$ 30-50; 1-2 semanas: preço final. Regra: se não precisa voar urgentemente, esperar 4-5 semanas antes para economizar.
- **Custo total ≠ preço da passagem** — para rotas urbanas (SDU↔CGH, GRU↔GIG), sempre somar transporte terrestre (Uber/transfer). Um voo de R$ 400 pode custar R$ 680 total com transferes.
- **Agent-browser CLI tem quirks** — `eval` precisa de sintaxe específica, `--session-name` é obrigatório para fluxos multi-passo, `--timeout` precisa estar na posição correta. Para tarefas complexas, usar `browser_exec` com `browser-use` (mais estável).
- **Cookies e sessões são necessários** — algumas APIs internas das companhias exigem cookies válidos (obtidos após navegação inicial). Não tentar reutilizar cookies de sessões antigas.

## Ferramentas

- **web_search**: fonte primária de dados de preço (cacheado de agregadores)
- **browser_exec + browser-use**: verificação manual de disponibilidade e preço exato
- **agent-browser CLI**: alternativa para automação básica, mas com mais quirks
- **Terminal (curl)**: NÃO funciona para sites de companhias aéreas (bloqueio anti-bot)
- **web_extract**: NÃO funciona para SPAs (Skyscanner, KAYAK, Decolar)

## Referências

- `references/airline-urls.md`: URLs atualizadas dos sites de busca das principais companhias aéreas brasileiras (Azul, GOL, LATAM) e agregadores
- `references/urban-route-costs.md`: estimativas de transporte terrestre para rotas urbanas (SDU↔CGH, GRU↔GIG, etc.)
- `references/onibus-buser-clickbus.md`: receita de extração de preços de ônibus — Buser via estado Nuxt (`?ida=ISO` + `__NUXT__.pinia.search`) e ClickBus via SSR (`?departureDate=ISO`, limitado a ~8 viagens/madrugada)

## Regras do Igor

- **Prioridade: menor custo total** (passagem + transferes), não apenas preço da passagem
- **Registrar endereços** (origem/destino) no MEGA para cálculo preciso de transferes
- **Alertar sobre antecedência** — se a data é >7 semanas, sugerir esperar 4-5 semanas para economia
- **Formato de entrega**: tabela com modal, preço ida+volta, transferes, custo total, recomendação
