---
name: escritorio-vivo-agentes
description: Use quando Igor pedir demo HTML viva de agentes estilo Sims.
---

# Escritório Vivo dos Agentes (demos HTML interativas)

Padrão validado (11/09/2026) para páginas HTML que mostram agentes de IA como personagens "vivos" em um escritório — demo de venda da TimeAutomático.

## Arquitetura canônica
- **Página única HTML/JS/CSS** sem build: `~/projetos/hermes-as-service/demos/<slug>.html`
- **Docker (versão oficial):** `demos/docker/docker-compose.yml` com 2 serviços:
  - `painel` (nginx:alpine, porta 8090) — serve os HTMLs + proxy `/tts`
  - `tts` (python:3.11-slim + piper-tts, vozes embutidas em `/voices`, porta interna 8777)
  - `nginx.conf`: `location /tts { proxy_pass http://tts:8777; }` (container irmão, SEM barra final no proxy_pass e SEM proxy para o host — firewall bloqueia container→host; **nunca usar 127.0.0.1 nem host.docker.internal**)
- **TTS:** Piper pt-BR (`faber`/`cadu`), endpoint `/tts?text=...&voice=...` com cache por hash; botão 🔊/🔇 salvo em localStorage
- **Túnel:** `ngrok http 8090` (free, link muda a cada restart) → ler URL em `http://127.0.0.1:4040/api/tunnels` e salvar em `demos/LINK-PUBLICO-ATUAL.txt`

## Elementos de realismo (estilo The Sims)
1. Estações fixas: mesa + cadeira com encosto; personagem com cabeça/corpo
2. Ciclo: senta → placa de atividade + café com vapor + ⌨ digitando → de vez em quando levanta, passeia, volta
3. Grade anti-sobreposição (células 5×4 com jitter)
4. Falas por domínio (cada agente só fala do próprio tema) + bolhas de fala
5. Painel lateral "Ações em tempo real" + alertas rotativos no topo (barra vermelha)
6. Relógio de expediente (8-18h, almoço 12h = todos levantam) + sala de reunião com mesa redonda (2-4 agentes se juntam)
7. Input do usuário com roteamento por palavras-chave para o agente do domínio
8. Mobile: media queries <768px, painel vira drawer, elementos menores

## Regras de privacidade (Igor)
- Demo principal com agentes pessoais (Rafael/relacionamento, Financeiro com faturas) **só roda local** — nunca publicar no ngrok sem a varredura de conteúdo pessoal
- Versões para clientes: remover agentes/falas/alertas pessoais; validação obrigatória com busca textual (SISBAJUD, Maricá, Adrielly, VALLO, fatura, CDB → zero ocorrências)
- Variações por cliente: trocar AGENTES/FALAS/ALERTAS/CHIPS/título `<title>` E `<h1>` (gerador que troca só um deles é bug já ocorrido)

## Geração de variantes
Usar `~/projetos/hermes-as-service/demos/gerar_escritorios_tematicos.py` como modelo: parte do HTML base, injeta título, paleta CSS (vars `--navy`/`--cyan`), decoração temática (CSS absoluto), agentes, falas, tarefas, alertas, chips. Validar: contagem de agentes, títulos, JS parse (node), zero conteúdo pessoal.

## QA obrigatória (Igor cobra explicitamente)
1. `docker compose up -d --build` e conferir 200 OK em todas as páginas
2. Screenshot headless: `google-chrome --headless --screenshot=... --window-size=1400,900 <url>` + análise visual (personagens sentados, placas, paleta, sobreposições)
3. TTS via proxy (200 + WAV) e `/health-tts`
4. Títulos `<title>` corretos por variante (gerador às vezes não troca — validar com grep)
5. Túnel: testar página + TTS pela URL pública

## Pitfalls
- Alpine não compila piper-tts (sem wheel) — usar `python:3.11-slim`
- `COPY *.html` no Dockerfile exige build context correto; copiar HTMLs para a pasta do contexto ou ajustar `context:` no compose
- Após mudar nginx.conf, `--force-recreate` pode ser necessário
- Proxy com barra final (`/tts/`) causa 301 que perde query string — usar `proxy_pass http://tts:8777;` sem path
- ngrok free: link muda a cada restart; sempre reler a API e atualizar o arquivo de links
