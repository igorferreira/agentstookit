# Senhas de PDF e valores sem anexo (emissores do Igor)

## Senha do PDF por emissor

| Emissor | Senha |
|---|---|
| Itaú (Passaí 6698, Uniclass 6651, Platinum 6423) | 5 primeiros dígitos do CPF |
| Luiza/Magalu (9105) | 5 primeiros do CPF |
| BMG (4367) | 5 primeiros do CPF |
| Carrefour/Atacadão (Banco CSF, 3825/1843) | 4 primeiros do CPF |
| C&A Pay (5777) | 4 primeiros do CPF |
| Porto Bank (8121) | 4 do CPF + 5 do CEP |
| BradesCard (Amazon 3018, Casas Bahia 6015) | 6 primeiros do CPF |
| Méliuz (Banco BV, 2048/3679) | CPF completo (11 dígitos) |

Novo emissor sem padrão conhecido: ler o corpo do e-mail — quase sempre a própria mensagem explica a composição da senha ("informe os cinco primeiros dígitos do seu CPF").

## Fatura sem PDF — valor no PIX do corpo

- **Digio** e **Carrefour CSF** mandam e-mail de fatura com **PIX copia-e-cola** em vez de anexo. O valor total está no payload EMV, tag 54: localizar `54` seguido do comprimento — `5407` = 7 dígitos seguintes = `2165.30` → R$ 2.165,30 (formato ponto decimal). Salvar o PIX copia-e-cola no `.md` em bloco de código: é a evidência de valor.
- **Nubank** com débito automático: e-mail "Sua fatura fechou e o débito automático está ativado" traz valor e vencimento no texto, sem PDF — registrar `.md` com status "pagamento agendado (débito automático)".
- **BradesCard** manda um e-mail por cartão (um por final) com o mesmo assunto — abrir os dois corpos e separar Amazon × Casas Bahia pelo arquivo anexo/nome.

## Ordem de tentativa de senha (novo emissor)

CPF (limpo) fatiado: 5 → 4 → 6 → completo; depois variantes com CEP (CPF4+CEP5, CPF5+CEP5); depois data de nascimento (ddmmaaaa, aaaammdd). Parar e ler o corpo do e-mail antes de brute-force longo — a resposta quase sempre está lá.
