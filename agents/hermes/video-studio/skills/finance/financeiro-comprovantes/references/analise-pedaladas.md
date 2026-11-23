# Análise de Pedaladas Financeiras

## Quando usar

Quando Igor perguntar se "vale a pena pedalar" ou "pedalar a X%", ou quiser usar limite de cartão para cobrir déficits de curto prazo até um evento de liquidez (13º salário, dissídio, etc.).

## O que é pedalada

Pedalar = usar o limite disponível de um cartão de crédito para fazer Pix crédito (via RecargaPay, app do banco, etc.), injetar o dinheiro no fluxo de caixa para cobrir déficits, e pagar a fatura do cartão no mês seguinte — repetindo até o evento de liquidez.

Custo típico: ~5% de taxa por ciclo (Pix crédito).

## Fluxo de análise

### 1. Identificar o déficit

```python
# Do fluxo de caixa atual (X##)
deficit_set = abs(saldo_set)  # ex: R$ 3.315
deficit_out = abs(saldo_out)  # ex: R$ 4.736
deficit_total = deficit_set + deficit_out
```

### 2. Identificar limites disponíveis

Para cada cartão ATIVO (NÃO de negociação):

| Cartão | Limite total | Utilizado | Disponível |
|---|---|---|---|
| Carrefour 3825 | ❓ | ❓ | R$ 4.541 |
| Luiza 9105 | R$ 8.055 | R$ 5.535 | R$ 2.520 |
| Nubank 3033 | R$ 11.321 | ❓ | ❓ |

Cartões de NEGOCIAÇÃO (Inter, PAN, Digio): Igor geralmente veta usar para pedalada. Confirmar antes de incluir.

### 3. Calcular líquido por ciclo

```python
limite_total = sum(disponivel)  # soma dos disponíveis
liquido_por_ciclo = limite_total * 0.95  # 5% taxa
custo_por_ciclo = limite_total * 0.05
```

### 4. Simular mês a mês

Para cada mês com déficit:
1. Pix crédito → líquido entra como "renda extra"
2. Cobre déficit → CDB não mexe (ou mexe menos)
3. A dívida do Pix vai pra fatura SEGUINTE do cartão
4. No mês seguinte: pagar fatura (original + Pix) → libera limite → novo Pix
5. Repetir até o evento de liquidez (13º, dissídio)

### 5. Calcular custo total e CDB final

```python
custo_total = custo_por_ciclo * num_ciclos
cdb_final_com_pedalada = cdb_inicial - deficits_nao_cobertos + superavit_evento
cdb_final_sem_pedalada = # do fluxo base
```

### 6. Comparar e decidir

| | Sem pedalada | Com pedalada |
|---|---|---|
| CDB mínimo | R$ X | R$ Y |
| CDB pós-evento | R$ A | R$ B |
| Custo total | R$ 0 | R$ C |

**Regra de decisão:**
- Se CDB com pedalada > CDB sem pedalada NO MÊS DO EVENTO → vale a pena
- Se CDB com pedalada < CDB sem pedalada → NÃO vale (a taxa comeu o benefício)
- Exceção: se CDB mínimo sem pedalada estiver perigosamente baixo (< R$ 5.000), a pedalada pode se justificar por segurança, mesmo com custo

## Pitfalls

- **Pedalar com cartão de negociação**: Igor geralmente veta. A lógica: aumentar dívida de cartão que já vai pra acordo de 280 dias. Se fizer, calcular o custo REAL pós-desconto (ex: 50% desconto = metade do valor pedalado).
- **Custo composto**: cada ciclo tem taxa de ~5%. Dois ciclos = ~10% sobre o valor. Três ciclos = ~15%. O custo sobe rápido.
- **Limite disponível ≠ limite total**: verificar no app o disponível REAL. O limite total menos utilizado pode não ser preciso se houver parcelamentos futuros já comprometidos.
- **Cartão com parcelamentos**: se o cartão tem parcelas futuras, o limite disponível pode ser menor que o cálculo simples.
- **Não contar com evento incerto**: só pedalar até evento CONFIRMADO (13º é certo, dissídio é certo, crédito Caixa NÃO é certo).

## Exemplo real (07/08/2026)

Pedalada Carrefour 3825 (R$ 4.541 disponível) × 2 ciclos (Set–Out/26):
- Custo: R$ 454
- CDB Nov/26 sem pedalada: R$ 19.428
- CDB Nov/26 com pedalada: R$ 17.028
- **Conclusão: NÃO valeu a pena.** O custo da taxa + bola de neve da fatura reduziu o CDB pós-13º.
