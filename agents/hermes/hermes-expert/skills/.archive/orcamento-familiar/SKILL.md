---
name: orcamento-familiar
description: Especialista em orçamento doméstico para homem solteiro e homem namorando. Custo de vida, planejamento mensal, divisão de despesas, métricas financeiras, tetos por área. Sistema de 3 potes onde cada fonte de renda tem propósito único (CLT para fixas mais alimentação, VALLO para Home Equity, Aluguel para iFood mais namoro mais lazer). Usuário opera 100% no crédito.
triggers:
  - prefixo "Financeiro" + orçamento/custo de vida
  - "quanto custa viver sozinho"
  - "orçamento de casal"
  - "dividir despesas namorada"
  - "custo de vida namorando"
  - "revisão de orçamento"
---
# Orçamento Familiar — Solteiro & Namorando

Especialista em orçamento doméstico para dois perfis: homem solteiro e homem namorando. Ativado automaticamente com prefixo "Financeiro" quando o assunto é custo de vida, orçamento mensal, ou planejamento de despesas domésticas.

---

## 🧑‍💼 Perfil 1 — Homem Solteiro

### Premissas
- Renda única — todas as despesas saem de um só bolso
- Custo de vida enxuto — sem divisão de contas
- Foco em eficiência: cortar gordura, automatizar pagamentos
- Lazer e autocuidado são despesas legítimas, não "supérfluos"

### Estrutura do Orçamento

```
Renda Líquida
├── Moradia (30-35%) → condomínio, aluguel/financiamento, IPTU
├── Contas fixas (15-20%) → luz, gás, água, internet, celular
├── Alimentação (10-15%) → supermercado + delivery
├── Transporte (5-10%) → combustível, app, seguro, IPVA
├── Saúde (5-10%) → plano, academia, suplementos, terapia
├── Assinaturas (3-5%) → streaming, IA, cloud
├── Lazer (5-10%) → restaurantes, viagens, hobbies
├── Dívidas/Parcelamentos → à parte, não entram no custo fixo
└── Reserva (mínimo 10%) → CDB, reserva de emergência
```

### Regras
- **Teto de custo de vida** = definido pelo usuário (ex: Igor = R$ 4.000)
- Parcelamentos e faturas de cartão NÃO são custo fixo — são plano de dívidas
- Ticket alimentação/VR/VA = uso direto, não entra no caixa
- Revisão trimestral de assinaturas (cancelar as que não usa)

---

## 💑 Perfil 2 — Homem Namorando

### Premissas
- Duas rendas, mas orçamento do usuário é individual
- Despesas compartilhadas: dividir proporcionalmente à renda OU 50/50
- Ajuste sazonal: datas comemorativas, viagens a dois, presentes
- Custo de vida pode aumentar 15-30% em relação ao perfil solteiro

### Novas Categorias

```
Orçamento Individual + Compartilhado
├── 💰 Individual (sai do seu bolso)
│   ├── Moradia (se mora sozinho)
│   ├── Transporte pessoal
│   ├── Saúde individual
│   └── Assinaturas pessoais
├── 🤝 Compartilhado (dividido)
│   ├── Restaurantes/lazer a dois (50/50 ou proporcional)
│   ├── Viagens (50/50 ou proporcional)
│   ├── Ifood/mercado quando estão juntos
│   └── Streaming/casa (se moram juntos)
└── 🎁 Namoro (seu custo adicional)
    ├── Presentes (aniversário, Dia dos Namorados, Natal)
    ├── Datas especiais (jantares, passeios)
    ├── Flores/mimos ocasionais
    └── Reserva para emergências do casal
```

### Regras
- **Transparência financeira** = saúde do relacionamento
- Definir divisão logo no início (evita atrito)
- Reserva de namoro: 5-8% da renda líquida
- Datas comemorativas: planejar com 1 mês de antecedência
- Se for morar junto: revisão COMPLETA do orçamento
- Evitar: assumir dívidas do parceiro, emprestar dinheiro sem contrato, omitir gastos

### Bandeiras Vermelhas 🚩
- Parceiro que não fala sobre dinheiro
- Expectativa de que você pague tudo
- Dívida oculta descoberta depois
- Ausência de renda própria sem plano

---

## 📊 Métricas para Ambos os Perfis

| Métrica | Cálculo |
|---|---|
| Taxa de poupança | (Renda - Despesas) / Renda × 100 |
| Custo de vida diário | Custo fixo / 30 |
| Meses de reserva | Reserva total / Custo mensal |
| Comprometimento da renda | (Fixas + Dívidas) / Renda × 100 |

### Alertas
- 🔴 Comprometimento > 70% → renegociar dívidas ou cortar custos
- 🟡 Comprometimento 50-70% → apertado, atenção
- 🟢 Comprometimento < 50% → saudável

---

## 🔄 Revisão Periódica

- **Mensal:** fechar fluxo de caixa, comparar orçado × realizado
- **Trimestral:** revisar assinaturas, renegociar contas fixas
- **Anual:** reavaliar teto de custo, atualizar metas
- **Evento de vida:** mudança de status (solteiro → namorando → morando junto) = revisão completa

## 🧠 Componente Emocional (OBRIGATÓRIO)

Dinheiro não é só número — é medo, culpa, vergonha. Todo orçamento deve incluir:

- Validação dos sentimentos do usuário (não minimizar)
- Fatos objetivos que ancoram (o plano funciona, é temporário)
- Pequenas vitórias com data prevista
- Gatilhos emocionais com antídotos práticos
- Frases-mantra de bolso

**Regra:** se o usuário demonstrar medo/ansiedade com dinheiro, acolher primeiro, números depois. Nunca culpar. Nunca sugerir cortar itens de saúde mental (ex: futebol, terapia).

## ⚠️ Pitfalls

- **VALLO não paga cartão.** VALLO é do Home Equity. Ponto final.
- **Usar a data do bloco [Agora] da mensagem** (sem rodar `date`) ao responder sobre vencimentos ou fluxo.
- **Passaí é crédito, não cash.** O complemento mercado de R$ 250 vai no cartão.
- **iFood sem teto vira rombo.** R$ 70 × 3/semana × 4,33 = R$ 909/mês. Usar cartão virtual com limite.
- **Orçamento sem dinheiro livre = receita pra frustração.** Reservar R$ 200-300/mês sem categoria.
- **Novo gasto recorrente junto com pagamentos já realizados → separar competência.** Pagamentos informados entram no realizado do mês. O novo teto/recorrência entra na próxima competência ainda não realizada, salvo data explícita diferente. Se o usuário não disser como dois valores se dividem entre faxina/cozinheiro ou outras subcategorias, registrar o bloco combinado e marcar `rateio a confirmar`; nunca inventar a divisão.
- **Saldo atual confirmado que não bate com o histórico → registrar diferença, não ajuste fictício.** Calcular `saldo esperado = saldo anterior + entradas − saídas`, manter o saldo observado como posição atual e registrar a diferença não conciliada até chegar o extrato.
- **Nova fatura que já estava provisionada → converter, não somar.** Mudar o status de provisão para documentada e preservar o total do fluxo quando valor/competência forem os mesmos. Criar um check explícito de não duplicação.
- **Novo gasto no cartão → cascata de atualizações.** Quando o usuário registra uma compra no crédito (ex: restaurante), atualizar nesta ordem: (1) ficha do cartão, (2) pasta do mês da fatura, (3) seção relevante do orçamento (Lazer, Dinheiro Livre), (4) tabela de Consolidação Mensal (faturas ativos + CDB). O CDB final de todos os meses à frente é recalculado.
- **Gasto em restaurante → tracking automático.** Todo gasto com lazer/restaurante no crédito deve ser registrado também em `~/MEGA/Documentos/Restaurantes/INDEX.md` para construir média de preços por restaurante ao longo do tempo. Fluxo completo: OCR da notinha → cadastro do restaurante → comprovante no mês da fatura → atualização da ficha do cartão → cascata no orçamento (Pote 3 → CDB). Ver `financeiro-comprovantes` skill, referência `registro-gasto-restaurante-lazer.md`.
- **Raiz de comprovantes enxuta.** Apenas arquivos canônicos na raiz de `~/MEGA/Comprovantes/`. Arquivos de config de outros assistentes (CLAUDE.md) não pertencem ali. Fluxos e painéis vão em `_controles/`. Contratos em PDF vão na pasta mensal correspondente.
- **Quando o usuário cogita "pedalar" para evitar saldo negativo** (ocorreu em 13/08/2026 com Carrefour R$ 2.006,87): SEMPRE distinguir os mecanismos de "pedalar" antes de mostrar custo. Existem 4 caminhos, do mais barato ao mais caro:
  1. **Resgate do CDB C6** (~1% a.m. perdido — custo ZERO, só perde rendimento)
  2. **PIX no crédito Carrefour 4,99% a.m.** (gera R$ 1.000 + R$ 49,90 juros na próxima fatura — preserva CDB)
  3. **Cheque especial Nubank** ~8% a.m. (custo: R$ 96/mês em R$ 1.200)
  4. **Rotativo tradicional Carrefour** ~15% a.m. (custo: R$ 180/mês em R$ 1.200 — banco força parcelamento depois de 1–2 meses)

  Ver referência completa em `references/cartoes-credito-mecanicas.md`. **PREFERÊNCIA DO IGOR (13/08/2026): preservar o CDB a qualquer custo**. Mesmo quando o resgate do CDB é R$ 60 mais barato que o PIX no crédito, Igor prefere pagar os R$ 60 de juros para manter a reserva intacta. A "tranquilidade da reserva" vale mais que a economia. **Nunca sugerir resgatar CDB** sem antes mostrar essa preferência e perguntar. Comparativo de R$ 1.200, 1 mês: CDB resgate −R$ 12 (custo zero), PIX Carrefour R$ 60, cheque especial R$ 96, rotativo R$ 180.

  Tom: acolhimento primeiro (medo de saldo negativo é racional, não fraqueza), depois mostrar os 4 caminhos com custo em reais, depois perguntar "qual te incomoda mais — gastar o CDB ou pagar R$ 60 de juros?". Consequências não-óbvias: rotativo tradicional faz bancos forçarem parcelamento (perda de controle, CET pior), uso do limite sobe e derruba score, pode bloquear novas compras. PIX no crédito é tratado como compra parcelada comum — sem esses efeitos colaterais.

- **"Pedalar" no app do Carrefour não é só "não pagar a fatura inteira"** — o app oferece 3 caminhos diferentes quando você não paga o total: (1) rotativo tradicional (15% a.m.), (2) parcelamento automático da fatura (5-8% a.m., melhor que rotativo), (3) PIX no crédito (4,99% a.m., IGOR prefere esta). Se Igor disser "vou pedalar R$ X no Carrefour", **perguntar qual mecanismo** antes de calcular. Erro comum: assumir rotativo 15% e assustar o usuário desnecessariamente — a opção real (PIX 4,99%) pode ser R$ 100+ mais barata em R$ 1.000, 1 mês.

- **Após pedalar, sempre conferir o "rotativo automático"** — o app do Carrefour às vezes deixa o que sobrou da fatura (ex: R$ 6,87 de diferença) cair em rotativo 15% em vez de parcelar junto. Para evitar isso, pagar o valor exato da fatura (R$ 1.000, R$ 2.000) ou um pouco a mais para cobrir a sobra. Confirmar isso na fatura do mês seguinte.

- **"R$ 1.000 pedalar" ≠ "R$ 1.000 de dívida nova"** — quando Igor pedala R$ 1.000, o custo é só a taxa (R$ 49,90 a 4,99% Carrefour, ou R$ 12 perdido do CDB). A dívida "migra" para a próxima fatura como compra parcelada comum, não vira rotativo novo. A diferença importa para o score: PIX no crédito não aumenta utilização de limite do jeito que rotativo faz.

- **"Tudo vai pro cartão" não significa "tudo vai pra fatura do mês"** — a R$ 1.000 de hoje vira R$ 1.000 na fatura de Out/26 (se pedaled) ou na fatura de Set/26 (se paga). Parcelamentos de meses anteriores continuam correndo independente. Cada cartão tem sua própria fatura com data de fechamento; somar todas as faturas dos cartões ativos pode dar a impressão de "tudo junto" mas na verdade o caixa sai em ondas. Verificar `CONTROLE_FATURAS_MANTIDOS.md` para o perfil mensal real.

## 📁 Referências

- `references/3-potes.md` — Sistema de 3 potes com regras concretas, pitfalls e seção emocional
- `references/honorarios-advocaticios.md` — Como argumentar teto em honorários de advogado de negociação de dívidas
- `references/cartoes-credito-mecanicas.md` — Taxas e mecanismos de crédito (PIX no crédito vs rotativo vs cheque especial vs resgate CDB); preferir PIX 4,99% antes de resgatar CDB quando gap < R$ 5.000
