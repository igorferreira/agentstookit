# Fluxo de Caixa — Fonte da verdade e processo de atualização

> Atualizado em 18/09/2026. Decisão do Usuário (28/08/2026, confirmada em 18/09): o **Markdown é o arquivo canônico**; o XLSX é espelho.
> Substitui a versão anterior deste arquivo, que tratava os JSONs `fluxo_xNN.json` como fonte (eles param no X35).

## Fonte da verdade

`~/MEGA/Comprovantes/FLUXO-CAIXA-2026-2030.md` (o título traz "Cenário Xn (CANÔNICO)").

- No começo há um bloco YAML: `scenario` (versão, ex. X43), `versao` (data e hora), `delta` (o que mudou nesta versão),
  `fonte`, `inputs`, `mensais`, `cenarios`, `estouro_meses`.
- As seções "Resultado comparativo" e "Evolução mensal por cenário" são **geradas pelo motor**; não editar à mão.
- `FLUXO-CAIXA-2026-2030.xlsx` é espelho gerado pelo motor. Se MD e XLSX divergirem, o **MD vence**. Nunca editar o XLSX à mão.
- A cópia `~/MEGA/Comprovantes/_controles/FLUXO-CAIXA-2026-2030.md` (X33, 27/08) está velha e **não vale**.

## Vocabulário: versão x cenário

- **Versão (Xn)** = estado do fluxo **vigente** (produção). Sobe (X42 -> X43) quando um dado real é confirmado
  (fatura fechada, extrato, mudança de renda ou despesa). **Não é uma simulação.**
- **Cenário (what-if)** = linha da lista `cenarios` do YAML: `[nome, diego_para, estouro_extra_mensal]`. São simulações
  calculadas pelo motor e comparadas lado a lado em "Resultado comparativo". Hoje: Base com Diego, Sem Diego Out/26,
  Sem Diego Set/26, Stress sem Diego +R$1k. O cenário **Base** é o vigente; os demais são projeções e não viram
  vigentes sozinhos.
- **Simulações fora do arquivo principal** (demissão, pedido de demissão, janela ótima, rescisão): ficam em
  `~/MEGA/Comprovantes/fluxo_caixa/cenario_*` e `~/MEGA/Comprovantes/_controles/FLUXO-CAIXA-RESCISAO.md`.
- Regra: um what-if pedido pelo usuário **não altera a versão vigente**. O cenário base só avança com dado confirmado.

## Como atualizar (nova fatura ou dado real)

1. Editar **só o YAML** do MD: `scenario` (X(n+1)), `versao` (AAAA-MM-DD HH:MM), `delta` (o que mudou, valor antes e depois)
   e os números em `inputs`/`mensais`.
2. Rodar: `python3.12 ~/MEGA/Comprovantes/fluxo_caixa/engine/fluxo.py` (usa pyyaml e openpyxl).
3. O motor reescreve "Resultado comparativo" e "Evolução mensal por cenário" no MD e regera o XLSX espelho
   (abas Resumo e Fluxo Base). Ele **não** altera `scenario`/`versao`/`delta`. CSV, PDF e JSON foram dispensados pelo Usuário (18/09/2026): as saídas são só o `.md` e o `.xlsx`.
4. Conferir o resultado (coluna "Zera?" de cada cenário e o CDB mínimo) e reportar ao Usuário terminando com o status do CDB.
5. Cascata do ciclo da fatura (`SKILL.md`, "Ciclo completo", passo 6): `ENDIVIDAMENTO.md`, `AVISOS.md`,
   `~/.hermes/scripts/dados-vencimentos.json`, `_controles/PAINEL_ACOMPANHAMENTO.xlsx` e o espelho no Google Drive (Insync).
   Esses passos continuam **manuais / a cargo do agente**.

## Como criar um what-if

Adicionar uma linha em `cenarios` no YAML e rodar o motor. Não muda o cenário Base nem a versão.

## Histórico e recuperação

- Versões antigas: `~/MEGA/Comprovantes/fluxo_caixa/historico/Xnn/` (até X34), `~/MEGA/Comprovantes/fluxo_caixa/cenario_atual/Xnn_atual.*` (X28 a X35) e
  `~/MEGA/Comprovantes/2026/_Analises/cenarios/fluxo_xNN.json` (até X35). **Não foram encontrados snapshots de X36 a X43.**
- Se o MD sumir ou estragar: restaurar do último backup do MEGA ou do snapshot mais recente e reaplicar as mudanças
  seguintes pelo YAML; depois rodar o motor.

## Nunca

- Ler CSV/XLSX como fonte primária.
- Editar o XLSX à mão.
- Mudar o formato do `.md` canônico (bloco YAML + tabelas): o **dashboard do Usuário lê esse arquivo**.
- Usar `execute_code` para gerar fluxo (bloqueado em cron/gateway); usar `write_file` + `terminal`.
- Assumir a versão vigente pelo `README.md` de `fluxo_caixa/` ou por memória: ler o título do MD canônico.
