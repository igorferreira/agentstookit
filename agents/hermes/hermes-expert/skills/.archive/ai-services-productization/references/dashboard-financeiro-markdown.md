# Dashboard financeiro estático alimentado por Markdown

## Pipeline validado

1. Ler o Markdown/YAML canônico.
2. Validar esquema e campos obrigatórios.
3. Calcular com precisão monetária (`Decimal` ou equivalente).
4. Reconciliar com as fontes e interromper em divergência material.
5. Minimizar dados: retirar CPF, Pix, contas, cartões completos, IDs, credenciais e comprovantes.
6. Gerar JSON determinístico e HTML/CSS/JS Vanilla em diretório separado das fontes.
7. Executar testes automatizados.
8. Servir apenas em `127.0.0.1` por padrão.
9. Fazer revisão final de código, testes, números, segurança e layout desktop/mobile.
10. Registrar evidências e declarar `APROVADO`, `APROVADO COM RESSALVAS` ou `REPROVADO`.

## Gates mínimos

- Parser/YAML e entradas inválidas.
- Precisão de centavos.
- Cenários, rendimento e limite inferior do CDB em zero.
- Regra de consignado e demais transições temporais.
- Idempotência do JSON.
- Varredura de dados sensíveis no artefato público.
- `py_compile` e `node --check`.
- HTTP 200, CSP e `Cache-Control: no-store`.
- Responsividade em desktop, celular retrato e celular paisagem.

## Limitação importante

Se a inspeção visual interativa depender de autorização manual do navegador e essa autorização não ocorrer, não afirmar aprovação visual total. Registrar a ressalva e manter o artefato como MVP técnico até a revisão ser concluída.

## Dependências de teste

Se `pytest` não estiver disponível, usar `unittest` da biblioteca padrão, preservando a cobertura dos gates em vez de eliminar os testes.
