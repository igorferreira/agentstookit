# Piloto, parceria, investimento e kit de envio

## Finalidade

Orientar a productização de serviços de agentes de IA quando a mesma pessoa pode aparecer como cliente-piloto, potencial sócio ou possível investidor.

## Separar os papéis

### Cliente-piloto

- Valida um problema real, um fluxo, o uso recorrente e a disposição para pagar.
- Participa de piloto com prazo, escopo, responsável e métricas.
- O piloto não concede participação societária, exclusividade ou direito sobre a propriedade intelectual.

### Potencial sócio

- Deve ser avaliado por contribuição concreta: execução, dedicação, vendas, capital, conhecimento ou canais.
- Antes de percentual, registrar metas, divisão de receitas e despesas, propriedade intelectual, poderes de decisão, confidencialidade e regras de saída.
- Tratar o piloto da empresa do potencial sócio separadamente da negociação societária.

### Possível investidor

- Não misturar pedido de investimento com o primeiro contato comercial.
- Conversar sobre aporte somente depois de evidências de problema, resultado, uso, preço aceito, receita e custo de suporte.
- Piloto gratuito não representa promessa de investimento nem reserva de participação.

## Série personalizada por cliente-piloto

Criar quatro peças curtas, preservando roteiro e áudio:

1. apresentação contextualizada ao segmento;
2. oportunidades descritas como hipóteses a confirmar;
3. piloto limitado, transparente e sem renovação escondida;
4. próximo passo ou perguntas para diagnóstico.

Padrão de nome:

- `AAAAMMDD_CLIENTE-01-APRESENTACAO.ogg`
- `AAAAMMDD_CLIENTE-02-OPORTUNIDADES.ogg`
- `AAAAMMDD_CLIENTE-03-PILOTO-GRATUITO.ogg`
- `AAAAMMDD_CLIENTE-04-PROXIMO-PASSO.ogg`

Validar programaticamente a quantidade esperada e a integridade dos arquivos de áudio.

## Kit de primeiro envio

Não despejar toda a biblioteca sobre o contato. A sequência recomendada é:

1. mensagem curta e personalizada;
2. um áudio de contexto;
3. apresentação em PDF;
4. um áudio sobre o piloto;
5. aguardar reação.

Guardar para a conversa seguinte:

- preços detalhados;
- arquivos editáveis;
- áudios adicionais;
- estratégia societária;
- documentos internos.

## Identidade visual antes do deck

Definir antes do material externo:

- conceito da marca;
- símbolo;
- paleta pequena;
- tipografia;
- versões de logotipo para fundo claro e escuro;
- ícone social;
- usos proibidos.

Gerar SVG editável e PNG. Renderizadores podem substituir fontes SVG e causar sobreposição; abrir o PNG exportado e inspecionar visualmente.

## Auditoria da apresentação

1. Exportar PPTX para PDF.
2. Confirmar quantidade de páginas.
3. Renderizar todos os slides em imagens e montar uma folha de contato.
4. Inspecionar cortes, sobreposição, contraste, densidade e consistência.
5. Revisar isoladamente os slides corrigidos.
6. Verificar especialmente palavras quebradas dentro de cartões e título de duas linhas colidindo com subtítulo.

## Salvamento e sincronização

- Preservar roteiros, áudios, editáveis, PDFs, índices e backlog.
- Versionar apenas materiais sem segredos.
- Ao espelhar um repositório em pasta sincronizada, excluir `.git/`; por exemplo, usar `rsync -a --delete --exclude='.git/' origem/ destino/`.
- Verificar arquivos principais na origem e no destino por checksum e comparar contagens esperadas antes de afirmar sincronização concluída.
