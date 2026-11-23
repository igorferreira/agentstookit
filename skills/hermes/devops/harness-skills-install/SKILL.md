---
name: harness-skills-install
description: Use when installing skill repos into agent harnesses.
---

# Instalar coleções de skills em harnesses de agente

Classe de tarefa: Igor manda um post/lista com N repositórios de skills e pede para instalar num harness (OpenCode, Claude Code, Hermes, Codex, OpenClaw). Tabela de paths e instaladores específicos por harness: [`references/harness-paths.md`](references/harness-paths.md).

## Procedimento

### 1. Resolver o conteúdo do post

Posts de X: fxtwitter API (`https://api.fxtwitter.com/<user>/status/<id>`) → extrair URLs dos repositórios do texto. Listas podem misturar skills individuais e coleções — classifique cada repo antes de instalar.

### 2. Verificar se o harness existe

`command -v <harness>` antes de tudo. Se não existe, instalar primeiro (pergunta ao Igor se o método não for óbvio) — não instale skills em harness inexistente.

### 3. Clonar tudo para staging (superfície de inspeção)

```bash
git clone --depth 1 https://github.com/<org>/<repo> <staging>/<nome>
```

### 4. Localizar os SKILL.md CANÔNICOS de cada repo

Coleções espelham skills em vários diretórios (`.claude/`, `.openclaw/`, `.agents/`, `plugins/`, `cli/assets/`, `tests/`). Instale **uma** fonte canônica por skill — normalmente `skills/` na raiz do repo ou o diretório específico do harness alvo (ex.: `.opencode/skills/`). Um mesmo skill espelhado 5× vira 5 skills duplicados no harness.

### 5. Scan de segurança ANTES de copiar

```bash
grep -rn --include='SKILL.md' -E 'curl .*\| *(ba)?sh|secret-tool|eval\(|rm -rf /|base64 -d' <staging>/
```

Ocorrências de `api_key`/`.env`/`credentials` em contexto de BOAS PRÁTICAS ("never commit .env") são benignas. Bloqueie: pipe para shell, leitura de keyring, envio de credenciais para domínios de terceiros. Ao menor sinal de exfiltração, não instale e reporte ao Igor.

### 6. Copiar com prefixo anti-colisão

Skills de coleções diferentes colidem de nome (duas coleções têm `test-driven-development`). Prefixe o DIRETÓRIO com sigla da coleção (`pt-`, `ao-`, `cav-`…) — a maioria dos harnesses registra pelo frontmatter `name`, não pelo nome da pasta, então o prefixo no diretório preserva proveniência sem quebrar descoberta. Garanta frontmatter `name` único no conjunto instalado.

**Não instale subcoleções que exigem plataforma externa** (ex.: skills que só funcionam com conta em serviço SaaS) nem `template-skill`/gabaritos — instale e informe ao Igor o que ficou de fora e por quê.

### 7. Usar o instalador OFICIAL quando o repo tiver um

Antes de copiar à mão, leia o README/INSTALL do repo — alguns têm mecanismo próprio que registra skills + comportamento de plugin (ex.: coleções que viram plugin no config do harness). Copiar à mão quando existe instalador oficial perde a parte de plugin/agentes. Quando o instalador não existir, use o universal `npx skills add <org>/<repo> -g` (ver `references/harness-paths.md`). Skills que embarcam runtime próprio de CLI (init por workspace, provedor de serviço, renderer) têm passos extras de setup e smoke test: [`references/tool-skill-runtimes.md`](references/tool-skill-runtimes.md).

### 7b. Claude Code: plugins nativos via CLI (preferir a copiar skills)

Claude Code ≥2.x tem CLI de plugin — para coleções empacotadas como plugin (ex.: ECC), esta é a rota oficial e não se copia skill à mão:

```bash
claude plugin marketplace add https://github.com/<org>/<repo>
claude plugin install <plugin>@<marketplace>
claude plugin list          # validar: status enabled + version
```

- Instalação em escopo user fica registrada no settings do usuário e os comandos/skills chegam **namespaced** (`/<plugin>:<comando>`) — citar a forma namespaced ao Igor, não os nomes curtos.
- **Verificar o que o plugin NÃO distribui antes de declarar pronto** — plugins não embarcam `rules/` nem rodam `npm install` do plugin (hooks podem precisar de deps do repo); o README do repo costuma marcar etapa manual obrigatória após o plugin install.
- O CLI avisa "N userConfig options not yet set" na instalação — registrar no reporte; configurar depois via `/plugin configure <plugin>@<marketplace>` dentro do Claude Code.

### 8. Validar a descoberta pelo harness

Cada harness tem comando de listagem (ver tabela em references/harness-paths.md — ex.: OpenCode `opencode debug skill`). Exigência: TODOS os skills instalados aparecem na listagem, 0 ausentes, 0 colisão de nome. Contar antes/depois.

### 9. Registrar e reportar

PEDIDOS.md/TAREFAS.md com início/fim, tabela instalados × excluídos (com motivo), e o passo pendente do usuário se houver (ex.: auth/provider do harness recém-instalado).

## Pitfalls

- **NUNCA instale skill espelhado múltiplas vezes** — coleções espelham o mesmo SKILL.md em `.claude/`, `.openclaw/`, `tests/`; escolha a fonte canônica (ou a do harness alvo) e copie 1×.
- **NUNCA confie que a pasta instalada = skill descoberto** — valide com o comando de listagem do harness; skill sem frontmatter `description` é filtrado silenciosamente.
- **Instaladores de terceiros que escrevem no harness de outro** (ex.: instalador que só escreve em `~/.claude/skills`) — rode, depois COPIE o resultado para o diretório do harness alvo.
- **Prefixo só no diretório, não no frontmatter `name`** — alguns harnesses casam `name` com pasta; se casar, prefira renomear ambos de forma consistente e revalidar.
