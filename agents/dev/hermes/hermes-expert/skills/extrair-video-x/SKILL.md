---
name: extrair-video-x
description: Extrai vídeo de post do X e gera versão WhatsApp 720p.
version: 1.0
---

# Extração de vídeos do X/Twitter + versão WhatsApp

Gatilho: Usuário manda link de post do X/Twitter e pede para extrair/baixar o vídeo, normalmente para compartilhar no WhatsApp.

## Fluxo validado (06/09/2026, 7 vídeos no dia)

1. **Buscar metadados via API fxtwitter** (sem login, sem proxy — Nitter está morto):
   ```
   curl -s "https://api.fxtwitter.com/<USUARIO>/status/<ID>" -o /tmp/t.json
   ```
   Extrair com Python: autor (name, screen_name), texto do post, e de `media.all[]` → type, duration, width, height, **url** (MP4 da CDN video.twimg.com).
   Se `type != video` → avisar (imagem/gif não segue este fluxo).

2. **Baixar o original** (sempre com User-Agent):
   ```
   curl -sL --max-time 90 -A "Mozilla/5.0" "<url_cdn>" -o /tmp/vid.mp4 -w "%{http_code} %{size_download}b\n"
   file /tmp/vid.mp4   # validar: ISO Media MP4
   ```

3. **Salvar original** em `~/MEGA/Documentos/educacao_leitura/filmes_aulas_ia/videos/<CATEGORIA>/`:
   - Nome: `AAAA-MM-DD_AUTOR-TEMA-ORIGINAL.mp4` (data da extração, autor, tema curto em MAIÚSCULAS)
   - Categorias: `IA_TECNICO/` (conteúdo técnico de IA/agentes), `POLITICA/` (treta/política BR) — perguntar Usuário se ambíguo

4. **Gerar versão WhatsApp 720p** (REGRA DO USUÁRIO: SEMPRE 720p, reescalado — não só reencodado):
   - Vertical/portrait: `scale=720:1280` (up/down para 720 de largura)
   - Paisagem: `scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2`
   - Quase-quadrado: escalar pro lado maior = 720 e pad na direção menor
   ```
   ffmpeg -y -v error -i /tmp/vid.mp4 -vf "<filtro>" -c:v libx264 -crf 30 -preset medium -c:a aac -b:a 96k -movflags +faststart <NOME>-WHATSAPP.mp4
   ```
   Fontes com menos de 720px de largura sofrem upscale (avisar Usuário que a nitidez é limitada pela fonte).

5. **Registrar no índice** `videos/INDEX.md` (tabela): data, autor, link, contexto/tema (resumo do texto do post em 1 linha), categoria, status.

6. **Entregar**: MEDIA:/caminho/do/-WHATSAPP.mp4 (o Usuário compartilha direto do Telegram).

## Pitfalls
- URLs do x.com bloqueiam extração direta (login wall) — SEMPRE fxtwitter, nunca tentar x.com direto
- Vídeos longos (5min+) podem passar de 30MB no WhatsApp — normal, envia igual (limite real ~2GB)
- Se fxtwitter falhar/404, tentar novamente em alguns segundos; se persistir, avisar Usuário
- Post com múltiplos vídeos: baixar TODOS, sufixo -P1, -P2
- Auto-classificação: política/treta BR → POLITICA; análise técnica IA/agentes → IA_TECNICO
