# Extração de perfil de pessoa-chave no LinkedIn (Chrome clonado + CDP)

> Aplicável a perfis públicos logados. O browser do Hermes fica no login wall; o Chrome clonado (porta 9224 nesta máquina, sessão do Usuário logada) abre direto.

## Receita

1. Descobrir o handle por web_search primeiro (`<Empresa> CTPO "Chief Product" OR "Chief Technology" LinkedIn`) — confirme cargo E nome, não o primeiro hit genérico.
2. Abrir o perfil em nova aba sem desafio:
   `PUT http://127.0.0.1:9224/json/new?https://www.linkedin.com/in/<handle>/` (retorna `{"id": "<TAB>", ...}).
3. Extrair o texto da aba via CDP websocket `ws://127.0.0.1:9224/devtools/page/<TAB>`: `Page.navigate` se precisar recarregar, então scroll (2–3 × 1200px via `Runtime.evaluate` com `window.scrollBy`) e capturar `document.body.innerText`.
4. Procurar no texto capturado: cargo e empresa atual, data de entrada no cargo, e **`· 1º` ou `· 2º` + "conexões em comum"** — o grau de conexão e a empresa compartilhada (ex.: SulAmérica no mesmo período) são o dado mais valioso para a mensagem de aproximação.
5. Salvar o dump em `~/.hermes/cache/scratch/linkedin_<handle>.txt` e escrever o arquivo canônico na pasta da empresa com: trajetória, por que a pessoa importa para a vaga, e mensagens rascunho de WhatsApp (pedir contexto, nunca pedir favor/aceleração).
6. **Atividade completa (posts/artigos)**: navegar `https://www.linkedin.com/in/<handle>/recent-activity/all/` — o `main.innerText` do perfil base trunca em ~3 posts; a página de atividade dá ~30k chars cobrindo os próprios posts, reposts e posts compartilhados (que falam DELE). Scroll 4 × 3000px + 4s antes de extrair. Re-extrair também o perfil base para pegar o headline atualizado (ele atrasa quando há promoção, ex. "Diretor" → "CTPO").
7. **Destilar a leitura num MD de preparação**: quem é (1 min), os N pilares da visão pública (com citação curta de cada), o que está construindo agora (posts dos últimos dias = estado atual do produto), e "golpes prontos" — vocabulário para espelhar e como conectar o histórico do Usuário à tese da pessoa. Cuidado: usar as IDEIAS naturalmente, nunca citar que leu os posts.

## Regras

- O grau de conexão e o histórico em comum SAEM da extração CDP logada — não afirmar conexão sem ter visto na página.
- O `hero` do LinkedIn mostra o cargo da época do print; validar o cargo atual contra o texto da experiência completa (o perfil atualiza o hero às vezes com atraso).
- Emails citados no perfil só são usados se o Usuário já conhece a pessoa; prefira o canal que ele tem (WhatsApp) e nunca use o email sem avisar que viu no LinkedIn.