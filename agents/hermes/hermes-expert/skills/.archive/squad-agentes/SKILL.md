---
name: squad-agentes
description: "Use ao criar perfis de agentes Hermes ou auditar AGENTES.md."
---

# Squad de Agentes — criação, auditoria e mapa canônico

## Quando usar
- Criar novos perfis de agentes (`~/.hermes/profiles/<nome>/SOUL.md`), especialmente squads temáticos (jurídicos `juris-*`, médicos `saude-*`, DevSquad `devsquad-*`).
- Atualizar/auditar o parque de agentes e o arquivo canônico `~/clawd/AGENTES.md`.
- Mapear apelidos de família em `~/clawd/IDENTITY.md`.

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
- Local: `~/clawd/AGENTES.md` · Espelho Google Drive: `~/Insync/GoogleDrive/igorferreirabr/03_Dev_IA/ia_agentes/AGENTES.md` (copiar SEMPRE nos dois, o Insync sincroniza).
- Estrutura: cabeçalho com data/hora + contagem total por família, seções por domínio (núcleo, financeiro, relacionamento, saúde, carreira, banca HDI, DevSquad, operacionais, jurídico), tabela "como chamar" (apelido / prefixo / assunto).
- **Sempre contar os perfis de verdade com `ls ~/.hermes/profiles/ | wc -l` e `grep -c juris` / `grep devsquad` etc.** — o parque cresce entre sessões; nunca confiar na contagem da memória.
- Ao dar apelido novo a um agente, atualizar também `~/clawd/IDENTITY.md`.

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
