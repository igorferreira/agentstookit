# Tracking de Cenários e Análises

## Estrutura

```
~/MEGA/Comprovantes/YYYY/_Analises/
├── INDEX-CENARIOS.md              ← tracking de TODOS os cenários X(N)
├── AAAA-MM-DD_ANALISES-<TOPICO>.md ← análises individuais
├── AAAA-MM-DD_ACOLHIMENTO.md       ← registros de acolhimento
└── cenarios/
    ├── fluxo_x12.json
    ├── fluxo_x13.json
    └── fluxo_xN.json
```

## INDEX-CENARIOS.md

Deve conter:

1. **Evolução X10→X(N)**: tabela com data, evento, CDB mínimo, CDB final, delta
2. **Matriz de faturas**: cartões × meses (Ago–Dez), marcando ❓ para não mapeado
3. **Premissas fixas**: comuns a todos os cenários
4. **Análises de pedalada**: tabela com data, cartão, limite, conclusão
5. **Arquivos JSON**: lista dos cenários salvos

## Quando criar novo X(N)

- Nova fatura mapeada (OCR de captura de app) → +1 no X
- Correção de valor (ex: Paulo Guerra R$ 3.175 → R$ 10.000) → +1 no X
- Cenário hipotético (what-if) → +1 no X, marcado como ⬜ Hipotético

## Quando criar análise (sem novo X)

- Comparação de estratégias (Opção 1 vs 2 vs 3)
- Simulação de pedalada
- Análise de "vale a pena?"

## Regras

- Cenário base (produção) é sempre o último X(N) sem flag "hipotético"
- Cenários hipotéticos têm `"cenario": "hipotético"` no JSON
- NUNCA apagar JSONs antigos — são histórico
- Toda análise concluída ganha MD + PDF com data no nome
