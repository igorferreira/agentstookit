# Controle completo de cartões — 3 blocos

Quando o usuário pedir visibilidade de TODOS os cartões (inclusive zerados), gerar uma tabela de controle em 3 blocos:

## Estrutura

```
✅ A PAGAR (N cartões)
❌ NÃO PAGOS — Negociação (N cartões)
🟢 ZERADOS / CANCELADOS / BLOQUEADOS (N cartões)
```

## Regras

1. **NUNCA omitir cartões zerados.** Mesmo que não tenham ação pendente, o usuário quer ver que foram considerados.
2. Cada bloco com: #, Cartão, Final, Venc, Valor, Origem (CDB/Renda/Pix), Status.
3. Status deve ser binário e visual: ⬜ PAGAR (com data) ou ❌ NÃO PAGO ou 🟢 CANCELADO/ZERADO/BLOQUEADO.
4. Incluir linha de subtotal em cada bloco.
5. Adicionar seção de CAIXA com: CDB inicial → saídas → CDB final.
6. Incluir linha 👤 Paulo Guerra separada, fora da numeração de cartões.
7. Coluna Origem indica de onde sai o dinheiro: CDB, Renda, CDB+Pix, Empréstimo, BCB.

## Resumo visual (obrigatório no final)

```
[N] cartões (ver CONTROLES.md para a contagem atual — era 26 no levantamento original de 30/07/2026)
├── ✅ N a pagar + Paulo Guerra  R$ X
├── ❌ N não pagos               R$ Y
└── 🟢 N zerados                 R$ 0
─────────────────────────────────────
    CDB final                    R$ Z
```

## Pitfall

"NÃO PAGO" contém a substring "PAGO" — ao calcular totais programaticamente, usar correspondência exata, não `"PAGO" in status`. Use `status == "✅ A PAGAR"` ou `"NÃO PAGO" not in status`.
