# Expansão de uma coorte de clientes-piloto

Use quando um novo cliente entra enquanto materiais de outros pilotos já estão em produção.

## Preservar ordem e escopo

1. Registrar o novo piloto no cadastro mestre e no backlog antes de produzir material.
2. Não interromper nem apagar entregas já iniciadas; incluir o novo cliente na sequência atual.
3. Tratar segmento, fatos confirmados, hipóteses, limites e próximo passo como campos separados.
4. Não presumir empresa, frota, ferramentas, volume, integrações ou dores que o cliente não confirmou.

## Matriz de paridade

Cada piloto deve receber o mesmo núcleo mínimo, adaptado ao nicho:

- ficha individual;
- apresentação setorial editável e PDF;
- quatro roteiros curtos;
- quatro áudios verificados;
- mensagem e ordem de envio;
- kit enxuto com apenas dois áudios e um PDF;
- registro da auditoria de segurança.

Controlar programaticamente a quantidade esperada por cliente. Quando a coorte crescer de N para N+1, atualizar índices, totais e textos que declarem o número de pilotos ou arquivos.

## Plataformas de terceiros

Quando o nicho usa plataformas fechadas — aplicativos de transporte, marketplaces, bancos, CRMs ou portais jurídicos — separar claramente:

- organização fora da plataforma que já pode ser demonstrada;
- integração futura que depende de API, permissão e validação;
- ações proibidas no piloto sem autorização;
- credenciais que nunca devem ser solicitadas ou armazenadas.

Exemplo: para um motorista de aplicativo, não prometer aceitar, cancelar, precificar ou confirmar corridas, nem solicitar senha da plataforma. O piloto pode começar pela agenda de corridas particulares, lembretes e registros informados pelo próprio motorista.

## Gate final da família de materiais

1. Exportar todos os decks para PDF.
2. Confirmar a mesma quantidade de slides esperada por deck.
3. Renderizar todos os slides e auditar visualmente a família inteira.
4. Validar idioma no texto extraído dos PDFs, não apenas nos fontes Markdown/Python.
5. Verificar integridade e duração real de todos os áudios.
6. Atualizar índices usando durações reais e totais recalculados.
7. Executar o auditor de segurança.
8. Registrar o resultado no log append-only.
9. Executar novamente o auditor, pois o próprio log alterou o projeto.
10. Só então versionar, sincronizar e comparar origem/destino por manifesto SHA-256.
