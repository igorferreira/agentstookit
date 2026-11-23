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

Para extrair texto de PDFs de exames:
- **PDFs normais/sem senha:** usar `pdftotext -layout <pdf_path> <txt_path>`. O `-layout` é essencial para preservar o alinhamento de colunas.
- **PDFs protegidos por senha (ex.: faturas ou laudos com senha de CPF/data de nascimento):** usar `pdftotext -upw <senha> -layout <pdf_path> <txt_path>`. Não requer pacotes Python adicionais como pypdf/qpdf.

Erros `Syntax Error: Bad block header in flate stream` são normais — são imagens/vetores embarcados, não afetam a extração do texto dos resultados. Para imagens (prints, fotos de resultados), usar `tesseract -l por`. Seguir o mesmo padrão de OCR documentado em `financeiro-comprovantes`.

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

Salvar em `~/MEGA/Documentos/pessoal_saude/YYYY-MM-DD_EXAMES-LABORATORIAIS-<LAB>-COMPLETO.md` ou `~/MEGA/Documentos/pessoal_saude/exames/YYYY-MM-DD_EXAMES-<LAB>-RELATORIO-COMPLETO.md`.

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
  - 🦠 Sorologias / Doenças Infecciosas (HIV 4ª geração, Sífilis treponêmica/não-treponêmica, Hepatite B HBsAg/Anti-HBs/Anti-HBc, Hepatite C Anti-HCV)
- Comparação histórica (se o PDF incluir resultados anteriores ou houver coletas anteriores no ano)
- Diagnóstico com 🟢🟡🔴 e recomendações acionáveis da Banca Multidisciplinar

### Extração Rápida de Mídias e Posts do X (Twitter)
Ao buscar postagens do X (`x.com/<user>/status/<id>`) para estudo de cursos e vídeos técnicos:
- Utilizar a API pública do FxTwitter (`https://api.fxtwitter.com/<user>/status/<id>`) com `User-Agent: Mozilla/5.0` via Python/curl para obter JSON estruturado completo com texto, autor, minutagens e URLs diretas do vídeo em 720p/1080p (.mp4).

### 4. Interpretar no contexto do Igor

- **Laudo Beep / Diagnósticos do Brasil (05/08/2026 - Conclusão em 14/08/2026):**
  - **Perfil Lipídico:** CT 233 mg/dL, HDL 31 mg/dL, LDL 187 mg/dL, Não-HDL 202 mg/dL, Triglicérides 47 mg/dL. Risco cardiovascular aterogênico elevado (Razão CT/HDL = 7,51). Exige adesão absoluta ao plano anticolesterol (gordura saturada < 12g/dia, aveia 40g/dia, 3 caps Ômega-3 e azeite).
  - **Série Vermelha:** Hematócrito 51,5% (risco de viscosidade), Eritrócitos 6,40 milhões/mm³ (eritrocitose), Hemoglobina 16,9 g/dL. Exige hidratação de 3,5L a 4,0L de água/dia e fracionamento semanal de doses androgênicas (0,5 mL/semana).
  - **Eixo Hormonal:** Testosterona Total 1.617 ng/dL (2x limite), Testosterona Livre 50,97 ng/dL (3x limite), SHBG 16,6 nmol/L (baixo), LH/FSH 0,3 mUI/mL (suprimidos), Estradiol 11,7 pg/mL (controlado / sem aromatização), Insulina em jejum 2,1 µUI/mL e Insulina Livre 2,2 µUI/mL (sensibilidade celular impecável).
  - **Bioquímica & Órgãos:** Fígado (TGO 20 / TGP 14), Rins (Creatinina 1,17 / Ureia 23), Próstata (PSA 0,32 / PSA Livre 0,15), Pâncreas (Amilase 35 / Lipase 20) e Tireoide (TSH 1,42 / T4L 1,50) todos 100% blindados e saudáveis.
  - **Sorologias:** Sífilis e Hepatite C negativas. Hepatite B: Anti-HBs < 2,00 UI/L (NÃO IMUNE) — indicação médica formal de reforço vacinal de 3 doses no posto de saúde.
- **Laudo Sérgio Franco / DASA (Coleta 14/08/2026 - Liberação 20/08/2026):**
  - **Sorologias / Doenças Infecciosas:** 100% Negativo / Não Reagente para HIV 1/2 (4ª geração CMIA índice 0,05), Sífilis (Anti-T. pallidum CMIA índice 0,04), Hepatite C (Anti-HCV índice 0,10) e Hepatite B HBsAg (índice 0,40). Anti-HBs < 2,0 mUI/mL reconfirma ausência de imunidade/anticorpos contra Hepatite B (reforço vacinal indicado).
  - **Evolução de Vitaminas & Órgãos:** Vitamina D subiu para 42 ng/mL (atingindo a meta ideal > 40 ng/mL da SBEM); Vitamina B12 em 596 pg/mL; TGO 26 U/L e TGP 24 U/L (fígado perfeito); Creatinina 0,92 mg/dL, Ureia 33 mg/dL e Taxa de Filtração Glomerular (eGFR) > 90 mL/min (função renal máxima).
  - **Testosterona Basal:** 363,0 ng/dL (coleta 14/08) representa a baseline fisiológica natural antes do início do protocolo fracionado semanal de Durateston.
- **TRT:** LH/FSH zerados + Testosterona alta = exógena confirmada. Hematócrito > 51% = risco de policitemia. T > 1000 = dose suprafisiológica.
- **Lipídico:** LDL > 100 + HDL < 40 = risco CV elevado. TRT/andrógenos podem reduzir o HDL e aumentar o hematócrito.
- **Ferro:** tríade Ferro Sérico (265 µg/dL) + Ferritina (63,9 ng/mL) + Transferrina (271,8 mg/dL). Ferritina normal indica estoque sem sobrecarga patológica generalizada.
- **Vitamina D:** alvo > 40 ng/mL (diretriz SBEM). Vitamina C (11,6 mg/L) e Vitamina A (0,57 mg/L) ótimas.

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

### Regra: data pelo bloco [Agora]

**SEMPRE** usar a data/hora do bloco [Agora] (sem rodar `date`) em QUALQUER resposta — não só alimentação, mas qualquer assunto. Regra global expandida pelo Igor em 11/08/2026. O contexto temporal de cada mensagem é essencial para respostas precisas e cronologicamente conscientes. Isso vale para todos os agentes e tópicos.

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

## Banca Multidisciplinar de Saúde

A banca atende exclusivamente Igor Ferreira (47 anos, praticante de Karatê, CrossFit e Musculação, histórico de LDL 187 e Hematócrito 51,5%):
- 🩺 **Dr. Nutrólogo:** Dieta, macros, suplementação, fibras e controle de colesterol
- 🫀 **Dr. Cardiologista:** Perfil lipídico, viscosidade sanguínea (hematócrito), risco CV, complacência vascular
- 🧬 **Dra. Endocrinologista:** Eixo HPT, testosterona, estradiol, tireoide, insulina
- 🏋️ **Preparador Físico:** Treino de musculação, periodização PPL, técnica e volume
- 💪 **Coach Fisiculturista & Expert em Ergogênicos:** Farmacologia esportiva, dosagens, fracionamento de ésteres, proteção de órgãos e sinergia de compostos
- 🧠 **Psicóloga Esportiva:** Adesão, sono, motivação e estresse

### Diretrizes para Recursos Ergogênicos (Durateston / Anabolizantes)
- **Princípio:** Anabolizante não queima gordura; preserva massa magra (anti-catabólico) enquanto o déficit calórico da dieta e cardio queimam a gordura.
- **Fracionamento de Durateston:** 125 mg a cada 7 dias (0,5 mL/semana) é superior a 250 mg a cada 14-21 dias para evitar picos suprafisiológicos de aromatização (estrogênio) e elevação aguda de hematócrito.
- **Contraindicações absolutas no contexto Igor:**
  - *Stanozolol (Winstrol):* Vetado com LDL > 130 ou HDL < 40 por destruição do perfil lipídico e sobrecarga hepática.
  - *Duplicação de Testosterona (Durateston + Enantato):* Redundante e desnecessário quando já se utiliza Durateston de farmácia.
- **Regras de Proteção em Uso de Andrógenos:**
  - Hidratação obrigatória: 3,5L a 4,0L de água/dia para controle de hematócrito.
  - Fibras solúveis (aveia 40g/dia) + Ômega 3 (3 caps) + Gordura saturada < 12g/dia para blindar o LDL.
  - Alternância de locais de injeção intramuscular (glúteo / vasto lateral).

## Carteirinha de plano de saúde

### Fluxo: salvamento

Quando Igor enviar foto da carteirinha do plano (ex: Amil S750, Bradesco, etc.):

1. **OCR da imagem** com `tesseract -l por --psm 6` para extrair: nome do titular, operadora, plano, número do cartão, abrangência, rede, nascimento, tipo de contratação.
2. **Salvar a imagem original** em `~/MEGA/Documentos/pessoal_saude/<operadora>/YYYY-MM-DD_CARTEIRINHA-<OPERADORA>-<PLANO>.jpg`.
3. **Salvar o OCR literal** em `.ocr.txt` no mesmo local.
4. **Criar registro .md** com metadados, links e observações úteis (coparticipação, rede conhecida).
5. **Atualizar a memória** com número e plano.

### Rede conhecida (Amil S750 na Freguesia/Jacarepaguá)
- **Sérgio Franco** — Estrada dos Três Rios, 200 (Shopping Main Street). Tel (21) 2672-7070.
- **Bronstein** — 2 unidades na Freguesia.
- Lavoisier não tem unidade no Rio.
- Confirmar sempre no app Amil antes de ir.

## Fluxo: pesquisa de GLP-1/Tirzepatida

### 1. Mounjaro Oficial (Brasil — Farmácias RJ/Jacarepaguá)
Para consultar dosagens oficiais (2,5mg a 15mg), preços PMC vs desconto de farmácia e programa *Lilly Melhor Para Você* (LMPV), carregar `skill_view(name="saude", file_path="references/precos-mounjaro-brasil.md")`.

### 2. Tirzepatida no Paraguai (T.G. / Lipoless)
Quando Igor perguntar sobre preços de Tirzepatida/Mounjaro/Zepbound no Paraguai (Tizerpatida, TG):

1. **Extrair dados das embalagens** (fotos do Igor): nome, laboratório (Indufar CISA [T.G.] ou Etikos [Lipoless]), dosagem, quantidade.
2. **Pesquisar preços nos sites:** comprasparaguai.com.br, comparaguay.com.py, farmaciabrasil.com.py, santaritasalud.com, puntofarma.com.py.
3. **Montar tabela por dosagem** (2.5/5/7.5/10/15mg): preço R$, R$/mg, R$/semana.
4. **Comparar fornecedores:** markup do contato PY vs preço de loja. Calcular em R$/mg, não preço total.
5. **Gerar mensagem via skill `whatsapp-message-writing`** se Igor quiser compartilhar a análise.

### Preços de referência (T.G. Indufar — 14/08/2026, US$1=R$5,30)
| Dosagem | PY (US$) | PY (R$) | R$/mg |
|---:|---:|---:|---:|
| 2.5 mg ×4 | 50 | 265 | 26,50 |
| 5 mg ×4 | 60 | 318 | 15,90 |
| 7.5 mg ×4 | 73 | 387 | 12,90 |
| 10 mg ×4 | 75 | 398 | 9,94 |
| 15 mg ×4 | 83 | 440 | 7,33 |
| Lipoless 15 mg ×4 | 110 | 583 | 9,72 |

### ⚠️ Pitfalls GLP-1
- **Sem registro ANVISA** — importação irregular. Informar riscos, não incentivar.
- Meia-vida: 5 dias (50%), 10 (25%), 15 (12,5%), 20 (6,25%).
- Fracionamento: frasco 15mg/0,5mL = 50 unidades na seringa; 1 unid = 0,3mg.
- Markup delivery PY→BR: ~170-180% sobre preço de loja, similar em todas as dosagens.

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

## Fluxo: preparação para coleta de exames laboratoriais

Quando Igor perguntar sobre jejum, agendamento ou preparo antes de ir ao laboratório:

### Jejum — o que de fato precisa

Não assumir que "todas as sorologias dispensam jejum". Separar por exame:

| Exame | Jejum |
|---|---|
| HIV-1/HIV-2 (teste rápido / sorologia) | ❌ Não |
| Sífilis (VDRL), Hepatites B e C | ❌ Não |
| Hemograma | ❌ Não |
| Glicemia em jejum | ✅ SIM (8-12h) |
| Colesterol total + frações + triglicérides | ✅ SIM (8-10h; 12h ideal p/ TG) |
| HbA1c | Pode sem jejum, mas se junto da glicemia segue o jejum |

**Regra prática:** se a solicitação for um painel combinado (ex.: HIV + sífilis + hepatites **+** glicemia/lipídios), o jejum de 8-12h é obrigatório por causa dos metabólicos/lipídicos — mesmo que as sorologias em si não exijam. Orientar a manter jejum quando a coleta for única do painel completo.

### Agendamento vs. ordem de chegada

- **Sérgio Franco (grupo Dasa)** orienta **agendamento prévio** (plataforma **Nav Dasa** ou telefone). Nem sempre atende "por ordem de chegada" — confirmar antes de ir.
- Sempre recomendar ligar para a unidade e perguntar explicitamente: *"fazem coleta por ordem de chegada ou preciso agendar?"* — a política varia por unidade/período.
- Comodidade "serviço de desjejum" na página da unidade indica que atende rotinas de jejum, mas não garante atendimento sem agendamento.

Quando Igor perguntar sobre jejum, agendamento ou preparo antes de ir ao laboratório:

### Jejum — o que de fato precisa

Não assumir que "todas as sorologias dispensam jejum". Separar por exame:

| Exame | Jejum |
|---|---|
| HIV-1/HIV-2 (teste rápido / sorologia) | ❌ Não |
| Sífilis (VDRL), Hepatites B e C | ❌ Não |
| Hemograma | ❌ Não |
| Glicemia em jejum | ✅ SIM (8-12h) |
| Colesterol total + frações + triglicérides | ✅ SIM (8-10h; 12h ideal p/ TG) |
| HbA1c | Pode sem jejum, mas se junto da glicemia segue o jejum |

**Regra prática:** se a solicitação for um painel combinado (ex.: HIV + sífilis + hepatites **+** glicemia/lipídios), o jejum de 8-12h é obrigatório por causa dos metabólicos/lipídicos — mesmo que as sorologias em si não exijam. Orientar a manter jejum quando a coleta for única do painel completo.

### Agendamento vs. ordem de chegada

- **Sérgio Franco (grupo Dasa)** orienta **agendamento prévio** (plataforma **Nav Dasa** ou telefone). Nem sempre atende "por ordem de chegada" — confirmar antes de ir.
- Sempre recomendar ligar para a unidade e perguntar explicitamente: *"fazem coleta por ordem de chegada ou preciso agendar?"* — a política varia por unidade/período.
- Comodidade "serviço de desjejum" na página da unidade indica que atende rotinas de jejum.

### Checklist padrão para enviar
- Ligar p/ confirmar agendamento/ordem de chegada + horário de coleta
- Confirmar cobertura no app Amil S750
- Jejum 8-12h (água pode) se o painel tiver glicemia/lipídios
- Levar pedido médico + carteirinha + RG
- Verificar validade do pedido (solicitações antigas podem não ser aceitas)

## Gestão e Registro de Exames Laboratoriais (Beep Saúde e Sérgio Franco)

Quando o usuário enviar laudos laboratoriais de rotina ou sorologias:
- **Extração com senha/layout:** Utilizar `pdftotext -upw <senha> -layout` ou `python3.12` com `pypdf` para PDFs protegidos por senha (ex: primeiros 6 dígitos do CPF).
- **Consolidação em Markdown:** Gerar relatório completo em `~/MEGA/Documentos/pessoal_saude/exames/` categorizado por sistemas (Lipídico, Hemograma, Hormônios, Hepático, Renal, Vitaminas e Sorologias).
- **Cruzamento Clínico com Histórico:** Comparar parâmetros chave (Testosterona total/livre, SHBG, Hematócrito, LDL/HDL, Ferro/Ferritina e Vitamina D) contra coletas anteriores para identificar tendências de adaptação metabólica e efeitos de recursos ergogênicos ou suplementação.
- **Alertas de Imunidade / Vacinação:** Se Anti-HBs < 10 UI/L (ou < 2 UI/L), alertar explicitamente sobre a perda de imunidade vacinal contra Hepatite B e orientar o esquema de reforço em 3 doses no posto de saúde público.

## Pitfalls

- **Comparação de Painéis Laboratoriais Sequenciais:** Quando Igor enviar laudos recentes de laboratórios diferentes (ex: Beep/DB e Sérgio Franco/DASA colhidos em datas próximas), correlacionar os parâmetros:
  - *Sorologias de ISTs:* VDRL/FTA-Abs, Anti-HIV 1/2 (4ª geração), Anti-HCV e HBsAg/Anti-HBs devem ser consolidados para atestar negatividade e verificar status vacinal (Anti-HBs < 10 = reforço indicado).
  - *Testosterona / Eixo Hormonal:* Explicar a variação fisiológica entre coletas pós-dose vs basais (ex: 1.617 ng/dL pós-aplicação na Beep vs 363 ng/dL basal no Sérgio Franco antes da dose semanal de 125mg).
  - *Vitaminas:* Monitorar a evolução da 25-OH Vitamina D (meta SBEM > 40 ng/mL) e B12.
- **Mensagens Prontas para WhatsApp sobre Saúde/Exames:** Quando o usuário pedir para enviar o resultado de exames a terceiros (ex: parceira/relacionamento), redigir mensagens objetivas, leves e naturais, entregues sempre em blocos de código Markdown (```text ... ```) com botão de cópia rápida.
- **NUNCA usar formatação LaTeX/Math ($...$ ou \text{}) nas respostas para o Igor:** para medidas, volumes e números comuns (ex: 0,5 mL, 125 mg, 100g, 4L), escrever sempre em texto puro e limpo. A formatação LaTeX polui e atrapalha a leitura em apps de mensagens como Telegram.
- **Segregação Estrita de Domínios de Bancas:** A Banca de Saúde / Performance (nutrólogo, cardiologista, endócrino, coach, preparador físico) é 100% isolada e NUNCA deve ser misturada com bancas técnicas de TI, arquitetura de software ou corporativas da HDI (que operam sob perfis dedicados de engenharia de software).
- **Protocolo de Insumos e Ordem de Agulhas para Injetáveis:** Sempre reforçar a regra clara de uso: Agulha VERDE (30x0,80mm / 21G) exclusivamente para aspirar/puxar do vidro; Agulha PRETA (30x0,70mm / 22G) nova e estéril exclusivamente para aplicar no músculo. Fracionamento de ampola de 1 mL deve ser feito puxando em 2 seringas descartáveis simultaneamente (uma aplica no dia, a outra é guardada encapada com agulha estéril em temperatura ambiente e ao abrigo da luz — nunca na geladeira).
- **Horário Ideal de Aplicação:** Aplicações de testosterona e compostos androgênicos oleosos devem ser feitas preferencialmente pela manhã (07h às 10h) para aproveitar a movimentação diurna na dispersão do óleo muscular (evitando dores/nódulos) e evitar insônia noturna.
- **Sincronização de Rotina e Lembretes:** Ao definir rotinas de suplementação e horários, criar cron jobs locais no Telegram e sincronizar arquivos `.ics` na pasta do Google Drive (`~/Insync/GoogleDrive/...`) para importação no Google Calendar.
- **Sinergia e Timing de Manipulados / Nutracêuticos:**
  - *Complexo Neuro-Mitocondrial (Ashwagandha + CoQ10 + PQQ + Metilfolato):* Tomar 2 caps pela manhã com a primeira refeição (CoQ10/PQQ necessitam de lipídios/azeite/ovos para absorção).
  - *HMB (800mg):* Tomar 2 caps pela manhã como anti-catabólico de proteção muscular.
  - *Creatina (5g) + Whey (30g):* Tomar à tarde / pós-treino com água.
- **Auditoria de Mercado Paralelo / Ergogênicos:** Vetar compra de esteroides orais 17-alfa-alquilados (oxandrolona/stanozolol) e boldenona se o paciente possuir perfil lipídico alterado (LDL alto / HDL baixo) ou hematócrito elevado (>51%). Preservar uso exclusivo de produtos de grau farmacêutico oficial (ex: Durateston Aspen).
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
