# Fluxo de Caixa — Fonte da verdade e processo de atualização

> O Markdown é a fonte canônica do fluxo; planilhas e páginas do dashboard são artefatos derivados, nunca fontes concorrentes.

## Fonte da verdade

`~/MEGA/Comprovantes/FLUXO-CAIXA-2026-2036.md` é a fonte vigente. Leia o arquivo e os insumos atuais antes de editar; nomes de cópias, índices ou arquivos históricos não provam qual versão está ativa.

- O Markdown é a referência canônica; a família de JSON/CSV/XLSX e as páginas publicadas são saídas geradas. Se uma saída divergir, corrija a fonte/modelo e regenere — não edite o espelho.
- O escritor canônico da família é `~/MEGA/Comprovantes/fluxo_caixa/dashboard/src/gerar_canonico_2036.py`. Execute-o a partir da raiz do repositório com o interpretador de projeto validado; não substitua esse fluxo por edição manual de tabelas ou planilhas.
- O dashboard tem uma etapa de geração própria (`gerar_dashboard.py`). Mudanças na fonte ou nos templates que afetem a interface exigem executar essa etapa após a última edição.
- Para projeções X46/X47, confira também o modelo de cenário `src/evolucao_2036.py`; regenerar a família canônica não garante, por si só, que cada projeção derivada mudou.

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

1. **Classifique antes de lançar:** fatura fechada sem comprovante permanece em aberto; negociação/calota não é pagamento operacional. Separe confirmado, provisionado e pendente, registrando fonte e premissa.
2. **Reconcilie as linhas:** compare compras/parcelas da fatura com despesas e provisões existentes. Não some uma parcela como saída separada quando ela já está incluída no total da fatura; preserve a diferença ainda não conciliada, sem inventar ajuste. Ao conferir se um emissor já aparece nas faturas de cartão, use limite de palavra (`\bclaro\b`) ou confira o contexto de cada match — substring de nome próprio bate dentro de palavras comuns do português ("declarou" contém "claro") e produz falsa duplicidade ou falsa ausência na deduplicação.
3. **Atualize a fonte/modelo correto:** altere o input canônico ou o motor que o produz, não a tabela gerada. Para cada mudança mensal, siga o efeito por todos os cenários afetados, inclusive X46/X47; aplique o delta nos meses corretos e confira séries e âncoras após o recálculo.
   - ⚠️ **PITFALL:** as linhas mensais do YAML são HARDCODED no próprio gerador — cada mês é um bloco `w(...)` com os valores das colunas dentro de `gerar_canonico_2036.py`. Editar somente o YAML do MD e regenerar REVERTE silenciosamente a edição; atualize as linhas do mês no gerador (incluindo o comentário da linha e o texto do delta embutido, se houver) ANTES de rodar o gerador, depois confira no MD gerado que o valor novo sobreviveu.
   - Semântica das colunas de cada linha mensal: `[mês, faturas(cartões), home_equity, outros, extra_renda(13º, VALLO extra), extra_despesa]`. "outros" agrupa condomínio + contas de consumo (luz, gás, telefone); valide cruzando o mês real com as faturas do mês antes de alterar a estimativa (em mês sem decomposição documental, a estimativa anterior prevalece).
4. **Gere a família canônica:** na raiz do repositório `~/MEGA/Comprovantes/fluxo_caixa/dashboard`, execute `~/.hermes/hermes-agent/venv/bin/python src/gerar_canonico_2036.py` (ou o interpretador de projeto comprovadamente configurado). Leia de volta o MD, JSON, CSV e XLSX; confira horizonte, quantidade de meses, totais, saldo mínimo e marcos de zeramento. ⚠️ **Depois de editar as linhas `w(...)`, rode o gerador DUAS vezes:** o motor `evolucao_2036.py` lê o YAML do MD EM DISCO, que só é regravado pela própria escrita do gerador — a 1ª execução grava o YAML novo mas calcula com o YAML antigo (termina exit 0 com a tabela do mês ainda nos valores velhos); a 2ª recalcula com os valores novos. Confira a linha do mês alterado no MD gerado antes de seguir para o dashboard.
5. **Gere o dashboard depois da última alteração de template/código:** execute `~/.hermes/hermes-agent/venv/bin/python gerar_dashboard.py` na raiz do mesmo repositório. Inspecione o artefato publicado, não só o fonte. Para mudança em JavaScript/CSS, confira a URL versionada no HTML gerado e busque exatamente o asset referenciado; valide um marcador da nova versão.
6. **Valide o servido:** consulte a rota local afetada e compare os dados exibidos com o JSON/cálculo canônico. Se houver publicação/túnel no escopo, confirme a URL atual e a rota pública; sucesso do build ou do servidor local, isoladamente, não prova que o usuário recebeu a versão nova.
7. **Sincronize controles e espelhos solicitados:** atualize fichas, controles, avisos e vencimentos aplicáveis. Não edite XLSX manualmente; confirme que eventuais cópias sincronizadas derivam do artefato gerado e que seus valores/ fórmulas podem ser lidos de volta.
8. **Feche com reconciliação:** totalize por status e compare a soma das linhas aos subtotais; liste divergências sem as corrigir por suposição e declare explicitamente testes/build/rotas que falharam ou ficaram sem verificação.

## Como criar um what-if

Mantenha o what-if identificado como cenário separado e use o ponto de entrada documentado pelo modelo atual. Não altere a base vigente nem registre um resultado hipotético como dado confirmado.

## Histórico e recuperação

Preserve versões anteriores no mecanismo de histórico/backup já usado pelo projeto. Se a fonte canônica estiver ausente ou corrompida, restaure a versão mais recente verificável, reaplique apenas alterações sustentadas por evidência e regenere a família pelo escritor oficial; nunca recrie números por memória.

## Nunca

- Tratar faturas em negociação/calota como pagamento realizado ou saída operacional.
- Contar a mesma compra/parcela simultaneamente no total da fatura e como despesa avulsa.
- Editar manualmente o XLSX, JSON, CSV ou HTML gerados para “corrigir” um número.
- Declarar atualização concluída apenas porque o gerador terminou: confira artefatos, âncoras, testes e rotas afetadas; exponha verificações pendentes.
- Presumir que o gerador canônico também atualiza todas as projeções ou assets do dashboard; execute e valide cada etapa aplicável.

## Sincronização de renda CLT (aprendido em 11/11/2026, tarefa t_1121d691)

Quando corrigir o `clt_liquido` no YAML do canônico (ex.: estimativa → real do extrato Nubank):

1. **Editar 3 lugares**: (a) YAML vivo do FLUXO-CAIXA-<HOR>.md (input do motor); (b) linhas `w(...)` do `gerar_canonico_2036.py` (YAML, reconciliação, nota, linha XLSX — o gerador REESCREVE o MD inteiro, então editar só o MD é perdido na próxima geração); (c) `evolucao_2036.py` se houver cálculo derivado do líquido (ex.: estimativa de dissídio = 4,32% × líquido).
2. **Efeito esperado do delta**: déficits X46/X47 são recalibrados por diferença (saldo_novo − saldo_legado, ambos com o mesmo clt_liquido), então **pico, juros, zeramento e sobras da dívida NÃO mudam**. Muda: rendas mensais (+delta), curva X45, CDBs pós-zeramento e marcos 2028/2031/2036. Se o valor mudado for grande demais, questionar se a dívida deveria acelerar — o mecanismo por delta congela o caminho da dívida na calibragem da leva anterior.
3. **Recalibrar testes por classe**: test_evolucao_2036 (rendas + cdb_dez27/dez36 X45/X46/X47 + marcos), test_atualizacao_faturas_out/nov_2026 (cdb + saldos + CSV + XLSX de painel), test_canonico_csv_x47 (cdb CSV), test_modelo_dashboard (rendas Decimal), test_evolucao_2036_view (cdb do JSON publicado). Âncoras LEGADO (cdb_dez27_legado 37108.77, cdb_dez36_legado 1562341.05) ficam intactas.
4. **Interpretadores**: `gerar_canonico_2036.py` e `gerar_dashboard.py` exigem openpyxl → usar `~/.hermes/hermes-agent/venv/bin/python` (python3 padrão falha com ModuleNotFoundError); pytest é `~/.local/bin/pytest` (o python3 padrão não tem pytest). openpyxl ausente deixa o XLSX stale silenciosamente — conferir que as 4 extensões (.md/.json/.csv/.xlsx) regeneraram.
5. **Ordem**: MD YAML → gerar_canonico → `python3 src/evolucao_2036.py` (publica JSON) → testes → `gerar_dashboard.py` (rebuild publica dados_dashboard.json e resolve o gate test_paridade_base_x45) → pytest completo → commit com caminhos explícitos (`git add -f` para publicacao/*.json, que estão no .gitignore mas rastreados).
6. **Deixar follow-up**: CONTA-SIMPLIFICADA.md e PAINEL_ACOMPANHAMENTO.xlsx têm salário/âncoras próprias e ficam stale — criar card filho em vez de escopo-creep. Outros testes pré-existentes (adrielly, fluxo_nov_dez, menu_js_gate, modelo card_registry/eventos/severance/fuel) podem estar vermelhos por trabalho paralelo — confirmar rodando o mesmo subconjunto no baseline antes de culpar a própria mudança: `git stash push -m '<tag>' -- <arquivos do próprio diff>`, rodar pytest e `git stash pop`; mesmas falhas sem o diff = falhas acopladas a dados novos/preexistentes, não regressão da leva.
