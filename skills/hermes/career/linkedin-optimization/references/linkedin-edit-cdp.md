# Editar o LinkedIn do Igor via Chrome CDP

O Chrome isolado do Hermes é barrado por Cloudflare na tela de login do LinkedIn (challenge sem checkbox, fingerprint de headless). O perfil Default do Igor não aceita `--remote-debugging-port` (Chrome 136+ bloqueia; /json responde 404). Método que funciona:

1. **Clonar sessão:** `mkdir ~/opt/linkedin-cdp-profile/Default` + copiar `~/.config/google-chrome/Default/Cookies` e `~/.config/google-chrome/Local State`. Com `li_at` no cookie, a sessão já vem logada.
2. **Subir Chrome:** `DISPLAY=:0 google-chrome --user-data-dir=/home/igorferreira/opt/linkedin-cdp-profile --remote-debugging-port=9224 --no-first-run --no-default-browser-check "<url>"` (background do terminal; health check `curl http://127.0.0.1:9224/json/version`).
3. **Driver:** `~/opt/linkedin_cdp.py` (ações: info/eval/nav/click/type/clicaxy/shot; aba alvo = 1ª page com linkedin.com). O Chrome fica visível na tela do Igor (headed).
4. **URLs-chave:** lista de experiências = `/in/igorferreira/details/experience/`; editar cargo = `/in/igorferreira/details/experience/edit/forms/<id>/`; criar = `/in/igorferreira/edit/forms/position/new/` (o botão "Adicionar cargo" abre modal vazio via CDP — usar a URL direta).
5. **GOTCHAS críticos:**
   - Cliques sintéticos (`dispatchEvent`) NÃO disparam React do LinkedIn — sempre `Input.dispatchMouseEvent` real (driver: ação `clicaxy`). Exceção: campos `input[type=text]` e `<select>` ACEITAM `Object.getOwnPropertyDescriptor(...).set` + `dispatchEvent('input'/'change')` — o que exige mouse real é toggle/switch, opção de typeahead e botão.
   - O localizador de aba do driver filtra por "linkedin.com" na URL — se a aba navegou para outro alvo (ex.: `file://`), ele devolve None; fazer fallback para a 1ª aba `type=page`.
   - Dois switches no formulário: o de CIMA é "Notificar a rede" (deixar OFF!); "Trabalho aqui atualmente" fica mais abaixo (só aparece após scroll).
   - Nos selects, mês é 1-based (1=Janeiro, 11=Novembro, 12=Dezembro) — conferir valor gravado após salvar; a primeira gravação registrou nov/2025 em vez de dez/2025 e precisou de re-edit.
   - Campos typeahead (Empresa): digitar com `Input.insertText`, esperar ~2,5s, ler `ul[role=listbox] li[role=option]` e clicar na opção com mouse real.
   - Descrição = `[contenteditable=true]` (placeholder "Destaques, máximo de 2.000 caracteres"): limpar innerHTML, focar, `Input.insertText`, conferir `innerText.length` após.
   - Salvar = botão texto exato "Salvar" com scrollIntoView + mouse real; sucesso = toast "O item foi salvo." e redirect.
   - Captura de tela exige `Page.enable` antes de `Page.captureScreenshot`.
6. **Verificação:** recarregar `/details/experience/` e conferir agrupamento (LinkedIn agrupa posições da mesma empresa), datas e descrição.
