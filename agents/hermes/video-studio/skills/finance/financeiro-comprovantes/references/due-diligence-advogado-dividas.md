# Due Diligence de Advogado para Dívidas

Quando Igor estiver avaliando um escritório de advocacia para renegociação de dívidas, executar este ciclo completo ANTES de recomendar contratação.

## Fase 1 — Coleta de dados do escritório

### Fontes obrigatórias

| Fonte | O que buscar |
|---|---|
| Site oficial | Especialidade, tempo de atuação, equipe |
| OAB Nacional | Inscrição ativa, situação, nome completo |
| Escavador | Volume de processos, estados, partes |
| Jusbrasil | Processos, principais adversários |
| Reclame Aqui | Reclamações de clientes |
| CNPJ | Razão social, quadro societário, endereço |
| Mídia | Menções em jornais, portais |
| Redes sociais | Seguidores, engajamento, consistência |

### Alertas

- Reclame Aqui: "propaganda enganosa" → 🚩. Sem resposta → 🚩🚩.
- OAB: Editais no Diário Eletrônico → possível processo disciplinar.
- CNPJ: Sociedade individual com nome de sociedade ("Fulano & Ciclano") → 🟡.
- Redes: Cruzar "desde 20XX" com data de inscrição OAB. Página comprada/convertida → 🟡.

## Fase 2 — Análise de honorários

### Modelos e alinhamento

| Modelo | Risco |
|---|---|
| Valor fixo único | Advogado ganha mesmo sem resultado |
| Mensalidade | Mais tempo = mais honorários |
| % sobre redução | Só ganha se você ganhar |
| Misto (mensal + %) | Risco parcial |

### Projeção de custo por duração

Sempre simular 3, 6, 12, 24 meses quando houver 2+ advogados.

## Fase 3 — Verificação de casos de sucesso

1. Extrair PDF com `pdftotext` ou `tesseract --psm 3 -l por`
2. **Verificar quem negociou**: PDF pode ser de terceirizada (CRC), não do escritório
3. **Desconto real vs anunciado**: "92%" frequentemente = "89%" no documento
4. **Tempo de atraso**: 10-18 meses é o preço do desconto de ~90%
5. Salvar PDF em `Dividas/`

> O "segredo" de 90% off é paciência + nome sujo, não habilidade jurídica. O advogado agrega na blindagem de cobranças (CDC art. 42).

## Fase 4 — Decisão

Só recomendar depois de: OAB ativa, Reclame Aqui, honorários, casos verificados, comparação lado a lado.

> ⚠️ Nunca pagar antes do contrato. Pressão por decisão rápida = 🚩.
