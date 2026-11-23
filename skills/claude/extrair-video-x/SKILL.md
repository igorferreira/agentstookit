# Skill: extrair-video-x (versão Claude Code — subagente/skill de projeto)

## Quando usar
Quando o usuário passar um link de post do X/Twitter e pedir para extrair/baixar o vídeo e gerar versão WhatsApp 720p.

## Contexto
- O X bloqueia extração direta (login wall). A rota que funciona é a API pública **fxtwitter** (JSON sem login).
- Pasta de destino: `~/MEGA/Documentos/educacao_leitura/filmes_aulas_ia/videos/<CATEGORIA>/`
- Categorias: `IA_TECNICO/` (análise técnica de IA/agentes) e `POLITICA/` (política/treta BR). Pergunte se ambíguo.
- REGRA: a versão WhatsApp é SEMPRE 720p reescalado (não só reencodado), nome `<BASE>-WHATSAPP.mp4`, junto ao original.

## Passo 1 — Metadados via fxtwitter
```bash
curl -s "https://api.fxtwitter.com/<USUARIO>/status/<ID>" -o /tmp/t.json
```
Com Python (stdlib): de `['tweet']` → `author.name`, `author.screen_name`, `text`; de `media.all[]` → `type`, `duration`, `width`, `height`, `url` (MP4 da CDN video.twimg.com).
Se `type != "video"` → informe que o post não tem vídeo.

## Passo 2 — Baixar original
```bash
curl -sL --max-time 90 -A "Mozilla/5.0" "<url_cdn>" -o /tmp/vid.mp4 -w "%{http_code} %{size_download}b\n"
file /tmp/vid.mp4   # deve ser "ISO Media, MP4"
```

## Passo 3 — Salvar original
Nome: `AAAA-MM-DD_AUTOR-TEMA-ORIGINAL.mp4` (data da extração; autor; tema curto MAIÚSCULAS com hífen).
```bash
mkdir -p <PASTA_CATEGORIA>
cp /tmp/vid.mp4 <PASTA_CATEGORIA>/<NOME>-ORIGINAL.mp4
```

## Passo 4 — Versão WhatsApp 720p
- Vertical/portrait: `scale=720:1280`
- Paisagem: `scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2`
- Quase-quadrado: lado maior = 720, pad na direção menor
```bash
ffmpeg -y -v error -i /tmp/vid.mp4 -vf "<FILTRO>" \
  -c:v libx264 -crf 30 -preset medium -c:a aac -b:a 96k \
  -movflags +faststart <PASTA_CATEGORIA>/<NOME>-WHATSAPP.mp4
```
Fontes < 720px de largura sofrem upscale — avise que a nitidez é limitada pela fonte.

## Passo 5 — Índice
Adicionar linha na tabela de `videos/INDEX.md`: data, autor, link, contexto (resumo em 1 linha do texto do post), categoria, status (`ORIGINAL + WHATSAPP 720p ✅`).

## Pitfalls
- Nunca baixar direto do x.com (login wall); sempre fxtwitter.
- Múltiplos vídeos no post: baixar todos, sufixos -P1, -P2.
- fxtwitter 404: aguardar segundos e repetir; persistindo, avisar o usuário.
- Vídeos 5min+ podem passar de 30MB — normal (limite WhatsApp ~2GB).
