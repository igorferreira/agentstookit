---
name: catalogo-compras
description: "Registrar roupas/perfumes do Igor com fotos e busca preço."
---

# Catálogo de Compras Pessoais — roupas, perfumes, produtos

## Quando usar
Igor manda fotos (provador + etiqueta) de roupa/perfume/produto, ou diz "pesquisa o melhor preço", "salva essa peça", ou fala de comprar algo que ele está avaliando em loja física.

## Fluxo obrigatório (6 etapas, sem pedir passo a passo)
1. **Contextualizar**: usar a data/hora do bloco [Agora] (data/hora da tiragem) e clima se relevante.
2. **Salvar fotos** em `~/MEGA/Documentos/pessoal_saude/<categoria>/` — `fotos/` (vestindo) e `etiquetas/` (código/preço). Nome: `AAAA-MM-DD_<MARCA-MODELO>-<DETALHE>.jpg`.
3. **Criar ficha .md** (uma por peça, data da FOTO no nome): tabela de dados da etiqueta (marca, modelo, código, cor, tamanho, EAN), tabela de compra (onde, preço, data, status), seção "Como ficou no corpo" com fotos embutidas, seção "Pesquisa de preço na internet".
4. **Pesquisar melhor preço online** (web_search): site oficial da marca primeiro, depois marketplaces (Netshoes, Dafiti, Centauro, Shopee, Amazon, Mercado Livre). Comparar com preço da loja física.
5. **⭐ REGRA DO IGOR (06/09/2026): o resultado da pesquisa de preço SEMPRE fica salvo DENTRO da ficha .md da peça** (tabela loja/preço + veredito) — nunca só no chat. Confirmado por ele: "sempre salva o resultado dessas pesquisas".
6. **Atualizar INDEX.md** da pasta (tabela geral: data, peça, marca/modelo, tamanho, onde, preço, status).

## Convenções
- Status: 🟡 avaliando / ✅ aprovou-comprou / ❌ descartou.
- Tamanhos do Igor (acumular a cada peça): camiseta P (Adidas slim), M (Olympikus/Mizuno reto), bermuda P, calça 38 na TACO, regata M.
- Uma peça = um .md; INDEX.md é o índice vivo.
- Perfumes: painel em `~/MEGA/Documentos/pessoal_saude/perfumes/` (agente Maurício); roupas em `pessoal_saude/roupas/` (agente Kléber).
- Fotos de corpo inteiro também servem de registro de evolução física.

## ⚠️ Pitfall: nomes ditados por voz
Igor dita nomes de lojas/marcas por áudio → transcrição erra nomes. Validado 06/09/2026: "Chopí" = **Shopee**, "Iuguente" = **YOUCAN** (loja física no ParkShopping Jacarepaguá), "Jojoquim" = Joaquim. Corrigir com `sed -i` no SOUL.md do agente + atualizar memória. Ao registrar nome novo de loja dito por voz, confirmar grafia quando houver dúvida.

## Agentes associados
- **Kléber** (`estiloso`) — moda/roupas, bibl. Reserva/TACO/Centauro/Shopee/Shein/YOUCAN.
- **Maurício** (`perfumaria`) — perfumes, WePink/Boticário/Natura, Luis Jordão/Fragrantica, vs original vs contratipo.
- **Dr. Promo** (`promo`) — comparação de preço multi-loja.

Ver detalhes do processo de roupas: `~/MEGA/Documentos/pessoal_saude/roupas/PROCESSO-REGISTRO-ROUPAS.md`.
