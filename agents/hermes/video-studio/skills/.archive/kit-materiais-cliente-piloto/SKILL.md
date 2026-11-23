---
name: kit-materiais-cliente-piloto
description: "Materiais do TimeAutomático para cliente-piloto."
---

# Kit de Materiais — Cliente-Piloto (TimeAutomático)

## Overview
Pipeline validado para produzir o pacote completo de um cliente-piloto do projeto
TimeAutomático (`~/projetos/hermes-as-service/`): ficha de diagnóstico, apresentação
setorial (9 slides), infográfico de 1 página, 4 áudios, roteiros, kit de envio e
distribuição (GitHub + Google Drive + email). Cada frente/segmento recebe materiais
SEPARADOS — Igor decide explicitamente o que mostrar (ex.: para o Augusto Nalin,
começar só pela frente pessoal/política, nunca empilhar áreas).

## Regras do Igor (obrigatórias)
- Sempre pt-BR; checar plural e nome correto de empresa (ex.: "DGM Eletro", "QUATRO FRENTES"). Rodar auditoria visual antes de entregar — Igor rejeita texto fora de caixa, cortes e erros de português.
- Nome de arquivos: `AAAAMMDD_TIPO-CLIENTE-CONTEXTO-TIMEAUTOMATICO.{pptx,pdf}`.
- NÃO exibir credenciais/tokens em nenhum material; rodar `scripts/auditar_seguranca_projeto.py` antes de commit.
- Materiais comerciais NUNCA citam parentesco (ex.: "primo do Igor") nem política partidária além do que Igor autorizar.
- Cada cliente-piloto = ficha individual + deck + infográfico + 4 áudios + kit. Nada fica "só no deck geral".

## Pipeline (ordem validada)
1. **Ficha**: `templates/FICHA-DIAGNOSTICO-PRESENCIAL.md` → salvar em `05-execucao-clientes/`.
2. **Deck setorial (9 slides)**: script python-pptx com `python3.12` (o python3 3.11 do sistema NÃO tem python-pptx). Copiar helpers do script de referência `07-apresentacoes/scripts/gerar_apresentacao_nalin_quatro_frentes.py` (cores NAVY #081223, CYAN #1FD3C4, BLUE #3B82F6, GOLD, fonte Aptos, 11×8.5in; funções `rrect/txt/bullets`).
3. **PDF**: `libreoffice --headless --convert-to pdf --outdir 07-apresentacoes <pptx>`.
4. **Auditoria visual**: `pdftoppm -png -r 50-80` → `montage -tile 3x3 -geometry ...` → `vision_analyze` pedindo problemas concretos por slide. Corrigir e reaudit (2ª rodada é comum; a 1ª costuma pegar colisão de rótulos e cartões cortados na borda).
5. **Infográfico 1 página**: mesmo pipeline; cuidado com rótulo colidindo com bullets e último cartão cortado (margem direita).
6. **Áudios**: 4 roteiros em `06-audios-salvos/20260904_ROTEIROS-<CLIENTE>.md` → `text_to_speech` provider `piper`, speed 0.96, output `.ogg` nomeado `20260904_<CLIENTE>-0N-TEMA.ogg`. Validar integridade com `ffprobe`.
7. **Kit**: `08-kits-envio/<cliente>/MENSAGEM-E-ORDEM-DE-ENVIO.md` (mensagem WhatsApp em bloco de código, quebras de linha curtas) + copiar PDF do deck, infográfico e áudios 1 e 3 (2 e 4 são reservados).
8. **Emails por cliente**: ver Pitfalls abaixo.
9. **Sync**: auditoria de segurança → `git add -A && git commit && git push` → `rsync -a --delete --exclude='.git/' --exclude='__pycache__/' --exclude='*.pyc' ./ <drive>` → conferir SHA-256 origem×drive (0 divergentes). Atualizar `01-projeto/AUDITORIA-SEGURANCA.md` (append-only) e `~/clawd/PEDIDOS.md`.

## Pitfalls
- **Patch de script via heredoc**: reescrever o script inteiro com `write_file` quebra menos que patch incremental — e conferir que não gerou `função(...) = valor` (erro de patch mal aplicado).
- **Erros de português em títulos gerados**: revisar sempre "FRENTE/FRENTES", "TODAS AS FRENTES"; o vision_analyze deve receber a pergunta explicitamente pedindo checagem de plural e do nome da empresa.
- **Emails himalaya**: `himalaya message send` NÃO aceita flags — montar MIME com `email.mime` (From/To/Cc/Subject), salvar `.eml` e enviar `himalaya message send --account gmail-igor < arquivo.eml`. Confirmar na pasta Sent (`himalaya envelope list --folder Sent`). Anexos com MIMEApplication; anexar PDF+PPTX por cliente.
- **Delegação em lote**: `delegate_task` com `tasks` exige ≥2 itens; para 1 tarefa usar `goal`. Subagente roda com `python3.12`.
- **Sync do Drive é append de 1 comando rsync** — nunca esquecer de re-verificar SHA-256 após o rsync; "commit feito" não garante Drive sincronizado.
- **Deck de 10 slides antigo ≠ deck setorial de 9 slides** — manter os dois índices corretos em `07-apresentacoes/INDEX.md`.

## Referências
- `references/exemplo-email-himalaya.md` — molde MIME e ordem de envio validada (04/09/2026).
- Script de referência de layout: `07-apresentacoes/scripts/gerar_apresentacao_nalin_quatro_frentes.py` (no repo do projeto).
