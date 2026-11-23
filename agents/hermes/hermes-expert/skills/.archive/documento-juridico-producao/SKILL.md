---
name: documento-juridico-producao
description: "Use ao criar/editar peças processuais forenses (DOCX, ABNT)."
version: 1.0.0
---

# Produção de Documentos Jurídicos (petições, pareceres, minutas)

Workflow canônico para criar/editar peças processuais do Igor (petições, pareceres, dossiês), no padrão forense brasileiro.

## WORKFLOW ESCRITO EM PEDRA (Igor corrigiu explicitamente)

**O DOCX é o artefato canônico/editável.** Fluxo correto:

1. Montar o conteúdo no **DOCX** (editável em Word).
2. **Derivar** o **MD e o PDF a partir do DOCX** (`pandoc file.docx -f docx -t gfm -o file.md`; PDF via LibreOffice `soffice --headless --convert-to pdf` para fidelidade).
3. **NUNCA** o caminho inverso (docx → md → docx). Igor: *"Não é melhor vc trabalhar no docx e depois gerar o markdown e o PDF?"*

## 4 FORMATOS OBRIGATÓRIOS

Todo documento do caso (petições + documentos) deve existir em: **`.md`**, **`.gddoc`**, **`.pdf`**, **`.docx`**.
- `.gddoc` é um **atalho** (JSON ~212 b) apontando p/ um Google Docs real. **Não criar `.gddoc` fake** (quebra no advogado). Requer OAuth Google não configurado no Hermes (`NOT_AUTHENTICATED`) → o Google Docs tem que ser criado manualmente pelo Igor/advogado (importando o `.docx` na pasta compartilhada), e o Insync gera o atalho.
- `.gddoc`/`.pdf` da versão canônica devem preservar conteúdo idêntico entre as 3 réplicas (hash igual).

## NOMENCLATURA (Igor corrigiu reiteradamente)

- **Datas nos nomes = `YYYYMMDD`** (ex.: `...20260819_V1.md`). NUNCA `19AGO` nem hífen.
- **CNPJ logo após o prefixo:** `DOC_CNPJ_07801460000168_CADASTRO_V1.pdf` (não `DOC_CNPJ_CADASTRO_07801460000168`).
- **NÃO** usar sufixo de formato no nome (`_WORD`, `_MD`, `_DOCX`) — a extensão revela o formato. `PETICAO_..._V6.gddoc`, não `_V6_WORD.gddoc`.
- Prefixos: petições = `PETICAO_*`, documentos = `DOC_*`; versões = `_V<n>`.

## PADRÃO FORENSE ABNT (via python-docx)

Use a skill `docx` + `python-docx` (instalar num venv `uv venv` + `uv pip install python-docx` se ausente):

- **Página A4** (21 x 29,7 cm), retrato. Especifique `page_width/page_height` (python-docx default é Letter!).
- **Margens:** superior 3 cm, esquerda 3 cm, direita 2 cm, inferior 2 cm.
- **Espaçamento entre linhas 1,5** (ONE_POINT_FIVE) em todos.
- **Fonte Times New Roman 12** (aplicar em `Normal` + cada run, incl. `w:rFonts` para tabelas/listas).
- Alinhamento: corpo **justificado**, títulos de seção **centralizados + negrito**.
- `space_after` ≈ 6pt, `space_before` 0.

## VALIDAÇÃO DE DIAGRAMAÇÃO (Igor exige)

Antes de entregar o PDF, validar:
1. **Sem título órfão** = título de seção (ex. `X. DOS HONORÁRIOS`) no FIM da página com corpo na página seguinte. Corrigir com CSS `page-break-after:avoid` + envolver `<h2>` e o parágrafo seguinte num `<div style="page-break-inside:avoid">` (pós-processar o HTML do pandoc/wkhtmltopdf; a regex deve casar `</h2>` seguido de `<p|ul|ol>` — NÃO inserir o `<div>` DENTRO do `<h1>/</h2>`).
2. **Sem página em branco** no fim (resíduo do wkhtmltopdf/LibreOffice). Remover com `pdfseparate` + `pdfunite`.
3. Verificar por script: cada página termina em texto normal (não cabeçalho romano solto), nenhuma página vazia.

## REPLICAÇÃO (3 pastas) + verificação

Após produzir, copiar .md/.pdf/.docx para:
- MEGA canônica: `~/MEGA/Documentos/legal_publico/processos/<pasta>/...`
- Shared (visível ao advogado): `.../Google Drive - Shared with me/igor/processo_marica_igor/...` (NOTA: Insync pode usar **`igor` minúscula**; re-localizar com `find`, não assumir o caminho).
- GDrive backup: `.../01_Pessoal/documentos_legais/processos_judiciais/processo_marica_igor/...`

Conferir que as 3 réplicas estão **idênticas por hash** (`md5sum`). A canônica MEGA é a fonte da verdade; as pastas `documentos/` e `peticao/` devem ter os mesmos arquivos (união por conteúdo/hash).

## HONESTIDADE JURÍDICA (não forçar tese)

Antes de alegar prescrição/decadência, distinguir com precisão e validar contra dados reais:
- **Prescrição da cobrança/execução do crédito (art. 174 CTN):** prazo de **5 anos da constituição definitiva** (data da **inscrição na CDA**). Comparar ajuizamento com data da CDA.
- **Prescrição intercorrente (art. 40 LEF):** após **1 ano de suspensão** (por falta de bens) fluem **5 anos**. Ver Temas 566–571/STJ e Tema 390/STF (suspensão 12/02/2025 → prescrição só ~2031). **Constrição SISBAJUD/JUD efetiva interrompe** a intercorrente (Temas 568/569-STJ).
- **Decadência da responsabilidade do sócio retirante (arts. 1.003, § único, e 1.032 CC):** **bienal** após a averbação (ex.: averbada 21/09/2007 → encerrada 21/09/2009).

Regra: **NUNCA alegar prescrição consumada sem verificar as datas reais de inscrição na CDA** (extrair do PDF do processo, coluna "DATA INSCR."). Se a execução foi ajuizada dentro dos 5 anos da inscrição, a prescrição do art. 174 não se consumou — forçar a tese fragilizaria a defesa. Quando houver ambiguidade (qual tese empregar), perguntar ao Igor com opções em vez de assumir.

## Support files
- `references/prescricao-e-decadencia-ctn-lef.md` — análise concreta do caso Maricá (datas CDA, cálculo art. 174) + distinção das teses prescricionais.