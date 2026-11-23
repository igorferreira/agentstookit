# Fatura em atraso confirmado + substituição de provisão por fatura completa

## Quando usar

Use este fluxo em dois cenários:

### 1. Fatura em atraso confirmado (imagem/captura)

O usuário envia uma captura do app mostrando "Sua fatura está em atraso", com valor atualizado (juros/multa). Difere de "fatura em aberto" porque:
- Já existe acréscimo por juros/multa em relação ao valor original
- O status é 🔴 e não ⬜
- Pode haver restrição de bloqueio iminente
- A dívida original pode estar em mês anterior ao controle atual

### 2. Fatura completa substitui provisão parcial

O usuário envia a fatura fechada oficial (PDF ou captura detalhada) de um cartão que até então só tinha provisão parcial. O valor documentado sobe, e o item muda de categoria:
- `obrigação parcial/provisionada` → `fatura completa/fechada`
- A provisão antiga é removida dos controles mensais
- O novo valor documentado entra como fatura completa

## Fluxo

### Passo 1: Extrair dados
- OCR + inspeção visual da imagem
- PDF: `pdftotext -layout` para extração limpa
- Identificar: valor atual, valor original (se houver diferença), dias em atraso, vencimento, multa/juros, pagamento mínimo, parcelas x/y, encargos, limite

### Passo 2: Verificar registro anterior
Buscar nos controles do mês se o cartão aparece como provisão, em aberto, ou sem informação.

### Passo 3: Calcular impacto
- Substituição: `diferença = valor_nova_fatura - valor_provisao_antiga; novo_total = total_anterior + diferença`
- Atraso novo: `novo_total = total_anterior + valor_atraso`

### Passo 4: Salvar arquivos
1. Salvar original na pasta do mês
2. Criar OCR bruto; se houver erros (ex.: RS no lugar de R$), criar OCR revisado
3. Criar .md canônico com identificação completa, composição, encargos e situação

### Passo 5: Atualizar controles em cascata

**Substituição de provisão:**
| Arquivo | Alteração |
|---|---|
| `DIVIDA.md` | Remover linha da provisão, inserir nova na seção "faturas completas" com nota "substitui provisão de R$ X" |
| `CONTROLE_PAGAMENTOS.md` | Substituir linha da provisão pela nova fatura; atualizar total |
| `DIAGNOSTICO` | Mover cartão de "obrigações parciais" para "faturas completas"; atualizar contagens e totais |

**Atraso confirmado:**
| Arquivo | Alteração |
|---|---|
| Mês atual — `DIVIDA.md` | Inserir linha com 🔴 e vencimento original |
| `CONTROLE_PAGAMENTOS.md` | Inserir linha com 🔴; total aumenta |
| `DIAGNOSTICO` | Cartão sai de "sem informação" → entra "em atraso comprovado" |

### Passo 6: Atualizar ativos derivados
- Relatório simplificado de cartões (nota 🔴)
- dados-vencimentos.json (entrada em meses_especificos)
- Agenda geral e agenda mensal

### Passo 7: Validar
- Soma das linhas = total declarado
- Links dos originais existem
- Cartão não aparece duplicado
- Contagem de cartões fecha: 26 = completas + parciais + zerados + atraso + sem informação

## Estratégia financeira — registro
Quando o usuário descrever uma operação planejada (ex.: pagar cartão A, Pix crédito no B, pagar C):
1. Registrar em "Notas/decisões" de `DIVIDA.md` como subseção "Estratégia registrada"
2. Calcular impacto projetado em cada cartão (antes → depois)
3. Calcular efeito líquido no endividamento total
4. Destacar riscos (juros rotativos, troca de credor sem amortizar)
5. Não alterar totais documentados — estratégia é intenção, não execução

## Pitfalls
- Não duplicar o valor: provisão antiga deve ser removida, não mantida junto com a fatura nova
- Atraso não é dívida do mês atual: se a fatura é de julho, aparece em ambos (julho: atualização, agosto: ainda em aberto)
- Não confundir "atraso comprovado" com "intenção de atrasar": o atraso só é confirmado por captura mostrando "em atraso" ou "X dias"
- Edição concorrente: antes de alterar controles, reler o estado atual
