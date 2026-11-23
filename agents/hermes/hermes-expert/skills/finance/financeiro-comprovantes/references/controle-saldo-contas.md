# Controle de Saldo por Conta (`_saldos/`)

Pasta `~/MEGA/Comprovantes/_saldos/` — um arquivo markdown por conta bancária/carteira digital, com `INDEX.md` consolidando todas.

## Estrutura

```
_saldos/
├── INDEX.md           ← tabela consolidada: Conta, Arquivo, Saldo, Rendimento
├── SALDO_NUBANK.md    ← conta corrente Nubank
├── SALDO_INTER.md     ← conta corrente Inter (+ dívida do cartão referenciada)
├── SALDO_C6.md        ← conta corrente + CDB + Home Equity
├── SALDO_ITAU.md      ← conta corrente Itaú
├── SALDO_99PAY.md     ← carteira digital 99Pay
└── SALDO_BRASILCARD.md ← conta BrasilCard
```

## Padrão de cada `SALDO_<BANCO>.md`

```markdown
# 🟢 Saldo <Banco>

> 📅 Atualizado: DD/MM/AAAA

| Campo | Valor |
|---|---|
| 💰 Saldo (conta) | **R$ X,XX** |
| 📦 Investimentos | CDB/outros |
| 💳 Dívida vinculada | se aplicável |

---

## 📊 Histórico

| Data | Saldo | Observação |
|---|---|---|
| DD/MM | R$ X,XX | origem do dado |
```

## Atualização

- Atualizar sempre que o usuário enviar print de saldo (app de banco)
- OCR com `tesseract -l por` para extrair valores
- Atualizar data no topo e adicionar linha no histórico
- Atualizar também o `INDEX.md`
- Contas zeradas também têm arquivo (ex: Nubank R$ 0,00, Inter R$ 0,00)

## Pitfalls

- **CDB e conta corrente são seções diferentes no app C6** — pedir print das duas telas
- **Saldo zerado ≠ conta inexistente** — criar o arquivo mesmo com R$ 0,00
- **Dívida do cartão não subtrai do saldo da conta** — referenciar na ficha, não no saldo
- **99Pay tem rendimento 186% CDI** — registrar o rendimento, não apenas o saldo
