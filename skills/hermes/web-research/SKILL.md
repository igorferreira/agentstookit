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

- Começar com poucas consultas de alto valor (em geral 3–5): uma ampla, uma com frase exata/identificador e, quando pertinente, uma em fonte oficial. Expandir só para preencher uma lacuna concreta; consultas quase duplicadas em grandes lotes consomem o limite de busca sem produzir evidência.
- Usar operadores avançados quando relevante: `site:`, `filetype:pdf`, `"exato"`, `-termo indesejado`.
- Para comparações entre 3+ opções, pesquisar cada opção separada.
- Assim que surgir uma fonte candidata, priorizar abrir e validar essa fonte em vez de continuar acumulando snippets.

### Fase 2 — Extração de Conteúdo Web

- Preferir `web_extract(urls=[...])` para páginas HTTP simples com conteúdo no HTML; depois conferir se o texto retornado é completo o bastante para a alegação pesquisada.
- Não confundir uma saída curta, truncada ou apenas um resumo agregado com extração da página. Verificar título, extensão do corpo e se os trechos necessários realmente estão presentes; tamanho de resultado ou quantidade de hits não é evidência factual.
- Se a extração estiver vazia ou materialmente incompleta, fazer GET direto da URL com cliente HTTP e User-Agent, registrar status e URL final e extrair o texto do HTML com `HTMLParser`/parser disponível, removendo scripts e estilos. O browser é necessário quando houver JavaScript que efetivamente renderiza o conteúdo, login ou interação.
- Quando o browser renderizar o texto, extrair `document.body.innerText` e depois imprimir apenas os parágrafos ou trechos ao redor do termo/identificador relevante; evitar despejar páginas longas, pois a saída pode ser truncada. Registrar URL e citação exata do trecho usado.
- Só classificar como SPA depois de verificar que o texto-alvo não está no HTML recebido. Para conteúdo em JSON embutido/data attributes (ex.: `initialState`, `<script type="application/json">`), extrair essa estrutura diretamente.
- Para SPA confirmada, evitar automatizar scroll/clique para apenas leitura; usar o fallback de baixar arquivos `.js` e procurar strings/contexto da página conforme `references/spa-extraction-pattern.md`.
- Para pesquisar arquivos PDF em lote (periódicos, atas ou catálogos de várias edições), seguir `references/pdf-archive-search.md`; isso é mais confiável que tratar retorno truncado de `web_extract` como corpus completo.
- Tratar snippets de busca como pistas, não como prova suficiente de uma alegação factual; validar a passagem na página ou em documento primário.

### Fase 3 — Validação Técnica

- Para verificar implementações (CSS, JS, HTML) de terceiros, ler arquivos-fonte diretamente via terminal (`curl` + `grep`, `cat`)
- Comparar resultados com especificações oficiais quando houver risco de informação desatualizada
- Validar claims técnicos contra documentação oficial verificável

### Fase 4 — Entrega

- Para referências a hoje, prazos e cronologia, usar primeiro o bloco de data/hora atual fornecido pelo sistema; se ele estiver ausente, consultar a hora por ferramenta permitida, sem inferir pelo relógio do modelo.
- Incluir URLs completas e verificáveis; informar status HTTP quando relevante e efetivamente verificado.
- Citar a fonte específica e a alegação que ela sustenta; não generalizar como "a internet diz".

### Pesquisas em formato dossiê

- Organizar por alegações e evidências: separar pistas fornecidas pelo usuário, fatos confirmados, inferências, contradições e lacunas.
- Para cada alegação central, registrar imediatamente no documento/ledger de evidências a fonte, autor/entidade, data de publicação e data do fato (se diferentes), trecho pertinente, URL, independência e nível de confiança; não depender de snippets, resumos agregados ou saídas temporárias da ferramenta, que podem não ficar preservados.
- Ao receber uma correção de identidade, trate-a como definição do sujeito pretendido e registre-a como informação do solicitante, não como corroboração externa. Preserve literalmente a grafia do usuário e, separadamente, a grafia documental. Reabra a fonte suspeita e valide título/H1/cabeçalho, corpo e identificadores distintivos; slug da URL, snippet ou coincidência de nomes não bastam. Se a fonte tratar de homônimo, exclua-a da evidência do sujeito ou mantenha-a apenas como pista explicitamente não probatória, retire inferências dependentes e audite as associações em todas as fontes, cronologias, sínteses e registros canônicos antes de concluir.
- Em vídeos e publicações de redes sociais, distinguir data de publicação de data da gravação/evento. Título, descrição ou legenda do uploader documentam a atribuição feita por aquela fonte, não provam por si só identidade, cronologia ou os fatos narrados.
- Não contar republicações ou matérias que copiam o mesmo despacho como confirmações independentes; anotar a provável cadeia de reprodução quando identificável.
- Uma busca sem resultado significa apenas “não localizado nas consultas/fontes examinadas”, nunca prova de inexistência.
- Quando o dossiê envolver processo judicial, confirme a ligação entre o fato pesquisado e o processo pela capa/andamento e pelos documentos oficiais — não basta uma busca nominal ou um número retornado pelo portal. Siga a cadeia de instâncias pelos identificadores oficiais do tribunal de origem e dos tribunais superiores; leia o teor das decisões e registre número, órgão, data, resultado e página/trecho pertinente. Para descrever a situação processual atual, confira o andamento oficial mais recente na data de corte; trate livros, notícias, blogs e relatórios institucionais como fontes secundárias e atribua a elas qualquer estado processual histórico que relatem, sem projetá-lo para o presente.
- Estruturar a entrega com síntese, cronologia, tópicos temáticos, inventário de fontes e limitações; não preencher lacunas biográficas por plausibilidade.

### Retomada de dossiê em andamento

- Antes de pesquisar de novo, leia o plano, o inventário/ledger de evidências, o registro de buscas e a nota canônica no MEGA; retome a primeira lacuna ainda aberta e não repita consultas já cobertas sem uma pergunta nova e concreta.
- Defina qual tipo de fonte poderia resolver essa lacuna antes de ampliar a busca (por exemplo: resultado oficial, registro contemporâneo ou identificação civil); priorize abrir e validar uma fonte candidata em vez de acumular consultas quase duplicadas.
- Se a nova rodada trouxer apenas snippets, republicações ou fontes já registradas, anote o escopo e o resultado no registro de buscas e atualize o plano/nota canônica quando forem os artefatos de status; não crie ficha de fonte nova nem altere a síntese factual sem uma passagem verificável.
- Mantenha explícita a diferença entre cobertura da busca e evidência: uma varredura improdutiva documenta onde se procurou, mas não comprova inexistência nem resolve a alegação.

### Fase 5 — Registro canônico do Igor

- Salvar toda pesquisa solicitada também no MEGA, em Markdown canônico na pasta da área correspondente; o arquivo de pesquisa interno não substitui esse registro.
- Incluir no Markdown: data da consulta, pergunta/escopo, conclusão, fontes com URLs, nível de confiança e limitações.
- Usar nomes com data compacta `YYYYMMDD` e snake_case na pasta; verificar a pasta canônica da área antes de criar uma nova.
- Informar na resposta o caminho absoluto do arquivo salvo no MEGA.

## Pitfalls

- Se `web_extract` falhar com erro "<backend> is a search-only backend and cannot extract URL", NÃO repetir a chamada: o backend configurado (ex.: ddgs) só busca. Corrigir uma vez `web.extract_backend` no config para um backend de extração (firecrawl/tavily/exa/parallel) e, na mesma execução, usar o fallback de GET direto com curl (já documentado na Fase 2) para não travar a tarefa.
- `web_extract` falha silenciosamente em SPAs (retorna HTML vazio mas HTTP 200) — verificar tamanho do retorno antes de confiar
- Resultados de busca podem estar desatualizados — sempre checar data/cronologia
- Operadores de busca funcionam diferente em backends diferentes (Exa, DDGS, Brave) — não assumir comportamento universal
- Não transformar links longos em "clique aqui" — mostrar URLs completas para verificabilidade
- NUNCA usar terminologia abstrata para detectar elementos HTML em auditorias (ex: procurar "feed" ao invés de `id=painelStatus`). Buscar SEMPRE IDs/classes/CSS selectors CONCRETOS existentes no DOM. False-negativos de regex são o erro #1 em QA de HTML.
