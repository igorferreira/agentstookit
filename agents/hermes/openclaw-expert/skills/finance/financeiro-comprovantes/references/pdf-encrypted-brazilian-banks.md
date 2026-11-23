# PDF Criptografado — Bancos e Cartões Brasileiros

## Padrão comum: senha = primeiros 5 ou 6 dígitos do CPF

Itaú, Itaú Cartões (Luiza, Signature, Passaí, etc.), Bradescard/Amazon e alguns outros emissores brasileiros protegem faturas com senha aberta baseada nos **5 ou 6 primeiros dígitos do CPF** do titular (ex.: CPF `XXX.XXX.XXX-XX` → senha `XXXXX` ou `XXXXXX`).

## 1. Método mais rápido e direto: pdftotext com flag `-upw`

O utilitário padrão `pdftotext` suporta a flag de senha de usuário (`-upw`), permitindo extrair diretamente o texto com colunas e tabelas alinhadas sem depender de scripts ou módulos Python adicionais:

```bash
pdftotext -upw <senha> -layout input.pdf /tmp/fatura_texto.txt
```

Exemplo prático:
```bash
pdftotext -upw XXXXX3 -layout "FATURA MENSAL.pdf" /tmp/fatura_amazon_layout.txt
```

## 2. Extração via Python (pypdf como fallback quando qpdf/pikepdf não estão disponíveis)

O ambiente pode não ter `qpdf` nem `pikepdf`. Verificar disponibilidade e usar o que estiver presente, na ordem:

```bash
# 1. Tentar qpdf (mais confiável, preserva estrutura)
qpdf --password=<SENHA> --decrypt input.pdf output.pdf

# 2. Tentar pikepdf (Python)
python3.12 -c "
import pikepdf
pdf = pikepdf.open('input.pdf', password='<SENHA>')
pdf.save('output.pdf')
"

# 3. Fallback: pypdf (quase sempre disponível)
python3.12 - << 'PY'
from pypdf import PdfReader, PdfWriter
reader = PdfReader("input.pdf")
if reader.is_encrypted:
    result = reader.decrypt("<SENHA>")
    # result 1 = user password, 2 = owner password
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.write("output.pdf")
PY
```

## Verificação prévia

Antes de tentar decriptar, confirmar que é realmente um PDF com senha:

```bash
pdfinfo input.pdf 2>&1 | grep -i encrypted
# ou
python3.12 -c "from pypdf import PdfReader; r=PdfReader('input.pdf'); print('encrypted:', r.is_encrypted)"
```

## Depois de decriptar

- **Sempre** extrair texto do PDF decriptado, não do original (`pdftotext -layout output.pdf`)
- Salvar o original criptografado como está — a senha continuará sendo necessária
- O PDF decriptado é temporário; apagar após extração (`rm /tmp/fatura_decrypted.pdf`)
- Nunca registrar a senha do CPF em arquivos Markdown
