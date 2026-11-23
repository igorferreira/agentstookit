# Veículo — templates

## Abastecimento

Use este template ao criar o arquivo Markdown de um novo abastecimento:

```markdown
# Abastecimento [COMBUSTÍVEL] — Fiat Punto ELX 2010 (KRK2101)

## Identificação

| Campo | Valor |
|---|---|
| Data | YYYY-MM-DD |
| Veículo | Fiat Punto ELX 1.4 2010 |
| Placa | KRK2101 |
| Combustível | [gasolina comum / aditivada / Shell V-Power / etanol] |
| Posto | [nome do posto] |
| Volume | XX L |
| Preço por litro | R$ X,XX |
| Total calculado | R$ X.XXX,XX |
| Odômetro na ocasião | XXX.XXX km |

## Observações

- [divergências, confirmações, dados fornecidos pelo usuário, etc.]
```

## Fechamento de ciclo

```markdown
# Fechamento de ciclo — [COMBUSTÍVEL] — [POSTO]

| Dado | Resultado |
|---|---|
| Volume | XX L |
| Distância | XXX, X km |
| Consumo | X,XX km/l |
| Equivalente | X,XX l/100 km |
| Custo por km | R$ X,XX |

Comparação com ciclo anterior: [incluir ressalvas sobre condições de direção]
```
