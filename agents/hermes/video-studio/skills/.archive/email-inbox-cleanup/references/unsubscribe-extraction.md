# Extrair links de descadastro de newsletters (03/09/2026 — workflow validado)

## Contexto
Ao "descadastrar antes de apagar", a maioria dos emailers NÃO expõe header `List-Unsubscribe`.
O link de descadastro fica no **CORPO** (rodapé/assinatura). Método de extração validado num
purge real de 62 e-mails divisórios.

## Passo 1 — Extrair o corpo (com os links)
```bash
himalaya message read --folder INBOX <id>    # imprime o corpo na stdout (com os links)
```
- **NÃO usar `himalaya message view`** → subcomando inexistente: `unrecognized subcommand 'view'`.
- **NÃO usar `himalaya message export` para ler** → salva o arquivo num diretório, não imprime
  o corpo na stdout (só diz "Message ... exported in /tmp!"); inviável para parsing em loop.
- Regex comprovado (PT-BR):
  ```
  (?i)(cancelar\s*assinatura|unsubscribe|descadastr|gerenciar\s*prefer[eê]ncias)\s*\(([^)]+)\)
  ```
  → captura `Cancelar assinatura (URL)`. Fallback: URLs com `unsub|preferences`.

## Passo 2 — Agrupar por serviço (mesmo link repete em N e-mails)
Um remetente manda muitos e-mails colando o MESMO link de descadastro. Agrupar por destino
evita cliques repetidos. Padrões por ferramenta de emailing (vistos em uso):
- **HubSpot**: `hs-*.hubspotemail.net/hs/preferences-center/...` (Alura, Casa do Código)
- **ActiveCampaign**: `*.activehosted.com/proc.php...` (DevMedia, Me Poupe, Liberta)
- **ConvertKit**: `*.unsubscribe.kit-mailN.com` (Filipe Deschamps, Oregonead)
- **List-Manage / Mailchimp**: `*.list-manage.com/unsubscribe` (BrazilJournal)
- **Oktoplus**: `mkt.oktoplus.com.br/asm/unsubscribe`
- **LinkedIn**: `/job-alert-email-unsubscribe?savedSearchId=...` e `/mypreferences`
- **Mercado Livre**: `myaccount.mercadolivre.com.br/communication-preferences`

## Passo 3 — Classificar o tipo de descadastro
1. **1-clique (basta abrir a URL)** — HubSpot `.../direct`, ConvertKit `.unsubscribe.*`,
   list-manage, activehosted `proc.php`, Glassdoor, Spotify (`/account/unsubscribe`),
   Suno (`click.mkt.suno.com.br/unsub_center.aspx`), Goodreads.
   Abrir com browser-use e confirmar sucesso (título/página de confirmação).
2. **Login / preferências (exige conta logada)** — LinkedIn, Mercado Livre,
   Facebook/Instagram/Meta (`facebook.com/aymt/instagram/unsubscribed`). Abrir a página e o
   usuário clica no navegador já logado.
3. **Sem link direto (só site com login)** — Substack, Diário do Rio, Netflix, promo Spotify.
   Não há atalho; comunicar ao usuário que exige acesso manual.

## Guardrails
- Confirmar ANTES que o e-mail é realmente promocional (não um alerta de segurança disfarçado).
  Ex visto: OpenAI "New sign-in" caiu na lista de promo e foi um ALERTA DE SEGURANÇA — reverter.
  Mesmo risco: "Novo login no Instagram", "Amazon security code", recibos de pagamento.
- Buscar o e-mail "crítico a preservar" (ex: E-CPF/contrato) em TODO o Gmail (paginando
  "Todos os e-mails") ANTES de apagar, pois ele pode não estar na INBOX.