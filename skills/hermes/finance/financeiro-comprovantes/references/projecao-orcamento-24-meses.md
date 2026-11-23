# Projeção Orçamentária de Longo Prazo (12-24 meses)

Quando o usuário pedir uma projeção de orçamento para 1-2 anos para verificar viabilidade de um compromisso financeiro.

## Estrutura do documento

1. **Renda mensal recorrente** — usar o contracheque real mais recente, subtrair itens pontuais (triênio retroativo, indenização especial) para estimar o líquido recorrente.

2. **Deduções fixas** — listar cada compromisso com valor, início, fim e tipo de amortização:
   - Empréstimos SAC: documentar a redução mensal da parcela (~R$ 40/mês para principal de R$ 100k a 1,70% a.m.)
   - Parcelamentos fixos (ex.: amigo, credor pessoal)
   - Cartões com parcelamento ativo

3. **Projeção mês a mês** — tabela com colunas: Mês | Renda | Dedução1 | Dedução2 | ... | Disponível | Custo vida | Folga
   - Incluir dissídios anuais (data-base da CCT, % estimado conservador de 4%)
   - Incluir redução SAC (diminui ~R$ 40/mês)
   - Marcar meses de mudança (início/fim de compromissos)

4. **Gráfico de folga** — visual ASCII mostrando a evolução da folga mês a mês

5. **Conclusão** — responder diretamente se o compromisso cabe no orçamento, qual o pior mês e quais riscos

6. **Riscos e mitigações** — tabela com riscos realistas e como mitigar cada um

## SAC — cálculo da redução mensal

Para empréstimos SAC (Sistema de Amortização Constante):
- Amortização = Principal ÷ Nº parcelas (fixa)
- Juros = Saldo devedor × Taxa mensal (decrescente)
- Redução mensal da parcela ≈ Amortização × Taxa mensal
- Exemplo: Principal R$ 108.720, 50 meses, 1,70% a.m. → redução ≈ R$ 108.720/50 × 0,017 ≈ R$ 37/mês

## Dissídio — quando projetar o aumento

- Data-base da CCT → o reajuste reflete no contracheque 1-3 meses depois
- Projetar aumento conservador de 4% (IPCA + pequeno ganho real)
- Aplicar o mesmo % ao VALLO BENEFÍCIOS (reajusta junto)
- Atualizar a projeção quando o contracheque com reajuste chegar
