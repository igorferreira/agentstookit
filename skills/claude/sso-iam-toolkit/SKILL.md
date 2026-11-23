---
name: sso-iam-toolkit
description: Reusable procedures for enterprise/cross-system authentication and identity architecture — SAML 2.0 metadata validation, OAuth2/OIDC integration checklists (authorization code + PKCE, client credentials, device code, refresh rotation), JWT/JWK/JWKS inspection, and generating a CTO-ready IAM architecture presentation outline (build vs. buy, roadmap, risk, ROI). Use when validating SAML metadata XML, scaffolding an OAuth2/OIDC client integration, reviewing JWT claims/signature setup, or drafting an executive IAM deck. Distinct from better-auth/create-auth-skill, which cover the Better Auth TypeScript library specifically — this skill is protocol/vendor-agnostic for enterprise SSO/IAM.
license: MIT
version: 1.0.0
---

# SSO / IAM Toolkit

Reusable, mostly mechanical procedures for enterprise and cross-system authentication —
SSO, OAuth2/OAuth2.1, OpenID Connect (OIDC), SAML 2.0, and adjacent identity-federation
protocols. This skill is the "mechanical arm": deterministic checklists and scripts for
recurring tasks. Architectural judgment (which protocol, which IdP, threat modeling, full
enterprise IAM design) belongs to the `iam-auth-architect` agent — invoke that agent for
open-ended design/review work; use this skill directly for the bounded procedures below.

## Scope note (avoid confusion with other auth skills)

This skill is protocol/vendor-agnostic and targets **enterprise/cross-system IAM** (SAML, OIDC,
WS-Federation, enterprise IdPs). It is **not** about a specific application auth library. For
adding login/session management to a TypeScript/JavaScript app with the Better Auth library, use
the `better-auth` or `create-auth-skill` skills instead — those are unrelated in scope to this
one.

## When to Use

- Validating a SAML 2.0 metadata XML file (SP or IdP) for correctness/expiration.
- Reviewing or scaffolding an OAuth2/OIDC client integration (which grant, PKCE, redirect_uri
  allowlist, scopes, refresh rotation).
- Inspecting JWT/JWK/JWKS setup (signature/issuer/audience/expiration validation, key rotation).
- Drafting the outline of a CTO/leadership-facing IAM architecture presentation.

For open-ended architecture decisions (choosing between OAuth2/OIDC/SAML/WS-Federation,
selecting or comparing IdPs, designing federation across partners, full threat modeling of a
proposed flow), delegate to the `iam-auth-architect` agent instead of trying to resolve it from
this skill alone.

## Procedure 1 — OAuth2/OIDC integration checklist

Before shipping or reviewing an OAuth2/OIDC integration, confirm:

1. **Grant type**: authorization code + PKCE for public clients (SPA/mobile/CLI); client
   credentials for machine-to-machine; never Implicit or Resource Owner Password Credentials in
   a new integration.
2. **`redirect_uri`** validated against an exact allowlist (never a prefix or wildcard match).
3. **`state`** and **`nonce`** generated and validated (CSRF/replay protection).
4. **Scopes**: minimum necessary requested (least privilege).
5. **Token lifetime**: short-lived access token + rotated refresh token, not a long-lived static
   token.
6. **Token validation**: signature, `iss`, `aud`, and `exp` all checked before trusting any
   claim — never trust an unverified claim.
7. **Key rotation**: JWKS rotation handled on the validating side (cache with reasonable TTL,
   not a hardcoded key).

## Procedure 2 — Validate SAML metadata

Run:
```
python3 scripts/validate_saml_metadata.py <path-to-metadata.xml>
```
The script (Python stdlib only, no external dependencies) checks for:
- a valid `EntityDescriptor` with `entityID`;
- at least one `X509Certificate` (signing key present);
- `SingleLogoutService` (SLO) endpoints, flagging their absence as a warning;
- `SingleSignOnService`/`AssertionConsumerService` endpoints;
- `validUntil` expiration, warning if the metadata expires within 30 days or has already expired.

Exit code is non-zero if a hard problem (malformed XML, missing EntityDescriptor, missing
certificate) is found; warnings alone do not fail the check.

## Procedure 3 — CTO/executive IAM presentation outline

When asked to produce material for a CTO or technical leadership audience, use this fixed
structure (feed it into the `pptx`/`slide-deck` skill, or produce structured markdown if no
slide tool is requested):

1. **Contexto/Problema** — why this is being discussed now.
2. **Estado Atual de IAM** — what exists today (IdP, protocols, pain points).
3. **Opções** — build vs. buy of an IdP, with a comparison table (cost, risk, time-to-value).
4. **Recomendação** — the proposed path, stated plainly.
5. **Arquitetura Proposta** — diagram/flow of the recommended solution.
6. **Riscos e Mitigação** — security, operational, and adoption risks with mitigations.
7. **Roadmap de Adoção** — phased rollout plan.
8. **Custo/ROI** — cost comparison and expected return/benefit.
9. **Próximos Passos** — concrete next actions and owners.

## Related

- Agent: `iam-auth-architect` (architectural judgment, threat modeling, full design work).
- Skills: `better-auth`, `create-auth-skill` (Better Auth TypeScript library — different scope).
