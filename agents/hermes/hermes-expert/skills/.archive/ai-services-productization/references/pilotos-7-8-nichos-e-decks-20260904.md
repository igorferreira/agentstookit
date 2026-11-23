# TimeAutomático — lições da sessão 04/09/2026 (clientes-piloto 7 e 8, decks, validações)

## Perfil de cliente antes de gerar material

- Pesquisar a pessoa na web ANTES de gerar o deck e salvar o perfil em `05-execucao-clientes/<NOME>-<SEGMENTO>.md` (ex.: `MARIANA-NALIN-ACREDIT-FINTECH.md`). A pesquisa frequentemente revela nicho correto: Mariana Nalin não é "área de cartões da Nalin" genérica — é Diretora Executiva da **A Credit Administradora de Cartões** (emissora do Cartão Nalin, 45% das vendas da rede, 96% de ativação). Isso muda o vocabulário do deck (crédito privado, LGPD, SAC multicanal).
- Nichos novos abertos nesta sessão: educação jurídica (Vinicius Tavares, Veiga de Almeida Cabo Frio) e fintech/credito privado (Mariana Nalin).
- Quando o usuário diz "X tem potencial para N assinaturas", gerar deck ÚNICO de N frentes + (depois de validado) decks INDIVIDUAIS por frente — o usuário opera em camadas: primeiro o geral, depois o específico da frente que interessar.
- CORREÇÃO IMPORTANTE: para o Augusto Nalin, a porta de entrada é SÓ a frente pessoal/política — "não pode apresentar todas as áreas". Gerar deck dedicado à frente escolhida, sem mencionar as outras. Cada frente tem deck próprio pronto (`20260904_APRESENTACAO-NALIN-F1..F4...`).
- Nomes de empresa: confirmar grafia na web antes de gerar material. O usuário corrigiu "DM Eletro" → **DGM Eletro**.

## Geração de decks (padrão validado)

- Script python-pptx com helpers `rrect/txt/bullets` (rotonded rect, textbox, bullets), cores NAVY #081223, CYAN #1FD3C4, BLUE #3B82F6, GOLD #EAB308, GREEN #22C55E, fonte Aptos, 11×8.5in. Rodar com `python3.12` (o python3 do sistema não tem python-pptx).
- Converter para PDF via `libreoffice --headless --convert-to pdf`.
- Auditoria visual OBRIGATÓRIA: `pdftoppm -png -r 50` + `montage -tile 4x2` + vision_analyze. Pegou nesta sessão: "QUATRO FRENTE" (plural errado), "SEGURANÇA EM TODAS AS FRENTE". Corrigir no script e regenerar; re-auditar.
- Deck por área: 8-9 slides (capa, dor, solução 3 colunas, prática, diferencial/resultado, segurança, piloto+preço, fechamento com contato Igor +55 21 96416-7952 / igorferreirabr@gmail.com).
- Para prospects financeiros: LGPD/sigilo apresentado como DIFERENCIAL (slide dourado), nunca como limitação; nunca mencionar automação de cobrança.

## Falha de subagente silencioso

- delegate_task pode retornar `status=completed` com resumo vazio sem ter gerado NENHUM arquivo. SEMPRE verificar a existência dos arquivos esperados após o retorno (ls/contagem de páginas via pdfinfo). Se vazio, gerar diretamente — não re-dispatch cegamente.

## Fluxo pós-geração (checklist)

1. copiar PPTX+PDF para `08-kits-envio/<cliente>/`
2. git add/commit/push
3. rsync para `~/Insync/GoogleDrive/igorferreirabr/03_Dev_IA/ia_agentes/hermes-as-service/`
4. verificação SHA-256 origem×drive (deve ser 0 divergentes)
5. registrar em PEDIDOS.md (~/clawd) e, se cliente novo, no CADASTRO-CLIENTES-PILOTO.md + memory

## Emails com apresentações (padrão validado)

- Um email por cliente para igorferreirabr@gmail.com com 4 anexos: deck PDF+PPTX e infográfico PDF+PPTX. Montar via Python email.mime, salvar .eml em /tmp, enviar com `himalaya message send --account gmail-igor < /tmp/x.eml`, confirmar com `himalaya envelope list --folder Sent`.
- Emails com ~7MB/15 anexos travam o SMTP do himalaya — quebrar em lotes pequenos (~5 anexos).

## Materiais de sociedade (Bernardo)

- Separar material comercial (deck setorial) de material de sociedade (proposta de participação) — são conversas diferentes. Gerada proposta formal 4 páginas (minuta, `03-precos-pacotes/PROPOSTA-SOCIEDADE-BERNARDO.pdf`) e versão curta 5 slides para WhatsApp. Divisões propostas: societária 40/25/25/10 ou receita 50/35/15; braço técnico Igor + Fernando Veronez (HDI), comercial/jurídico Bernardo (Rio e SP).
- Minibiografias dos sócios baseadas apenas em dados públicos (LinkedIn), marcadas como minuta.
