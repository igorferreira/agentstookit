# Controle de saídas internas em dashboards financeiros

## Escopo

Separar combustível, supermercado/estoque e comida na rua/restaurante/delivery. Não misturar automaticamente essas classes com contas recorrentes, eventos extraordinários, faturas ou dívidas.

## Fontes canônicas

- `~/MEGA/Documentos/financas_bancos/GASTOS-COMBUSTIVEL.md`: abastecimentos, litros, preço por litro, posto, odômetro e total.
- `~/MEGA/Documentos/financas_bancos/PRECO-SUPERMERCADO-REGISTRO.md`: lista padrão mensal e histórico append-only de preços.
- `~/MEGA/Documentos/financas_bancos/ESTOQUE-ALIMENTOS.md`: retrato atual do estoque e data de conferência.
- `~/MEGA/Documentos/lazer_interesses/restaurantes/INDEX.md`: cadastro e histórico de estabelecimentos.

## Modelo de dados

Distinguir explicitamente: planejado, comprado/realizado, preço observado, estoque atual e gasto efetivo. Ausência de quantidade, preço, data ou estoque mínimo deve permanecer `Não informado`, nunca zero.

Lista inicial de compras: 6 kg de peito de frango, 4 kg de patinho moído, 30 ovos, 6 kg de arroz integral, 4 kg de feijão, manteiga, 1 kg de açúcar, 1 kg de sal e 1 garrafa de azeite.

## Ingestão por agente

Ao receber nota, foto, print ou mensagem: identificar a classe; preservar o original; extrair somente campos comprovados; acrescentar ao histórico sem apagar registros; atualizar o estoque apenas com conferência explícita; relacionar fatura/comprovante para evitar dupla contagem; regenerar o dashboard; executar testes; relatar campos pendentes.

## Telas recomendadas

1. Saídas internas: combustível, supermercado e comida na rua, com total realizado, quantidade, média e comparação mensal.
2. Lista/preços: quantidades planejadas, compradas, preço total/unitário, local, marca e histórico por mês.
3. Estoque: item, quantidade, unidade, mínimo, nível, data da conferência e observações.
4. Histórico: menor, maior e último preço conhecido, sempre com fonte e data.

A existência dos Markdown não basta para concluir a tarefa: parsers, JSON, rotas, menu, responsividade, testes e proteção contra dupla contagem precisam ser verificados.