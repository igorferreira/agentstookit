---
name: demos-html-interativas
description: Use ao criar ou depurar demos HTML interativas estilo Sims.
---

# Demos HTML Interativas (estilo Sims / escritórios vivos)

Escopo: páginas HTML de animação/demonstração em vanilla JS + CSS (sem React), servidas via Docker (nginx) e expostas via ngrok. Caso canônico: "Escritório Vivo dos Agentes" TimeAutomático (`~/projetos/hermes-as-service/demos/`), mas os padrões valem para qualquer demo interativa.

## Decisões de arquitetura (validadas com o Igor)

- **Vanilla JS, NÃO React** para demos: 1 arquivo HTML, roda em Docker nginx, ngrok e até file://. React só quando virar produto com estado complexo (login, WebSocket, multi-tenant).
- **Docker**: painel nginx (:8090) + TTS Piper como **container irmão** na mesma rede compose (o firewall do host bloqueia container→host; container↔container sempre funciona). Alpine não compila piper-tts — usar `python:3.11-slim`.
- **compose com context do pai**: `build: {context: .., dockerfile: docker/Dockerfile}` — evita `failed to compute cache key` quando o Dockerfile copia pastas irmãs (`principal/`, `tematicos/`, `clientes/`).
- **ngrok free temporário**: ler URL viva de `http://127.0.0.1:4040/api/tunnels`; link muda a cada restart — manter `LINK-PUBLICO-ATUAL.txt` e INDEX atualizados.

## Estrutura de pastas (multi-demo)

`principal/` (uso interno), `tematicos/` (versões seguras sem dados pessoais), `clientes/` (demo por cliente), `docker/`, `tts/`, gerador Python. Dockerfile copia das 3 pastas. Regra: editar sempre o `principal/` e regenerar os demais via gerador — nunca editar cópia solta.

## ⚠️ Pitfalls críticos (causaram bugs reais nesta classe)

1. **"Validou com screenshot" não é QA funcional.** Bolhas, cliques e handlers só se provam com clique REAL via CDP (`Runtime.evaluate` → `.click()` → contar elementos). Veja `references/qa-cdp-clicks.md`.
2. **Erro de script mata o script inteiro silenciosamente** — listeners definidos DEPOIS do ponto de erro nunca anexam (botão "não faz nada" sem erro visível). Capturar `Runtime.exceptionThrown` com `Runtime.enable` após `Page.reload`.
3. **Refatorações via regex em múltiplos HTML apagam funções silenciosamente** (caso: `trocarTarefa` perdida, `walk()` chamada sem definição, TDZ de `msg`). Depois de qualquer refatoração em lote: validar sintaxe de TODOS os arquivos com `node -e "new Function(...)"` E rodar QA funcional por clique — sintaxe OK ≠ runtime OK (TDZ/ReferenceError só aparecem executando).
4. **Cache do navegador mascara a versão servida**: o container pode ter a versão nova e o navegador a velha. Navegar com querystring anti-cache (`?v=<timestamp>`) ou `Page.reload` via CDP antes de testar; conferir o arquivo que o SERVIDOR entrega (`curl`) contra o erro reportado (nº de linha).
5. **Camadas z-index estilo Sims** (câmera frontal): cadeira z4 → mesa z7 → robô sentado z8 posicionado ACIMA da mesa (top ≈ st.y−16, left ≈ st.x+32). Robô andando sobe pra z8. Se o robô "sumir atrás da mesa", é ordem/posição de camada.
6. **Docker compose cache/`--force-recreate`**: após mudar Dockerfile/compose, usar `--build --force-recreate`; conferir o conteúdo DENTRO do container (`docker exec ... md5sum`) antes de diagnosticar mais longe.
7. **Legibilidade de personagens**: plaquinha de NOME sobre a cabeça + antena pulsante + olhos LED; grade anti-sobreposição (células) em vez de posições aleatórias puras.

## Fluxo de trabalho canônico

1. Editar `principal/*.html` (fonte da verdade).
2. Validar JS de todos os arquivos com node (parse).
3. Regenerar derivados (gerador Python) quando a mudança for estrutural.
4. `docker compose build painel && docker compose up -d --force-recreate`.
5. **QA funcional via CDP** (clique real + contagem de elementos + captura de exceções) — ver referência.
6. Screenshot headless + análise visual (vision) para composição/paleta/legibilidade.
7. Atualizar INDEX de links + `LINK-PUBLICO-ATUAL.txt` + commit no repo privado (Igor espera os dois: arquivo vivo + GitHub privado).

## Interatividade padrão (expectativa do usuário)

- Input de chat no rodapé com **botão ENVIAR explícito (➤)** além do Enter — em mobile o Enter não é confiável (teclados virtuais). Handler único `despachar()` chamado por ambos.
- Roteamento da mensagem por domínio (palavras-chave → agente específico), bolha do usuário + resposta do agente com TTS opcional (botão 🔊 lembrado em localStorage).