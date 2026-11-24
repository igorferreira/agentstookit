---
name: task-management
description: Task orchestration for Igor — daily task capture, agent routing, mood tracking, and multi-agent delegation patterns.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [task-management, daily-tasks, agent-routing, mood, productivity]
---

# Task Management — Daily Orchestration

## Overview

Igor quer que o agente principal organize suas tarefas diárias, roteie para os agentes especialistas corretos e mantenha arquivos de fonte da verdade. Esta skill cobre o padrão completo.

## When to Use

Quando Igor:

- Listar tarefas do dia ("coisas que fiz e ainda tenho que fazer")
- Pedir para "organizar" ou "registrar" tarefas
- Mencionar "agentes que podem me ajudar"
- Quiser registrar humor/estado emocional
- Pedir "faz o que você consegue fazer" e delegar o resto
- Quiser um briefing do que está pendente

## Arquivos e Registros Canônicos

| Arquivo / Sistema | Propósito |
|---|---|
| `~/MEGA/Documentos/TAREFAS.md` | Fonte da verdade — todas as tarefas com status, agente e links |
| `~/MEGA/Documentos/HUMOR.md` | Registro de humor com intensidade e contexto |
| `hermes kanban` (Board `default`) | Registro operacional durável dos pedidos em fila e ciclo de vida (`references/protocolo-fila-pedidos.md`). **Obrigatório enviar o link do Kanban em todas as respostas.** |

**Nunca criar arquivos canônicos fora de `~/MEGA/Documentos/`. Para pedidos recebidos no chat, registrar e sincronizar no board `default` do `hermes kanban`, mantendo horários de início e fim e enviando sempre o link do Kanban nas mensagens ao Igor.**

**Fila cronológica e dispatcher:** Quando um pedido novo precisar aguardar itens anteriores, crie o card já com dependência(s) dos pedidos anteriores ainda abertos, para que permaneça em `todo` até a fila liberar. Não presuma que criar sem assignee evita despacho: `create` pode colocar o card em `ready`. Não use `block --kind dependency` como substituto após criar sem parent; sem parent aberto, a transição pode virar `needs_input` e registrar um run bloqueado. Procedimento e verificação em `references/protocolo-fila-pedidos.md`.

**Pedido com prazo:** Antes de enfileirar um pedido ligado a uma data, confira o prazo e conte os predecessores abertos. Se o volume da fila ameaçar a data, preserve a ordem até Igor autorizar prioridade, mas informe que a tarefa ainda não começou, diga o número exato de predecessores e ofereça a opção de repriorização; não prometa uma data de entrega sem base.

Quando Igor complementar ou corrigir um pedido que já está **NA FILA**, atualize o card e a linha espelhada desse pedido, preservando sua posição, status e dependências; não aplique o detalhe ao card em execução nem comece o item. Uma clarificação não é autorização para furar a fila.

### Autorização ampla para executar a fila com orquestração

Quando Igor pedir explicitamente para liberar/executar os pedidos pendentes e distribuir o trabalho em paralelo, trate isso como autorização para iniciar todos os cards pendentes que estejam prontos ou cuja dependência operacional já tenha sido satisfeita — não pergunte novamente se o escopo inclui “todos ou só os recentes”. A autorização não libera tarefas já concluídas, não cancela tarefas em execução e não remove dependências ou bloqueios reais.

1. Faça um inventário do board `default` e reconcilie os IDs com `PEDIDOS.md`; para cada card aberto, confira descrição completa, dependências, comentários, anexos, estado e runs. O board é a fonte operacional; o Markdown é o espelho.
2. Atue como orquestrador: monte uma matriz curta `ID → objetivo/área → dependências/arquivos compartilhados → perfil escolhido → decisão (despachar, serializar ou manter bloqueado)`. Selecione o melhor perfil existente pelo domínio e pelas instruções reais do perfil; não atribua o lote inteiro a um único agente nem suponha que perfil criado significa perfil disponível.
3. Preserve a ordem cronológica ao decidir o que entra em cada onda, mas permita concorrência explícita entre tarefas independentes. A autorização de paralelismo substitui apenas a regra normal de uma tarefa principal por vez; não autoriza furar precedências.
4. Despache em paralelo somente cards `ready` sem dependências abertas e sem colisão de escrita. Tarefas que alterem os mesmos arquivos, controles ou fontes canônicas devem ter um único responsável ou ser serializadas com dependência explícita. Não use dispatcher às cegas antes da triagem/atribuição.
5. Mantenha `todo` quando houver predecessor aberto. Mantenha `blocked` quando faltar dado/decisão do Igor, aprovação específica, perfil obrigatório ou etapa externa; registre objetivamente o bloqueio e prossiga com os demais cards elegíveis. Autorização ampla para trabalhar não é autorização para enviar comunicação externa, movimentar dinheiro, comprar, excluir em lote ou fazer mudança irreversível sem o consentimento específico exigido.
6. Passe a cada agente o escopo e contexto autocontidos, o perfil selecionado, caminhos canônicos, limites de escrita e critérios verificáveis de conclusão. Após a onda, confira artefatos, resultados e conflitos; não aceite resumo do agente como prova suficiente.
7. Registre início no momento do despacho e fim apenas após verificação real, tanto no Kanban quanto na linha correspondente de `PEDIDOS.md`. Não feche o cartão de coordenação enquanto houver despacho/integração ou reconciliação obrigatória pendente.



**Pitfall — execução direta e dispatcher:** Antes de começar um pedido que será executado nesta sessão, verifique o card recém-criado. Se ele foi atribuído a `default` e iniciou um worker automático, evite duplicidade: recupere o ID exato com `reassign <id> none --reclaim`, depois faça `claim <id>` para esta sessão. Feche pelo agente-pai somente após verificar a entrega. Atualize `PEDIDOS.md` por patch da linha específica, após reler o estado atual, para preservar alterações concorrentes.

### Retomar pedido em andamento após troca de contexto

Quando uma lista de tarefas preservada indicar o item ativo e os próximos itens pendentes, trate-a como plano operacional: confira `PEDIDOS.md` e o card exato no board `default`, continue do primeiro item ativo e revalide cada pendência contra os artefatos antes de repetir trabalho. Em uma fila sequencial, carregue somente as skills necessárias à etapa ativa; deixe as skills exclusivas das etapas futuras para quando elas se tornarem ativas e não faça um lote de leituras antecipadas que misture todas as etapas. Preserve o mesmo ID, não crie card duplicado e não refaça subetapas já verificadas. Se uma leitura de contexto/skill ou lote paralelo falhar parcialmente, separe resultados válidos dos bloqueados e não repita uma chamada barrada pela guarda de idempotência. Continue pela primeira etapa ativa usando o conteúdo já retornado ou uma fonte equivalente; faça uma única leitura alternativa específica somente se faltar instrução indispensável. Classifique a tarefa como `blocked` apenas quando um pré-requisito operacional real (dado/decisão do Igor, acesso externo ou aprovação) impedir a próxima ação. Uma leitura inacessível, truncada, bloqueada ou uma decisão ainda irrecuperável não basta, por si só, para encerrar o trabalho: avance em tudo que não dependa dela. Não encerre a interação nem peça ao Igor para reenviar “continue” por causa de um aviso interno; reporte apenas o impedimento real que ainda impeça progresso.

## Gate: confirmar a fonte antes de criar ou reorganizar

1. Pesquisar primeiro por `TAREFAS.md` e por referências a `TAREFAS.md` no workspace e em `~/MEGA/Documentos/`.
2. Ler o arquivo candidato completo o suficiente para identificar cabeçalho, tarefas ativas, recorrentes e histórico antes de escrever.
3. Se `~/MEGA/Documentos/TAREFAS.md` já existir, tratá-lo como a fonte canônica: adicionar ou reorganizar uma visão diária dentro dele, preservando as seções e IDs existentes.
4. Manter `~/clawd/PEDIDOS.md` como fila geral operacional, quando o protocolo local exigir; não transformar essa fila em uma segunda lista diária nem copiar todas as tarefas para ela.
5. Atualizar o carimbo de data/hora após a mudança e verificar que o painel diário, as tarefas existentes e os links continuam legíveis.

**Pitfall:** não crie um segundo `TAREFAS.md`, `TASKS.md` ou lista diária concorrente apenas porque encontrou arquivos auxiliares; duas fontes de verdade fazem uma atualização parecer concluída enquanto a outra permanece desatualizada.

## Padrão: captura de tarefas do dia

Quando Igor listar tarefas (numeradas ou em parágrafos), seguir este ciclo:

### 1. Analisar cada item

Para cada tarefa listada:

- Classificar: ✅ Concluída / 🔴 Hoje / 🟡 Essa semana / 🟢 Futuro
- Identificar agente especialista relevante
- Identificar o que o main agent pode fazer IMEDIATAMENTE
- Identificar o que depende do Igor (presencial, decisão pessoal)

### 2. Criar/atualizar TAREFAS.md

Estrutura do arquivo:

```markdown
# TAREFAS.md — Fonte da Verdade

> 📅 YYYY-MM-DD HH:MM

## ✅ Concluídas hoje
| # | Tarefa | Agente | Detalhe |

## 🔴 Hoje — ainda preciso fazer
| # | Tarefa | Agente | Ação concreta |

## 🟡 Essa semana
| # | Tarefa | Agente | Ação concreta |

## 🟢 Setembro / Futuro próximo
| # | Tarefa | Agente | Ação concreta |

## 🤖 Mapeamento de agentes sugeridos
| Agente | Para tarefas de |

## 💰 Contas a pagar (se relevante)

## 🔁 Recorrentes

| ID | Dias | Horário | Tarefa |
|---|---|---|---|
| TAR-REC-KARATE | Terça, Quinta | 20:00–22:00 | 🥋 Karatê |
| TAR-REC-KARATE-SAB | Sábado | 09:00–11:00 | 🥋 Karatê |

---

## 📝 Notas
```

### 3. Reconciliar correções posteriores de status

Se Igor disser depois que começou a trabalhar em uma tarefa antes marcada como concluída, reabrir imediatamente o item como `🔄 Em andamento`: remover/retirar a linha da seção de concluídas, preservar o mesmo ID, registrar data e hora exatas de início, atualizar o painel diário e não inventar uma data de fim. Ao receber a confirmação de término, registrar a hora de fim e só então mover o item para concluídas.

**Pitfall:** não trate a frase anterior “tudo concluído” como imutável quando Igor iniciar explicitamente um item depois; o estado operacional mais recente prevalece, e manter o item como concluído oculta trabalho ativo no painel.

### 4. Criar/atualizar HUMOR.md

Quando Igor mencionar estado emocional (ansiedade, angústia, cansaço, etc.):

```markdown
# 😰 HUMOR.md — Registro de Humor

> 📅 YYYY-MM-DD HH:MM

## [emoji] Hoje: [estado]

**Intensidade:** X/10

**O que pesa:**
1. [fator 1]
2. [fator 2]

**O que ajuda:**
- [ação concreta]
```

Analisar cada fator com profundidade: por que isso pesa? Qual o histórico? O que pode aliviar?

### 4. Executar o que o main agent consegue fazer AGORA

Itens que NÃO dependem do Igor:

- Verificar contas a pagar (consultar AGENDA.md)
- Atualizar LinkedIn (preparar sugestão)
- Analisar propostas financeiras
- Preparar scripts de conversa
- Delegar para agentes especialistas

### 5. Delegar para agentes em paralelo

Usar `delegate_task` com batch de até 3 tarefas. Cada subagente recebe:

- `goal`: descrição clara da entrega
- `context`: TODOS os fatos relevantes (nomes, valores, datas, histórico)
- `role`: `leaf`
- `toolsets`: apenas os necessários (`terminal`, `file`, `web`)

**Pitfall:** subagentes NÃO têm acesso à memória da conversa. Todo contexto precisa estar no campo `context`.

## Tabela de roteamento de agentes

| Gatilho | Agente | Profile |
|---|---|---|
| `financeiro`, `fatura`, `boleto`, `pix`, `cdb` | `finance-senior` | `finance-senior` |
| `rh`, `carreira`, `curriculo`, `rescisao`, `linkedin` | `hr-tech-senior` | `hr-tech-senior` |
| `carro`, `rubens`, `combustivel` | `mecanico` | `mecanico` |
| `saude`, `exame`, `alimentacao` | `saude` | `saude` / `health-performance-board` |
| `rafael`, `adrielly`, `relacionamento` | `relationship-senior` | `relationship-senior` |
| `java`, `codigo`, `debug` | `java-senior` | `java-senior` / `java-architect` |
| `dotnet`, `c#`, `.net` | `dotnet-architect` | `dotnet-architect` |
| `ia`, `genai`, `mcp`, `agentes` | `ai-solution-architect` | `ai-solution-architect` |
| `arquitetura`, `solucoes`, `hdi` | `solution-architect` | `solution-architect` |
| `devex`, `plataforma`, `cli`, `ide` | `devex-platform-senior` | `devex-platform-senior` |
| `seguranca`, `devsecops`, `lgpd`, `susep` | `devsecops-governance-senior` | `devsecops-governance-senior` |
| `seguros`, `insuremo`, `sinistro`, `apolice` | `insurance-domain-senior` | `insurance-domain-senior` |
| `transformacao-digital`, `c-level`, `dora` | `digital-transformation-exec` | `digital-transformation-exec` |
| `python`, `script`, `automacao` | `python-senior` | `python-senior` |
| `aws`, `cloud`, `oswaldo` | `aws-tutor` | `aws-tutor` |
| `diario`, `registro`, `memoria` | `diario` | `diario` |
| Produto, Discovery | `product-senior` | `product-senior` |
| Tudo o resto | **main** | `main` |

## Padrão: Rafael (relacionamento)

Quando a tarefa envolver [NOME-REDACTADO]:

1. Confirmar e rotear para o perfil Hermes real `relationship-senior`. A skill `conselheiro-relacionamento` fornece metodologia/voz ao perfil que a carrega; isso não prova que o perfil especializado foi executado.
2. Em uma segunda opinião independente sobre exports, exigir que o revisor examine os ZIPs originais, reconstrua a cronologia e formule uma leitura preliminar antes de consultar o relatório anterior; depois comparar concordâncias e divergências com citações e limites explícitos.
3. Se o perfil não iniciar, inspecionar o card exato e seus eventos/runs; não repetir a mesma falha nem alterar credenciais/configuração para contornar conflito. Não substituir silenciosamente por `delegate_task`: usar fallback somente com autorização explícita para um substituto e identificá-lo como fallback, nunca como Rafael real. Se não houver autorização para substituição, manter bloqueado e perguntar se Igor prefere aguardar/reparar o perfil ou aceitar uma análise alternativa. Se o critério de aceite exigir o perfil real, manter o card bloqueado até o perfil executar ou Igor alterar o critério.
4. Produzir rascunho em `~/clawd/` apenas como staging; mover relatório pessoal verificado para `~/MEGA/Documentos/relacionamentos/adrielly/` na subpasta canônica de conversas. Atualizar `INDEX.md`, `DIARIO-RELACIONAMENTO-ADRIELLY.md`, `TAREFAS.md` e a linha correspondente em `PEDIDOS.md`, preservando o mesmo ID Kanban.

**Regra de ouro:** Igor consulta Rafael antes de qualquer ação com [NOME-REDACTADO]. Se ele já interagiu com ela, o Rafael analisa DEPOIS, mas a regra para próximas ações continua valendo.

## Padrão: "faz o que você consegue fazer"

Quando Igor disser isso:

1. Identificar TODAS as tarefas que não dependem de ação física/presencial dele
2. Executar o que o main agent consegue fazer diretamente (verificar contas, preparar textos, analisar dados)
3. Delegar o resto em paralelo via `delegate_task` (batch de até 3)
4. Reportar o que foi feito + o que ficou para o Igor fazer

## Pitfalls

### Subagentes não têm contexto da conversa
O campo `context` precisa conter TUDO que o subagente precisa saber. Não referenciar "conforme discutimos antes" — o subagente não viu a discussão.

### TAREFAS.md pode crescer demais
Use links para arquivos de detalhe em vez de duplicar informação e mantenha o painel diário enxuto. Não remova automaticamente tarefas concluídas, IDs antigos ou histórico existente só para reduzir o tamanho: arquive ou limpe apenas com uma regra explícita já definida para o arquivo, porque apagar histórico quebra rastreabilidade e pode invalidar links.

### Rafael precisa do contexto REAL
[NOME-REDACTADO] é um tópico sensível. Se o Rafael receber informação incompleta na primeira análise, fazer REANÁLISE com os fatos completos (mensagens literais, status, timing). Nunca manter uma análise baseada em premissas erradas.

### Arquivos de entrega no workspace
`~/clawd/` é área de trabalho e pode ser usada como **staging temporário**, não como destino pessoal permanente. Quando uma entrega for documento pessoal/profissional do Igor:

1. Classificar o arquivo individualmente antes de mover; nunca assumir que todo o conteúdo de `clawd/` é pessoal.
2. Excluir do escopo arquivos de agente, configuração e infraestrutura (`AGENTS.md`, `SOUL.md`, `USER.md`, `MEMORY.md`, `PEDIDOS.md`, `TOOLS.md`, `HEARTBEAT.md`, `IDENTITY.md`, `BOOTSTRAP.md`, `memory/`, `.hermes/`, `.git/`, `canvas/`).
3. Verificar tipo real, conteúdo e indícios de credenciais/configuração antes da migração.
4. Mover somente documentos pessoais confirmados para a pasta canônica sob `~/MEGA/Documentos/` ou `~/MEGA/Comprovantes/`.
5. Se um arquivo misturar assuntos, dividi-lo por domínio e preservar uma cópia integral em `MEGA/Documentos/registros_manutencao/originais_clawd/`.
6. Atualizar todos os links em `TAREFAS.md` para os novos caminhos relativos.
7. Verificar destinos, links e ausência das fontes antigas. Para uma operação sensível, compare hashes dos arquivos protegidos antes/depois.
8. Downloads inválidos ou itens ambíguos ficam parados até confirmação; não apagá-los por conta própria.

Procedimento detalhado: [`references/workspace-document-migration.md`](references/workspace-document-migration.md).

## Padrão: tarefas recorrentes com cron

Quando Igor registrar tarefa recorrente com dias e horários fixos (ex.: karatê ter/qui 20h, sáb 9h):

1. Registrar no TAREFAS.md na seção `### 🔁 Recorrentes`
2. Criar script de lembrete em `~/.hermes/scripts/` (bash, verifica dia da semana + hora)
3. Criar cron job `no_agent=True` com o script (usar `cronjob action='create'`)
4. Horário do lembrete = 30 min antes da tarefa

**Exemplo de script de lembrete:**
```bash
#!/bin/bash
DIA=$(date '+%u')   # 1=Seg, 2=Ter, 3=Qua, 4=Qui, 5=Sex, 6=Sab, 7=Dom
HORA=$(date '+%H%M')
if [ "$DIA" = "2" ] && [ "$HORA" = "1930" ]; then
    echo "🥋 Karatê em 30 minutos! (20:00–22:00)"
elif [ "$DIA" = "4" ] && [ "$HORA" = "1930" ]; then
    echo "🥋 Karatê em 30 minutos! (20:00–22:00)"
elif [ "$DIA" = "6" ] && [ "$HORA" = "0830" ]; then
    echo "🥋 Karatê em 30 minutos! (09:00–11:00)"
fi
```

**Script path:** usar caminho relativo (`lembrete-karate.sh`) — o cron job espera scripts em `~/.hermes/scripts/`.

## Padrão: listas de pendências por local com aviso sem LLM

Quando Igor pedir controle recorrente de compras ou pendências de uma casa, pessoa ou local específico:

1. Criar uma fonte canônica Markdown em `~/MEGA/Documentos/` dentro do domínio correspondente, com uma seção `## Compras pendentes` usando checkboxes `- [ ]` e uma seção `## Itens concluídos` usando `- [x]`.
2. Registrar imediatamente cada item informado, preservando quantidade e descrição; não normalizar uma unidade de compra sem autorização.
3. Criar um script Python determinístico em `~/.hermes/scripts/` que leia apenas essa lista, extraia as linhas `- [ ]` e imprima os itens e o total. O script deve permanecer silencioso quando não houver pendências, se esse for o comportamento desejado.
4. Criar o cron com `cronjob_manage(action="create", no_agent=true, script="nome-do-arquivo.py", schedule="59 23 * * *", deliver="origin")` quando o usuário pedir aviso diário às 23:59. Passe somente o nome do script, nunca caminho absoluto, porque o scheduler resolve a partir de `~/.hermes/scripts/`.
5. Verificar o script manualmente e listar o job criado para confirmar `no_agent=true`, horário, destino e `next_run_at`.

**Pitfall:** não use um cron com prompt/LLM para repetir uma lista estática; o modo `no_agent` entrega o stdout do script literalmente, reduz custo, evita reformulação dos itens e mantém o aviso fiel ao arquivo canônico.

**Pitfall:** não misture uma lista de compras de uma casa específica com `TAREFAS.md` ou com listas de outro endereço; separar por local evita que o aviso contenha pendências da pessoa errada.

**Pitfall (marcar item como concluído):** ao concluir um item, MUVA a linha para a seção `## Itens concluídos` como `- [x]` com a data e quem concluiu, atualize o carimbo **Atualizado em** no topo e apague placeholders residuais (ex.: `Nenhum item registrado.`) que tenham ficado dentro da seção de concluídos. O script do cron lê o arquivo cru — item riscado sem ser movido volta a aparecer como pendência aberta, e a seção de concluídos não pode herdar lixo da seção de pendências.
