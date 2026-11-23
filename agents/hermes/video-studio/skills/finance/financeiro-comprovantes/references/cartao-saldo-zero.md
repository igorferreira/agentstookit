# Cartão com saldo zero confirmado

Use este procedimento quando o usuário enviar uma captura de aplicativo mostrando `R$ 0,00` em aberto e informar que não há fatura nem parcelamentos pendentes.

## 1. Separar fontes de evidência

Registre explicitamente o que cada fonte prova:

- **Imagem/OCR:** valor em aberto, vencimento exibido, limite disponível, bloqueio, final do cartão e demais campos visíveis.
- **Declaração do titular:** ausência de parcelamentos, ausência de compras futuras, cancelamento ou qualquer informação que não apareça na tela.

Nunca escreva que a imagem comprova ausência de parcelamentos se ela mostra apenas o saldo atual.

## 2. Classificação no inventário

Use quatro categorias distintas na auditoria mensal:

1. fatura completa/agregada localizada;
2. obrigação parcial/provisionada;
3. **saldo zero confirmado**;
4. nenhuma informação localizada.

Regras:

- “Fatura não localizada” nunca equivale a saldo zero.
- Uma captura explícita de `R$ 0,00`, apoiada pela confirmação do titular sobre parcelamentos, permite mover o cartão da categoria “sem informação” para “saldo zero confirmado”.
- Não aumente a contagem de faturas completas apenas porque há uma tela de saldo zero.
- Garanta que as categorias somem exatamente o número total de contas/produtos inventariados.

## 3. Arquivos a criar

Na pasta mensal, preservar:

- imagem original;
- OCR bruto `.ocr.txt`;
- Markdown canônico;
- PDF da imagem;
- PDF pesquisável derivado do Markdown quando o relatório financeiro precisar de versão PDF auditável.

No Markdown, incluir:

- valor em aberto;
- vencimento exibido;
- limite disponível;
- status operacional;
- origem de cada informação;
- declaração do titular;
- regra de reabertura do controle se surgir compra, tarifa, anuidade, estorno ou parcelamento.

## 4. Cascata de atualização

Atualizar, quando existirem:

- `AAAA-MM_00_DIVIDA.md`: nota de saldo zero, sem inserir obrigação positiva;
- `AAAA-MM_00_CONTROLE_PAGAMENTOS.md`: linha de R$ 0,00 com status `Sem fatura / sem parcelamentos` e comprovante `Não necessário`;
- `INDEX.md` mensal;
- diagnóstico mensal;
- inventário anual;
- resumo anual.

O total financeiro deve permanecer inalterado. Recalcule para comprovar.

## 5. Status operacional não é dívida

- Cartão bloqueado, desbloqueado, cancelado ou inativo é condição operacional.
- Não transforme bloqueio em dívida nem em prova de quitação.
- Registre o status separadamente do saldo.

## 6. Variante: liquidação do emissor pelo Banco Central

Quando o usuário informar que o cartão/banco foi liquidado pelo Banco Central (ex.: Will Bank, Banco Master):

### 6.1 Confirmação independente

1. Pesquisar no site oficial do BCB (`bcb.gov.br`) ou em fontes jornalísticas primárias (G1, InfoMoney, Valor) pelo nome da instituição + "liquidação" + "Banco Central".
2. Verificar a data da liquidação e se foi extrajudicial (decretada pelo BC) ou falência (judicial).
3. Confirmar quais produtos/operações foram atingidos: cartão, conta corrente, poupança, Pix, etc.
4. Salvar a URL da fonte oficial como evidência no Markdown do cartão.

### 6.2 Classificação

- Liquidação extrajudicial pelo BC = status mais forte que qualquer captura de aplicativo.
- O cartão não pode ter saldo futuro, fatura, compras ou parcelamentos — a instituição não opera mais.
- Classificar como **"saldo zero confirmado — banco liquidado"** no inventário.
- Como não há captura de app (o app não funciona mais), a evidência é a nota oficial do BCB.
- Registrar no Markdown e no controle: "Cancelado por liquidação extrajudicial do emissor em DD/MM/AAAA".

### 6.3 Atenção ao grupo econômico

- Bancos do mesmo grupo (ex.: Banco Master → Will Financeira) podem ter sido liquidados em datas diferentes.
- Verificar cada emissor individualmente — a liquidação de um não garante a do outro.
- Exemplo real: Banco Master liquidado em nov/2025, Will Financeira (Will Bank) liquidada em 21/01/2026, ambas do mesmo grupo, mas com atos distintos.

## 7. Cartão sem uso futuro (voluntário)

Quando o usuário declarar que um cartão está **zerado e não será mais usado** (mas não está bloqueado nem cancelado):

- Tratar como categoria distinta de: (a) bloqueio operacional, (b) liquidação do emissor, (c) saldo zero temporário.
- Registrar a declaração: `"sem uso futuro"` + data + fonte (usuário).
- O cartão pode ser **reativado a qualquer momento** — não equivale a cancelamento.
- Se o usuário posteriormente informar novo uso, remover a nota de "sem uso futuro" e registrar a nova fatura.

## 8. Auditoria final

## 9. Confirmação verbal sem captura de tela

Quando o usuário informar que um cartão está zerado/cancelado **sem enviar imagem** (ex.: "O cartão X foi cancelado tá zerado"):

1. **Registrar a origem como declaração do titular** — não como evidência documental. O status é `🟢` mas a observação deve deixar claro que não há captura de tela.
2. **Não criar OCR/arquivo de imagem** — sem imagem, não há OCR. Criar apenas o Markdown com os dados informados e marcar origem como `"Confirmado por Usuário em DD/MM/AAAA (verbal, sem captura)"`.
3. **Atualizar a cascata normalmente**: dossiê, controle mensal, diagnóstico, inventário.
4. **Total financeiro não se altera** (zerado não contribui).
5. **Se o usuário posteriormente enviar captura**, substituir a evidência verbal pela documental e atualizar a origem.

Exemplos reais desta sessão:
- Itaú Latam Pass final 7909 — "O cartão latampass foi cancelado tá zerado" (28/07/2026)
- Itaú Cheque Especial — "já quitei o cheque especial do Itaú tambem" (28/07/2026)
