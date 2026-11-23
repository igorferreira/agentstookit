---
name: extrair-posts-x
description: "Use when extracting X posts and archiving their text/media."
---

# extrair-posts-x

Extrair e salvar posts do X/Twitter (com texto, metadados e mídias) para estudo, política ou envio a terceiros. Regra da thread: um link X enviado isoladamente nesta conversa já é um pedido para extrair e arquivar; não peça um verbo adicional. O MEGA é o destino padrão, mas um destino explícito indicado por Usuário para aquele post prevalece. Preserve a organização hierárquica temática e a indexação central. Aplique o protocolo global da fila antes de iniciar.

## Procedimento

### 1. Preservar a fonte e obter dados via API fxtwitter

Antes de derivar o endpoint da API, registre o URL original exatamente como recebido, incluindo query string; não o normalize nem remova parâmetros comuns de compartilhamento. Use o handle e o ID para consultar fxtwitter, mas mantenha o URL original na seção Links Originais do arquivo final. Se o URL contiver credenciais reais, aplique as regras de segurança abaixo e redija apenas o segredo.

```bash
SCRATCH_DIR="${TMPDIR:-$HOME/.hermes/cache/scratch}"
mkdir -p "$SCRATCH_DIR"
POST_JSON="$SCRATCH_DIR/post_<ID>.json"
curl -sS "https://api.fxtwitter.com/<usuario>/status/<ID>" > "$POST_JSON"
python3 -c "import json,sys; print(json.dumps(json.load(open(sys.argv[1]))['tweet'], indent=2))" "$POST_JSON"
```

**GOTCHA:** `curl | python3` precisa aprovação de segurança — usuário pode negar. Se bloqueado, usar `browser_exec` navegando direto em `https://x.com/<usuario>/status/<ID>`.

### 2. Escolher e verificar o destino

- Use o destino explicitamente indicado para aquele post; somente quando Usuário não especificar outro lugar, use o padrão `~/MEGA/Documentos/educacao_leitura/filmes_aulas_ia/posts/<tema>/<DATA>-<TOPICO>`.
- Mantenha o Markdown e a mídia juntos no destino solicitado. Não duplique os artefatos em MEGA e Google Drive, a menos que Usuário peça ambos; mesmo quando o artefato estiver em outro destino, atualize o índice central do MEGA com o caminho real.
- Se uma correção posterior mudar o destino, atualize o mesmo card e o mesmo registro — não crie pedido duplicado. Resolva expressões como “esse post” pelo URL mais recente enviado na mesma conversa; se houver mais de um candidato plausível, pergunte antes de redirecionar.
- Para destinos Insync/Google Drive, confira a conta e os componentes reais do caminho. Não substitua uma pasta ausente por outra parecida. Se a pasta solicitada não existir, registre o caminho exato; crie a hierarquia apenas quando a execução efetivamente começar e o usuário tiver pedido para salvar ali, pois a pasta sincronizada grava no cloud. Não crie pastas enquanto o item estiver apenas enfileirado.
- Temas comuns: `politica`, por área de estudo, etc. **Nomear sem acentos.** Inserir sempre ano-mês-dia no início do nome.

Exemplo do destino padrão:
```
posts/politica/AAAA-MM-DD_TOPICO
```

### 3. Extrair e organizar do JSON

Do campo `tweet` extrair:
- `id`, `url`, `created_at`, `lang`, `author.*`
- Textos: `text`, `raw_text.text`, `raw_text.facets`
- Métricas: `likes`, `retweets`, `replies`, `bookmarks`, `views`, `quotes`
- Mídia: `media.url` (links diretos mp4), `media.thumbnail_url`, `media.duration`, `media.width`, `media.height`
- `source_tweet_reposted`: URL do tweet repostado
- `community_note`: se existir, incluir no MD

### 4. Baixar mídia (vídeo/imagem)

```bash
# Vídeo HD (melhor qualidade disponível)
curl -fSL -o "VIDEO_<NOME>.mp4" "<URL_VÍDEO_JSON>" --progress-bar

# Thumbnail
curl -fSL -o "thumbnail.jpg" "<URL_THUMB_JSON>"
```

**Nota:** Vídeos de amplify_video podem ser lentos (até 9min). Usar `--progress-bar` para feedback. Timeout alto (120s+). Após baixar, confirme tamanho não nulo e inspecione streams/duração com `ffprobe`; se copiar a mídia para outro destino, compare os SHA-256. Só declare a mídia arquivada depois dessas verificações.

### 5. Tradução (se necessário)

Se `lang` != `pt`: traduzir o texto completo preservando formatação (emojis, listas numeradas, citações). **Sempre colocar texto original primeiro, depois tradução entre blocos separadores `---`.** Idioma-alvo: pt-BR.

### 6. Gerar arquivo Markdown

Arquivo `.md` na pasta destino com estrutura:
- Cabeçalho: título + fonte + data extração + idioma
- Seção Mídia: links relatáveis ao vídeo/thumbnail + tabela de metadados técnicos
- Seção Texto Original (idioma source): entre crase/triplo-backtick
- Seção Tradução (pt-BR): texto traduzido completo
- Seção Métricas: tabela com todas as métricas
- Seção Autor: dados do autor do post
- Seção Contexto/Resumo (opcional): análise contextual quando relevante

**REGRAS DO MD:**
- Nunca expor chaves/tokens/senhas → `[REDACTED]`
- Listar TODOS os links originais no final (seção Links Originais)
- Incluir timestamp UNIX e Video ID quando aplicável

### 7. Atualizar INDEX.md

Adicionar entrada na seção correspondente do `~/MEGA/Documentos/educacao_leitura/filmes_aulas_ia/INDEX.md`. Formato (mais recente primeiro):

```markdown
### N — Título (@handle)
- **Data de extração:** DD/MM/YYYY
- **Fonte original:** https://x.com/.../status/XXXX
- **Idioma:** ...
- **Mídia:** ...
- **Local do MD:** caminho absoluto
- **Resumo:** 1-2 frases sintetizando o conteúdo
```

## Conversão de vídeo para WhatsApp Status

Requisitos obrigatórios: **≤10 MB**, formato vertical/portrait.

### Passo a passo

```bash
INPUT="video_original.mp4"
OUTPUT="whatsapp-status.mp4"
ffmpeg -i "$INPUT" \
  -c:v libx264 -preset fast -crf 26 \
  -vf "scale=360:640:force_original_aspect_ratio=decrease,pad=360:640:(ow-iw)/2:(oh-ih)/2:color=black" \
  -pix_fmt yuv420p \
  -c:a aac -b:a 96k \
  -shortest -movflags +faststart \
  "$OUTPUT" -y
```

**Parâmetros chave:**
- `-crf 26`: equilíbrio qualidade/tamanho (range útil: 24-30)
- `scale=360:640`: resolução vertical compacta, cabe no status
- `pad=...`: barras pretas nas laterais para manter proporção
- `-b:a 96k`: áudio AAC suficiente
- `-movflags +faststart`: streaming otimizado
- `-shortest`: corta no menor stream

### Se passar de 10 MB, refazer com:
- Reduzir escala para `280:500`
- Aumentar CRF para `28-30`
- Reduzir áudio para `64k`

**Ordem preferencial:** reduzir dimensões antes de piorar qualidade. Menos pixels = melhor compressão que maior CRF.

## Pitfalls

- **fxtwitter rate limit:** se retornar erro, usar fallback `api.vxtwitter.com` ou navegador (`new_tab`)
- **Vídeos amplify_video:** usam URL diferente dos vídeos normais do X — endpoint inclui `/vid/avc1/RESOLUÇÃO/NOME.mp4`
- **Conteúdo sensível:** `possibly_sensitive=true` no JSON indica conteúdo adulto/violento — considerar avisar o usuário
- **Árabe/RTL:** textos em árabe/heraico precisam `ensure_ascii=False` ao gerar JSON para preservar caracteres. No MD, manter original EXATO (sem alterar diacríticos).
- **Tweet longo (note tweet):** campo `is_note_tweet` = true significa texto truncado — buscar variante com `_extended` ou usar browser para texto completo.

## Segurança

- NUNCA armazenar tokens, chaves API, senhas no arquivo MD
- URLs de vídeo são temporárias mas não expiram rapidamente (~dias); salvar cópia local é mandatório
- Chave de API OpenRouter/chatGPT/etc nunca deve entrar nos arquivos salvo
