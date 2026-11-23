---
data: {{DATA}}
tipo: comprovante
subtipo: nota-fiscal-mercado
valor: {{VALOR_TOTAL}}
mercado: {{MERCADO}}
chave_nfce: {{CHAVE_NFCE}}
fonte_extracao: {{FONTE}}
status: processado
---

# Nota Fiscal — {{MERCADO}} — R$ {{VALOR_TOTAL}}

**Data**: {{DATA}}
**Valor Total**: R$ {{VALOR_TOTAL}}
**Chave de Acesso NFC-e**: `{{CHAVE_NFCE}}`
**Fonte de Extração**: {{FONTE_DESCRICAO}}

## Itens

| Descrição | Qtd | Un | V. Unit | Total |
|---|---|---|---|---|
{{ITENS_TABELA}}

---

*Registrado em: {{TIMESTAMP}} via decodificar_nfce.py*
