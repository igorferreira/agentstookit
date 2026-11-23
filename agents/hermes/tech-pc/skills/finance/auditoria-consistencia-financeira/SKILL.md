---
name: auditoria-consistencia-financeira
description: "Use when Usuário asks to check consistency across the financial controls (\"audita os controles\", \"confere se os números batem\", \"tem algo desatualizado?\"), and periodically after `atualizar-controles` to catch drift between root files and between skill files."
version: 1.0.0
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

Esse padrão se repete porque cada skill/arquivo é atualizado isoladamente quando um fato muda, mas nada varre o conjunto para achar o que ficou pra trás. Esta skill é essa varredura.

## Quando usar

- Usuário pedir explicitamente: "audita os controles", "confere consistência", "os números batem?", "tem algo desatualizado?".
- Como último passo de uma rodada de `atualizar-controles`, quando um cartão mudou de status ou um dossiê novo foi gerado.
- Antes de entregar qualquer dossiê/relatório externo (advogado, contador) que consolide números de várias fontes.

## Escopo da auditoria

### 1. Arquivos-raiz de `~/MEGA/Comprovantes/`

1. `ls ~/MEGA/Comprovantes/*.md` para ter a lista real de arquivos existentes hoje.
2. Em cada arquivo-raiz, `grep` por menções a outros arquivos-raiz (padrão `` `NOME.md` `` ou `[texto](./NOME.md)`) e confirmar que cada um existe na lista do passo 1. Reportar qualquer referência a arquivo inexistente.
3. Extrair de `ENDIVIDAMENTO.md` (seção 1) a contagem oficial de cartões ativos/mantidos e em negociação e os totais em R$.
4. Comparar essa contagem/total com o que aparece em `CONTROLES.md`, `CONTROLE_FATURAS_MANTIDOS.md`, `FLUXO-CAIXA-*.md` e `ORCAMENTO.md`. Divergência = achado.
5. Se existir mais de um arquivo com o mesmo prefixo e datas/intervalos diferentes (ex.: `FLUXO-CAIXA-2026-2028.md` e `FLUXO-CAIXA-2026-2030.md` coexistindo), reportar como possível duplicação — não apagar sozinho, perguntar qual é o vigente.
6. Conferir a data de "Última atualização"/"Atualizado" no cabeçalho de cada arquivo-raiz; se um arquivo citado como fonte por outro for mais antigo que quem o cita, sinalizar possível defasagem.
7. **🎯 Checagem de prioridade #1 (a mais importante desta skill):** para cada mês da tabela mensal de `FLUXO-CAIXA-2026-2030.md`, confirmar `renda_mês ≥ custo_de_vida (R$4.421) + parcela_HE_mês` — **sem contar com o CDB**. Se algum mês falhar essa conta, é o achado mais crítico possível (o Usuário definiu isso como a maior preocupação dele: sempre ter dinheiro pra custo de vida e Home Equity). Registrar imediatamente em `AVISOS.md` como 🚨, no topo do relatório, antes de qualquer outro achado.

### 2. Skills do Hermes (`~/.hermes/skills/finance/` e `~/.hermes/skills/financeiro/`)

1. `grep -rn "FLUXO-CAIXA-\|ENDIVIDAMENTO\|CONTROLES.md\|R\$ [0-9]" **/SKILL.md` nos diretórios de skills financeiras.
2. Para cada nome de arquivo citado (ex.: `FLUXO-CAIXA-2026-2028.md`), confirmar que existe em `~/MEGA/Comprovantes/`. Arquivo citado que não existe mais = achado prioritário (a skill vai instruir uma ação sobre um arquivo morto).
3. Para valores em R$ citados como "premissa" ou "fato atual" (CDB, dívida total, contagem de cartões) fora de uma tabela explicitamente marcada como histórica/exemplo, comparar contra o valor atual em `ENDIVIDAMENTO.md`/`FLUXO-CAIXA-*.md`. Números voláteis (CDB, saldo de dívida) não deveriam estar hardcoded numa skill — sinalizar como candidato a virar ponteiro ("ver arquivo X") em vez de valor fixo.

## Formato do relatório

Tabela única, achados mais críticos primeiro:

| # | Arquivo | Afirmação encontrada | Fonte canônica diz | Severidade |
|---|---|---|---|---|
| 1 | ... | ... | ... | 🔴 referência morta / 🟡 número divergente / 🟢 cosmético |

Fechar com uma lista curta do que está **consistente** (não só o que está errado) — evita a sensação de que tudo está sempre quebrado.

Além do relatório para o Usuário, **adicionar uma linha em `~/MEGA/Comprovantes/AVISOS.md`** para cada achado 🔴 ou 🟡 (não precisa para os 🟢 cosméticos) — data, tipo, resumo de uma linha, link pro arquivo com o detalhe. `AVISOS.md` é um log, nunca editar/apagar entrada antiga.

## Regra de ação

**Não corrigir em massa sem reportar primeiro.** Mostrar o relatório completo, e só editar os arquivos depois de Usuário confirmar — exatamente como na sessão de 03/08/2026 que originou esta skill (diagnóstico completo, depois execução). Exceção: correções triviais e inequívocas (ex.: link para arquivo apagado há mais de um mês, sem ambiguidade sobre o substituto) podem ser aplicadas direto, mas devem aparecer listadas no relatório final mesmo assim.

## Referências

- [`../atualizar-controles/SKILL.md`](../atualizar-controles/SKILL.md) — rotina que gera/atualiza os controles; esta skill audita o resultado dela.
- `~/MEGA/Comprovantes/ENDIVIDAMENTO.md` seção 10 — regra de atualização e changelog, útil para entender o que mudou recentemente antes de auditar.
