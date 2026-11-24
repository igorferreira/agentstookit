# Prompts prontos por domínio

Exemplos de prompts testados no padrão do repositório. Formato Hermes: `hermes -p <agente> -z "<prompt>"`. Em Claude, invoque o agente e cole o mesmo prompt; em Codex, idem via definição `.toml`.

---

## juridico

**Consulta técnica direta a uma especialidade:**
```
hermes -p juris-tributario -z "Empresa do Simples Nacional recebeu auto de infração por exclusão retroativa do regime. Analise a legalidade da exclusão de ofício, os efeitos sobre os meses já declarados e as vias de defesa administrativa e judicial, com jurisprudência consolidada."
```

**Banca completa (orquestração):**
```
hermes -p juris-master -z "Atue como coordenador da banca. Questão: cancelamento de contrato de software B2B por descumprimento de SLA, com multa de 20% e retenção de dados do cliente. Distribua a análise para as especialidades relevantes (contratos, consumidor, empresarial, LGPD), consolide as posições e emita veredito único com embasamento."
```

**Segunda opinião sobre tese de advogado:**
```
hermes -p juris-processo-civil -z "Meu advogado ajuizou embargos à execução alegando prescrição da dívida ativa. Avalie criticamente a tese, aponte pontos fortes, fragilidades e o que faltou sustentar, e sugira reforço probatório."
```

---

## dev

**Squad completa para uma feature:**
```
hermes -p devsquad-lead -z "Funcionalidade: API REST de contas a pagar com conciliação bancária. Monte o plano da squad (PO, architect, backend, QA), liste os contratos de API, os riscos técnicos e o ordem de implementação. Não escreva código ainda."
```

**Revisão de arquitetura:**
```
hermes -p solution-architect -z "Revise esta arquitetura: [cole o diagrama/descrição]. Foco: escalabilidade em picos 10x, consistência eventual entre pagamentos e notificações, e custo de cloud. Aponte os 3 riscos maiores e a mudança de menor custo com maior ganho."
```

**Code review sênior:**
```
hermes -p java-senior -z "Revise este código como reviewer sênior: [cole o código]. Critério: bugs, concorrência, performance, legibilidade. Uma linha por achado, ordenado por severidade, com correção sugerida."
```

**Diagnóstico de infra:**
```
hermes -p linux-sys -z "Servidor Ubuntu com CPU em 285% e RAM crescendo 250MB a cada 30s. Me dê a sequência exata de comandos de diagnóstico, o que observar em cada um e as hipóteses mais prováveis antes de qualquer ação."
```

---

## saude

> Os agentes de saúde contextualizam e educam — não substituem consulta.

**Interpretar exames:**
```
hermes -p saude-endocrinologista -z "Resultados: TGO 38, TGP 42, LDL 187, HDL 45, testosterona total 612 ng/dL, glicose 92. Interprete cada marcador para um homem de 45 anos em protocolo de recomposição, aponte o que está fora da meta e o que monitorar."
```

**Plano de treino:**
```
hermes -p saude-preparador-fisico -z "Monte periodização de 12 semanas para déficit de gordura preservando massa magra: 4 sessões de musculação/semana + 2 de crossfit + karatê 4x/semana. Deixe os parâmetros (volume, intensidade, progressão) em tabela."
```

**Banca multidisciplinar:**
```
hermes -p saude-master -z "Coordene a banca sobre: colesterol LDL elevado em paciente que prefere abordagem dietética antes de estatina. Peça posições ao nutrólogo, cardiologista e endocrinologista, e consolide um plano de 90 dias com marcos de reavaliação."
```

---

## finance

```
hermes -p finance-senior -z "Minhas saídas fixas mensais são X e a renda Y. Monte o orçamento em 3 potes (fixos, variáveis, reserva), aponte os 3 maiores vazamentos por categoria e a ordem de corte de menor dor para maior dor."
```

```
hermes -p financas-quitacao-dividas -z "Dívidas: [lista com valores, juros e vencimentos]. Ordene por custo efetivo (juros a.m.), calcule o impacto de pagar o mínimo em cada cenário e proponha uma sequência de quitação em 24 meses com valores mês a mês."
```

```
hermes -p finops-ia -z "Analise este consumo de LLM: [token/custo por modelo]. Estime o custo mensal projetado, compare com o custo de assinaturas equivalentes e proponha contenção sem perder capacidade crítica."
```

---

## negocios

```
hermes -p salarios-glassdoor -z "Pesquise a faixa salarial de mercado para Arquiteto de Soluções de IA no RJ com 25 anos de experiência. Traga mediana, p25/p75, e calcule meu gap em relação à mediana."
```

```
hermes -p hr-tech-senior -z "Prepare-me para entrevista técnica com o Head de Engenharia: liste as 10 perguntas mais prováveis dado o contexto da vaga, o que cada uma testa e a estrutura de resposta ideal (método STAR)."
```

```
hermes -p sindico-virtual -z "Monte a pauta de assembleia trimestral: prestação de contas do período, obras pendentes com 3 orçamentos, e inadimplência. Formato de convocação pronto com os itens fundamentados."
```

---

## agentic

```
hermes -p copilot-agent-builder -z "Quero um agente no Microsoft Copilot que triage tickets de suporte por prioridade e sugere resposta baseada na base de conhecimento. Escreva as Instructions (até 8.000 chars), o nome e a configuração de knowledge dentro dos limites da plataforma."
```

```
hermes -p hermes-expert -z "Meu gateway Hermes reclama de conflito de credencial entre dois perfis. Diagnostique as causas possíveis na ordem de probabilidade e o passo a passo de correção sem expor segredos."
```

---

## pesquisas

```
hermes -p celular-doc -z "Comparo [modelo A] x [modelo B] para uso principal: foto de documentos e detalhes de perto. Avalie autofoco de perto, nitidez de texto, scanner nativo e resolução da ultrawide. Veredito único com justificativa."
```

```
hermes -p perfumaria -z "Indique 3 opções de perfume amadeirado para uso diário no escritório nas faixas até R$200, R$400 e acima, com projeção, fixação e onde comprar mais barato."
```

---

## pessoais

```
hermes -p agenda-daily -z "Gere meu briefing do dia: compromissos, aniversários próximos, tarefas vencidas do TAREFAS.md e as 3 prioridades sugeridas para hoje."
```

```
hermes -p diario -z "Registre no diário de hoje: [evento do dia]. Separe fatos de interpretação e proponha 1 lição ou ajuste de comportamento."
```

---

## criativo

```
hermes -p linkedin-post-specialist -z "Escreva um post sobre [tema técnico] para um arquiteto de IA com 26 anos de carreira. Estrutura: gancho nas 2 primeiras linhas, 1 insight contraintuitivo, exemplo concreto, CTA de discussão. Máximo 1.300 caracteres."
```
