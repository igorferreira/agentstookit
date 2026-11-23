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
- **Feedback obrigatório:** Sempre informar ao usuário a classificação ("Incluído na tarefa atual", "Adicionado à fila" ou "Tarefa atual cancelada").
- **Continuidade automática:** Ao concluir uma tarefa, iniciar imediatamente o próximo item da fila.
