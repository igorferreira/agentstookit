# Fluxo de caixa detalhado com contas de consumo no crédito

## Quando usar

Quando o usuário pedir projeção de fluxo de caixa incluindo contas de consumo (luz, gás) que serão pagas via cartão de crédito (Itaú Signature ou Passaí).

## ⚡ Estratégia Dígio (cartão em negociação)

Se houver um cartão que **vai para negociação** (ex: Dígio), usar o limite dele para pagar contas de consumo via RecargaPay **antes** de usar os cartões mantidos. Isso preserva o fluxo de caixa dos cartões bons.

- Pague pelo app RecargaPay → PIX com QR code → selecionar o cartão Dígio como fonte
- Taxa RecargaPay: **3,99%** sobre boletos vencidos (confirmar se há taxa para boletos a vencer)
- O valor aparece na fatura do Dígio — que não será paga (vai pra negociação)
- **Resultado:** contas pagas, fluxo de caixa 100% preservado, custo zero real

⚠️ **Registrar todos os comprovantes** em `~/MEGA/Comprovantes/{ano}/{mes}/` com o padrão:
`AAAA-MM-DD_CONTA-{LUZ|GAS}-REF{MM}{AAAA}-R{VALOR}-COMPROVANTE-DIGIO.(jpg|md)`

## Workflow

### 1. Levantar contas atrasadas

- **Light**: verificar último comprovante de pagamento em `~/MEGA/Comprovantes/{ano}/{mes}/`. Histórico recente: ~R$ 771/mês (venc ~24 de cada mês).
- **Naturgy (gás)**: último comprovante. Histórico: ~R$ 110-120/mês (venc ~20 de cada mês). Referência é sempre do mês anterior (ref Jun vence 20/Jul).
- Confirmar com o usuário quantos meses atrasados e valores exatos se disponíveis.

### 2. Definir cartão de pagamento

Perguntar: **Signature (6651) ou Passaí (6698)?**

A partir do mês seguinte, adicionar ~R$ 881/mês (luz + gás) como despesa recorrente na fatura do cartão escolhido.

### 3. Estrutura da projeção

Para cada mês (Ago a Dez):

| Coluna | Fonte |
|---|---|
| **Parcelas** | Matriz de parcelamentos dos cartões mantidos |
| **C6** | Parcela SAC decrescente (~R$ 4.389 → R$ 4.349 ao longo de 4 meses) |
| **Total saídas** | Parcelas + C6 + novas contas no crédito |
| **Renda** | CLT líquido + VALLO |
| **Fluxo** | Renda − saídas |
| **Reserva** | Reserva anterior + fluxo |

### 4. Eventos sazonais

- **Dissídio:** data-base 1º/ago, reflete no contracheque de out/nov. Projetar ~4% de aumento sobre CLT + VALLO a partir de out.
- **13º salário:** 1ª parcela até 30/nov, 2ª até 20/dez. VALLO extra no 13º conforme histórico.

### 5. Apresentação

Entregar como tabela Markdown com:
- Uma linha por mês
- Reserva em negrito na última coluna
- Destaque visual (🟢/🟡/🔴) para fluxo positivo/neutro/negativo
- Nota sobre premissas (dissídio estimado, valores de conta pendentes de confirmação)
