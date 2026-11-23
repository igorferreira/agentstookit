# Ônibus — extração de preços reais (Buser, ClickBus)

Receita para pegar preços/horários reais de passagens de ônibus (ex.: RJ↔SP) lendo os dados internos dos sites, sem brigar com formulários bugados. Complementa o fluxo de voo do SKILL.md (mesma fase de "verificação via browser", mas a técnica é extrair estado interno, não preencher form).

## Buser (fonte primária — dados completos)

1. **Navegar por URL com datas ISO, nunca pelo formulário:**
   `https://www.buser.com.br/onibus/{origem-slug}/{destino-slug}?ida=2026-11-26&volta=2026-11-28`
   - Query com data `dd-mm-2026` é IGNORADA (a página retorna o dia corrente) — só ISO funciona.
   - O datepicker da Buser está bugado ("Invalid Date", sem grade de dias) e rejeita eventos sintéticos React — não gastar tempo na UI.
   - Para buscar só a volta, trocar os slugs: `/onibus/sao-paulo-sp/rio-de-janeiro-rj?ida=YYYY-MM-DD`.
2. **Ler o estado interno Nuxt em vez de parsear cards:**
   `window.__NUXT__.pinia.search.gruposByDate` → array de slots `{datetime_ida, grupos[]}`.
   Campos úteis por grupo: `datetime_ida`/`chegada_ida` (ISO com offset), `origem.nickname`/`destino.nickname` (ponto de embarque/desembarque), `tipo_assento`, `vagas`, `company_friendly_name`, flags `closed`/`grupo_classe_closed` (filtrar). O store Pinia dehydrated não expõe actions — só dados; não tentar disparar busca por action.
3. **Preço cobrado = `ref_split_value`** (fallback `preco_base`, que é o valor cheio). `preco_rodoviaria` é referência de rodoviária, não o cobrado. Validar sempre: o valor tem que bater com um card visível na página.
4. Filtrar por janela de horário do usuário comparando `datetime_ida[11:16]` — o dataset cobre o dia inteiro, então qualquer janela (madrugada, pós-21h etc.) sai do mesmo dump.

## ClickBus (só como referência — limitada)

1. **Não perder tempo com API:** `search.clickbus.com.br` não existe mais (NXDOMAIN) e o BFF `bff.clickbus.com/web/api/v4/*` responde 403 WAF mesmo via `fetch` da própria página. Hook de fetch/XHR não captura nada — a busca de viagens é feita server-side (SSR), nunca no browser.
2. **Única via: SSR da página de resultados:**
   `https://www.clickbus.com.br/onibus/{from}/{to}?departureDate=YYYY-MM-DD&returnDate=YYYY-MM-DD`
   - Slugs no formato `rio-de-janeiro-rj-todos`, `sao-paulo-sp-todos` (descobrir outros via autocomplete `bff.clickbus.com/web/api/v4/places?clientId=2&limit=5&name=...` — esse endpoint SIM responde 200; a resposta é array direto, não `.content`).
   - Sem `departureDate` a página volta a data corrente.
3. **Limitação dura: o SSR expõe só ~8 viagens por perna, sempre da primeira página (horários de madrugada 00:05–01:30).** Scroll, lazy-load, `?page=N` e re-busca pelo painel Editar não trazem o resto; a hidratação React ainda limpa os cards SSR após interação — extrair o `body.innerText` IMEDIATAMENTE após a carga, depois de aceitar o banner de cookies.
4. **Regra de decisão:** para janela de horário específica do usuário (pós-21h, manhã etc.), a ClickBus não serve — usar o Buser. Citar ClickBus apenas como preço de referência da madrugada (Novo Rio → Tietê, Expresso Do Sul).

## Gotchas gerais

- Parsear o `innerText` dos cards da ClickBus por `split('Viaje com ')` + regex `HH:MM\norigem\nHH:MM\ndestino\nXh Ym`; preço em linha própria `R$169,99` (sem espaço) e clube em `No clube R$ 136,99`.
- Nunca comprar/reservar sem aprovação explícita do Usuário — registrar preços e links, ele compra na conta dele.
- Formato de entrega preferido: 3 opções por perna com horário, rota, assento e preço + combo recomendado com total; salvar no arquivo canônico da viagem no Drive e citar o link direto de compra.
