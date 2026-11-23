# SPA Content Extraction — Padrão Validado (12/09/2026)

## Quando usar

Quando `web_extract()` ou `curl` retornam uma página sem conteúdo textível — sinal de SPA (React/Vue/Angular) que injeta conteúdo via JavaScript após carregamento inicial. Exemplos típicos: catálogos de produtos dinâmicos, dashboards web, sites com indexação client-side.

## Método Validado

### Passo 1 — Baixar HTML e identificar links de scripts JS

```bash
cd /tmp && curl -sL <url-da-spa>.html > index.html
grep -oE '/assets/[^\"]+\.js' index.html > js_links.txt
```

> ⚠️ Em ambiente Hermes, preferir `search_files` ao invés de `grep`, e `read_file` ao invés de `cat`.

### Passo 2 — Baixar cada script individualmente

```bash
for url in $(cat js_links.txt); do
  filename=$(basename "$url")
  curl -sL "https://<domain>$url" > "$filename" 2>/dev/null
done
```

### Passo 3 — Buscar strings alvo nos arquivos baixados

```bash
# Se souber o termo-alvo específico:
grep -rli 'termo-alvo' *.js | xargs grep -oP '.{0,200}termo-alvo.{0,200}'
```

Ou se souber que é conteúdo pt-BR:

```bash
grep -rl 'pt-BR\|pt_br\|Português\|brasileiro\|real R$\|R\$ ' *.js
```

### Passo 4 — Verificar conteúdo encontrado

Comparar palavras-chave do alvo com o extraído. Se bater → extrair e formatar resultado.

## Limitações Conhecidas

- Não funciona com conteúdo renderizado via WebAssembly
- Arquivos minificados podem ter strings incompletas ou ofuscadas
- Dependência de CDN cache — pode precisar limpar antes de rebaixar
- Só recupera strings visíveis na UI — não dados internos de API

## Variantes

### Conteúdo embutido em JSON/`<script>` tag

Muitas SPAs injetam dados no HTML através de `<script type="application/json">` ou variáveis globais como `window.__INITIAL_STATE__`:

```bash
grep -A500 'application/json\|__INITIAL_STATE__' index.html | head -n 600 > data.json
python3 -c "import json,sys; d=json.load(sys.stdin); print(json.dumps(d,indent=2,ensure_ascii=False))" data.json
```

### Verificar tamanho do retorno antes de confiar

Se `web_extract()` retorna menos de ~500 caracteres, provavelmente está vazio para SPA:

```python
content = open('index.html').read()
if len(content.strip()) < 500 or '<script>' not in content:
    # Provavelmente SPA vazia — aplicar fallback .js
    pass
```

## Exemplo Real Validado (12/09/2026)

Durante QA responsivo dos escritórios TimeAutomático, um catálogo de cursos Workshop Tecleads estava inacessível via `web_extract`. Aplicando este padrão:

1. Baixar `workshop-ia.techleads.club/index.html`
2. Extrair links `/assets/*.js` encontrados no HTML
3. Baixar scripts JS individualmente
4. Grep por strings contendo "IA", "Agentes", "Prompt" — encontrou descrições completas dos módulos em português

Conteúdo extraído foi suficiente para responder consulta do usuário sobre módulos e preços do curso.

## Referências Relacionadas

- `../SKILL.md` — trigger e workflow geral de web research
- Skills de browser automation (`browser-use`) quando a leitura simples não basta e é necessário interação real (login, scroll, clique)
