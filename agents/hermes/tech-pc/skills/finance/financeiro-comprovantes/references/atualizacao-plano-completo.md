# Atualização completa do plano financeiro

> **Trigger:** "financeiro atualiza todo o nosso plano", "atualiza tudo", ou quando múltiplos pagamentos + resgate CDB ocorrem na mesma sessão.

## Quando usar

Quando Usuário fizer múltiplas operações financeiras significativas em sequência (pagamentos de cartão, resgates de CDB, acordos pessoais) e pedir para atualizar o plano completo — ou quando a sessão claramente demanda sincronização de todos os arquivos após transações.

## Ordem da cascata (14 arquivos, nesta ordem)

### Fase 1: saldos (`_saldos/`)

| # | Arquivo | O que atualizar |
|---|---|---|
| 1 | `SALDO_BANCO.md` (cada conta afetada) | Saldo final, tabela de transações |
| 2 | `INDEX.md` | Todos os saldos, data |

### Fase 2: controles do mês (`YYYY/YYYY_MM_MES/`)

| # | Arquivo | O que atualizar |
|---|---|---|
| 3 | `AAAA-MM_00_CONTROLE_PAGAMENTOS.md` | Linhas afetadas: status → ✅ Pago, fonte pagadora, link comprovante, data de revisão no header |
| 4 | `AAAA-MM_00_DIVIDA.md` | Seção 2 (status dos itens), seção 3 (Pagos no mês), header data, total se mudou |
| 5 | `AGENDA.md` | Itens pagos, header data |

### Fase 3: canônicos da raiz

| # | Arquivo | O que atualizar |
|---|---|---|
| 6 | `ENDIVIDAMENTO.md` | Tabela de cartões ativos, seção de decisão, log de auditoria no final, CDB, contagem de ativos/negociação |
| 7 | `AVISOS.md` | Nova entrada 🔵 com resumo da operação (valor, data, impacto) |

### Fase 4: índices

| # | Arquivo | O que atualizar |
|---|---|---|
| 8 | `_controles/CONTROLE_INDICE.md` | Data, contagem de cartões por categoria, status do fluxo |
| 9 | `YYYY/YYYY_MM_MES/INDEX.md` | Data de revisão, novos arquivos listados |

### Fase 5: comprovantes individuais

| # | Arquivo | O que atualizar |
|---|---|---|
| 10+ | `.md` de cada comprovante | Criar se novo, com metadados padrão (data, valor, origem, destino, IDs) |
| 10+ | Controle de acordo (ex.: Paulo Guerra) | Status, comprovante vinculado |

## Checklist pós-atualização

- [ ] Todos os arquivos de `_saldos/` batem com os valores reais
- [ ] `CONTROLE_PAGAMENTOS` e `DIVIDA` estão sincronizados (pago em ambos)
- [ ] `AGENDA.md` reflete os pagamentos
- [ ] `ENDIVIDAMENTO.md` tem contagem correta de ativos/negociação/quitados
- [ ] `AVISOS.md` tem entrada do dia
- [ ] `CONTROLE_INDICE.md` tem data e contagem atualizadas
- [ ] `INDEX.md` do mês lista os novos arquivos
- [ ] Nenhum pipe duplo (`||`) nas tabelas (ver pitfall abaixo)
- [ ] Links entre comprovante, controle, dívida e agenda são relativos e funcionam

## Pitfalls

### Patch em linhas de tabela Markdown — pipes duplos

⚠️ **Ocorreu em 10/08/2026:** Ao usar `patch` para adicionar/editar linhas de tabela no `CONTROLE_PAGAMENTOS.md`, o `old_string` parecia começar com `|` (pipe único) mas o `read_file` mostra `LINE_NUM|CONTENT` — o primeiro `|` do output do `read_file` é o número da linha, não conteúdo do arquivo.

**Erro:** usei `||` como início do `new_string` (pensando que o pipe único era parte do conteúdo), criando linhas com pipes duplos que quebraram a tabela.

**Correto:** sempre usar `|` como primeiro caractere, nunca `||`. Verificar com:
```bash
head -n <N> arquivo.md | cat -A  # revela caracteres reais
```

**Regra:** depois de qualquer patch em tabela, reler a região editada e verificar que não há pipes extras.
