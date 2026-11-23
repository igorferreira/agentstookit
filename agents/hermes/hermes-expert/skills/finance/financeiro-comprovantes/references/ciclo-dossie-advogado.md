# Ciclo completo: reconciliação → dossiê → PDF → email ao advogado

Quando o usuário pedir "atualiza o dossiê pro advogado" ou "envia pro Dr. Israel", execute o ciclo completo:

## Gatilhos

- "atualiza o dossiê pro advogado"
- "envia o dossiê atualizado"
- "manda pro Israel"
- "preciso enviar tudo que fizemos"

## Ciclo completo (6 passos)

### 1. Consolidar status de pagamentos

```bash
find ~/MEGA/Comprovantes/2026/ -name "*COMPROVANTE*" | sort
```
Cruzamento: comprovantes × CONTROLE_PAGAMENTOS.md → o que foi pago, o que foi absorvido, o que está em negociação.

### 2. Montar a tabela de absorções (💀)

Cada pagamento feito com Inter/Dígio:
- Sai do grupo "mantidos"
- Entra no grupo "negociação"
- Aumenta o total da dívida de negociação daquele emissor

### 3. Atualizar o dossiê (.md)

Seções obrigatórias (ordem canônica):
1. Resumo executivo + "O que mudou desde o último dossiê"
2. Situação atual: mantidos PAGOS + absorções + CDB preservado
3. Cartões para negociação (agrupados por bloco: Inter, PAN, demais)
4. Parcelamentos futuros (só dos mantidos)
5. Projeção financeira (renda, reserva, evolução)
6. O que esperamos do Dr. Israel (meta, cronograma, simulação)
7. Observações finais

### 4. Gerar PDF

```bash
pandoc DOSSIE-ADVOGADO-CARTOES.md -t html | sed 's/<table>/<table style="width:100%;border-collapse:collapse;">/g' > /tmp/dossie-body.html
# Injetar em template HTML com CSS branco
wkhtmltopdf --encoding UTF-8 --no-background --page-size A4 /tmp/dossie-final.html DOSSIE-ADVOGADO-CARTOES.pdf
```

### 5. Localizar thread de email com o advogado

```bash
himalaya envelope list -f "[Gmail]/E-mails enviados" | grep -i "dossi"
```
Pegar o ID da mensagem mais recente. O subject da thread é o mesmo desde o primeiro envio.

### 6. Enviar email com PDF anexo

Usar MML para anexar o PDF:
```
From: Usuário <SEU-EMAIL@gmail.com>
To: advisraelmachado@gmail.com
Subject: Re: [subject original da thread]

[Resumo das mudanças em bullet points]

<#part filename=/caminho/absoluto/DOSSIE-ADVOGADO-CARTOES.pdf name=Dossie-Usuário-Ferreira-V3.pdf><#/part>
```

Enviar com: `cat email.txt | himalaya template send`

## Pitfalls

- O sent folder do Gmail em português é `[Gmail]/E-mails enviados`, não `[Gmail]/Sent Mail`
- Os IDs de mensagem mudam entre sessões — sempre relistar antes de referenciar
- O PDF deve ser gerado com `--no-background` e CSS `background: #fff` explícito
- O nome do arquivo anexo no MML deve ser curto e sem espaços (ex: `Dossie-Usuário-V3.pdf`)
- Anexo no MML requer caminho ABSOLUTO no parâmetro `filename=`
