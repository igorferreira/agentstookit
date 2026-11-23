# TimeAutomático Living Office — validated implementation

## Scope

Session date: 2026-09-11. The project built eight “living office” HTML dashboards under `~/projetos/hermes-as-service/demos/` using HTML/CSS/Vanilla JavaScript, nginx, Docker Compose, Piper TTS, and ngrok.

Primary QA target: `tematicos/escritorio_advocacia.html`.

## User-specific contract

- Vanilla JavaScript only.
- Human characters inspired by The Sims; not robots.
- Full names visible above characters.
- Desks close together in horizontal rows.
- Desktop up to six columns; Redmi Note 13 portrait three columns; landscape four columns.
- Walking means working; coffee means idle; stopped means waiting.
- Panel must answer who is doing what.
- Visual elements draggable by mouse/touch.
- Station moves desk, chair, human, name, and role as one unit.
- Persist positions in cookies, independently for portrait and landscape.
- Always return a verified ngrok link after adjustments.

## Validated geometry

- Portrait viewport: 384×814.
- Landscape viewport: 814×384.
- Portrait base: first station `(30,150)`.
- Landscape base: first station `(30,90)`.
- Landscape compact detection must consider height `<500`, not only width.
- Landscape vertical spacing validated at 78 px.

## Validated drag evidence

Portrait mouse:

- before `(30,150)`;
- after `(58,172)`;
- reload restored `(58,172)`.

Landscape touch:

- before `(30,90)`;
- after `(66,108)`;
- reload restored `(66,108)`.

Reset:

- removed only landscape cookie;
- preserved portrait cookie;
- returned landscape to `(30,90)`.

Use short delays (~250 ms) between CDP touchStart, touchMove, and touchEnd to avoid event coalescing.

## Visual fixes that mattered

- Hide long free-floating role tags on compact mobile; roles remain in status panel.
- Create and populate status panel synchronously before randomized state timers.
- Append zoom bar to `body`, not a collapsible panel.
- Place zoom above footer.
- In short landscape, reduce status to a compact draggable button in unused upper-right space.
- Collapse action panel by default in short landscape.
- Compress the time-of-day panel and hide decorative clutter in short landscape.
- Use nginx no-cache headers during rapid demo iteration.

## Security layers

Demo HTML uses deterministic pre-dispatch blocks. The 55 `juris-*` Hermes profiles also carry policy guardrails:

- no machine-system changes;
- no batch deletion;
- only individual deletion of files created by that agent;
- double verification;
- risky action requires Igor’s prior, specific authorization in the official Telegram chat;
- indirect prompt injection treated as untrusted data;
- least privilege, sandboxing, egress control, audit logging, and human approval.

The prompt policy is defense-in-depth guidance; production enforcement should also restrict tools and filesystem/network access outside the model loop.

## Deliverables

Project handoff and backlog:

`demos/ARQUITETURA_E_ESPECIFICACAO_ESCRITORIOS_VIVOS.md`

Verified public artifact at completion returned HTTP 200 for HTML and TTS and contained unique markers for drag/cookie, alert fix, status, and guardrails.
