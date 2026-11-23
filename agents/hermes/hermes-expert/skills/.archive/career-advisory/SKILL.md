---
name: career-advisory
description: "Use for career strategy, résumé/CV and LinkedIn reviews, professional positioning, seniority calibration, job transitions, promotion cases, and compensation or interview preparation."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [career, linkedin, resume, cv, positioning, promotion, compensation, interviews]
    related_skills: [humanizer, ocr-and-documents]
    created_by: agent
---

# Career Advisory

## Overview

Use this class-level skill to help a professional understand and improve their career narrative, market positioning, résumé/CV, LinkedIn profile, promotion case, interview story, or transition plan. Favor evidence-based, practical recommendations over generic motivational advice.

## Trigger conditions

Use when the user asks about:

- career direction, next role, promotion, or transition;
- résumé/CV or LinkedIn review;
- headline, About/Summary, experience descriptions, or portfolio positioning;
- seniority calibration (senior, staff, principal, architect, manager, executive);
- compensation, negotiation, interviews, or recruiter visibility;
- financial preparation for resignation, dismissal, or changing jobs, including CLT termination scenarios and runway;
- reconciling consulting, outsourcing, client assignment, and legal employer relationships.

## Intake: establish the target before rewriting

Collect or infer only what is necessary:

1. Current role and actual scope.
2. Legal employer, client/project assignment, and employment model.
3. Years and domains of experience.
4. Target role, timeline, geography, language, and work model.
5. Concrete outcomes: revenue, cost, latency, reliability, adoption, team size, risk reduction, delivery speed, or governance impact.
6. Constraints: confidentiality, non-disclosure, employment sensitivity, or public-profile visibility.

If the user provides a public LinkedIn identifier, normalize it to `https://www.linkedin.com/in/<id>` and verify that the visible name/company match before analyzing.

## Evidence hierarchy

Use this order:

1. User-provided résumé/PDF or exported LinkedIn profile.
2. User-provided facts and corrections.
3. Public profile content visible without authentication.
4. Search snippets or third-party mirrors only as weak corroboration.

Never invent hidden experience details, dates, achievements, certifications, or metrics. Clearly separate:

- **Observed on profile/document**
- **Provided by the user**
- **Recommendation/inference**

## LinkedIn and résumé review workflow

1. Verify identity and profile URL.
2. **Preferred data source:** When the user can provide a LinkedIn data export ZIP (Settings → Data Privacy), use that over browser/public-view scraping — it contains full experience history, skills, saved jobs, company follows, and job preferences that the public profile hides. See [`references/linkedin-data-export-analysis.md`](references/linkedin-data-export-analysis.md).
3. If only the public URL is available: capture the visible headline, About/Summary, current company, services, experience, education, certifications, recommendations, and recent topical activity.
3. State access limitations early. LinkedIn often hides complete experience behind login; request the exported PDF or screenshots for a full review.
4. **What IS visible without login on a typical LinkedIn public profile:**
   - Name, headline (often truncated), location, current company name, follower/connection count
   - About/Summary (truncated — first ~2 lines only)
   - Services listed
   - Recent activity (posts liked/shared, not full text)
   - First entry of "Experience & Education" section (company name only, no dates/description)
   - Certifications and licenses (full list usually visible)
   - Languages
   - Recommendations text (partially visible)
   - "Other people named X" sidebar
5. **What is NOT visible without login:** full experience history (dates, descriptions, prior roles), full About text, skills endorsements, featured content, contact info, education details.
6. Compare the profile against user-provided facts and session history:
   - years of experience; current title and scope; current technical domain; employer/client relationship; outdated services, keywords, or certifications.
7. Identify the highest-impact gaps first; do not bury the main issue under cosmetic edits.
8. Draft improvements in this order: headline → first 2–3 lines of About → full About → current-role description → selected prior roles → skills/services → activity/content strategy.
9. Tie recommendations to a target outcome.

See [`references/linkedin-public-profile-review.md`](references/linkedin-public-profile-review.md) for the browser/public-view procedure and common access limitations. For the complete LinkedIn data export ZIP workflow (22 CSV files, priority order, gap analysis framework, bilingual rewrite output), see [`references/linkedin-data-export-analysis.md`](references/linkedin-data-export-analysis.md). For CV generation toolchain (pandoc/wkhtmltopdf commands, folder structure, segmentation rules) see [`references/cv-generation-toolchain.md`](references/cv-generation-toolchain.md). For CLT termination calculation pitfalls see [`references/clt-rescisao-pitfalls.md`](references/clt-rescisao-pitfalls.md). For salary market data Brazil 2026 see [`references/salary-market-brazil-2026.md`](references/salary-market-brazil-2026.md). For candidate referral workflow (email structure, formal indication, CC rules, Noorden-specific) see [`references/candidate-referral-workflow.md`](references/candidate-referral-workflow.md).

## Employer versus client assignment

When a professional is employed by a consultancy/vendor but works at a client:

- Do not imply direct employment by the client unless that is true.
- Prefer a transparent structure such as:
  - `Employer — Role (consultant assigned to Client)`; or
  - `Role | Employer — project/assignment at Client`.
- Preserve the client's strategic value without misrepresenting the contract.
- Ask whether confidentiality or contract terms restrict naming the client.
- Keep dates aligned with the legal employer record and explain overlapping assignments when needed.

## Senior technical-career positioning

For professionals with long experience, avoid reducing the narrative to an old implementation stack. Emphasize current scope and durable leverage:

- architecture and decision quality;
- business and risk outcomes;
- modernization and integration;
- governance, security, and reliability;
- mentoring, standards, and technical influence;
- cross-functional stakeholder leadership;
- adoption of new capabilities such as AI, cloud, data, or platform engineering.

Legacy certifications and technologies can demonstrate depth, but they should support—not dominate—the current narrative.

### Technical System Design & Distributed Architecture Preparation
When preparing senior candidates (Architect, Staff/Principal Engineer, Senior Backend) for high-scale system design and distributed systems interview questions (e.g. payment APIs at 100k req/min, concurrent processing, exactly-once vs at-most-once semantics, idempotency):
- Always structure the answer around core distributed systems concepts: **Idempotency Keys**, **Atomic Locking / Unique Constraints in DB**, **State Machines**, **External Gateway Key Propagation**, and **Transactional Outbox Pattern / Reconciliation**.
- Emphasize why naive approaches fail (local ACID transactions don't rollback external HTTP network side-effects; Redis cache lacks durable write guarantees across network partitions; TOCTOU race conditions occur when checking status before processing).
- Format study notes with clear visual sequence diagrams (Mermaid) and 1-minute executive interview summaries. Save distributed systems and system design interview questions in `~/MEGA/Documentos/carreira/estudos/` and `~/MEGA/Documentos/educacao_leitura/estudos/`.

### AI Systems, Context Engineering & Multi-Agent Architecture Preparation (2026+)
When preparing senior candidates (AI Solutions Architect, Principal AI Engineer) for interviews and positioning on modern AI engineering:
- **Core Curricula / Benchmarks:**
  - *Anthropic Official Engineering Principles:* XML context tags, strict task boundary delimitation, response prefilling for deterministic JSON/code, Context Window hygiene (avoiding log dumping), and Harness & Loop Engineering.
  - *Google AI Engineering Patterns:* Transition from simple linear ReAct/DAG pipelines to **Graph Engineering (LangGraph / StateGraph)** with cyclic feedback loops, conditional edges, supervisor/router topologies, and Human-in-the-Loop checkpoints.
- Study artifacts and references should be mirrored across `~/MEGA/Documentos/educacao_leitura/estudos/`, `~/MEGA/Documentos/carreira/estudos/` and `~/projetos/hdi/Arquitetura/referencias/`.

## Career-transition financial readiness

When the user is preparing for a possible resignation, dismissal, or employer change:

1. Treat financial readiness as part of the career decision, not as a separate motivational aside.
2. Compare scenarios side by side and distinguish immediately accessible cash from conditional or blocked values.
3. Maintain separate ledgers for employment-law remuneration and personal disposable resources. A benefit may count toward current living-expense capacity without entering salary, FGTS, vacation, 13th salary, or termination bases; preserve date, recurrence, restrictions, payroll treatment, and evidence. When the user explicitly confirms the benefit is excluded from their termination model, treat that as a **permanent planning rule** and do not revisit it with speculative reclassification caveats — not even when the benefit coincides with a payroll event such as the 13th salary. For Igor specifically: VALLO BENEFÍCIOS (and any deposit that accompanies the 13th salary) is excluded from all termination calculations by explicit user directive.
4. Ask for exact contract, vacation, FGTS, and current-remuneration data rather than inventing a precise estimate.
5. Normalize employment history before calculating: effective amended start date versus earlier communicated date, admission role versus current role, and initial/proposed salary versus current salary.
6. Preserve evidence provenance—original document, user transcription, or inference—and keep unresolved fields null.
7. Convert the conservative accessible total into months of the user's stated net cost of living.
8. Use current official legal and tax sources and label all outputs as planning estimates, not guaranteed TRCT values.
9. For recurring analysis, use stable structured input, deterministic calculations, monthly reports, and explicit missing-data gates.
10. When payroll evidence is stored in email or document archives, save the questionnaire and source first, verify authorization before claiming access, request the narrowest needed access, and preserve message/document provenance without modifying the mailbox.

### FGTS: saque-aniversário vs saque-rescisão (critical distinction)
Always verify the FGTS modality from the actual Caixa statement before projecting saque value:
- **Saldo bloqueado** = antecipação de saque-aniversário active → worker does NOT receive that saldo on dismissal, only receives multa 40% + the small **saldo disponível** (total − bloqueado).
- Signs in the statement: `SAQUE JAM - COD 60` or `SAQUE DEP - COD 60` entries confirm saque-aniversário is active.
- **Never project saldo total as sacável** without first checking for a bloqueio entry.
- Scenario label: use "dispensa + FGTS disponível" (not "saldo FGTS") to avoid the confusion.
- Retorno to saque-rescisão requires cancellation with 24-month wait — note this in every scenario table.

See [`references/clt-transition-financial-planning.md`](references/clt-transition-financial-planning.md) for the scenario model, data intake, payroll-evidence workflow, automation pattern, edge cases, and official sources.

For mailbox-to-report implementation details—message manifests, deterministic PDF extraction, salary normalization, split-vacation reconstruction, CCT auditing, FGTS reconstruction, scenario separation, and repository/cron relocation—see [`references/payroll-evidence-extraction-and-audit.md`](references/payroll-evidence-extraction-and-audit.md).

## User-specific execution preference

For Igor, break substantive career work into small tasks, execute them sequentially one at a time, and close with a report listing work performed, files changed, hypotheses, missing data, and next steps. Do not merely present a plan when the tools can complete the work now.

**CV format preferences (Igor):**
- Always generate **3 formats per CV**: `.md` (source), `.docx`, `.pdf`. Use `pandoc` for DOCX and `pandoc` → HTML → `wkhtmltopdf` for PDF.
- **Resumido = 2 pages**, not 1. Igor is senior (26 years). Rule: last 5 companies with full descriptions + prior experience (2005–2013) collapsed into one compact paragraph.
- **Completo = full history** from first job (2005) with each company individually listed.
- When segmenting by target role, generate **4 areas × 2 sizes = 8 MDs + 8 DOCX + 8 PDF**. Areas: Arquiteto IA, Java Sênior, Open Finance, Seguros.
- Before generating from LinkedIn, always check `/home/igorferreira/MEGA/Documentos/cv/Igor_Ferreira/` — Igor keeps existing CV versions there. Use the most complete source found (typically `Fonte_Editavel/` + `ATUAL/CV_*_ATS_Optimized_pt.md`).
- Output folder: `/home/igorferreira/MEGA/Documentos/carreira/curriculos/` with area subfolders.
- Ask for approval of the segmentation plan **before** generating all files.

For long evidence-processing or calculation runs, do not go silent: send a brief progress update after each major phase (collection, extraction, normalization, calculation, verification). If the conversation is interrupted or compacted, resume from the active task and explicitly state the current phase instead of restarting or making Igor ask whether work is continuing.

## Salary market research workflow (Igor)

When Igor asks for salary market research or positioning vs market:

1. Research **all 4 profiles simultaneously** using `delegate_task` with 2 tasks of 2 profiles each (max 3 concurrent children; splitting into 2 avoids the limit).
2. Sources to use in priority order: Robert Half Guia Salarial, Glassdoor BR, Indeed BR, LinkedIn Jobs, Portal Salário (CAGED), Código Fonte TV annual survey, HUNT IT, JobRise.
3. Return for each profile: CLT faixa (P25/P50/P90/teto), PJ equivalente, valor hora PJ, vagas abertas estimadas, hub geográfico, principais contratantes.
4. Save research to `/home/igorferreira/MEGA/Documentos/carreira/mercado-salarial/pesquisas/AAAA-MM_GLASSDOOR-4-PERFIS.md`.
5. Then generate `evolucao/AAAA-MM-DD_ADERENCIA-SALARIAL-POSICIONAMENTO.md` with the vendor margin analysis (see below).

### Vendor margin analysis (Noorden/HDI model)

When the user mentions a client billing rate:
- **Custo total CLT** = salário bruto × 1.65 (fator encargos patronais: FGTS 8% + provisões 13º + férias + encargos sociais)
- **Margem da consultoria** = receita cliente − custo total CLT
- **Valor hora para o cliente** = receita mensal ÷ 160h
- **Valor hora bruto do trabalhador** = salário bruto ÷ 160h
- Present these numbers plainly — the worker's leverage in salary negotiation comes from knowing the margin
- Save as part of the aderência file, not as a separate document

### Salary negotiation analysis

When Igor asks "should I ask for a raise?":
1. State verdict first (yes/no/timing).
2. List concrete arguments (role mismatch, market gap, vendor margin room).
3. List risks (job loss timing, debt situation, contract renewal sensitivity).
4. Give 3 scenarios: conservador, justo, ideal — with specific R$ targets and minimum acceptable.
5. Give exact timing recommendation based on current financial situation.
6. Save to `evolucao/AAAA-MM-DD_PROPOSTA-AUMENTO-ANALISE.md`.

### Debt strategy analysis

When Igor asks for a debt payment strategy:
1. Calculate: margem mensal = renda disponível − custo de vida; prazo sem evento de liquidez = dívida ÷ margem.
2. If prazo > 24 months: "inviável sem evento de liquidez" — identify the available events (home equity, aumento, 13º, rescisão).
3. For each event: quantify what it covers and what remains.
4. Phase the plan: Fase 1 = parar juros abusivos agora; Fase 2 = evento de liquidez; Fase 3 = margem ampliada.
5. Always include negotiation scenario (desconto médio 40% = benchmark realista para cartões).
6. Save to `evolucao/AAAA-MM-DD_ESTRATEGIA-DIVIDA-[VALOR].md`.
7. Order of attack for high-interest debt: cheque especial (12–15%/mês) → rotativo de cartão → parcelado fixo → dívidas pessoais sem juros.

## Output format

Default to a direct, useful structure:

1. **Diagnosis:** 3–5 highest-impact findings.
2. **Risks/gaps:** contradictions, ambiguity, outdated positioning.
3. **Recommended positioning:** target title and one-sentence value proposition.
4. **Ready-to-use copy:** headline/About/current-role draft.
5. **Evidence still needed:** metrics, PDF, dates, or confidential details.
6. **Next action:** the single most useful step.

**Bilingual output (Igor):** When generating LinkedIn rewrites, always produce both Portuguese (🇧🇷) and English (🇺🇸) versions in separate files. Save to `~/MEGA/Documentos/carreira/linkedin/VERSOES-REESCRITAS-LINKEDIN.md` (PT) and `VERSOES-REESCRITAS-LINKEDIN-EN.md` (EN). Each file should be self-contained copy-paste ready for LinkedIn.

Avoid pretending to know salary ranges or market conditions without current research and location/contract context.

## Verification checklist

- [ ] Identity/profile URL verified.
- [ ] Publicly observed facts separated from user-provided facts.
- [ ] Years, dates, and titles are internally consistent.
- [ ] Employer/client relationship is accurate and transparent.
- [ ] Recommendations fit the user's target role.
- [ ] No confidential client details or invented metrics were added.
- [ ] Full-profile limitations were disclosed and a PDF/screenshots requested when needed.
- [ ] Draft language is concrete, seniority-appropriate, and ready to paste.

## Templates available

- [`templates/curriculo.md`](templates/curriculo.md) — starter CV in Portuguese with all key sections, checklist, and employer/client transparency guidance for consulting/outsourcing professionals.

### Dissídio CCT — payroll normalization pitfall

When reconstructing salary history from payslips (contracheques), the CCT reajuste date ≠ the month it appears in the payslip:

- **FEAAC data-base**: 1st August every year → reajuste historically appears in the **October or November** payslip (1–3 month lag).
- When normalizing salary for a rescisão calculation, use the salary from the most recent payslip, not the CCT competence month.
- If projecting a future salary after a pending dissídio, model 3 scenarios (IPCA 4%/5%/6%) and flag which CCT governs each scenario.
- **VALLO BENEFÍCIOS reajusta proportionally** with the dissídio each August — when projecting post-dissídio income, scale VALLO by the same percentage as the salary.

### Custo de vida e mapa canônico de despesas

Igor mantém um mapa canônico em dois lugares idênticos — sempre consultar antes de responder perguntas sobre custo de vida:
- `~/MEGA/Comprovantes/MAPA-CUSTO-VIDA.md`
- `~/MEGA/Documentos/carreira/MAPA-CUSTO-VIDA.md`

**Fixas mapeadas (ago/2026): R$ 3.956,61/mês** (moradia, energia, gás, telefone, academia×3, IA×4, combustível, 🆕 Meli+/Disney+ R$40).
**Orçamento canônico:** `ORCAMENTO.md` — lazer R$1.970 + não-lazer R$2.491 = **R$4.461/mês**.
**Teto de custo de vida confirmado por Igor em 25/07/2026: R$ 4.000/mês.** Parcelamentos e faturas de cartão pertencem ao plano de dívidas, não ao custo fixo.
Alimentação é coberta pelo ticket VR/VA de R$650 da empresa — não entra como custo em conta.

**4 assinaturas de IA:** ChatGPT Plus + Gemini Advanced + Claude Pro + Manus Pro Entry ≈ $79,99/mês (converter pela cotação vigente).

Ao analisar viabilidade de rescisão, uso da margem para dívidas ou runway pós-desligamento, usar o teto de custo de vida de **R$ 4.000/mês**, salvo atualização posterior explícita do Igor.

### Emotional sensitivity around debt data

Igor has explicitly said debt information is emotionally difficult to process and will share card/debt details gradually, one at a time. When handling debt disclosures:
- Accept each piece without pushing for the full picture immediately.
- Integrate each new number into the existing plan and show the updated state clearly.
- Never present the total debt picture as overwhelming or hopeless — always frame with the concrete path forward.
- When a new debt item changes the plan materially, recalculate and update the relevant files, then present only the key delta and revised action order.

### Home equity installment — impact on career timing decisions

When the user has a home equity loan with monthly installments:
- Always recalculate post-installment margin before any career move analysis.
- The installment effectively removes a chunk of monthly buffer — "months of runway" must use `renda_disponível - custo_vida - parcela_HE`, not just `renda_disponível - custo_vida`.
- The grace period (carência) before installments start = strategic window to secure a salary increase before cash flow tightens.
- Job change timing: if installments + cost of living ≈ current income, a gap in employment (even 1–2 months) becomes critical. Factor this into resignation timing advice.

Without login, the public profile shows: name, headline (truncated), location, current company, follower count, About (first ~2 lines only), services, recent activity thumbnails, first experience entry (company name only), certifications list, languages, and partial recommendation text. **Everything else — full experience with dates, prior roles, full About, skills endorsements, featured content, contact info, education details — requires login.** Always disclose this limitation upfront and ask the user for an exported LinkedIn PDF or screenshots of each section before writing full copy.

### Consulting/outsourcing — never list the client as employer
When the user works at a client via a staffing/consulting firm, structure experience as:
`[Role] | [Legal Employer] — consultant assigned to [Client]`
Never imply direct employment by the client. Ask whether contract terms restrict naming the client at all.

### Experience history gap when LinkedIn requires login
When only the current/most recent company is visible from the public profile, draft the resume with a clear "⚠️ — to be completed by the user" section for prior roles rather than fabricating or omitting history. Ask the user explicitly for: company names, periods, roles, key responsibilities, and measurable results for each prior position.

### FGTS saque-aniversário impact on career financial planning
See `career-advisory` financial readiness section. When projecting "runway" after dismissal, always split FGTS into `saldo disponível` (sacável) vs `saldo bloqueado` (antecipação) before reporting total accessible cash. The difference can be R$ 40k+ and materially changes the career decision.
