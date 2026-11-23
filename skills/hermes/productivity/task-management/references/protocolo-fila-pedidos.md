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

### Complemento de um pedido já enfileirado

Se Usuário acrescentar um dado ou corrigir requisito de um pedido que já está `NA FILA` (em vez do item ativo):

1. Localize o pedido exato pelo ID no board `default` e em `PEDIDOS.md`; não transfira a correção para a tarefa atualmente em execução.
2. Registre a proveniência do dado: diferencie o que está visível no documento do que Usuário informou.
3. Acrescente o contexto ao card exato (comentário ou edição do corpo) e atualize apenas a linha correspondente em `PEDIDOS.md`.
4. Preserve ordem, status `todo`, dependências e campos de início/fim ainda vazios; releia ambos para confirmar a sincronização.
5. A clarificação apenas complementa o pedido: não o inicia, não remove dependências e não autoriza furar a fila. Só uma autorização explícita para aquele card pode alterar a prioridade, e dependências reais de dados continuam valendo.
- **Estados obrigatórios:** `[EM EXECUÇÃO]`, `[NA FILA]`, `[CONCLUÍDO]`, `[CANCELADO]`.
- **Registro obrigatório de horários (Início e Fim):** Toda tarefa deve registrar compulsoriamente o horário exato de início e de término (HH:MM), tanto na tabela de `~/clawd/PEDIDOS.md` quanto no ciclo do board Kanban.
- **Envio Obrigatório do Link do Kanban:** Em toda resposta de status ou conclusão, incluir link do board. Para Web/Celular, ler a URL vigente em `~/MEGA/Comprovantes/fluxo_caixa/dashboard/URL-TUNEL-CANONICO.md`, montar o caminho `/kanban.html` e validar a resposta antes de enviar; URLs de túnel mudam e não devem ser fixadas nesta skill. Se não houver endpoint público respondendo, dizer isso claramente e fornecer o link local `http://localhost:8766/kanban.html` sem alegar que está ativo. O dashboard nativo `http://localhost:9119/kanban` só deve ser apresentado como disponível se verificado.
- **Feedback obrigatório:** Sempre informar ao usuário a classificação ("Incluído na tarefa atual", "Adicionado à fila" ou "Tarefa atual cancelada").
- **Continuidade automática:** Ao concluir uma tarefa, iniciar imediatamente o próximo item da fila.

## 🗂️ Integração Operacional com o Board `Default` (Hermes Kanban)

O rastreamento de pedidos opera sincronizado com o board nativo **`default`** do Hermes Kanban (banco SQLite durável), com espelho em `~/clawd/PEDIDOS.md`:

1. **Garantir o Board Ativo:**
   ```bash
   hermes kanban boards switch default
   ```
2. **Formato da Tabela Diária em `PEDIDOS.md`:**

   **Edição segura:** Antes de atualizar um pedido, releia a linha-alvo e faça patch somente nela; não reescreva o arquivo inteiro, pois outro pedido pode ser anexado em paralelo. Depois, releia e confirme status, ID e horários.
   ```markdown
   | # | Início | Fim | Pedido | Status | ID Kanban |
   |---|---|---|---|---|---|
   | 1 | 09:46 | 09:54 | Descrição da tarefa | ✅ CONCLUÍDO — resumo | `t_xxxxxxxx` |
   ```
3. **Mapeamento de Ciclo de Vida:**

   **Execução direta vs. worker automático:** Antes de executar, inspecione o estado do card. Se `create --help` oferecer opção para criar sem atribuição, use-a para trabalho na sessão principal; caso contrário, após criar o card, recupere imediatamente a autoatribuição com o comando `reassign ... none --reclaim` abaixo e faça `claim` pelo ID exato antes de editar arquivos.
   - **`[NA FILA]`**: Releia `PEDIDOS.md` e o board, identifique os pedidos anteriores ainda abertos e crie o novo card com esses predecessores vinculados já na chamada inicial (`--parent <id>` no CLI ou `parents=[...]` na ferramenta). A dependência mantém o card em `todo` até a fila liberar; se o predecessor mais recente já fizer parte de uma cadeia serial verificada, basta depender dele. Depois, leia o card de volta e confirme status `todo`, parents corretos e ausência de worker/run ativo antes de espelhar em `PEDIDOS.md`.

     **Pitfall:** não omita o parent supondo que um card sem assignee ficará em `todo`: `create` pode deixá-lo em `ready`, permitindo despacho automático. Não crie primeiro como `ready` para bloquear depois; `block --kind dependency` sem parent aberto pode ser convertido em `needs_input` e registrar um run bloqueado, o que representa mal uma espera cronológica.

     ```bash
     hermes kanban --board default create "<título do pedido>" --body "<detalhes e requisitos>" --parent <id-do-predecessor>
     ```

     Se não houver pedido anterior aberto e este for o próximo item autorizado a iniciar, crie-o normalmente e comece apenas após confirmar o ID e o estado no board.
   - **`[EM EXECUÇÃO]`**: Identificar o ID gerado (`t_xxxxxxxx`), registrar o horário de início na tabela e iniciar com status `running`. Se o card foi atribuído a `default` e um worker automático já começou, recupere apenas o ID exato com `hermes kanban --board default reassign <task_id> none --reclaim --reason 'Execução direta nesta sessão'`, depois `hermes kanban --board default claim <task_id>`.
   - **`[CONCLUÍDO]`**: Verificar os artefatos, registrar o horário de término em `PEDIDOS.md` e fechar pelo agente-pai com resultado explícito:
     ```bash
     hermes kanban --board default complete <task_id> --result "<entrega e verificações>"
     ```
   - **`[CANCELADO]`**: Arquivar ou registrar o cancelamento com justificativa:
     ```bash
     hermes kanban archive <task_id>
     ```
4. **Comandos de Consulta e Auditoria:**
   - Listar pedidos em aberto/prontos: `hermes kanban list`
   - Listar pedidos finalizados: `hermes kanban list --status done`
   - Estatísticas por status: `hermes kanban stats`

## ⚠️ Pitfalls do CLI do Kanban (scripting via terminal)

- **`--board <slug>` vem ANTES do subcomando** — é flag do comando top-level: `hermes kanban --board default create '...'`. Depois do subcomando, é rejeitado como argumento não reconhecido.
- **Valores com R$ em ASPAS SIMPLES** — em aspas duplas o bash expande `$1`, `$2`..., e `R$107` vira `R07` no título gravado. Vale para qualquer texto com `$` seguido de dígito.
- **Subagente `delegate_task` NÃO pode fechar tarefa do Kanban** (contexto filho não muta o board). Ao despachar um filho cujo trabalho deve fechar card, tire o `complete` do goal dele e rode `hermes kanban --board default complete <id> --result ...` no PAI depois de verificar a entrega.
- **Nunca usar `claim` sem ID específico** — sem ID ele pode pegar tarefa alheia pronta na fila; se errar, reverter com `reclaim`.
- **O link ngrok do board MUDA a cada restart do túnel** — não fixe a URL; leia a vigente em `~/MEGA/Comprovantes/fluxo_caixa/dashboard/URL-TUNEL-CANONICO.md`, valide o endpoint com `curl` antes de enviar e não armazene essa URL transitória na memória.
- **`complete <id>` falha com "unsatisfied parent dependencies" quando os parents são só gate de fila** — se o pedido já foi executado diretamente por autorização específica do Usuário, desvincule cada parent com `hermes kanban --board default unlink <parent> <child>` (laço, um por parent) e então complete; `complete --force` encerra o card apesar dos parents quando a execução direta está justificada.
- **`complete <id>` também falha com "a live worker is running it"** — o dispatcher pode dar spawn no card assim que os parents são desvinculados. Se o trabalho real foi feito na sessão principal, use `complete <id> --force --result "..."` com o motivo explícito (fecha o run do worker e completa); deixar o worker rodar duplica o trabalho.
- **Perfil especialista que falha no spawn não é card quebrado** — run com erro de adapter/token do gateway: `reassign <id> <perfil-executável> --reclaim --reason "..."` preserva corpo e dependências e o card volta a fluir no perfil que funciona; não mexa em credenciais para forçar o spawn. Card pronto após `reclaim` NÃO precisa de `unblock` — a chamada falha com "cannot unblock" porque ele já está pronto.
