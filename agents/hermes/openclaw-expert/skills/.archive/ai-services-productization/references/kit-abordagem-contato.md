# Kit de abordagem por contato (TimeAutomático) — fluxo validado 05/09/2026

## Fluxo passo a passo

1. **Identificar a pessoa**: áudio do Igor costuma ter nome gaguejado ("ego pimentel", "sudo da costa"). Confirmar nome exato com Igor (lista numerada de candidatos do LinkedIn) ANTES de pesquisar a fundo.
2. **Traçar perfil**: web_search (LinkedIn snippets, EFIRMA, notícias). Salvar em `~/MEGA/Documentos/pessoas_clientes/<slug>/PERFIL.md` com: quem é, cargos, empresas, dados societários, marcas do perfil (discursos públicos, depoimentos de colegas) e **ângulo para o TimeAutomático**.
3. **Deck**: subagente gera 9 slides via `uv run --with python-pptx` → PDF via `soffice --headless --convert-to pdf`. Auditoria visual: `pdftoppm` + `montage` + vision_analyze. Identidade: navy `#081223`, cyan `#1FD3C4`.
4. **Áudios TTS**: Piper pt-BR, um por etapa, em `~/projetos/hermes-as-service/05-execucao-clientes/audios/` nome `YYYYMMDD_<PESSOA>_<ETAPA>.ogg`.
5. **Mensagens WhatsApp**: `*_MENSAGENS-WHATSAPP.md` com ordem de envio; mensagens em bloco de código; frases curtas, uma ideia por linha.
6. **Commit + sync**: git em `~/projetos/hermes-as-service/` + rsync para `~/Insync/GoogleDrive/igorferreirabr/03_Dev_IA/ia_agentes/hermes-as-service/`.

## ⚠️ Regra do Igor para áudios de reaproximação (validada caso Tiago Braga Machado, 05/09)

Igor NÃO quer áudio em primeira pessoa fingindo ser ele ("aqui é o Igor"). Formato certo — **o Hermes fala em nome do Igor**:

1. Apresentação: "Meu nome é Hermes, sou o agente de IA do Igor"
2. O que faz para o Igor: finanças, fluxo de caixa, faturas, jurídico, agenda, treinos
3. Visão macro: **100+ agentes** — banca engenharia, banca saúde (13 especialistas médicos), 55 jurídicos, squad dev completa (PO, arquiteto, backend, frontend, QA, DevSecOps)
4. Últimas entregas conjuntas concretas (deck + áudios <1h, auditoria financeira com recálculo automático)
5. Contextualiza o contato: como Igor o conhece e o que achou (ex: "te encontrou na rua agora no bairro, voltou falando de você com entusiasmo danado")
6. Elogia trajetória do contato com FATOS reais (sócio, CTO, empresa de IA, SUS no caso Sofya)
7. Explica **Hermes como Serviço** (levar esse time de agentes a empresas menores)
8. Fecha com convite do Igor: quer saber da empresa/projetos e ouvir a leitura de mercado — nunca pitch de venda

Para parceiro comercial puro (não amigo/mentor), áudio pode seguir na "voz do Igor" — decidir caso a caso; em dúvida, perguntar.

## Tom

- Leve, direto, informal mas respeitoso; "mano"/"cara" só conforme a relação
- Nunca hypar ("imperdível", "oportunidade única"); sempre CTA leve (conversa de 30 min, trocar ideia)
- Para contatos técnicos/CTO: pedir OPINIÃO (leitura de mercado) em vez de vender — validado como abertura mais digna

## Pitfalls

- Delegation cria diretórios mas pode falhar em escrever os arquivos — sempre verificar no filesystem antes de confiar no report
- LinkedIn bloqueia consulta por IP de datacenter e web_extract falha (login wall) — usar web_search e filtrar snippets
- Usar a data do bloco [Agora] (sem rodar `date`) ao salvar nomes de arquivo com data
