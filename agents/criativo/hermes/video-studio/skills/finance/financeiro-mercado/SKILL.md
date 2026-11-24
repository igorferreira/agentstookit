---
name: financeiro-mercado
description: "Use when capturing, extracting, and analyzing grocery/supermarket receipts (NFC-e notes) to track prices by product/store and build historical price databases."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [financeiro, supermercado, notas-fiscais, nfc-e, precos, analise, brasil]
    related_skills: [financeiro-comprovantes, ocr-and-documents]
---

# Financeiro: Mercado (Controle de Preços)

## Overview

Use esta skill para capturar notas fiscais de supermercado via foto, extrair itens estruturados, armazenar com histórico de preços, e analisar variações de preço por supermercado.

Pastas base autorizadas:

- `~/MEGA/Comprovantes/` — armazenamento de comprovantes originais (integrado com `financeiro-comprovantes`)
- `~/MEGA/Documentos/Mercado/` — catálogo de produtos, índices de preço, análises

Perfil recomendado:

`finance-senior`

## When to Use

Use quando:

- Usuário enviar **foto de nota fiscal de supermercado** via Telegram (`@finance`)
- Precisar **catalogar novo produto** (normalizar entre diferentes marcas/supermercados)
- Precisar **analisar histórico de preços** (ranking de mercado mais barato, variações anômalas)
- Precisar **comparar preço de item** entre supermercados
- Rodar **auditoria semanal/mensal** de preços

## Fase 1: Captura e Armazenamento (Versão Atual)

### 1.1 Fluxo de captura via Telegram

```
Usuário enviar foto via @finance
        ↓
Decodificar QR Code (NFC-e)
        ├─ Sucesso: buscar SEFAZ → itens estruturados ✓ (preferido)
        └─ Falha: OCR do cupom (fallback)
        ↓
Normalizar descrição → produto canônico (com confirmação do Usuário se necessário)
        ↓
Armazenar em ~/MEGA/Comprovantes/AAAA/AAAA_MM_MES/
├─ AAAA-MM-DD_NOTA-MERCADO-NOMELOJA-R$VALOR.jpg (original)
└─ AAAA-MM-DD_NOTA-MERCADO-NOMELOJA-R$VALOR.md (metadados)
        ↓
Adicionar linha em ~/MEGA/Documentos/Mercado/precos_itens.csv
```

### 1.2 Estrutura de dados (Fase 1)

**Em `~/MEGA/Documentos/Mercado/`:**

- `INDEX.md` — visão geral (mercados cadastrados, ticket médio)
- `CATALOGO_PRODUTOS.csv` — mapeamento produto crú → canônico (categoria, marca, unidade)
- `precos_itens.csv` — histórico item-a-item (data, mercado, produto, preço, R$/kg, referência)

**Compatibilidade com `financeiro-comprovantes`:**

O comprovante original (`*.jpg` + `*.md` irmão) continua em `~/MEGA/Comprovantes/AAAA/MES/` — não muda nada do padrão existente. O campo `chave_nfce` (44 dígitos) no `.md` vincula à análise de preços.

## Roadmap Futuro (Fases 2+)

**Fase 2**: Catálogo de produtos + normalização inteligente
**Fase 3**: Análise histórica + ranking de mercado mais barato
**Fase 4**: Alertas de variação de preço + cron jobs
**Fase 5**: Sazonalidade / otimização de cesta
**Fase 6**: WhatsApp como canal adicional (após validar qual integração é a padrão)

## Não use para

- Alterar arquivos fora de `~/MEGA/Comprovantes/` e `~/MEGA/Documentos/Mercado/` sem autorização
- Deletar comprovantes originais em caso de dúvida
- Inventar dados de preço sem suporte de foto/OCR/SEFAZ
