# Envio de Dossiê PDF ao Advogado (Dr. Israel)

## Quando usar
Quando Igor pedir para enviar um dossiê financeiro resumido ao advogado (Dr. Israel Júnior Gomes Machado, `advisraelmachado@gmail.com`), na thread existente "Dossiê financeiro — Igor Ferreira".

## Workflow completo

### 1. Compor o Markdown
Criar `/tmp/dossie-resumido-dr-israel-<data>.md` com:
- Posição de caixa (CDB, conta corrente)
- Home Equity (dados do contrato)
- Custo de vida detalhado (fixo + lazer)
- Renda mensal (CLT + VALLO + outras fontes)
- Cartões mantidos (tabela com final, emissor, parcelamentos até)
- Cartões para negociação (tabela com valor de face, status)
- Projeção de caixa (meses de déficit, CDB mínimo, CDB final)

**Regra:** CDB deve refletir apenas o disponível — descontar dívidas pessoais reservadas (ex: Paulo Guerra R$10.000). Explicar o desconto no email.

### 2. Converter Markdown → HTML
Usar Python com regex para converter markdown básico em HTML, com CSS inline para estilização profissional:

```python
import re
md = re.sub(r'^### (.+)$', r'<h3>\1</h3>', md, flags=re.MULTILINE)
md = re.sub(r'^\*\*(.+?)\*\*', r'<strong>\1</strong>', md)
# ... tables, blockquotes, etc.
```

CSS recomendado:
- `font-family: 'Segoe UI', Arial, sans-serif`
- Cores: `#1a5276` (títulos), `#2c3e50` (corpo)
- Tabelas: `border-collapse: collapse`, header com fundo `#2c3e50` e texto branco
- Blockquotes: fundo `#ebf5fb`, borda esquerda azul

### 3. Gerar PDF com wkhtmltopdf

```bash
wkhtmltopdf --encoding UTF-8 /tmp/dossie-israel.html \
  /home/igorferreira/MEGA/Comprovantes/2026/2026_08_AGOSTO/2026-08-03_DOSSIE-RESUMIDO-DR-ISRAEL.pdf
```

Salvar na pasta do mês corrente em `~/MEGA/Comprovantes/YYYY/YYYY_MM_MES/`.

### 4. Enviar email com PDF anexo via Himalaya

```bash
cat << 'EOF' | himalaya template send
From: Igor Ferreira <igorferreirabr@gmail.com>
To: advisraelmachado@gmail.com>
Subject: Re: Dossiê financeiro — Igor Ferreira (26 cartões, dívida R$ 89 mil)

Dr. Israel,

Segue em anexo o PDF com o dossiê resumido atualizado.

[Explicar correções ou mudanças relevantes aqui]

Atenciosamente,
Igor Ferreira

<#multipart type=related>
<#part type=application/pdf filename="/caminho/absoluto/do/arquivo.pdf" name="Nome-Amigavel.pdf"><#/part>
<#/multipart>
EOF
```

### 5. Verificar envio

```bash
himalaya envelope list --folder "Sent" --page-size 3
```

Confirmar que o ID aparece e o assunto está correto.

## Pitfalls

1. **CDB value**: sempre confirmar com Igor o valor exato a reportar. Ele pode querer descontar dívidas pessoais.
2. **Thread subject**: usar EXATAMENTE o mesmo subject da thread original. Buscar com `himalaya envelope list --folder "Sent"`.
3. **MML attachment**: o path no `<#part>` deve ser absoluto, e o `name` é o nome que aparece no email.
4. **Encoding**: sempre usar `--encoding UTF-8` no wkhtmltopdf para caracteres brasileiros.
5. **Tabelas**: converter manualmente com regex — pandoc não está disponível no ambiente.
