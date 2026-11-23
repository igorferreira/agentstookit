---
name: mercadolivre-price-search
description: Use to search and compare product prices on Mercado Livre Brasil (mercadolivre.com.br) — RAM, SSD, hardware, and any product. Use this whenever Igor (or the tech-pc persona) needs online prices to cross-check physical-store prices (BoaDica/Infobarra) or find the best online deal. Load alongside boadica-price-search when doing full price comparisons.
---

# Mercado Livre Brasil — Pesquisa de Preços (mercadolivre.com.br)

## Quando usar
- "Quanto custa X no Mercado Livre?"
- Comparar preço online vs loja física (BoaDica/Infobarra)
- Achar o menor preço de hardware/qualquer produto online

## Estratégia de acesso adaptativa
1. Para Mercado Livre e outros marketplaces dinâmicos/protegidos, **carregue também a skill oficial `browser-use` e navegue como usuário real via Chrome/CDP**. Use-a para abrir listagens, clicar no anúncio, selecionar capacidade/variação, conferir preço, vendedor, estoque, frete e reputação.
2. Prefira a sessão real do navegador quando o site depender de JavaScript, localização/CEP, cookies, login já existente ou proteção antibot. Não apresente scraping, snippet de buscador ou API como equivalente à navegação real.
3. Use `web_search` com `site:mercadolivre.com.br` e o **código exato do modelo** somente para descobrir URLs e candidatos. O snippet é pista, não confirmação de preço.
4. Se preço, SKU, vendedor e disponibilidade não puderem ser confirmados na página real, forneça o link e marque `preço não confirmado`; nunca converta resultado antigo, artigo ou outro SKU em preço atual.
5. APIs públicas são apenas auxiliares. Não insistir nelas quando a tarefa pede simulação de navegação real.
6. Para instalação, diagnóstico e permissão CDP do `browser-use`, consulte `references/browser-use-real-marketplace-navigation.md`.

## Estrutura de URL (para interpretar resultados)
- **Busca/listagem:** `https://lista.mercadolivre.com.br/<termo-com-hifens>`
  - ex.: `https://lista.mercadolivre.com.br/ssd-kingston-a400-480gb`
- **Produto de catálogo:** `https://www.mercadolivre.com.br/<slug>/p/MLB<ID>`
  - ex.: `.../ssd-kingston-480gb-sata-iii-a400-sa400s37480g-preto/p/MLB27966626`
- **Anúncio único (lojista):** `https://www.mercadolivre.com.br/<slug>/up/MLBU<ID>`

## Passo a passo
1. Normalize a especificação antes de comparar: tipo, formato, capacidade, frequência/interface e **SKU exato**.
2. Monte a query com produto + modelo + `site:mercadolivre.com.br`:
   ```
   web_search(query="SSD Crucial BX500 CT480BX500SSD1 site:mercadolivre.com.br")
   ```
3. Prefira página individual `/p/MLB...` ou anúncio `/MLB-...` a uma busca genérica. Se abrir no browser, extraia os dados do DOM e confirme que título, SKU, capacidade e preço são do mesmo item.
4. Leia os trechos (`description`) apenas como pista. Um trecho pode combinar ofertas relacionadas ou preço de outro SKU.
5. Para várias ofertas, use a URL de listagem como **link de consulta**, não como prova de um preço exato.
6. Registre data/hora, preço à vista, vendedor quando visível, condição, frete não incluído e link.
7. Faça cross-check com pelo menos uma loja concorrente, mas só compare valores realmente confirmados.

## Saída para orçamento/WhatsApp do Igor
- Texto puro, informal, pronto para copiar e colar.
- Mostrar opções exatamente no escopo solicitado (ex.: `1×4 GB` ou `2×8 GB`; `240 GB` ou `480 GB`).
- Informar preço + link por loja; se não houver preço verificável, escrever `consultar no link`.
- Calcular totais somente com preços confirmados ou rotulá-los claramente como faixa/estimativa.
- Incluir uma recomendação curta e avisar sobre frete, reputação, nota fiscal e garantia.
- Salvar também um relatório Markdown no diretório do projeto quando solicitado.

## Pitfalls
- **Acesso variável:** páginas podem abrir normalmente, pedir CAPTCHA, redirect para `gz/account-verification`, retornar challenge JS de SHA256 PoW, ou exibir `Hubo un error accediendo a esta pagina...` (sintoma de headless detectado pelo servidor, NÃO erro real do usuário). Veja `references/mercadolivre-bot-detection-fallback.md` antes de tentar loop.
- **Bloqueio em três camadas:** ML combina (1) verificação de conta obrigatória, (2) Anubis-like PoW em JS, e (3) `PolicyAgent PA_UNAUTHORIZED_RESULT_FROM_POLICIES` na API REST por geolocalização. Não existe uma combinação de headers/UA que contorne a camada 3.
- **API `api.mercadolibre.com` sempre 403 em IPs não-BR residenciais.** Use como último recurso ou desista dela quando a tarefa pede navegação real.
- **Snippet contaminado:** buscadores podem misturar no mesmo trecho preço do item, produto relacionado, modelo novo ou oferta antiga. Só associe preço quando SKU/título e preço estiverem inequivocamente ligados.
- **Preço antigo não é preço atual:** não usar blogs, Promobit/Pelando antigos ou memória da sessão como valor vigente.
- **Preços variam por vendedor:** catálogo reúne diversos vendedores. Reporte vendedor e preço à vista quando visíveis.
- **Frete e parcelas:** preço anunciado pode ser sem frete; parcela não é preço total. Use o valor à vista.
- **Mesmo modelo, mesma capacidade:** `240 GB`, `480 GB`, `500 GB` e `512 GB` são SKUs distintos; não somar/comparar como se fossem iguais.
- **Variações do mesmo SKU são anúncios diferentes:** `MLB26106184` (Prata canônico), `MLB2795973422`, `MLB1724144651` e similares são anúncios distintos do mesmo relógio Casio LA680WA-1DF Prata — não misturar.
- **Marketplace dentro de varejista:** Amazon/KaBuM podem mostrar terceiros. Identifique `vendido e entregue por` e não trate marketplace como venda direta da plataforma.
- **Anúncio inconsistente:** se título, URL e SKU divergirem (por exemplo, título 480 GB com código de 240 GB), descarte ou marque para verificação manual.
- **Sem preço verificável:** entregar link + `consultar preço`, não inventar faixa. Aceitar preço de agregador parceiro (Buscapé/Zoom) como fallback aceitável, rotulando a fonte.

## Cross-check multiloja
Para comparativos com Mercado Livre, Shopee, Amazon e KaBuM:
- Para **Amazon Brasil** especificamente, carregue também a skill irmã `amazon-price-search` — ela traz o passo-a-passo e os snippets DOM específicos da Amazon (ASIN, `#corePrice_feature_div`, `.a-price-whole`/`.a-price-fraction`, `#sellerProfileTriggerId`, `#deliveryMessageMirula`). Não reaproveite os snippets/seletores desta skill na Amazon; o DOM é completamente diferente.
- Para Mercado Livre, Shopee e KaBuM, carregue `browser-use` e abra cada loja no Chrome real. Pesquise o SKU, entre no anúncio e confirme variação/capacidade, preço à vista, vendedor, entrega, estoque e URL final.
- Mercado Livre/Shopee: não derive preço de snippet quando a página dinâmica estiver disponível; snippets servem só para localizar anúncios.
- Amazon/KaBuM: identifique explicitamente `vendido por` e `entregue por`; marketplace de terceiro não equivale à loja direta.
- Se surgir CAPTCHA, login, MFA, consentimento ou escolha ambígua de conta, pare e peça intervenção do usuário conforme a skill `browser-use`; não faça loop de tentativas.
- Só faça ranking/totais com valores confirmados na mesma data/hora e para o mesmo SKU.
- Não generalize que loja física ou plataforma é sempre mais barata; compare o mesmo SKU no momento da pesquisa.

## Referência de preços (ago/2026, ML Brasil)
- SSD Kingston A400 480GB (SA400S37/480G): ~**R$ 379–450** à vista (listagens variam R$ 379,60 até R$ 520).
- RAM DDR4 8GB SODIMM 2666: ~**R$ 130–190** (Crucial/Adata/Kingston no catálogo).
- Sempre confirmar via `web_search` no dia, pois preço de ML flutua.

## Referências
- `references/browser-use-real-marketplace-navigation.md` — instalação, permissão CDP e fluxo para confirmar preços navegando como usuário real no Chrome.
- `references/hardware-upgrade-price-validation.md` — checklist condensado para validar RAM/SSD e produzir comparativos multiloja sem misturar SKU, snippet ou marketplace.
- `references/mercadolivre-bot-detection-fallback.md` — sintomas das três camadas de defesa (verificação de conta, JS SHA256 PoW, `PolicyAgent` na API) e cadeia de fallback para Buscapé/Zoom quando o navegador headless é bloqueado.

## Fluxo resumido
1. Normalizar especificação + SKU
2. Tentar página individual no browser
3. Usar `web_search(site:...)` como fallback/pista
4. Confirmar preço, estoque, vendedor e SKU
5. Cross-check concorrentes
6. Entregar texto puro + links; marcar preços não confirmados
7. Salvar relatório Markdown quando solicitado
