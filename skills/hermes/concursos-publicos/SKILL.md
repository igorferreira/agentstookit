---
name: concursos-publicos
version: 1.0.0
category: carreira
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [carreira, concursos, dossie, vigia]
    related_skills: [price-watch-cron, dossie-empresa-vaga]
description: Use quando Igor pedir dossiê ou vigia de concursos.
---

# Concursos Públicos — dossiê, pasta por concurso e vigia

## When to Use

- Igor pedir pesquisa de concursos públicos ("concursos de TI", "concursos nível médio", "previstos para 2027").
- Pedir para reestruturar a pasta de concursos ou criar ficha de um concurso novo.
- Pedir vigia para edital previsto ("me avise quando sair o edital").

## Standing rules (Igor)

- **Lotação RJ only:** qualquer concurso com lotação fora do RJ é descartado e marcado `❌` na ficha — nunca sugeri-lo como oportunidade. Única exceção: polo RJ dentro de concurso nacional (ex.: Transpetro).
- **Separar por escolaridade:** concursos de TI ficam em `~/MEGA/Documentos/carreira/concursos/ti/`; concursos de nível médio (para a [NOME-REDACTADO]) em `concursos/segundo-grau/`. Nunca misturar as duas áreas.
- **Sempre conferir o edital oficial antes de inscrever** — portais de concursos (pci, Estratégia, Gran, citytudo, Acelera) podem estar defasados ou divergir entre si; os dados deles são ponto de partida, não verdade.
- Registrar prazos de inscrição abertos com destaque na resposta final — o vigia cobre só os previstos.

## Procedure

1. **Definir os alvos** com Igor ou pelo critério do pedido (área, escolaridade, local). Classificar em: ABERTOS / PREVISTOS-AUTORIZADOS / ENCERRADOS (prova futura, referência).
2. **Pesquisar** — rodar 4-8 `web_search` em paralelo: panoramas de portais (pci/estrategia/aprovati/grancursos/citytudo) + buscas focadas por órgão/UF + buscas de "previstos 2027". Segunda rodada só nos furos (ex.: certame nacional específico, órgão estadual).
3. **Criar o dossiê geral datado** na raiz da área (`concursos/<area>/DOSSIE-CONCURSOS-<AREA>-<YYYY-MM-DD>.md`): tabelas por classificação (cargo, vagas, salário, inscrições, prova, banca, lotação) + seção de recomendações para o perfil do candidato + fontes com URL.
4. **Estruturar pastas** — uma pasta por concurso com `FICHA.md` cada (gerar por script Python com lista de tuplas, não à mão). Ficha: órgão, status, cargo, vagas, salário, inscrições, prova, banca, lotação, fit (`✅ RJ` / `⚠️` / `❌`), observações, links. Seção **Histórico (append-only)**: nova informação = append datado, nunca sobrescrever dados antigos.
5. **Indexar** — `_INDEX.md` na raiz da área com tabelas por status (abertas/previstos/encerrados), links relativos para cada pasta, e a convenção (append-only, nova ficha entra no _INDEX). Raiz `concursos/` tem um `_INDEX.md` apontando para as áreas.
6. **Vigia para previstos** — seguir o skill `price-watch-cron` (padrão vigia: script `~/.hermes/scripts/vigia-<slug>.py`, cron `--no-agent --deliver telegram`, stdout vazio = silêncio). Para concursos: alvos com listas `gatilhos`/`excluir` por órgão, fontes = portais de concursos + site oficial de cada órgão. **Semear o baseline rodando o script 2× antes do primeiro disparo** (senão o 1º cron entrega o estado atual como novidade). Registrado em `concursos/<area>/VIGIA-CONCURSOS-<AREA>-CONFIG.md`.
7. **Fechar com prazos críticos** — listar os concursos ABERTOS com data de fechamento próxima, separados do que o vigia cobre.

## Pitfalls

- **Salário "teto" vs inicial:** portais citam o salário máximo/teto; o edital define vencimento inicial. Marcar valores como máximos/aproximados e sinalizar para conferir no edital.
- **Banca em definição:** órgão com IBFC/outra banca rescindida pode ter banca indefinida por meses — status "previsto" dura muito; o vigia é o que dá visibilidade, não a estimativa de data.
- **Registro de regra do usuário:** mudanças de critério (ex.: lotação, área) vão na ficha/dossiê com data e nas standing rules acima — não só na resposta do chat.

## File conventions

- Pastas e arquivos em português sem acento (`CONCURSO-PUBLICO`, não `CONCURSO-PÚBLICO`).
- `_INDEX.md` sempre na raiz de cada área — é o mapa de descoberta para sessões futuras.
