# LinkedIn Complete Data Export — Analysis Workflow

## When to use

When the user sends a LinkedIn data export ZIP (Settings → Data Privacy → Get a copy of your data) containing the full CSV archive. This is the "Opção 2" path — the most complete source, revealing everything the public profile hides.

## ZIP contents — priority order

The export contains ~22 CSV files. Process in this priority:

| Priority | File | What it reveals |
|---|---|---|
| 🔴 1 | `Profile.csv` | Name, headline, summary, location, industry, birth date |
| 🔴 1 | `Positions.csv` | Full work history with dates, titles, and descriptions |
| 🔴 1 | `Skills.csv` | All listed skills |
| 🔴 1 | `Certifications.csv` | Certifications with dates and license numbers |
| 🟡 2 | `Education.csv` | Education entries (school often missing) |
| 🟡 2 | `Languages.csv` | Languages and proficiency levels |
| 🟡 2 | `Registration.csv` | Account creation date |
| 🟢 3 | `Jobs/Saved Jobs.csv` | All saved jobs with URLs — reveals career interests |
| 🟢 3 | `Jobs/Job Seeker Preferences.csv` | Open to Work status, target titles, job types |
| 🟢 3 | `Company Follows.csv` | Companies followed — reveals industry/pivot signals |
| 🟢 3 | `Projects.csv` | Projects section of profile |
| ⬜ 4 | `Endorsement_Received_Info.csv` | Who endorsed which skills |
| ⬜ 4 | `Endorsement_Given_Info.csv` | Skills you endorsed for others |
| ⬜ 4 | `Email Addresses.csv` | Registered emails |
| ⬜ 4 | `PhoneNumbers.csv` | Registered phones |
| ⬜ 4 | `Rich_Media.csv` | Posts and media shared |
| ⬜ 5 | `SavedJobAlerts.csv`, `Receipts_v2.csv`, etc. | Low signal |

## Extraction workflow

1. Unzip the file with `unzip -o <file> -d /tmp/linkedin_export/`
2. Read files in priority order using `read_file` or terminal `cat`
3. Build a structured profile document and save to `~/MEGA/Documentos/carreira/linkedin/PERFIL-LINKEDIN-COMPLETO.md`
4. Never invent missing data — mark as "❌ Não informada"

## Gap analysis framework

After extracting all data, run this diagnostic:

### 7-point gap check (ordered by severity)

1. **Headline** — Does it reflect the CURRENT role? Or a past one?
2. **Summary (About)** — Are years-of-experience current? Does it mention current domain (AI/cloud/etc.)?
3. **Current position** — Is the description complete? Does the legal employer appear (vs just client)?
4. **Skills** — Are in-demand skills from the headline actually LISTED? (Common: "Kubernetes" in headline but not in skills)
5. **Languages** — Is English listed? If not, the profile is invisible to international recruiter filters
6. **Projects** — Are they recent or frozen in time?
7. **Certifications** — Are they current or from 10+ years ago?

### Hidden-signal analysis (from Saved Jobs + Company Follows)

The user's browsing behavior often reveals their TRUE career direction before the profile reflects it:

- **Saved Jobs** — Cluster by: company frequency, role level (Senior/Lead/Architect), technology domain, geography
- **Company Follows** — Recent follows (last 12 months) reveal industry pivot: e.g., following OpenAI + Anthropic + NVIDIA = AI pivot even if profile says "Java Developer"
- **Job Seeker Preferences** — Open to Work status, target titles, job types, visibility level

Present this as: "Your own LinkedIn data already shows you're pivoting to X — but your profile hasn't caught up yet."

## Rewrite output format

When the user asks for rewrites, generate these in order and save ALL to the linkedin folder:

### Files to create

```
~/MEGA/Documentos/carreira/linkedin/
├── PERFIL-LINKEDIN-COMPLETO.md          ← Full structured analysis
├── VERSOES-REESCRITAS-LINKEDIN.md       ← 🇧🇷 Portuguese copy-paste
└── VERSOES-REESCRITAS-LINKEDIN-EN.md    ← 🇺🇸 English copy-paste
```

### Each rewrite file contains (in copy-paste order)

1. **HEADLINE** (max 220 chars) — bilingual
2. **ABOUT (Summary)** — bilingual, 3 paragraphs: career arc, current scope, what drives them
3. **CURRENT ROLE (Experience)** — bilingual, 3-5 bullet points with concrete scope
4. **SKILLS TO ADD** — top 5 missing skills
5. **LANGUAGE TO ADD** — with level placeholder

### Employer vs client rule (always enforce)

When the user is employed by a consultancy (e.g., Noorden) but works at a client (e.g., HDI):
- Cargo atual format: "Arquiteto de IA | HDI Seguros (via Noorden Services)"
- English: "Innovation & AI Architect | HDI Seguros (via Noorden Services)"
- Never imply direct employment by the client
- Always note this gap in the analysis

## Pitfalls

- **ZIP inside ZIP**: Some exports come as `.zip.zip` — unzip twice
- **CSV encoding**: LinkedIn exports use UTF-8, but some fields have special characters (∴, accents)
- **Positions.csv has blank descriptions**: Early-career positions often have no description — don't fabricate
- **Education.csv school name**: Often empty — mark as "❌ Não informada" and ask user
- **Saved Jobs URL format**: `http://www.linkedin.com/jobs/view/<id>` — can be opened to see current status
