---
name: legal-case-files-br
description: "Use ao organizar/enviar arquivos de processo para advogados."
version: 1.0.0
---

# Organização & Comunicação de Arquivos de Processo (clientes/advogados do Igor)

Governa como manipular o acervo de um processo judicial do Igor ao entregar para advogados (ex.: Dr. Diogo Simas, caso Maricá 0040223-62.2021.8.19.0031) e ao manter as pastas locais/Drive.

## ⛔ Regras de comunicação com advogados e terceiros (IMPERATIVAS)

1. **NUNCA enviar arquivos Markdown (.md) para advogados ou profissionais terceiros.** O advogado não trabalha com Markdown. **Converta SEMPRE para PDF** antes de enviar (pandoc → wkhtmltopdf, fundo branco).
2. **Markdown é apenas para uso interno** Igor/Hermes. No acervo entregue a terceiros, o `.md` fica como fonte canônica local, mas **toda versão entregue sai em PDF**.
3. Todo documento de processo deve ter **uma versão PDF** correspondente (`.md`/`.docx` → `.pdf`), mantendo todas as versões.
4. Um advogado que ainda não domina o contexto recebe email **autossuficiente** (nº do processo, tese, prova), sem pressupor conhecimento prévio.

## �  Sobre arquivos `.gddoc` / `.gdlink` (Insync + Google Docs)

- Um `.gddoc` é um **atalho JSON** (ex.: 212 bytes, `{"url":"https://docs.google.com/document/d/...","file_id":"..."}`), NÃO um documento real. Aponta para um Google Docs que já existe no Drive.
- `.gdlink` é atalho equivalente para outros tipos de arquivo do Drive.
- **Não é possível criar um Google Docs funcional por linha de comando** em `/MEGA` ou no Insync — escrever um `.gddoc` manual gera atalho órfão apontando pra nada. Para criar um `.gddoc` real, o documento precisa ser criado no app Google Docs (usuário/advogado).
- Ao inspecionar arquivos com extensão `.gddoc`/`.gdlink`, confira o **magic bytes / conteúdo** — pode conter um PDF ou texto real sob extensão errada (aconteceu com V5/V6 da petição, renomeados errado por substring no mapeamento).

## 🗂 Estrutura de pastas de um processo (padrão MEGA + Google Drive)

Origem canônica: **MEGA** (`~/MEGA/Documentos/legal_publico/processos/<processo_nome>/`). Replicar para as pastas do Drive (backup e cópia compartilhada do advogado).

```
<processo_nome>/                 # ex.: processo_marica_igor (snake_case, sem acento)
├── peticao/                     # petiçoes, minutas, exceções, pareceres
└── documentos/                  # provas, quadros, comprovantes, docs pessoais, processo
```

Regras de organização:
- **Nome do processo igual nas duas/todas as pastas** (`processo_<nome>`), mesmo nas cópias do Drive.
- Pastas internas fixas: `peticao/` e `documentos/`.
- **Todas as pastas têm os MESMOS arquivos**; se uma tem a mais, acrescenta-se nas demais (união por conteúdo).
- **Arquivos de autos** ficam na subpasta `documentos/`; **petiçoes/minutas** em `peticao/`. Ficha/contexto de gestão pode ficar na raiz.
- **NUNCA apagar arquivo** — manter todas as versões. Deduplicar por **hash md5** (same content = 1 cópia; different content = versão distinta com sufixo). Antes de apagar pasta antiga após reorganização, **verificar por hash que nenhum arquivo ficou só na pasta antiga** (faltante → copiar antes).

## 🏷 Padrão de nomenclatura de arquivo

- País `SNAKE_CASE`, **MAIÚSCULAS**, **sem acento** (remover NFKD combining chars).
- **Prefixo com palavra-chave** que identifica o tipo:
  - Petiçoes: `PETICAO_...` (ex.: `PETICAO_EXCECAO_PRE_EXECUTIVIDADE_FINAL_DR_DIOGO_V1.pdf`)
  - Provas/documentos: `DOC_...` (ex.: `DOC_ALTERACAO_CONTRATUAL_CESSAO_COTAS_JUCERJA_2007_V1.pdf`)
- **Sufixo de versão** `_V1/_V2/...` quando houver duplicata de conteúdo (versões numeradas da mesma peça).
- Nunca deixar espaços nem caracteres especiais.

## ⚠ Pitfall: mapeamento por substring

Ao mapear arquivos antigos para nomes-alvo usando `substring in nome`, **nomes que compartilham prefixo colidem** (ex.: `07801460000168.pdf` vs `Screenshot_.../CNPJa...`). Um arquivo pode ser sobrescrito por outro de conteúdo diferente se o matching não for específico. Use correspondência **pelo hash md5** (conteúdo), não por substring do nome, e valide que cada destino tem o conteúdo esperado.

## PNG/conversão de .md → .pdf (padrão usado)

pandoc → HTML com CSS inline (fundo `#fff`, tabelas `#ccc`, cabeçalhos `#e8f0ec`, linhas alternadas `#f7faf8`) → `wkhtmltopdf --enable-local-file-access --no-background`. Evita títulos órfãos e fundo escuro.

## 👥 Mensagens a um amigo/contato que é juiz (tom)

Quando o destinatário é **amigo pessoal do Igor que também é profissional** (ex.: Bruno, juiz estadual tributário):
- Tom de amigo, frase curta e quebras de linha por mensagem (padrão WhatsApp do Igor), mas os dados técnicos ficam precisos.
- Dividir em **várias mensagens curtas** (máx. ~6-8 linhas cada), não um bloco contínuo.
- Usar o termo **"amigo"**, nunca **"brother"** (Igor corrigiu explicitamente: ele fala "amigo"). Não inventar gírias afetivas que o Igor não usa.