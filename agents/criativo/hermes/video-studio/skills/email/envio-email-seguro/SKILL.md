---
name: envio-email-seguro
description: Impeça duplicação e erros de Cc/Bcc ao enviar e-mail.
---

# Envio de E-mail Seguro (anti-duplicação)

## Quando usar
Sempre que enviar e-mail que possa danificar se duplicado ou com destinatário errado:
- Jurídico (advogados, órgãos públicos, processos)
- Financeiro (bancos, cobranças)
- Qualquer envio a terceiros onde destinatário visível/oculto importa

## Regra ABSOLUTA (oráculo anti-duplicação)
**1 e-mail destino = consultar o log ANTES + registrar DEPOIS.**

## Procedimento passo a passo

### PASSO 1 — ANTES de enviar: verificar duplicidade
1. Identificar uma pasta de controle canônica (ex: pasta do processo/caso).
2. Procurar o arquivo `EMAIL_ENVIADOS.md` (ou criar se não existir).
3. Checar se o par **(destinatário + assunto + data)** já consta como enviado.
4. **Se já consta:** NÃO reenviar. Parar e perguntar ao usuário:
   - "Este e-mail já foi enviado em [data/hora]. Deseja realmente reenviar? Por quê?"
   - Só enviar com autorização explícita + registrar motivo.
5. **Se é novo:** prosseguir.

### PASSO 2 — Confirmar a configuração de destinatários ANTES do disparo
Antes de disparar, **mostrar/revisar explicitamente**:
- **Para** (visível ao destinatário principal)
- **Cc** (visível a todos: copiados)
- **Bcc** (oculto: recebe sem aparecer para os demais)
Regra: **nunca 'corrigir' depois de enviado**. Erro de Cc/Bcc = e-mail errado no ar.

### PASSO 3 — Enviar
Usar via himalaya (stdin) ou smtplib. Exemplo himalaya:
```
himalaya message send --account <conta> < /tmp/raw.eml
```
- Rodar em background (evita timeout em e-mails grandes).
- Grandes (~>5MB / muitos anexos): **dividir em e-mails menores** (5 anexos cada).

### PASSO 4 — DEPOIS: registrar no log
Adicionar linha em `EMAIL_ENVIADOS.md`: data/hora, Para, Cc, Bcc, assunto, anexos, status.

## Pitfalls (validados 03/09/2026)
- **Envio duplicado:** corrigir Cc→Bcc após disparo causa REENVIO (registrar todos os disparos; 1 envio = 1 registro).
- **Timeout SMTP:** e-mails >~7MB/15 anexos travam ('request timed out'). Dividir ou reduzir.
- **himalaya send NÃO aceita flags de assunto/destino** — construir o .eml com Python email.mime e passar raw via stdin.
- **Bcc:** para ser oculto, adicionar header `Bcc` no .eml MIME (não colocar no Cc).
- **Verificação:** conferir `rc==0` AND mensagem 'successfully sent' no output — não dar como enviado antes disso.

## Template do log
```
| # | Data/Hora | Para | Cc | Bcc | Assunto | Anexos | Status |
```