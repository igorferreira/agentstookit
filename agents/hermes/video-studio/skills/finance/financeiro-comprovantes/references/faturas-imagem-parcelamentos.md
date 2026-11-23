# Faturas por imagem: identificação, OCR e projeção de parcelas

Use este procedimento quando Igor enviar captura de aplicativo de cartão e pedir OCR, Markdown/PDF, atualização mensal ou projeções futuras.

## 1. Vincule cada imagem à mensagem correta

- Prefira sempre o caminho explícito fornecido na mensagem ou no bloco de resposta (`Replied-to image ... saved at:`).
- Não presuma que o arquivo mais recente em `~/.hermes/image_cache/` corresponde ao pedido atual: podem existir imagens diferentes enviadas em sequência.
- Trate cada captura como documento independente até confirmar cartão, competência e conteúdo.
- Se a descrição do usuário e o conteúdo visual divergirem, não misture cartões. Registre a divergência como pendência e peça confirmação ou a imagem correta.

## 2. Faça OCR e leitura visual independentes

1. Preserve a imagem original antes de editar controles.
2. Rode OCR local, de preferência em mais de um modo de segmentação quando a tela tiver cartões, abas e colunas.
3. Faça inspeção visual independente e compare:
   - cartão/emissor e final;
   - competência selecionada;
   - situação aberta/fechada/futura;
   - valor atual e vencimento;
   - fechamento e melhor data;
   - lançamentos, datas, descrições e valores;
   - número da parcela `x/y`.
4. Preserve o OCR bruto mesmo quando estiver errado e anote explicitamente a correção visual. Erros comuns: `7/10` lido como `2/10`, centavos trocados e nomes de estabelecimentos truncados.
5. A versão visual revisada prevalece sobre OCR bruto quando os pixels estão legíveis.

## 3. Não atribua valores por diferença sem prova

- Uma diferença aritmética entre total da fatura e lançamentos visíveis não prova que todo o residual pertence a um parcelamento específico.
- Só atribua o residual a uma compra quando houver linha visível, documento relacionado ou confirmação explícita do usuário.
- Se evidência posterior mostrar valor diferente, preserve a conciliação antiga como histórico, corrija a provisão e classifique o restante como `outros lançamentos não visíveis`.

## 4. Diferencie valor atual de pagamento/crédito anterior

Quando a tela mostrar simultaneamente `valor atual` e `pagamentos/créditos`:

- trate o valor atual exibido como a nova fatura, salvo indicação contrária do próprio app;
- não subtraia de novo pagamento/crédito anterior se o aplicativo já apresenta o total atual líquido;
- documente a relação com a fatura anterior ou pagamento cruzado para evitar falsa duplicação;
- duas obrigações podem coexistir: nova fatura no cartão original e dívida transferida ao cartão usado para pagar a anterior.

## 5. Projete parcelas com calendário explícito

Se a captura comprovar parcela `x/y` de valor fixo:

- mês atual: `x/y`;
- próximo mês: `(x+1)/y`;
- continue até `y/y`;
- após a última parcela, projete R$ 0,00 apenas para essa compra;
- escreva a premissa `sem novas compras, juros, tarifas ou estornos`;
- não invente vencimento se ele não estiver visível; use `A confirmar`.

Exemplo abstrato: parcela 2/4 em agosto implica 3/4 em setembro e 4/4 em outubro.

## 6. Artefatos obrigatórios

Na pasta mensal:

- imagem original;
- OCR bruto `.ocr.txt`;
- Markdown canônico revisado;
- PDF da imagem;
- quando o usuário pedir uma versão PDF do conteúdo extraído, gerar também PDF pesquisável do Markdown para não confundir `PDF da imagem` com `PDF do relatório OCR`.

O Markdown deve conter metadados, lançamentos, conferência das somas, projeções, texto OCR, links relativos e pendências.

## 7. Cascata de atualização

Ao adicionar ou corrigir uma fatura/parcela, revisar todos os artefatos aplicáveis:

1. `AAAA-MM_00_DIVIDA.md`;
2. `AAAA-MM_00_CONTROLE_PAGAMENTOS.md`;
3. meses futuros afetados;
4. `INDEX.md` de cada mês;
5. `_Controle_Anual/AAAA_00_DIVIDA_RESUMO.md`;
6. `_Controle_Anual/AAAA_00_CONTRATADO_FUTURO.md`;
7. inventário de cartões;
8. diagnóstico consolidado;
9. estrutura do ano seguinte quando a parcela atravessar dezembro.

Não altere apenas o total. Adicione ou corrija a linha que explica o total.

## 8. Capturas complementares e fatura “já consolidada”

Quando uma segunda imagem do mesmo cartão detalhar lançamentos que já pertencem a uma fatura registrada:

1. Trate-a como **evidência complementar**, não como nova obrigação.
2. Faça o batimento explícito dos componentes contra o total mostrado pelo aplicativo.
3. Separe compras à vista, parcelas que terminam no mês e parcelas que continuam; uma captura que mostra apenas lançamentos atuais não autoriza inferir a seção de lançamentos futuros.
4. Se a resolução não permitir ler `x/y` com segurança, registre somente as linhas confirmadas e peça recorte ampliado da seção específica. Não projete números ambíguos.
5. Quando o usuário disser que a fatura “já foi consolidada”, procure o valor exato em dívida, controle de pagamentos, índice e resumos:
   - se encontrado, vincule o novo detalhamento sem somar novamente;
   - se não encontrado, não declare que existe consolidação local e não some silenciosamente. Salve o detalhamento, registre uma pendência de reconciliação e peça confirmação sobre onde o total deveria estar.
6. Preserve as capturas separadamente, mas pode gerar um único Markdown canônico e um PDF combinado de evidências quando elas documentarem a mesma fatura.

## 9. Auditoria final

- Recalcule cada total pela soma das linhas de dívida.
- Verifique links locais.
- Procure nomes temporários, caminhos antigos e totais obsoletos.
- Confirme no texto extraído dos PDFs valores, cartão e parcelas.
- Renderize todas as páginas do PDF pesquisável e dos relatórios consolidados.
- Corrija tabelas divididas, subtotal isolado, título órfão, página quase vazia, cortes e sobreposição.
- Se uma tabela não couber, use quebra explícita antes da seção ou divisão manual com cabeçalho repetido.
