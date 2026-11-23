# Resposta a Bloqueio SISBAJUD de Contas — Workflow (caso Maricá, 31/08-01/09/2026)

Workflow validado ao vivo em 31/08 e 01/09/2026, quando a Execução Fiscal 0040223-62.2021.8.19.0031
(Prefeitura de Maricá × Salada de Sabores Ltda ME / sócio retirante) saiu da suspensão e bloqueou via
SISBAJUD **todas** as contas (Nubank, C6, Itaú, 99Pay).

## O que o usuário relatou + o que estava realmente acontecendo
- Notificação: "Bloqueio Judicial de R$ 34,23, ordem 0040223-62.2021.8.19.0031. Saldo disponível R$ 0,00."
- A conta inteira travou: "nenhum valor entra ou sai."
- O VALLO (R$ 4.420, renda alimentar) tinha caído em 28/08 e ficou preso na Nubank.
- Salário CLT já tinha sido usado para pagar cartões → o R$ 34,23 era apenas o resíduo, mas a travada total da conta é que era o problema.

## O que movimentou o caso para o desbloqueio rápido
1. **Priorizar a verba alimentar/salarial impenhorável** (Art. 833, IV e V, CPC): o argumento decisivo é que o bloqueio prende a renda de sustento do CLT. Pedir **desbloqueio liminar**.
2. Juntar prova de que o usuário é CLT: **últimos 3 contracheques** (maio, junho, julho/2026).
3. Enviar a documentação completa ao advogado constituído: RG, CPF, **fatura** de residência (não o comprovante PIX), CNH, contracheques.

## Exemplo de e-mail de cobrança urgente (tom respeitoso)
"Prezado Dr. X, desculpa apertar, mas preciso reforçar a urgência do desbloqueio da conta [banco].
O bloqueio travou: nem valor entra nem sai. O VALLO (minha renda alimentar, R$ 4.420) caiu dia [data] e
está preso. Não tenho como pagar contas. É verba de natureza alimentar — o Art. 833, IV e V do CPC protege.
Peço que priorize o desbloqueio liminar com base na impenhorabilidade da verba alimentar + minha
ilegitimidade passiva + decadência (sócio retirante desde [ano], JUCERJA). Qualquer documento, mando na hora."

## Padrão de envio de e-mail com anexos (himalaya)
- Montar MIME multipart em Python: `MIMEMultipart` + `MIMEText(body)` + `MIMEApplication(anexo, _subtype="pdf")` com `Content-Disposition: attachment`.
- `To` pode conter vários e-mails separados por vírgula (usuário pediu enviar para os 3 e-mails do advogado).
- Enviar via `himalaya message send --account gmail-igor < /tmp/doc.eml` (lê MIME bruto do stdin; a opção `-a/-s` não existe no `send` desta versão — ele recebe a mensagem crua como argumento/stdin).
- **Confirmar** na pasta de enviados: `himalaya envelope list --account gmail-igor --folder Sent` e localizar o assunto/registro.

## Documentos: caminhos canônicos (01/09/2026)
- RG: `~/MEGA/Documentos/pessoal_saude/id/Carteira de Identidade (RG).pdf`
- CPF: `~/MEGA/Documentos/pessoal_saude/id/outros/IgorFerreira_CPF.pdf`
- CNH: `~/MEGA/Documentos/carros/CNH-e-IGOR-DOS-SANTOS-FERREIRA-2034.pdf`
- Conta de luz (fatura junho): `~/MEGA/Comprovantes/2026/2026_06_JUNHO/2026-06-24_FATURA-LIGHT-COMPROVANTE-PAGAMENTO.pdf`
- Contracheques: `~/MEGA/Documentos/carreira/rescisao_clt/contracheques/` (2026-05, 2026-06, 2026-07)

## Nota de segurança
- Não reenviar RG/CPF/CNH para contatos não formalmente engajados no processo (ex.: "conhece alguém na prefeitura") — só para advogado constituído.
- Não pagar a dívida executada sem o advogado guiar quando houver tese de ilegitimidade passiva.