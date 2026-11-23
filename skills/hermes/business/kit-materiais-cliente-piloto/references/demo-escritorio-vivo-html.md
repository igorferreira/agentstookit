# Demo Viva — Escritório de Agentes no Navegador (TimeAutomático)

Referência validada em 11/09/2026: página HTML que mostra os agentes do cliente
trabalhando em tempo real — vitrine de venda da TimeAutomático.

## Arquivos canônicos
- Template principal: `~/projetos/hermes-as-service/demos/escritorio_agentes_vivo.html` (v3, modo The Sims)
- Gerador de versões por cliente: `demos/gerar_demos_clientes.py` → `escritorio_<cliente>.html` (rodrigo, luis, bernardo, nalin)
- Docker: `demos/docker/` (nginx + painel :8090) + `demos/tts/` (Piper pt-BR container irmão) — `docker compose up -d`
- TTS host (alternativa): `demos/tts_server.py` — bindar 0.0.0.0 se for acessado fora do host
- Link público: `demos/LINK-PUBLICO-ATUAL.txt` + túnel `ngrok http 8090` (URL via `http://127.0.0.1:4040/api/tunnels`)

## Arquitetura validada
- **Página única self-contained** (HTML+CSS+JS inline, sem build). Agentes = bolhas coloridas com cabeça; estações = mesa + cadeira com encosto (estilo The Sims). Ciclo de vida: sentado trabalhando → aleatoriamente levanta, passeia, volta (12–32s).
- **Grade anti-sobreposição**: dividir a tela em células (ex. 5×4) com jitter dentro da célula — random puro faz estações se sobreporem (bug pego por screenshot QA).
- **Falas por domínio**: cada agente só fala do próprio tema (objeto `FALAS[dominio]`). Roteamento do input do usuário por keyword (fatura→financeiro, exame→saúde etc.).
- **Painel "Ações em tempo real"**: prepend de itens no DOM + teto de 18 filhos (evita memory leak).
- **Alertas**: barra vermelha no topo alternando avisos a cada 15s (fatura vence, advogado, CDB).
- **TTS**: endpoint local `GET /tts?text=...&voice=faber|cadu` → WAV (cache por hash md5 texto+voz). Botão 🔊/🔇 persistido em localStorage.

## Pitfalls (todos encontrados em QA real, 11/09/2026)
1. **Container → host NUNCA funciona neste ambiente** (firewall bloqueia em qualquer IP, inclusive gateway da rede). NÃO perder tempo com `host.docker.internal` / gateway IP — ir direto para **container irmão** na mesma rede compose (container↔container sempre funciona).
2. **Piper no Alpine falha** (`piper-phonemize` sem wheel) — usar `python:3.11-slim`. Vozes (~150MB) copiadas pro build em `tts/voices/`.
3. **`proxy_pass` com path**: `location /tts { proxy_pass http://tts:8777; }` (sem URI no proxy_pass) — com URI causa 301/redirect perdendo a query string.
4. **`docker compose up -d` não recria container com config nova** — usar `--build --force-recreate` quando mudar nginx.conf/COPY.
5. **Validar JS embutido** com `node -e "new Function(html.match(/<script>([\s\S]*?)<\/script>)[1])"` antes do rebuild.
6. **QA visual com screenshot**: `google-chrome --headless --screenshot=/tmp/x.png --window-size=1400,900 URL` + `vision_analyze` com pergunta específica ("há sobreposição?"). 2 rodadas — 1ª pegou colisão, 2ª validou a grade.
7. **Título `<title>` esquecido no gerador**: gerar versões por cliente via regex troca só H1 — sempre trocar `<title>` também.

## Mobile (regra do Igor: o HTML TEM que funcionar no celular)
- viewport meta + media queries < 768px (mesas/agentes/bolhas menores)
- painel lateral vira drawer (bottom sheet) com botão flutuante 📊
- acesso pela rede local: `python3 -m http.server 8765 --bind 0.0.0.0` na pasta demos → `http://<IP-LAN>:8765/<arquivo>.html`

## Exposição pública (ngrok)
- ngrok instalado + authtoken já configurado. `ngrok http 8090` em background → ler URL da API local :4040.
- Túnel free = temporário (URL muda a cada restart). Salvar sempre em `LINK-PUBLICO-ATUAL.txt`.
- TTS funciona pelo túnel (proxy /tts) — no celular o som funciona também.
- Para link permanente: domínio fixo na conta ngrok do Igor.
