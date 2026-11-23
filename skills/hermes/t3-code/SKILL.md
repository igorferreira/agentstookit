---
name: t3-code
description: "Use quando Usuário pedir projeto ou thread no T3 Code."
version: 2.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [t3code, ferramentas]
---

# T3 Code — operação (CLI, desktop, Android)

## When to Use

Quando Usuário pedir para criar/abrir projeto ou thread no T3 Code, conectar o celular ao PC via T3, ou depurar por que algo "não aparece no app".

## O que é (docs oficiais)

T3 Code (github.com/pingdotgg/t3code, t3.codes, MIT, by Theo/Ping) é um **"agent harness control surface"**: plano de controle open-source para orquestrar agentes de código JÁ instalados e autenticados na máquina (Claude Code, Codex, Cursor, Grok Build, OpenCode, Pi, Muse Code, Kiro, fx, Antigravity e agentes ACP). Não é modelo nem agente. Servidor WebSocket roda na máquina e expõe 3 clientes: desktop (Electron), web (app.t3.codes ou web local) e mobile (iOS/Android). Custo zero — usa as assinaturas existentes. Arquitetura: cliente → acesso (ws direto, relay T3 Connect, Tailscale Serve, SSH gerenciado pelo desktop) → UM servidor T3 que detém identity, providers, projects/threads, terminais, git e filesystem. O runtime nunca é dividido; remoto é só camada de conexão.

## Comandos que funcionam

- CLI: `~/.local/bin/t3` (v0.1.10 desde 23/11/2026; confirmar com `t3 --version`). Subcomandos: serve, app, pair, auth, environment, browser, project, thread.
- **Criar projeto:** `t3 project add <caminho-absoluto> --title "Nome"` — imprime o project_id (UUID). Não existe `t3 project list` (só add/remove/rename); listar via sqlite: `sqlite3 ~/.t3/userdata/statev2.sqlite "SELECT project_id,title FROM projection_projects WHERE deleted_at IS NULL"`.
- **Abrir projeto no desktop:** `t3 app <caminho>` — exige o app desktop RODANDO (servidor t3 ativo não basta; sem o desktop dá DesktopAppUnreachableError).
- **Criar thread:** `t3 thread start <project_id|caminho> <mensagem> --title "..."` — sem modelo padrão no projeto, o start falha com "project has no default model"; passar SEMPRE `--provider codex --model <slug>` JUNTOS (o CLI exige os dois; slug vigente no `~/.codex/config.toml`). Conferir criação em `orchestration_v2_projection_threads` (thread_id pode vir com prefixo `mcp:`).
- **Acesso remoto/pairing:** `t3 pair` gera token/QR que EXPIRA em ~5 min e é loopback-only; `t3 up --lan` falha com ServerAlreadyRunningError se o desktop está de pé (lock em ~/.t3/userdata/server-owner.sqlite).

## App Android mostra THREADS, não projetos

A aba Chats do celular lista threads; um projeto recém-criado (sem thread) não aparece. Ao criar um projeto pro Usuário, abrir logo uma thread nele (comando acima) — é o que faz o projeto "aparecer" no celular.

## Pitfalls

- Projeção tem atraso: a thread pode existir em `orchestration_v2_projection_threads` e ainda não estar em `projection_threads` (o que o app lista). Verificar os dois bancos antes de concluir que falhou; pedir pull-to-refresh no app.
- Diagnóstico de execução de thread: `~/.t3/userdata/logs/provider/events.<thread>.log` mostra o protocolo do provider (turns, turn/completed, tokens). Sem eventos lá = o turno não rodou.
- Estado em sqlite: `~/.t3/userdata/statev2.sqlite` (projetos, threads, provider sessions). Ler apenas — escrever direto no banco de um servidor vivo é arriscado.

## Referência CLI completa (v0.1.10, verificada localmente)

```
t3                          # sobe servidor + abre navegador (web local)
t3 serve                    # sobe servidor sem navegador
  --host <ip>               # bind customizado (ex: $(tailscale ip -4))
  --lan                     # aceita LAN + tailnet (pairing code é a única trava)
  --tailscale-serve         # expõe HTTPS no tailnet (porta 443 default)
  --base-dir <path>         # data dir alternativo (equivale a T3CODE_HOME)
t3 up                       # setup de acesso por outros dispositivos
t3 status                   # serviço, T3 Connect, rede local
t3 update [<versão>] [--channel stable|nightly] [--allow-downgrade] [--yes]
t3 service install|status|restart|uninstall
t3 project add|remove|rename                 # NÃO existe list
  list via sqlite: SELECT project_id,title FROM projection_projects WHERE deleted_at IS NULL
t3 thread list|start|send|show
t3 auth pairing|session|connect-device        # credenciais, sessões, dispositivos
t3 environment link|list|unlink              # ligar outros ambientes T3 (agentes cruzam máquinas)
t3 browser setup            # prepara host Linux p/ browser headless do T3
```

Instalação em outra máquina: `curl -fsSL https://t3.codes/install.sh | sh` (vai para `~/.local/bin/t3`; Windows `irm https://t3.codes/install.ps1 | iex`; trial: `npx t3@latest`). Desktop: brew cask `t3-code` / winget `T3Tools.T3Code` / `.deb` GitHub Releases / AUR `t3code-bin`.

## Serviço de fundo (docs oficiais)

- Linux: systemd user service + linger (sobrevive boot/logout). macOS: launchd (exige usuário logado + Mac acordado). Windows: não suportado.
- `t3 update` repointa o serviço e PERGUNTA antes de reiniciar (reinício interrompe turns de agente, terminais e clientes remotos); `--yes` para script. Recusando, fica `restart-pending` até `t3 service restart`.
- `t3 uninstall` remove launcher + versões baixadas, preservando projetos/threads/settings em `~/.t3/userdata`.
- Versões ficam em `<baseDir>/runtime/versions/<versão>`; update tira snapshot do SQLite (runtime/db-backup/) e faz rollback se a trial não reportar `prepared` em 120s.
- Linger só via `loginctl enable-linger` (com admin) — nunca pelo próprio T3. `t3 service status` reporta estados tipo `linger-disabled`/`service-stopped` com orientação.
- Serviço e T3 Connect são independentes: sair do Connect não desinsta o serviço.

## Migração V1 → V2 e gotchas das docs (internet)

- V1 (0.0.x) → V2 (v0.1.0+): migrar TODOS os apps/servidores juntos (V1 e V2 se recusam mutuamente). Threads migradas copiam títulos/projetos/mensagens, mas PERDEM sessão viva do provider, checkpoints/diffs e histórico de aprovações — restate contexto importante no 1º turno novo.
- Sem export de thread inteira: recovery = copiar `~/.t3/userdata` e ler com `sqlite3 -readonly` (tabelas `projection_threads`, `projection_thread_messages`). NUNCA apontar um servidor para a cópia.
- Provider CLI precisa estar autenticado NA MÁQUINA DO SERVIDOR (não no dispositivo que navega). Provider sem auth falha só no início da sessão.
- Version manager que só inicializa em shell interativo esconde binários do shell não-interativo que o T3 usa → "not found" mesmo instalado. Testar: `ssh user@host 'sh -lc "command -v claude codex"'`.
- `npx t3@latest` é trial de um-off; `t3 update`, `t3 uninstall` e serviço exigem o `t3` instalado.
- app.t3.codes (HTTPS) não conecta a backend LAN em http:// (mixed-content do navegador) — usar pair direto, Tailscale HTTPS ou túnel.
- Copiar pairing link do desktop só enquanto a página Connections segue aberta; após navegar/recarregar, emitir novo link.
- Intel Mac não tem binário `t3` (build do source com Node 24).
- Pairing token = tratar como senha: quem tiver token cria sessão até expirar/revogar (via `t3 auth`).

## Fontes (pesquisa internet, 23/11/2026)

- Wiki LLM oficial (raw md por página): agentwikis.com/raw/t3code/wiki/<page>.md — índice em /wiki/t3code/wiki/index.md (concepts: overview, install, providers, permission-modes, remote-access, t3-connect, background-service, architecture, troubleshooting, glossary; cobertura oficial até v0.1.8 de 09/11/2026).
- Sites: t3.codes (produto/docs) e t3code.org (guia/FAQ); GitHub pingdotgg/t3code; web app app.t3.codes; cópia bruta da wiki salva em ~/.hermes/cache/scratch/t3code_wiki/ (expira 24h).
- Para feature nova, re-checar github.com/pingdotgg/t3code/releases antes de afirmar.
