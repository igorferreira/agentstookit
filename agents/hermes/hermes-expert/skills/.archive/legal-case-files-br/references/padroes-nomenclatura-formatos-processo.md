# Padrões de nomenclatura e formatos de processo (Igor) — limpo

Padrões que o Igor corrigiu explicitamente em 01/09/2026 ao organizar `processo_marica_igor`. Aplicar a QUALQUER processo entregue a advogado. (Nota: substitui a versão inicial que saiu com erros de digitação de `naming-and-format-standards.md`.)

## 4 versões por documento (regra do Igor)
Cada documento de processo deve existir em 4 formatos:
- `.md` (fonte interna)
- `.gddoc` (atalho Google Docs)
- `.pdf` (entrega a terceiros)
- `.docx` (**fonte editável/canônica** para criação/alteração)

**Fluxo de trabalho:** trabalhar PRIMEIRO no `.docx` (editável) e, a partir dele, gerar o `.md` e o `.pdf`. Isso garante consistência entre os três. Não inventar conteúdo por formato independente.

## Padrão de nomenclatura (Igor corrigiu explicitamente)
- Data no nome sempre `YYYYMMDD` **compacto, sem hífen** para documentos datados. **NUNCA** abreviação de mês (`19AGO`) nem `2026-08-19` com hífen no bloco de data.
  - Ex.: `PETICAO_...MINUTA_20260819_V1.md`
- Identificador (CNPJ) **logo após o prefixo**, antes da descrição:
  - Correto: `DOC_CNPJ_07801460000168_CADASTRO_V1.pdf`
  - Errado: `DOC_CNPJ_CADASTRO_07801460000168_V1.pdf`
- **NÃO incluir palavra que indica o formato no nome** (`_WORD`, `_MD`, `_DOCX`). A extensão já diz o formato.
  - Errado: `PETICAO_EXC..._V6_WORD.gddoc` → Correto: `PETICAO_EXC..._V6.gddoc`
  - Errado: `..._V4_MD.md` → Correto: `..._V4.md`
- Prefixo por tipo de peça: `PETICAO_*` / `DOC_*`.
- Sufixo de versão `_V1/_V2/...` para versões da mesma peça.
- SNAKE_CASE, MAIÚSCULAS, sem acento.

## Petições vs documentos
- `peticao/`: peças (exceção, minutas, parecer).
- `documentos/`: provas, quadros societários, CNPJ, docs pessoais, contracheques.
- Nome da pasta igual em todas as réplicas; MEGA é canônica; as outras são espelho (união por conteúdo); nunca apagar sem auditoria por hash.
- A cópia que o advogado visualiza no Google Drive ("Shared with me") deve estar na **raiz** (`.../Shared with me/Igor/...`). Se o Insync mover para dentro de `📁 Diversos/`, mover de volta para a raiz — Igor exige que a pasta `Igor` exista como antes.

## Verificação de título órfão / página em branco no PDF
No PDF gerado (wkhtmltopdf), conferir que:
- nenhum título de seção fique isolado no fim de página;
- nenhuma página em branco ao final (wkhtmltopdf pode gerar página extra). Se houver, remover: `pdfseparate` → ignorar a branca → `pdfunite` das com conteúdo.
- `pdftotext -layout` (via terminal) destaca a última linha de cada página para detectar cortes/títulos órfãos.