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

### PASSO 3 — Construir MIME + enviar via heimalaya (stdin)

**PASSO 3A — Construir MIME (Python `email.mime`)**
Sempre construir o `.eml` usando Python `MIMEMultipart` + `MIMEBase`:
1. Criar `MIMEMultipart()` e setar To/From/Subject via dicts.
2. Attach corpo com `MIMEText(body, 'plain', 'utf-8')`.
3. Para cada anexo: `MIMEBase('application', 'vnd.openxmlformats-officedocument.wordprocessingml.document')` → `set_payload(f.read())` → `encoders.encode_base64(part)` → `add_header('Content-Disposition', 'attachment; filename=...')` → `msg.attach(part)`.
4. Escrever via `msg.as_string()` em arquivo temporário.

**PASSO 3B — Enviar via heimalaya NOVA LINHA (09/2026)**
```python
# Via stdin (único caminho válido para heimalaya!)
subprocess.run(['himalaya', 'message', 'send', '-a', 'gmail-igor'],
               input=open(path_eml).read(),
               capture_output=True, text=True, timeout=120)
```

⚠️ **NUNCA passar caminho de arquivo como argumento:**
❌ `himalaya message send -a conta /caminho/arquivo.txt` → crash com `index out of bounds: the len is 0 but the index is 0` (exit 101).
✅ Sempre usar `-a conta < /tmp/arquivo.txt` (shell redirection) OU `subprocess.run(..., input=open().read())` (Python pipe).

- Usar `-a <nome-conta>` explicitamente mesmo quando há uma única conta.
- Rodar em foreground com timeout alto; se `returncode != 0` verificar stderr.
- Para e-mails >~7MB / muitos anexos: dividir em e-mails menores (5 anexos cada).

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