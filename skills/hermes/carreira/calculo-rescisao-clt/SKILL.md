---
name: calculo-rescisao-clt
description: Use quando Igor pedir cálculo de rescisão ou verbas CLT.
version: 1.1.0
author: hermes
license: MIT
metadata:
  hermes:
    tags: [Carreira, CLT, Rescisão, Financeiro]
    related_skills: [himalaya, atualizar-controles, planejamento-financeiro]
---

# Cálculo de Rescisão CLT (Noorden/HDI)

## When to Use

Acionar quando Igor pedir: cálculo/estimativa de rescisão, verbas rescisórias, aviso prévio, férias/13º proporcionais, multa de FGTS ou simulação de cenários de desligamento (sem justa causa, pedido de demissão, acordo 484-A).

Classe de trabalho recorrente: produzir estimativa de verbas rescisórias com aritmética conferida, premissas explícitas e registro canônico. Todo valor entregue é BRUTO e CONDICIONAL — o TRCT oficial é a única fonte de líquido.

## Procedimento

1. **Base salarial:** ler `~/MEGA/Documentos/carreira/SALARIO-CANONICO-NOORDEN.md` (soma das rubricas do contracheque mais recente) e conferir a soma com Decimal. Quando o total impresso no contracheque divergir da soma das rubricas, usar a soma como base provisória e citar a divergência centavo-exata no relatório — nunca escolher um dos dois em silêncio.
2. **Buscar só o que falta no e-mail:** holerites de competências já arquivadas estão em `carreira/rescisao_clt/contracheques/`; procurar no Gmail apenas a competência em curso (a folha do mês fecha ~no último dia útil — um holerite buscado antes disso NÃO existe ainda; verificar o cache de envelopes antes de concluir ausência). VALLO Benefícios não envia e-mail: o valor vem do canônico. Receita de varredura de evidência de verbas (pastas da empresa + ZapSign + contracheques PDF) em `references/evidencia-verbas-email.md`.
3. **Aplicar as regras fixas de `~/MEGA/Regras/carreira.md`:** VALLO é pacote percebido e NÃO entra em salário, aviso, férias, 13º, FGTS ou verbas (só compõe a renda mensal perdida, em linha separada); seguro-desemprego não entra na conta.
4. **Calcular com Decimal (ROUND_HALF_UP), nunca float** — o usuário audita centavos. Cada verba em função da base; cada dia de saldo salarial = base/30.
5. **Avos por projeção do aviso indenizado:** o aviso indenizado projeta o fim do contrato (data de comunicação + dias de aviso). 13º: avos jan–dez, contando cada mês projetado que o contrato cubra ≥15 dias. Férias proporcionais: avos do período aquisitivo vigente (conta o mês civil com ≥15 dias dentro da projeção; o mês de aniversário do contrato conta 0 se menos de 15 dias decorridos). Férias vencidas + 1/3 só se o período aquisitivo anterior não foi quitado — marcar como condicional e subtrair o valor do total se pago.
6. **Aviso pela CCT, não pela CLT:** a CCT FEAAC dá 30 dias + 3 por ano, até 90 (com 3+ anos de casa = 39 dias). Produzir sempre a sensibilidade com aviso de 30 dias — a empresa pode não aplicar a CCT. Analisar cláusulas especiais (abonos condicionados, PLR) antes de incluir qualquer verba extra.
7. **FGTS separado do TRCT — Igor é OPTANTE pelo saque-aniversário (com antecipação):** na dispensa sem justa causa ele saca APENAS a multa de 40% (fgts.gov.br); o saldo da conta NÃO é sacável — nem a parte livre da antecipação. Voltar ao saque-rescisão = desistência no App FGTS + carência de 25 meses + quitação das antecipações. Pedido de demissão não gera multa. Receita completa da multa em `references/fgts-multa-saque-aniversario.md` — pontos que definem o resultado: (a) a base legal é o HISTÓRICO COMPLETO de depósitos corrigidos (art. 18 §1º Lei 8.036/90; TST IRR 255), não o saldo atual — saques-aniversário já feitos NÃO reduzem a base; (b) apresentar SEMPRE dois cenários de depósito rescisório — padrão (8% sobre TODAS as verbas do TRCT) e conservador (8% só sobre o saldo de salário) — a diferença passa de R$ 2.000; (c) quando Igor avisar que mandará o saldo atualizado depois, entregar a fórmula fechada multa = 0,4 × (S + depósitos mensais + depósito rescisório) com S como única variável, e recalcular/reemitir quando o valor chegar; (d) quando o extrato Caixa chegar, o campo "VALOR PARA FINS RESCISÓRIOS" é a base real que substitui S + M — ver receita em `references/fgts-multa-saque-aniversario.md`.
8. **Entregável:** Markdown em `carreira/rescisao_clt/relatorios/YYYY-MM-DD_RELATORIO-RESCISAO-*.md` com: tabela de verbas por cenário, memória aritmética linha a linha, sensibilidades (dias de saldo, aviso 30×39, acordo 484-A se relevante) e seção de pendências que só o TRCT resolve (tipo/data de desligamento, avos reais, IRRF/INSS, consignado, férias quitadas). Quando Igor pedir também PDF e/ou e-mail, seguir a receita de `references/entrega-pdf-email.md` (PDF via Chrome CDP; envio via himalaya com anexo base64 e corpo em prosa).
   - **Planilha** ("planilha que resume e detalha"): xlsx salvo em `carreira/rescisoes/<empresa>/` com convenções excel-author — células AZUIS = input com Comment citando a fonte, derivados como FÓRMULA viva, named ranges (SALARIO_BASE, FINS_RESCISORIOS...), abas Resumo/Verbas/FGTS/Cenarios/Descontos/Pendencias/Checks, verba condicional destacada em amarelo; rodar LibreOffice `--convert-to xlsx` para cachear valores, conferir Checks=TRUE e cenários centavo-a-centavo contra o relatório, e copiar a versão recálculada por cima da original.
   - **E-mail "padrão HTML"** (Igor pede para si mesmo quando não nomeia destinatário): .eml multipart/alternative (text/plain prosa + text/html com estilos INLINE em cada elemento, tabelas `<table role=presentation>`), headers 100% ASCII (Subject via Header utf-8 encode), enviar com `himalaya message send < arquivo.eml` (STDIN, nunca path posicional) e ANTES do envio renderizar o HTML com `google-chrome --headless --screenshot` + vision_analyze — colunas de valor estreitas quebram "R$" do número (usar `white-space:nowrap`).
   - Mudança de premissa DEPOIS do envio: não reenviar o e-mail inteiro de cara — atualizar canônico + planilha, e reenviar só se a diferença for material e o Igor não tiver dado a última palavra (ex.: verba condicional pendente de confirmação já vai marcada no e-mail original).
9. **Registrar:** Kanban board default (create → start → comment com resumo → complete) + espelho em `~/clawd/PEDIDOS.md` com data/hora de início e fim. NÃO regenerar o fluxo 2026–2036 nem dar baixa financeira com base na estimativa — só com TRCT conferido.

## Armadilhas

- Líquido documental de contracheque com dias parciais (ex.: folha com 18 dias) NÃO é salário mensal integral — extrapolar ele é o erro clássico; usar a soma das rubricas recorrentes.
- Verbas condicionais (férias vencidas, abono de CCT) entram marcadas como condicionais com o impacto exato da remoção — nunca somadas como se certas.
- VERBAL CONTRA DOCUMENTO: quando Igor afirmar verbalmente que uma verba não existe ("não tenho férias vencidas"), executar a varredura de evidência ANTES de remover o valor — folha paga aparece em contracheque (rubrica), férias aparecem em documento ZapSign assinado. Se os documentos contradizerem a afirmação, MANTER a verba condicional, apresentar as duas leituras com os dois totais e deixar o TRCT decidir — nunca remover dinheiro do usuário com base só na fala, nem manter com base só no documento sem avisar do conflito.
- Mensagem ao Igor: tom direto e empático (demissão é tema sensível), tabelas com valores por verba, total geral explícito, e o que pode mudar no TRCT listado em cima da resposta.
