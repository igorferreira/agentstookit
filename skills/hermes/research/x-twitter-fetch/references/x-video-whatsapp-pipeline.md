# Vídeos de X para WhatsApp — pipeline de extração e compartilhamento (validado 06/09/2026)

Fluxo completo usado para extrair vídeos de posts do X e entregá-los prontos para grupos de WhatsApp.

## 1. Extrair metadados via fxtwitter API

```bash
curl -s --max-time 10 "https://api.fxtwitter.com/<usuario>/status/<id>" -o /tmp/tweet.json
python3 -c "
import json
t = json.load(open('/tmp/tweet.json'))['tweet']
print('AUTOR:', t['author']['name'], '@'+t['author']['screen_name'])
print('TEXTO:', t['text'][:600])
m = t.get('media', {})
for x in m.get('all', []):
    print('tipo:', x.get('type'), '| dur:', x.get('duration'), '| size:', x.get('width'), 'x', x.get('height'))
    print('url:', x.get('url'))
"
```

- `tweet.text` = texto completo do post
- `tweet.media.all[]` = URLs diretas na CDN (video.twimg.com / pbs.twimg.com)
- Threads = uma chamada por status ID

## 2. Baixar o vídeo original

```bash
curl -sL --max-time 90 -A "Mozilla/5.0" "<url-do-CDN>" -o /tmp/video.mp4
```

- SEMPRE com User-Agent de navegador.
- Se 404: refazer a chamada do fxtwitter — o parâmetro `?tag=` da URL muda entre fetches; URL velha é a falha nº 1.
- Vídeos de 4-5 min ~120 MB em 1080p; 1-2 min ~25-30 MB.

## 3. Gerar versão WhatsApp (720p — REGRA DO USUÁRIO)

Reescalar para 720p, não apenas reencodar (Usuário rejeitou versão só-reencodada):

**Vertical (origem 1080x1920):**
```bash
ffmpeg -y -v error -i original.mp4 \
  -vf "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2" \
  -c:v libx264 -crf 30 -preset medium -c:a aac -b:a 96k -movflags +faststart saida-WHATSAPP.mp4
```

**Horizontal (origem 1920x1080):**
```bash
# mesma linha, trocando para: scale=1280:720:... pad=1280:720:...
```

**Quase-quadrado (ex.: 1081x1272):** pad para o short-side 720: `scale=720:852:... pad=720:852:...`

Resultados reais: 60s 1080p 22 MB → 720p ~4,8 MB; 4min20s 1080p 120 MB → 720p ~26,5 MB; 2min 32 MB → 5,7 MB.

## 4. Salvar com nomenclatura padrão

Pasta: `~/MEGA/Documentos/educacao_leitura/filmes_aulas_ia/videos/<CATEGORIA>/`

- `AAAA-MM-DD_AUTOR-TEMA-ORIGINAL.mp4`
- `AAAA-MM-DD_AUTOR-TEMA-WHATSAPP.mp4`

Categorias: `IA_TECNICO/` (conteúdo técnico de IA — estudo) | `POLITICA/` (posts políticos/treta BR). Outro tema → criar pasta + atualizar INDEX.

## 5. Atualizar índice

Append em `videos/INDEX.md`: data, autor, handle, link, resumo de 1 linha do conteúdo, duração/formato, status de arquivos salvos.

## 6. Entregar no Telegram

Usar o caminho do arquivo `-WHATSAPP.mp4` no formato de entrega de arquivo (MEDIA:) para Usuário encaminhar direto ao grupo.

## Padrões do acervo (INDEX.md em filmes_aulas_ia/)

- Pesquisas/tweets técnicos → tabela "PLANO DE ESTUDO" no INDEX.md pai.
- Tweets com conteúdo denso → salvar resumo estruturado (pontos-chave em pt-BR) direto no INDEX.md — Usuário não sempre abre o link.
