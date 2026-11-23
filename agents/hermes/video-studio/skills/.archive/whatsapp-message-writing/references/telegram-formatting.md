# Formatação de respostas do Hermes → Igor no Telegram

Estabelecido em 03/09/2026 (correção explícita do Igor ao revisar respostas).

## Regra núcleo
NUNCA usar **tabelas Markdown** (`| ... |`) nas respostas do Hermes ao Igor no Telegram.
O Telegram não renderiza tabelas — viram gordura ilegível ("fica uma merda", nas palavras dele).

## O que usar no lugar de tabelas no Telegram
- Listas com marcadores (`•` ou `-`)
- `**negrito**` para rótulos-chave e valores
- Emojis para sinalizar categoria/seção (💰 📇 ✅ etc.)
- Linhas `campo: valor` simples, uma por linha (key:value)

## Formato de exemplo (aprovado)
```
✅ Financeiro (bem completo)
• CONTRACHEQUE.md (renda)
• MAPA-CUSTO-VIDA.md (despesas)
• FLUXO-CAIXA (projeção)

🆕 Faltou criar
• CONTROLE-DA-VIDA.md (índice-mestre)
```

## Escopo
- Aplica-se a **respostas do agente ao Igor** no chat Telegram (todo domínio: finanças, saúde, jurídico, etc.).
- Para mensagens destinadas a TERCEIROS via WhatsApp, ver `SKILL.md` (fenced `text` block + formatação WhatsApp nativa).
- Outros Markdown que o Telegram interpreta (negrito, itálico, code block, links) seguem OK.

## Pitfall
- NUNCA introduzir tabela para "slides de dados estruturados" apenas porque o dado é tabular — use key:value + bullets e preserve a leitura no mobile.
- Se uma tabela real for imprescindível (planilha), entregue como **arquivo** (XLSX/MD anexado), não como tabela inline no chat.