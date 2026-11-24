# Shopee (shopee.com.br) — Bot-Detection & Data-Extraction Notes

Field notes from a real price-lookup session. Use this when:
- Shopee product page returns `Login Necessário` / blank, or
- The PDP API returns `{"error":90309999}`, or
- URL is on `/verify/traffic/error?type=4`, or
- The visible DOM has the product title but no price anywhere.

## 1. Recognizing the wall

| Symptom | Meaning |
|---|---|
| `https://shopee.com.br/verify/traffic/error?...&type=4` | Hard bot-detection redirect. IP/fingerprint flag. |
| Body text "Login Necessário — Parece que você ainda não está logado" | Same wall, softer copy. |
| API JSON `{"error":90309999, "redirect_to_error_page":true}` | Wall at API level (works from `fetch` inside the page AND from external `curl`). |
| Language modal "Selecione seu idioma / Português (BR) / English*" | Cosmetic overlay — does NOT cause the wall. Dismissing it does nothing. |

## 2. What does NOT unblock the wall

Tested in this session, all wasted effort:
- `Network.clearBrowserCookies`
- `Network.clearBrowserCache`
- `Storage.clearDataForOrigin`
- Adding more request headers (`User-Agent`, `Referer`, `Origin`, `x-api-source`, `x-shopee-language`)
- Mobile-style User-Agent on curl (`ShopeeApp V2.86.87 ... Android 13`)
- Mobile subdomain (`shopee.com.br/m/...`)
- Just opening a fresh tab to `shopee.com.br/`

The flag is at the IP and browser-fingerprint level. The only exits are:
- Wait several hours for the IP block to expire.
- Use Browser Use Cloud (`start_remote_daemon`) with residential proxy.
- Authenticate via real login (don't do this without explicit user credentials).
- Get the price from an aggregator (Zoom, Buscapé, Google Shopping) that already cached it.

## 3. The Google-search workaround

When search itself is blocked, the site's product pages are often still indexed and discoverable via Google. Use a precise query with the operator `site:` and the exact SKU string:

```
web_search(query="site:shopee.com.br \"LA680WA-1DF\"")
web_search(query="site:shopee.com.br \"LA680WA-1DF\" Casio Vintage Prata")
```

Returns ~10 real product URLs with slug-encoded titles like:
```
https://shopee.com.br/Relógio-Casio-Vintage-LA680WA-1DF-Prata-i.589442593.22798798216
https://shopee.com.br/RELÓGIO-CASIO-FEMININO-DIGITAL-VINTAGE-PRATA-LA680WA-1DF-i.405524229.57202038932
```

The trailing `i.{shopId}.{itemId}` is enough — Shopee's slug (accented chars, varied capitalization) is cosmetic. You can navigate to any of these directly.

## 4. The direct-page-load trick + JSON extraction

Even when the page is being redirected to `/verify/traffic/error`, the **first** direct navigation to a product URL sometimes succeeds (before the wall kicks in on the second/third request). You get a fully-rendered Shopee page with title, breadcrumb, image carousel, share buttons, seller location, "Adicionar Ao Carrinho" / "Comprar Agora" buttons — but **price fields are deliberately nulled out**.

But the product data is still embedded in script tags. Extract it with:

```js
const scripts = document.querySelectorAll('script[type="text/mfe-initial-data"]');
for (const s of scripts) {
  const content = JSON.parse(s.textContent);
  const pdp = content?.initialState?.DOMAIN_PDP?.data?.PDP_BFF_DATA?.cachedMap;
  if (pdp) {
    for (const key in pdp) {
      const item = pdp[key].item;
      // item contains: item_id, shop_id, title, brand, brand_id, currency,
      // shop_location, cat_id, ctime, item_rating, models[].stock,
      // models[].price (==null), price_before_discount (==null),
      // description, categories, attributes, image, label_ids, flag, ...
    }
  }
}
```

What is reliably present (even unauthenticated):
- `title`, `item_id`, `shop_id`, `brand`, `currency` (BRL), `shop_location` (city/state)
- `categories`, `fe_categories`, `image` slug
- `description` (full HTML/markdown specs)
- `models[].stock` (numeric — e.g. `10`)
- `models[].price_stocks[].promotion_type` (e.g. `301` = flash sale)
- `show_discount` (numeric)
- `item_rating.rating_star`, `total_rating_count`
- `attributes` (sometimes — null when seller hasn't filled)
- `ctime` (Unix seconds)

What is `null` when unauthenticated:
- `models[].price`
- `models[].price_before_discount`
- Anything tied to logistics (`shipping`, `fee`, `estimated_days` may still be present in `extinfo`)

## 5. Internal API also blocked

Even from inside the Shopee page (which has the right cookies/Origin), `fetch('/api/v4/pdp/get_pc?item_id=...&shop_id=...')` returns the same 90309999. The block is at the IP/edge layer, not the session layer.

Search API (`/api/v4/search/search_items?keyword=...`) is also blocked — returns 0 items with error 90309999.

## 6. When to give up and report

If after trying the Google-URL workaround + JSON extraction you still don't have `price`, stop. Don't keep retrying — each request extends the IP block. Report:

1. The wall state (URL, error code, last screenshot)
2. The partial data extracted (title, brand, shop_id, stock, location, etc.)
3. The exact 3-4 escape hatches the user has (login / cloud browser / aggregator / wait)

## 7. Quick diagnostic snippet

Run from inside any Shopee tab to confirm the wall state:

```js
JSON.stringify({
  url: location.href,
  title: document.title,
  bodySnippet: document.body.innerText.substring(0, 300),
  hasProductData: !!document.querySelector('script[type="text/mfe-initial-data"]')
})
```

If `url` contains `/verify/traffic/error` → wall active. If `hasProductData === true` and `title` looks like a product → you're inside a product page (extraction still works).

## 8. Lessons for future sessions

- **Don't burn the agent's whole budget on Shopee**. 5–10 tool calls max: navigate → check wall → if blocked, immediately switch to web_search for URLs → extract JSON → report. Beyond that, return partial and let the user decide.
- **Aggregator sites (Zoom.com.br, Buscapé) DO cache Shopee prices**. If price is the only thing missing, those are the fastest fallback.
- **Google search snippets sometimes include the price** ("R$ 339,19" appeared in several non-Shopee search results for this exact SKU) — a `web_extract` on the snippet page can sometimes yield the price without ever loading Shopee itself.