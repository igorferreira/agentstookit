# Snippets JS para extração de dados na Amazon Brasil

Use estes snippets com `browser_console(expression=<js>)` em páginas da Amazon Brasil (`amazon.com.br`). Cada snippet retorna um objeto JSON com os campos relevantes. Todos foram validados em navegação real (ago/2026).

## Snippet A — Listagem de busca (`/s?k=...`)

Retorna os 8 primeiros resultados com ASIN, título, preço à vista e link. Use para identificar o produto certo antes de abrir o `/dp/<ASIN>`.

```javascript
Array.from(document.querySelectorAll('[data-component-type="s-search-result"]')).slice(0, 8).map((el, i) => {
  const titleEl = el.querySelector('h2');
  const title = titleEl ? titleEl.innerText.trim() : 'N/A';
  const linkEl = el.querySelector('a.a-link-normal.s-no-outline, h2 a');
  const link = linkEl ? linkEl.href : 'N/A';
  const priceEl = el.querySelector('.a-price .a-offscreen');
  const price = priceEl ? priceEl.innerText.trim() : 'N/A';
  const asin = el.getAttribute('data-asin');
  return { idx: i, asin, title, price, link };
})
```

## Snippet B — Página de produto (`/dp/<ASIN>`)

Retorna título, preço à vista (com centavos exatos), parcelado, Pix/NuPay, vendedor (Marca), frete, reputação e ASIN.

```javascript
(() => {
  const data = {};
  data.titulo = document.querySelector('#productTitle')?.innerText.trim() || 'N/A';
  const priceBlock = document.querySelector('#corePrice_feature_div, #price');
  const priceWhole = priceBlock?.querySelector('.a-price-whole')?.innerText.trim() || '';
  const priceFraction = priceBlock?.querySelector('.a-price-fraction')?.innerText.trim() || '';
  data.preco_vista_formatado = (priceWhole && priceFraction) ? `R$ ${priceWhole},${priceFraction}` : (priceBlock?.querySelector('.a-offscreen')?.innerText.trim() || 'N/A');
  const installmentEl = document.querySelector('#installmentPrice, #installment-block .a-color-price, .a-section.a-spacing-small #installment');
  data.preco_parcelado = installmentEl?.innerText.trim() || document.querySelector('[id*="installment"]')?.innerText.trim().slice(0, 200) || 'N/A';
  data.pix_desconto = document.querySelector('#priceblock_saleprice, #corePrice_feature_div .savingsPercentage')?.innerText.trim() || 'N/A';
  data.vendedor = document.querySelector('#merchantInfo, #bylineInfo, #sellerProfileTriggerId')?.innerText.trim() || 'N/A';
  data.frete = document.querySelector('#deliveryMessageMirula, #mir-layout-DELIVERY_BLOCK, #delivery_feature_div')?.innerText.trim().slice(0, 300) || 'N/A';
  data.reputacao = document.querySelector('#acrPopover, [data-feature-name="reviews"] .a-icon-alt')?.getAttribute('title') || 'N/A';
  data.asin = document.querySelector('[data-asin]')?.getAttribute('data-asin') || 'N/A';
  data.url = window.location.href;
  return data;
})()
```

## Snippet C — Buybox detalhado (vendido por, enviado por, frete, estoque, parcelado total)

Use quando precisar separar explicitamente quem vende, quem envia, qual o parcelado total e quantos outros vendedores existem.

```javascript
(() => {
  const data = {};
  const sellerLink = document.querySelector('#sellerProfileTriggerId, a#bylineInfo');
  data.vendedor_link = sellerLink?.innerText.trim() || 'N/A';
  data.vendedor_href = sellerLink?.href || 'N/A';
  data.vendido_amazon_check = document.body.innerText.includes('Vendido por Amazon') || document.body.innerText.includes('Vendido e enviado por Amazon');
  data.buybox_text = document.querySelector('#merchantInfo, #desktop_buybox_feature_div, #rightCol')?.innerText.trim().slice(0, 800) || 'N/A';
  data.num_avaliacoes = document.querySelector('#acrCustomerReviewText')?.innerText.trim() || 'N/A';
  data.frete_detalhado = document.querySelector('#deliveryMessageMirula, #mir-layout-DELIVERY_BLOCK')?.innerText.trim() || 'N/A';
  data.prime = document.querySelector('.a-icon-prime, [aria-label*="Prime"]') ? 'Sim' : 'Verificar';
  return data;
})()
```

## Snippet D — CEP atual no header

Confirme o CEP antes de fechar prazo/frete. Retorna `cep_header` no formato "Bairro XXXXX-XXX" ou texto cru.

```javascript
(() => {
  const cepEl = document.querySelector('#glow-ingress-line2, #nav-global-location-slot, [data-action="nav-global-location-popover-link"]');
  return { cep_header: cepEl?.innerText.trim() || 'N/A' };
})()
```

## Snippet E — JSON final consolidado (use em página de produto)

Rode o snippet B + C juntos para um dump único:

```javascript
(() => {
  const B = (() => {
    const d = {};
    d.titulo = document.querySelector('#productTitle')?.innerText.trim() || 'N/A';
    const pb = document.querySelector('#corePrice_feature_div, #price');
    const pw = pb?.querySelector('.a-price-whole')?.innerText.trim() || '';
    const pf = pb?.querySelector('.a-price-fraction')?.innerText.trim() || '';
    d.preco_vista = (pw && pf) ? `R$ ${pw},${pf}` : 'N/A';
    d.preco_parcelado = document.querySelector('[id*="installment"]')?.innerText.trim().slice(0, 200) || 'N/A';
    d.frete = document.querySelector('#deliveryMessageMirula')?.innerText.trim().slice(0, 300) || 'N/A';
    d.reputacao = document.querySelector('[data-feature-name="reviews"] .a-icon-alt')?.getAttribute('title') || 'N/A';
    d.asin = document.querySelector('[data-asin]')?.getAttribute('data-asin') || 'N/A';
    d.url = window.location.href;
    return d;
  })();
  const C = (() => {
    return {
      buybox_text: document.querySelector('#desktop_buybox_feature_div, #rightCol')?.innerText.trim().slice(0, 800) || 'N/A',
      num_avaliacoes: document.querySelector('#acrCustomerReviewText')?.innerText.trim() || 'N/A',
      prime: document.querySelector('.a-icon-prime') ? 'Sim' : 'Verificar'
    };
  })();
  return { ...B, ...C };
})()
```

## Pitfalls dos próprios snippets

- `.a-offscreen` é arredondado (R$ 196, R$ 207). Para centavos exatos use SEMPRE `.a-price-whole` + `.a-price-fraction` juntos.
- O `buybox_text` (snippet C) mistura preço, parcelado, frete, vendedor e ações — pode chegar a ~800 chars. Não use como preço único; extraia campos estruturados.
- `[data-asin]` pode estar em qualquer elemento. O primeiro `data-asin` da página é geralmente o ASIN do próprio produto.
- `#deliveryMessageMirula` é o bloco dinâmico de frete que troca quando o CEP muda; capture logo após o carregamento, antes de rolar.
- A Amazon Brasil pode reescrever elementos sob A/B testing — se um seletor falhar, tente o alternativo listado em `||` nos snippets.
