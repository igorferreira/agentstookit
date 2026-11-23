# Negociação de Parcelamento com Amigo/Credor Pessoal\n\n> ⚠️ **Regra de modelagem:** no fluxo de caixa e nos cenários, modelar SEMPRE como **pagamento integral à vista na data informada pelo usuário**. Só mudar para parcelamento depois que o credor aceitar explicitamente. O default é \"não parcelou\". Isso evita superestimar a folga mensal com parcelas que podem não se concretizar.\n\nQuando o usuário tiver dívida com pessoa física (amigo, familiar) e precisar propor parcelamento, apresentar uma proposta que mostre ser **melhor para o credor** que receber à vista e aplicar em renda fixa.

## Cálculo da rentabilidade real para o credor

1. **Calcular a TIR mensal do parcelamento** — resolver `valor à vista = soma(parcela / (1 + r)^n)` para `n` parcelas
2. **Anualizar:** `(1 + r)^12 - 1`
3. **Comparar com 100% CDI** (verificar taxa atual)

### Fórmula aproximada para parcelas iguais

Para `n` parcelas de valor `P` com total `n × P` sobre principal `V`:
- Se `n` for pequeno (≤12), a TIR mensal aproximada é `r ≈ 2 × (n×P/V - 1) / (n+1)`
- Anualizar e comparar com CDI

### Exemplo real: 10× R$ 1.100 = R$ 11.000 sobre R$ 10.000

```
TIR mensal ≈ 1,77%
TIR anual ≈ 23,4% a.a.
CDI ≈ 14% a.a. → 100% CDI ≈ 14% a.a.
Conclusão: rentabilidade 67% maior que 100% CDI
```

## Estrutura da proposta

1. **Mensagem WhatsApp** — tom amigável e transparente:
   - Oferecer as duas opções (à vista ou parcelado)
   - Mostrar que o parcelado é MELHOR pra ele que aplicar no CDI
   - Explicar em linguagem simples ("quase o dobro do CDI, sem imposto, sem risco")
   - Dar liberdade de escolha ("se preferir à vista, transfiro amanhã sem problema")

2. **Conta detalhada** — à parte, pra ter na mão se ele perguntar:
   - Opção A: À vista + aplicar no CDI (com imposto de renda)
   - Opção B: Parcelado (com TIR real)
   - Tabela comparativa: total recebido, rentabilidade, liquidez, imposto, risco, comodidade

3. **Respostas prontas pra objeções** — tabela "se ele disser X, responda Y"

## Cuidados

- Nunca prometer o que não pode pagar — verificar antes na projeção de 24 meses
- O parcelamento precisa caber na folga mensal com margem
- Se o amigo precisar do dinheiro, não insistir — pagar à vista
- Formalizar por escrito (contrato simples de gaveta ou WhatsApp como evidência)
