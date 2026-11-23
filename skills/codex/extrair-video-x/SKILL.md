# Skill: extrair-video-x (versão Codex CLI)

## Quando usar
Quando aparecer um link de post do X/Twitter e o usuário pedir para extrair/baixar o vídeo e gerar versão WhatsApp 720p.

## Contexto
- O X bloqueia extração direta (login wall). A rota que funciona é a API pública **fxtwitter** (JSON sem login).
- Pasta de destino dos vídeos: `~/MEGA/Documentos/educacao_leitura/filmes_aulas_ia/videos/<CATEGORIA>/`
- Categorias: `IA_TECNICO/` (análise técnica de IA/agentes) e `POLITICA/` (política/treta BR). Pergunte ao usuário em caso de dúvida.
- REGRA DO USUÁRIO: a versão para WhatsApp é SEMPRE 720p reescalado (não apenas reencodado), nome `<BASE>-WHATSAPP.mp4`, salvo junto ao original.

## Passo 1 — Metadados via fxtwitter
```bash
curl -s "https://api.fxtwitter.com/<USUARIO>/status/<ID>" -o /tmp/t.json
```
Com Python (stdlib), extrair de `['tweet']`: `author.name`, `author.screen_name`, `text`, e de `media.all[]` → `type`, `duration`, `width`, `height`, `url` (MP4 da CDN video.twimg.com).
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
Fontes < 720px de largura sofrem upscale — avise o usuário que a nitidez é limitada pela fonte.

## Passo 5 — Índice
Adicionar linha na tabela de `videos/INDEX.md`: data, autor, link, contexto (resumo do texto do post em 1 linha), categoria, status (`ORIGINAL + WHATSAPP 720p ✅`).

## Pitfalls
- Nunca tentar baixar direto do x.com (login wall); sempre fxtwitter.
- Posts com múltiplos vídeos: baixar todos, sufixos -P1, -P2.
- Se fxtwitter retornar 404, aguarde alguns segundos e repita; persistindo, avise o usuário.
- Vídeos 5min+ podem passar de 30MB — normal, o limite do WhatsApp é ~2GB.
