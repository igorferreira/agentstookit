# Fluxo de Caixa — nota de legado

Este arquivo preserva apenas uma referência histórica. Não use as instruções, valores de exemplo, horizonte, planilhas ou procedimentos manuais antigos deste documento para atualizar o fluxo vigente.

## Procedimento válido

Para uma fatura nova ou outra mudança financeira que afete o fluxo:

1. Reconcilie a obrigação com a evidência primária e as fontes/controles mensais, separando valor confirmado, provisão, pagamento e saldo ainda aberto.
2. Leia o arquivo canônico vigente, os insumos aplicáveis, o estado atual do repositório e o escritor oficial; não presuma nomes, horizonte, estrutura YAML, motor ou formatos derivados.
3. Atualize apenas as fontes e os campos canônicos necessários, preservando alterações existentes fora do escopo.
4. Gere a família de saídas com o escritor oficial e reconstrua o dashboard se a mudança afetar seus dados ou interface.
5. Leia de volta os artefatos publicados, reconcilie totais e âncoras, e teste as rotas aplicáveis.

A referência operacional e seus gates estão em [`fluxo-caixa-source-of-truth.md`](fluxo-caixa-source-of-truth.md). Nunca edite à mão uma saída gerada para corrigir divergência: encontre a fonte/modelo correto e regenere.