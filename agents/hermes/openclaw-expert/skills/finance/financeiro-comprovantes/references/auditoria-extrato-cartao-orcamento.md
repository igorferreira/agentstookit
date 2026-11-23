# 🛒 Análise de Extrato de Cartão vs. Metas do Orçamento Mensal

Este documento estabelece o procedimento padrão quando o usuário envia capturas de tela ou extratos parciais de lançamentos de cartão de crédito e solicita auditoria de atingimento de metas orçamentárias.

---

## 🎯 1. Pré-processamento e Extração de Lançamentos

1. **Varredura de OCR e Imagens:**
   - Em prints móveis com fundo claro e texto cinza/azul, usar `tesseract` com `--psm 6` ou `--psm 4` após recorte e thresholding (Pillow/PIL).
   - Extrair cada transação contendo: Data, Descrição/Estabelecimento, Valor (R$), e se é lançamento à vista ou parcela (`x/y`).

2. **Segregação de Componentes da Fatura:**
   - **Novos Gastos do Mês Corrente:** Compras e serviços contratados no ciclo de faturamento atual.
   - **Parcelas Residuais de Meses Anteriores:** Parcelamentos antigos que apenas continuam caindo na fatura (ex: `Parcela 5/10`).
   - **Estornos / Créditos:** Devoluções de IOF, cashback ou créditos de cancelamento.
   - **Pagamentos Anteriores:** Baixa da fatura do mês anterior.

---

## 📊 2. Classificação Orçamentária das Despesas

Classificar cada novo lançamento nas categorias do modelo de orçamento do usuário (`ORCAMENTO.md`):

| Categoria Orçamentária | Exemplos Comuns de Estabelecimentos / Lançamentos |
|---|---|
| **L5 — Gastos Livres (Lazer / Saídas)** | Bares, restaurantes, confeitarias, padarias/deli, lanches, conveniência, varejo, vestuário, entretenimento. |
| **L4 — Combustível / Transporte** | Postos de gasolina (`AUTO POSTO`), Uber, 99 Táxi. |
| **L1 / N2 — Telecomunicações** | Claro, Vivo. |
| **N1 / N4 / N5 — Contas Fixas de Casa** | Condomínio, Light, Naturgy (gás). |
| **N3 — Inteligência Artificial / Ferramentas** | OpenAI, Claude, Google One, etc. |
| **N7 — Serviços Domésticos** | Faxina, diarista, cozinheiro. |
| **Saúde / Farmácia** | Clínicas médicas (`JIM.COM`), farmácias, laboratórios. |
| **Pedaladas / Transferências de Crédito** | Transações de liquidez via RecargaPay / PicPay / PIX no crédito. |

---

## 🍽️ 3. Integração com o Índice de Restaurantes e Lazer

Quando forem identificados lançamentos em novos restaurantes, bares ou cafeterias:
1. Atualizar o arquivo de catálogo gastronômico em `~/MEGA/Documentos/lazer_interesses/restaurantes/INDEX.md`.
2. Registrar o nome do estabelecimento, endereço aproximado, valor pago, cartão utilizado e companhia (se informada).
3. Atualizar a tabela de preços médios e histórico de visitas.

---

## 📈 4. Cálculo de Atingimento do Orçamento

1. Somar o total de novos gastos correntes por categoria.
2. Comparar com o teto mensal planejado em `ORCAMENTO.md`:
   $$\% \text{ Atingido} = \left(\frac{\text{Gasto Realizado}}{\text{Teto Planejado}}\right) \times 100$$
3. Determinar o status:
   - 🟢 **Sob controle / Dentro da meta:** $\le 100\%$
   - 🟡 **Atenção / Próximo do limite:** $90\% \text{ a } 105\%$
   - 🔴 **Estourado / Acima do teto:** $> 100\%$
4. Atualizar o `ORCAMENTO.md` da competência mensal com os valores realizados e o saldo excedente ($\Delta$).
5. Se houver estouro significativo em categorias de gastos livres, registrar linha de alerta informativo/risco no `AVISOS.md`.
