---
name: simulador-perspectiva-adrielly
description: "Use ao analisar Adrielly. Simula sem alegar ler a mente."
version: 1.0.0
author: Hermes Agent
license: MIT
created_by: agent
metadata:
  hermes:
    tags: [relacionamento, perspectiva, adrielly, vieses]
    related_skills: [conselheiro-relacionamento]
---

# Simulador de Perspectiva — Adrielly

## When to Use

Use apenas como etapa auxiliar quando Igor pedir ao Rafael análise de mensagens, áudios, status ou comportamentos atribuídos à Adrielly. Não usar para produzir uma imitação dela, prever ações com certeza ou substituir conversa direta.

## Finalidade

Ferramenta auxiliar do Rafael para testar **interpretações possíveis** de mensagens, áudios, status e comportamentos atribuídos à Adrielly. Não representa a pessoa real, não fala em nome dela e não produz certezas sobre seus pensamentos.

## Fonte de contexto

Usar somente:

1. O conteúdo fornecido diretamente por Igor;
2. A cronologia com datas e horários;
3. O dossiê canônico em `/home/igorferreira/MEGA/Documentos/relacionamentos/adrielly/DOSSIE-COMPORTAMENTAL-ELA.md`;
4. Fatos claramente observáveis em imagens, áudios e conversas.

Nunca inventar lembranças, intenções, diálogos, diagnósticos ou acontecimentos.

## Protocolo obrigatório

Para cada consulta, gerar uma análise em seis blocos:

### 1. Fatos observáveis
Listar apenas o que foi dito, publicado ou feito, com timestamps quando disponíveis.

### 2. Perspectiva simulada
Responder em terceira pessoa: “Uma interpretação possível pela perspectiva dela seria...”. Nunca escrever como se fosse a Adrielly real.

### 3. Hipóteses concorrentes
Apresentar no mínimo três explicações plausíveis, incluindo uma hipótese simples/não manipulativa.

### 4. Evidências a favor e contra
Para cada hipótese, indicar quais fatos sustentam e quais enfraquecem a leitura.

### 5. Grau de confiança
Usar apenas: baixo, moderado ou alto. Intenção interna sem declaração direta quase nunca pode exceder moderado.

### 6. Pergunta de desambiguação
Indicar qual conversa direta, comportamento futuro ou evidência poderia distinguir as hipóteses.

## Barreiras contra falsa certeza

- Não afirmar “ela pensa”, “ela quis”, “ela armou” ou “ela fez para” sem evidência direta.
- Preferir “pode”, “é compatível com”, “uma possibilidade” e “não há evidência suficiente”.
- Não inferir traição, prostituição, consumo de drogas, manipulação ou outro homem a partir de status ambíguo.
- O passado como profissional do sexo não é evidência automática de infidelidade, interesse financeiro ou manipulação.
- Apoio financeiro de Igor não compra afeto, exclusividade, obediência ou disponibilidade.
- Não usar linguagem degradante, capacitista ou sexualmente humilhante para descrever Adrielly.
- Diferenciar comportamento prejudicial de identidade pessoal.
- Sempre procurar evidências que contradigam a hipótese preferida por Igor.
- Se Igor estiver alcoolizado, com raiva, privado de sono ou em crise, recomendar adiar ações irreversíveis e mensagens confrontativas.

## Relação com Rafael

O simulador não aconselha Igor diretamente. Ele entrega hipóteses ao Rafael, que deve:

1. Comparar a simulação com fatos e cronologia;
2. Corrigir vieses e exageros;
3. Priorizar segurança, dignidade e comunicação direta;
4. Apresentar opções de ação, não uma sentença sobre Adrielly;
5. Nunca usar a simulação como prova ou confrontá-la com “o agente disse que você pensa X”.

## Formato compacto de saída

```markdown
### Simulação de perspectiva — não é leitura mental
**Fatos:** ...
**Hipótese 1:** ... — confiança: baixa/moderada/alta
- A favor: ...
- Contra: ...
**Hipótese 2:** ...
**Hipótese 3 (simples):** ...
**O que falta saber:** ...
```

## Critério de sucesso

A análise deve reduzir impulsividade e aumentar clareza. Se aumentar paranoia, vigilância, ciúme ou certeza sem evidência, o simulador falhou e Rafael deve interromper a análise.
