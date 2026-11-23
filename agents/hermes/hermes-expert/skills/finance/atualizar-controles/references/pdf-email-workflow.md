# PDF Generation for Email Attachments

When sending a financial report, CV, or any markdown document as PDF via email:

## 1. Generate PDF from Markdown

```bash
python3 << 'PYEOF'
import subprocess, re

md_path = '/path/to/file.md'
pdf_path = md_path.replace('.md', '.pdf')

with open(md_path) as f:
    md = f.read()

# Basic markdown → HTML conversion
md = re.sub(r'^### (.+)$', r'<h3>\1</h3>', md, flags=re.MULTILINE)
md = re.sub(r'^## (.+)$', r'<h2>\1</h2>', md, flags=re.MULTILINE)
md = re.sub(r'^# (.+)$', r'<h1>\1</h1>', md, flags=re.MULTILINE)
md = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', md)
md = re.sub(r'\*(.+?)\*', r'<em>\1</em>', md)
md = re.sub(r'^---$', r'<hr>', md, flags=re.MULTILINE)
md = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', md, flags=re.MULTILINE)

# Tables: wrap in HTML table tags
lines = md.split('\n')
# ... (table parsing logic — see full script in any session that generated a PDF)

full_html = f'''<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
<style>body{{font-family:'Segoe UI',Arial,sans-serif;max-width:800px;margin:40px auto;padding:0 20px;color:#2c3e50;line-height:1.6}}
h1{{color:#1a5276;border-bottom:3px solid #2980b9;padding-bottom:8px;font-size:1.4em}}
h2{{color:#2471a3;margin-top:28px;border-bottom:1px solid #aed6f1;padding-bottom:4px;font-size:1.15em}}
strong{{color:#1a5276}}
blockquote{{background:#ebf5fb;border-left:4px solid #2980b9;margin:12px 0;padding:8px 16px;color:#1a5276}}
table{{border-collapse:collapse;width:100%;margin:12px 0}}
th{{background:#2c3e50;color:white;text-align:left;padding:8px}}
td{{padding:6px;border:1px solid #ddd}}</style></head><body>
{html_body}
</body></html>'''

with open('/tmp/doc.html','w') as f: f.write(full_html)
subprocess.run(['wkhtmltopdf','--encoding','UTF-8','/tmp/doc.html',pdf_path], capture_output=True)
PYEOF
```

## 2. Attach to Email via Himalaya

Use MML multipart syntax — pipe to `himalaya template send`:

```bash
cat << 'EOF' | himalaya template send
From: Usuário <SEU-EMAIL@gmail.com>
To: recipient@example.com
Subject: Subject here

Email body text here.

<#multipart type=related>
<#part type=application/pdf filename="/absolute/path/to/file.pdf" name="Nice-Name.pdf"><#/part>
<#/multipart>
EOF
```

Key points:
- Use `type=related` (not `mixed`) for inline PDF
- `filename` must be an **absolute path**
- `name` is the display name the recipient sees
- Gmail sent folder: `[Gmail]/E-mails enviados` for Portuguese

## 3. Verify Sent

```bash
himalaya envelope list --folder "Sent" --page-size 3
```

## Pitfalls

- **wkhtmltopdf not installed**: `sudo apt install wkhtmltopdf`
- **MML multipart fails silently**: if the `<#multipart>` block has wrong syntax, himalaya may send the email WITHOUT the attachment and exit 0. Always verify in Sent folder.
- **CDB value corrections**: if the user corrects a value (e.g., "CDB é 29mil, não 39mil"), regenerate the PDF with the corrected value and send a new email. Don't just send a text correction — the PDF is the authoritative document.
