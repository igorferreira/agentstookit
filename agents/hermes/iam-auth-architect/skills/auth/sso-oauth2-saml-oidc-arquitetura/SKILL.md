---
name: sso-oauth2-saml-oidc-arquitetura
description: Use when Igor needs to design, review, or troubleshoot SSO/OAuth2/OIDC/SAML integrations, compare identity providers, validate SAML metadata, or produce IAM architecture material for a CTO/leadership audience.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [auth, sso, oauth2, oidc, saml, iam, identity, seguranca]
    related_skills: []
---

# Arquitetura de SSO / OAuth2 / SAML / OIDC

## Objetivo

Dar suporte a decisões e implementações de autenticação entre aplicações e sistemas — SSO,
OAuth2/OAuth2.1, OpenID Connect, SAML2 e protocolos correlatos — cobrindo tanto o julgamento
arquitetural quanto procedimentos mecânicos repetíveis (validação de metadata SAML, checklist
de integração OAuth2/OIDC, outline de apresentação executiva).

## Quando usar

Use esta habilidade para:

- decidir entre OAuth2/OIDC, SAML2, WS-Federation ou Kerberos para uma integração específica;
- revisar um fluxo OAuth2/OIDC existente (grant usado, PKCE, escopos, rotação de refresh token);
- validar um arquivo de metadata SAML (EntityDescriptor, certificados, SingleLogoutService);
- comparar Identity Providers (Keycloak, Auth0, Okta, Azure AD/Entra ID, PingFederate, ADFS,
  ForgeRock, ORY Hydra/Kratos, AWS Cognito) para um cenário workforce ou CIAM;
- montar o outline de uma apresentação de arquitetura IAM para CTO/liderança.

## Regra de execução do agente

Toda solicitação deve ser quebrada em tarefas pequenas, executadas **uma por vez**. Ao terminar,
emitir relatório com: (1) tarefas realizadas, (2) arquivos criados/atualizados, (3) riscos e
próximos passos.

## Checklist de decisão: OAuth2 vs. OIDC vs. SAML2

1. O parceiro/IdP já exige um protocolo específico? Se sim, isso decide — nunca forçar o outro
   lado a adotar um protocolo que não suporta.
2. Cenário enterprise/legado com Active Directory já federando via ADFS/SAML? Tende a SAML2 ou
   WS-Federation.
3. Cenário consumer/API-first, mobile ou SPA? Tende a OIDC (com PKCE obrigatório em cliente
   público).
4. Autenticação service-to-service sem usuário humano? Avaliar client credentials (OAuth2) ou
   mTLS/SPIFFE-SPIRE em vez de qualquer fluxo interativo.
5. Precisa de Single Logout coordenado entre múltiplos SPs? SAML2 tem SLO nativo; em OIDC,
   avaliar `end_session_endpoint` (RP-Initiated Logout) ou revogação de token.

## Checklist de integração OAuth2/OIDC

- Qual grant? (authorization code + PKCE para clientes públicos; client credentials para
  máquina-a-máquina; nunca usar Implicit ou Resource Owner Password Credentials em integração
  nova.)
- `redirect_uri` validado contra allowlist exata (nunca prefixo/wildcard amplo)?
- `state` e `nonce` gerados e validados (proteção CSRF/replay)?
- Escopos mínimos necessários solicitados (princípio do menor privilégio)?
- Token de acesso de vida curta + refresh token rotacionado?
- Validação do token confirma assinatura, `iss`, `aud` e `exp` antes de usar qualquer claim?
- Rotação de chaves JWKS contemplada no lado que valida o token?

## Procedimento: validar metadata SAML

Rodar `scripts/validate_saml_metadata.py <arquivo.xml>` — parser em Python puro (stdlib
`xml.etree`, sem dependências externas) que confere:

- presença de `EntityDescriptor` e `entityID`;
- presença de ao menos um certificado (`KeyDescriptor`/`X509Certificate`);
- presença de `SingleLogoutService` (SLO), quando exigido pelo cenário;
- atributo `validUntil`, alertando se já expirado ou próximo do vencimento.

## Procedimento: outline de apresentação executiva para CTO

Estrutura fixa a seguir sempre que solicitado um deck de arquitetura IAM (usar as skills de
apresentação já disponíveis no perfil — `productivity/powerpoint` — ou markdown estruturado):

1. Contexto/Problema
2. Estado Atual de IAM
3. Opções (build vs. buy de IdP, com tabela comparativa de custo/risco/prazo)
4. Recomendação
5. Arquitetura Proposta
6. Riscos e Mitigação
7. Roadmap de Adoção
8. Custo/ROI
9. Próximos Passos

## Diferenciação de escopo

Esta habilidade é sobre **IAM/SSO corporativo, multi-protocolo e agnóstico de linguagem**.
Não é sobre uma biblioteca de aplicação específica (ex.: Better Auth em TypeScript) — para isso,
usar a stack/framework já em uso no projeto em questão.
