# SMTP Attachment Fallback

When `himalaya template send` with MML attachments fails, use Python SMTP directly.

The password is stored in GNOME keyring — retrieve it the same way himalaya does:

```python
import smtplib, subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

# Get password from keyring (same method as himalaya config)
result = subprocess.run(
    ['secret-tool', 'lookup', 'service', 'hermes-gmail',
     'account', 'user@gmail.com'],
    capture_output=True, text=True
)
password = result.stdout.strip()

msg = MIMEMultipart()
msg['From'] = 'Name <user@gmail.com>'
msg['To'] = 'recipient@email.com'
msg['Subject'] = 'Subject here'

msg.attach(MIMEText('Email body text', 'plain'))

# Attach PDF
with open('/path/to/file.pdf', 'rb') as f:
    part = MIMEBase('application', 'pdf')
    part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',
                    'attachment; filename="Nice-Name.pdf"')
    msg.attach(part)

with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()
    server.login('user@gmail.com', password)
    server.send_message(msg)
```
