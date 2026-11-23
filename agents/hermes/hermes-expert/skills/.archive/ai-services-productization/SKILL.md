---
name: ai-services-productization
description: "Use when turning AI setup/support into a sellable service."
metadata:
  version: 1.0.0
---

# AI Services Productization

## Objetivo

Transformar instalação, configuração, manutenção, treinamento e evolução de agentes de IA em um serviço comercial claro, demonstrável e sustentável.

Use esta skill quando o trabalho envolver empacotar consultoria de IA, criar oferta recorrente, preparar pilotos, apresentações comerciais, roteiros de descoberta, materiais em áudio ou backlog de lançamento.

## Regras de comunicação para este usuário

- Produzir todo o conteúdo em **português do Brasil**. Fazer uma revisão final específica de idioma antes da entrega; não confiar apenas no prompt do modelo.
- Nomes de arquivos devem usar palavras corretas em português do Brasil, sem acentos. Exemplo: `CRIACAO`, nunca `CREACAO` ou `CREACION`.
- Para mensagens de WhatsApp: frases curtas, uma ideia por linha e texto pronto para copiar em bloco de código.
- Evitar promessas técnicas não verificadas. Apresentar possibilidades como possibilidades até conhecer sistemas, dados e integrações reais do cliente.
- Não afirmar números de lojas, candidaturas, cargos, dores internas, resultados ou integrações sem fonte confirmada.

## Fluxo obrigatório

### 1. Descobrir o resultado que o cliente compra

Não vender “instalação de software”. Identificar o ganho esperado:

- menos trabalho repetitivo;
- informação organizada;
- acompanhamento de prazos e pendências;
- redução de erros;
- melhoria do atendimento;
- apoio à decisão com controle humano.

Registrar separadamente:

- problema atual;
- frequência;
- pessoas envolvidas;
- ferramentas atuais;
- impacto em tempo, dinheiro ou risco;
- resultado mínimo que provaria valor.

### 2. Definir um recorte inicial

Começar por **um problema, um fluxo e um responsável humano**. Não prometer automação integral antes de mapear sistemas e dados.

Exemplo de recorte: receber uma demanda, classificar, registrar, alertar o responsável e acompanhar até a conclusão.

### 3. Estruturar a oferta

Separar explicitamente:

- diagnóstico;
- instalação;
- configuração;
- personalização;
- migração ou organização de dados;
- treinamento;
- manutenção;
- suporte;
- consumo de modelos e serviços externos;
- novos desenvolvimentos fora do escopo.

A cobrança deve distinguir:

1. **implantação/setup** — remunera diagnóstico e construção inicial;
2. **mensalidade** — remunera manutenção, suporte e evolução limitada;
3. **custos de terceiros** — modelos, hospedagem, canais e APIs;
4. **serviços extraordinários** — integrações e novos módulos.

Nunca usar “ajustes ilimitados” sem política de uso justo, limite de horas ou definição objetiva de ajuste pequeno.

### 4. Desenhar um piloto controlado

Piloto gratuito ou subsidiado precisa de:

- duração definida;
- apenas um caso de uso;
- dados e acessos mínimos;
- responsável humano do cliente;
- critérios de sucesso mensuráveis;
- data de início e encerramento;
- regra de desligamento ou conversão;
- custos externos previamente combinados;
- nenhuma renovação automática escondida.

A gratuidade do piloto não deve significar manutenção gratuita indefinida. Antes de iniciar, informar por escrito o que passa a ser cobrado depois e em quais condições.

### 5. Preparar a apresentação

Ordem recomendada:

1. contexto do cliente;
2. problema observado ou hipótese a validar;
3. resultado desejado;
4. demonstração de um fluxo;
5. limites e controle humano;
6. proposta de piloto;
7. próximo passo simples.

Quando houver vários contextos — empresarial, institucional e pessoal — apresentar como módulos separados, sem misturar dados, acessos ou memórias.

### 6. Fazer descoberta antes de prometer

Perguntas mínimas:

- Qual atividade mais consome tempo hoje?
- Quem executa e quem aprova?
- Onde os dados estão?
- Qual ferramenta já é usada?
- O que não pode sair do ambiente?
- Qual erro ou atraso mais prejudica?
- Como saberemos em 15 ou 30 dias que o piloto funcionou?
- Quem será o ponto focal técnico e operacional?

Transformar respostas em fatos, hipóteses e pendências. Não escrever como fato aquilo que ainda é apenas ideia de venda.

### 7. Criar materiais comerciais em camadas

Manter materiais separados:

- mensagem curta de primeiro contato;
- apresentação geral;
- explicação de funcionamento;
- perguntas e respostas;
- roteiro de descoberta;
- proposta formal;
- roteiro de piloto;
- treinamento inicial;
- perguntas pós-piloto;
- estudo de caso, somente após resultado real.

Para áudios, preservar sempre:

- roteiro em Markdown;
- arquivo de áudio;
- idioma e voz usados;
- duração;
- público e finalidade;
- data compacta no nome: `AAAAMMDD_TIPO-DESCRICAO.ogg`.

Ver `templates/serie-audios-comerciais.md`.

### 8. Manter execução auditável

Estrutura mínima do projeto:

- visão do negócio;
- backlog;
- preços e escopo;
- marca e comunicação;
- materiais por cliente;
- áudios;
- contratos e políticas;
- operação e suporte;
- histórico de decisões.

Após cada mudança:

1. atualizar backlog e índice;
2. verificar arquivos gerados;
3. versionar no repositório;
4. sincronizar o backup, quando configurado;
5. confirmar que não há dados sensíveis em repositório ou material comercial.

## Armadilhas

- Escolher marca antes de esclarecer a promessa central.
- Vender capacidade abstrata de IA em vez de um resultado concreto.
- Criar três módulos completos para um prospect antes de validar um único fluxo.
- Oferecer piloto sem prazo, métrica ou condição de conversão.
- Cobrar apenas manutenção depois de doar uma implantação extensa sem limite.
- Confundir software de terceiros com marca própria ou insinuar parceria oficial inexistente.
- Colocar segredos, credenciais, dados de clientes ou áudios confidenciais no Git.
- Usar depoimentos ou estudos de caso sem autorização.
- Produzir texto híbrido entre português e espanhol; fazer revisão lexical antes de salvar e antes de gerar PDF/áudio.

## Critérios de conclusão

A oferta só está pronta para apresentação quando existem:

- público inicial definido;
- problema inicial definido;
- piloto com escopo e métrica;
- preço pós-piloto comunicado;
- responsabilidades de ambas as partes;
- exclusões claras;
- mensagem curta;
- roteiro de descoberta;
- apresentação e perguntas frequentes;
- backlog com próximo passo;
- verificação de idioma e privacidade.

## Referências

- `references/timeautomatico-case-study.md` — aprendizados condensados do projeto TimeAutomático, sem transformar detalhes temporários em regras universais.
- `templates/serie-audios-comerciais.md` — estrutura reutilizável para apresentação, funcionamento e perguntas frequentes em áudio.
