---
name: boadica-price-search
description: Use to search and compare computer/hardware prices on BoaDica (boadica.com.br), the Rio de Janeiro price-comparison site for PC parts, RAM, SSD, notebooks, monitors, etc. Navigates category trees, extracts prices by store/model/region, and locates specific stores (e.g. Infobarra/Info Barra). Load whenever Usuário (or the tech-pc persona) asks to find the price of computer hardware, compare prices across Rio stores, or check a specific store's listing.
---

# BoaDica — Pesquisa de Preços (boadica.com.br)

Site brasileiro de **comparação de preços de informática** focado em lojas do **Rio de Janeiro**. As lojas cadastram os próprios preços (não há comissão/vínculo do site).

## Quando usar
- "Quanto custa X?" (RAM, SSD, processador, notebook, placa de vídeo...)
- "Pesquisa no boadica e acha o preço na loja Y"
- Comparar preço entre lojas do RJ
- Orçamento de peças para upgrade/conserto

## Estrutura de URL
- Homepage: `https://boadica.com.br/`
- Página de categoria: `https://boadica.com.br/pesquisa/{slug}`
  - Exemplo confirmado: `memorias_notebooks` = "Memórias para Notebooks"
- Página de preços (resultados): `https://boadica.com.br/pesquisa/{slug}/precos?{params}`

## Passo a passo (browser)

### 1. Abrir a categoria
Navegue até `https://boadica.com.br/pesquisa/{slug}`. Slugs conhecidos:
- `memorias_notebooks` → Memórias para Notebooks
- (`discos_hd_ssd`, `ssd`, etc. — descubra pelo link na home ou pesquise)

A página de categoria lista **subcategorias** (ex.: "Para Notebook DDR4 de 8 GB") e **filtros por fabricante** (Kingston, Crucial...).

### Slugs de categoria conhecidos
- `memorias_notebooks` → Memórias para Notebooks
- `arm_ssd` → SSD - Solid State Drives
- `arm_hd` → Discos (HD) e SSD
- Descubra outros pelo link na home (extraia `href` dos links da árvore de categorias).

### 2. Descobrir a URL de resultados da subcategoria
Os links de subcategoria usam query params opacos. NÃO adivinhe — extraia o `href` com JS no console:

```js
Array.from(document.querySelectorAll('a'))
  .filter(a => a.textContent.includes('DDR4 de 8'))
  .map(a => a.href)
```

Depois navegue direto no `href` retornado.

**Padrão de params (exemplos confirmados):**
- RAM: `.../memorias_notebooks/precos?ClasseProdutoX=3&CodCategoriaX=15&XT=1&XE=4&XG=4` (XE=4 → DDR4, XG=4 → 8GB)
- SSD 256GB: `.../arm_ssd/precos?ClasseProdutoX=15&CodCategoriaX=6&XT=2&XM=0` (XT=2 → 200–300GB)
- SSD 512GB: `.../arm_ssd/precos?ClasseProdutoX=15&CodCategoriaX=6&XT=4&XM=0` (XT=4 → 512–980GB)

### 3. Ler os preços (resultados)
Na página `/precos`, a tabela de resultados tem as colunas:
**Fabricante | Modelo | Especificação | Preço R$ | Vendedor | Local**

A página tem filtros (`<select>` reais, embora componentes visuais possam parecer customizados):
- **Modelo** (lista de produtos específicos)
- **Região da loja** (Barra/Recreio/Jacarepaguá, Centro, Zona Norte, Zona Oeste, Zona Sul...)
- **Tipo** (OEM / BOX)
- **Loja** (lista de lojas)
- Paginação no rodapé ("Página 1 de 9")

## Extraindo dados (importante)
O `browser_snapshot` (accessibility tree) **trunca** a tabela de preços. Para ler tudo, use `browser_console` com o texto completo:

```js
document.body.innerText.substring(0, 6000)  // ajuste o range para paginar
```

O `innerText` contém fabricante, modelo, especificação, preço, vendedor, telefone e região de cada linha.

## Filtrar por loja/região/tipo (como aplicar o filtro)
Os filtros são `<select>` reais (Modelo/Região/Tipo/Loja) dentro de um `<form method="get">`. Para aplicar **programaticamente** via `browser_console`:

```js
// achar o select da região (o que tem option value="D" = Barra/Recreio)
const sels = Array.from(document.querySelectorAll('select'));
const regiao = sels.find(s => Array.from(s.options).some(o => o.value === 'D'));
regiao.value = 'D';
regiao.dispatchEvent(new Event('change', {bubbles:true}));
// clicar "Listar" para aplicar (a página atualiza sem mudar a URL)
Array.from(document.querySelectorAll('button')).find(b => b.textContent.trim()==='Listar').click();
```

**Valores da Região:** `D`=Barra/Recreio/Jacarepaguá, `A`=Centro, `B`=Zona Sul, `C`=Zona Oeste, `E`=Zona Norte, `F`=Niterói, `G`=Baixada, `K`=Região dos Lagos.

Depois de clicar "Listar", ler de novo o `innerText` — o conteúdo é atualizado in-place (a URL não muda).

## Filtrar por loja específica
1. Na página `/precos`, busque o nome da loja no `innerText`:
   ```js
   (() => { const t = document.body.innerText.toLowerCase();
     const i = t.indexOf('infobarra');
     return i < 0 ? 'NÃO encontrado' : t.substring(i-300, i+600); })()
   ```
2. Se não achar, a loja pode estar cadastrada com outro nome (ex.: "Info Barra" vs "Infobarra", "Info Box", "Info Center Campo Grande"). Liste as lojas presentes no dropdown "Loja" ou no texto.

## Pitfalls
- **Preços à vista**: cartão/parcelado pode ser maior; confirmar diretamente.
- **Preço/estoque auto-reportado**: o BoaDica não valida; registrar data/hora e confirmar com a loja.
- **Filtro de região é obrigatório quando o usuário limita o local**: se pedir Barra da Tijuca, aplique `D` e não apresente Centro/Niterói como opção principal.
- **Nome de loja pode ser aproximado**: não force equivalência entre "Infocentro", "Infobarra", "Info X" ou "Acti Info". Liste os nomes cadastrados e peça confirmação quando necessário.
- **Endereço completo**: a tabela de resultado pode mostrar apenas bairro/região. Abra o detalhe do produto/loja ou pesquise a loja antes de afirmar endereço; telefone + região não equivalem a endereço completo.
- **Filtros são `<select>` reais**: descubra pelo conteúdo das opções, não pela posição fixa. O front-end pode mudar a aparência.
- **Estado do browser pode ser perdido**: se o documento vier vazio/novo, reabra a URL e reaplique filtros; registre isso como retry, não como limitação permanente.
- **Infobaú não é Infobarra**: é conteúdo/banner do site.
- **Compatibilidade primeiro**: confirme DDR4/SO-DIMM/2400, quantidade de pentes e SATA 2,5"/SKU antes de comparar.
- **Não generalizar diferença online/física**: compare o mesmo SKU, na mesma data, e só use preços confirmados.
- **Página 1 tende a genéricos**: filtre fabricante/modelo exato quando o usuário escolheu uma linha específica.

## Saída para orçamento do Usuário
- Respeitar exatamente região e combinações pedidas.
- Informar loja cadastrada, preço à vista, telefone, bairro/região, link do produto/detalhe e endereço completo somente se verificado.
- Fornecer texto puro, informal e pronto para WhatsApp quando o destinatário for amigo.
- Não incluir mão de obra no total quando Usuário fará gratuitamente; pode mencionar separadamente que uma loja/técnico cobraria instalação, sem inventar valor.
- Separar preço confirmado de estimativa e calcular totais apenas com valores sustentados.

## Referências
- Para validação de SKU e comparação com marketplaces, veja `mercadolivre-price-search/references/hardware-upgrade-price-validation.md`.

## Fluxo resumido
1. `browser_navigate` → `https://boadica.com.br/pesquisa/{slug}`
2. Extrair `href` da subcategoria com `browser_console` (querySelectorAll filter)
3. `browser_navigate` → URL de `/precos?...`
4. `browser_console` → `document.body.innerText` para ler preços/lojas (o texto vem no formato `Fabricante \nModelo \nEspecificação\nPreço R$ \nVendedor \nLocal` por item)
5. Filtrar por loja/região e reportar os valores (sempre com o aviso "à vista, confirmar com a loja")

## Notas históricas de sessão (não usar como preço vigente)
- Faixas observadas em ago/2026 foram voláteis e variaram fortemente por região, fabricante e marketplace.
- `480 GB`, `500 GB` e `512 GB` pertencem a SKUs/faixas diferentes; não substitua um pelo outro sem explicitar.
- O cadastro de lojas muda. Não mantenha como verdade permanente que uma loja existe ou não existe no BoaDica; consulte o dropdown na sessão atual.
- Sempre refaça a pesquisa no dia e compare o mesmo modelo/SKU.
