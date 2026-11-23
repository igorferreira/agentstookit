# Dashboard financeiro: desligamento mensal e dicas determinísticas

## Padrão de implementação validado

Para dashboards pessoais alimentados por Markdown/JSON:

1. Buscar automaticamente o arquivo mensal mais recente por padrão estrito `rescisao_YYYY-MM.md`; não hardcode o mês no parser.
2. Separar pedido de demissão com aviso dispensado, pedido com aviso descontado e dispensa sem justa causa.
3. Carregar proveniência: fonte, data de referência, status de incerteza e aviso de que não é TRCT oficial.
4. Excluir seguro-desemprego quando a inelegibilidade estiver documentada.
5. Aceitar formatos numéricos pt-BR (`32.179,37`) e legado anglo (`32,179.37`), testando os resultados contra a tabela da fonte.
6. Gerar dicas determinísticas com prioridade, categoria, evidência, recomendação, impacto, status e fonte.
7. Dicas podem sugerir revisão/proteção, mas nunca executar pagamento, cancelamento, transferência, alteração de cartão ou uso de limite como patrimônio.
8. Testar: fonte mais recente, três cenários, valores, cobertura, fonte ausente, margem negativa, JSON sem PII, `node --check`, geração idempotente e rotas HTTP 200.
9. No cockpit, distinguir margem estrutural, margem efetiva, pior CDB e cenário-base; não esconder meses negativos cobertos pela reserva.

## Riscos a revisar

- VALLO não pode ser contado duas vezes: separar renda e cobertura do Home Equity.
- Custo de vida orçamentário não substitui o custo mensal comprometido com dívida, Home Equity e imprevistos.
- CDB atual, mínimo e final precisam de competência e cenário.
- Estimativas e dados confirmados precisam de rótulos diferentes.
- Ausência de fonte não deve virar zero silencioso.
- Parcelamentos parcialmente mapeados devem ser marcados como não totalmente confirmados.

## Critérios de aceite

Cada KPI e cenário deve possuir fórmula ou fonte, competência e classificação. Testes devem cobrir cenário-base, estresse, déficit, CDB zerado e fonte ausente. O frontend permanece somente leitura e não dispara ações financeiras.
