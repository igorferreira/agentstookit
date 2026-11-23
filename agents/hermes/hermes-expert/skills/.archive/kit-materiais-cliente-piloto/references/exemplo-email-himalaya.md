# Exemplo de envio via himalaya (validado 04/09/2026)

O `himalaya message send` não aceita flags de Subject/To. Montar o MIME completo:

```python
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

msg = MIMEMultipart()
msg['From'] = 'igorferreirabr@gmail.com'
msg['To'] = 'destinatario@exemplo.com'
msg['Cc'] = 'igorferreirabr@gmail.com'   # cópia sempre
msg['Subject'] = 'TimeAutomático — Apresentações: <CLIENTE>'
msg.attach(MIMEText(corpo, 'plain', 'utf-8'))
for f in anexos:  # PDF + PPTX por cliente; 10 anexos (~2.5 MB) passam bem
    part = MIMEApplication(open(f,'rb').read(), Name=f.name)
    part['Content-Disposition'] = f'attachment; filename="{f.name}"'
    msg.attach(part)
Path('/tmp/envio.eml').write_bytes(msg.as_bytes())
```

Enviar e confirmar:

```bash
himalaya message send --account gmail-igor < /tmp/envio.eml
himalaya envelope list --account gmail-igor --folder Sent --page-size 5
```

## Ordem de envio recomendada por cliente-piloto
1. mensagem curta WhatsApp (bloco de código)
2. áudio 1 (apresentação)
3. PDF do deck setorial
4. áudio 3 (piloto gratuito)
5. aguardar resposta — áudios 2 e 4 são de aprofundamento
