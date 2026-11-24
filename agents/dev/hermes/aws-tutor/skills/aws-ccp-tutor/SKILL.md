---
name: aws-ccp-tutor
description: Teaches and quizzes AWS Cloud Practitioner exam content.
version: 1.0.0
author: Usuário
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Education, AWS, Certification, Cloud, Exam Prep]
    related_skills: [memento-flashcards]
    category: education
---

# AWS CCP Tutor Skill

Ensina e avalia o conteúdo oficial da certificação **AWS Certified Cloud Practitioner (CLF-C02)**, seguindo fielmente os 4 domínios e task statements do exam guide da AWS. Não ensina arquitetura ou implementação além do que o exame cobre — CCP é conhecimento geral, não hands-on.

Esta skill cuida do **conteúdo e da avaliação**. O agendamento de revisão espaçada é delegado à skill `memento-flashcards` (já instalada neste perfil) — não duplique lógica de repetição espaçada aqui.

## When to Use

Use esta skill quando Usuário:
- Pedir para aprender/revisar um domínio ou tópico da AWS CCP
- Pedir um simulado, prova, ou questões de múltipla escolha sobre AWS
- Perguntar sobre seu progresso/prontidão para o exame
- Perguntar se um serviço AWS específico cai na prova CLF-C02

Não use para dúvidas de arquitetura/implementação real de sistemas AWS (isso é fora do escopo do CCP) — nesse caso, avise que é conteúdo além do que o exame cobre, mas pode responder se ele quiser mesmo assim.

## Prerequisites

Nenhuma chave de API necessária. O conteúdo do exame vem de `references/clf-c02-exam-guide.md` e `references/clf-c02-service-scope.md`, coletados do exam guide oficial da AWS. A skill `memento-flashcards` (`terminal`) é usada para armazenar flashcards.

## Quick Reference

| Intenção de Usuário | Ação |
|---|---|
| "me ensina o domínio X" / "explica IAM" / "o que é shared responsibility" | **Modo Aula** |
| "faz um simulado" / "quero 20 questões" / "me testa" | **Modo Simulado** |
| "revisa comigo" / "quais cards estão pendentes" | **Modo Revisão** (delega ao Memento) |
| "como tá meu progresso" / "tô pronto pro exame?" | **Modo Progresso** |
| "X cai na prova?" | Consultar `clf-c02-service-scope.md` e responder objetivamente |

## Procedure

### Modo Aula

1. Identifique o domínio/task statement relevante em `references/clf-c02-exam-guide.md`. Se Usuário não especificar, pergunte qual domínio ele quer (ou sugira o mais fraco via `track_progress.py weak`).
2. Explique o conceito citando o Task Statement (ex: "Task Statement 2.3 — Identify AWS access management capabilities"). Use exemplos concretos, mas só com serviços listados em `clf-c02-service-scope.md` como em-escopo.
3. Ao fechar o conceito, gere 2-3 flashcards Q/A cobrindo os pontos-chave e grave via Memento:
   ```bash
   python3 ~/.hermes/profiles/aws-tutor/skills/productivity/memento-flashcards/scripts/memento_cards.py add \
     --question "..." --answer "..." --collection "CLF-C02 - D2 Security"
   ```
   Convenção de collection (uma por domínio): `CLF-C02 - D1 Cloud Concepts`, `CLF-C02 - D2 Security`, `CLF-C02 - D3 Technology`, `CLF-C02 - D4 Billing`.
4. Registre a sessão como uma "lesson" no progresso (mesmo sem nota, para refletir cobertura):
   ```bash
   python3 ~/.hermes/profiles/aws-tutor/skills/aws-ccp-tutor/scripts/track_progress.py record --domain D2 --correct 1 --total 1 --source lesson
   ```
   (1/1 aqui é só um marcador de "domínio tocado", não uma nota real — a nota de verdade vem do Modo Simulado.)

### Modo Simulado

1. Pergunte quantas questões (padrão: 20 se Usuário não especificar; 65 para simulado completo).
2. Distribua as questões pela proporção oficial dos domínios: **D1 24% · D2 30% · D3 34% · D4 12%** (arredonde mantendo o total exato).
3. Gere as questões você mesmo (você é o LLM), baseado SOMENTE nos Task Statements de `clf-c02-exam-guide.md` e nos serviços em-escopo de `clf-c02-service-scope.md`. Regras de formato, iguais ao exame real:
   - Misture **multiple choice** (1 certa + 3 distratores plausíveis) e **multiple response** (2+ certas entre 5+ opções) — não faça só múltipla escolha simples.
   - Distratores devem ser plausíveis (erros comuns), não absurdos óbvios.
   - Não use serviços fora de escopo como opção de resposta.
4. Apresente uma questão por vez, espere a resposta de Usuário antes de mostrar a próxima. Não revele a resposta certa antes dele responder.
5. Ao final, corrija tudo, mostre nota por domínio, e:
   - Registre o resultado real por domínio:
     ```bash
     python3 ~/.hermes/profiles/aws-tutor/skills/aws-ccp-tutor/scripts/track_progress.py record --domain D2 --correct 4 --total 6 --source quiz
     ```
   - Para cada questão errada, crie um flashcard no Memento (collection do domínio correspondente) cobrindo o conceito que faltou.

### Modo Revisão

Delegue ao fluxo de revisão do Memento (ver `SKILL.md` do `memento-flashcards` para o protocolo exato de grading em texto livre):
```bash
python3 ~/.hermes/profiles/aws-tutor/skills/productivity/memento-flashcards/scripts/memento_cards.py due --collection "CLF-C02 - D1 Cloud Concepts"
# ou sem --collection para revisar todos os domínios CLF-C02 juntos
```
Depois da revisão, mostre um resumo com `memento_cards.py stats` (filtrando mentalmente pelas 4 collections CLF-C02).

### Modo Progresso

```bash
python3 ~/.hermes/profiles/aws-tutor/skills/aws-ccp-tutor/scripts/track_progress.py stats
python3 ~/.hermes/profiles/aws-tutor/skills/aws-ccp-tutor/scripts/track_progress.py weak
```
Apresente: % de acerto por domínio, comparado ao peso do domínio na prova. Domínios com **peso alto e acerto baixo** (ex: Security 30%) são prioridade máxima — use `weak` (que já pondera peso × lacuna) para ordenar a recomendação. Dê uma leitura honesta de prontidão (ex: "geral 72%, mas isso não é a nota oficial — é só um sinal"), nunca prometa que ele vai passar.

## Pitfalls

- **Nunca invente serviço, preço ou comportamento.** Se não está em `references/`, diga que não tem certeza.
- **Não confunda Region com Availability Zone** — erro clássico de quem está estudando; enfatize isso ao ensinar 3.2.
- **Modelo de nota é compensatório** — não é preciso "passar" em cada domínio, só na média geral (700/1000).
- **Serviços fora de escopo não viram questão de simulado.** Confira sempre contra `clf-c02-service-scope.md` antes de usar um serviço numa questão nova.
- **`progress.json` e `cards.json` nunca devem ser editados à mão** — sempre via os scripts (atomic write).

## Verification

```bash
python3 ~/.hermes/profiles/aws-tutor/skills/aws-ccp-tutor/scripts/track_progress.py record --domain D1 --correct 1 --total 1 --source lesson
python3 ~/.hermes/profiles/aws-tutor/skills/aws-ccp-tutor/scripts/track_progress.py stats
python3 ~/.hermes/profiles/aws-tutor/skills/aws-ccp-tutor/scripts/track_progress.py weak
```
Confirme que `stats` reflete o registro e que `weak` ordena por prioridade (peso × lacuna) coerente com os domínios ainda não tocados.
