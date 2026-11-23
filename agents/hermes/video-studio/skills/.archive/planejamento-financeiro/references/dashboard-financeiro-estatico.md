# Dashboard financeiro estático — contrato e checklist

## Objetivo

Painel de consulta derivado do Markdown/YAML canônico do fluxo de caixa, sem banco de dados e sem edição direta pelo frontend.

## Regras obrigatórias

- Markdown/YAML é a única fonte da verdade.
- Gerar JSON minimizado por Python; manter fontes financeiras brutas fora do diretório servido.
- Usar aritmética monetária precisa (`Decimal` ou equivalente).
- Nunca transformar dado ausente em zero; distinguir confirmado, parcial, estimado, pendente e não localizado.
- Testar parser YAML, esquema, valores monetários, meses, CDB, cenários, reconciliação, geração determinística, allowlist de dados e servidor local.
- Falhar fechado em divergência material não explicada e preservar o último artefato aprovado.
- Exibir origem, versão/cenário, data da fonte e horário de geração.
- Bind local em `127.0.0.1`; ngrok somente por habilitação explícita.
- Fazer revisão pós-implementação completa de código, testes, cálculos, dados, segurança, responsividade, gráficos e regeneração.
- Salvar evidências em relatório de reconciliação e relatório de revisão.

## Critério de pronto

Abrir a página não basta. O dashboard só é aprovado após testes automatizados, reconciliação sem divergência material não explicada e revisão completa documentada.