# Registro de Gasto Avulso — Restaurante / Lazer

Fluxo completo quando Usuário envia foto de nota fiscal de restaurante/lazer pago com cartão de crédito:

## 1. OCR da Nota

```bash
tesseract imagem.jpg stdout -l por+eng --psm 3 2>/dev/null
```

- A qualidade do OCR em fotos de notinha térmica é frequentemente ruim
- Tentar: upscale 2-3×, grayscale, contraste 1.5-2.0×, `--psm 3`
- Se ilegível, extrair pelo menos: nome do restaurante, endereço, valor total
- Confirmar visualmente com o usuário se os valores não baterem

## 2. Registrar Restaurante (se novo)

Criar/atualizar `/home/usuario/MEGA/Documentos/Restaurantes/INDEX.md`:

```markdown
# 🍽️ Restaurantes — Registro de Gastos

## 📊 Média de Preços
| Restaurante | Visitas | Gasto Total | Média |
|---|---|---|---|

## 🔍 Fichas dos Restaurantes
### Nome Restaurante
| | |
|---|---|
| **Endereço** | ... |
| **Tipo** | Restaurante/Pizzaria/Bar |
| **Primeira visita** | data |

#### Histórico de Visitas
| Data | Valor | Cartão | Companhia | Obs |
|---|---|---|---|---|
```

## 3. Salvar Comprovante no Mês da Fatura

⚠️ O mês da pasta é o **mês de vencimento da fatura**, não o mês da compra.

- Copiar imagem original: `AAAA-MM-DD_NOTA-RESTAURANTE-RVALOR.jpg`
- Criar `.md` com metadados: restaurante, data, valor, cartão, fatura, companhia, categoria de orçamento

## 4. Atualizar Ficha do Cartão

Em `_fichas/FICHA_CARTAO_BANCO_NOME_FINAL.md`:

- Se o cartão estava zerado: reativar, mudar status para 🔴 Aberta
- Adicionar linha na tabela de lançamentos do mês da fatura
- Atualizar total da fatura

## 5. Atualizar Orçamento (ORCAMENTO-AREAS.md)

O gasto entra no **Pote 3 (Aluguel → prazer/lazer)**:

| Tipo de gasto | Categoria | Teto |
|---|---|---|
| Restaurante c/ amigos | 🎮 Lazer Pessoal | R$ 150 |
| Restaurante c/ namorada | 💑 Namoro → Date/restaurante | R$ 150 |
| Qualquer lazer sem categoria | 💸 Dinheiro Livre | R$ 300 |

- Se exceder o teto da categoria, cobrir com Dinheiro Livre
- Atualizar tabela de consolidação: faturas do mês, saldo, CDB (efeito cascata)
- Recalcular CDB mínimo

## 6. Cascata Financeira

```
Compra R$ X no cartão
  → Fatura do cartão sobe R$ X no mês de vencimento
  → Consolidação: 💳 Faturas ativos aumenta R$ X
  → 🟢 Saldo diminui R$ X
  → 📦 CDB final diminui R$ X (efeito cascata em todos os meses seguintes)
  → CDB mínimo recalculado
```
