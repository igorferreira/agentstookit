---
name: corporate-agent-demo-setup
description: "Install, configure and validate OpenClaw + Ollama (and similar agentic CLIs) on a Windows corporate machine for HDI Seguros demos. Covers npm allow-scripts pitfalls on Windows, PowerShell admin sequence, removing bloat cleanly, fallback paths, and the standardized report folder. Load when Igor mentions installing/reinstalling OpenClaw, Ollama, Node.js agents, or setting up the HDI corporate demo on a new/clean machine."
tags: ["hdi", "openclaw", "ollama", "nodejs", "npm", "windows", "powershell", "corporate-demo"]
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [hdi, openclaw, ollama, nodejs, npm, windows, powershell, corporate-demo]
    related_skills: [hermes-agent]
---

# Corporate Agent Demo Setup (Windows / HDI)

Standardized playbook for setting up OpenClaw, Ollama and similar agentic CLIs on **Igor's HDI corporate Windows machine** (`C:\Users\igorfe>`, PowerShell) so demos run offline, locally and reproducibly.

The original target version recorded is **OpenClaw 2026.6.34 (5c38f99)** installed globally with `npm`.

## When to use

Trigger this skill when Igor (or anyone acting as Igor) asks to:

- Install, reinstall, or "limpar e instalar de novo" OpenClaw.
- Set up Ollama for the local LLM demo that pairs with OpenClaw.
- Document the corporate demo environment so it can be replicated on another laptop.
- Recover from a broken OpenClaw install (binário bloqueado, scripts nativos não rodam, permissões).
- Add a new agent CLI to the same machine and wants the same clean-install pattern.

## Where to save evidence

All reports, install logs, screenshots and recaps live under the HDI corporate IA folder, NOT under Igor's personal Comprovantes tree:

```
~/MEGA/Documentos/trabalho_projetos_ti/ia_corporativa/
└── <agent-name>/                         ← one folder per agent (openclaw/, ollama/, …)
    ├── AAAA-MM-DD_INSTALACAO-<AGENT>-POWERSHELL.md
    ├── AAAA-MM-DD_REINSTALACAO-<AGENT>-POWERSHELL.md   ← playbook version
    ├── AAAA-MM-DD_<AGENT>-<VERSAO>-<ESTADO>.txt        ← raw install log
    └── …
```

Naming pattern (Portuguese, snake-case):
`AAAA-MM-DD_TIPO-EMISSOR-DETALHE-RVALOR.ext`

## Standard install procedure (PowerShell **as Administrator**)

### 1. Confirmar versão antes de mexer

```powershell
PS C:\Users\igorfe> openclaw --version
OpenClaw 2026.6.34 (5c38f99)
```

If the command is broken, skip straight to uninstall.

### 2. Uninstall limpo

```powershell
npm uninstall -g openclaw
npm prune -g
npm cache clean --force
Remove-Item -Recurse -Force "$env:USERPROFILE\.openclaw"      -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "$env:APPDATA\openclaw"           -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "$env:LOCALAPPDATA\openclaw"      -ErrorAction SilentlyContinue
```

Confirm both `npm ls -g openclaw` and `where.exe openclaw` return nothing.

### 3. Liberar `allow-scripts` — UM PACOTE POR VEZ (pitfall crítico)

⚠️ **PITFALL — ocorreu em 12/08/2026 e 13/08/2026:** Both `--allow-scripts=lista` (CLI flag) and `npm config set allow-scripts=lista` (config) silently fail. npm joins the names with a space and the parser rejects them as `ignoring unparseable entry "<name> <name> <name>"`. The .npmrc ends up with a literal string instead of a valid config — the warnings look like noise but the scripts never run.

The only working syntax is **`pacote:script=true`**, one npm config command per package:

```powershell
# 1. Clear anything left over from broken attempts
npm config delete allow-scripts -L user

# 2. Enable allow-scripts globally (catches openclaw's own scripts)
npm config set -L user allow-scripts=true

# 3. Enable the specific scripts of the 3 known-transitive deps
npm config set -L user @google/genai:preinstall=true
npm config set -L user protobufjs:postinstall=true
npm config set -L user tree-sitter-bash:install=true

# 4. Verify .npmrc — should be exactly 4 lines, no giant string
Get-Content "$env:USERPROFILE\.npmrc"
```

Expected output:
```
allow-scripts=true
@google/genai:preinstall=true
protobufjs:postinstall=true
tree-sitter-bash:install=true
```

If `allow-scripts=openclaw @google/genai protobufjs tree-sitter-bash` appears, delete it and rerun the four `npm config set -L user` commands above. **Do NOT use `npm config set allow-scripts=lista`** — it always parses to a single garbage string.

### 4. Install

```powershell
npm install -g openclaw
```

The output should NOT include `npm warn install-scripts ... 4 packages have install scripts not yet covered by allowScripts:` anymore. If it does, the .npmrc is wrong — go back to step 3.

### 5. Verify

```powershell
openclaw --version
# OpenClaw 2026.6.34 (5c38f99)

npm ls -g openclaw
# C:\Users\igorfe\AppData\Roaming\npm
# └── openclaw@2026.6.34
```

## Fallbacks (Windows-only quirks)

### SmartScreen / ExecutionPolicy blocks the new binary

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
icacls "$env:APPDATA\npm" /grant "$env:USERNAME:(OI)(CI)F" /T
Unblock-File -Path (Get-Command openclaw).Source
```

In corporate environments, validate these with Security/SRE first — especially `tree-sitter-bash`, which compiles a native binary via `node-gyp`.

### Roll back everything

```powershell
npm uninstall -g openclaw
npm config delete allow-scripts -L user
npm config delete @google/genai:preinstall -L user
npm config delete protobufjs:postinstall -L user
npm config delete tree-sitter-bash:install -L user
```

## Pitfalls

- **`npm config set allow-scripts=pkg1,pkg2,pkg3`** silently writes a single garbage string to `.npmrc`. Always use one command per `pacote:script=true`.
- **`--allow-scripts=pkg1,pkg2,pkg3`** on the CLI flag does the same thing — the CLI joins names with spaces and npm rejects them.
- **Running `npm install` from a non-admin PowerShell** fails silently for global packages. Always use "Executar como administrador".
- **Logs disappearing** — npm 10+ emits `install-scripts` warnings to stdout but the actual install may still complete. Always verify with `openclaw --version` + `npm ls -g openclaw` instead of trusting "no errors".
- **Ignoring the `.npmrc` review step** — the four-line `Get-Content` is the only way to confirm the config is what you think it is. Skip it and you'll be debugging ghost warnings next session.
- **Trying to install OpenClaw from an OneDrive-synced folder** can corrupt node_modules. Always run `npm install -g` from `C:\Users\igorfe>` (or any non-synced folder), never from `~/MEGA/...` or `~/OneDrive/...`.

## Companion checklist (for the HDI demo presentation)

After OpenClaw is installed and verified, the typical companion asks are:

1. **Rodar o agente corporativo local** — confirm `openclaw agent run --help` (or equivalent sub-command for the installed version) before the demo.
2. **Emparelhar com Ollama local** — install Ollama, pull a small SLM (e.g. `qwen2.5:3b` for CPU), point OpenClaw at `http://localhost:11434`.
3. **Gravar POC** — short screen capture (≤5 min) showing the agent running locally, no cloud, executing a real task. Save the .mp4 in the same agent folder.
4. **Atualizar a apresentação** `IA_Corporativa_Privada_AWS_HDI_v2.pptx` com o print do `openclaw --version` como evidência de execução local.

These companion tasks live as separate entries in `TAREFAS.md` (TAR-20260812-003, TAR-20260812-004) and should not be conflated with the install task itself.

## References

- `references/npm-allow-scripts-pitfall.md` — full transcript of the npm parser failure with both CLI and config attempts, plus the correct one-per-package syntax.
- `templates/instalacao-windows.md` — Markdown template for the `AAAA-MM-DD_INSTALACAO-<AGENT>-POWERSHELL.md` report file.
- `templates/reinstalacao-windows.md` — Markdown template for the reinstallation playbook file.