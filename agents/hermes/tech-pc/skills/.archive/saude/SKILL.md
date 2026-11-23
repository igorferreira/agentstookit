---
name: saude
description: "Use quando Igor usar o prefixo 'saude' ou 'saúde' — pesquisa de rede credenciada, cobertura de plano Amil S750, exames, laboratórios na Freguesia/Jacarepaguá e análises de banca de saúde."
---

# Saúde — Plano, Rede e Exames

## Overview

Skill para tarefas relacionadas à saúde de Igor: plano Amil S750, rede credenciada de laboratórios e hospitais na Freguesia (Jacarepaguá, Rio de Janeiro), resultados de exames e análises de banca multidisciplinar.

## Pastas

| Pasta | Conteúdo |
|---|---|
| `~/MEGA/Documentos/pessoal_saude/` | Resultados de exames laboratoriais, análises corporais (Zepp Life), rede de laboratórios |
| `~/MEGA/Documentos/PLANO_SAUDE_PJ/` | Comparações de planos de saúde PJ |

## Arquivos principais

| Arquivo | Conteúdo |
|---|---|
| `~/MEGA/Documentos/Exames/REDE-LABORATORIOS.md` | Labs credenciados Amil S750 na Freguesia (Sérgio Franco, Bronstein) |
| `~/MEGA/Documentos/Exames/.beepsaude_credenciais.json` | Credenciais Beep Saúde |

## Fluxo: pesquisa de cobertura de plano

Quando o usuário perguntar se o plano cobre determinado laboratório/exame na região:

1. **Pesquisar na internet** — site oficial do laboratório (página de convênios) e site da Amil (busca de rede credenciada).
2. **Confirmar endereço e aceitação** — verificar se a unidade específica no bairro atende o plano.
3. **Buscar alternativas** — se o lab principal não atender, pesquisar outros na mesma região (Bronstein, Lavoisier, etc.).
4. **Salvar em `REDE-LABORATORIOS.md`** — atualizar o arquivo com os achados.
5. **Sempre alertar** — rede credenciada pode mudar; confirmar no app da Amil antes de agendar.

## Plano atual

| | |
|---|---|
| **Plano** | Amil S750 |
| **Cobertura** | Nacional |
| **Laboratórios na Freguesia** | Sérgio Franco (Shopping Main Street), Bronstein (2 unidades) |
| **Site Amil** | [amil.com.br](https://amil.com.br/portal/web/servicos/saude/rede-credenciada/amil/busca-avancada) |

## OCR de exames e documentos de saúde

Para extrair texto de PDFs de exames, usar `pdftotext -layout` (o `-layout` é essencial para preservar o alinhamento de colunas). Para imagens (prints, fotos de resultados), usar `tesseract -l por`. Seguir o mesmo padrão de OCR documentado em `financeiro-comprovantes`.

## Fluxo: PDF de exames laboratoriais → relatório estruturado

Quando Igor enviar um PDF de exames de sangue/urina (ex.: Diagnósticos do Brasil/Fleury, Sérgio Franco, Bronstein):

### 1. Extrair texto do PDF

```bash
pdftotext -layout <pdf_path> /tmp/exames_full.txt
```

Erros `Syntax Error: Bad block header in flate stream` são normais — são imagens embarcadas, não afetam a extração do texto dos resultados.

### 2. Parse dos resultados

O layout típico de laudo segue este padrão:

```
NOME_DO_EXAME                            Info de referência
Resultado:  VALOR UNIDADE                Faixa de referência
Método: ...
Material: SORO/SANGUE/...
```

**Script de extração (Python heredoc no terminal):**
- Encontrar todas as linhas com `Resultado:\s+([\d.,]+)\s+(\S+)`
- Para cada resultado, escanear até 15 linhas acima procurando o nome do exame (texto em caixa alta com acentos, ignorando cabeçalhos estruturais)
- Palavras a pular: Método, Material, Coleta, Hash, Liberado, Dr., PAGINA, NOME:, DATA DE, CPF:, HUB:, MÉDICO:, RESPONSÁVEL, Unidade produtiva

**Hemograma tem formato diferente** — valores inline:
```
HEMOGLOBINA  16,9 g/dL  12,5 a 17,0 g/dL
HEMATÓCRITO  51,5 %     37,5 a 51,0 %
```
Parse separadamente buscando pelos nomes conhecidos dos parâmetros.

### 3. Montar o relatório

Salvar em `~/MEGA/Documentos/pessoal_saude/YYYY-MM-DD_EXAMES-LABORATORIAIS-<LAB>.md`.

**Estrutura do relatório:**
- Cabeçalho: lab, médico, data/hora coleta, status jejum
- Seções por categoria com tabelas markdown (Exame | Resultado | Referência | Status):
  - 🔴 Perfil Lipídico (CT, HDL, LDL, Não-HDL, VLDL, TG)
  - 🩸 Hemograma (Série Vermelha, Série Branca, Plaquetas)
  - 💉 Bioquímica (Ferro, Ferritina, Transferrina, Creatinina, Ureia, Amilase, Lipase)
  - 🧬 Função Hepática (TGO, TGP)
  - 💪 Hormônios (Testosterona, LH, FSH, Estradiol, Cortisol, Insulina)
  - 🦋 Tireoide (TSH, T4 Livre)
  - 🩺 PSA
  - 💊 Vitaminas e Minerais (D, B12, Ác. Fólico, A, C, Zinco, Magnésio)
  - 🦠 Sorologias
- Comparação histórica (se o PDF incluir resultados anteriores)
- Diagnóstico com 🟢🟡🔴 e recomendações acionáveis

### 4. Interpretar no contexto do Igor

- **TRT:** LH/FSH zerados + Testosterona alta = exógena confirmada. Hematócrito > 51% = risco de policitemia. T > 1000 = dose provavelmente excessiva.
- **Lipídico:** LDL > 100 + HDL < 40 = risco CV elevado. TRT pode piorar HDL.
- **Ferro:** tríade Ferro Sérico + Ferritina + Transferrina. Ferro alto + Ferritina normal pode indicar ingestão recente ou hemólise.
- **Vitamina D:** alvo > 40 ng/mL (diretriz SBEM).

### 5. Referência cruzada com medições anteriores

Sempre que houver exames anteriores no mesmo ano, montar tabela comparativa com tendências (↑↓). O laudo do Fleury já inclui 2 coletas anteriores como referência — extrair esses dados da tabela de comparação ao final de cada seção de exame.

## Fluxo: balança inteligente — Xiaomi Mi Scale 2 + Zepp Life

Quando Igor enviar prints do app Zepp Life (Xiaomi) com medições corporais:

1. **Capturar screenshots por seção** — cada métrica em um print separado (Zepp Life tem fonte fina, difícil OCR em tela cheia)
2. **OCR com resize 3x:** `convert img.jpg -resize 300% -sharpen 0x1 /tmp/ocr.png && tesseract /tmp/ocr.png stdout -l eng --psm 6`
3. **Inglês funciona melhor que português** para as métricas numéricas do Zepp Life (termos como "Body fat", "Visceral fat", "Bone mass" são reconhecidos em inglês)
4. **Compilar métricas:** Peso, IMC, Gordura corporal (%), Água (%), Massa muscular (kg), Proteína (%), Massa óssea (kg), Metabolismo basal (kcal), Gordura visceral, Idade corporal, Pontuação corporal
5. **Analisar evolução:** comparar com medição anterior (mês a mês), destacar variação de peso, gordura e massa muscular
6. **Priorizar alertas:** gordura visceral > 9 = risco cardiovascular (prioridade #1)
7. **Salvar relatório:** `~/MEGA/Documentos/pessoal_saude/YYYY-MM-DD_AVALIACAO-CORPORAL-ZEPLIFE.md`

## Fluxo: geração de PDF para médicos

Quando Igor pedir "faz versão em pdf" do relatório de exames para levar à médica:

```bash
pandoc <relatorio.md> \
  --pdf-engine=wkhtmltopdf \
  --metadata title="Título" \
  -o <saida.pdf> \
  --from markdown+emoji
```

**⚠️ Cuidado:** não sobrescrever o PDF do laudo original. Usar nomes distintos:
- `YYYY-MM-DD_EXAMES-LABORATORIAIS-<LAB>.md` — fonte markdown da análise
- `YYYY-MM-DD_EXAMES-LABORATORIAIS-<LAB>-LAUDO.pdf` — laudo original do laboratório
- `YYYY-MM-DD_EXAMES-LABORATORIAIS-<LAB>-ANALISE.pdf` — análise comentada (PDF pra médica)

## Fluxo: registro alimentar

Quando Igor mandar informações de alimentação (prefixo "Saúde" ou "saude"):

### Regra: `date` antes de tudo

**SEMPRE** executar `date` no terminal antes de registrar qualquer informação de alimentação. Nunca confiar na data de contexto ou memória.

### Antes de registrar: carregar referências

1. `skill_view(name="saude", file_path="references/macros-alimentos.md")` — tabela de macros para cálculo
2. `skill_view(name="saude", file_path="references/plano-anticolesterol.md")` — regras anti-LDL se relevante

### Arquivo

`~/MEGA/Documentos/pessoal_saude/YYYY-MM_ALIMENTACAO.md` (um arquivo por mês).

### Formato da tabela

```markdown
## DD/MM/AAAA (Dia da semana)

| Hora | Refeição | Alimento | Qtde | Prot (g) | Carbo (g) | Gord (g) | kcal |
|---|---|---|---|---|---|---|---|
| 13:00 | Almoço | Patinho moído | 200g | 42 | 0 | 10 | 260 |
| 13:00 | Almoço | Arroz integral | 100g | 2,5 | 23 | 1 | 110 |
| 17:00 | Lanche | Ovos inteiros | 3 un | 18 | 1,5 | 15 | 210 |
| 21:00 | Jantar | Whey Protein | 30g | 24 | 3 | 1,5 | 120 |
| | | **Total** | | **86,5** | **27,5** | **27,5** | **~700** |

### Observações
- Notas sobre o dia, déficit, qualidade da dieta
- Sempre comentar se gordura saturada passou do limite (12g/dia)
- Alertar se fibra ficou abaixo de 25g
```

### Cálculo de macros

Usar `references/macros-alimentos.md` como referência. Para alimentos novos (foto de rótulo), seguir o fluxo "leitura de rótulo nutricional" abaixo.

### Atualização incremental

Quando Igor adicionar um alimento à refeição já registrada, usar `patch` para editar a tabela, recalculando o total e atualizando as observações. NÃO reescrever o arquivo inteiro.

### Pitfalls específicos de alimentação

- Igor pode dizer "não vou jantar" mas depois decidir tomar whey — atualizar, não deletar o jantar.
- **"Na arfrieyr"** = "na air fryer" — frango/carne grelhada na air fryer. Tratar como grelhado (sem óleo adicional).
- Pesos em gramas sempre, medidas caseiras com moderação (1 scoop, 3 un).
- **Alerta automático de colesterol:** se o dia tiver >12g gordura saturada, <25g fibra, ou >300mg colesterol dietético, emitir alerta 🚨 com referência ao plano anticolesterol.

## Fluxo: controle de suplementos

Arquivo canônico: `~/MEGA/Documentos/pessoal_saude/SUPLEMENTOS.md`.

### Quando Igor mencionar um suplemento

1. **Registrar ou atualizar** no `SUPLEMENTOS.md` com: nome, marca, data de início, dose diária, quantidade do frasco.
2. **Calcular duração:** `qtd_frasco ÷ dose_diária = dias`.
3. **Estimar data de término:** `data_início + dias`.
4. **Se faltar dado** (ex.: quantas cápsulas no frasco, gramas do pote), **perguntar uma vez**.
5. **Atualizar status:** 🟢 Em uso → 🟡 Acabando (<7 dias) → 🔴 Finalizado.

### Estrutura da tabela

| # | Suplemento | Marca | Início | Dose Diária | Qtd. Frasco | Duração | Término Previsto |
|---|---|---|---|---|---|---|---|

### Regras

- Suplemento para colesterol (ômega 3): 2-3 caps/dia, tomar **com refeição** (lipossolúvel), dividir em 2 tomadas.
- Cronômetro de término: quando faltarem 7 dias, avisar Igor proativamente.
- Quando Igor disser "acabou X" ou "comprei mais Y", atualizar movendo para 🔴 Finalizados e criando nova linha em 🟢.

## Fluxo: leitura de rótulo nutricional a partir de fotos

Quando Igor enviar foto da tabela nutricional de um produto (ex.: "Saúde comi X gramas disso aqui"):

1. **Extrair os valores da porção** — o sistema já fornece descrição da imagem com os números da tabela. Conferir:
   - Porção de referência (ex.: 30g, 10g, 1 colher de sopa)
   - Valor energético (kcal)
   - Proteínas (g), Carboidratos (g), Gorduras totais (g), Gorduras saturadas (g)
2. **Converter para a quantidade consumida** — regra de 3 simples: (qtde_consumida / porção_ref) × valor
3. **Registrar no arquivo de alimentação** conforme o fluxo acima
4. **Adicionar à tabela de macros** em `references/macros-alimentos.md` se for um alimento novo ou recorrente
5. **Se o produto for rico em gordura saturada** (>5g/porção), emitir alerta automático considerando o plano anticolesterol

### Exemplo

Igor manda foto do Cream Cheese Danubio (30g = 77 kcal, 1.4g prot, 7.4g gord) e diz que comeu 60g:
- 60g = 2 porções → 154 kcal, 2.8g prot, 14.8g gord
- 14.8g de gordura saturada já estoura o limite diário → 🚨 alerta

## Plano anticolesterol

Quando a conversa envolver colesterol, LDL, HDL, ou perfil lipídico, carregar `skill_view(name="saude", file_path="references/plano-anticolesterol.md")` com as regras dietéticas específicas (metas de gordura saturada, fibra, trocas alimentares, proibições).

## Fluxo: treino de musculação

Quando Igor pedir um plano de treino de musculação:

1. **Considerar a semana completa** — ele treina 7 dias: karatê 3× (ter/qui/sáb 20-22h, sáb também 9-11h), CrossFit 2×, musculação 3×. Encaixar sem sobrecarregar (ex.: sábado pernas de manhã + karatê à noite = pernas leve).
2. **Foco solicitado:** peito, costas, pernas (PPL simples).
3. **Formato:** 5 exercícios por dia, 3 séries cada, 45 min, progressão linear (sobe 2.5kg quando bate 10 reps fáceis).
4. **Salvar:** `~/MEGA/Documentos/pessoal_saude/YYYY-MM_TREINO-MUSCULACAO.md`.
5. **Regras do treino:** aquecer 5 min bike/esteira, falha só na última série, pernas no sábado NUNCA pesado (tem karatê depois).

## Pitfalls

- Confirmar sempre no app/site da Amil antes de ir ao laboratório — rede pode mudar.
- Distinguir "aceita Amil" de "aceita Amil S750" — alguns labs aceitam planos mais básicos mas não o S750.
- Lavoisier só tem unidades em São Paulo — não serve para Igor (RJ).
- Ao gerar PDF da análise, NUNCA sobrescrever o PDF do laudo original. Usar `-ANALISE.pdf` e `-LAUDO.pdf` como sufixos distintos.
- **Cream cheese/manteiga:** gordura saturada concentrada — cada 60g de Danubio = ~15g gordura saturada (estoura limite anti-colesterol). Flag automático.
- **Bisnaguinha:** açúcar é o 2º ingrediente. Carbo refinado, péssimo pro perfil lipídico. Alertar.
- **Nescau Protein:** tem açúcar adicionado. Whey DUX puro é superior pra mesma proteína sem o açúcar.
- **Omega-3 é lipossolúvel:** tomar com refeição que tenha gordura. Dividir em 2 tomadas (almoço + jantar) reduz arrotos de peixe.
- **Creatina vencida:** perde potência mas não faz mal. Flag validade vencida, mas não bloquear uso.
- **"Na arfrieyr"** = na air fryer. Tratar como grelhado (sem óleo adicional).
