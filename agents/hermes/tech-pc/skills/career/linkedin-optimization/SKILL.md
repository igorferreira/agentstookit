---
name: linkedin-optimization
description: "Use for LinkedIn profile optimization, networking strategy, data export analysis, headline/About writing, recruiter visibility, and complete LinkedIn profile overhauls. Covers all sections of a LinkedIn profile plus data-driven insights from LinkedIn exports."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [linkedin, career, profile, networking, recruiter, optimization]
    related_skills: [career-advisory]
    created_by: agent
---

# LinkedIn Optimization Specialist

## Overview

Complete LinkedIn optimization: profile analysis, headline/About writing, skill strategy, networking, content, recruiter visibility, and data export analysis. Grounded in real LinkedIn export data structures and recruiter search behavior.

## Trigger conditions

Use when the user asks about:
- LinkedIn profile review, optimization, or rewrite
- LinkedIn headline, About/Summary, or experience descriptions
- LinkedIn networking or connection strategy
- LinkedIn data export analysis
- Recruiter visibility and search optimization
- LinkedIn skills and endorsement strategy
- LinkedIn content or activity strategy

## LinkedIn Export Data Structure

When the user provides a LinkedIn data export (ZIP), these are the key files and what they reveal:

### Core Profile Files
| File | Content | Use |
|---|---|---|
| Profile.csv | Name, headline, summary, industry, location, websites | Headline/About audit |
| Positions.csv | Full work history with dates, titles, descriptions | Experience gap analysis |
| Profile Summary.csv | Full About section text | Rewriting target |
| Skills.csv | All listed skills | Skill gap analysis |
| Certifications.csv | Certifications with dates, authorities | Freshness check |

### Social Proof
| File | Content | Use |
|---|---|---|
| Recommendations_Received.csv | Full text of recommendations | Social proof strength |
| Endorsement_Received_Info.csv | Skills endorsed, by whom, when | Skill credibility |
| Recommendations_Given.csv | Recommendations you wrote | Network engagement |

### Activity & Network
| File | Content | Use |
|---|---|---|
| Invitations.csv | Sent/received connection invitations | Network growth analysis |
| Company Follows.csv | Companies followed | Career interest mapping |
| Events.csv | Events attended | Learning & networking |
| Saved Jobs.csv | Jobs saved over time | Career aspiration history |
| Comments/Shares/Reactions | Platform activity | Content strategy |
| messages.csv | LinkedIn messages | Relationship mapping |

### Job Seeking
| File | Content | Use |
|---|---|---|
| Job Seeker Preferences.csv | Open to work, job types, titles | Recruiter visibility check |
| SavedJobAlerts.csv | Job alert configurations | Target market analysis |

## Complete Profile Audit Methodology

When given a full LinkedIn export, audit in this order:

1. **Identity & Branding**
   - Headline: does it match current role and target role?
   - About: length, keywords, narrative arc, recency
   - Profile photo/banner: mentioned in Rich_Media.csv

2. **Experience**
   - Current role: accurate title, employer/client relationship, concrete achievements
   - Prior roles: dates consistent, descriptions present, metrics where possible
   - Employment gaps: identified and explained
   - Consulting/outsourcing: employer vs client clearly distinguished

3. **Skills & Endorsements**
   - Missing target-role skills
   - Outdated/legacy skills dominating the profile
   - Endorsement recency (when was the last endorsement?)
   - Top 3 skills by endorsement count

4. **Social Proof**
   - Recommendations: count, recency, quality, diversity of recommenders
   - Gaps: no recommendations from recent roles?

5. **Education & Certification**
   - Completeness of education entries
   - Certification freshness (anything older than 5 years may need renewal/removal)

6. **Activity & Network**
   - Connection growth pattern
   - Companies followed → career interests
   - Events attended → learning priorities
   - Saved jobs → aspiration mapping

7. **Recruiter Visibility**
   - Open to Work status
   - Job preferences configured correctly
   - Target titles aligned with profile content
   - Location and remote preferences

## Headline Formulas

### For Senior IC (Individual Contributor)
```
[Role] | [Top 3 Technologies] | [Years] years in [Domain]
Example: Arquiteto de IA | Java • Python • AWS | 22+ anos em Tecnologia
```

### For Leadership
```
[Role] @ [Company] | [Top Skill 1] • [Top Skill 2] • [Top Skill 3] | [Differentiator]
```

### For Career Transition
```
[Target Role] | [Transferable Stack] | [Years] years building [Outcome]
Example: Arquiteto de Inovação e IA | Java • Spring Boot • Docker • AWS | 22+ anos
```

### Rules
- Max 220 characters
- Lead with target role, not current role
- Include 3-5 keywords recruiters search for
- No buzzwords ("passionate", "guru", "ninja")
- Reflect the role you WANT, not just what you HAVE

## About/Summary Structure

```
Paragraph 1: Identity statement (who you are NOW, years, transition if applicable)
Paragraph 2: Domain expertise (industries, scale, impact)
Paragraph 3: Current focus / what drives you (3-5 bullet points)
Paragraph 4: Technical anchor (key technologies, platforms)
```

### Anti-patterns to remove
- "20 anos de experiência desenvolvendo e mantendo sistemas" → dated, passive
- "Responsável por..." → replace with active achievements
- Missing current role focus (if you're doing AI now, SAY IT)
- English not listed as a language

## Recruiter Search Optimization

LinkedIn Recruiter searches primarily on:
1. **Headline keywords** (highest weight)
2. **Job titles** (current + past)
3. **Skills** (explicit match)
4. **Location**
5. **Industry**

To appear in searches for "AI Architect":
- Headline MUST contain "AI" or "Inteligência Artificial" or "Machine Learning"
- Current job title should include "Arquiteto" and "IA"
- Skills must include AI, GenAI, LangChain, or similar
- English language MUST be listed (excluded from international filters otherwise)

## Skill Strategy

### What to ADD
- AI/ML stack: Generative AI, LangChain, LLM, Agent Architecture
- Cloud: Kubernetes (if missing), AWS Bedrock, Azure AI
- Architecture: Solution Architecture, Enterprise Architecture
- Languages: English (even basic — without it, filtered out of international roles)

### What to DEMOTE (not delete)
- Legacy tech still relevant for depth: WebLogic, Oracle SOA, BPEL
- Move these to bottom of skills list (top 3 are most visible)
- They show depth and longevity — keep but don't feature

### What to DELETE
- Duplicate skills (WebLogic AND Weblogic)
- Skills with 0 endorsements
- Outdated frameworks with no modern relevance

## Employer vs Client Relationship

When the user works via consulting/staffing (Noorden → HDI):
```
Position: [Role] at [Client]
Company: [Legal Employer] — consultant assigned to [Client]

NOT:
Company: [Client]  ← MISLEADING in background checks
```

Template for experience entry:
```
Title: Arquiteto de Inovação e IA
Company: Noorden Services (alocado na HDI Seguros)
Period: Jan 2026 – present (3 yrs prior as Senior Specialist)
```

## Networking Strategy

### Connection requests
- Always add a note (LinkedIn limits without notes)
- Reference: mutual connections, shared events, common interests
- Template: "Olá [Nome], vi que você [trabalha na X / participou do evento Y / tem experiência com Z]. Gostaria de conectar para trocar ideias sobre [tópico relevante]."

### Companies to follow
- Target employers (for job alerts)
- Competitors (industry awareness)
- AI/tech leaders (learning)
- Recruiting firms in target domain

## Content Strategy

### What to post
- Technical insights from daily work (anonymized)
- Course/certification completions
- Event participation
- Tool/methodology discoveries
- Career milestones

### Frequency
- 1-2 posts per week minimum for visibility
- Engage (like/comment) on 3-5 posts daily
- Comment > Like for algorithmic reach

## Verification Checklist

- [ ] Headline reflects target role and contains recruiter keywords
- [ ] About section is current (<6 months old)
- [ ] Current role title and description are accurate
- [ ] Employer/client relationship is transparent
- [ ] Skills cover target domain (not just legacy stack)
- [ ] English is listed as a language
- [ ] At least 5 skills endorsed in the last 12 months
- [ ] Profile photo is professional and recent (<2 years)
- [ ] Open to Work settings are intentional
- [ ] Certifications are current (remove expired/irrelevant)
