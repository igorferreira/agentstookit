# Templates e geradores — escritório vivo dos agentes

Fontes canônicas (reproduzir com modificações):

## Arquivos no disco (fonte da verdade funcional)
- `~/projetos/hermes-as-service/demos/escritorio_agentes_vivo.html` — página base completa (Sims + TTS + mobile + expediência + reunião)
- `~/projetos/hermes-as-service/demos/gerar_escritorios_tematicos.py` — gerador de variantes temáticas (injeta título, paleta, decoração, agentes, falas, tarefas, alertas, chips)
- `~/projetos/hermes-as-service/demos/gerar_demos_clientes.py` — gerador de versões por cliente (Rodrigo, Luís, Bernardo, Nalin)
- `~/projetos/hermes-as-service/demos/tts_server.py` — servidor TTS Piper (versão host, bind 0.0.0.0)
- `~/projetos/hermes-as-service/demos/docker/` — Dockerfile, nginx.conf, docker-compose.yml (painel + tts irmãos)
- `~/projetos/hermes-as-service/demos/tts/` — Dockerfile do TTS (python:3.11-slim + piper) e vozes
- `~/projetos/hermes-as-service/demos/painel_24h.sh` — launcher kiosk 24h com auto-restart
- `~/projetos/hermes-as-service/demos/LINK-PUBLICO-ATUAL.txt` — links públicos atuais do túnel

## Temas já gerados (11/09/2026)
- `escritorio_psicologia.html` — só Rafael, paleta verde-sálvia, poltronas/plantas/tapete
- `escritorio_contabilidade.html` — só Contador, azul corporativo, arquivos/calculadora (falas 100% genéricas)
- `escritorio_advocacia.html` — 7 agentes jurídicos, bordô/dourado, estantes/balança
- Por cliente: rodrigo, luis, bernardo, nalin

## Variantes geradas por IA de imagem
Capa isométrica estática (estilo post ofercama) pode ser gerada com image_generate (estilo 3D isométrico, painéis flutuantes com nomes dos agentes, slogan TimeAutomático) — salva em MEGA como `AAAAMMDD_AGENTES-TIMEAUTOMATICO-ISOMETRICO.png`.
