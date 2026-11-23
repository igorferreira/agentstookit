# Mercado Livre — Camadas de bot detection e fallback

Esta referência documenta os padrões de defesa observados no `mercadolivre.com.br` quando o acesso via navegador headless é detectado. Use para diagnosticar e decidir o próximo passo quando o navegador real for bloqueado.

## Três camadas observadas

### Camada 1 — Redirect de verificação de conta
- URL inicial: `https://www.mercadolivre.com.br/jm/search?...`
- Resposta: redirect para `https://www.mercadolivre.com.br/gz/account-verification?go=...&tid=...`
- Conteúdo: botões "Sou novo" / "Já tenho conta" exigindo login
- **Diagnóstico**: `curl -I` da URL mostra `200` mas body é a página de verificação.

### Camada 2 — JavaScript Proof-of-Work (Anubis-like)
- Estrutura: página mínima com `<button id="continue-button" disabled>` + script inline
- Cookie de controle: `_bmstate=<a>;<i>` (setado client-side pelo challenge inicial)
- Mecânica: lê `_bmstate`, calcula `SHA256(a + c)` até encontrar hash com prefixo de `"0"*i` zeros
- Resposta: seta `_bmc=<a>;<c>` e chama `navigateToContinue()` que faz `window.location.href = <url_original>`
- Server valida `_bmc` e libera o produto.
- **Observação**: se o JS resolve e o navegador redireciona mas a página final mostra `Hubo un error accediendo a esta pagina...`, o servidor detectou headless mesmo com PoW correto.

### Camada 3 — API REST bloqueada por política
- Endpoint: `https://api.mercadolibre.com/items/<MLB_ID>`
- Erro retornado: `{"blocked_by":"PolicyAgent","code":"PA_UNAUTHORIZED_RESULT_FROM_POLICIES","message":"At least one policy returned UNAUTHORIZED.","status":403}`
- Endpoint de busca: `https://api.mercadolibre.com/sites/MLB/search?q=...` → mesmo `403 forbidden`
- **Causa**: bloqueio por geolocalização do IP (precisa ser IP residencial brasileiro).
- **Não é contornável** com User-Agent, Accept-Language ou cookies — é checagem server-side.

## Sintomas de bloqueio no navegador via CDP

| Sintoma | Camada |
|---|---|
| Página `Olá! Para continuar, acesse sua conta` com botões Sou novo/Já tenho conta | 1 |
| Página com spinner "Continuar" + spinner JS challenge | 2 |
| URL correta mas body mostra `Hubo un error accediendo a esta pagina...` | 2 (PoW ok, mas headless detectado) |
| `Mercado Libre - Donde comprar y vender de todo` no header (espanhol, não PT-BR) | 2 (detectado como bot, caiu na versão argentina) |
| `User-Agent: HeadlessChrome/...` exposto | indicador de que será bloqueado |

User-Agent exposto em sessão headless típica:
```
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/151.0.0.0 Safari/537.36
```

## Fallback chain quando o navegador é bloqueado

Não insista em loop no browser. Use esta cadeia em ordem:

1. **`web_search` com `site:mercadolivre.com.br` + SKU exato** — coleta URLs canônicos (`/p/MLB...` e `/MLB-..._JM`) e snippets de preço. Snippet é **pista**, não confirmação.

2. **Listas de agregadores parceiros** que indexam ML oficialmente:
   - `buscape.com.br/busca/<sku>`
   - `zoom.com.br/busca/<sku>`
   - `jacotei.com.br/busca?q=<sku>`
   Buscapé/Zoom costumam mostrar preço, vendedor e botão "ir à loja". Preço é confirmado pelo agregador, link aponta para a página real no ML.

3. **Lojas oficiais Casio** que vendem o mesmo SKU com preço público:
   - `lojasrenner.com.br` (busca por `LA680WA-1DF`)
   - `cea.com.br`
   - `newlooktime.com.br`
   - `aconfianca.com.br`

4. **Amazon BR** `amazon.com.br/<dp/ASIN>` — comparar como concorrente, não como venda direta da Casio.

## Links curtos `meli.la` compartilhados pelo usuário

- `meli.la/<id>` NÃO é link de produto: resolve para `mercadolivre.com.br/social/<usuario>?...forceInApp=true` — link de compartilhamento social que SÓ abre no app do ML logado na conta do remetente. Fora do app dá `Hubo un error accediendo a esta pagina` em qualquer variação (com/sem `forceInApp`, URL social base). Não insistir em abrir variações.
- O ID do produto vem dentro do parâmetro `ref=` (token assinado) — não é decodificável.
- Procedimento: confirmar o destino com `curl -s -o /dev/null -w '%{redirect_url}' https://meli.la/<id>` (com UA de navegador); se for `/social/`, pedir ao usuário o NOME/MODELO do produto ou o link completo (`mercadolivre.com.br/...MLB-...` ou `/p/MLB...`).

## Outras lojas quando o ML bloqueia

- Quando o ML cai na camada 2, continuar o comparativo em lojas que costumam responder ao navegador real: **KaBuM** e **Fast Shop** (abrem direto) e **Amazon** (interstitial "Continuar comprando" — clicar o botão e refazer a navegação; se o dp/ASIN direto cair na home, navegar pela URL de busca `/s?k=...` e entrar no item).
- **Magalu** responde 403 CloudFront para IP de datacenter — não insistir; rotular como bloqueado no comparativo.
- **Buscapé e Zoom** bloqueiam o navegador (403 CloudFront) mas RESPONDEM via `curl` com UA de navegador + `Accept-Language: pt-BR` (HTTP 200, HTML completo). Fluxo: `curl -s -L -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ... Chrome/131 Safari/537.36" -H "Accept-Language: pt-BR,pt;q=0.9" "https://www.buscape.com.br/busca/<sku-com-+>" -o /tmp/buscape.html` e parsear o HTML (a página é Next.js estático, não precisa de JS).
- Parsing Buscapé/Zoom: cada card de oferta tem `data-testid="product-card::name"`, `product-card::price` (`<strong>R$ X</strong>`) e `<span>Via <loja></span>`. SEMPRE dividir o HTML por bloco de card (split em `product-card::image`) ANTES de casar nome↔preço — um regex global sobre o HTML inteiro desalinha nomes e preços de cards vizinhos. Filtrar acessórios do mesmo termo de busca (ex.: "capa rígida para <produto>" aparece nas buscas com preço menor que o produto).
- Índice do agregador pode estar desatualizado vs a página viva da loja: se o mesmo vendedor aparecer mais barato na página real, use o preço vivo e rotule a divergência.
- No KaBuM, o PRIMEIRO `R$` no `innerText` pode ser o preço antigo RISCADO (span com classe `line-through`), e o preço vigente pode nem aparecer na extração por nós-folha. Validar o preço por aritmética: preço PIX = total parcelado × 0,95 (ex.: 6x R$ 26,31 = R$ 157,86 → PIX ≈ R$ 149,99). Se o valor extraído não fechar com o parcelamento, procure o span `line-through` e o card de compra completo.

## Quando desistir do produto principal no ML

Se após aplicar a fallback chain você tem:
- URL canônica ML conhecida
- Preço confirmado em pelo menos **um agregador parceiro** (Buscapé/Zoom)
- Link ML fornecido

Entregue o seguinte formato:
```
Produto: <nome completo>
SKU: <código>
Preço à vista: R$ <valor> (fonte: Buscapé — última coleta <data>)
Preço parcelado: 12x R$ <valor> sem juros
Frete: <verificar no link>
Vendedor: <nome> (<reputação>) — se conhecido
Link ML: <url canônica>
Link Buscapé: <url da listagem>
Status: preço de listagem agregado, não do anúncio individual
```

**Nunca**:
- Inventar preço "estimado" quando não foi confirmado.
- Apresentar snippet de buscador como preço vigente.
- Misturar SKU Prata com Prata/Preto ou Preto — são SKUs adjacentes (`LA680WA-1DF` vs `LA680WA-1DF` variação).
- Confundir `MLB26106184` (canônico Prata) com `MLB2795973422` ou `MLB1724144651` (anúncios de variações prata/preto).

## Reprodução do challenge JS (referência técnica)

O challenge está em `script type="module"` com SHA256 via `crypto.subtle.digest`. Estrutura relevante:

```js
// 1. Lê _bmstate do cookie: formato "<a>;<i>"
const state = document.cookie.split(";").find(c => c.trim().startsWith("_bmstate="))
const [a, i] = state ? decodeURIComponent(state.split("=")[1]).split(";") : [null, null]

// 2. Se i==="0" ou null, c=0 (trivial, sem PoW real)

// 3. Senão, busca c tal que SHA256(a + c).startsWith("0".repeat(i))

// 4. Seta _bmc = "<a>;<c>" e redireciona para a URL original
```

Ataque por curl é teoricamente possível mas:
- Exige resolver SHA256 iterativo (pode levar minutos se i > 4)
- O servidor **ainda detecta** headless no header/cookie set mesmo com PoW correto
- Resultado prático: bloqueio na camada 2 mesmo após sucesso na camada 1

## TL;DR para próxima sessão

Quando `mercadolivre.com.br` retornar qualquer página de erro/verificação:
1. **Não tente loop** — vai continuar bloqueado.
2. **Use Buscapé/Zoom** para confirmar preço.
3. **Use `web_search`** só para achar URL canônica ML.
4. **Entregue preço agregado + link ML**, rotulado como não-confirmado no anúncio individual.