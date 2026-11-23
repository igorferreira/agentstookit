# Cálculo de oferta salarial CLT (Brasil)

Método para converter um bruto de oferta em líquido, pacote de caixa e pacote anual — usado em dossiês de vagas. Calcular com script (nunca de cabeça), com as tabelas vigentes explicitadas.

## INSS progressivo (CLT, tabela anual vigente)

Faixas: 1.518,00 @ 7,5% · 1.518,01–2.793,90 @ 9% · 2.793,91–4.190,83 @ 12% · 4.190,84–8.157,41 @ 14%.

```python
def inss(base):
    if base >= 8157.41:
        return 113.85 + 114.83 + 167.63 + 555.32   # teto = 951,63
    fx = [(1518.00, .075), (2793.90, .09), (4190.83, .12), (8157.41, .14)]
    inc, r = 0.0, 0.0
    for lim, ali in fx:
        if base > inc:
            r += (min(base, lim) - inc) * ali; inc = lim
        else: break
    return round(r, 2)
```

## IRRF progressivo (base = bruto − INSS; tabelas mensais vigentes)

Faixas: ≤ 2.428,80 isento · ≤ 2.826,65 @ 7,5% (ded. 182,16) · ≤ 3.751,05 @ 15% (ded. 394,16) · ≤ 4.664,68 @ 22,5% (ded. 675,49) · acima @ 27,5% (ded. 908,73). Subtrair deduções por dependente quando aplicável. A faixa de isenção ampliada (até R$ 5.000/mês, com redutor parcial até R$ 7.350, vigente desde 2026) não muda brutos acima de R$ 7.350 de base.

## Pacote de caixa (o que Igor compara)

```
líquido = bruto − INSS − IRRF
pacote_mensal = líquido + VA/VR + auxílio_home_office + setup_único/12
pacote_anual  = 12 × pacote_mensal + (13º + férias + 1/3 em bruto)   # 13º+fé+⅓ = bruto × 4/3
sobra_mensal  = líquido + VA_cobrindo_alimentação − 4.000            # custo de vida
```

Para o PLR/variável: só soma ao pacote anual com histórico real de pagamento comprovado; senão listar como "não contar".

## Exemplo de referência (bruto R$ 14.000, sem dependentes)

INSS 951,63 · base IR 13.048,37 · IRRF 2.679,57 · **líquido 10.368,80**.

## Diferença vs bloco de rescisão da SKILL.md

O bloco de rescisão usa aproximações simplificadas (`INSS = min(bruto×0,10, …)`) adequadas para estimar verbas. Em análise de OFERTA usar o método progressivo real acima — a diferença passa de R$ 100/mês e muda o líquido entregue ao Igor.

## Onde guardar

Pasta da empresa em `~/MEGA/Documentos/oportunidades/<Empresa>/`, dossiê MD com a tabela do cálculo + banda de salários da empresa (Glassdoor) + veredito e perguntas para o recrutador.
