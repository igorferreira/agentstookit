# Arquivamento por cliente — TimeAutomático

## Convenção canônica

Todo material criado, enviado ou recebido deve ficar na pasta individual do cliente no projeto TimeAutomático no MEGA. Use diretórios exclusivamente em `snake_case`, minúsculos e sem acentos:

```text
timeautomatico/clientes/vieira_da_costa/
├── INDEX.md
├── apresentacoes/
├── audios/
├── registros/
└── fontes/
```

## Regras

- Apresentações destinadas ao cliente devem ser entregues em PDF; PPTX fica preservado apenas em `fontes/`.
- Todo envio gera ou atualiza um registro datado em `registros/` com destinatário, materiais, formato e status.
- Manter `INDEX.md` individual e índice geral de clientes.
- Nunca misturar materiais, nomes ou possíveis clientes em apresentação personalizada.
- Nunca apagar versões anteriores; usar data compacta `AAAAMMDD`.
- Ao migrar estrutura, validar diretórios com `^[a-z0-9]+(?:_[a-z0-9]+)*$`.
