# Extração do Glassdoor logado via Chrome clonado (CDP)

O browser do Hermes fica preso no Turnstile do Cloudflare na Glassdoor — não gaste tempo nele. O caminho validado é o Chrome clonado do Igor (perfil copiado, CDP exposto).

## Pré-requisitos

- Chrome clonado rodando em `127.0.0.1:9224` (perfil do Igor com sessão Google). Se não estiver: copiar Cookies + Local State de `~/.config/google-chrome/Default` para um perfil clone e subir `google-chrome --user-data-dir=<clone> --remote-debugging-port=9224` (Chrome moderno RECUSA `--remote-debugging-port` no user-data-dir padrão).
- `import websockets` disponível no python do Hermes.

## Passos

1. **Listar alvos**: `curl -s http://127.0.0.1:9224/json` — pegar `webSocketDebuggerUrl` (`ws://127.0.0.1:9224/devtools/page/<id>`).
2. **Abrir a URL do Glassdoor em nova aba**: `curl -s -X PUT "http://127.0.0.1:9224/json/new?<url>"` (PUT, não GET).
3. **Driver CDP mínimo em websocket** (asyncio + websockets): enviar `{id, method, params}` e consumir eventos até chegar a resposta do mesmo id. Métodos usados: `Page.navigate`, `Runtime.evaluate` (`returnByValue: true`), `Page.captureScreenshot`, `window.scrollBy` para lazy-load, clique por seletor (`el.click()` em `<a|button>` cujo innerText casa com "Entrar com Google"/"Mostrar mais").
4. **Login (se "Entrar" apareceu)**: clicar "Entrar com Google"; abrirá aba do Google pedindo verificação em duas etapas (notificação no celular do Igor). AVISAR o Igor e aguardar; a aba do Google some quando aprovado; confirmar login (nome do usuário no topo) antes de extrair.
5. **Extração**: `document.querySelector('main') || document.body` → `innerText`. Nas páginas logadas a sidebar "Empresas seguidas" polui — fatie a partir do título da seção (ex.: `t.indexOf('Avaliações da empresa')`). Clique em "Mostrar mais" para expandir textos longos antes de extrair.

## URLs padrão (substituir E<IID> pelo company id)

- Avaliações: `/Avaliações/<Empresa>-Avaliações-E<IID>.htm` (PT: encode `%C3%A7%C3%B5es`)
- Sobre: `/Sobre/Trabalhar-na-<Empresa>-EI_IE<IID>.11,17.htm` (ou Visão-geral/Trabalhar-na)
- Salários: `/Salário/<Empresa>-Salários-E<IID>.htm`; por cargo: `/Salário/<Empresa>-<Cargo>-Salários-E<IID>_D_KO7,27.htm` (pegar o link exato nas âncoras da página)
- Benefícios: `/Benefícios/<Empresa>-Brasil-Benefícios-EI_IE<IID>..._IN36.htm`
- Entrevistas: `/Entrevista/<Empresa>-Perguntas-entrevista-E<IID>.htm`
- Vagas: `/Vagas/<Empresa>-Vagas-E<IID>.htm`
- LinkedIn (mesma sessão clonada): navegar `https://www.linkedin.com/in/<handle>/` — navegação direta por CDP funciona; `/json/new?url=` às vezes cai no feed, então usar `Page.navigate` na aba.

**Os sufixos numéricos (`.11,17`, `_D_KO9,29`, `.0,8_IL.9,15_IN36`) são posições de caractere do nome da empresa no slug — NÃO são constantes por empresa e NÃO adivinhe**; chutar dá 404 (página "procuramos pela galáxia"). Pegue a URL exata (a) dos links `<a href>` na página de salários/avaliações via `Runtime.evaluate`, ou (b) buscando no Google `glassdoor.com.br Benefícios <Empresa> E<id>` (o snippet do Google costuma trazer a URL exata E os resumos do empregador das subpáginas BNFT).

## Protocolo CDP — gotchas que custam tempo

- **Respostas CDP têm `id`, não `method`** — casar resposta por nome de método trava no recv (só eventos carregam `method`); mantenha contador de `id` e consuma até o `id` enviado.
- **`Runtime.evaluate` com await**: a expressão precisa de IIFE async `(async()=>{ ... })()` com `awaitPromise: true` — top-level await dá SyntaxError. E a IIFE precisa de `return` explícito: sem `return` o resultado volta `undefined` silenciosamente (sem exceptionDetails), o que parece "página vazia".
- **Rode o CDP inline no execute_code (asyncio.run), não num driver subprocessado** — um driver em subprocess pode devolver só a 1ª resposta (navegação) e sair 0.4s depois, parecendo falha da página.
- **Kernel Python 3.14 não tem event loop ambiente** — use `asyncio.run(main())`, não `loop.run_until_complete` direto.
- **Páginas pesadas do Glassdoor demoram 11–14s para renderizar** — espere esse tempo (setTimeout dentro da IIFE) antes do innerText; espere MENOS e você extrai 0 chars sem erro.
- Reutilize o driver pronto da skill: `scripts/cdp_extractor.py` (funções `navigate`, `eval_js`, `tab_by_url`, `main_text`, `scroll`, `new_tab`). Cópias salvas em `~/.hermes/cache/scratch/` MORREM (pruning de scratch) — quando a cópia sumir, importe do diretório da skill, não reescreva o protocolo por página.
- **websockets ≥ 14**: `websockets.connect(url, open_timeout=T, max_size=50MB)` — o argumento é `open_timeout`; passar `timeout=` dá `TypeError: create_connection() got an unexpected keyword argument 'timeout'`.
- **Kernel do execute_code cacheia módulos importados**: depois de PATCH num módulo de driver, `del sys.modules["nome"]` antes de importar de novo — senão roda a versão velha e você depura um bug que não existe.
- `Runtime.evaluate` com `return` top-level dá `SyntaxError: Illegal return statement` — envolva em IIFE `(() => { ... })()` (sync) ou `(async () => { ... })()` com `awaitPromise: true`.

## O que esperar por página (não insistir além disso)

- Avaliações: ~5 avaliações completas (relevância) + FAQ agregada (nota geral, % recomendam, tendência 6 meses, notas por categoria). Paginação `_P2.htm` tende a re-render a página 1 — ignore.
- Salários: faixa/média/variável + N salários individuais (data, experiência, local, base+variável) + FAQ com percentis.
- Benefícios: nota geral, lista de categorias, benefícios mais populares com citações, ~10 avaliações individuais recentes. **MAS: em empresas com pouca contribuição a página pode vir quase vazia (só categorias sem nota)** — nesse caso o valor real dos benefícios mora em três lugares: os posts oficiais "Atualizações da empresa" na página Visão-geral (ex.: anúncio oficial de VR por dia útil), os snippets do Google das subpáginas `BNFT<id>_E<IID>_N<cat>.htm` (resumo do empregador) e, principalmente, **os anúncios oficiais de vaga da própria empresa (Gupy/site de carreiras) — a única fonte que dá R$ exato de VA/VR/auxílios; a página de benefícios do Glassdoor quase nunca publica valor**. Não gastar 30 min clicando na página vazia.
- Entrevistas: estatística (origem, dificuldade, % positiva) + 5 relatos completos.

## Aplicação da regra de segurança

- Nunca registrar cookies/tokens da sessão; a sessão mora no perfil clonado.
- Fluxo OAuth do Google só com o Igor aprovando a verificação em duas etapas; se aparecer campo de senha, PARAR e pedir a ele.
