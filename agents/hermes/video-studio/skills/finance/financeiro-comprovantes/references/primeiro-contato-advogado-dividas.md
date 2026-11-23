# Primeiro Contato com Advogado — Portfólio de Dívidas

Quando Igor inicia contato com um novo advogado para renegociação de dívidas (via WhatsApp ou email), preparar resposta seguindo este padrão.

## Perguntas típicas do advogado

1. Valor total aproximado da dívida
2. Há quanto tempo está em atraso
3. Para quais bancos deve

## Regras para a resposta

### 1. Apresentar APENAS os cartões em negociação (não pagos)

Igor mantém 8 cartões ativos (pagos) e ~7 cartões em negociação (não pagos). A resposta para o advogado deve listar **somente os cartões que NÃO serão pagos** — agrupados por banco emissor, com o valor da dívida.

NÃO incluir:
- Cartões ativos/mantidos (Nubank, Passaí, Signature, Luiza, Amazon, Carrefour, Atacadão, Porto Seguro)
- Home Equity (é dívida garantida, entra em passo posterior)
- Empréstimo consignado (desconta em folha)
- Empréstimo pessoal (Paulo Guerra) — só mencionar separadamente

### 2. Agrupar por banco/emissor

```markdown
🏦 **Banco PAN** (2 cartões)
→ Méliuz: R$ 12.164 — atrasado desde 06/08
→ Buscapé: R$ 6.723 — atrasado desde 01/08
```

### 3. Mencionar negativação se existir

Se Igor já estiver negativado por algum credor (ex.: RecargaPay), incluir essa informação.

### 4. Formatar duas versões

- **`.md` completo**: registro histórico com tabelas, salvo em `2026/2026_MM_MES/AAAA-MM-DD_ESCRITORIO-CONTATO.md`
- **`.txt` pronto pra colar**: sem tabelas Markdown, com emojis, pronto pra WhatsApp, mesmo nome com sufixo `-WHATSAPP.txt`

### 5. Separar se é segunda opinião ou substituição

Se Igor já tem outro advogado (Dr. Israel), perguntar se o novo é segunda opinião ou substituição. Se for segunda opinião, NÃO mencionar o advogado anterior na resposta.

## Exemplo de resposta WhatsApp

```
Minha dívida total gira em torno de R$ 145.000, dividida assim:

💳 Cartões de crédito em atraso/negociação: ~R$ 83.500
São 7 cartões em 5 instituições

🏠 Home Equity C6: R$ 100.000
📄 Empréstimo consignado: ~R$ 12.000
👤 Empréstimo pessoal: R$ 10.000

⏰ Atrasos:
RecargaPay — R$ 20.958, venceu 10/07 (1 mês, já estou negativado)
Banco PAN — Méliuz R$ 12.164 (desde 06/08) + Buscapé R$ 6.723 (desde 01/08)
Bradescard — Casas Bahia R$ 9.536 (em atraso)
Banco Inter — R$ 31.910
Banco Digio — R$ 2.165

🏦 Bancos envolvidos na negociação:
RecargaPay, Banco PAN, Bradescard, Banco Inter, Banco Digio
```

## Fontes de dados

- Fichas dos cartões: `_fichas/FICHA_CARTAO_*.md`
- Cartões em negociação: `_controles/CONTROLE_FATURAS_MANTIDOS.md` (seção "Cartões em negociação")
- Status de negativação: memória do Igor, confirmar verbalmente
