# Extração de CCB — Cédula de Crédito Bancário

## Técnica de extração

CCBs de bancos brasileiros (C6, Itaú, etc.) são PDFs com texto pesquisável. Extrair com `pdftotext` diretamente — sem OCR:

```bash
pdftotext '/path/para/ccb.pdf' - | head -120
```

Campos críticos a localizar (normalmente nas primeiras 3 páginas):

| Campo | Seção típica | Exemplo |
|---|---|---|
| Principal | II.A | R$ [REDACTADO] |
| Valor Líquido | II.B | R$ 100.000,00 |
| Tarifas financiadas | II.C | Avaliação + Registro |
| IOF financiado | II.E | R$ 3.413,59 |
| Juros (a.m.) | II.J | 1,7% ao mês |
| Prazo (meses) | II.K | 50 meses |
| Vencimento final | II.K | 10/Ago/2030 |
| CET (a.a.) | II.L | 30,09% ao ano |
| Parcela estimada | II.M | R$ [REDACTADO] |
| Amortização | II.M(i)(a) | R$ 2.343,98 |
| Juros (1ª parcela) | II.M(i)(b) | R$ 1.976,99 |
| Seguro MIP | II.M(i)(c) | R$ 42,97 |
| Seguro DFI | II.M(i)(d) | R$ 25,50 |
| Sistema amortização | II.M(ii)(c) | SAC |
| 1ª parcela | II.M(ii)(a) | 10/Set/2026 |
| Forma pagamento | II.M(i) | Débito em Conta |
| Garantia | Título | Alienação Fiduciária de Imóvel |

## Caso concreto: CCB C6 nº 004505 (Usuário)

- **Credor**: Banco C6 S.A.
- **Emitente**: Usuário
- **Principal**: R$ [REDACTADO] (inclui tarifa avaliação R$ 2.183,54 + registro R$ 3.122,60 + IOF R$ 3.413,59)
- **Líquido**: R$ 100.000,00
- **Sistema**: SAC
- **Juros**: 1,70% a.m. (pré-fixado, 22,4197% a.a.)
- **Prazo**: 50 meses
- **Parcela inicial**: R$ [REDACTADO] (R$ 2.343,98 amortização + R$ 1.976,99 juros + R$ 68,47 seguros)
- **1ª parcela**: 10/Set/2026
- **Vencimento final**: 10/Ago/2030
- **CET**: 30,09% a.a. / 2,1854% a.m.
- **Garantia**: Alienação fiduciária — [ENDEREÇO-REDACTADO] 405, Anil, Rio de Janeiro/RJ
- **Conta débito**: C6 Bank, Agência 1, Conta XXXXXX-X
- **Arquivo**: `~/MEGA/Documentos/Emprestimo/1. ccb - vn.pdf` (26 páginas, 1,2 MB)

## Discrepâncias típicas entre relato verbal e contrato

Ao confrontar o que o titular relata com o documento assinado:

1. **Principal**: o titular tende a arredondar para cima ou incluir mentalmente taxas como "parte do empréstimo"
2. **Nº de parcelas**: frequentemente inflado na memória
3. **Valor da parcela**: o titular frequentemente omite seguros (MIP/DFI) que podem adicionar R$ 60–70/mês
4. **Carência**: o titular conta do desembolso; o contrato conta da assinatura
5. **Tabela**: Price vs. SAC — confusão comum

Regra: o contrato assinado prevalece. Atualizar o dossiê com os dados extraídos do PDF, não com o relato verbal.
