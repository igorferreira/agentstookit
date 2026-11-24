# Instagram Dossiê — Dossiê completo de perfil + PDF de orientações

Use quando Usuário enviar a URL de um perfil do Instagram e pedir dossiê. Somente leitura.

## Passo a passo

### (a) Abrir o perfil
- Extrair o @handle da URL (ex: `instagram.com/nome.perfil/` → handle `nome.perfil`).
- `browser_exec` com **session dedicada** (`session='instagram'`), `new_tab('https://www.instagram.com/<handle>/')`, `wait_for_load()`, `page_info()` + `capture_screenshot()`.

### (b) Login wall
- Se aparecer login/obrigação de entrar: `browser_vault_list` e procurar login salvo de instagram.com.
- Existe → `fill_input` (usuário) + `browser_vault_fill` com o handle. Continuar só lendo.
- NÃO existe → **PARAR** e relatar que Usuário precisa salvar o login do Instagram no vault. Nunca pedir/admitir senha em chat.
- Perfil privado → parar e relatar (nunca tentar contornar).

### (c) Coleta (loop até varrer tudo)
Coletar em loop e salvar rascunho em arquivo de trabalho (ex: `/tmp/dossie-<handle>.json` ou MD):
- Nome, @, bio, links da bio, categoria, seguidores/seguindo/posts
- Posts fixados (1–3)
- Feed post a post: rolar com `js('window.scrollTo(0, document.body.scrollHeight)')` + esperar + extrair (data, legenda, tema, likes/comentários visíveis). Repetir até repetir posts.
- Highlights visíveis (nomes dos álbuns)
- Datas de postagem para estimar frequência

### (d) Dossiê MD
Consolidar em `~/MEGA/Documentos/instagram/dossies/<handle>/DOSSIE-<HANDLE>.md` com seções:
1. **Identidade** (quem é, @, categoria, números)
2. **Posicionamento** (o que ele quer ser/parecer)
3. **Temas/pilares** (3–6 recorrentes)
4. **Padrão de postagem** (frequência, formatos, horários estimados)
5. **Top posts** (mais engajados, com métricas visíveis)
6. **Tom de voz**
7. **Audiência inferida**
8. **Oportunidades** (gaps, ideias, comparação com melhores práticas)
9. **Veredicto** (resumo final direto da Aline)

### (e) PDF — SEMPRE gerar (qualquer perfil)
- Para TODO perfil (educativo ou não): extrair TODAS as orientações/dicas/passes/conteúdo ensinado dos posts (da legenda e do texto visível nas imagens) e gerar `GUIA-<HANDLE>.pdf` na mesma pasta.
- Se o perfil for instrutivo → PDF concentra as dicas passo a passo.
- Se não for instrutivo → PDF é a compilação do conteúdo/posicionamento e do que ele ensina de forma implícita (práticas, estilo, técnicas).
- Gerador PDF (VALIDADO 11/11/2026): reportlab, fpdf e wkhtmltopdf NÃO instalados; pdflatex não existe. Caminho que funciona:
  1. `pandoc GUIA-<HANDLE>.md -o /tmp/guia-<handle>.html --standalone --metadata title="Guia — @<handle>"`
  2. `google-chrome --headless --disable-gpu --no-sandbox --print-to-pdf="<caminho absoluto>/GUIA-<HANDLE>.pdf" --no-pdf-header-footer /tmp/guia-<handle>.html`
  (chrome headless gera ~130KB em segundos; conferir com pdftotext que o conteúdo é o GUIA, não o dossiê)

### (f) Relatório final
- Contagens: posts lidos, posts fixados, highlights, dicas extraídas (se educativo), arquivos gerados (caminhos completos).
- Veredicto resumido em pt-BR.

## Regras
- SOMENTE LEITURA: nunca curtir/seguir/comentar/DM/postar/salvar.
- Nunca contornar login/privacidade.
- Sempre pt-BR.