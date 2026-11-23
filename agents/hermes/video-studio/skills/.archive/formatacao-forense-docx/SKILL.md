---
name: formatacao-forense-docx
description: "Gerar/reformatar peças DOCX no padrão forense ABNT."
version: 1.0.0
---

# Formatação Forense DOCX (padrão ABNT / arquivos jurídicos)

Workflow para **produzir ou reformatar peças processuais** (petições em especial) no padrão forense brasileiro, com o DOCX como fonte da verdade editável. Aplicável a qualquer caso, não só a um processo específico. Carregar `docx`, `legal-drafting-br` e a skill de estilo do cliente quando houver.

## Quando usar

- Usuário pede gerar/corrigir uma petição ou documento forense que deve seguir padrão ABNT.
- Precisa gerar PDF fiel + MD consistentes a partir de um único DOCX canônico.
- Precisa padronizar/renomear lotes de documentos jurídicos.

## Configuração ABNT da página

| Item | Valor |
|---|---|
| Página | **A4** (21 × 29,7 cm), retrato |
| Margens | sup **3**cm, esq **3**cm, dir **2**cm, inf **2**cm |
| Fonte | **Arial** 11–12pt (não Times) |
| Cor | **Preto `000000` no branco — SEM cores/highlight/shading** |
| Espaçamento | 1,5 |
| Alinhamento | corpo justificado; títulos centralizados |
| Recuo 1ª linha | 1,25 cm no corpo |

## Primeira página — espaçamento vertical

Intercalar **3–4 parágrafos vazios** entre os blocos iniciais (não depender de `space_after`):
`endereçamento → 4 vazios → Processo nº → 4 vazios → preâmbulo → 4 vazios → título da peça → 4 vazios → "pelos fundamentos..."`. Comparar sempre com o PDF de referência do cliente se existir.

## Workflow (DOCX canônico → PDF → MD)

1. Trabalhar **só no `.docx`**; nunca editar PDF/MD à mão.
2. Aplicar estilo via python-docx: Arial (`w:rFonts` ascii/hAnsi/cs/eastAsia) em todas as runs; `w:color w:val="000000"` em cada run; remover `w:highlight`/`w:shd`; A4+margens; espaçamento 1,5.
3. Gerar **PDF fiel via LibreOffice**: `soffice --headless --convert-to pdf --outdir out/ arquivo.docx`.
4. Validar PDF: com `pdfseparate` + `pdftotext -f N -l N`, conferir que **não há página em branco final nem título órfão** (título de seção isolado na última linha da página; `page-break-after:avoid` nem sempre resolve — ajuste manual). Remover página em branco com `pdfunite` das páginas que têm conteúdo.
5. Gerar **MD** derivado do DOCX: `pandoc arquivo.docx -f docx -t gfm -o arquivo.md`.
6. Entregar `.docx`/`.md`/`.pdf` com **mesmo nome base** (só extensão muda).
7. Verificar em `/tmp` com `python-docx`: `unzip -p f.docx word/document.xml | grep -oE 'w:ascii="[^"]*"' | sort | uniq -c` e idem `w:color`/`w:highlight`.

## Pitfalls

- NÃO usar Times New Roman (padrão forense = Arial na prática do cliente) — conferir `w:ascii` antes de entregar.
- Não confiar na "cor padrão"; **fixar preto explicitamente** em cada run.
- python-docx pode não estar no python default — usar `uv venv` + `pip install python-docx`, ou o venv do Hermes.

## `.gddoc` (atalho Google Docs)

`.gddoc` é um **atalho JSON (~212b)** apontando para um Google Docs real. **Sem OAuth NÃO criar `.gddoc` falso** — focar no `.docx`; quem abrir o `.docx` no Drive gera o atalho depois. Avise o usuário sobre isso em vez de forçar atalho quebrado.

## Renomeação em massa de documentos jurídicos (dry-run obrigatório)

- Padrão alvo `TIPO_VERSAO_DESCRICAO.ext` (ex `PETICAO_V7_EXCECAO_PRE_EXECUTIVIDADE.pdf`); versão logo após o TIPO, nunca no fim.
- UPPER_SNAKE_CASE, sem acentos/espaços; extensão minúscula; fotos sem extensão → `.jpg`.
- Remover palavras vazias (DE/DA/DO/DAS/DOS/PARA/PROCESSO se redundante); preservar versão; **não inventar versão** se ausente (marcar revisão).
- Mesma base p/ diferentes extensões do mesmo doc; **não sobrescrever em colisão** (diferenciar por caminho/pasta).
- **DRY-RUN primeiro** (analisar + propor, sem renomear), relatório (caminho/atual/proposto/status), **aguardar aprovação explícita** ("APROVADO. PODE EXECUTAR AS RENOMEACOES.").
- Validar mapa: todos cobertos, zero colisões de destino; incorporar arquivos que existem em só 1 réplica (união por conteúdo).
- Executar com `os.replace` se destino não existir; aplicar idêntico nas réplicas (MEGA canônica, Shared cliente, backup GDrive); conferir por hash `diff=0 extra=0 aus=0`.