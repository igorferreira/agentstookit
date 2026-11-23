---
name: rescisao-clt-planejamento
description: Use when Igor asks for monthly estimates of Brazilian CLT termination amounts, comparing resignation, dismissal without cause, and optionally mutual agreement, including salary balance, notice, 13th salary, accrued/proportional vacation, FGTS, penalty, estimated deductions, and financial runway.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [rh, carreira, clt, rescisao, fgts, ferias, planejamento-financeiro]
    related_skills: []
---

# Planejamento de Rescisão CLT

## Objetivo

Produzir estimativas mensais auditáveis para Igor Ferreira, comparando quanto estaria disponível em cada modalidade de encerramento do vínculo CLT com a Noorden Services Ltda. e relacionando o resultado ao custo de vida líquido de **R$ 9.000 por mês**.

Esta habilidade serve para planejamento. Não substitui cálculo oficial do empregador, homologação, advogado trabalhista, contador ou conferência do TRCT.

## Quando usar

Use esta habilidade para:

- atualizar a projeção mensal de rescisão;
- comparar pedido de demissão e dispensa sem justa causa;
- simular acordo do art. 484-A da CLT, quando solicitado;
- estimar saldo de salário, aviso-prévio, 13º, férias e FGTS;
- calcular quantos meses do custo de vida a reserva rescisória cobriria;
- conferir um TRCT ou demonstrativo enviado por Igor.

Não apresente números exatos sem os dados mínimos. Identifique hipóteses e diferencie valor comprovado de valor projetado.

## Regra de execução do agente

Toda solicitação deve ser quebrada em tarefas pequenas, executadas **uma por vez**. Ao terminar, emitir relatório com:

1. tarefas realizadas;
2. arquivos criados ou atualizados;
3. valores calculados;
4. hipóteses usadas;
5. dados faltantes;
6. riscos e próximos passos.

## Dados obrigatórios

Manter os dados em:

`/home/igorferreira/MEGA/Documentos/carreira/rescisao_clt/dados-contrato.json`

Campos mínimos:

- salário bruto mensal atual;
- data de admissão na Noorden Services;
- data de referência ou data hipotética de desligamento;
- saldo/base rescisória do FGTS, preferencialmente do aplicativo FGTS;
- modalidade do FGTS: saque-rescisão ou saque-aniversário;
- períodos de férias vencidos, adquiridos e já gozados;
- início do período aquisitivo atual;
- médias de remuneração variável, horas extras, adicionais, bônus ou comissões;
- número de dependentes para IRRF;
- adiantamentos de 13º salário;
- descontos pendentes autorizados;
- modalidade de aviso-prévio em cada cenário.

Se algum campo estiver ausente, não inventar. Gerar uma lista de pendências e, se possível, uma faixa de valores.

## Cenários obrigatórios

### 1. Pedido de demissão

Considerar, conforme o caso:

- saldo de salário;
- 13º proporcional;
- férias vencidas/adquiridas não gozadas + 1/3;
- férias proporcionais + 1/3;
- possível desconto de até 30 dias de aviso-prévio se Igor não trabalhar e a empresa não dispensar o cumprimento;
- sem multa de 40% do FGTS;
- sem saque-rescisão do FGTS por esse motivo;
- sem seguro-desemprego.

Apresentar duas versões quando a decisão sobre aviso não estiver definida:

- pedido com aviso trabalhado ou dispensado sem desconto;
- pedido com desconto de 30 dias.

### 2. Dispensa sem justa causa

Considerar:

- saldo de salário;
- aviso-prévio trabalhado ou indenizado;
- aviso proporcional de 30 dias até um ano, acrescido de 3 dias por ano completo, limitado a 90 dias;
- projeção do aviso indenizado no tempo de serviço para férias e 13º quando aplicável;
- 13º proporcional;
- férias vencidas/adquiridas e proporcionais + 1/3;
- depósitos de FGTS faltantes sobre verbas aplicáveis;
- multa de 40% calculada preferencialmente sobre a **base para fins rescisórios** informada pelo FGTS, não apenas sobre o saldo visível;
- saque do FGTS condicionado à modalidade escolhida e às regras vigentes;
- possível seguro-desemprego, tratado separadamente e somente se os requisitos estiverem satisfeitos.

### 3. Extinção por acordo — opcional

Quando solicitado, considerar o art. 484-A da CLT:

- metade do aviso-prévio se indenizado;
- multa de 20% do FGTS;
- saque limitado a 80% do FGTS, observadas as regras vigentes;
- sem seguro-desemprego;
- demais verbas integralmente devidas.

## Componentes do cálculo

### Saldo de salário

`salário mensal / 30 × dias trabalhados no mês`

Incluir médias habituais quando comprovadas.

### Décimo terceiro proporcional

`remuneração-base × avos / 12`

Cada mês com pelo menos 15 dias computáveis conta como um avo. Tratar o 13º separadamente para INSS/IRRF.

### Férias

- período adquirido não gozado: remuneração + 1/3;
- período proporcional: remuneração × avos/12 + 1/3;
- período fora do prazo concessivo pode exigir pagamento em dobro; só aplicar após validar datas e situação real;
- descontar férias já gozadas ou pagas.

### Aviso-prévio

Na dispensa sem justa causa:

`30 + 3 × anos completos de serviço`, limitado a 90 dias (30 dias para menos de um ano; 33 dias ao completar um ano, 36 dias ao completar dois anos, e assim por diante).

No pedido de demissão, não aplicar aviso proporcional contra Igor automaticamente. Simular no máximo o desconto do aviso legal aplicável ao empregado mensalista, normalmente 30 dias, sujeito ao caso concreto e à convenção coletiva.

### FGTS

- depósito mensal ordinário: 8% da remuneração sujeita ao FGTS;
- incluir 13º salário na base de depósito quando aplicável;
- multa de dispensa sem justa causa: 40% da base rescisória;
- acordo do art. 484-A: 20%;
- pedido de demissão: 0%;
- usar extrato/base rescisória real sempre que disponível.

Não confundir:

1. saldo atual da conta;
2. base para fins rescisórios;
3. valor efetivamente sacável, especialmente no saque-aniversário ou quando houver antecipações.

## Estimativa líquida

Separar o relatório em:

1. **Verbas pagas pelo empregador**;
2. **FGTS e multa**;
3. **Seguro-desemprego potencial**;
4. **Total imediatamente acessível**;
5. **Valores bloqueados ou condicionais**.

Usar as tabelas oficiais de INSS e IRRF vigentes no mês da análise. Para 2026, consultar as fontes oficiais antes de executar. Não tributar automaticamente verbas indenizatórias; registrar o tratamento aplicado e marcar o líquido como estimativa.

## Segurança financeira

Usar como referência:

`custo_de_vida_liquido_mensal = R$ 9.000,00`

Calcular:

`meses_de_cobertura = total_imediatamente_acessivel / 9.000`

Produzir também uma leitura conservadora excluindo:

- FGTS bloqueado;
- seguro-desemprego ainda não aprovado;
- valores contestáveis;
- bônus, PLR ou remuneração variável não garantida.

## Procedimento mensal

1. Ler `dados-contrato.json`.
2. Confirmar a data de referência.
3. Conferir se salário, férias e FGTS foram atualizados.
   - Se houver novos contracheques, usar o salário-base mais parcelas fixas salariais recorrentes; não confundir vencimentos extraordinários de férias, 13º ou dissídio com remuneração mensal.
   - Reconstrução de FGTS por contracheques deve ser marcada como estimativa e nunca substituir silenciosamente o saldo e a base para fins rescisórios do aplicativo FGTS.
4. Ler a CCT vigente e verificar data-base, reajuste, aviso-prévio, adicionais por tempo de serviço, abonos e indenizações especiais.
5. Consultar regras e tabelas oficiais vigentes se o ano ou as normas mudaram.
6. Executar `scripts/calcular_rescisao.py`.
7. Separar no pedido de demissão:
   - saída imediata com dispensa do aviso sem desconto;
   - saída imediata com desconto de 30 dias;
   - aviso de 30 dias efetivamente trabalhado, cuja data final altera 13º e férias proporcionais.
8. Revisar manualmente as hipóteses, especialmente empréstimos de folha, dependentes e projeção do aviso sobre a data-base.
9. Salvar relatório em:

`/home/igorferreira/MEGA/Documentos/carreira/rescisao_clt/relatorios/AAAA-MM_RELATORIO-RESCISAO-CLT.md`

10. Atualizar o índice da pasta.
11. Emitir resumo final ao usuário.

## Fontes oficiais prioritárias

- CLT compilada: <https://www.planalto.gov.br/ccivil_03/decreto-lei/del5452compilado.htm>
- Lei nº 8.036/1990 — FGTS: <https://www.planalto.gov.br/ccivil_03/leis/l8036consol.htm>
- Lei nº 12.506/2011 — aviso-prévio proporcional: <https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/lei/l12506.htm>
- Tabela INSS: <https://www.gov.br/inss/pt-br/direitos-e-deveres/inscricao-e-contribuicao/tabela-de-contribuicao-mensal>
- Tabelas IRPF 2026: <https://www.gov.br/receitafederal/pt-br/assuntos/meu-imposto-de-renda/tabelas/2026>
- Seguro-desemprego: <https://www.gov.br/trabalho-e-emprego/pt-br/servicos/trabalhador/seguro-desemprego/seguro-desemprego-formal>

## Alertas obrigatórios

- Convenção coletiva pode alterar regras e benefícios.
- Valores de FGTS devem ser conferidos no extrato e na base para fins rescisórios.
- Saque-aniversário pode limitar o saque imediato do saldo na dispensa.
- Empréstimos com antecipação do saque-aniversário podem bloquear saldo.
- Datas de férias devem ser verificadas antes de classificar um período como simples ou em dobro.
- Benefícios, PLR, bônus, stock options e previdência privada exigem análise separada.
- O cálculo é estimativo e deve ser confrontado com o TRCT.

## Verificação final

- [ ] Data de admissão confirmada
- [ ] Salário bruto e médias confirmados
- [ ] Férias conferidas por período aquisitivo
- [ ] Base rescisória do FGTS conferida
- [ ] Modalidade de saque do FGTS confirmada
- [ ] Pedido de demissão com e sem desconto de aviso
- [ ] Dispensa sem justa causa calculada
- [ ] Acordo calculado somente se solicitado
- [ ] Tributos e descontos explicitados
- [ ] Cobertura do custo de vida de R$ 9.000 calculada
- [ ] Hipóteses e limitações registradas
- [ ] Relatório mensal salvo
