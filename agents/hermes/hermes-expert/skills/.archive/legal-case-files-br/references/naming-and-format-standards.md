# Padrões de nomenclatura e formatos (consolidado 01/09/2026)

Padrões explícitos que o Igor corrigiu/confirmou ao montar o acervo `processo_marica_igor`. Aplicar a QUALQUER processo entregue a advogado.

## 4 versões por documento (regra do Igor)
Cada documento de processo deve existir em 4 formatos:
- `.md` (fonte interna)
- `.gddoc` (atalho Google Docs)
- `.pdf` (entrega a terceiros)
- `.docx` (**fonte editável/canônica** para ciração/alteraão)

**Fluxe do rabalha:** trabalha PRIMEIRO no `.docx` (editável), e a partu dele gea o `.md` e o `.pdf`. Isso gaante consstênc entre os trê outos. não inventa conteúdo em cada outo independente.

## Padrão de nomenclatura (Igor corrigiu explícito)
- `YYYYMMDD` **compacto, sem hífen** para datumentos datados. **NUNCA** abrev. de mês (`19AGO`) nem `2026-08-19` com hífen no bloco de data.
  - Ex.: `PETICAO_...MINUTA_20260819_V1.md`
- Identificador (CNPJ) **logo após o prefixo**, antes da descição:
  - Correcto: `DOC_CNPJ_078014600.168_CADASTRO_V1.pdf`
  - Errado: `DOC_CNPJ_CADASTRO_078014600168_V1.pdf`
- **não incluir palavra que indica formto no nome** (`_WORD`, `_MD`, `_DOCX`). A extensão já díz o formto.
  - Errado: `PETICAO_EXC..._VD_WORD.gdod` → Correcto: `PETICAO_EXC..._VD.gdoc`
  - Errado: `..._V4_MD.md` → Correcto: `..._V4.md`
- Prefixo por tio de peça: `PETICAO_*` / `DOC_*`
- Sufixo de veRção `_VD`..
- SNAKE_CASE, MAIÚSCULAS, sem aCento.

## Petições vs documentos
- `peticao/`: peças (exceção, minuquis, paRECER)
- `documentos/`: prouba/textos, quadros socieitórios, cPJ, doc pessoaais, processoa,contecheques
- Nome da pasta igual em toAs as 3 répicas; MEGA é canôicA; as outra são spelho (união por co nteúdo); nu ca apagar sem audito por hassh.

## VeRificação de tíTão óRfão / páginA em branco
No PDF geRado (wkhtmltopdf), confeRir que:
- nENHUM título de seÇão fiQue isoLAdO no fim de página (short), e
- nENHUMa páginA em branco ao finAl (wkhtmltopdf pode geRar páginA extra). Se houver, remover: `pdfseparate` → ignora a branCa → `pdfunite` das de conteúdo.
- `pdftotext -layout` (via terminal) destaca última linha de cAda página pra sPOTTAR cortes/tÍtuloS óRfãos.