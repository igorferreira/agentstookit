# Gate de segurança e apresentações por nicho

## Apresentações individuais

Não reutilizar um deck genérico trocando somente o nome. Manter identidade visual e estrutura comercial comuns, mas adaptar para cada nicho:

- vocabulário e exemplos;
- hipótese de problema a validar;
- fluxo inicial demonstrável;
- limites e controles humanos específicos;
- métrica do piloto;
- próxima ação solicitada.

Nunca declarar que o cliente possui determinada dor sem diagnóstico. Usar “podemos avaliar”, “hipótese inicial” e “o fluxo real será escolhido após diagnóstico”.

### Verificação de um deck

1. Validar a sintaxe do gerador.
2. Executar o gerador de verdade.
3. Exportar PPTX para PDF.
4. Confirmar quantidade de páginas.
5. Renderizar todos os slides e montar folha de contato.
6. Inspecionar cortes, colisões, contraste, palavras quebradas e densidade.
7. Revisar isoladamente os slides corrigidos.
8. Executar auditoria de idioma, privacidade e credenciais.

Escrever um script não equivale a gerar e verificar uma apresentação.

## Gate de segurança obrigatório

Cada projeto comercial deve possuir:

- Markdown canônico com as rotinas de segurança;
- auditor automático reutilizável;
- log append-only das auditorias;
- `.gitignore` bloqueando credenciais, chaves e caches;
- resultado explícito APROVADO/FALHA.

Executar o gate:

1. antes de cada commit;
2. antes de sincronizar backups;
3. antes de montar um kit de envio;
4. antes de enviar material externo;
5. depois de incorporar arquivos externos.

Se houver falha bloqueante, não versionar, sincronizar nem enviar. Corrigir e repetir a auditoria.

O auditor deve:

- limitar-se à pasta do projeto;
- ignorar `.git/` e caches;
- detectar extensões sensíveis, chaves privadas e padrões fortes de credenciais;
- revisar idioma nos materiais comerciais;
- imprimir somente categoria e caminho do arquivo, nunca o conteúdo nem o possível segredo;
- distinguir falhas bloqueantes de alertas para revisão humana.

Usar `scripts/auditar_materiais_comerciais.py` como base.

## Armazenamento verificável

- Preservar roteiros, áudios, PPTX, PDFs, scripts, índices, identidade visual, segurança e backlog.
- Excluir `.git/`, `__pycache__/` e `.pyc` ao espelhar o projeto.
- Comparar origem e destino por manifesto SHA-256 completo.
- Só declarar sincronização concluída quando não houver arquivos ausentes, extras ou divergentes.
- Registrar total auditado e identificação do commit no log.
