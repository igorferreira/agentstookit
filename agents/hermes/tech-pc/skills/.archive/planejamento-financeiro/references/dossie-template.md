# Template de Dossiê para Advogado — Negociação de Dívidas

Estrutura canônica em 5 seções. Adaptar com os dados do usuário.

```markdown
# Dossiê — Atualização Estratégia Financeira | [MÊS]/[ANO]

> **Para:** Dr. [NOME DO ADVOGADO]
> **De:** [NOME DO USUÁRIO]
> **Data:** [DATA]

---

## 1. O que aconteceu desde o último dossiê

[Contexto: o que mudou, quais descobertas motivaram a mudança de estratégia]

### 📊 Parcelamentos mapeados

| Cartão | Período | Maior parcela | Última |
|---|---|---|---|
| [NOME] | [MÊS INÍCIO] a [MÊS FIM] | R$ [VALOR] | R$ [VALOR] |

---

## 2. Nova estratégia

**Decisão: [FRASE RESUMO DA ESTRATÉGIA]**

### ✅ Cartões MANTIDOS

| # | Banco | Cartão | Final | Valor atual | Parcelamentos |
|---|---|---|---|---|---|
| 1 | | | | R$ | |

### ❌ Cartões para NEGOCIAÇÃO

| # | Banco | Cartão | Final | Valor atual |
|---|---|---|---|---|
| 1 | | | | R$ |

> 🔴 [PRIORIDADES — ex: cartão já vencido]

---

## 3. Projeção financeira

### Renda mensal

| Fonte | Valor |
|---|---|
| [FONTE 1] | R$ |
| **Total** | **R$** |

### Compromissos fixos

| Compromisso | Valor | Início |
|---|---|---|
| [NOME] | R$ | [DATA] |

### Eventos de renda extra

| Quando | Evento | Valor est. |
|---|---|---|
| [MÊS] | [EVENTO] | R$ |

### 📈 Evolução da reserva

| Data | Reserva | Evento |
|---|---|---|
| Hoje | R$ | Após pagamentos |
| [MÊS] | R$ | 🔻 Pior momento |
| [MÊS/ANO] | R$ | 🏆 Disponível para acordos |

---

## 4. O que esperamos do advogado

### 🎯 Meta

[FRASE RESUMO DA META]

### 📅 Cronograma

| Marco | Data | Ação |
|---|---|---|
| Hoje | [DATA] | [AÇÃO] |
| [DATA] | 280 dias | Melhores condições de desconto |
| [DATA] | 🏆 | Reserva disponível para acordos |

### 💡 Simulação de quitação

Dívida total: R$ [VALOR]

| Cenário | Desconto | Custo | Sobra |
|---|---|---|---|
| Conservador | 40% | R$ | R$ |
| Otimista | 60% | R$ | R$ |

### ⚠️ Prioridade

[Cartão mais urgente e por quê]

---

## 5. Observações finais

- ✅ [FATO POSITIVO]
- ⚠️ [RESSALVA]
- 📱 [DOCUMENTAÇÃO DISPONÍVEL]

---

**[NOME DO USUÁRIO]**
[Cidade], [DATA]
```

## Geração do PDF

```bash
pandoc dossie.md --pdf-engine=wkhtmltopdf -o dossie.pdf \
  --css=<(echo 'body { font-family: Arial; font-size: 11pt; color: #1a1a1a; line-height: 1.6; }
    h1 { font-size: 18pt; border-bottom: 2px solid #2563eb; }
    h2 { font-size: 14pt; color: #2563eb; margin-top: 24px; }
    table { width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 9pt; }
    th { background: #2563eb; color: white; padding: 6px 8px; text-align: left; }
    td { padding: 4px 8px; border: 1px solid #ddd; }
    tr:nth-child(even) { background: #f7f7f7; }')
```

## Envio por email com PDF anexo

Usar Python SMTP com `secret-tool` para obter a senha (mesmo método do himalaya):

```python
import smtplib, subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

result = subprocess.run(['secret-tool', 'lookup', 'service', 'hermes-gmail', 
                        'account', 'user@gmail.com'], capture_output=True, text=True)
password = result.stdout.strip()

msg = MIMEMultipart()
msg['From'] = 'User <user@gmail.com>'
msg['To'] = 'lawyer@email.com'
msg['Subject'] = 'Assunto'

msg.attach(MIMEText('Corpo do email', 'plain'))

with open('/path/to/dossie.pdf', 'rb') as f:
    part = MIMEBase('application', 'pdf')
    part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="Dossie.pdf"')
    msg.attach(part)

with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()
    server.login('user@gmail.com', password)
    server.send_message(msg)
```
