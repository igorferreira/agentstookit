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
- **Sempre rodar `date` antes de responder** sobre vencimentos ou fluxo.
- **Passaí é crédito, não cash.** O complemento mercado de R$ 250 vai no cartão.
- **iFood sem teto vira rombo.** R$ 70 × 3/semana × 4,33 = R$ 909/mês. Usar cartão virtual com limite.
- **Orçamento sem dinheiro livre = receita pra frustração.** Reservar R$ 200-300/mês sem categoria.
- **Novo gasto no cartão → cascata de atualizações.** Quando o usuário registra uma compra no crédito (ex: restaurante), atualizar nesta ordem: (1) ficha do cartão, (2) pasta do mês da fatura, (3) seção relevante do orçamento (Lazer, Dinheiro Livre), (4) tabela de Consolidação Mensal (faturas ativos + CDB). O CDB final de todos os meses à frente é recalculado.
- **Gasto em restaurante → tracking automático.** Todo gasto com lazer/restaurante no crédito deve ser registrado também em `~/MEGA/Documentos/Restaurantes/INDEX.md` para construir média de preços por restaurante ao longo do tempo. Fluxo completo: OCR da notinha → cadastro do restaurante → comprovante no mês da fatura → atualização da ficha do cartão → cascata no orçamento (Pote 3 → CDB). Ver `financeiro-comprovantes` skill, referência `registro-gasto-restaurante-lazer.md`.
- **Raiz de comprovantes enxuta.** Apenas arquivos canônicos na raiz de `~/MEGA/Comprovantes/`. Arquivos de config de outros assistentes (CLAUDE.md) não pertencem ali. Fluxos e painéis vão em `_controles/`. Contratos em PDF vão na pasta mensal correspondente.

## 📁 Referências

- `references/3-potes.md` — Sistema de 3 potes com regras concretas, pitfalls e seção emocional
- `references/honorarios-advocaticios.md` — Como argumentar teto em honorários de advogado de negociação de dívidas
