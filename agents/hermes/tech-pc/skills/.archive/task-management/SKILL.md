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

## Arquivos canônicos

| Arquivo | Propósito |
|---|---|
| `~/MEGA/Documentos/TAREFAS.md` | Fonte da verdade — todas as tarefas com status, agente e links |
| `~/MEGA/Documentos/HUMOR.md` | Registro de humor com intensidade e contexto |

**Nunca criar esses arquivos fora de `~/MEGA/Documentos/`.**

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

### 3. Criar/atualizar HUMOR.md

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
| `java`, `codigo`, `debug` | `java-senior` | `java-senior` |
| `python`, `script`, `automacao` | `python-senior` | `python-senior` |
| `aws`, `cloud`, `oswaldo` | `aws-tutor` | `aws-tutor` |
| `diario`, `registro`, `memoria` | `diario` | `diario` |
| Produto, Discovery | `product-senior` | `product-senior` |
| Tudo o resto | **main** | `main` |

## Padrão: Rafael (relacionamento)

Quando a tarefa envolver Adrielly:

1. Delegar para subagente com o contexto COMPLETO (mensagens literais, datas, histórico)
2. Subagente deve escrever análise em `~/clawd/rafael-reanalise-adrielly-YYYYMMDD.md`
3. Atualizar TAREFAS.md com link para o arquivo

**Regra de ouro:** Igor consulta Rafael antes de qualquer ação com Adrielly. Se ele já interagiu com ela, o Rafael analisa DEPOIS, mas a regra para próximas ações continua valendo.

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
Manter apenas tarefas ativas. Remover itens concluídos com mais de 48h. Usar links para arquivos de detalhe em vez de duplicar informação.

### Rafael precisa do contexto REAL
Adrielly é um tópico sensível. Se o Rafael receber informação incompleta na primeira análise, fazer REANÁLISE com os fatos completos (mensagens literais, status, timing). Nunca manter uma análise baseada em premissas erradas.

### Arquivos de entrega no workspace
Subagentes devem salvar arquivos em `~/clawd/` com nomes descritivos (ex.: `analise-batista-frahlich.md`, `plano-estudos-ia-igor.md`). O main agent depois referencia esses arquivos no TAREFAS.md.

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
