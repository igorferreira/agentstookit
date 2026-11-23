# Matriz de Parcelamentos Futuros — Cartão a Cartão

## Quando usar

Quando o usuário estiver montando cenários de pagamento e precisar saber as
obrigações futuras (parcelamentos, compras parceladas, portabilidades) de cada
cartão que está sendo pago no mês corrente. Essas obrigações são **invisíveis**
na fatura atual mas vão aparecer nas faturas dos meses seguintes e podem
inviabilizar o orçamento projetado.

## Procedimento

### 1. Identificar cartões sem parcelamento mapeado

A partir da lista de cartões que serão PAGOS no cenário (não os que vão pra
negociação), listar explicitamente quais têm e quais NÃO têm parcelamentos
futuros documentados.

### 2. Solicitar prints ao usuário

Para cada cartão sem mapeamento, pedir um print por vez. O usuário deve dizer
qual cartão está enviando.

### 3. Extrair via OCR

Usar tesseract com pré-processamento (contraste 2.0, nitidez 2.0, threshold
140) e PSM 6:

```python
from PIL import Image, ImageEnhance
import pytesseract

img = Image.open(path)
for e in [ImageEnhance.Contrast, ImageEnhance.Sharpness]:
    img = e(img).enhance(2.0)
img = img.convert('L').point(lambda x: 0 if x < 140 else 255)
text = pytesseract.image_to_string(img, config='--oem 3 --psm 6 -l por')
```

### 4. Montar série mensal

Para cada cartão, extrair a projeção mês a mês (ex.: ago/26 a ago/27).
Gráficos de barras de apps bancários mostram o total projetado por fatura.

### 5. Consolidar na matriz cruzada

Criar tabela com meses nas linhas e cartões nas colunas:

| Mês | Cartão A | Cartão B | ... | **Total parcelas** |
|---|---|---|---|---|
| Set/26 | 5.161 | 1.276 | ... | **6.437** |
| Out/26 | 4.862 | 1.272 | ... | **6.134** |

### 6. Cruzar com a projeção de folga

Adicionar coluna da folga mensal projetada e calcular o saldo real:

| Mês | Total parcelas | Folga P | **Saldo real** |
|---|---|---|---|
| Set/26 | 6.437 | 3.849 | **−2.588** 🔴 |

## Pitfalls

### O valor da fatura atual NÃO é o valor dos parcelamentos futuros
A fatura que está sendo paga agora (ex.: Inter R$ 8.317) é uma coisa.
Os parcelamentos futuros são as faturas que virão DEPOIS (ex.: R$ 1.276,
R$ 1.272...). Não confundir — a fatura atual já está provisionada no
cenário; os parcelamentos futuros são descobertos agora e precisam entrar
na projeção.

### Gráficos de barra mostram o total da fatura projetada, não cada parcela
O app do Inter, por exemplo, mostra um gráfico de barras com o valor
TOTAL de cada fatura futura (já somando todos os parcelamentos ativos
naquele mês). Não tente separar — o total já é o que importa.

### OCR pode falhar em fontes estilizadas de apps brasileiros
Números como R$ 1.272,24 podem sair como "R$ 1272,24" (sem vírgula)
ou "R$ 1.27257". Cruzar com a seção de detalhe da fatura (que o app
mostra para um mês específico) para confirmar.

### Vários prints do mesmo cartão são normais
O app pode mostrar o gráfico em partes (ex.: 6 meses por tela).
Solicitar prints adicionais até cobrir todo o horizonte visível.

### O usuário pode fornecer valores manualmente
Se o OCR estiver falhando consistentemente (ex.: dark mode, fontes
estilizadas), o usuário pode ler os valores diretamente da tela e
digitá-los. Isso é mais rápido que 5+ tentativas de OCR frustradas.
Exemplo real (31/07/2026): Nubank e Amazon — usuário digitou valores
mês a mês porque o OCR do gráfico de barras estava ilegível.

### Parcelamentos que acabam no meio do horizonte
Alguns cartões têm parcelamentos que expiram durante o período
projetado (ex.: Nubank cai de R$ 5.161 para R$ 0 em ago/27).
Isso é normal — a projeção do app já reflete o término.
