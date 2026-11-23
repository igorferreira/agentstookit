# Auditoria cruzada de dossiê financeiro

Quando o dossiê estiver completo, antes de gerar o PDF final e entregar, executar esta verificação de consistência numérica.

## Regra de ouro

**Soma dos valores em "O que VAI pagar" + "O que NÃO vai pagar" deve ser exatamente igual à dívida total declarada na Seção 2.**

```
total_pago (6.1) + total_nao_pago (6.2) = divida_total (Seção 2)
```

Diferença aceitável: **R$ 0,00**.

## Procedimento

### 1. Conferir cada valor individual contra a tabela-mestra

Os valores na Seção 6 (plano de ação) devem vir da tabela da Seção 3, não de estimativas. Para cada grupo como "Méliuz, Carrefour, PicPay, C&A, Digio, Atacadão":

- Pegar o valor exato de cada cartão na tabela da Seção 3
- Somar com precisão de centavos
- Substituir qualquer "~R$ X.XXX" pelo valor calculado exato

### 2. Verificar totais agregados

Rodar script de verificação:

```python
# Extrair valores da Seção 6 e Seção 2
# Verificar: sum(6.1 pago) + sum(6.2 não_pago) == total_divida

total_pago = sum(valores_6_1)
total_nao_pago = sum(valores_6_2)
total_divida = cartoes_agosto + recargapay + paulo_guerra

assert abs(total_pago + total_nao_pago - total_divida) < 0.01, \
    f"Discrepância: R$ {total_pago + total_nao_pago - total_divida:.2f}"
```

### 3. Verificar cobertura de recursos

```
cdb_apos_fase1 = cdb - fase1_cdb
disponivel_fase2 = renda_mensal_disponivel + cdb_apos_fase1
assert disponivel_fase2 >= fase2_custo, f"Fase 2 descoberta em R$ {fase2_custo - disponivel_fase2:.2f}"
```

### 4. Verificar consistência de percentuais

- Cobertura CDB: `cdb / total_divida * 100` — conferir que o % no dossiê está correto
- Déficit: `total_divida - disponivel_mensal` — conferir valor exato
- Meses para quitar: `total_divida / disponivel_mensal` — conferir arredondamento
- Capacidade pós-C6: `disponivel_mensal - parcela_c6` — conferir valor exato

## Pitfalls

### Estimativas agrupadas não batem com a tabela

O erro mais comum: agrupar cartões pequenos com "~R$ X.XXX" sem verificar a soma real na tabela-mestra. Exemplo real:

- Dossiê dizia "~R$ 7.480" para 6 cartões (Méliuz + Carrefour + PicPay + C&A + Digio + Atacadão)
- Soma real: R$ 704,98 + R$ 3.721,40 + R$ 800,13 + R$ 407,10 + R$ 1.117,97 + R$ 420,83 = **R$ 7.172,41**
- Discrepância: R$ 307,59

**Regra:** nunca usar "~" em valores do plano de ação. Todo valor deve ser exato e rastreável à tabela da Seção 3.

### Encoding do pdftotext causa falsos negativos

`pdftotext -layout` pode corromper acentos. Para verificação de conteúdo no PDF, usar `pdftotext -raw`.

### Cobertura de recursos parece OK mas tem gap

O CDB cobre a Fase 1, mas a nota de rodapé pode ter um erro de redação que sugere gap onde não existe. Exemplo: "CDB: R$ 39.000 − R$ 10.000 (Paulo) = R$ 29.000 livres" — isso sugere que só R$ 29.000 estão disponíveis, quando na verdade os R$ 39.000 inteiros estão disponíveis e a conta correta é R$ 39.000 − R$ 29.914,72 = R$ 9.085,28. A redação deve refletir o uso real, não uma subtração prévia arbitrária.
