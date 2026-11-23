# Técnicas de OCR para screenshots de apps bancários brasileiros

## Problema comum

Apps de cartão de crédito brasileiros (Bradescard, Nubank, Itaú, Banco PAN, Inter, PicPay) usam fontes estilizadas para o **valor total da fatura** — números grandes, bold, às vezes com gradiente ou sombra. O Tesseract padrão (PSM 3) frequentemente falha nesses valores, mesmo quando extrai corretamente o resto da tela.

## Solução: varredura de PSM modes

O Tesseract tem modos de segmentação de página (PSM) que mudam radicalmente o comportamento do OCR. Para screenshots de apps:

```bash
# Varredura rápida — testa os modos mais úteis
for psm in 6 11 12 3 4; do
    tesseract imagem.jpg stdout -l por --psm $psm 2>/dev/null
    echo "--- PSM $psm ---"
done
```

### Modos com melhor resultado

| PSM | Descrição | Eficácia para apps |
|-----|-----------|-------------------|
| 3 | Default — automático | Útil como baseline; às vezes limpo para telas simples |
| 4 | Coluna única de texto | Pode superar 11/12 para telas com layout limpo (ex.: C&A Pay) |
| 6 | Bloco uniforme de texto | Bom para telas densas (Inter, PicPay) |
| 11 | Texto esparso | **Excelente** para Bradescard (Casas Bahia, Amazon) — captura valor total estilizado |
| 12 | Texto esparso com OSD | **Excelente** — similar ao 11, às vezes melhor |

### Ordem recomendada de tentativa

1. **PSM 11, 12** — melhores para fontes estilizadas de apps bancários (Bradescard, Nubank, Itaú)
2. **PSM 6** — fallback para telas mais densas (Inter, PicPay com muitos lançamentos)
3. **PSM 3, 4** — fallback final; PSM 4 é subestimado e funciona bem para telas com layout limpo

### OCR em lote de múltiplas imagens

Quando o usuário envia várias imagens da mesma fatura (screenshots em sequência), processar todas em lote:

```bash
for f in img_*.jpg; do
  echo "=== $(basename $f) ==="
  tesseract "$f" - -l por --psm 6 2>/dev/null
  echo "---"
done
```

A última imagem frequentemente contém o resumo (valor total, vencimento, fechamento) — priorizá-la para extrair dados consolidados. Imagens intermediárias contêm lançamentos e parcelamentos.

### Quando o OCR ainda falha: pré-processamento da imagem

Se nenhum PSM capturar o valor total, redimensionar e aplicar sharpen antes de repetir a varredura:

```bash
# Upscale 2x + sharpen, depois varredura
convert imagem.jpg -resize 200% -sharpen 0x1 /tmp/preprocessed.png
for psm in 11 12 6 4; do
    tesseract /tmp/preprocessed.png stdout -l por --psm $psm 2>/dev/null
    echo "--- PSM $psm (preprocessed) ---"
done
```

Isso frequentemente resolve fontes estilizadas que o Tesseract não lê na imagem original.

### Quando o OCR falha completamente

**Caso:** Casas Bahia VISA final 6015 (app Bradescard)

- PSM 3 (default): valor total ilegível — só "Valor total" sem o número
- PSM 6: ilegível — "14]" ou similar
- PSM 11: ✅ **"R$ 8.627,58"**
- PSM 12: ✅ **"R$ 8.627,58"** (confirmado)
- PSM 13: falhou completamente

**Caso:** Amazon Mastercard final 3018 (app Bradescard)

- PSM 6: capturou a maior parte dos metadados mas o valor total saiu truncado (\"14]\" etc.)
- PSM 11: ✅ **\"R$ 1.145,01\"**
- PSM 12: ✅ **\"R$ 1.145,01\"** (confirmado)
- Valores menores (~R$ 1.000) podem ter melhor resultado que valores grandes (~R$ 8.000) devido ao espaçamento da fonte

## Quando o OCR falha completamente

Se nenhum modo PSM capturar o valor total:

1. Extrair o que for possível: status da fatura, vencimento, pagamento mínimo, limite disponível
2. **Estimar pelo pagamento mínimo**: apps brasileiros mostram mínimo ~15% do total → `total ≈ mínimo ÷ 0.15`
3. Pedir confirmação ao usuário com a estimativa
4. NUNCA registrar valor estimado como confirmado sem validação do usuário

## Dica extra: idioma

Sempre usar `-l por` (português). O dicionário português ajuda o Tesseract a reconhecer "fatura", "fechada", "vencimento", "pagamento mínimo", etc. Sem isso, caracteres acentuados e palavras compostas são frequentemente quebrados.

## Prefixo do valor: "RS" vs "R$"

O Tesseract frequentemente confunde `R$` com `RS` (sem cifrão). Corrigir manualmente ao digitar o valor extraído — o cifrão é um caractere especial que o OCR erra com frequência.

## ⚠️ Photo de comprovante impresso (não screenshot de app)

Quando o documento é uma **foto de um comprovante/papel impresso** (comprovante de pagamento, boleto impresso, recibo) — não um screenshot de app com fonte estilizada — o PSM 3 default costuma bastar, MAS a foto precisa de pré-processamento para fotografias (luz, inclinação, ruído):

```bash
convert foto.jpg -colorspace Gray -resize 200% -contrast-stretch 2%x2% /tmp/ocr.png
tesseract /tmp/ocr.png stdout -l por --psm 3 2>/dev/null
```

**Pipeline recomendada para fotos de comprovante:**
1. `-colorspace Gray` — converte pra escala de cinza (remove interferência de cor do papel/luz amarela)
2. `-resize 200%` — dobra a resolução (texto impresso pequeno ganha muito)
3. `-contrast-stretch 2%x2%` — normaliza o contraste (clareia o que está na sombra, escurece o que está claro demais)
4. Rodar `tesseract -l por --psm 3` (foto de papel = layout de bloco uniforme; não precisa da varredura PSM 11/12 feita para telas estilizadas)

Se o valor monetário ainda sair truncado, aplicar a varredura PSM 11/12 sobre o PNG pré-processado como fallback.

**Caso real (14/08/2026):** foto do comprovante 99Pay da conta Vivo. A pipeline acima extraiu corretamente "Transação concluída / R$102,23 / 14/08/26 01:01:33 / TELEFONICA BRASIL S.A. / IDs". O OCR de um comprovante de pagamento é a fonte da evidência para: valor, timestamp, remetente, beneficiário e IDs de transação.

**Dica de reconciliação (valiosa):** um **pagamento bem-sucedido partindo de uma conta confirma que o crédito "previsto" daquela conta realmente entrou.** Exemplo: 99Pay com saldo confirmado de R$ 10,40 e um crédito Digio "🟡 previsto" de R$ 900 — quando Igor paga uma conta de R$ 102,23 a partir do 99Pay e a transação é concluída, isso COMPROVA que o crédito de R$ 900 entrou (o saldo confirmado R$ 10,40 sozinho não cobriria R$ 102,23). Atualizar o saldo e marcar o crédito como confirmado; não mantê-lo como "previsto" indefinidamente quando um pagamento real o valida.

## ⚠️ Dark mode — Tesseract falha consistentemente

Screenshots de apps em **modo escuro** (fundo preto, texto branco) são um caso conhecido de falha do Tesseract. O pré-processamento padrão (contrast 2×, sharpen 2×, threshold 140) funciona para apps claros, mas em dark mode produz ruído ou texto ilegível.

**Estratégias (em ordem):**

1. **Tentar inverter a imagem** (`ImageOps.invert`) antes do threshold — transforma fundo escuro em claro, às vezes suficiente para o Tesseract ler.
2. **Tentar múltiplos thresholds** (80, 100, 120, 160) no modo L — o ideal varia conforme o contraste da fonte.
3. **Tentar PSM modes alternativos**: PSM 6 (bloco uniforme), PSM 4 (coluna única), PSM 11 (texto esparso) — cada modo interpreta o layout de forma diferente.
4. **Se nada funcionar (3+ tentativas), pedir ao usuário para ler os valores** — ele está vendo a tela. É mais rápido que 5 tentativas de OCR frustradas. O usuário pode digitar mês a mês como fez com Nubank e Amazon em 31/07/2026.

**Sinal de falha:** output do Tesseract é caracteres ASCII aleatórios, símbolos, ou texto estruturado como `"E E Ê s 5 555"`.

**Exemplo real (31/07/2026):** App Banco Inter em dark mode, gráfico de barras de faturas futuras. Tesseract com todos os thresholds produziu ruído. Usuário leu os valores manualmente.

## ⚠️ Nubank: três valores na mesma tela — não confundir

O app do Nubank (tela do cartão de crédito) mostra **três valores distintos** próximos uns dos outros:

| Campo | Significado | Exemplo real |
|---|---|---|
| **Fatura atual** | Valor da fatura ABERTA deste mês | R$ 5.660,52 |
| **Próxima fatura** | Estimativa da fatura do MÊS SEGUINTE | R$ 5.160,86 |
| **Total das próximas faturas** | Soma de TODOS os parcelamentos futuros (meses à frente) | R$ 28.548,29 |

**PITFALL: o OCR pode capturar "R$ 28.548,29" e parecer que é a fatura atual, mas é o total parcelado futuro** — a diferença é de ~5×. Isso já causou erro de modelagem em 31/07/2026 (fatura de R$ 5.661 foi confundida com dívida de R$ 28.548).

**Regra:** ao extrair valores do app Nubank, identificar CADA um dos três campos separadamente. O layout típico é:
- Fatura atual no topo, número maior/destacado
- "Próximas faturas" mais abaixo, com total consolidado
- Confirmar com o usuário se houver ambiguidade no OCR
