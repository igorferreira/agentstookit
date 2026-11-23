# Projeção de Acordos, Desconto Real e Plano Master de Quitação de Cartões (PDD)

## 1. Contexto & Fundamentos Regulatórios

Quando um cliente entra em inadimplência no Brasil em cartões de crédito:
1. **Meses 1 a 3 (0 a 90 dias):** O banco aplica juros rotativos de 15% a 22% ao mês e aciona cobrança ostensiva (call center). As propostas oferecem "descontos" nominais baixos (10% a 20%) sobre um saldo já inflado, ou refinanciamentos parcelados com taxas altas.
2. **Meses 4 a 6 (120 a 180 dias):** A cobrança interna é encerrada e a carteira é repassada para assessorias de cobrança terceirizadas.
3. **Meses 9 a 12 (280 a 360 dias — Janela de Ouro):** Por força da **Resolução CMN/BCB nº 4.966**, a instituição financeira é obrigada a provisionar 100% do saldo contábil como perda (**PDD — Provisão para Devedores Duvidosos / Crédito Liquidado contra Prejuízo**). Contabilmente, o banco já amortizou o prejuízo e busca qualquer recuperação de caixa nos feirões (**Serasa Limpa Nome, Acordo Certo, Consumidor.gov.br**), gerando descontos nominais de **80% a 95%**.
4. **24+ Meses (Janela Especial para Grandes Volumes — ex: Banco Inter):** Dívidas maiores que foram cedidas ou provisionadas há 2 anos atingem o patamar máximo de desconto histórico, podendo ser liquidadas por 5% a 15% do saldo contábil inflado.

---

## 2. A Armadilha do Desconto Nominal vs. Desconto Real

Bancos e securitizadoras vendem a ilusão de "90% de desconto" sobre um saldo que eles mesmos inflaram artificialmente com juros rotativos compostos.

### Fórmula Matemática do Desconto Real

$$\text{Desconto Real (\%)} = 1 - \left( \frac{\text{Valor Final do Acordo}}{\text{Valor de Face Original de Entrada em Default}} \right)$$

* **Valor de Face Original:** É o valor exato utilizado pelo titular no ciclo de entrada em atraso (ex: faturas de Agosto/2026), excluindo encargos de mora futuros e rotativo acumulado pós-atraso.
* **Critério de Validação do Acordo:** Todo acordo proposto só deve ser aceito se o **Desconto Real for positivo e represente no mínimo 40% a 75% de economia sobre o dinheiro que o usuário efetivamente utilizou**.

---

## 3. Matriz de Cenários Padrão para Fichas de Cartões em Negociação

Ao modelar a ficha individual (`_fichas/FICHA_CARTAO_BANCO_NOME_FINAL.md`), incluir 4 cenários:

| Cenário de Negociação | Desconto Nominal Feirão | Faixa de Pagamento à Vista (R$) | Desconto Real s/ Face Original | Veredito Estratégico |
|:---|:---:|:---:|:---:|:---|
| ❌ **Desfavorável (0–180 dias)** | 20% a 50% | R$ [Valor Elevado] | **Negativo ou < 20%** | **RECUSAR SUMARIAMENTE**. Queima caixa sem desconto real. |
| 🟡 **Aceitável (240–300 dias)** | 70% a 80% | R$ [Valor Médio] | **30% a 45% real** | Avaliar apenas se houver urgência de crédito ou restrição. |
| 🟢 **Ótimo (280–360 dias - Janela de Ouro)** | 85% a 92% | R$ [Teto Recomendado] | **50% a 65% real** | **ALVO DE EXECUÇÃO**. Quitar via Serasa / Consumidor.gov.br à vista. |
| 🌟 **Excelente (Feirão / 18–24 meses)** | 93% a 96% | R$ [Piso Histórico] | **70% a 80% real** | Liquidação perfeita com impacto patrimonial mínimo. |

---

## 4. Playbook de Execução Master

1. **Blindagem Inicial:** Silêncio tático durante os primeiros 180 dias. Bloqueio de chamadas e não atendimento de cobranças telefônicas.
2. **NUNCA Parcelar Acordos:** O parcelamento reativa a dívida, quebra o desconto e reembute juros. Acordo só se celebra e paga **À VISTA (PIX / Boleto bancário único)**.
3. **Canais Oficiais:**
   * Plataforma Serasa Limpa Nome e Acordo Certo (consulta digital mensal sem contato telefônico).
   * Notificação via `Consumidor.gov.br` direcionada à Ouvidoria do banco emissor após 280 dias de atraso.
4. **Condição Prévia de Pagamento:**
   * Obtenção da **Minuta / Termo de Quitação Integral** com renúncia a saldos remanescentes.
   * Validação do CNPJ do favorecido no boleto bancário (conferir se pertence ao banco emissor ou à securitizadora oficial).
   * Solicitação e arquivo da **Declaração de Quitação Anual de Débitos (Lei Federal 12.007/2009)**.
