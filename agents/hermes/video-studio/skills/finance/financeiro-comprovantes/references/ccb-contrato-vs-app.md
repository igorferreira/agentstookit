# CCB Contrato vs App — Reconciliação de valores

> **PITFALL — documentado em 05/08/2026 (CCB [REDACTADA] C6)**

## O problema

O contrato assinado (CCB Via Não Negociável) mostra valores ESTIMADOS calculados na data de assinatura. A cláusula 2.3 da CCB diz explicitamente que os valores se ajustam na data efetiva de liberação dos recursos.

O app do banco mostra os valores REAIS que podem divergir do contrato em:
- Data da 1ª parcela
- Valor da 1ª parcela
- Existência de carência (só seguro nos primeiros meses)

## Procedimento

1. **Extrair o contrato com `pdftotext`** — seguir `references/extracao-ccb-contrato.md`
2. **Anotar o que o contrato DIZ**: data 1ª parcela, valor estimado, amortização, juros, seguros
3. **Perguntar ao usuário o que o APP mostra**: abrir o app do banco, ver as parcelas futuras lançadas
4. **Confrontar e registrar a divergência** no HOME-EQUITY.md com tabela explícita:

```
| Campo | Contrato | App real | Delta |
|---|---|---|---|
| 1ª parcela | 10/Set/2026 | 10/Out/2026 | +1 mês |
| Valor 1ª parcela | R$ [REDACTADO] | R$ 4.333,63 | −R$ 55,81 |
```

5. **Usar os valores do APP no fluxo de caixa** — são os que o banco vai efetivamente cobrar
6. **Documentar a cláusula 2.3 como explicação** para futuras reconciliações

## Por que isso acontece

A CCB tem dois desembolsos (Primeiro e Segundo). O primeiro libera parte do crédito na assinatura. O segundo só é liberado após registro em cartório (averbação da alienação fiduciária). Enquanto o registro não sai, o banco cobra apenas os seguros (MIP+DFI). A 1ª parcela com amortização+juros só inicia após o Segundo Desembolso.

## Exemplo real (Usuário, C6 CCB [REDACTADA])

- Contrato assinado com valores de julho/2026
- Registro em cartório concluído ~agosto/2026
- App mostra: Ago e Set/26 = só seguro R$67,90. Out/26 = 1ª parcela completa R$4.333,63
- Contrato dizia: 1ª parcela 10/Set/2026, R$[REDACTADO]

## O que NÃO fazer

- ❌ Confiar cegamente no contrato sem verificar o app
- ❌ Usar os valores do contrato no fluxo de caixa sem confrontar com o app
- ❌ Assumir que não existe carência
