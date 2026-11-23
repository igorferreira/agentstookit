# Sequência e Confirmação de Envio em Cadeia de Imagens

## Regra de Operação

Quando o usuário enviar sequências de capturas de tela, comprovantes ou evidências de chat em mensagens sucessivas (ex.: "salva esse comprovante", "salva a primeira parte do print", "salva a segunda parte"):

1. **Atribuição Correta de Mídia:**
   - Cada arquivo de mídia recebido do Telegram fica temporariamente no cache local (`/home/igorferreira/.hermes/cache/images/img_*.jpg`).
   - Mapear cada imagem recebida para o seu respectivo arquivo físico final antes de vincular ou gerar o resumo de metadados.

2. **Unificação de Diálogos Multipartes:**
   - Em registros de atendimento ou chats com suporte (ex.: RecargaPay, bancos, operadoras), unificar as imagens sequenciais num único relatório/dossiê documental `.md` indicando os números de protocolo, carimbos de data/hora e falas transcritas.

3. **Confirmação e Atualização Imediata:**
   - Não adiar o salvamento ou a escrita em disco esperando que o usuário peça uma segunda vez. Cada imagem processada deve ser copiada para a pasta mensal canônica do ano/mês vigente e ter seus metadados persistidos.
