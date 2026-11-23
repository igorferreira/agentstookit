# Navegação real em marketplaces com `browser-use`

Use esta referência quando Mercado Livre, Shopee, Amazon ou KaBuM dependerem de JavaScript, cookies, CEP, sessão autenticada ou proteção antibot.

## Objetivo

Confirmar na página real — não em snippets — o SKU, a variação, o preço à vista, o vendedor, o estoque, a entrega/frete e a URL final.

## Instalação oficial isolada

```bash
uv tool install --python 3.12 --upgrade --force \
  'browser-use @ git+https://github.com/browser-use/browser-use.git'
```

Depois registre/carregue a skill oficial `browser-use` no ambiente do agente. Não copie uma versão antiga do pacote global para dentro do projeto.

## Diagnóstico

```bash
browser-use --version
browser-use --doctor
```

Se o Chrome abrir `chrome://inspect/#remote-debugging`, o usuário precisa marcar **Allow remote debugging for this browser instance** e clicar **Allow**. A conexão seguinte pode gerar mais um popup por conexão; isso é esperado. Não repetir tentativas em loop antes da confirmação do usuário.

## Teste mínimo

```bash
browser-use <<'PY'
print(page_info())
PY
```

Primeira navegação:

```bash
browser-use <<'PY'
new_tab('https://lista.mercadolivre.com.br/')
wait_for_load()
print(page_info())
PY
```

## Fluxo de pesquisa

1. Abra a listagem com `new_tab(url)` e espere `wait_for_load()`.
2. Use a árvore de acessibilidade/CDP para localizar busca, filtros e anúncios; clique como usuário.
3. Entre no anúncio e selecione explicitamente a capacidade/variação correta.
4. Extraia e valide em conjunto:
   - título e SKU;
   - capacidade/frequência/formato;
   - preço à vista;
   - vendedor e `vendido/entregue por`;
   - condição, estoque, frete/entrega e URL.
5. Repita na outra loja para o mesmo SKU.
6. Registre data/hora. Calcule totais apenas com valores confirmados.
7. Se login, senha, MFA, CAPTCHA, consentimento ou conta ambígua forem necessários, pare e peça intervenção ao usuário.

## Pitfalls duráveis

- Snippet de buscador pode misturar oferta antiga, produto relacionado ou outro SKU.
- URL/título/código divergentes invalidam a oferta até revisão manual.
- Catálogo e anúncio podem mostrar vendedores diferentes; capture o vendedor realmente selecionado.
- A capacidade escolhida na página pode alterar o preço sem alterar claramente o título.
- Não chamar scraping/API de "navegação real". Se o usuário pediu navegação real, use Chrome/CDP.
- Não afirmar que uma plataforma é sempre mais barata; compare o mesmo SKU na mesma janela de tempo.
- **Marketplaces grandes (Mercado Livre em particular) podem bloquear headless em três camadas mesmo com browser real via CDP.** Quando aparecer `Hubo un error accediendo a esta pagina...` (header em espanhol indica redirect argentino), redirect para `gz/account-verification`, ou challenge JS de SHA256 PoW (cookie `_bmstate` + `_bmc`), **não fazer loop** — consultar `references/mercadolivre-bot-detection-fallback.md` para a cadeia de fallback Buscapé/Zoom/Renner/CEA antes de tentar de novo.

## Quando desistir e usar agregador

Sinais de que o browser será bloqueado de novo:

- `navigator.userAgent` contém `HeadlessChrome` (não foi possível spoofar).
- O redirect inicial leva para `mercadolibre.com/` (versão argentina) e não `.com.br/`.
- O conteúdo retornado é sempre a mesma página de erro mesmo após refresh.

Nesses casos, **não gastar mais tentativas**. Aceitar preço do Buscapé/Zoom como fonte secundária, rotulando claramente.

## Fonte

- Skill oficial: https://github.com/browser-use/browser-use/blob/main/skills/browser-use/SKILL.md
- Instalação/diagnóstico: https://github.com/browser-use/browser-harness/blob/main/install.md