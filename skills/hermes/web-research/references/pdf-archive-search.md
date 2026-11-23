---
title: Busca reproduzível em arquivos de PDFs
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [web-research, pdf, archives]
    related_skills: [web-research]
---

# Busca reproduzível em arquivos de PDFs

## When to Use

Use ao pesquisar em várias edições de uma revista, boletim ou acervo de documentos PDF, sobretudo quando uma conclusão depender de confirmar se o material pesquisável contém uma menção.

## Procedimento

1. **Delimite o corpus.** Abra o índice oficial do arquivo, liste todas as edições que cobrem o intervalo investigado e guarde cada URL direta. Registre também eventuais lacunas do arquivo; não escolha uma única edição e a trate como cobertura do ano inteiro.
2. **Baixe e valide cada PDF.** Prefira a fonte primária. Faça GET com User-Agent descritivo; registre URL final e status HTTP. Confirme assinatura `%PDF-` e tamanho não nulo antes de extrair. Quando usar `browser_exec`, obtenha o diretório persistente por `os.environ.get('BH_AGENT_WORKSPACE')` (ou pelo caminho de workspace exibido pelo tool); não presuma que existe uma variável Python `workspace` nem que variáveis Python sobrevivem entre chamadas. Mantenha arquivos temporários no workspace/scratch, não em `/tmp`.
3. **Extraia todos os números em lote.** Para PDFs com camada textual/OCR, rode `pdftotext -layout arquivo.pdf arquivo.txt` para cada item do manifesto; preserve o código de retorno e confirme que o texto foi produzido. Prefira executar download e extração num único comando de terminal (`curl` em loop + `pdftotext` em loop + `ls -la` final): o terminal devolve tamanho de arquivo, código de saída e contagens completos, enquanto chamadas que rodam Python/browser intermediário truncam a saída em resumos opacos e a rodada acaba sem nada verificável — se uma tentativa anterior via ferramenta intermediária só retornou tamanhos/`1 lines output`, refaça no terminal em vez de insistir na mesma via. Confirme tamanho real por `ls -la` e produza contagens por `grep -c`. Automatize a lista em vez de processar uma edição por chamada. `pdftotext` não executa OCR: se o texto estiver vazio, incompleto ou claramente desordenado, aplique OCR/inspeção visual às páginas relevantes antes de interpretar qualquer ausência.
4. **Valide a extração com nomes conhecidos antes de interpretar resultado negativo.** Antes de concluir que "não há menção", `grep -ic` no corpus nomes de pessoas/entidades notoriamente presentes no domínio pesquisado (pilotos famosos, autores do periódico, termos genéricos do esporte). Se esses nomes aparecem, o OCR/camada textual captura nomes quando existem e a busca negativa ganha peso; se nada deles aparece, a extração está fraca e a ausência não é interpretável. Além disso, confirme quantas edições o índice oficial realmente lista — lacunas do acervo (meses ausentes) são a explicação alternativa mais provável para um negativo.
5. **Localize variantes, depois confira os acertos.** Defina termos literais e variantes de grafia, transliteração, localização e nomes. Conte e extraia contexto por arquivo, sem despejar transcrições integrais. Abra a página original do PDF para verificar acertos relevantes, distinguir coincidência lexical de menção ao evento e registrar a página e o trecho exatos.
6. **Faça uma afirmação negativa estreita.** Se nada aparecer, escreva apenas: “não localizada nos textos extraídos das edições X–Y com os termos consultados”. Busca/OCR sem acerto não demonstra que um evento, pessoa ou artigo não existiu; páginas escaneadas, OCR, grafias inesperadas e lacunas do arquivo podem produzir falsos negativos — cite sempre quantas edições o índice oficial lista e quais faltam.
6. **Registre a trilha.** No registro de buscas, inclua índice da fonte, URLs de todas as edições, intervalo coberto, data de consulta, método (`pdftotext -layout` e/ou OCR), termos efetivamente consultados, resultado, limitações e próximo passo. No inventário de fontes, marque a busca negativa como corpus consultado/metodologia, não como prova positiva de inexistência. No dossiê, preserve a lacuna substantiva e não transforme o silêncio do arquivo em conclusão factual.

## Exemplo de comando

```bash
pdftotext -layout edicao.pdf edicao.txt
```

Para muitas edições, execute esse comando via um loop Python sobre uma lista explícita de URLs/arquivos e, numa segunda passada, localize todas as variantes nos `.txt`, retornando apenas nome do arquivo e trechos ao redor dos acertos. Um resultado vazio só é interpretável depois de confirmar que todas as edições previstas foram baixadas e que a extração textual foi adequada.