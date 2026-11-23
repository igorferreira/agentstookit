# Análise de Risco — Fluxo de Caixa

## Quando usar

Quando o usuário perguntar "tem risco de não cumprir?", "o plano está seguro?", "o que pode dar errado?", ou demonstrar preocupação com a viabilidade do plano financeiro após uma atualização.

## Formato

### 1. Começar com tranquilidade

Se o plano está estruturalmente sólido (CDB não zera, Gate 0 ok), iniciar com uma linha de tranquilidade: "Calma, [nome]. Os números estão no seu lado." ou equivalente. Depois entregar os dados.

### 2. Tabela de riscos — 3 níveis

| Nível | Emoji | Horizonte | O que incluir |
|---|---|---|---|
| ALTO | 🚨🔴 | Próximos 60 dias | Premissas não confirmadas, dependências frágeis, vencimentos iminentes sem comprovante |
| MÉDIO | ⚠️🟡 | 6 meses | Projeções incertas (dissídio), concentração de risco, dependências de terceiros |
| BAIXO | 🔮 | 2027+ | Cenários macro, reserva de emergência, acordos de negociação |

Cada risco deve ter: descrição curta, impacto se ocorrer (com número quando possível), e probabilidade (Alta/Média/Baixa).

### 3. Stress test

Tabela com **pior cenário realista** (2-3 coisas dando errado ao mesmo tempo):

| | Normal (X[n]) | Stress |
|---|---|---|
| CDB mínimo | R$ X | **R$ Y** |
| CDB zerou? | Não ✅ | **Não/SIM** |
| Meses de déficit | N | **N+M** |

Se mesmo no stress o CDB não zera, destacar isso como prova de robustez.

### 4. Mitigações

Listar o que já protege o plano (13º, Gate 0, fim de parcelamentos, cancelamento de despesas).

### 5. Ações imediatas

Checklist com `✅ Já feito` e `🔲 A fazer` — ações concretas que reduzem risco agora.

## Exemplo

```
## 🔴 Sim, tem riscos. Aqui estão, por ordem de perigo:

### 🚨 Risco ALTO — próximos 60 dias
| # | Risco | Se acontecer | Prob. |
|---|---|---|---|
| 1 | Faturas subestimadas | Déficit sobe R$ 3.377 | ⚠️ Alta |

### ⚠️ Risco MÉDIO
| # | Risco | Impacto |
|---|---|---|
| 5 | Dissídio < 4% | −R$ 135/mês CLT |

### 📊 Stress test
| | Normal | Stress |
|---|---|---|
| CDB mínimo | R$ 23.438 | R$ 16.500 |
| CDB zerou? | Não ✅ | Não ✅ |

### ⚡ O que você pode fazer AGORA
1. ✅ Já feito: cancelar seguro
2. 🔲 Puxar cronograma dos 5 cartões sem info
```

## Pitfalls

- Não fazer terrorismo — se o CDB não zera nem no stress, dizer claramente.
- Números exatos sempre. "~R$ 3.000" é aceitável, "uns 3 mil" não.
- Distinguir risco real de ansiedade. Se o usuário está preocupado mas o plano está sólido, mostrar os números e explicar POR QUE está sólido.
- Nunca sugerir cortar assinaturas de IA (ferramentas de trabalho).
