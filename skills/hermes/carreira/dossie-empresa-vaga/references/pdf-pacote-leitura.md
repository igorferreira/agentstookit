# Pacote de PDFs de leitura no celular (dossiês de entrevista)

Quando a entrevista se aproxima, Igor LÊ o material no celular (Redmi Note 13). O MD cruza não serve: cada documento vira PDF com capa, sumário navegável e versão de letra grande. Pipeline validado, use o template `templates/build_pdfs_leitura.py` (copie para scratch e adapte `Z`, `OUT`, `TOPOS` por empresa).

## Requisitos do Igor (NÃO negociáveis)

- **Página 1 = CAPA de leitura**: título grande + instruções "como ler" + dicas de memorização + ⭐ pontos-chave. O 1º título do documento começa na **página 2** (aviso "▶ Vire a página" no fim da capa).
- **Outline/bookmarks navegáveis**: hierarquia h1→h2→h3 aparece no painel de marcadores do leitor de PDF.
- **Zero título órfão** (título no fim de página): `page-break-after: avoid` em todo título.
- **Tabelas cabem**: `table-layout: fixed`, `overflow-wrap: anywhere`, `page-break-inside: avoid` em table/tr/blockquote.
- **Versão CELULAR paralela**: segunda rodada com corpo 13,5pt (padrão 10pt), títulos escalados juntos, em pasta `-CELULAR` irmã. **NUNCA apague a versão anterior** — "faz uma nova versão... sem apagar a anterior".
- **Nomes: rótulo DOSSIE em TODOS os arquivos do pacote** + numeração de ordem de leitura `NN_DOSSIE-*.pdf`, com `01_DOSSIE-INDICE-PACOTE` = tabela de leitura (o que é, tempo de leitura, o que memorizar por bloco). Igor confirmou o padrão: "todos os materiais que falam sobre algo devem ter o apelido de DOSSIE".
- **Incluir sempre**: dossiê da EMPRESA (números/risco), dossiês por entrevistador, e **perguntas-e-respostas** (respostas modelo em 1ª pessoa com `[CONFIRMAR]` nos detalhes pessoais) — "falta as perguntas e respostas" veio como correção quando faltou.
- **Réplica no Google Drive**: copiar as pastas PDF prontas para `~/Insync/GoogleDrive/igorferreira08/Documentos/<Empresa>/` (Insync sincroniza; verificar processo insync vivo). Re-copiar inteira a cada atualização.

## Pipeline

1. **Build**: `pandoc -f markdown+emoji -t html` por MD → template HTML com capa (divs `.capa-*`) + caixa topo + corpo + adendo verde + rodapé → `weasyprint` (motor que gera bookmarks de h1/h2/h3 nativamente).
2. **Renderer**: use o binário que TIVER weasyprint na máquina (procurar `/usr/bin/python3*` e `/usr/local/bin/python3*`; o python3 default pode não ter). Fallback sem weasyprint: `pandoc` → `google-chrome --headless --print-to-pdf` (sem outline).
3. **Validar SEMPRE**: (a) outline com pypdf (`PdfReader(f).outline` — conta bookmarks e lista os 2 primeiros; deve começar pelo título REAL do documento); (b) visual com `pdftoppm -png -r 55 -f 1 -l 2` + vision nas páginas 1–2 (capa completa, documento na pág. 2); (c) contagem de arquivos vs MDs de origem.

## Pitfalls

- **Títulos da CAPA nunca em h2/h3** — vira bookmark no outline (o sumário abre em "Como ler...", lixo). Na capa, use divs com classe própria (`.t-topo`) com aparência de título. Só o corpo do documento usa h1/h2/h3.
- **Renomear/deletar PDFs por nome EXATO** — padrões tipo `rm 0[2-9]_*.pdf` casam com numeração ANTIGA e NOVA ao mesmo tempo e apagam o pacote inteiro; recuperar é regenerar do MD (barato, mas evite).
- **Fonte de verdade = MDs em `oportunidades/<Empresa>/`** — a pasta de PDFs no MEGA pode amanhecer vazia (sync do MEGA mexe); nunca presuma que o PDF sobreviveu, regenere do MD.
- **Lua/coração/emoji**: pandoc converte `+emoji`; confira que o renderizador tem fonte (DejaVu + Noto). ASCII art decorativa quebra a leitura no celular.
- Índice numerado (01) muda sempre que entra documento novo — regenerar a tabela COMPLETA (renumerar tudo), não só anexar.

## Ordem de leitura típica (entrevista)

01 índice · 02 cronograma · 03 empresa · 04 perguntas-e-respostas · 05–08 entrevistador 1 (tudo-sobre → master → imprensa → perfil) · 09–15 entrevistador 2 (tudo-sobre → pensamento → artigos → mídia) · 16 pack de estudo. Revisão do dia = índice + respostas + tudo-sobre + ficha de 5 min.
