# Sessão 04/09/2026 — Kits por cliente, parceiros e lições de produção

## Contexto
Sprint de fechamento do TimeAutomático: 8 clientes-piloto completos, deck de parceiro técnico (Fernando Veronez), kit de parceiro estratégico (Rafael Alcemar/Webdec), proposta de sociedade com Bernardo, e refoco do deck do Augusto Nalin.

## Padrão de kit cliente-piloto validado (kit completo)
Cada piloto recebe:
1. Ficha em `05-execucao-clientes/NOME-CLIENTE.md` (dados públicos + dores como hipóteses + limites de segurança)
2. Deck setorial 8-9 slides PPTX+PDF (script python-pptx em `07-apresentacoes/scripts/`)
3. Infográfico 1 página PPTX+PDF
4. Roteiros de 4 áudios em `06-audios-salvos/20260904_ROTEIROS-NOME.md`
5. 4 áudios TTS Piper pt-BR (speed 0.96, tom executivo/amigável)
6. Kit em `08-kits-envio/nome/MENSAGEM-E-ORDEM-DE-ENVIO.md` — mensagem WhatsApp em bloco de código + ordem de envio + regras de segurança

## Fluxo de produção validado (rápido e auditável)
1. Escrever script python-pptx (usar `python3.12` — o 3.11 do sistema não tem pptx; Pyright reclama dos imports, ignorar)
2. Rodar script → LibreOffice headless converte PPTX→PDF
3. Auditoria visual OBRIGATÓRIA: `pdftoppm -png -r 50` + `montage -tile 4x2` → vision_analyze (uma chamada por deck; pegar plurais e erros de pt-BR — já pegou "QUATRO FRENTE" e "DM ELETRO"→"DGM ELETRO")
4. Corrigir script, regenerar, reaudit
5. Commit + rsync Drive + verificação SHA-256 (contagem origem=drive, divergentes=0)

## Delegação de kits em background (delegate_task) — lições
- Subagentes de geração de kit FALHARAM SILENCIOSAMENTE 2x: status "completed" mas zero arquivos criados (leu referências e parou). O log live mostra `final | summary: All` sem entregas.
- **Lição:** verificar SEMPRE os arquivos esperados após delegation de geração (ls dos caminhos esperados). Se faltarem, gerar direto no turno principal em vez de re-despachar — o fluxo direto (script + libreoffice + montage + vision) levou ~3 min por deck.
- Vale re-despachar só para tarefas paralelas independentes; para sequência única, fazer direto.

## Perfis por dados públicos (web_search) — técnica
- Buscar `"Nome" + empresa` e `"Nome" + LinkedIn`: LinkedIn retorna cargo, histórico e autodeclarações; sites de CNPJ (juridicoonline etc.) dão QSA/data de entrada; Gust/AeroLeads dão contatos.
- Converter achados em: tabela de dados confirmados + "dores mapeadas (hipóteses a confirmar no diagnóstico)" + ângulo de abordagem + limites de segurança. Nunca afirmar dores como fato.
- Casos: Mariana Nalin (A Credit, Cartão Nalin 45% das vendas — dado de podcast), Rafael Alcemar (Webdec, +5.000 empresas — dado do LinkedIn), Vinicius Tavares (Veiga de Almeida, professor desde 2011 — marcado como "provável, confirmar").

## Limites de segurança por relacionamento (padrão que funcionou)
- Parentesco/amizade NUNCA citado em material comercial (Bernardo primo, Mariana/Augusto Nalin família, Alcemar amigo) — só na ficha interna
- Segmentos sensíveis: fintech (não tocar em dados de clientes do cartão, não oferecer automação de cobrança de cara), educacional (LGPD de alunos), motorista (sem integração Uber/99, sem senhas)
- Proposta societária separada do material comercial (Bernardo); para parceiros, só em 2ª rodada após demonstrar interesse
- Envelope para parceiro técnico (Veronez) e parceiro estratégico (Alcemar): deck de papel + arquitetura + próximos passos, tom de colega respeitando senioridade

## Deck por frente vs deck geral (correção do Igor)
Igor corrigiu: "a apresentação é por área, não pode apresentar todas as áreas" — para cliente multi-negócio, a PORTA DE ENTRADA é um deck focado na frente escolhida (Nalin: pessoal/política), e os decks das outras frentes ficam reservados para depois da conversão. Gerar ambos (geral 4 frentes + individual por frente) e usar o focado primeiro.

## Entrega por chat (padrão)
PDFs e áudios entregues no Telegram com MEDIA: caminho absoluto. Subagente pode entregar errado — sempre verificar arquivo existe antes do MEDIA.

## Mensagem WhatsApp multi-partes para destinatário viajando (Alcemar)
- Quebrar em partes curtas, ordem: mensagem de abertura → logo (claro+escuro) → deck 1 → deck 2 → áudios → "responde quando puder"
- Áudio de abertura TTS cobre resumo completo + tese de parceria + convite de 30 min "quando voltar"
