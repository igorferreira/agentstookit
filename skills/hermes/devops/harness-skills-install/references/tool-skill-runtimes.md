# Skills que embarcam runtime próprio (CLI + init + provedor)

Alguns skills não são só instruções: trazem um CLI npm que o agente instala e configura por workspace (ex.: OpenEdit/VEED `@veedstudio/openedit-cli`, Graphify `graphifyy`). Instalar o SKILL.md não é suficiente — a classe tem passos próprios.

## Procedimento

1. **Requisitos de sistema: confiar no SETUP/requirements do REPO, não nos docs de marketing do site.** Páginas de documentação podem estar desatualizadas (ex.: afirmar "só macOS" quando o SETUP.md do repo lista macOS/Linux/Windows) — ler `SETUP.md`/`README.md` do checkout antes de concluir incompatibilidade com Linux.
2. **Instalar o skill globalmente** (`npx skills add <org>/<repo> -g` ou caminho do repo) e preparar prerequisites (node/ffmpeg/git) — checar versões com `command -v` + `--version`.
3. **Init do workspace**: rodar primeiro `init --dry` para LER o plano de ações antes de aplicar; depois `init` sem flag (modo safe nunca instala nada machine-global sem aprovação). O init cria `package.json` com o CLI pinado, hooks de sessão para os agentes e define `OPEN_EDIT_ROOT`-equivalente.
4. **Registrar escolhas de provedor via COMANDO do CLI** (`<cli> transcribe --record ...`), nunca editando o JSON de prefs à mão.
5. **Smoke test de ponta a ponta antes de prometer funcionamento**:
   - Render: HTML mínimo com elemento `#stage` animado → `<cli> render page.html --out runs/teste.mp4 --frames 90` → validar com `ffprobe` (codec, fps, duração exata).
   - Transcrição: gerar fala sintética em pt-BR (`espeak-ng -v pt-br -w /tmp/x.wav "..."`) + envelope em vídeo (`ffmpeg -f lavfi -i color... -i x.wav -shortest`), rodar o comando do skill e conferir o JSON de timings por palavra.

## Pitfalls

- **Para conteúdo em pt-BR, escolher tier de modelo MULTILINGUE** — tiers marcados `.en` (ex.: `small.en`, `medium.en` no Whisper) são mono-idioma inglês e produzem lixo em português; o tier "rápido" oferecido pelo skill costuma ser o `.en`. Gravar `medium` (multilíngue) como padrão e informar que dá para trocar.
- **Primeira execução de modelo local baixa GBs** (WhisperX medium ≈ 1,5 GB) — rodar o smoke test de transcrição em background com notificação e avisar o usuário do download, não tratar demora como falha.
- **Renderer headless no Ubuntu moderno pode reclamar de sandbox AppArmor** (unprivileged user namespaces) — o CLI normalmente cai para `--no-sandbox` sozinho; reportar o aviso ao usuário em vez de mexer em sysctl sem pedir.
- **Transcrição local vs SaaS**: oferecer as duas rotas (local grátis/offline vs conta SaaS com cota gratuita) e gravar a escolha; a escolha fica em `.open-edit-prefs.json`-equivalente no root do workspace.
