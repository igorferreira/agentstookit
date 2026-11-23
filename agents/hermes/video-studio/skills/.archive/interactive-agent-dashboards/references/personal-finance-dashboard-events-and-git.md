# Dashboard financeiro: eventos extraordinários e Git seguro

## Fonte canônica e tela

- Mantenha eventos extraordinários em um Markdown dedicado, por exemplo `EVENTOS-EXTRAORDINARIOS.md`.
- Registre mês, evento, motivo, valor conhecido, parcelamento, impacto mensal, categoria, status e fonte.
- Preserve `Não informado`; nunca converta ausência em zero.
- O parser deve agrupar headings `## Mês/Ano` e subseções `### N. Evento` em JSON.
- A tela é somente leitura e deve manter eventos extraordinários separados de recorrências, faturas e orçamento.
- Mostre o total nominal conhecido separadamente; eventos sem valor não entram no total.

## Atualização mensal

- Para documentos de rescisão, selecione o arquivo mais recente no padrão `rescisao_YYYY-MM.md`.
- Exponha data da fonte, tipo de cenário, status de estimativa e meses de cobertura.
- Valide números brasileiros e legados: `32.179,37` e `32,179.37` devem resultar em 32179.37.
- Marque cálculos como estimativa e não como TRCT oficial.

## Git e sincronização

1. Verifique autenticação do GitHub sem expor token.
2. Inicialize o repositório dentro do projeto, use branch `main`, crie `.gitignore` antes do primeiro `git add`.
3. Crie o repositório explicitamente privado com `gh repo create --private --source=. --remote=origin --push`.
4. Verifique URL, privacidade, branch, commit, push e `git status`.
5. `.gitignore` não controla clientes de nuvem. Configure exclusão no Mega/Insync/Google Drive separadamente.
6. No MEGA, confirme a regra de arquivos ocultos ou `.megaignore` antes de declarar `.git` protegido.
7. No Insync, confirme a regra pela interface ou CLI licenciada; se o modo headless estiver bloqueado, registre como pendência e não alegue proteção concluída.
8. Nunca coloque credenciais, `.env`, chaves ou tokens no commit.

## QA mínimo

Após alterações: gerar o dashboard, executar `unittest`, `py_compile`, `node --check` em todos os JS e testar HTTP 200 para todas as páginas e JSON. Registrar ressalvas no relatório de revisão.
