---
name: financeiro
description: "Use when Igor asks about financeiro tasks — planejamento financeiro, cenários de pagamento, projeção de fluxo de caixa, registro de faturas e comprovantes, matriz de parcelamentos de cartão."
category: finance
---

# Financeiro — Planejamento e Controle

## Gatilhos

Igor usa "Financeiro" como prefixo para tarefas do domínio financeiro. Reconhecer esse prefixo para ativar automaticamente o contexto.

## Estrutura de pastas

```
~/MEGA/Comprovantes/YYYY/YYYY_MM_MES/
├── INDEX.md                          (controle → contas)
├── FATURA-CARTAO-<NOME>-R<VALOR>.pdf  (fatura original)
├── FATURA-CARTAO-<NOME>-R<VALOR>.md   (OCR + metadados)
├── COMPROVANTE-PAGAMENTO.*            (recibo PIX/boleto)
└── CENARIOS-PAGAMENTOS.xlsx           (planilha de cenários)
```

## Padrão de nomenclatura de arquivos

- Fatura: `AAAA-MM-DD_FATURA-CARTAO-<NOME_CARTAO>-R<VALOR>.(pdf|md)`
- Comprovante pagamento: `AAAA-MM-DD_FATURA-CARTAO-<NOME_CARTAO>-R<VALOR>-COMPROVANTE-PAGAMENTO.(jpg|pdf|md)`
- Cenários: `AAAA-MM-DD_CENARIOS-PAGAMENTOS.xlsx`
- Playbook: `AAAA-MM-DD_PASSO-A-PASSO-<CENARIO>.md`
- Projeção: `AAAA-MM-DD_PROJECAO-24-MESES.md`

## Fluxo de criação de cenários de pagamento

1. **Listar todos os cartões** — ver `~/MEGA/Comprovantes/CONTROLES.md` para a contagem e status atuais (26 era o total no mapeamento original de 30/07/2026; já mudou desde então), com finais, bancos, valores
2. **Separar em blocos** — CDB (01/08), Renda (03-12/08), Pedaladas (Pix crédito)
3. **Criar cenários** — variando quais cartões pagar, usar Pix 18× ou não, crédito extra ou não
4. **Calcular fluxo de caixa** — CDB inicial → (−) fixos → (−) déficit renda → CDB final
5. **Projetar parcelamentos futuros** — matriz mês a mês com TODOS os cartões
6. **Incluir cheque especial** — se fluxo negativo, calcular 8% a.m. de juros sobre saldo devedor
7. **Comparar cenários** — planilha Excel com uma aba por cenário + aba Comparativo

## Matriz de parcelamentos — CRÍTICO

⚠️ **SEMPRE** mapear os parcelamentos futuros de cada cartão ANTES de validar qualquer cenário. Um cenário que parece viável pode quebrar quando os parcelamentos reais entram.

Formato da matriz:
```
| Mês | Nubank | Inter | Amazon | ... | Total | Folga | Saldo |
```

Para cada cartão, extrair do app/boleto as próximas faturas projetadas (gráfico de barras).

## Cheque especial

Nubank cobra ~8% a.m. sobre saldo devedor. Se o fluxo mensal ficar negativo:
- Calcular: OD_acumulado = OD_anterior + |fluxo_negativo| + juros
- Juros = OD_acumulado * 0,08
- Projetar até o OD estabilizar ou virar positivo

## PDFs de fatura Itaú — senha

Faturas Itaú (Signature, Luiza, Passaí) vêm com PDF criptografado.
- **Senha:** 5 primeiros dígitos do CPF (ex: XXXXX)
- **Decriptar com:** `pypdf.PdfReader.decrypt(password)`

## OCR de prints de app (modo escuro)

Apps como Itaú em dark mode falham no Tesseract direto. Padrão:
```python
from PIL import Image, ImageEnhance, ImageOps
img = ImageOps.invert(img.convert('RGB')).convert('L')
img = ImageEnhance.Contrast(img).enhance(2.0)
img = img.point(lambda x: 0 if x < thresh else 255)  # thresh 70-100
text = pytesseract.image_to_string(img, config='--oem 3 --psm 6 -l por')
```

## Contracheque — fluxo de atualização

1. Buscar email com `himalaya envelope list` procurando "Noorden - Contra Cheque"
2. Email de Camila Lima (camilalima@noorden.com.br) com assunto "Noorden - Contra Cheque - <MÊS> <ANO>"
3. Extrair PDF do email com `himalaya message export` + Python `email` module
4. Extrair texto com `pdftotext -layout`
5. Atualizar `dados-contrato.json` com novos valores
6. Atualizar memória com novo líquido
7. Atualizar planilha de cenários com nova renda

## Playbook de execução

Quando Igor decidir um cenário, criar passo a passo com:
- 📅 Data, #, horário, ação, app, valor
- Saldo após cada pagamento (evolução visual)
- ⚠️ Ordem correta (pagar Nubank antes das pedaladas)
- Checklist pré-execução

## Pitfalls

- **Nunca validar cenário sem matriz de parcelamentos.** O buraco real pode ser 3× maior.
- **Sempre calcular cheque especial** se fluxo negativo — juros de 8% a.m. mudam tudo.
- **Nunca descontar custo de vida da renda** ao calcular capacidade de pagamento — o custo já está nas faturas dos cartões.
- **VALLO NUNCA entra em cálculo de rescisão CLT.**
- Faturas Itaú são PDF criptografado com senha = 5 primeiros dígitos do CPF.
