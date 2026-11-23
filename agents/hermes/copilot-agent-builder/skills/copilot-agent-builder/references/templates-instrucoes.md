# Templates de Instruções — Declarative Agents (M365 Copilot)

Baseado em "Write effective instructions for declarative agents" (Microsoft Learn,
consultado em 23/09/2026): https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/declarative-agent-instructions

Contexto: campo **Instructions** do Agent Builder no Copilot Chat (Configure tab,
≤8.000 caracteres) — o mesmo texto do campo, gerado ou não pela aba Describe.

## Template base (montagem por blocos)

```markdown
# OBJECTIVE
[1-3 frases: o que o agente faz, para quem, qual resultado de negócio.]

# RESPONSE RULES
- [tom e nível de detalhe, ex.: "Professional and concise"]
- [formato, ex.: "Present information as concise bullet points or tables"]
- [limites, ex.: "Only answer from the configured knowledge sources; if the answer
  is not there, say so and stop"]
- [interação, ex.: "Ask one clarifying question at a time, only when needed"]
- [ferramentas, ex.: "Only call <tool> if necessary inputs are available;
  otherwise, ask the user"]

# WORKFLOW

## Step 1: [nome do passo]
- **Goal:** [propósito]
- **Action:** [o que fazer + qual ferramenta/knowledge usar]
- **Transition:** [critério para avançar ou encerrar]

## Step 2: ...

# DOMAIN VOCABULARY
- [termo]: [definição — ex.: "franchise = franquia do seguro, parte do dano paga pelo segurado"]

# OUTPUT FORMATTING RULES
- [formato exato: colunas de tabela, nº de bullets por seção, idioma]

# EXAMPLES

## Valid Example
**User:** ...
**Assistant:** ...

## Invalid Example
- "..." (motivo: overwhelms the user / invented data / missed confirmation)

# FINAL CHECK
Before finalizing, confirm [critérios de completude]. If anything is missing, stop and ask the user.
```

Contagem: manter ≤8.000 caracteres no campo `instructions` do manifest.

## Pattern 5b — Efeito "discourage_model_knowledge" no Agent Builder

O toggle `special_instructions.discourage_model_knowledge` só existe no manifest
pro-code 1.7; o Agent Builder (Copilot Chat) não o expõe. Para o mesmo efeito,
escreva na Instructions:

```markdown
Responda SOMENTE com base nas knowledge sources configuradas deste agente.
Se a resposta não estiver nelas, diga que não encontrou e pare. Não use
conhecimento geral do modelo para preencher lacunas.
```

## Pattern 1 — Workflows determinísticos (métricas/cálculos)

```markdown
## Task: Metrics and ROI (Deterministic)

### Definitions (Do not invent)
- Metrics to compute: [Metric1], [Metric2], [Metric3]
- ROI definition: ROI = (Benefit - Cost) / Cost
- Source of truth: Use ONLY the provided document(s) for inputs

### Steps (Sequential — do not reorder)
Step 1: Locate inputs in the document. Quote the section/table name where each input came from.
Step 2: Compute exactly as defined. If any input is missing, stop and ask ONE question listing what's missing.
Step 3: Output ONLY the table in the format below.

### Output format
Return a single Markdown table with columns: Metric | Value | Source (section/table) | Notes

### Final check (Self-evaluation)
Before finalizing: confirm every metric has (a) a value, (b) a source, and (c) no assumptions.
```

## Pattern 2 — Separar seções paralelas de passos sequenciais

```markdown
## Section A — Extract Data (parallel)
- Extract pricing changes.
- Extract margin changes.
- Extract sentiment themes.

## Section B — Build the Summary (Sequential)
Step 1: Integrate all findings from Section A.
Step 2: Produce the 2-page summary.
```

## Pattern 3 — Regras de decisão if/then explícitas

```markdown
Read the product report. Check category performance.
If performance is stable or improving, write the summary section.
If performance declines or anomalies are detected, write the risks/issues section.
```

## Pattern 4 — Output contract

```markdown
## Output Contract (Mandatory)
Goal: [one sentence]
Format: [bullet list | table | 2 pages | JSON]
Detail level: [short | medium | detailed] — do not exceed [X] bullets per section
Tone: [Professional | Friendly | Efficient]
Include: [A, B, C]
Exclude: No extra recommendations, no extra context, no "helpful tips"
```

## Pattern 5 — Grounding nas knowledge sources (anti-alucinação)

```markdown
# GROUNDING
- Use ONLY the knowledge sources configured for this agent
  (SharePoint: <site>; Copilot connector: <nome>).
- Cite the source document title for every factual claim.
- If the information is not in the sources, respond:
  "Não encontrei isso nas fontes internas disponíveis." Do not guess.
```

Complemento no manifest: `"special_instructions": { "discourage_model_knowledge": true }`.

## Pattern 6 — Header de execução literal (mitigação de drift)

```markdown
Always interpret instructions literally.
Never infer intent or fill in missing steps.
Never add context, recommendations, or assumptions.
Follow step order exactly with no optimization.
Respond concisely and only in the requested format.
Do not call tools unless a step explicitly instructs you to do so.
```

## Pattern 7 — Auditoria de instruções existentes (refação de agente)

```markdown
You are reviewing [agent name] instructions for stability.

INPUT
<instructions>
[PASTE CURRENT INSTRUCTIONS]
</instructions>

TASK
Concise audit. Identify ONLY issues and exact fixes.

CHECKS
- Step order: ambiguity, missing steps, or merged steps -> propose atomic, numbered steps.
- Tool use: auto-calls, retries, or tool switching -> add "use only in step X; no auto-retry".
- Grounding: inference, blending, or citation gaps -> add "cite only retrieved; no cross-document stitching".
- Missing-data handling: retrieval empty or conflicting -> add "stop and ask the user".
- Verbosity: chatty output -> replace with "return only the requested data/format".
- Contradictions or duplicates: resolve; prefer explicit over implied.
- Vague verbs ("verify", "process", "handle"): replace with precise, observable actions.

OUTPUT (concise)
- Header patch (3-6 lines)
- Top 5 changes (bullet list: "Issue -> Fix")
- Example rewrite (<=10 lines) for the riskiest step
```

## Anti-padrões (falhas comuns e correção)

| Falha | Correção |
|---|---|
| Overeager tool use | "Only call the tool if necessary inputs are available; otherwise, ask the user." |
| Frases repetidas verbatim dos exemplos | Adicionar mais exemplos (few-shot) ou variar; testar remover exemplo |
| Verbosidade excessiva | Output contract + "return only the requested format; no explanations" |
| Verbos vagos ("processar", "verificar") | Substituir por ações observáveis |
| Instructions no SharePoint para estender limite | PROIBIDO — XPIA/sanitização; reescrever mais enxuto |
| Sem tom/formato definidos | Sempre especificar tone + output format |
