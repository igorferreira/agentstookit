---
name: planejamento-financeiro
description: "Use when Igor asks about financeiro tasks — modelagem de cenários, projeções, parcelamentos, cheque especial, registro de faturas/comprovantes, cenários de pagamento, matriz de cartões, dossiês para advogado, negociação de dívidas."
version: 1.0.0
---

# Planejamento Financeiro — Cenários e Projeções

Skill para modelagem de cenários financeiros complexos: múltiplos cartões, parcelamentos futuros, CDB, cheque especial, projeções de longo prazo e dossiês para advogados.

## Triggers

- "Financeiro" como prefixo de mensagem
- "cenário", "projeção", "planilha", "orçamento"
- "parcelamento", "parcelas futuras"
- "negociar dívida", "advogado", "dossiê"
- "cheque especial", "estourou a conta"

## Workflow

### 0. ⚠️ ANTE S de modelar: confirmar lista de mantidos vs negociação

**Este é o passo em que mais se erra.** A lista de cartões muda DURANTE a sessão — o usuário decide manter um que era pra negociar, paga um com limite de outro, absorve cartão novo. Se você modelar com a lista errada, TODO o fluxo de caixa fica errado.

**Antes de QUALQUER projeção:**
- Ler `~/MEGA/Comprovantes/ENDIVIDAMENTO.md` (seções 3 e 4) para a classificação vigente — é a fonte da verdade, criada exatamente para não depender da memória da sessão.
- Confirmar com o usuário só se o `ENDIVIDAMENTO.md` estiver desatualizado (checar a data de "Última atualização" no topo) ou se houver uma mudança recente que ainda não foi registrada lá.
- Tratar 3 categorias separadamente: **ATIVOS/MANTIDOS** (pagar), **NEGOCIAÇÃO** (não pagar), **ZERADOS** (sem dívida — seção 7 do `ENDIVIDAMENTO.md`)
- Se houver cartão com emissor desconhecido (ex: Méliuz), **buscar na internet** antes de classificar
- **Sempre que um cartão mudar de categoria, atualizar `ENDIVIDAMENTO.md` (seções 1, 3, 4) e `CONTROLES.md` junto** — não deixar a mudança só na sessão atual, ou a próxima sessão volta a perguntar do zero.

### 1. Mapear TODOS os compromissos

Antes de qualquer cenário:
- Listar todos os cartões com fatura atual, vencimento e emissor
- **Perguntar sobre parcelamentos futuros de CADA cartão.** Não assumir que a fatura atual é o único custo.
- Parcelamentos ocultos são o maior risco — insistir com o usuário até ter todos mapeados.
- **Saldo em conta corrente é recurso.** Se o usuário tem dinheiro na conta do Itaú, usar para pagar cartões Itaú primeiro — libera o CDB.

### 2. Descobrir parcelamentos futuros

- Pedir prints dos apps de cartão (gráfico de "próximas faturas" ou "parcelamentos")
- Extrair com OCR (pytesseract). Em modo escuro, **inverter a imagem** antes: `ImageOps.invert(img.convert('RGB')).convert('L')`
- Se OCR falhar (comum em apps dark mode), pedir para o usuário ditar os valores
- Montar matriz: linhas = meses, colunas = cartões
- Ver `references/dark-mode-ocr.md` para técnicas de extração

### 3. Modelar cenários

Para cada cenário:
- **Caixa disponível:** CDB + conta corrente + renda mensal
- **Pagamentos imediatos:** faturas do mês atual
- **Parcelamentos futuros:** da matriz
- **Renda recorrente:** CLT líquido + VALLO + outros
- **Compromissos fixos:** empréstimos, custo de vida
- **Eventos sazonais:** 13º (1ª parcela nov, 2ª parcela dez), dissídio (confirmar data-base)

### 4. ⚠️ PITFALL: Cheque especial

**SEMPRE incluir juros do cheque especial em projeções com saldo negativo.**

- Nubank: ~8% a.m. sobre o saldo devedor
- O juro composto do OD transforma um déficit pequeno em bola de neve
- Projetar mês a mês: `OD_acumulado = OD_anterior + déficit_mensal + juros(OD_anterior * 0.08)`
- Mostrar explicitamente: "Sem OD" vs "Com OD" para o usuário ver o impacto

### 5. Projeção de longo prazo

- **NUNCA incluir aumentos de renda não confirmados.** Dissídio só entra na projeção depois de confirmada a data-base e o percentual.
- Ser conservador: usar a renda recorrente comprovada, sem bônus ou pontuais
- Projetar até o marco relevante (ex: fim dos parcelamentos, fim dos 280 dias de negociação)
- Incluir 13º nas datas legais (1ª parcela até 30/nov, 2ª até 20/dez)
- Empréstimos SAC: a parcela diminui ~R$ 40/mês (recalcular amortização × taxa)

### 6. Formato de entrega

Para cada cenário, entregar:
1. **Markdown:** visão completa com tabelas
2. **Excel (openpyxl):** uma aba por cenário + aba comparativo
3. **Passo a passo:** playbook de execução com data, app, valor, saldo após cada pagamento
4. **PDF:** para enviar a terceiros (advogado, contador)

### 7. Dossiê para advogado

**Sempre fazer due diligence ANTES de recomendar qualquer escritório.** Ver `references/due-diligence-advogado.md` para o checklist completo.

**⚠️ PITFALL: Confirmar estrutura COMPLETA de honorários.** Advogados frequentemente mencionam só uma dimensão e "esquecem" as outras. Sempre confirmar as 3:

| Dimensão | Perguntar |
|---|---|
| **Entrada** | Valor à vista? Parcelamento? |
| **Mensalidade** | Cobra valor fixo mensal? Quanto? |
| **Sucesso** | % sobre redução? Tem cap (teto máximo)? |

Projetar custo total por tempo: `Entrada + (Mensalidade × Meses) + (% × Redução)`. Comparar escritórios com projeção de 3/6/12/24 meses.

Formato canônico do dossiê (ver template completo em `references/due-diligence-advogado.md`):
1. Identificação (OAB, CNPJ, endereço)
2. Perfil do advogado (processos, experiência, adversários)
3. Resultados apresentados (com alerta de autodeclaração)
4. Alertas e riscos (Reclame Aqui, OAB, inconsistências)
5. Comparação de honorários (se 2+ escritórios)
6. Perguntas essenciais antes de fechar
7. Proposta de honorários detalhada

Salvar em `~/MEGA/Documentos/Dividas/dossie-NOME-snakecase.md`.

## Fluxo de caixa detalhado com contas de consumo

Quando o usuário pedir projeção de fluxo de caixa incluindo contas de consumo (luz, gás) que serão pagas no crédito:

1. **Identificar contas atrasadas**: verificar último pagamento registrado e meses em aberto. Para Light (~R$ 771/mês) e Naturgy (~R$ 110/mês), usar histórico recente como estimativa quando a fatura não estiver disponível.
2. **Confirmar com o usuário**: quantos meses atrasados e qual cartão (Signature ou Passaí).
3. **Incluir como despesa recorrente no cartão escolhido**: a partir do mês seguinte, adicionar ~R$ 881/mês (luz + gás) na fatura do cartão indicado.
4. **Projetar mês a mês**: renda (CLT + VALLO) → menos faturas dos cartões → menos C6 → saldo. Incluir dissídio e 13º nas datas corretas.
5. **Apresentar tabela com**: Mês, Parcelas, C6, Renda, Fluxo, Reserva.

## Nubank: antecipação de parcelas vs CDB

- **Taxa de antecipação Nubank:** ~10,58% a.a. (0,84% a.m.) — confirmado via pesquisa no site oficial.
- **CDB C6:** ~14% a.a. (1,1% a.m.).
- **Conclusão:** Matematicamente, **NÃO antecipar**. Deixar o dinheiro no CDB rende mais do que o desconto da antecipação. Só antecipar se o alívio de fluxo de caixa for crítico (risco de cheque especial).

## Estrutura do orçamento de Igor

O orçamento mensal se divide em duas categorias:

### 🍺 LAZER (~R$ 1.970)
| Item | Valor | Nota |
|---|---|---|
| Claro | R$ 330 | 🔒 Futebol em casa — NUNCA sugerir cortar |
| Karatê | R$ 100 | Saúde |
| TotalPass | R$ 240 | SmartFit + Crossfit (Set/26+) |
| Combustível | R$ 300 | |
| Livres | R$ 1.000 | Mercado, restaurante, lazer |

### 🏠 NÃO-LAZER (~R$ 2.451)
| Item | Valor | Nota |
|---|---|---|
| Condomínio | R$ 1.020 | Estrutural |
| Vivo | R$ 105 | |
| IA (4 assinaturas) | R$ 408 | 🔒 Ferramentas de trabalho — NUNCA sugerir cortar |
| Light | R$ 778 | Jul/26: 454 kWh |
| Gás | R$ 140 | Média histórica |

> Total gasto mensal: ~R$ 4.421. Aparece na fatura do mês seguinte.

## VALLO BENEFÍCIOS + Home Equity

**⚠️ CRÍTICO: VALLO NÃO é renda livre.** R$ 4.420 de VALLO vai integralmente para o Home Equity C6 (CCB 004505, SAC 50m, 1ª parcela R$ 4.389 em 10/Set/2026). Sobra apenas ~R$ 31/mês no início, crescendo ~R$ 40/mês conforme o SAC reduz a parcela.

**Sempre modelar:**
```
Disponível = CLT líquido + (VALLO − Home Equity) + 13º
```
NUNCA somar CLT + VALLO como renda total sem descontar o Home Equity.

## Estrutura de pastas e nomenclatura

```
~/MEGA/Comprovantes/
├── 📄 CONTRACHEQUE.md              ← canônicos (raiz)
├── 📄 HOME-EQUITY.md
├── 📄 MAPA-CUSTO-VIDA.md
├── 📄 ENDIVIDAMENTO.md
├── 📄 FLUXO-CAIXA-2026-2030.md
├── 📄 AVISOS.md
│
├── 📁 _controles/                  ← prefixo CONTROLE_ obrigatório
│   ├── CONTROLE_INDICE.md
│   ├── CONTROLE_FATURAS_MANTIDOS.md
│   ├── CONTROLE_SALDO_CONTAS.md
│   ├── CONTROLE_ORCAMENTO.md
│   └── ...
│
├── 📁 _fichas/                     ← prefixo FICHA_CARTAO_BANCO_ obrigatório
│   ├── FICHA_CARTAO_NUBANK_3033.md
│   └── ... (26 fichas)
│
├── 📁 _Analises/
├── 📁 2026/YYYY_MM_MES/
│   ├── INDEX.md
│   ├── FATURA-CARTAO-<NOME>-R<VALOR>.pdf
│   └── ...
```

### Padrão de nomenclatura de arquivos

- Fatura: `AAAA-MM-DD_FATURA-CARTAO-<NOME_CARTAO>-R<VALOR>.(pdf|md)`
- Comprovante pagamento: `AAAA-MM-DD_FATURA-CARTAO-<NOME_CARTAO>-R<VALOR>-COMPROVANTE-PAGAMENTO.(jpg|pdf|md)`
- Cenários: `AAAA-MM-DD_CENARIOS-PAGAMENTOS.xlsx`
- Playbook: `AAAA-MM-DD_PASSO-A-PASSO-<CENARIO>.md`
- Projeção: `AAAA-MM-DD_PROJECAO-24-MESES.md`

## Contracheque — fluxo de atualização

1. Buscar email com `himalaya envelope list` procurando "Noorden - Contra Cheque"
2. Email de Camila Lima (camilalima@noorden.com.br) com assunto "Noorden - Contra Cheque - <MÊS> <ANO>"
3. Extrair PDF do email com `himalaya message export` + Python `email` module
4. Extrair texto com `pdftotext -layout`
5. Atualizar `dados-contrato.json` com novos valores
6. Atualizar memória com novo líquido
7. Atualizar planilha de cenários com nova renda

## PDFs de fatura Itaú — senha

Faturas Itaú (Signature, Luiza, Passaí) vêm com PDF criptografado.
- **Senha:** 5 primeiros dígitos do CPF (ex: XXXXX)
- **Decriptar com:** `pypdf.PdfReader.decrypt(password)`

## OCR de prints de app (modo escuro)

Apps como Itaú em dark mode falham no Tesseract direto. Ver `references/dark-mode-ocr.md` para o pipeline completo. Resumo rápido:

```python
from PIL import Image, ImageEnhance, ImageOps
img = ImageOps.invert(img.convert('RGB')).convert('L')
img = ImageEnhance.Contrast(img).enhance(2.0)
img = img.point(lambda x: 0 if x < thresh else 255)  # thresh 70-100
text = pytesseract.image_to_string(img, config='--oem 3 --psm 6 -l por')
```

## Projeção de fluxo de caixa (padrão canônico)

### Arquivos na raiz de Comprovantes

Os arquivos canônicos do fluxo de caixa ficam em `~/MEGA/Comprovantes/`:
- `FLUXO-CAIXA-2026-2030.xlsx` — planilha com abas de fluxo, resumo, métricas e contracheque
- `FLUXO-CAIXA-2026-2030.md` — versão Markdown (fonte da verdade; o `.xlsx` é derivado)
- `HOME-EQUITY.md` — cronograma SAC completo da CCB 004505
- `CONTRACHEQUE.md` — real + projeção até Dez/2028
- `_controles/CONTROLE_INDICE.md` — índice vivo de todos os controles ativos e status por cartão; ler primeiro para saber quais arquivos existem hoje
- `ENDIVIDAMENTO.md` — classificação atual mantidos/negociação, propostas recebidas, monitoramento de negativação — ler ANTES do passo 0 (confirmar lista de mantidos vs negociação) em vez de perguntar do zero ao usuário

> ⚠️ Nomes datados mudam de versão (ex.: `FLUXO-CAIXA-2026-2028` foi substituído por `FLUXO-CAIXA-2026-2030` em 03/08/2026, e o arquivo antigo foi apagado). Confirmar com `ls ~/MEGA/Comprovantes/FLUXO-CAIXA-*.md` antes de citar um nome de arquivo específico de memória.

### Geração com Python

Usar script Python com `openpyxl` para gerar Excel com 5 abas:
1. **Visão Geral** — Orçamento, ajustes, métricas KPIs
2. **Fluxo de Caixa** — 29 meses com CLT, VALLO, HE, parcelamentos, C6, reserva
3. **Resumo** — Cartões mantidos, negociação, recursos CDB
4. **Parcelamentos** — Matriz por cartão mês a mês
5. **Premissas** — Todas as premissas do modelo

Pattern: `python3.12` com script em here-document. Gera Excel + Markdown de uma vez.

### Dados reais, não estimativas

- **SEMPRE extrair CCB do PDF** (`pdftotext`) para valores reais do Home Equity
- **SEMPRE usar contracheque real** para CLT líquido
- **SEMPRE usar faturas reais** para parcelamentos (não estimar)
- Fonte CCB: `~/MEGA/Documentos/Emprestimo/1. ccb - vn.pdf`
- Fonte contracheque: email Camila Lima `camilalima@noorden.com.br`

### "Meses no vermelho"

Quando o usuário disser "não posso ter meses no vermelho", explicar que:
- Déficit mensal coberto por reserva NÃO é "estar no vermelho" de verdade
- A reserva do CDB funciona como ponte até os parcelamentos acabarem
- Mostrar a reserva NUNCA zera — só diminui temporariamente
- Após os parcelamentos (Jul/27), o fluxo fica positivo todo mês

## Pitfalls

- **NUNCA assumir que a fatura atual é o único custo.** Parcelamentos futuros explodem o orçamento.
- **SEMPRE incluir juros do cheque especial** em projeções negativas.
- **NÃO antecipar dissídio** sem confirmação de data e percentual.
- **Separar itens pontuais de recorrentes** na renda (ex: triênio retroativo é pontual, triênio é recorrente).
- **VALIDAR com o usuário** antes de gerar Excel/PDF final — ele revisa os números.
- **Senha de PDF de fatura:** perguntar ao usuário (normalmente CPF parcial). Descriptografar com `pypdf`.
- **OCR do app Nubank — não confundir "fatura atual" com "total das próximas faturas".** São números muito diferentes — R$ 5.660 vs R$ 28.548 no mesmo print. Confirmar qual é qual com inspeção cuidadosa.
- **IA é ferramenta de trabalho — NUNCA sugerir cortar.** ChatGPT, Gemini, Claude e Manus são custo fixo intocável.
- **Claro é lazer, não telefone.** R$ 330/mês = futebol em casa. Economiza bar. NUNCA sugerir cortar.
- **VALLO paga Home Equity.** NUNCA modelar VALLO como renda livre sem descontar a parcela do HE.
- **Usar dados reais da CCB.** Extrair do PDF com `pdftotext`, nunca estimar parcela do HE.
- **Cartão Dígio em negociação = limite "grátis".** Pagar contas (luz, gás) com ele preserva caixa. Ver `references/fluxo-caixa-contas-consumo.md`.
- **Limite de qualquer cartão em negociação é recurso.** Usar PIX crédito do cartão que não será pago para quitar cartões menores. Ex: PAN Buscapé pagou PicPay → PicPay saiu da negociação, PAN absorveu +R$880.
- **"Pagou o cartão X?" — sempre especificar o mês da fatura.** Perguntar "pagou o Nubank?" sem o mês gera confusão — a resposta pode ser "só paguei o que vencia em agosto" enquanto a fatura de setembro ainda está em aberto. Sempre listar mês a mês com vencimento.
- **Saldo em conta corrente paga cartões do mesmo banco.** Dinheiro na conta Itaú → usar para cartões Itaú primeiro. Libera o CDB para outros pagamentos. SEMPRE verificar saldo em conta antes de modelar uso do CDB.
- **Mensalidade de advogado muda tudo.** Um advogado que parece "só cobra se reduzir" pode ter R$ 800/mês de mensalidade que ninguém mencionou. Em 6 meses = R$ 4.800 — mais caro que valor fixo de R$ 4.500. Sempre projetar custo total por tempo (3/6/12/24 meses).

## Referências

- `references/dark-mode-ocr.md` — Técnicas para extrair texto de screenshots em modo escuro
- `references/due-diligence-advogado.md` — Checklist completo de due diligence para avaliação de escritório de advocacia (OAB, CNPJ, Jusbrasil, Reclame Aqui, honorários, red flags)
- `references/dossie-template.md` — Template completo do dossiê para advogado (5 seções + geração PDF + envio email)
- `references/fluxo-caixa-contas-consumo.md` — Projeção de fluxo de caixa incluindo contas de consumo (luz/gás) pagas no crédito + estratégia Dígio
- `references/geracao-excel-fluxo.md` — Padrão para gerar Excel + Markdown do fluxo de caixa com openpyxl
- `references/emissores-cartoes.md` — Mapeamento de emissores de cartões de loja (Atacadão=Carrefour, Méliuz=PAN, C&A=Bradescard, etc.)
