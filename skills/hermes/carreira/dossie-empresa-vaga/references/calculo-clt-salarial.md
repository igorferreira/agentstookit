# Cálculo CLT centavo-exato (líquido, anual, caixa) — Igor

Parâmetros vigentes VALIDADOS (última validação: fim de 2026, batendo com líquidos já confirmados do Igor). **Revalidar contra a tabela vigente quando passar para outro ano ou se a legislação mudar.**

## Parâmetros

- INSS: teto de contribuição R$ 951,63 (salários ≥ ~R$ 8.157 já pagam o teto — aplicar R$ 951,63 direto para faixas sênior).
- IRRF: alíquota máxima 27,5% com dedução R$ 908,73 sobre a base (base = fixo − INSS), 0 dependentes.
- Fórmula: `irrf = round((fixo − inss) × 0,275 − 908,73, 2); líquido = fixo − inss − irrf`.
- Ano = 13 salários (12 fixos + 13º). 1/3 de férias bruto = fixo / 3.

## Verificação de sanidade (números que batem)

- 14.000 → INSS 951,63 · base IR 13.048,37 · IRRF 2.679,57 · **líquido 10.368,80**
- 15.000 → líquido **11.093,80** · 12.000 → líquido **8.918,80**

## Saída esperada (o que o Igor quer ver)

1. Linha de cima para baixo por oferta: INSS, base IR, IRRF, líquido mensal.
2. Anual: fixo anual bruto (13 salários) · **líquido anual (13 × líquido)** · benefícios em caixa/mês e /ano (VA/VR ×12 — vales NÃO recebem 13º) · setup único amortizado no ano 1 (÷12 na comparação mensal).
3. **Caixa anual ano 1 = líquido anual + benefícios ×12 + setup** — a métrica de decisão entre ofertas.
4. Sobra mensal sobre o custo de vida de R$ 4.000.
5. Delta entre as duas ofertas no fim (bruto, líquido, caixa).

## Regras

- Escrever o script em arquivo e rodar — nunca calcular de cabeça; validar reproduzindo um líquido já confirmado antes de confiar nos demais.
- PLR/variável só entra com prova de pagamento real (histórico); senão listar como linha separada "não contabilizada".
- VA/VR nem sempre é pago em 13º/férias — usar ×12, nunca ×13, a menos que o empregador confirme.
- CLT vs PJ: PJ pelo mesmo valor é perda de ~R$ 2,5–3k/mês em direitos — nunca comparar fixo com fixo entre modalidades.
- Anúncio de vaga oficial (Gupy etc.) é a fonte dos valores de benefício; a proposta escrita é a fonte final — se mudar, refazer a conta e avisar o Igor.