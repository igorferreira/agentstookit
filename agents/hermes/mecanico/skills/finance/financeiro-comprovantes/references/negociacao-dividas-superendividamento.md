# Negociação de dívidas de cartão e superendividamento

Use esta referência para planos de renegociação de dívidas de consumo no Brasil. É metodologia técnico-informativa; não substitui advogado/OAB.

## 1. Dados mínimos antes da proposta

- Dívida total declarada e dívida documentalmente conciliada — mostrar ambas.
- Matriz por contrato: credor, produto, final, principal, encargos, pagamentos, saldo, CET, garantia, vencimento e status.
- Renda disponível recorrente.
- Custo de vida/minimum existencial informado pelo usuário.
- Margem para dívida: `renda disponível - custo de vida`.
- Dívidas garantidas, alimentares, fiscais, imobiliárias e rurais separadas das dívidas de consumo elegíveis.
- Pedaladas/pagamentos cruzados separados para evitar dupla contagem.

Nunca fechar plano global enquanto houver fatura relevante ausente ou sobreposição não conciliada.

## 2. Cálculos obrigatórios

### 2.1 Normalização das premissas

Antes dos cenários, montar um fluxo auditável:

```text
remuneração CLT bruta = salário-base + parcela fixa/CCT
salário CLT líquido = bruto - INSS - IRRF - empréstimo/descontos recorrentes
recursos em conta = salário CLT líquido + benefícios líquidos utilizáveis
margem prudencial = recursos em conta - teto de custo de vida
```

Regras:

- O contracheque mensal normal mais recente é a fonte da remuneração recorrente; férias, 13º e complemento retroativo não servem como mês-base.
- Benefício utilizável pode entrar em “recursos em conta”, mas deve permanecer em linha separada e nunca ser renomeado como salário.
- Somar as linhas do mapa de custos por cálculo independente. Um total escrito pode estar incorreto mesmo quando a diferença é pequena.
- Se `fixos comprovados < teto confirmado`, exibir `fixos comprovados — incluídos no teto` e subtrair somente o teto. Não fazer `recursos - fixos - teto`.
- Não misturar parcelas de dívida/cartão com custo de vida; elas serão tratadas no orçamento de quitação.

### 2.2 Cenários de quitação

Para horizonte `n` meses:

- Parcela nominal: `dívida total / n`.
- Margem mensal: `recursos em conta - teto de custo`.
- Folga sem desconto: `margem mensal - parcela nominal`.
- Capacidade matemática total: `margem mensal × n`.
- Valor do acordo por desconto `d`: `dívida × (1 - d)`.
- Parcela do acordo: `valor do acordo / n`.
- Folga após acordo: `margem mensal - parcela do acordo`.
- Desconto mínimo de uma meta mensal: `(dívida - meta_mensal × n) / dívida`.

Distinguir no documento:

- **meta negocial:** parcela desejada, com folga confortável e desconto-alvo;
- **teto absoluto:** parcela nominal máxima que ainda preserva o custo e uma contingência definida;
- **capacidade matemática:** não deve ser automaticamente comprometida por inteiro.

Simular, no mínimo, cenário sem desconto, meta recomendada e vários descontos. Desconto anunciado é hipótese negocial. Comparar sempre valor total, CET, entrada, parcelas e efeito de quitação.

### 2.3 Requalificação obrigatória

Quando salário, benefício, custo de vida ou dívida total mudarem:

1. recalcular toda a tabela, não fazer apenas substituição textual;
2. reavaliar se existe impossibilidade manifesta de pagamento sem comprometer o mínimo existencial;
3. retirar afirmação de superendividamento se a nova margem demonstrar viabilidade nominal, mantendo a via legal apenas como subsidiária quando apropriado;
4. recalcular home equity nos cenários com e sem garantia;
5. atualizar modelos de proposta, indicadores, conclusão e limitações — não apenas o resumo executivo.

## 3. Base jurídica essencial

- CDC aplicável a instituições financeiras: Súmula 297/STJ.
- Lei 14.181/2021: superendividamento de pessoa natural de boa-fé e repactuação pelo CDC, arts. 54-A e 104-A a 104-C; plano pode chegar a 5 anos, mas pode propor prazo menor.
- Lei 14.690/2023/CMN: no rotativo e parcelamento de fatura abrangidos, juros e encargos não podem ultrapassar 100% do principal financiado. Não generalizar como “toda dívida está limitada ao dobro”.
- CDC art. 42: cobrança não pode expor ao ridículo, constranger ou ameaçar.
- CDC art. 43: negativação tem limite legal; não confundir fim do cadastro negativo com extinção da dívida.
- Consumidor.gov.br exige resposta no prazo da plataforma, mas não obriga o credor a conceder desconto.
- Dívida com garantia real/home equity tem risco próprio e pode ficar fora do procedimento global de superendividamento.
- Proteção de salário e bem de família não é premissa absoluta: considerar exceções legais e relativizações jurisprudenciais.

Priorizar fontes oficiais: Planalto, Banco Central, CNJ, STJ e Consumidor.gov.br. Verificar regras atuais na data da análise.

## 4. Boa-fé e atraso planejado

Um prazo empírico (90, 180, 280 dias) é apenas marco de reavaliação, não direito a desconto.

- Contar o atraso a partir do vencimento efetivamente não pago.
- Interromper novas compras, saques e transferências no crédito que o usuário sabe não conseguir pagar.
- Não ocultar patrimônio, ignorar citação ou criar contratos sem intenção de pagamento.
- Negociar em ondas: pedido documental; proposta direta; Consumidor.gov.br; Procon/CEJUSC; avaliação de repactuação judicial.
- Aceitar acordo antecipado se ele quitar a obrigação e couber no teto global; não esperar passivamente um dia “mágico”.

## 5. Home equity

Nunca tratar home equity como evento gratuito de liquidez.

1. Calcular primeiro o cenário **sem garantia**: `margem - parcela nominal da dívida`.
2. Calcular o fluxo do home equity: `recursos - teto de custo - parcela home equity`.
3. Se o crédito não quitar toda a dívida, calcular também `saldo restante / horizonte` e a folga final após as duas parcelas.
4. Se a margem ficar negativa ou sem contingência, rejeitar como plano sustentável.
5. Se a operação ficar matematicamente possível, isso não basta para recomendá-la: comparar com o cenário sem garantia, CET total, prazo, seguros, custo de registro, risco de mora e execução do imóvel.
6. Não converter dívida sem garantia em dívida garantida pelo imóvel para pagar apenas parte dos cartões sem acordos globais escritos.
7. Considerar somente após revisão jurídica do contrato, preservação de reserva e fluxo mensal positivo.
8. Distinguir “quitar cartões” de “ficar sem dívidas”: home equity refinancia e normalmente prolonga a obrigação além do horizonte dos cartões.
9. Se a via sem garantia já quita a dívida no prazo com folga, tratá-la como opção preferencial, salvo vantagem de CET total robustamente demonstrada.

## 6. Estrutura recomendada do plano

1. Conclusão executiva e teto mensal.
2. Documentos e premissas.
3. Diagnóstico financeiro/documental.
4. Enquadramento jurídico e mitos corrigidos.
5. Cenários econômicos.
6. Fases de 0–15, 16–90, 91–180, 181–280 dias e meses restantes.
7. Estratégia por classe de dívida.
8. Home equity: condições de veto e eventual uso.
9. Modelos de solicitação documental, proposta e Consumidor.gov.br.
10. Checklist para advogado/Procon/CEJUSC.
11. Indicadores, gatilhos e limitações.
12. Fontes oficiais.

## 7. Geração de Markdown e PDF

- Criar Markdown canônico e gerar PDF A4.
- No Pandoc, use YAML frontmatter (`title`, `author`, `date`, `subtitle`) para evitar título duplicado com `--toc`.
- Em CSS para wkhtmltopdf, force `:root { color-scheme: light only; }` e `html, body { background:#fff !important; color:#... !important; }`.
- Defina explicitamente fundo de `td`, linhas pares/ímpares, cabeçalhos e TOC; ambiente com tema escuro pode tornar áreas transparentes ilegíveis.
- Para manter tabelas inteiras, use:

```css
table, thead, tbody, tr {
  page-break-inside: avoid !important;
  break-inside: avoid-page !important;
}
.page-break {
  display: block;
  page-break-before: always !important;
  break-before: page !important;
  height: 0;
}
```

- Tabelas maiores que uma página são exceção: permita quebra e repita `thead`; nunca reduza a fonte até ficar ilegível apenas para forçar uma página.
- `page-break-after: avoid` em `h2/h3` pode ser ignorado pelo wkhtmltopdf. Se o título ficar sozinho no rodapé, inserir `<div class="page-break"></div>` **antes do título da seção**, não entre o título e a tabela.
- Cada quebra explícita pode deslocar o restante do documento. Depois de qualquer correção, renderizar **todas** as páginas (`pdftoppm`) e montar um contact sheet para auditoria global; não inspecionar apenas as páginas originalmente problemáticas.
- Fazer também auditoria textual por limite de página: executar `pdftotext -f N -l N -layout` para cada página e comparar as primeiras e últimas linhas não vazias. Um `h2/h3`, rótulo como “Plano A”, “Fase N” ou título de checklist no fim da página, seguido do conteúdo na página seguinte, é órfão mesmo quando o contact sheet em baixa resolução não evidencia o problema.
- Ao encontrar título órfão, inserir `<div class="page-break"></div>` **antes do título** no Markdown canônico; nunca entre título e conteúdo. Regerar o documento inteiro imediatamente.
- Verificar efeitos em cascata depois de cada quebra: a correção de um título pode isolar outro título, deixar somente o primeiro item de uma lista na página anterior, criar uma página em branco/quase vazia ou empurrar o parecer final para uma página própria.
- Para listas numeradas e checklists, não aceitar apenas um item isolado numa página. Mover o subtítulo e a lista juntos quando possível.
- Para a conclusão, evitar uma página contendo somente o parecer final. Agrupar de forma lógica, por exemplo `Fontes + Limitações + Parecer`, ou reservar página completa para uma seção conclusiva substancial.
- Na auditoria visual, conferir: tabela dividida, título/subtítulo órfão, uma única linha de checklist isolada, página em branco/quase vazia, cortes, sobreposição, contraste e duplicação do título.
- Remover quebras explícitas que deixarem de ser necessárias após o fluxo mudar; isso evita páginas extras ou grandes vazios.
- Extrair texto do PDF e validar valores-chave, ausência de `�`, número de páginas e termos jurídicos. Opcionalmente medir pixels não brancos das páginas renderizadas para detectar página realmente vazia.
- Verificar em alta resolução a primeira página, **todas as páginas com tabelas**, toda página que recebeu quebra manual e a última página antes de entregar.
- Para Usuário, manter e entregar sempre os dois artefatos sincronizados: Markdown canônico atualizado e PDF derivado. Nunca corrigir apenas o PDF.

## 8. Pitfalls

- Não prometer desconto de 90% ou afirmar que um banco “não processa” abaixo de certo valor.
- Não usar benchmark fixo de desconto como fato; apresentar cenários.
- Não chamar provisão/fundo de negociação de ocultação patrimonial.
- Não recomendar ignorar citação ou mover dinheiro para frustrar credores.
- Não adicionar benefício não salarial à remuneração/rescisão; use somente como renda disponível quando a regra do usuário permitir.
- Não dizer que plano de 24 meses é viável sem provar a capacidade matemática.
