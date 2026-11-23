---
name: direito-processual-tributario
description: "Use para gestão de processos judiciais, execuções fiscais municipais/estaduais/federais, defesa de sócios retirantes e minutas de Exceção de Pré-Executividade."
---

# Direito Processual, Empresarial e Tributário

## Overview

Skill para gestão jurídica de execuções fiscais, cobrança de dívida ativa, ilegitimidade passiva de sócios retirantes e elaboração de peças processuais e pareceres.

## Pastas e Arquivos Canônicos

| Caminho | Descrição |
|---|---|
| `~/MEGA/Documentos/legal_publico/processos/` | Pasta canônica para processos judiciais, certidões e minutas de petições |
| `~/MEGA/Documentos/legal_publico/processos/INDEX.md` | Índice consolidado de todos os processos judiciais ativos e arquivados |
| `~/MEGA/Documentos/legal_publico/banca_juridica/` | Acervo da Banca Jurídica Multiagente (Knowledge Base, pareceres e casos) |
| `~/MEGA/Documentos/TAREFAS.md` | Acompanhamento de prazos e diligências processuais |

## Estratégia Jurídica — Sócio Retirante em Execução Fiscal

Quando houver execução fiscal proposta contra empresa e sócio que já se retirou da sociedade:

### 1. Prova Pré-Constituída (JUCERJA)
* Obter a **Certidão de Inteiro Teor** da Junta Comercial comprovando a data exata do arquivamento da alteração contratual com a cessão de cotas.
* O arquivamento perante a Junta Comercial confere **eficácia erga omnes** perante terceiros e Fazenda Pública (**Art. 36 da Lei nº 8.934/1994**).

### 2. Limite Temporal de Responsabilidade (Código Civil)
* Conforme os **Arts. 1.003, parágrafo único, e 1.032 do Código Civil**, a responsabilidade do sócio retirante pelas obrigações sociais encerra-se em definitivo **2 (dois) anos após a averbação na Junta Comercial**.
* Débitos gerados ou cobrados após esse biênio decadencial não podem ser imputados ao ex-sócio.

### 3. Via Processual Adequada — Exceção de Pré-Executividade
* Fundamento: **Súmula nº 393 do STJ**.
* Não exige garantia do juízo ou penhora de bens (cabível de plano quando demonstrada por prova documental pré-constituída).
* Pedidos essenciais:
  1. Acolhimento da exceção;
  2. Reconhecimento da ilegitimidade passiva *ad causam*;
  3. Exclusão imediata do executado do polo passivo e baixa em registros de distribuição;
  4. Fixação de honorários advocatícios sucumbenciais em desfavor da Fazenda Pública (**Art. 85 do CPC**).

### 4. Envio a Advogado Constituído e Geração de PDF
* Consultar a referência detalhada em `references/protocolo-envio-advogados.md`.
* **Geração de Pareceres e Peças em PDF:**
  * Compilar o parecer consolidado e/ou minuta via Markdown para HTML/PDF usando `pandoc` + `wkhtmltopdf --enable-local-file-access --page-size A4 --margin-top 20mm --margin-bottom 20mm --margin-left 20mm --margin-right 20mm --footer-right 'Página [page] de [topage]'`.
  * Adicionar cabeçalho e tipografia forense limpa com CSS inline para renderização nítida.
* Quando Igor solicitar envio de dossiê para advogado:
  * Estruturar relatório executivo com número CNJ, juízo, partes, valor, histórico cronológico dos andamentos e fundamentação jurídica;
  * Incluir a minuta completa da petição;
  * Anexar a certidão da Junta Comercial (PDF) e o parecer formal gerado (PDF);
  * Solicitar confirmação expressa antes do disparo de e-mail via terminal.

## Pitfalls
* **Falta de Atualização Cadastral Municipal:** A omissão do sócio remanescente/administrador em comunicar a alteração à Fazenda Municipal não afasta a publicidade do registro público na Junta Comercial.
* **Processos Suspensos (Art. 40 da LEF):** Se o processo estiver suspenso após tentativas frustradas de citação postal, não há citação válida nem ordem de penhora imediata (SISBAJUD), mas a exclusão formal via Exceção de Pré-Executividade é necessária para evitar penhora futura de surpresa.
