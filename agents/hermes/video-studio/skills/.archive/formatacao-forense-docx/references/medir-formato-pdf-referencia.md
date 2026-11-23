# Medindo a formatação REAL de um PDF de referência

Quando o cliente fornece um PDF de referência ("siga este estilo"), NÃO assuma
valores ABNT teóricos (3/2 cm etc.) — **meça o PDF real**. O padrão do Google Docs
/ do advogado pode ser bem diferente e é isso que o cliente quer reproduzir.

## 1. Margens reais (pts → cm)

`pdftotext -bbox` reporta coordenadas em **pontos (pts)** (A4 = 596 × 842 pts):

```bash
pdftotext -bbox -f 1 -l 1 ref.pdf /tmp/ref.html
```

Parseie `<word xMin= yMin= xMax= yMax=>`:
- **margem esquerda** = menor `xMin` (ignorar `<>` de número de página: texto só dígitos)
- **margem superior** = menor `yMin`
- **margem direita** = 596 − maior `xMax`
- **margem inferior** = 842 − maior `yMax`
- conversão: **1 pt = 0,035278 cm**

Exemplo medido (V6 do Dr. Diogo): esq 72pts=2,54cm; sup 82,4pts=2,91cm; dir 72,7pts≈2,57cm; inf 78,7pts≈2,78cm. **Recuo de parágrafo** = x0 do corpo (100,5pts≈3,55cm) − margem (72pts) ≈ 1cm.

## 2. Negritos (quais blocos estão em bold)

`pdftohtml -xml` marca `<b>` em `<text font="N">`:

```bash
pdftohtml -xml -f 1 -l 1 ref.pdf /tmp/ref.xml
```

Em Python, para cada `<text ...>(.*?)</text>`: se contém `<b>` → NEGRITO;
extraia o texto com `re.sub(r'<[^>]+>','')`. O `<fontspec ...>Bold</fontspec>`
confirma a variante (ex. `Arial-BoldMT`).

## 3. Fonte / variantes

`pdffonts -f 1 -l 1 ref.pdf` → lista fontes (ex. `ArialMT` + `Arial-BoldMT`).

## 4. Espaçamento vertical (primeira página)

Diferença de `top` entre blocos indica linhas vazias. V6: blocos em
`top=124, 339, 431, 585, 739, 831` → ~46u entre blocos = **4 parágrafos vazios**.

## Consequência prática

Ajuste o DOCX com as margens medidas (não 3/2 cm): sup≈2,9 / esq 2,54 / dir 2,57 /
inf 2,78 cm. Aplicar com `python-docx`: `section.left_margin=Cm(2.54)` etc.

## Armadilhas

- `pdftotext -layout` (texto puro) NÃO revela negrito nem margens — use `-bbox` e
  `pdftohtml -xml` para dados de geometria/formatação.
- Ignorar palavras que são só dígitos — números de página falseiam as margens
  (aparecem na borda).
- Depois de aplicar no DOCX, **re-medir o PDF gerado** e comparar as 4 margens com
  o de referência para confirmar fidelidade antes de replicar às réplicas.