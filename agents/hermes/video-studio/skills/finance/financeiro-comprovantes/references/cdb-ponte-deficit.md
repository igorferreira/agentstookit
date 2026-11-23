# CDB como ponte — exibição de déficit coberto por reserva

## Quando usar

Quando a projeção de fluxo de caixa tiver meses com déficit (renda < faturas + C6), mas com reserva de CDB suficiente para cobrir.

## Padrão de exibição

Igor prefere **visão realista**: mostrar o déficit e quem cobre, sem esconder meses negativos.

### Tabela de fluxo

Cada mês deve ter:

| Mês | Renda | Faturas | C6 | Déficit | 🏦 CDB usou | 📦 CDB saldo |
|---|---|---|---|---|---|

- **Déficit**: valor negativo em vermelho (🔴)
- **CDB usou**: quanto foi sacado do CDB naquele mês (`−R$ X.XXX` nos meses de déficit, `—` nos meses positivos)
- **CDB saldo**: saldo do CDB após o saque (ou após o aporte, nos meses positivos)

### Seção de alerta no topo

Antes da projeção detalhada, incluir um bloco de resumo:

```
## 🏦 Reserva CDB — A ponte até Jul/2027

| | Valor |
|---|---|
| 📦 CDB inicial | R$ 21.131 |
| 💸 Total sacado em X meses | R$ 25.613 |
| 🔻 CDB mínimo | R$ 13.141 (Mai/27) |
| 🟢 CDB zerou? | NÃO |
```

### Timeline visual (ASCII)

Incluir um gráfico de evolução do CDB:

```
Ago/26  R$ 21.131 ●●
        +R$ 13.731 (sem faturas)
Set/26  R$ 34.862 ●●●●  ← pico
        −R$ 10.096 (CDB cobre)
Out/26  R$ 24.766 ●●●
        ...
Mai/27  R$ 13.141 ●   ← 🔻 fundo
        ...
Dez/28  R$ 105.260 ●●●●●●●●●●  🏆
```

## Regras

1. **Nunca esconder déficits** — mostrar com 🔴 e explicitar "CDB cobre"
2. **CDB saldo nunca pode ser negativo** — se a projeção zerar o CDB, alertar como cenário inviável
3. **Total sacado ≠ CDB inicial − CDB mínimo** — há meses com aporte (positivos) entre os meses de déficit. Somar apenas os déficits
4. **Atualizar o CDB saldo após cada mês**, não apenas nos meses de déficit
5. O termo "ponte" comunica que é temporário: o CDB cobre até os parcelamentos acabarem
