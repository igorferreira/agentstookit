---
name: amazon-price-search
description: Use to search and compare product prices on Amazon Brasil (amazon.com.br) — any product category (watches, electronics, hardware, books, fashion). Use this whenever Igor needs online prices, wants to cross-check physical-store prices (BoaDica/Infobarra) against Amazon, or needs to confirm "vendido por"/"enviado por" on a third-party marketplace listing. Load alongside boadica-price-search and mercadolivre-price-search for full price comparisons across physical Rio stores, Mercado Livre, and Amazon.
---

# Amazon Brasil — Pesquisa de Preços (amazon.com.br)

## Quando usar
- "Quanto custa X na Amazon Brasil?"
- Comparar preço online Amazon vs loja física (BoaDica/Infobarra) vs Mercado Livre
- Confirmar se uma oferta é vendida pela própria Amazon ou por terceiro (marketplace)
- Validar frete Prime, prazo de entrega e elegibilidade a devolução

## Estratégia de acesso adaptativa
1. Para Amazon Brasil (site dinâmico, dependente de CEP, com marketplace de terceiros e proteção antibot moderada), **carregue também a skill oficial `browser-use` e navegue como usuário real via Chrome/CDP**. Use-a para abrir a listagem de busca, clicar no produto, conferir preço à vista, parcelado, vendedor real e frete.
2. Prefira a sessão real do navegador quando o site depender de CEP, cookies, login já existente, variação do produto ou proteção antibot. Não apresente snippet de buscador, API ou raspagem de página estática como equivalente à navegação real.
3. Use `web_search` com `site:amazon.com.br` e o **código exato do modelo/SKU/ASIN** somente para descobrir URLs e candidatos. O snippet é pista, não confirmação de preço.
4. Se preço, ASIN, vendedor e disponibilidade não puderem ser confirmados na página real, forneça o link e marque `preço não confirmado`; nunca converta resultado antigo, blog ou outro ASIN em preço atual.
5. APIs de afiliados/PA-API são apenas auxiliares; não insistir nelas quando a tarefa pede simulação de navegação real.
6. Para instalação, diagnóstico e permissão CDP, consulte `references/browser-use-real-marketplace-navigation.md` (compartilhado com a skill `mercadolivre-price-search`).

## Estrutura de URL
- **Home:** `https://www.amazon.com.br/`
- **Busca/listagem:** `https://www.amazon.com.br/s?k=<termo-com-+>`
  - ex.: `https://www.amazon.com.br/s?k=Casio+Vintage+LA680WA-1DF+Prata`
- **Página de produto:** `https://www.amazon.com.br/<slug>/dp/<ASIN>`
  - ex.: `https://www.amazon.com.br/Rel%C3%B3gio-Feminino-Digital-Vintage-LA680WA-1DF/dp/B00FBO3JD0/`
- **Página de produto (formato curto):** `https://www.amazon.com.br/dp/<ASIN>`
- **ASIN** é o identificador canônico (= SKU). Sempre confirme o ASIN na página via atributo `data-asin` do card ou via `data-asin` do `<div id="averageCustomerReviews">`.
- **Outros vendedores:** `https://www.amazon.com.br/gp/offer-listing/<ASIN>` (pode estar obsoleto; hoje aparece como "Outros vendedores na Amazon — Comparar outras N ofertas").

## Passo a passo
1. Normalize a especificação: tipo, modelo, **ASIN** (quando conhecido), variação/cor/capacidade.
2. Navegue à home da Amazon Brasil e use a caixa de busca (`#twotabsearchtextbox` ou o `searchbox` "Pesquisar Amazon.com.br") para digitar o termo. Confirme o CEP — ele aparece no header como `A entrega será feita em <bairro> <cep>`; se não for o CEP do usuário, clique em "Atualizar CEP" e insira o CEP correto antes de prosseguir (preço, frete e prazo variam por CEP).
3. Pressione Enter; aguarde o carregamento da listagem (`[data-component-type="s-search-result"]`).
4. Identifique o produto certo pelo título + ASIN + preço. **Ignore** cards de patrocinado (`data-adfeedback-details`) se houver modelo idêntico em orgânico.
5. Entre na página de produto (`/dp/<ASIN>`). Confirme que URL, título e ASIN batem.
6. Extraia em conjunto via `browser_console(expression=...)`:
   - **título:** `#productTitle`
   - **ASIN:** atributo `data-asin` de qualquer elemento (card na listagem ou bloco de reviews) — também legível na URL `/dp/<ASIN>`
   - **preço à vista (centavos exatos):** `#corePrice_feature_div .a-price-whole` + `.a-price-fraction` (NÃO use só `.a-offscreen` porque ele é arredondado)
   - **preço parcelado:** procure por texto que case `em até \d+x de R$` ou `sem juros` (geralmente em `#installment-block`, `.a-section [id*="installment"]`)
   - **preço Pix / NuPay / desconto:** procure por texto contendo "à vista no Pix" ou "NuPay" no buybox
   - **vendido por:** texto entre "Vendido por" e o próximo bloco (geralmente `a#sellerProfileTriggerId` ou nó do `#merchantInfo`)
   - **enviado por:** texto entre "Enviado por" e o próximo bloco
   - **frete / entrega:** `#deliveryMessageMirula` ou `#mir-layout-DELIVERY_BLOCK` (cuidado: pode incluir propaganda do Amazon Now)
   - **reputação:** `i.a-icon-star span.a-icon-alt` ou `[data-feature-name="reviews"] .a-icon-alt`
   - **nº de avaliações:** `#acrCustomerReviewText` (formato `(691)`)
   - **em estoque:** texto contendo "Em estoque" no buybox
   - **URL final:** `window.location.href`
7. Tire print (`browser_vision(question=...)`) com confirmação visual dos campos críticos.
8. Salve JSON em `~/clawd/amazon_<slug>_preco.json` com `data_coleta` em ISO.

## Saída para orçamento/WhatsApp do Igor
- Texto puro, informal, pronto para copiar e colar.
- Sempre distinguir **preço à vista (Pix)** de **preço parcelado total**.
- Informar preço + link + **vendido por** + **enviado por** + frete.
- Se "Vendido por [terceiro] / Enviado por Amazon", marcar como marketplace FBA — não é venda direta da Amazon.
- Se houver "Outros vendedores na Amazon: a partir de R$ X", reportar como faixa alternativa, não como preço único.
- Incluir recomendação curta e avisar sobre garantia, política de devolução e prazo Prime.

## Pitfalls
- **Nome de produto impreciso: pedidos do tipo "TCL 1000 32 pl" ou "g87" citam faixa de preço ou série, não modelo. Identifique o modelo real correspondente e confirme que ele existe no mercado BR (site oficial + comparadores) ANTES de reportar preço; se o modelo não chegou ao Brasil, informe isso e apresente o equivalente real vendido aqui — nunca produza preço para SKU inexistente.**
- **Página de erro é transiente, não bloqueio definitivo: "Algo deu errado"/resposta vazia da Amazon costuma ser limite temporário — espere alguns segundos e retente, preferindo ir direto ao /dp/<ASIN> conhecido em vez de refazer a busca. Se o buybox não renderizar na página do produto, use a listagem /s?k= como superfície de extração (h2 + .a-price-whole + data-asin por card) e o regex de R$ no body text para revelar ofertas de terceiros; snippet de web_search com preço Pix/parcelado serve só como pista a confirmar na página real.**
- **ASIN errado:** títulos parecidos (LA680WA-1DF vs LA680WA-7DF vs LA680WA-1BDF) têm ASINs diferentes e preços diferentes. Confirme o ASIN antes de fechar.
- **Preço parcelado ≠ preço à vista:** Amazon mostra os dois lado a lado. Parcela sem juros de 6x de R$ 34,40 significa total R$ 206,15 — não é o mesmo que "R$ 34,40".
- **Marketplace:** "Vendido por SKINAO JOALHERIA, Enviado por Amazon" é terceiro usando logística da Amazon. Trate como terceiro, não como Amazon direta. Confirme `vendido_por` no buybox, não na barra de marca (`#bylineInfo` mostra "Marca: Casio", não vendedor).
- **CEP errado muda preço/frete:** a Amazon exibe CEP no header e recalcula frete/prazo por CEP. Sempre confira o CEP antes de afirmar prazo.
- **Amazon Quase Novo / Amazon Renewed:** se o card mencionar "Quase Novo" ou "Renewed", é usado/recondicionado, não novo. Não comparar com preço de novo.
- **Variação/cor/tamanho:** `/dp/<ASIN>` pode abrir numa variante diferente da anunciada. Confira o título completo.
- **Oferta relâmpago / Cupom:** preço riscado com desconto pode ser devido a cupom automático que some ao adicionar ao carrinho; o preço real é o do buybox, não o da listagem.
- **Snippet de buscador contaminado:** `site:amazon.com.br` pode trazer avaliações, lista de "Inspirado por", "Comparar com similares" — todos misturam SKUs diferentes. Use o snippet só para localizar a URL `/dp/<ASIN>`.
- **CEP Bela Vista 01319900 (default):** se o usuário não informar CEP, use o do perfil dele ou pergunte antes de fechar prazo de entrega.
- **CAPTCHA / consentimento:** se a Amazon mostrar CAPTCHA ou modal de consentimento, pare e peça ao usuário conforme `browser-use`; não insista em loop.
- **Preço à vista sem Pix:** alguns produtos só mostram preço "em 1x sem juros" — nesse caso `preco_vista` = `preco_parcelado_total`.
- **Preço Pix é um desconto percentual no buybox, não um número extraível:** o buybox mostra "N% off à vista no Pix e NuPay" sobre o preço cheio — calcule `pix = preco_cheio × (1 − N/100)` e registre os dois valores. Leia o percentual do texto do buybox em cada coleta (pode ser 5%, 9% ou outro); nunca presuma 9% nem reutilize o percentual de uma sessão anterior.
- **Cupom exige login para validar:** cupons do tipo "Salve o cupom / Faça login para resgatar" não podem ser confirmados sem checkout do usuário — reporte como cupom disponível (não validado) e instrua o Igor a testar antes de fechar; nunca some o cupom ao preço como se fosse aplicado.

## Cross-check multiloja
- Carregue `browser-use` e abra Amazon, Mercado Livre e (se hardware) BoaDica no Chrome real.
- Para cada loja: pesquise o SKU/modelo/ASIN, entre na página de produto e confirme variação, preço à vista, vendedor real, entrega, estoque e URL final.
- Compare **o mesmo SKU** (ou SKU equivalente — ASIN vs código do fabricante vs MLB) na mesma data/hora.
- Se Amazon mostrar "Outros vendedores na Amazon: N ofertas a partir de R$ X", abra `/gp/offer-listing/<ASIN>` ou clique em "Comparar outras N ofertas" para confirmar a faixa.
- Só faça ranking/totais com valores confirmados. Marque preço não confirmado como `consultar no link`.
- Guias de faixa de preço ("quanto vale pagar" por modelo em guias de Black Friday de grandes portais BR) aceleram o veredito: dão régua 🔥/👍/😐 por variante e mínimo histórico — cite como régua de referência, mas o preço atual confirmado continua vindo da página real.
- Quando o pedido for registrar histórico, faça append no arquivo canônico já existente do produto; registre data/hora, variante exata, preço à vista e parcelado separadamente, URL e vendedor/condições que foram vistos na página real. Snippets, preço antigo, bloqueio ou página incompleta nunca viram preço confirmado; se forem úteis, registre-os apenas como não confirmados e identifique o motivo.
- Não generalize que Amazon é sempre mais barato; compare o mesmo SKU no momento da pesquisa.

## Referências
- `references/amazon-dom-extraction-snippets.md` — snippets JS prontos para `browser_console(expression=...)` em páginas da Amazon Brasil (listagem, buybox, frete, reputação).
- `references/browser-use-real-marketplace-navigation.md` (compartilhado via skill `mercadolivre-price-search`) — instalação, permissão CDP e fluxo de navegação real em marketplaces.

## Fluxo resumido
1. Normalizar SKU/ASIN e variação
2. Atualizar CEP se necessário
3. Buscar na home; entrar no `/dp/<ASIN>` correto
4. Extrair via DOM (não snippet): título, ASIN, preço à vista, parcelado, Pix, vendedor, frete, reputação
5. Confirmar visualmente com print
6. Checar `Outros vendedores na Amazon` para faixa
7. Cross-check com Mercado Livre (e BoaDica se hardware)
8. Entregar texto puro + JSON + link; marcar preços não confirmados
9. Salvar JSON em `~/clawd/amazon_<slug>_preco.json`
