# Evolução de dashboards financeiros estáticos

Quando um dashboard é construído por etapas, preserve uma pasta `tasks/` no diretório do projeto com `README.md`, `BACKLOG.md` e arquivos numerados por etapa. Cada task deve registrar data, objetivo, fontes canônicas, decisões, arquivos, testes, ressalvas e estado final.

Para uma tela de orçamento diário sem arquivo canônico de gastos realizados, mostrar somente um limite calculado. Identificar na interface: fonte, número de dias da referência, fórmula e que o realizado ainda não está disponível. Nunca apresentar o limite derivado como gasto real.

Após cada alteração: regenerar JSON/HTML, executar testes de parser/cálculo/reconciliação, validar todos os JS com `node --check`, testar todas as rotas HTTP e atualizar o relatório de revisão.,