# Decifra Bravo — Dicionário Técnico de Freela

## When to Use

Use when Igor receives truncated/cryptic messages from his friend Wallace "Bravo" Resende (architect + superintendente de obras) about freelance work. This skill provides a dictionary of construction/architecture/IT jargon terms to decode what Bravo really means, identify gaps, and generate clarifying questions.

## How It Works

When the `freelance-bravo` agent receives a message from Bravo:
1. Scan for technical terms in the diction below
2. For each found term: note probable meaning + gap + question generator
3. Never assume — always mark as "PENDENTE DE CONFIRMAÇÃO"

---

## Dictionary of Terms and Abbreviations

### Architecture / Projects

| Term/Abbr | Probable Meaning | Typical Gap | Question Generator |
|-----------|-----------------|-------------|-------------------|
| **PL** | Projeto Legal / Prefeitura | Detail level required by local municipality | "Pra qual município? Tem modelo próprio?" |
| **PEX** | Projeto Executivo | Material/end details, MEP integration | "Inclui todas especialidades ou só arquitetura?" |
| **MEMÓRIA / MC** | Memória de Cálculo | Applicable standard (specific NBR) | "Qual NBR rege? 13528? 6494?" |
| **LAUDO** | Technical / Forensic Report | Exact object (structural, foundation?) | "É pra quê? Estrutura? Vedação?" |
| **MN** | Memorial Descritivo | Scope completeness of services/materials | "Cobre tudo ou partes específicas?" |
| **LOD** | Level of Development (BIM) | LOD 100-400 geometric+information detail | "Qual LOD? 200? 300?" |
| **PGRCC** | Construction Waste Management Plan | Estimated tons, disposal site | "Quantas tn de RCC? Aterro aprovado?" |
| **AVCB** | Fire Department Inspection Certificate | Building type, risk class | "Comercial? Residencial? Classe de risco?" |
| **Habite-se** | Occupancy Completion Certificate | Current phase (ready? pending items?) | "Vistoria prévia ou direto no Habite-se?" |

### Superintendência de Obras

| Term/Abbr | Probable Meaning | Typical Gap | Question Generator |
|-----------|-----------------|-------------|-------------------|
| **CPF** | Cronograma Físico-Financeiro | Period, total value, installments | "Valor total? Prazo? Quero ver contrato." |
| **CRS** | Controle de Resultado/Serviços | What's being controlled? | "De quê? Andares? Edições?" |
| **DFI** | Diários de Obra | Format (spreadsheet, system?) | "Planilha Excel ou sistema?" |
| **RGI** | Relatório Geral / Avanço | Frequency, format | "% avanço semanal ou relatório?" |
| **FISICO-FINANCEIRO** | Physical performance vs cash outflow | S-curve, monthly targets | "Gerar curva S ou consolidar existente?" |
| **QTO** | Quantitativo | Base (drawing, BIM, memory?) | "Baseado em planta ou BIM?" |
| **ESPECIFICAÇÃO** | Materials / Services Specification | Scope (all disciplines?) | "Qual parte? Arquitetura? Elétrica?" |
| **REUNIÃO** | Site Meeting Minutes | Standard format, recurring agendas | "Plano de ata pronto ou montar do zero?" |
| **CronoEng** | CrontoEng software | Version, modules | "Qual versão?" |
| **ORSE** | ORSE-based estimate spreadsheet | Items, price composition | "Baseado em SINAPI? Tabela regional?" |

### BIM / 3D Modeling

| Term/Abbr | Probable Meaning | Typical Gap | Question Generator |
|-----------|-----------------|-------------|-------------------|
| **CLASH DETECTION** | Interference/collision detection | Standards (ISO 19650?) | "Entre quais disciplinas? AR+STR+EMP?" |
| **COORDENAÇÃO BIM** | Multi-model coordination | Bim Collaborator, Navisworks, federated? | "Federado ou juntar arquivos?" |
| **REVIT** | Autodesk Revit software | Version, custom families ready? | "Qual versão? Famílias prontas?" |
| **LAYOUTS** | Spatial layout/planting plans | Total area, room count | "Quantos ambientes? Área total?" |
| **FAMÍLIA REVIT** | Custom Revit family | Parameterized? Generic? | "Parametrizada ou genérica?" |
| **NAVISHOWS** | Autodesk Navisworks | 4D schedule simulation, coordination | "Simulação 4D ou só Clash?" |
| **BEP** | BIM Execution Plan | Detail levels, responsibilities | "Já tem BEP ou criar?" |

### IT / Digital Management (in construction)

| Term/Abbr | Probable Meaning | Typical Gap | Question Generator |
|-----------|-----------------|-------------|-------------------|
| **KPI** | Key Performance Indicator | Which ones? Dashboard? Update frequency? | "Quais KPIs? Quantidade?" |
| **Dashboard** | Visual metrics panel | Tool (Excel, Power BI, web?) | "Excel, Power BI ou online?" |
| **Fluxo Caixa** | Project revenue/expenses control | Forecast or historical? | "Prognóstico ou histórico?" |
| **ERP** | Management system (Protheus, Totvs etc.) | Integrate or export data? | "Integrar ou exportar dados?" |
| **SIGA** | Construction management software | Specific module | "SIGA Obras? Qual módulo?" |

### Documents / Deliverables

| Term/Abbr | Probable Meaning | Typical Gap | Question Generator |
|-----------|-----------------|-------------|-------------------|
| **PDF/A** | Long-term archival PDF | Can it be scanned image? | "PDF comum ou arquivo?" |
| **EDITÁVEL** | Editable file (DOCX, XLSX, RVT) | File format expected | "Que formato editável?" |
| **FEEDBACK LOOP** | Review rounds | How many rounds included? | "Quantas rodadas de revisão?" |
| **PROPOSTA COMERCIAL** | Commercial proposal/budget | Generate or paste info? | "Gerar proposta ou colar info?" |
| **Contratual** | Contract-bound/CNPJ-linked | Which contract number? | "Qual contrato/número?" |

---

## Validation Checklist Before Generating Questions

Before finalizing the question list for Igor to send to Bravo, verify:

1. [ ] All explicit numbers/deadlines captured
2. [ ] All mentioned documents (or implied) identified
3. [ ] Gaps mapped as PENDENTES
4. [ ] No assumption made without clear flagging
5. [ ] Questions numbered and prioritized
6. [ ] Max 10 questions per round (split into batches if >10)
7. [ ] Natural response template ready if requested

---

## Example Complete Flow

### Message from Bravo:
> "mano, precisava da memoria daquele projeto lá, pra prefeito, urgente, ta pedindo pra semana que vem"

### Analysis:
```
ENTENDI QUE ELE QUER:
→ Memória de Cálculo para submeter à prefeitura de um projeto existente
→ Urgente: prazo ~1 semana

LACUNAS:
→ Qual projeto exatamente? (endereço/número do processo)
→ Tipo de edificação? (comercial/residencial/misto)
→ Qual prefeitura?
→ Qual NBR base?
→ Já existe material anterior?
→ Formato de entrega?

PERGUNTAS PRA BRABO:
─────────────────────
1. De qual projeto é a memória? Endereço ou número do processo?
2. É residencial, comercial ou misto?
3. Pra qual prefeitura/submissão?
4. Já existe memória parcial ou é do zero?
5. Precisa seguir template específico da prefeitura?
```

---

## Important Rules

- Always load this skill before analyzing any message from Bravo
- When a term is NOT in the dictionary, mark as "TERMO NÃO MAPEADO → pedir esclarecimento ao Bravo"
- If more than 5 unknown terms appear in one message, flag that a personal glossary might be worth maintaining
- Maintain ~/MEGA/Documentos/freelance_bravo/DICIONARIO-CRESCENT.md with newly discovered terms added here over time
