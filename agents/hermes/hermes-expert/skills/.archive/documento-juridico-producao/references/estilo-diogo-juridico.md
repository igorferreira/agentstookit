# ESTILO-DIOGO-JURIDICO — Formatação canônica de peças (Dr. Diogo / Google Docs)

Fonte da verdade: versão 6 canônica (`6 EXCEÇÃO DE PRÉ-EXECUTIVIDADE IGOR DOS SANTOS FERREIRA.pdf`, renderizada por Google Docs — Skia/PDF). Guia no caso: `ESTILO-DIOGO-JURIDICO.MD` (replicado nas 3 pastas do processo_marica_igor).

TODA peça/petição do processo deve seguir este estilo. Igor: *"todas as versões devem seguir o mesmo formato dessa versão 6"*.

## Configuração
- Página **A4** (596×842 pts), retrato.
- Margens: sup 3 cm · esq 3 cm · dir 2 cm · inf 2 cm.
- Fonte **Arial** (ArialMT normal + Arial-BoldMT). Google Docs → **Arial**, não Times.
- **Preto puro `#000000`, fundo branco, SEM CORES** (sem highlight/shading).
- Espaçamento entre linhas **1,5**.

## Estrutura obrigatória (ordem)
1. Endereçamento — CAIXA ALTA, sem recuo.
2. `Processo nº ...` — uma linha, sem recuo.
3. Qualificação/preâmbulo — parágrafo contínuo.
4. Título da peça — CAIXA ALTA, destaque.
5. `pelos fundamentos a seguir expostos.`
6. Seções `I.` a `XI.` — romanos, caixa alta, negrito.
7. Pedidos numerados `1.` a `12.` — recuados.
8. Fechamento — `Termos em que,` / `Pede deferimento.` / local-data / assinaturas.

## Parágrafos
- Recuo de 1ª linha **1,25 cm**.
- Espaçamento 1,5 · corpo justificado.
- Blocos de dados: **um campo por linha** (ex.: `Titular: ...;` `CPF: ...;` `Processo: ...;` `Data do bloqueio: ...;` `Valor bloqueado: ...;`).
- Listas numeradas recuadas; itens fecham com `;`, último com `.`.
- Rodapé: **número de página centralizado**.

## Títulos de seção (V6)
`I. O QUE EXIGE APRECIAÇÃO IMEDIATA` · `II. DO CABIMENTO ... TEMA 108 STJ` · `III. IGOR DEIXOU A SOCIEDADE... DEZ ANOS ANTES` · `IV. A QUESTÃO TEMPORAL ...` · `V. A PROVA DA RETIRADA É PÚBLICA...` · `VI. A INFORMAÇÃO SOCIETÁRIA NÃO ESTAVA OCULTA` · `VII. DA URGÊNCIA CONCRETA: A ORDEM SISBAJUD ESTÁ ATIVA...` · `VIII. DO LEVANTAMENTO DAS CONSTRIÇÕES JÁ EFETIVADAS` · `IX. DA ILEGITIMIDADE DE IGOR ...` · `X. DOS HONORÁRIOS ADVOCATÍCIOS SUCUMBENCIAIS` · `XI. DOS PEDIDOS`.

## Como forçar preto no DOCX (python-docx)
```python
from docx import Document
from docx.shared import RGBColor
from docx.oxml.ns import qn
doc = Document(path)
for p in doc.paragraphs:
    for r in p.runs:
        r.font.color.rgb = RGBColor(0x00,0x00,0x00)
        rpr = r._element.get_or_add_rPr()
        for el in rpr.findall(qn('w:highlight')): rpr.remove(el)
# idem em doc.tables; doc.save(path)
```
Verificar: `unzip -p file.docx word/document.xml | grep -oE 'w:color w:val="[0-9A-F]{6}"' | sort | uniq -c` → só `000000`.

## Checklist antes de salvar
- [ ] A4 retrato, margens 3/3/2/2
- [ ] Fonte Arial 11–12
- [ ] **Sem cor** (`w:color` só 000000; sem `w:highlight`/`w:shd`)
- [ ] Espaço 1,5
- [ ] Títulos romanos I–XI caixa alta negrito
- [ ] Recuo 1ª linha 1,25 cm
- [ ] Blocos campo-por-linha; pedidos numerados
- [ ] Rodapé página centralizada