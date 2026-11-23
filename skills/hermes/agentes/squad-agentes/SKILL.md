---
name: squad-agentes
description: "Use ao criar perfis de agentes Hermes ou auditar AGENTES.md."
---

## Squad de Agentes — criação, auditoria e mapa canônico

## Quando usar
- Criar novos perfis de agentes (`~/.hermes/profiles/<nome>/SOUL.md`), especialmente squads temáticos (jurídicos `juris-*`, médicos `saude-*`, DevSquad `devsquad-*`).
- Atualizar/auditar o parque de agentes e o arquivo canônico `~/clawd/AGENTES.md`.
- Mapear apelidos de família em `~/clawd/IDENTITY.md`.

## Fluxo completo: criar agente especialista do zero

Criar um novo agente de domínio passa por duas fases distintas: (A) pesquisa + base documental canônica; (B) estrutura de perfil + registro. Nunca pular a fase A — um SOUL.md sem referência documental gera respostas alucinadas.

### Fase A — Pesquisa e base canônica
1. **Mapear fontes primárias:** Wikipedia da comunidade relevante, instituições oficiais, portais de referência, artigos acadêmicos. Priorizar fontes com profundidade (limitar `web_extract` a 25k chars/página). Post de rede social (LinkedIn etc.) via página guest: o texto integral costuma estar no `og:description` do HTML — baixe com curl + UA e extraia a meta tag.
   - **Encurtadores (lnkd.in/lnkd.id) NÃO redirecionam via `curl -I`** — o -w %{redirect_url} vem vazio e o -L devolve o próprio atalho. Faça GET da página intersticial e extraia o destino real com grep no `href="https://..."`. Atalho que nem abre (HTTP 000): confirme o recurso conhecido direto na fonte primária (ex.: github.com/<owner>/<repo>) e anote no documento que foi verificação direta — nunca deixe encurtador no artefato canônico.
2. **Pesquisas convergentes separadas por sub-domínio:** ex. "entidades vs orixás", "história/marco fundador", "dogmas/princípios", "estatísticas/presença contemporânea". Cada busca cobre um aspecto distinto para evitar recapitulação.
3. **Compilar em documento único:** todo o conhecimento estruturado em `~/.hermes/docs/memoria/<tema>-base-conhecimento-completa.md`. Organizar por seções claras. Não fragmentar em múltiplos arquivos curtos.
4. **Registrar no INDEX.md:** append ao fim de `~/.hermes/docs/memoria/INDEX.md` com caminho e descrição resumida.

### Fase B — Perfil e registro
1. **Diretório:** `mkdir ~/.hermes/profiles/<nome>/`
2. **SOUL.md:** identidade (persona/nome), domínios, regramas específicas. Mínimo viável ~25-30 linhas.
3. **`.env`:** copiar de perfil funcionando SEM ler conteúdo.
4. **`config.yaml`:** mínimo — só `model.default` + `model.provider`.
5. **Smoke test:** pergunta real do domínio com timeout 180s.
6. **Registros:** `hermes profile describe`, `IDENTITY.md`, `AGENTES.md`, `INDEX.md`.

## Estrutura de um perfil
Cada agente = diretório `~/.hermes/profiles/<nome>/` com `SOUL.md` dentro. SOUL.md mínimo viável (~25-30 linhas):

1. Título `# <nome> — <papel>` + missão em 1 linha
2. **Quando acionar** (trigger concreto)
3. **Personalidade** (tom, idioma pt-BR)
4. **Responsabilidades** (5-8 bullets)
5. **Entregáveis típicos**
6. **Regras** (quality gates aplicáveis ao domínio)
7. (Squads) nota de coordenação: quem orquestra, quem fala com o Hermes

## Regras de criação
- Base canônica > SOUL.md curto: a memória densa em `.md` no `memoria/` é muito mais eficaz que tentar condensar tudo no SOUL.md — futuro-sessão vai consumir todo o contexto anyway.
- Apelido obrigatório: todo agente novo recebe nome próprio registrado em `IDENTITY.md`; Igor chama pelo apelido nos canais.
- Limite de chaves/credenciais: NUNCA incluir senhas, tokens ou keys em qualquer artefato; substituir por `[REDACTED]`.

## Estrutura de um perfil
Cada agente = diretório `~/.hermes/profiles/<nome>/` com `SOUL.md` dentro. SOUL.md mínimo viável (~25-30 linhas):

1. Título `# <nome> — <papel>` + missão em 1 linha
2. **Quando acionar** (trigger concreto)
3. **Personalidade** (tom, idioma pt-BR)
4. **Responsabilidades** (5-8 bullets)
5. **Entregáveis típicos**
6. **Regras** (quality gates aplicáveis ao domínio)
7. (Squads) nota de coordenação: quem orquestra, quem fala com o Hermes

## DevSquad (criada 05/09/2026, 8 perfis `devsquad-*`)
Squad genérica agnóstica de domínio (sem HDI/seguros). Fluxo: `po → architect → backend/frontend → qa → reviewer → devsecops`, orquestrados por `devsquad-lead`. Quality gates: spec antes de código (SDD), testes 100%, cobertura ≥80% core, zero segredos. Chamar pelo prefixo "devsquad" ou explicar a demanda de dev que o Hermes direciona ao lead.

## Mapa canônico AGENTES.md
- Local: `~/clawd/AGENTES.md` · Espelho Google Drive: `~/Insync/GoogleDrive/igorferreirabr/Dev_IA/ia_agentes/AGENTES.md` (copiar SEMPRE nos dois, o Insync sincroniza; confirme o caminho com `find ~/Insync -name AGENTES.md` — o prefixo de pasta pode mudar).
- O índice em tabela pode estar com linhas vazias/corrompidas — quando estiver, faça APPEND de seção datada no fim (padrão: `- **Apelido (`id`)** — descrição, base de conhecimento, uso`) em vez de regenerar tudo.
- Estrutura: cabeçalho com data/hora + contagem total por família, seções por domínio (núcleo, financeiro, relacionamento, saúde, carreira, banca HDI, DevSquad, operacionais, jurídico), tabela "como chamar" (apelido / prefixo / assunto).
- **Sempre contar os perfis de verdade com `ls ~/.hermes/profiles/ | wc -l` e `grep -c juris` / `grep devsquad` etc.** — o parque cresce entre sessões; nunca confiar na contagem da memória.
- Ao dar apelido novo a um agente, atualizar também `~/clawd/IDENTITY.md`.

## Dando vida ao perfil (setup de runtime)
Criar o SOUL.md NÃO deixa o agente utilizável. Completar, nesta ordem:
1. `.env`: copiar de um perfil que funciona SEM ler o conteúdo (`cp ~/.hermes/profiles/<funcionando>/.env ~/.hermes/profiles/<novo>/.env && chmod 600 ...`) — sem isso `hermes -p <nome>` falha com "No LLM provider configured". O template traz `TELEGRAM_BOT_TOKEN`: para agente só-local (uso via `-p`), remova a linha (`sed -i '/^TELEGRAM_BOT_TOKEN=/d'` no .env do perfil novo, sem ler o valor) — token duplicado faz o gateway estacionar o perfil.
2. `config.yaml` próprio e MÍNIMO, só com `model.default` + `model.provider` (o .env copiado não traz modelo; herdar config inteiro arrasta risco de drift) — sem isso o -p falha com "No models provided" (HTTP 400 do OpenRouter).
3. Smoke test com persona real: rode `timeout 150 hermes -p <nome> -z "<pergunta típica do domínio>"` sem overrides e confira se a resposta segue o tom/regras do SOUL. Se o resultado for ambíguo, repita com `-m <modelo> --provider <provider>` para separar falha de resolução da configuração do perfil de falha da chamada ao provedor; se só o comando com overrides funcionar, corrija a configuração salva e repita o teste normal antes de declarar o perfil pronto.
   - **PITFALL `Gateway inaccessible: profile_parked`:** se a falha citar CONFLITO ENTRE OUTROS perfis (dois perfis com o mesmo `TELEGRAM_BOT_TOKEN`), o problema é global — o multiplexer em execução se recusa a servir QUALQUER perfil nomeado e até perfis conhecidos falham. Contorne SEM tocar nos outros perfis: remova o token do .env do perfil novo E adicione `gateway:\n  standalone: true` ao config.yaml dele (o cliente passa a subir gateway próprio em vez de esperar o multiplexer). O fix raiz (remover o token duplicado do perfil conflitante) modifica outro perfil — só com autorização explícita do Igor.
4. Registrar: `hermes profile describe <nome> --text "..."` (flag é `--text`). Comando é `hermes profile` (singular); `hermes profiles` não existe.
5. Avisos "profile shares its telegram credential with default" no `hermes profile list` são inofensivos para agentes usados só via `-p` local.

## Verificação de delegação (pitfall crítico)
⚠️ Validado 05/09/2026: um `delegate_task` para criar 8 perfis criou os **diretórios mas não escreveu os SOUL.md** e respondeu "completed" (summary genérico "Now writing..."). A sub-avaliação de tarefa de spawn em lote pode parar no meio.

**Regra:** após qualquer delegação que deva criar arquivos, verificar no processo principal ANTES de reportar:
```bash
find ~/.hermes/profiles/devsquad-* -name "SOUL.md" | wc -l   # deve bater com o pedido
grep -il "HDI\|SUSEP" <arquivos criados>                       # regras de domínio respeitadas
```
Se incompleto: apagar os restos (`rmdir` nos diretórios vazios) e escrever os arquivos diretamente no processo principal — é rápido e confiável para ~8 arquivos pequenos. Delegação só vale a pena para geração longa (decks, PDFs) com verificação de saída obrigatória.

## Cron jobs de rotina de agentes
- Vigias existentes: faturas por email (`verificar-faturas-email.py`), vencimentos (`verificar-vencimentos.py`), AVISOS (`verificar-avisos.py`), CCT (`vigia-cct-feaac.py`), horas HDI semanal (job `85e92800ae50`, sexta 17h — lê a planilha de horas e reporta dias faltando).
- Ao criar job novo, pinnar modelo (`hermes cron edit <id> --provider openrouter --model <modelo>`) — jobs unpinned falham com `drift_skip` quando o modelo global muda.
- Sempre testar com `hermes cron run <id>` na hora e checar `last_status: succeeded`.

## Agentes de monitoramento externo
Para um agente que acompanha preços, disponibilidade ou horários, trate estes estados separadamente:
1. **Perfil pronto:** `SOUL.md`, `.env` copiado sem leitura, `config.yaml` mínimo e smoke test real aprovados.
2. **Operação configurada:** parâmetros persistidos em um diretório canônico, incluindo origem/destino, datas, restrições, custos acessórios e campos ainda pendentes.
3. **Monitoramento ativo:** cron criado, modelo fixado, execução manual bem-sucedida e `last_status: succeeded` verificado.
4. **Primeira cotação válida:** pelo menos uma coleta produz resultados verificáveis e é registrada no histórico append-only.

Não chame o monitoramento de “ativo” só porque o perfil foi criado: informe explicitamente qual desses quatro gates passou. Antes de agendar coletas, resolva os campos que mudam a validade do resultado — por exemplo, endereço completo para calcular deslocamentos — ou registre a limitação no job. Faça uma coleta manual inicial antes de confiar no cron; ela revela parâmetros inválidos e evita um histórico preenchido com resultados incompletos.

Ao criar um agente de domínio, registre-o no `AGENTES.md` e, se houver apelido, no `IDENTITY.md`; mantenha o arquivo canônico de configuração separado do perfil executável para que ajustes de operação não alterem a persona. Se o mapa exigir espelho em outra pasta sincronizada, copie o registro para os dois destinos e releia ambos antes de reportar.
