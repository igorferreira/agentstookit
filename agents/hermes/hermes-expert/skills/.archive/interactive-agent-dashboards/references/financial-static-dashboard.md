# Dashboard financeiro estático gerado por Markdown

Use esta referência quando o dashboard for pessoal/financeiro, sem banco de dados, gerado por Python a partir de Markdown/YAML.

## Contrato

- Markdown/YAML canônico é a única fonte da verdade.
- Python gera JSON determinístico minimizado e as páginas HTML/CSS/JS.
- Nunca corrigir números editando HTML manualmente.
- Servidor local deve ouvir somente em `127.0.0.1`; ngrok é opt-in e temporário.
- Fontes brutas ficam fora do diretório servido.

## Páginas

Use um menu compartilhado para páginas independentes: fluxo de caixa, contas/cartões pagos e orçamento. Todas leem o mesmo snapshot JSON.

## Extração

Parseie explicitamente os controles Markdown de pagamentos, saldos e orçamento. Preserve estados honestos: confirmado, parcial, estimado, pendente e desconhecido. Nunca transforme ausência em zero. Mascarar dados bancários e pessoais no artefato público.

## Gráficos

Para dashboards offline simples, prefira SVG inline gerado por Vanilla JS em vez de barras CSS frágeis. Re-renderize em `resize`, inclua `role="img"`/`aria-label` e valide a existência dos elementos SVG no teste/QA.

## Testes mínimos

- Parser YAML/esquema;
- valores monetários com `Decimal`;
- cenários e piso do CDB em zero;
- extração de pagamentos e orçamento;
- JSON determinístico;
- exclusão de CPF/agência/identificadores sensíveis;
- sintaxe de todos os JS;
- rotas geradas e HTTP 200;
- headers CSP e `Cache-Control: no-store`.

## Revisão pós-implementação

Revisar código, reconciliação com fontes, segurança, todas as rotas, responsividade desktop/retrato/paisagem e visual. Classificar como `APROVADO`, `APROVADO COM RESSALVAS` ou `REPROVADO`; não declarar final se a QA visual do navegador ainda estiver pendente.
