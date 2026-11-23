# Auditoria operacional de escritórios realtime

Use esta matriz quando o usuário pedir o estado atual de vários escritórios. O objetivo é distinguir disponibilidade técnica de atividade real.

## Camadas independentes

1. **HTTP:** página local e pública respondem 200.
2. **Consumidor:** a página ou módulo carregado instancia `EventSource`. Audite scripts externos e módulos importados, não apenas o HTML inline.
3. **Produtor:** `/source-status?office=<id>` informa heartbeat recente e PID verificado.
4. **Evento:** `eventsSeen > 0` e `/snapshot?office=<id>` mostram evento correlacionável.
5. **Cobertura:** identifique se o heartbeat cobre só um recepcionista ou todos os especialistas.
6. **Simulação:** classifique como `ausente`, `presente mas bloqueada em runtime` ou `presente e executável`.
7. **Áudio:** informe se está desligado/ligado, se é opt-in e se houve fala real agente→agente.

## Regras de interpretação

- HTTP 200 prova somente disponibilidade da página.
- SSE conectado prova somente capacidade de receber eventos.
- Heartbeat prova somente que um produtor roteado está vivo.
- `eventsSeen > 0` prova histórico, não atividade neste exato instante; confronte timestamp/status.
- Um recepcionista ativo não transforma todo o escritório em ativo.
- Um adapter que bloqueia timers cenográficos evita execução, mas não equivale a remoção física do código.
- Só afirmar `realtime completo` quando consumidor, produtor, evento correlacionável, cobertura dos agentes e ausência de simulação estiverem verificados.

## Áudio opt-in

Áudio agente→agente deve permanecer desabilitado por padrão. Só tocar após habilitação manual explícita. Ao desligar: parar reprodução atual, limpar fila e bloquear novas falas, mantendo o realtime textual funcionando.
