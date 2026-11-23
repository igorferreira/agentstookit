---
name: xtool
description: "Use quando precisar construir, assinar, instalar ou deployar apps iOS (Swift/SwiftPM) a partir de Linux, Windows (WSL) ou macOS sem Xcode — via xtool (github.com/xtool-org/xtool)."
---

# xtool — Xcode multiplataforma (build/deploy iOS sem Mac)

Ferramenta open source (MIT, autor Kabir Oberai / xtool-org) que replica o Xcode:
builda pacotes SwiftPM em apps iOS, assina e instala em aparelhos, e fala com os
Apple Developer Services por código. Roda em Linux, Windows (via WSL) e macOS.

- Repo: https://github.com/xtool-org/xtool
- Docs: https://xtool.sh/documentation/xtooldocs/installation-linux
- Clone de referência local: ~/projetos/xtool-repo-reference (obtido em 12/11/2026,
  commit a2875dd; atualize com git pull se necessário)

## Segurança (auditoria 12/11/2026)

- Licença MIT; sem binários empacotados no repo; sem curl|bash; deps de fontes
  confiáveis (apple/, xtool-org, pointfreeco, vapor, swiftlang).
- Credenciais Apple (login `xtool setup`) vão SOMENTE para a Apple. Em Linux sem
  Keychain, o storage é arquivo local — proteger o diretório de config.
- Modo "Password" usa APIs privadas da Apple; prefira API Key se houver conta
  paga do Apple Developer Program.

## Instalação (Linux)

Pré-requisitos:
1. Swift 6.4 toolchain — https://swift.org/install/linux
2. usbmuxd (libimobiledevice): `sudo apt-get install usbmuxd` (útil também:
   `sudo apt-get install libimobiledevice-utils` → `ideviceinfo`)
3. Xcode 27.1 .xip baixado com login Apple em
   https://developer.apple.com/download/all/?q=Xcode (não dá via curl — requer login)

Instalar o AppImage do release mais recente:

```bash
curl -fL "https://github.com/xtool-org/xtool/releases/latest/download/xtool-$(uname -m).AppImage" -o xtool
chmod +x xtool
sudo mv xtool /usr/local/bin/
xtool --help
```

Configuração única:

```bash
xtool setup   # login (0=API Key pago / 1=Password) + caminho do Xcode.xip
swift sdk list   # deve mostrar: darwin
```

## Uso (subcomandos principais)

```bash
xtool new <nome>       # cria projeto SwiftPM novo
xtool dev              # builda e roda no aparelho conectado
xtool devices          # lista aparelhos iOS
xtool install <ipa>    # instala um .ipa
xtool uninstall        # desinstala app
xtool launch           # roda app instalado
xtool auth             # autenticação Apple Developer Services
xtool sdk              # gerencia o Darwin Swift SDK
xtool ds               # interage com Apple Developer Services
```

## Como biblioteca Swift

```swift
.package(url: "https://github.com/xtool-org/xtool", .upToNextMinor(from: "1.2.0"))
// produto: XKit (provisionamento/dispositivo) ou XToolSupport
```

## Convenções de desenvolvimento (repo)

- Swift 6 moderno, strict concurrency habilitado.
- Injeção de dependência via swift-dependencies (`@Dependency(\.foo)`).
- Commits: `subsystem: imperative description` (ex.: `auth: support reading password from stdin`).
- `Task { @concurrent in ... }` em vez de `Task.detached`.
- CLI é API estável (semver); a interface Swift não é.
- No repo, o CLAUDE.md apenas inclui o AGENTS.md (`@AGENTS.md`).
- Lint com `make lint` (swiftlint) antes de fechar mudanças.

## Limitações

- Buildar precisa do SDK extraído de um Xcode.xip oficial (download autenticado).
- Testar em aparelho real exige usbmuxd (Linux) ou USB passthrough (WSL/usbipd).
- Sem conta paga Apple Developer, o modo Password usa APIs privadas da Apple
  (recomendado criar Apple ID descartável para isso).
