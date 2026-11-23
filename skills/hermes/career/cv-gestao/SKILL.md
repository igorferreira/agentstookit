---
name: cv-gestao
description: Use quando Usuário pedir atualização ou PDF do currículo dele.
version: 1.0.0
author: Hermes
license: MIT
metadata:
  hermes:
    tags: [cv, curriculo, carreira, pdf]
    related_skills: [pdf, linkedin-optimization]
---

# Gestão do CV do Usuário (versões, atualização e PDF)

## Quando usar

Qualquer pedido de "meu CV", "currículo atualizado", "CV em PDF" ou criação de variação segmentada (arquiteto IA, Java sênior, open finance, seguros).

## Canon e versionamento

- Fonte canônica: `~/MEGA/Documentos/carreira/curriculos/` — arquivo principal `YYYY-MM-DD_CURRICULO-USUARIO-V<N>.md`; variações segmentadas por área em subpastas `arquiteto_ia/`, `java_senior/`, `open_finance/`, `seguros/` (cada uma com MD + DOCX + PDF próprios).
- **NUNCA edite um arquivo de versão antiga** — é histórico. Novo pedido de atualização = `cp` do V mais recente para um novo `YYYY-MM-DD_...-V<N+1>.md` e aplicar patches no novo arquivo.
- Pontos que SEMPRE precisam de revisão a cada atualização: datas dos cargos (incl. fim de vínculo real, nunca deixar "Presente" após desligamento), resumo executivo, seção de realizações (anos sem "presente"), competências de IA, e o rodapé "*Currículo atualizado em <mês>/<ano>.*".
- Bullos de cargos novos devem ancorar em artefatos reais (programas, apresentações, hackathons) — mesma fonte do canônico LinkedIn (`linkedin/2026-11-14_ATUALIZACAO-LINKEDIN-ENGENHARIA-AGENTES-HDI.md`); não inventar realizações.

## Renderização em PDF

Usar a skill `pdf`, referência `references/markdown-html-reports.md` (pandoc → HTML com CSS → headless Chrome → PDF).

- NÃO passe `--metadata title` no pandoc quando o MD já começa com H1 (o nome do Usuário) — gera o nome duas vezes no topo do PDF.
- Se não houver wkhtmltopdf/LaTeX instalado, usar o Chrome já em execução com `--remote-debugging-port` via CDP (`Page.printToPDF`; base64 em `result.data`; `Page.enable` antes de screenshot) — recipe completo na referência da skill pdf.
- Nome de saída: mesmo base do MD com `.pdf`, na mesma pasta `curriculos/`.

## Verificação obrigatória antes de entregar

1. `pdftotext` e conferir os marcadores da atualização (datas novas, termos novos — ex. "DevAI", "Novembro 2026") e que o nome aparece uma única vez no topo.
2. Screenshot visual da página 1 (visão) para conferir legibilidade e layout.
3. `pdfinfo` para contagem de páginas e tamanho (letter OK).

## Entrega

Enviar o PDF direto no chat com `MEDIA:/caminho/do/arquivo.pdf` (Usuário recebe como documento nativo). Não anexar em e-mail sem pedido explícito.
