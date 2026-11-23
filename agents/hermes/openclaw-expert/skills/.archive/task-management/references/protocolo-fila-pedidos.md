# Protocolo de Fila e Controle de Pedidos

Referência operacional para governança e execução de pedidos em fila cronológica estrita, conforme estabelecido em `~/clawd/PROTOCOLO_FILA_E_CONTROLE_DE_PEDIDOS.md`.

## 🎯 Categorias de Mensagens Recebidas

Quando uma nova mensagem chegar durante uma tarefa em andamento, classifique-a obrigatoriamente:

1. **PARAR:** Cancela, interrompe ou substitui a tarefa atual.
   - *Ação:* Interrompa com segurança, informe o que foi cancelado e inicie a nova solicitação.
2. **INCLUIR:** Complementa, corrige ou adiciona requisitos à tarefa atual.
   - *Ação:* Incorpore os requisitos na execução corrente, preservando o trabalho válido já feito.
3. **ENFILEIRAR:** Pedido novo e independente sem ordem de parada.
   - *Ação:* Mantenha a tarefa atual em execução, registre o novo pedido no fim da fila (`~/clawd/PEDIDOS.md`) e execute-o na ordem de chegada.
4. **DÚVIDA OU STATUS:** Pergunta sobre o andamento sem cancelamento.
   - *Ação:* Informe o status resumido e continue a tarefa atual. Se exigir novo trabalho, adicione à fila.

## 📋 Regras de Execução

- **Ordem cronológica:** Nunca inverter ou pular pedidos.
- **Monotarefa:** Apenas uma tarefa principal em execução por vez.
- **Estados obrigatórios:** `[EM EXECUÇÃO]`, `[NA FILA]`, `[CONCLUÍDO]`, `[CANCELADO]`.
- **Registro obrigatório de horários (Início e Fim):** Toda tarefa deve registrar compulsoriamente o horário exato de início e de término (HH:MM), tanto na tabela de `~/clawd/PEDIDOS.md` quanto no ciclo do board Kanban.
- **Envio Obrigatório do Link do Kanban:** Em TODA resposta de status, relatório intermediário ou conclusão de pedidos entregue ao Igor, incluir OBRIGATORIAMENTE os links de acesso ao board Kanban:
  - **Web / Celular (Ngrok):** `https://f848-2804-1b3-7142-f0bf-87c4-8f2-1a41-4bad.ngrok-free.app/kanban.html`
  - **Local PC:** `http://localhost:9119/kanban` (Dashboard nativo) ou `http://localhost:8766/kanban.html`
- **Feedback obrigatório:** Sempre informar ao usuário a classificação ("Incluído na tarefa atual", "Adicionado à fila" ou "Tarefa atual cancelada").
- **Continuidade automática:** Ao concluir uma tarefa, iniciar imediatamente o próximo item da fila.

## 🗂️ Integração Operacional com o Board `Default` (Hermes Kanban)

O rastreamento de pedidos opera sincronizado com o board nativo **`default`** do Hermes Kanban (banco SQLite durável), com espelho em `~/clawd/PEDIDOS.md`:

1. **Garantir o Board Ativo:**
   ```bash
   hermes kanban boards switch default
   ```
2. **Formato da Tabela Diária em `PEDIDOS.md`:**
   ```markdown
   | # | Início | Fim | Pedido | Status | ID Kanban |
   |---|---|---|---|---|---|
   | 1 | 09:46 | 09:54 | Descrição da tarefa | ✅ CONCLUÍDO — resumo | `t_xxxxxxxx` |
   ```
3. **Mapeamento de Ciclo de Vida:**
   - **`[NA FILA]`**: Criar a tarefa no board com status `ready`/`todo`:
     ```bash
     hermes kanban create "<título do pedido>" --body "<detalhes e requisitos>" --priority 0
     ```
   - **`[EM EXECUÇÃO]`**: Identificar o ID gerado (`t_xxxxxxxx`), registrar o horário de início na tabela e iniciar com status `running`.
   - **`[CONCLUÍDO]`**: Finalizar com sumário explícito da entrega e registrar o horário de término em `PEDIDOS.md`:
     ```bash
     hermes kanban complete <task_id> --summary "<resumo das ações e verificações>"
     ```
   - **`[CANCELADO]`**: Arquivar ou registrar o cancelamento com justificativa:
     ```bash
     hermes kanban archive <task_id>
     ```
4. **Comandos de Consulta e Auditoria:**
   - Listar pedidos em aberto/prontos: `hermes kanban list`
   - Listar pedidos finalizados: `hermes kanban list --status done`
   - Estatísticas por status: `hermes kanban stats`
