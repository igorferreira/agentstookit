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
2. Capture the visible headline, About/Summary, current company, services, experience, education, certifications, recommendations, and recent topical activity.
3. State access limitations early. LinkedIn often hides complete experience behind login; request the exported PDF or screenshots for a full review.
4. Compare the profile against user-provided facts:
   - years of experience;
   - current title and scope;
   - current technical domain;
   - employer/client relationship;
   - outdated services, keywords, or certifications.
5. Identify the highest-impact gaps first; do not bury the main issue under cosmetic edits.
6. Draft improvements in this order:
   - headline;
   - first 2–3 lines of About;
   - full About narrative;
   - current-role description;
   - selected prior roles;
   - skills/services and featured proof;
   - activity/content strategy.
7. Tie recommendations to a target outcome: recruiter discovery, architect/principal positioning, consulting authority, leadership track, promotion, or transition.

See [`references/linkedin-public-profile-review.md`](references/linkedin-public-profile-review.md) for the browser/public-view procedure and common access limitations.

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

## Career-transition financial readiness

When the user is preparing for a possible resignation, dismissal, or employer change:

1. Treat financial readiness as part of the career decision, not as a separate motivational aside.
2. Compare scenarios side by side and distinguish immediately accessible cash from conditional or blocked values.
3. Maintain separate ledgers for employment-law remuneration and personal disposable resources. A benefit may count toward current living-expense capacity without entering salary, FGTS, vacation, 13th salary, or termination bases; preserve date, recurrence, restrictions, payroll treatment, and evidence. When the user explicitly confirms the benefit is excluded from their termination model, treat that as a stable planning rule and do not repeatedly blur it with speculative reclassification caveats.
4. Ask for exact contract, vacation, FGTS, and current-remuneration data rather than inventing a precise estimate.
5. Normalize employment history before calculating: effective amended start date versus earlier communicated date, admission role versus current role, and initial/proposed salary versus current salary.
6. Preserve evidence provenance—original document, user transcription, or inference—and keep unresolved fields null.
7. Convert the conservative accessible total into months of the user's stated net cost of living.
8. Use current official legal and tax sources and label all outputs as planning estimates, not guaranteed TRCT values.
9. For recurring analysis, use stable structured input, deterministic calculations, monthly reports, and explicit missing-data gates.
10. When payroll evidence is stored in email or document archives, save the questionnaire and source first, verify authorization before claiming access, request the narrowest needed access, and preserve message/document provenance without modifying the mailbox.

See [`references/clt-transition-financial-planning.md`](references/clt-transition-financial-planning.md) for the scenario model, data intake, payroll-evidence workflow, automation pattern, edge cases, and official sources.

For mailbox-to-report implementation details—message manifests, deterministic PDF extraction, salary normalization, split-vacation reconstruction, CCT auditing, FGTS reconstruction, scenario separation, and repository/cron relocation—see [`references/payroll-evidence-extraction-and-audit.md`](references/payroll-evidence-extraction-and-audit.md).

## User-specific execution preference

For Igor, break substantive career work into small tasks, execute them sequentially one at a time, and close with a report listing work performed, files changed, hypotheses, missing data, and next steps. Do not merely present a plan when the tools can complete the work now.

For long evidence-processing or calculation runs, do not go silent: send a brief progress update after each major phase (collection, extraction, normalization, calculation, verification). If the conversation is interrupted or compacted, resume from the active task and explicitly state the current phase instead of restarting or making Igor ask whether work is continuing.

## Output format

Default to a direct, useful structure:

1. **Diagnosis:** 3–5 highest-impact findings.
2. **Risks/gaps:** contradictions, ambiguity, outdated positioning.
3. **Recommended positioning:** target title and one-sentence value proposition.
4. **Ready-to-use copy:** headline/About/current-role draft.
5. **Evidence still needed:** metrics, PDF, dates, or confidential details.
6. **Next action:** the single most useful step.

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
