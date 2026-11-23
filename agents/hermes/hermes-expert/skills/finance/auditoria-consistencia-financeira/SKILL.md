---
name: auditoria-consistencia-financeira
description: "Use when Usuário asks to check consistency across the financial controls (\"audita os controles\", \"confere se os números batem\", \"tem algo desatualizado?\"), and periodically after `atualizar-controles` to catch drift between root files and between skill files."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [financeiro, auditoria, consistencia, controles, dividas]
    related_skills: [atualizar-controles, financeiro-comprovantes, fluxo-caixa]
---

# Auditoria de Consistência Financeira

## Por que essa skill existe

Em 03/08/2026, uma sessão de revisão encontrou: 4 arquivos de controle de dívida com totais divergentes para a mesma dívida (já consolidados em `ENDIVIDAMENTO.md`); um `CONTROLES.md` recém-criado que referenciava 4 arquivos inexistentes; um `ENDIVIDAMENTO.md` com a classificação de cartões desatualizada frente ao `CONTROLES.md`/`FICHA_CARTAO_*.md`; um `FLUXO-CAIXA-2026-2028.md` apagado mas ainda citado em 3 outros lugares; e **números hardcoded nos próprios SKILL.md** (`fluxo-caixa`, `planejamento-financeiro`) que já não batiam com a realidade (CDB mínimo, contagem de cartões mantidos/negociação).

Em 13/08/2026 (auditoria quinzenal automática), a mesma classe de drift reapareceu em outra forma:
- **`FLUXO-CAIXA-2026-2030.md` existe em 3 paths** (raiz X23, `fluxo_caixa/cenario_atual/X23_atual.md` idêntico, e `_controles/FLUXO-CAIXA-2026-2030.md` que é X19 de 07/08 — defasado). Quem lê `_controles/` pega cenário errado.
- **Divergência de totais na negociação**: `ENDIVIDAMENTO.md` seção 1 = 7 cartões / R$ 51.845,35 (face, BrasilCard incluso); `fluxo_caixa/README.md` e X23 .xlsx = 6 cartões / R$ 62.744 (BrasilCard fora + valores diferentes por cartão). Metodologia do X23 não documentada no ENDIVIDAMENTO.
- **Drift estrutural**: `CLAUDE.md` linhas 24-26 ainda cita `CONTROLES.md` e `CONTROLE_FATURAS_MANTIDOS.md` na raiz; o real é `_controles/CONTROLE_INDICE.md` e `_controles/CONTROLE_FATURAS_MANTIDOS.md`.
- **Skill aponta para pasta inexistente**: passos anteriores desta skill citavam `~/.hermes/skills/financeiro/` — não existe. Todos os skills financeiros estão em `~/.hermes/skills/finance/`.
- **Coluna "CDB saldo" no .md X23 é enganosa**: mostra o **déficit/superávit mensal**, não o saldo acumulado. O saldo real está no .xlsx aba "CDB Evolução". Quem só lê o .md acha que CDB Out/26 = −R$ 10.227,79 (na verdade é R$ 24.064,67 com cap).

Esse padrão se repete porque cada skill/arquivo é atualizado isoladamente quando um fato muda, mas nada varre o conjunto para achar o que ficou pra trás. Esta skill é essa varredura.

## Quando usar

- Usuário pedir explicitamente: "audita os controles", "confere consistência", "os números batem?", "tem algo desatualizado?".
- Como último passo de uma rodada de `atualizar-controles`, quando um cartão mudou de status ou um dossiê novo foi gerado.
- Antes de entregar qualquer dossiê/relatório externo (advogado, contador) que consolide números de várias fontes.
- **Quando o agente desconfiar de drift** (arquivo criado em pasta nova sem mover o antigo; skill citando path inexistente; total agregando "X cartões" mas as fichas somam outro número).

## Estrutura real da árvore (validada em 13/08/2026)

Antes de auditar, mapear o que existe DE FATO — não confiar em nomes citados em outras skills/docs:

```bash
ls ~/MEGA/Comprovantes/*.md                          # raiz
ls ~/MEGA/Comprovantes/_controles/                    # todos os CONTROLE_*.md
ls ~/MEGA/Comprovantes/_fichas/                       # FICHA_CARTAO_*.md
ls ~/MEGA/Comprovantes/_saldos/                       # SALDO_*.md
ls ~/MEGA/Comprovantes/_Analises/                     # planos/dossiês
ls ~/MEGA/Comprovantes/fluxo_caixa/                   # cenários de saída
ls ~/MEGA/Comprovantes/fluxo_caixa/cenario_atual/     # versão vigente do fluxo
ls ~/MEGA/Comprovantes/fluxo_caixa/historico/         # versões antigas (X23 a X28)
ls ~/.hermes/skills/finance/                          # ÚNICA pasta de skills financeiros
```

**Mapeamento canônico validado em 20/08/2026:**

| O que docs/skills dizem | Onde está de verdade |
|---|---|
| `CONTROLES.md` (raiz) | `_controles/CONTROLE_INDICE.md` |
| `CONTROLE_FATURAS_MANTIDOS.md` (raiz) | `_controles/CONTROLE_FATURAS_MANTIDOS.md` |
| `ORCAMENTO.md` (raiz) | `_controles/CONTROLE_ORCAMENTO.md` (canônico) + `ORCAMENTO-AREAS.md` (raiz, complementar) |
| `FLUXO-CAIXA-2026-2030.md` (raiz) | Sincronizado com `fluxo_caixa/cenario_atual/X29_atual.md` e `_controles/FLUXO-CAIXA-2026-2030.md` (Cenário X29 vigente) |
| `FLUXO-CAIXA-RESCISAO.md` (raiz) | `_controles/FLUXO-CAIXA-RESCISAO.md` |
| `~/.hermes/skills/financeiro/` | **NÃO EXISTE**. Todos em `~/.hermes/skills/finance/` |

## Escopo da auditoria

### 1. Arquivos-raiz + `_controles/` + `fluxo_caixa/` de `~/MEGA/Comprovantes/`

1. **Mapear estrutura real** com os `ls` acima. Anotar tudo que NÃO está onde a documentação diz que está — isso já é o primeiro conjunto de achados.
2. Em cada arquivo-raiz e em `_controles/*.md` e `fluxo_caixa/**/*.md`, `grep` por menções a outros arquivos (padrão `` `NOME.md` ``, `[texto](./NOME.md)`, paths absolutos `~/MEGA/Comprovantes/...`) e confirmar que cada um existe no mapeamento do passo 1. Reportar qualquer referência morta ou path errado.
3. **Extrair de `ENDIVIDAMENTO.md` (seção 1)** a contagem oficial de cartões ativos/mantidos e em negociação e os totais em R$.
4. **Cruzar com:**
   - `_controles/CONTROLE_INDICE.md` (lista de fichas por status — fonte da verdade da taxonomia)
   - `_controles/CONTROLE_FATURAS_MANTIDOS.md` (snapshot mensal dos ativos)
   - `fluxo_caixa/cenario_atual/` (cenário vigente, ex: `X29_atual.md` — referenciar pela pasta `cenario_atual/`, não pela raiz)
   - `_controles/CONTROLE_ORCAMENTO.md` (custo de vida canônico)
   - `fluxo_caixa/README.md` (totais consolidados da negociação no cenário vigente)
   - Divergência = achado.
5. **Detectar duplicações por path**, não por nome-de-data. A falha de 03/08 era `FLUXO-CAIXA-2026-2028.md` vs `FLUXO-CAIXA-2026-2030.md`; a falha de 13/08 era `FLUXO-CAIXA-2026-2030.md` em 3 paths com cenários diferentes. Primeiro identificar o maior `X<n>_atual.md` existente em `fluxo_caixa/cenario_atual/`, depois usar `md5sum` (ou `diff -q`) para comparar esse arquivo com as cópias consumidas na raiz e em `_controles/`. Nunca hardcodar um cenário antigo no comando de auditoria.
6. **Conferir datas de "Última atualização"/"Atualizado"** no cabeçalho de cada arquivo-raiz e em `_controles/`. Se um arquivo citado como fonte por outro for mais antigo que quem o cita, sinalizar possível defasagem. **Atenção especial**: `CONTROLE_FATURAS_MANTIDOS.md` historicamente fica semanas atrás do `FLUXO-CAIXA-*.md` (padrão já flagado em 06/08/2026 e ainda não resolvido em 13/08).
7. **🎯 Checagem de prioridade #1 (a mais importante desta skill):** para cada mês da tabela mensal do fluxo vigente, confirmar `renda_mês ≥ custo_de_vida + parcela_HE_mês` — **sem contar com o CDB**. Se algum mês falhar essa conta, é o achado mais crítico possível. Registrar imediatamente em `AVISOS.md` como 🚨, no topo do relatório, antes de qualquer outro achado.

   ⚠️ **ATENÇÃO — "custo de vida" tem definições coexistentes (estado auditado em 27/08/2026):**
   - `_controles/CONTROLE_ORCAMENTO.md`: **R$ 4.720/mês** — fonte canônica orçamentária (Lazer R$ 1.929 + Não-lazer R$ 2.791, já incluindo faxina R$ 300).
   - `MAPA-CUSTO-VIDA.md`: **R$ 4.394,46** em Ago–Set/26 e **R$ 4.256,61** a partir de Out/26 — visão de fixas, não equivalente ao orçamento completo.
   - `ORCAMENTO-AREAS.md`: **R$ 4.418** em Ago–Set/26 e **R$ 4.280** a partir de Out/26 — visão do Pote 1, com metodologia própria.

   **Para o cheque de Prioridade #1, usar SEMPRE o valor vigente de `_controles/CONTROLE_ORCAMENTO.md` (R$ 4.720 em 27/08/2026), nunca um número hardcoded antigo.** Se o XLSX/MD do fluxo usar valor diferente (ex.: R$ 4.721 no X29), isso é 🟡 e deve ser registrado.

8. **Cruzar camada estratégica × operacional da negociação** (divergência frequente, classe de erro de 13/08):
   - `ENDIVIDAMENTO.md` seção 1 e 4: totais e contagem oficiais
   - `fluxo_caixa/README.md`: totais consolidados (inclui "X cartões em negociação")
   - `FLUXO-CAIXA-2026-2030.xlsx` aba "Estratégia Negociação": valores por cartão no cenário vigente
   
   Se os números batem, OK. Se divergem, é 🟡 no mínimo — pode ser metodologia diferente (face vs projeção de juros) ou desatualização de um lado. Documentar qual lado é mais novo e qual metodologia ele usa; não tentar resolver sozinho, apenas sinalizar.

9. **Validar contagem de ativos** entre pelo menos 4 fontes que podem divergir:
   - `ENDIVIDAMENTO.md` seção 1 (resumo), seção 2 (estratégia vigente), seção 3 (tabela de ativos)
   - `_controles/CONTROLE_INDICE.md` (Ativos: 7)
   - `_controles/CONTROLE_FATURAS_MANTIDOS.md` (cabeçalho "🟢 Cartões ativos (N)")
   - `fluxo_caixa/cenario_atual/X<n>_atual.md` (usar o maior `<n>` encontrado; se houver mais de uma versão na pasta, sinalizar a versão antiga como candidata a arquivamento)
   
   Padrão típico de drift em 13/08: seção 1 diz "8 ativos" mas seção 3 lista 7 ativos + Porto como "✅ QUITADO" (só parcelamento residual). Pick a canonical count.

10. **Procurar colunas/tabelas enganosas em arquivos .md**: se o cabeçalho de uma coluna promete "X" mas os valores mostram "Y" (ex.: coluna "CDB saldo" mostrando déficit mensal em vez de saldo acumulado), registrar como achado de apresentação.

11. **Auditoria visual obrigatória de PDF financeiro:** validade técnica não equivale a apresentação aprovada. Para cada PDF final:
   - conferir `pdfinfo` e extrair texto com layout;
   - renderizar **todas** as páginas para imagem e montar folha de contato;
   - verificar página por página: fundo branco, título/subtítulo órfão, tabela quebrada sem cabeçalho repetido, coluna fora da margem, sobreposição, página vazia/quase vazia e legibilidade;
   - regenerar até obter **APROVADO**; não entregar um PDF apenas porque abre e tem texto extraível.

   Para tabelas longas, prefira HTML com paginação controlada: resumo executivo fechado na página 1, fluxo em blocos com `<thead>` próprio e checks na última página. Forçar `html, body, section { background: #fff !important; }`; quando o CSS usa preenchimentos, gerar com `wkhtmltopdf --background`.

12. **Cópias legadas consumidas não podem ficar silenciosamente defasadas:** se raiz, `cenario_atual/X<n>_atual.*` e `_controles/` coexistirem, escolher uma fonte canônica e:
   - sincronizar cópias ainda consumidas; ou
   - arquivar/remover a referência de forma explícita.
   Não tratar automaticamente `_controles/FLUXO-CAIXA-2026-2030.md` como histórico imutável se ferramentas ainda o leem.

### 2. Skills do Hermes (`~/.hermes/skills/finance/` — única pasta)

> **Pasta `~/.hermes/skills/financeiro/` NÃO existe** (estado em 13/08/2026). Se uma referência a ela aparecer, é 🔴 referência morta.

1. `grep -rn "FLUXO-CAIXA-\|ENDIVIDAMENTO\|CONTROLES\.md\|CONTROLE_FATURAS_MANTIDOS\.md\|ORCAMENTO\.md\|R\$ [0-9]\|~/.hermes/skills/financeiro" **/SKILL.md` em `~/.hermes/skills/finance/`.
2. Para cada nome de arquivo citado (ex.: `FLUXO-CAIXA-2026-2028.md`), confirmar que existe em `~/MEGA/Comprovantes/`. Arquivo citado que não existe mais = achado prioritário (a skill vai instruir uma ação sobre um arquivo morto). Padrão em 13/08: skills citaram `~/MEGA/Comprovantes/FLUXO-CAIXA-RESCISAO.md` (raiz), real está em `_controles/`.
3. Para valores em R$ citados como "premissa" ou "fato atual" (CDB, dívida total, custo de vida, contagem de cartões) fora de uma tabela explicitamente marcada como histórica/exemplo, comparar contra `ENDIVIDAMENTO.md`, `_controles/CONTROLE_ORCAMENTO.md` e o maior `X<n>_atual.md` em `fluxo_caixa/cenario_atual/`. Números voláteis não deveriam ficar hardcoded numa skill — sinalizar como candidato a virar ponteiro ("ver arquivo X") em vez de valor fixo.

## Formato do relatório

Tabela única, achados mais críticos primeiro:

| # | Arquivo | Afirmação encontrada | Fonte canônica diz | Severidade |
|---|---|---|---|---|
| 1 | ... | ... | ... | 🔴 referência morta / 🟡 número divergente / � cosmético |

Fechar com uma lista curta do que está **consistente** (não só o que está errado) — evita a sensação de que tudo está sempre quebrado. Sempre recalcular e citar o cenário vigente; não carregar números de uma auditoria anterior como se fossem atuais. Exemplos de itens a confirmar:
- ✅ Prioridade #1 (renda ≥ custo canônico vigente + HE) passou em todos os meses
- ✅ CDB nunca zera e o mínimo confere com a aba `CDB Evolução`
- ✅ HOME-EQUITY.md × CONTRACHEQUE.md × cenário vigente: valores SAC/renda consistentes
- ✅ AVISOS.md preserva o formato append-only
- ✅ Estrutura `fluxo_caixa/` contém os cenários previstos e somente a versão vigente em `cenario_atual/`

## AVISOS.md — formato e regra de não-duplicação

Adicionar uma linha em `~/MEGA/Comprovantes/AVISOS.md` para cada achado 🔴 ou 🟡 (não precisa para os 🟢 cosméticos) — data, tipo, resumo de uma linha, link pro arquivo com o detalhe. `AVISOS.md` é um log, nunca editar/apagar entrada antiga.

**Não duplicar linhas que já existem para o mesmo achado.** Padrão concreto: se um achado de 06/08/2026 diz "`CONTROLE_FATURAS_MANTIDOS.md` X6 desatualizado" e a auditoria de 13/08 encontra que continua desatualizado mas agora o X23 cita valor diferente, NÃO adicionar nova linha sobre "X6 desatualizado" — apenas mencionar no relatório que o achado de 06/08 continua sem resolução.

## Regra de ação

**Não corrigir em massa sem reportar primeiro.** Mostrar o relatório completo, e só editar os arquivos depois de Usuário confirmar — exatamente como na sessão de 03/08/2026 que originou esta skill (diagnóstico completo, depois execução). Exceção: correções triviais e inequívocas (ex.: link para arquivo apagado há mais de um mês, sem ambiguidade sobre o substituto) podem ser aplicadas direto, mas devem aparecer listadas no relatório final mesmo assim.

**Pitfall: a auditoria pode descobrir que ESTA PRÓPRIA SKILL está errada** (paths que ela cita não existem, totais que ela pede para cruzar estão em arquivos que mudaram de lugar). Quando isso acontecer, NÃO se auto-corrigir silenciosamente — adicionar achado 🔴 no relatório e patchar a skill no final via `skill_manage`. Padrão de 13/08: a skill citou `~/.hermes/skills/financeiro/` e arquivos de raiz que já tinham migrado para `_controles/`.

## Referências

- [`../atualizar-controles/SKILL.md`](../atualizar-controles/SKILL.md) — rotina que gera/atualiza os controles; esta skill audita o resultado dela.
- `~/MEGA/Comprovantes/ENDIVIDAMENTO.md` seção 10 — regra de atualização e changelog, útil para entender o que mudou recentemente antes de auditar.
- `~/MEGA/Comprovantes/fluxo_caixa/README.md` — qual cenário é o vigente e totais consolidados da negociação.
- `~/MEGA/Comprovantes/_controles/CONTROLE_INDICE.md` — fonte da verdade da taxonomia de status por cartão.