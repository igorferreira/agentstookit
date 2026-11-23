# Governança de dashboards financeiros estáticos

## Fonte canônica e derivação

- Mantenha fatos em Markdown/YAML canônico, fora de `publicacao/`.
- Cada novo documento canônico precisa de parser, seção determinística no JSON, teste e rota validada.
- Preserve `Não informado` e diferencie confirmado, planejado, provável, pago e derivado.
- Nunca corrija valores editando HTML/JSON gerado.

## Telas e QA

Ao adicionar uma tela, atualize o menu compartilhado, a lista de cópia do gerador, os testes, `node --check`, rotas HTTP locais e a documentação.

Para celular, tablet e PC: use grids responsivos, menu quebrável/touch-friendly, tabelas com overflow horizontal controlado e testes em retrato e paisagem. Não esconda dados financeiros apenas para caber na tela.

## Git e nuvem

`.gitignore` controla o Git; não prova exclusão em MEGA, Google Drive ou Insync. Para projetos em pasta sincronizada, verificar cada provedor separadamente e só declarar exclusão após confirmar a regra no cliente. Links ngrok são efêmeros: validar a URL e rotas, mas nunca salvá-la no Git ou no Markdown canônico.

## Governança

`TASKS.md` registra tarefas; `tasks/BACKLOG.md` registra melhorias; a fila geral permanece no arquivo de fila definido pelo projeto. O dashboard é somente leitura e não executa ações financeiras.
