# Pesquisa de emissores, financiadores e credores de cartões

Use quando o cadastro/fatura local mostrar apenas a marca comercial, trouxer emissor genérico ou houver co-brand com possível divergência jurídica.

## Objetivo

Não tratar `marca`, `emissor`, `financiador` e `credor atual` como sinônimos. Para negociação de dívida, registrar quatro campos separados:

1. **Marca/cartão:** nome visto pelo cliente.
2. **Emissor jurídico:** entidade que emite/administra o instrumento de pagamento.
3. **Financiador do saldo:** entidade que concede crédito no rotativo/parcelamento.
4. **Credor atual:** entidade indicada na fatura, contrato individual, SCR ou cessão.

## Ordem de pesquisa

1. Fatura e contrato individual do usuário.
2. Contrato/regulamento oficial do produto.
3. Central de ajuda ou página institucional oficial.
4. Banco Central: instituição autorizada, razão social e CNPJ-base.
5. Termos de uso, política institucional ou demonstração financeira oficial.
6. Bandeira/arranjo de pagamento, CVM ou Diário Oficial como confirmação complementar.
7. Fontes secundárias somente para localizar documento primário; não usar isoladamente para conclusão jurídica.

## Procedimento

1. Liste apenas os produtos cujo emissor está ausente, genérico ou conflitante.
2. Pesquise o nome exato do produto com `contrato`, `regulamento`, `emissor`, `CNPJ`, `financiador` e `PDF`.
3. Abra e extraia a cláusula que define `Emissor`, `Administradora`, `Financiador` ou `Credor`.
4. Confirme razão social/CNPJ no Banco Central ou fonte institucional.
5. Para co-brands, procure se a loja é apenas correspondente bancário.
6. Para instituições de pagamento, verifique quem financia o saldo: uma IP pode emitir o cartão sem conceder o crédito.
7. Registre nível de confiança:
   - **Alta:** contrato/página oficial define a entidade;
   - **Média-alta:** instituição regulada confirmada, contrato individual pendente;
   - **Pendente:** marca encontrada, mas credor do saldo não comprovado.
8. Atualize o relatório cadastral, a matriz por credor e o dossiê de negociação sem alterar o total financeiro apenas por reclassificação.
9. Salve URLs e a data-base da pesquisa em relatório próprio.

## Regras de segurança e precisão

- Não agrupar produtos apenas porque compartilham marca ou aplicativo.
- Não atribuir automaticamente cartão de loja ao banco mais conhecido do grupo.
- Não chamar a marca comercial de credor jurídico sem cláusula/fatura.
- Se houver securitização ou cessão prevista, registrar a possibilidade e exigir prova do credor atual antes de acordo/pagamento.
- Na negociação, exigir saldo atualizado, identificação do credor, canal oficial, condições e termo de quitação.
- Exibir apenas os três últimos dígitos no relatório principal; quatro somente em anexo autorizado quando necessário para identificar contrato.

## Exemplos de distinção

- Cartão co-branded pode ter loja como correspondente e financeira separada como emissora.
- Uma instituição de pagamento pode emitir o cartão, enquanto um banco financia o saldo.
- O credor que cobra após atraso pode ser cessionário distinto do emissor original.

## Verificação final

- [ ] Nenhuma célula continua como `emissor não identificado` sem tentativa documentada de pesquisa.
- [ ] Marca, emissor, financiador e credor atual estão separados.
- [ ] Cada conclusão tem fonte oficial ou está marcada como pendente.
- [ ] Reclassificação por credor preservou o total das obrigações.
- [ ] Relatório e plano jurídico apontam para a pesquisa de fontes.
