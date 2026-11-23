# Case TimeAutomático — aprendizados de execução (set/2026)

Registro condensado de técnicas e correções feitas durante a construção dos materiais. É contexto específico da sessão, não regra universal.

## Stack validada de geração de materiais

- **PPTX via python-pptx** (python3.12). Paleta TimeAutomático: azul-noite `#081223` (fundo), ciano `#1FD3C4`, azul `#3B82F6`, verde `#22C55E`, laranja `#F97316`, dourado `#EAB308` (slide de sociedade/oferta pessoal), vermelho `#EF4444` (rótulo de problemas), cinza-azulado `#0E1F35` e `#1C2A3D` (caixas).
- **PDF via LibreOffice headless**: `libreoffice --headless --convert-to pdf --outdir <dir> arquivo.pptx`. Sempre em diretório de saída separado.
- **Auditoria visual**: `pdftoppm -png -r 60..85` + `montage -tile NxM -geometry LxA+4+4` para montar painel com todos os slides, depois inspecionar o painel com visão. Duas rodadas: gerar → auditar → corrigir offsets → auditar de novo. A primeira rodada quase sempre encontra cortes e sobreposições.
- **Verificação de idioma nos PDFs**: `pdftotext` + busca por termos inequívocos de espanhol (usted, entonces, creacion, configuracion, puede, nuestro...). Palavras ambíguas (como "real", "no") geram falso positivo — usar só termos inequívocos.

## Armadilhas de layout que causaram rejeição (fixadas em números)

- Título a 0.9" com stripe decorativo em cima → encosta no cabeçalho. Descer título para ~1.0".
- Rótulo de seção (ex.: "PROBLEMAS ENCONTRADOS") na mesma faixa Y do primeiro bullet → colide. Rótulo ~0.2–0.3" acima dos bullets.
- Linha de cards: `x = inicio + i * largura_passo` sem conferir o último card → corta na borda. Calcular: total_disponivel = largura_util - (n-1)*passo, card = total_disponivel / n.
- Ícone grande em painel lateral: centralizar no painel inteiro (x=painel_x+margem, y=centro vertical), não "no meio do slide".
- Caixa de texto precisa de altura para N bullets com espaço; bullet_list com `space_after=Pt(3)` e fonte 10–11pt dentro de caixas de ~1.8".

## Erro de escrita de código a evitar (ocorreu 2x)

Ao gerar scripts de apresentação com `write_file`, strings de dicionário ficaram malformadas (`'problemas:[...'` sem dois-pontos de fechamento) e um patch subsequente corrompeu uma linha (`txt(...) = OUT / ...`). Lições:
- Reler o arquivo gerado (ou confiar no lint do write_file) antes de executar.
- Patch com old_string/new_string pode capturar trecho errado se a âncora for curta — incluir contexto suficiente e reler o diff retornado.
- Estrutura de tuplas SLIDES com itens de tamanhos diferentes (3 ou 4 elementos) → desempacotar com indexação condicional, não `for a,b,c,d in lista`.

## Pipeline de e-mail em lote (himalaya)

- Um `.eml` por destinatário: `MIMEMultipart` + `MIMEText` (plain, utf-8) + `MIMEApplication` para anexos com `Content-Disposition: attachment; filename="..."`.
- Enviar com `himalaya message send --account gmail-igor < arquivo.eml`.
- Confirmar entrega lendo `himalaya envelope list --account gmail-igor --folder Sent --page-size N` e procurando os assuntos.
- **Anti-duplicação**: 1 envio = 1 registro (log canônico EMAIL_ENVIADOS.md quando for caso sensível); conferir Para/Cc antes de disparar.
- Lote de ~7 emails pequenos + 1 grande (2.5 MB, 10 anexos) passou sem o timeout que ~7 MB causava. Manter emails abaixo de ~3 MB; acima disso, dividir.

## Kit de cliente-piloto — composição canônica

Cada cliente-piloto tem 4 materiais, sempre os quatro:
1. ficha de diagnóstico presencial (template único em `templates/FICHA-DIAGNOSTICO-PRESENCIAL.md`, preenchido na reunião, nunca enviado antes);
2. áudio (série de 4: apresentação, possibilidades, piloto, próximo passo — roteiro + OGG, duração ~15-35s cada);
3. apresentação setorial de 9 slides (PPTX + PDF);
4. infográfico curto de 1 página (PPTX + PDF).
Mais kit de envio: mensagem WhatsApp pronta (frases curtas, bloco de código) + ordem de envio + materiais reservados + limites comunicados.

## Ficha de diagnóstico presencial

Template com 7 seções: dados básicos, problemas mapeados (prioridade 🔴🟡🟢), sistemas atuais, limites inegociáveis (o que NÃO automatizar, o que não sai do ambiente, senhas), metas/expectativas, disponibilidade para o piloto, observações + assinatura. Uso interno — preencher na conversa.

## Proposta de sociedade em camadas

- **Formal (4 páginas)**: apresentação do negócio, problema, mercado, pacotes/preços, papéis dos sócios, duas opções de divisão (societária 40/25/25/10 vs. split de receita 50/35/15), cláusulas essenciais, minibiografias profissionais, próximos passos. Marcar como "minuta para discussão — não constitui contrato".
- **Curta (5 slides)**: capa, ideia, como cobrar, proposta de sociedade (barra dourada destacando que é oferta pessoal), próximo passo. Para WhatsApp.
- Gerar PDF de MD com `pandoc --standalone` → `wkhtmltopdf --no-background`; auditar títulos órfãos e páginas quase vazias.
- Minibiografias: construir a partir do LinkedIn público (nunca inventar conquistas); no caso de executivo de grandes empresas, descrever porte (ex.: "lidera organização de 60+ pessoas") sem dados não públicos.

## Governança aplicada

- Auditor automático de segurança (`auditar_seguranca_projeto.py`) antes de cada commit/sync/envio. Falsos positivos conhecidos: documentos que DESCREVEM os padrões (rotinas de segurança, o próprio auditor).
- Sync GitHub + Google Drive com verificação SHA-256 de manifesto completo (origem vs. Drive), excluindo .git/__pycache__/.pyc.
- Email enviado = registrado no PEDIDOS.md com hora; cada pedido do Igor vira linha na tabela de fila.
- Parentesco (ex.: primo) registrado só na ficha interna, nunca em material comercial.
- Verbas/benefícios de terceiros: apresentar como hipótese até confirmação (ex.: "49 lojas" só depois de validar no CNPJ público).
