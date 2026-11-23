---
name: atualizar-controles
description: Atualiza todos os controles financeiros quando Usuário diz "atualize nossos controles" ou "financeiro atualiza os controles"
---

# Atualizar Controles Financeiros

Quando o Usuário disser **"atualize nossos controles"** ou **"financeiro atualiza os controles"**, seguir este procedimento.

## Pré-requisito
1. Ler `CONTROLE_INDICE.md` em `~/MEGA/Comprovantes/_controles/CONTROLE_INDICE.md` para ver a lista completa

## ⚠️ ANTES de recalcular o fluxo — Verificação de consistência

**Este passo é obrigatório.** O erro mais comum é o fluxo usar renda diferente do contracheque real — já aconteceu de o fluxo usar ~R$9.000/mês quando o real era ~R$12.415/mês.

### Fórmula correta da renda mensal:
```
Renda = CLT líquido (CONTRACHEQUE.md) + VALLO BENEFÍCIOS
```
- O CLT líquido do `CONTRACHEQUE.md` **já inclui** o desconto do empréstimo folha (−R$1.000). Não descontar de novo.
- Nos meses de **novembro**: adicionar 13º 1ª parcela (50% do bruto)
- Nos meses de **dezembro**: adicionar 13º 2ª parcela (~39% do bruto após descontos)
- O VALLO acompanha o % de dissídio (mesmo % do salário)

### Fórmula correta das saídas:
```
Déficit/Superávit = Renda − Faturas − Home Equity (SAC)
```
- **Faturas**: valores do `CONTROLE_FATURAS_MANTIDOS.md` + parcelamentos conhecidos + custo base (R$ 4.421)
- **Home Equity**: valores exatos do cronograma SAC no `HOME-EQUITY.md`, NUNCA os valores aproximados do fluxo antigo
- O CDB cobre os déficits; superávits são aportados no CDB

### Checklist de reconciliação:
- [ ] `CONTRACHEQUE.md` carregado e renda extraída mês a mês
- [ ] `HOME-EQUITY.md` carregado e parcelas SAC extraídas mês a mês
- [ ] Renda do fluxo confere com CONTRACHEQUE.md (não usar números herdados de versões anteriores!)
- [ ] Home Equity do fluxo confere com HOME-EQUITY.md
- [ ] **🎯 Prioridade #1 do Usuário:** para todo mês, `renda_mês ≥ R$4.421 (custo de vida) + parcela_HE_mês`, sem contar com o CDB. Se algum mês falhar, isso é mais grave que qualquer outro achado — parar e avisar antes de continuar o recálculo.

## Passo a passo

### 1. Revisar alterações recentes
- Verificar se há novas faturas, comprovantes ou prints enviados recentemente
- Identificar o que mudou desde a última atualização
- Se houver prints de extrato/fatura, extrair via OCR (ver `references/ocr-card-extraction.md`)

### 2. Atualizar arquivos 🔴 (obrigatórios)

| Ordem | Arquivo | Ação |
|---|---|---|
| 0º | `CONTRACHEQUE.md` + `HOME-EQUITY.md` | **Carregar primeiro** — são a fonte da verdade para renda e HE |
| 1º | `_controles/CONTROLE_FATURAS_MANTIDOS.md` | Atualizar faturas do mês corrente com novos valores |
| 2º | `FLUXO-CAIXA-2026-2030.md` | Recalcular com Python usando renda real + HE real do SAC (ver `references/fluxo-recalculation-formula.md`) |
| 3º | `FLUXO-CAIXA-2026-2030.xlsx` + `.csv` | Regenerar com `python3.12` + openpyxl |
| 4º | `CONTRACHEQUE.md` | Atualizar se houve dissídio ou alteração salarial |
| 5º | `HOME-EQUITY.md` | Atualizar se houve alteração de taxa |
| 6º | `ENDIVIDAMENTO.md` | Camada estratégica de dívida (em `~/MEGA/Comprovantes/ENDIVIDAMENTO.md`) — atualizar sempre que um cartão mudar de status (ativo ↔ negociação), chegar proposta de acordo, ou houver evento de negativação/protesto/ação judicial. Não é opcional: se ficar sem sincronizar com `CONTROLE_FATURAS_MANTIDOS.md`, volta a haver duas fontes de verdade divergentes sobre a mesma dívida. |

### 🚨 Pitfall: Fluxo com renda errada
O fluxo de caixa já foi gerado com renda ~R$9.000/mês quando o real era ~R$12.415/mês. **Sempre** recalcular do zero com os valores reais do CONTRACHEQUE.md. Nunca confiar nos números de renda de uma versão anterior do fluxo.

### 3. Atualizar fichas 🟡 (se necessário)
- Atualizar `FICHA_CARTAO_*.md` dos cartões que tiveram movimentação
- Registrar parcelamentos novos, pagamentos, status
- Ao extrair parcelamentos via OCR, detalhar cada um com: total da compra, já pago, falta pagar (R$ + nº parcelas), última parcela (mês/ano)
- Incluir projeção mês a mês até a quitação

### 🔄 Cartão muda de status (ex: negociação → mantido)

Quando Usuário decide manter um cartão que estava em negociação:

1. **Ficha do cartão**: mudar status, adicionar parcelas detalhadas, projeção de quitação
2. **`CONTROLE_FATURAS_MANTIDOS.md`**: adicionar à lista de ativos, incluir nas faturas do mês
3. **`FLUXO-CAIXA-2026-2030.md`**: adicionar o valor das parcelas nas colunas de faturas dos meses afetados e recalcular
4. **`CONTROLES.md`**: atualizar status na tabela de fichas
5. **`ENDIVIDAMENTO.md`**: mover o cartão entre as seções 3 (Ativos) e 4 (Em negociação), recalcular os totais da seção 1 e o racional/concentração de risco da seção 2

> Exemplo: Atacadão 1843 saiu de 💀 Negociação para 🟢 Mantido com 2 parcelas de R$ 323,08 em Set–Out/26.

### 💳 Pagamento com CDB

Quando um cartão é pago com o CDB:
1. Subtrair o valor do CDB inicial (ex: R$ 29.000 − R$ 6.959 = R$ 22.041)
2. Registrar na ficha do cartão: valor, data, origem (CDB), chave PIX usada
3. Recalcular o fluxo com o novo CDB inicial
4. O impacto real no CDB de 2030 é tipicamente pequeno (~R$ 10k pra cada R$ 7k gasto hoje)

### 4. Atualizar arquivos de custo fixo quando necessário

Sempre que um custo fixo mensal for adicionado, removido ou alterado:

| Arquivo | Ação |
|---|---|
| `MAPA-CUSTO-VIDA.md` | Adicionar/remover linha na tabela de contas fixas, recalcular TOTAL FIXO |
| `_controles/CONTROLE_ORCAMENTO.md` | Atualizar NÃO-LAZER (teto), adicionar/remover item da tabela N1–N6, atualizar total no resumo |
| `FLUXO-CAIXA-2026-2030.md` | Atualizar referência ao custo de vida (Prioridade #1), recalcular pior margem |

> Exemplo: Meli+ (Disney+) R$40/mês adicionado em ago/2026 → não-lazer R$2.451 → R$2.491, total R$4.421 → R$4.461.
- Listar o que foi alterado
- Destacar impactos no CDB (se fluxo foi recalculado), comparando com a versão anterior
- Listar o que segue pendente (ex: faturas sem info)
- Listar o que NÃO mudou (para tranquilizar)
- Usar tabela comparativa "Antes → Agora" com Δ
- **Sempre avisar via Telegram ao terminar** (`hermes send --to telegram "..."`), resumo curto — regra do perfil, ver `SOUL.md`

### 5. Registrar no AVISOS.md

Sempre que uma atualização revelar algo digno de nota, escrever uma linha em `~/MEGA/Comprovantes/AVISOS.md`:

- 🔴 **Gasto fora do padrão** — fatura muito acima do provisionado, categoria de orçamento estourada
- ⚠️ **Risco identificado** — racional frágil, concentração de exposição, lacuna de dado
- 🚨 **Negativação / atraso crítico** — protesto, ação judicial
- 🟡 **Inconsistência de dados** — números que não batem entre arquivos
- 🔵 **Informativo** — mudança relevante (novo cartão, dissídio, nova renda)

O AVISOS.md é um **log cronológico** — nunca editar ou apagar entradas antigas. Se um alerta for resolvido, adicionar uma nova linha `✅ resolvido` referenciando a original.

### 6. Quando um cartão mudou de status ou um arquivo foi substituído

Rodar a skill `auditoria-consistencia-financeira` antes de encerrar — ela pega divergências que a atualização pontual costuma deixar passar (arquivo antigo ainda referenciado em outro lugar, contagem de cartões que não bateu em todo canto).

## Notas
- O fluxo de caixa sempre usa Python para recalcular quando há alteração numérica
- Usar `python3.12` para openpyxl (geração de Excel), `python3` para cálculos
- Manter formato Markdown brasileiro (R$ 1.000,00)
- Usar emojis: 🟢 ativo/pago/superávit, 🔴 déficit, ⬜ pendente, ✅ concluído, 💀 negociação, ⚠️ atenção
- Salvar tudo em `~/MEGA/Comprovantes/`
- Atualizar também `_controles/CONTROLE_INDICE.md` quando um controle novo for criado

## 📚 Referências

| Arquivo | Conteúdo |
|---|---|
| `references/pdf-email-workflow.md` | Geração de PDF (wkhtmltopdf) + anexo em email (himalaya MML) |
| `references/ocr-card-extraction.md` | Workflow de OCR com tesseract para extrair dados de prints de extrato |
| `references/fluxo-recalculation-formula.md` | Fórmula completa e fontes para recalcular o fluxo de caixa |
| `references/monitoramento-cron-jobs.md` | Padrão de cron jobs para monitoramento automático (ex: vigia CCT FEAAC, AVISOS.md) |
