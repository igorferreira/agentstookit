# Dossiê / pacote de leitura em PDF (padrão do Igor)

Convenção canônica (também em ~/MEGA/Regras/documentos_e_arquivos.md): o Markdown é a fonte da verdade no MEGA; cada dossiê gera SEMPRE 2 PDFs do mesmo conteúdo — versão PADRÃO e versão CELULAR (fonte maior). Ambos com capa de leitura, outline/bookmarks navegáveis (h1/h2/h3), sem título órfão nem quebra de página indevida, tabelas dentro da margem, bloco azul no topo (como ler + dicas de memorização + ⭐ pontos-chave) e adendo no fim.

## Pipeline (ordem)

1. **Canônico:** escrever/revisar o MD na pasta canônica do tema (ex.: MEGA/Documentos/carreira/oportunidades/<tema>/). Nunca editar o PDF direto.
2. **Builder:** gerador com lista de dossiês + TOPOS (bloco topo por documento) + CSS + TPL HTML; gera HTML por doc e chama o renderer. Script de referência do Igor: `~/.hermes/cache/scratch/build_pdfs_leitura.py` (arg `celular` = versão com fonte maior; ATENÇÃO: scratch expira em 24h — se sumiu, recriar a partir desta receita).
3. **Renderer:** weasyprint CLI: `/usr/local/bin/python3.12 -m weasyprint in.html out.pdf`. O weasyprint gera o outline/bookmarks AUTOMATICAMENTE a partir de h1/h2/h3 — headless Chrome (`--print-to-pdf`) NÃO gera outline; usar Chrome só quando outline não importar.
4. **Renomear por nome EXATO** (mapa old→new em Python) com rótulo `DOSSIE` + numeração de ordem de leitura (`01_DOSSIE-INDICE-PACOTE`, `02_`…). O índice do pacote é o 01 e sua tabela lista a ordem + tempo de leitura por documento.
5. **Réplica:** `cp -r` das pastas de PDF para `~/Insync/GoogleDrive/igorferreira08/Documentos/<pasta>/` (Insync sobe pro Drive sozinho). Ao atualizar dossiê, regenerar as 2 versões E re-replicar (a réplica não sincroniza sozinha).
6. **Verificação:** `pdftoppm -png -r 55 -f 1 -l 2 x.pdf _pv/` + inspeção visual da capa e da página 2 (documento começa na 2); outline conferido com pypdf no python3.12 (`r.outline`, contar títulos, conferir que NÃO começa pelos títulos da capa).

## Pitfalls (imperativos)

- **Capa: NUNCA usar h2/h3 nos blocos da capa** (como-ler, memorização, ⭐) — o weasyprint transforma todo heading em bookmark e o outline abre poluído com os títulos da capa. Usar `<div class="...">` estilizado com a mesma aparência; reservar h1/h2/h3 para o documento real (adendo pode ter h2, é navegação útil).
- **Renomeação/duplicatas: aplicar o mapa de renome por nome exato, nunca por wildcard** (`rm -f 0[2-9]_[A-Z-]*.pdf`) — padrões de caractere casam TANTO os nomes antigos quanto os novos (ex.: `02_CRONOGRAMA` e `02_DOSSIE-CRONOGRAMA`) e apagam a rodada boa junto. Depois de renomear, conferir a contagem de arquivos antes de replicar.
- **CSS de fonte da versão celular: trocar por substituição exata de string no CSS com assert** (`assert a in CSS` antes de cada replace) — replace silencioso que falha gera "versão celular" igual à padrão sem erro aparente. Valores validados do Igor: corpo 13,5pt/lh 1,62; h1 19,5pt; h2 15,5pt; h3 13,5pt; tabela 10,5pt; capa-título 27pt.
- **Anti-título-órfão:** `page-break-after: avoid` em h1/h2/h3; tabelas `width:100%; table-layout:fixed` + `overflow-wrap:anywhere` nas células; capa com `page-break-after: always` e o documento começa na página 2.
- **Réplica não subiu?** Verificar se os arquivos estão no diretório local do Insync; se estão e nada sobe em minutos, o Insync travou: matar o PID (`pgrep -af insync start`), reiniciar com `DISPLAY=:0 /usr/lib/insync/insync start --no-daemon` (sessão background) — ele re-escaneia tudo no boot. `~/.config/Insync/settings.db` dá 'database is locked' com o app de pé (normal); `out.txt` só tem erros de notification-daemon (inofensivos). Última suspeita: sync seletivo com a pasta desmarcada nas preferências do app.
- **Locais que o Igor procura:** além da pasta canônica, manter cópias dos PDFs nos pontos de navegação dele (pasta do tema no MEGA e no Drive) — ele navega por tema, não por `_Analises/`.
