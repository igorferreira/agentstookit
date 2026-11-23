# Registrar lançamento "Pix no crédito" (pedalada) no cartão → ficha + fluxo

Workflow validado (02/09/2026) quando Igor envia um comprovante de **Pix no crédito**
(99Pay / RecargaPay à frente de um cartão, ex.: Carrefour 3825) ou qualquer nova fatura/lançamento.

## Trigger
- Comprovante de Pix no crédito para pagar pessoa/fatura/despesa usando cartão como meio.
- "registra esse pix", "lança no cartão X", nova fatura fechada.

## Passos

1. **Extrair o comprovante** (imagem → tesseract `-l por`; PDF → `pdftotext -upw <senha>`).
   Campar: valor, data/hora, método ("Cartão" = Pix no crédito), beneficiário (+banco/conta),
   pagador, ID transação. Senha típica: 4 primeiros dígitos do CPF do titular.
2. **Salvar comprovante** na pasta do mês de CAIXA (dia da transação):
   `~/MEGA/Comprovantes/2026/2026_MM_MES/AAAA-MM-DD_PIX-CREDITO-<CARTAO>-R<VALOR>-<BENEFICIARIO>.{jpg,md}`.
   Criar o `.md` com tabela de metadados + finalidade dita pelo Igor.
3. **Atualizar a ficha** do cartão (`_fichas/FICHA_CARTAO_<BANCO>_<FINAL>.md`):
   - adicionar o lançamento à lista de "Lançamentos já processados" da **fatura que recebe o valor**;
   - recomputar a projeção total daquela fatura;
   - nota estratégica justa (custo juros 4,99% a.m. se não pagar à vista) sem julgar a despesa.
4. **Bump do fluxo de caixa**: editar o YAML de `FLUXO-CAIXA-2026-2030.md` somando o valor à
   coluna `cartoes` do **mês da fatura** (ver off-by-one abaixo), versionar X<n>→X<n+1>
   (bump explícito com delta "antes → agora"), rodar `python3.12 fluxo_caixa/engine/fluxo.py`
   para regenerar MD + XLSX. Nunca editar o XLSX à mão (MD canônico vence).
5. **Verificar**: confirmar a linha do cenário recalculado (CDB mínimo / mês) e que segue
   "não zera".

## Pitfall crítico — OFF-BY-ONE do mês da fatura
Uma compra no **dia 02/09** cai na fatura que fecha **22/09** e vence em **Out/26** — então o
valor entra na linha `cartoes` de **Out/26**, NÃO em Set/26. Regra geral: lançamento PERTENCE ao
mês do VENCIMENTO da fatura que o recebe, não ao mês do dia da compra. Conferir a ficha do cartão
(fechamento/vencimento) antes de escolher a linha do YAML. Errar isso desloca o CDB mínimo em um
mês e subestima o aperto real.

## Observação de acolhimento (Igor é sensível a dinheiro)
Registrar sem julgamento moral da despesa; apenas citar objetivamente o custo (juros a.m. se
parcelado/rotativo) e, quando aplicável, a regra tática da "torneira" (despesa pontual vs recorrente).
Número primeiro, tom de apoio — nunca culpar.