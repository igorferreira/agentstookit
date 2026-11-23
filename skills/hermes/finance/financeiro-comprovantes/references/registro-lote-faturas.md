# Registro em lote de faturas — maratona de atualização

## Quando usar

Quando o usuário envia **múltiplos prints de fatura em sequência rápida** (ex.: 10-14 cartões na mesma sessão), cobrindo a maioria dos cartões pendentes de um mês.

## Padrão da sessão

Cada fatura segue o mesmo ciclo atômico:

1. **OCR** — `tesseract` com varredura PSM 3, 4, 6, 11, 12 (`-l por`). Ver `ocr-banking-apps.md`.
2. **Salvar PDF** — cópia do original na pasta mensal com nome padronizado:
   `AAAA-MM-DD_TIPO-BANCO-CARTAO-FINAL-COMPETENCIA-RVALOR.ext`
3. **Evidência** — criar `.md` na pasta mensal com dados extraídos, metadados, parcelamentos, projeção e observações.
3. **Ficha do cartão** — sobrescrever `_fichas/FICHA_CARTAO_BANCO_NOME.md` com:
   - Cabeçalho padronizado obrigatório (Nome, Banco emissor, Vencimento, Últimos 4 dígitos)
   - Dados da fatura atual + parcelamentos ativos + projeção
   - Histórico de eventos + observações
4. **Plano master-detail** (se aplicável) — `patch` no `PLANO-DOSSIE-MASTER-DETAIL.md` em `_Analises/`:
   - Linha do cartão: `⬜` → `✅ CONFIRMADO (R$ X.XXX, fonte data)`
5. **Resumo ao usuário** — tabela antes/depois + novo total + próximos pendentes.

## Variação: lote de PDFs oficiais fechados e comprovantes

Use quando a conferência envolve faturas oficiais em PDF, cópias sem senha e comprovantes de pagamento — não apenas prints de app.

1. Monte o inventário esperado com uma linha por obrigação, identificada por emissor, cartão/final quando disponível, competência e vencimento. Conte documentos únicos, não arquivos: original e cópia sem senha da mesma fatura são um só item.
2. Abra os PDFs com PyMuPDF. Confirme que o original está preservado e que a versão sem senha abre; se o próprio original já abre, registre isso como normal, sem exigir uma segunda cópia descriptografada.
3. Extraia de cada fatura o valor total e o vencimento. Compare com o Markdown correspondente e com o controle mensal. Some valores com `Decimal`, validando contagem e total do lote. Ao ler Markdown em tabela, localize a linha pelo rótulo do campo e extraia o valor monetário dessa linha; não dependa de negrito ou outro estilo de formatação. Normalize datas antes de comparar, pois o PDF pode escrever o mês por extenso/abreviado enquanto o controle usa `dd/mm/aaaa`.
4. Para cada comprovante, confira no conteúdo visível valor pago, data efetiva, beneficiário e referência/vencimento; concilie com uma única fatura. Nome do arquivo, agendamento ou proximidade de valor não provam pagamento.
5. Separe total documental bruto de necessidade de caixa pendente. Se a fatura foi paga antes do mês de vencimento, preserve-a no inventário da competência, marque-a como paga e vincule o comprovante; retire-a da saída futura do fluxo, mantendo a saída somente no mês do desembolso. Atualize os dois controles mensais quando forem distintos, sem duplicar o desembolso.
6. Se a alteração afeta o fluxo projetado, atualize a fonte canônica e regenere os derivados pelo escritor oficial; depois reconstrua e valide o dashboard conforme `fluxo-caixa-source-of-truth.md`.

**Pitfalls:** não contar a cópia sem senha como uma segunda fatura; não exigir cópia adicional quando o original já é legível; não aceitar um total do Markdown sem compará-lo ao PDF; e não confundir a soma de todas as faturas oficiais com o valor ainda necessário pagar no mês.

## Ordem de prioridade na maratona

1. Cartões com vencimento mais próximo (01-05 do mês) — impacto no grupo "iminente"
2. Cartões completamente sem informação (❓ → 🟡/🟢)
3. Cartões com obrigação parcial (⬜ → 🟡 com valor real)
4. Cartões já zerados/confirmados (só atualizar status)

## Evolução típica dos números

O total pode oscilar durante a sessão:
- **Sobe** quando fatura real >> valor provisionado (Porto Seguro, Digio)
- **Desce** quando vencimento é adiado para mês seguinte (BrasilCard: ago → set)
- **Não muda** quando cartão zerado é confirmado ou fatura já estava no total

Manter o usuário informado da direção e magnitude de cada mudança.

## Marcos a celebrar

- Todos os cartões com alguma posição, fim dos ❓ (ver `CONTROLES.md` para a contagem atual — era 26 no levantamento original de 30/07/2026)
- Fim das obrigações parciais (fim dos ⬜)
- Dossiê completo para o advogado

## Pitfalls específicos da maratona

- **Fadiga de patch**: após 10+ patches no mesmo arquivo, reler o estado atual antes de cada patch para evitar conflitos.
- **Acumular patches pendentes**: se um patch falhar, resolver imediatamente — não deixar inconsistências entre resumo e tabela.
- **Cartão com final diferente do cadastro**: apps podem mostrar final físico vs virtual diferente do inventário. Registrar ambos (ex.: C6 6781/7004).
- **Vencimento diferente do cadastro**: sempre conferir o vencimento exibido no app — pode divergir do histórico (Signature 15→03, BrasilCard 10/08→10/09).
