# Caso real: Requerimento SIMPLIFICA Maricá (03/09/2026)

Formulário "Requerimento Geral" da Prefeitura de Maricá (1 página A4), anexo `req.CPF.pdf`
em e-mail do Simplifica. Preenchido e verificado por colisão de pixels.

## Campo → baseline (y) → coluna (x) — referência
| Campo | baseline y (pt) | texto | x |
|---|---|---|---|
| NOME | 145 | IGOR DOS SANTOS FERREIRA | 56 |
| RG | 188 | 11.599.465-9 | 56 |
| ÓRGÃO | 188 | DETRAN-RJ | 226 |
| DATA EMISSÃO | 188 | 01/02/2017 | 300 |
| CPF | 188 | XXX.XXX.XXX-XX | 370 |
| ENDEREÇO | 220 | RUA ITUVERAVA, 705 - BLOCO 01, APTO 405 - JACAREPAGUA, RJ | 56 |
| TELEFONE | 258 | (21) 99641-67952 | 56 |
| E-MAIL | 258 | igorferreirabr@gmail.com | 210 |
| INSCRIÇÃO MERCANTIL | 325 | CNPJ 07.801.460/0001-68 | 320 |
| ASSUNTO | 372 | DESVINCULACAO DO QUADRO SOCIETARIO E DOS DEBITOS | 56 |
| DESCRIÇÃO | 405→562 | parágrafos | 56 |

- Assinatura/DATA ficam **em branco** (assinar à mão). Assinatura original em y≈750.
- IPTU **não preenche** (fora do caso). Inscrição Mercantil = CNPJ da empresa.

## Dados do titular validados (fonte)
- RG 11.599.465-9, DETRAN-RJ, 01/02/2017 → OCR do cartão (NÃO usar número da CNH).
- Endereço Rua Ituverava 705 B01/405, RJ, CEP 22750-005 → fatura Naturgy do processo.

## Dica de verificação por banda
Projeção vertical dos pixels azuis → cada `y`-banda corresponde a um campo preenchido.
No original, bandas azuis em y47-78 = logo/cabeçalho do próprio formulário (NÃO é vazamento).
Não tratar eles como erro ao comparar original vs preenchido.