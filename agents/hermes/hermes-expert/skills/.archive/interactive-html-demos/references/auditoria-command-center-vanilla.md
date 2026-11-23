# Auditoria antes de evoluir escritórios para Command Center

Use este gate quando uma demo de escritório virtual existente precisar evoluir para uma central operacional, sem perder personagens, mesas e gamificação.

## Restrições a confirmar

- Inspecionar a stack real antes de propor arquitetura.
- Se o projeto for HTML + CSS + JavaScript Vanilla, permanecer nessa stack.
- Não adicionar framework, biblioteca ou dependência sem necessidade demonstrada.
- Não recriar a aplicação; trabalhar incrementalmente sobre o código funcional.
- Não substituir o escritório por cards ou dashboard SaaS genérico.
- Não inventar modelo, ferramenta, custo, token, dependência, squad ou dado de backend ausente.

## Gate obrigatório: diagnóstico antes de código

Não editar arquivos até entregar o diagnóstico solicitado. Auditar todas as variantes, não apenas o template principal:

1. Arquivos HTML/CSS/JS envolvidos.
2. Estrutura atual da tela.
3. Criação dos agentes no DOM.
4. Modelo de memória/estado dos agentes.
5. Fluxo de atualização de estados e tarefas.
6. Posicionamento de agentes, mesas e etiquetas.
7. Zoom, pinch e persistência por orientação.
8. Tooltips, hover, tap, painéis e chat.
9. Origem dos dados e contratos existentes.
10. WebSocket, SSE, polling ou simulação por timers.
11. Listeners, `setInterval`, `setTimeout` e risco de duplicação.
12. Valores fixos, estilos inline e posicionamento absoluto.
13. Problemas de CSS e hierarquia visual.
14. Problemas de JavaScript e atualização integral do DOM.
15. Mobile: 320, 360, 375, 390, 412, 430 e 480 px.
16. Tablet, desktop, ultrawide e mudança de orientação.
17. Performance e escala para 20/50/100 agentes.
18. Código reutilizável versus refatoração necessária.
19. Arquitetura proposta + wireframes textuais.
20. Arquivos a modificar, fases, testes e riscos de regressão.

## Evidência mínima do diagnóstico

- Caminhos e linhas representativas, sem presumir comportamento.
- Matriz por família de template e por resolução.
- Capturas reais; HTTP 200 e análise estática não substituem QA visual.
- Separar fatos observados, hipóteses e propostas.
- Identificar explicitamente salas vazias, agentes cortados e contaminação entre variantes.

## Direção arquitetural Vanilla, sem overengineering

Só depois do diagnóstico, avaliar incrementalmente:

- `office-grid` com CSS Grid fluido para organizar estações; `position:absolute` apenas dentro da estação.
- Design tokens em `:root` para cor, espaçamento, tipografia, raio, sombra e z-index.
- `Agent Station` sem apagar personagem/mesa: nome, avatar, atividade, duração e status textual.
- Atualização somente do agente alterado em vez de reconstruir toda a workforce.
- Event delegation para reduzir listeners.
- Drawer/bottom sheet por tap no mobile; hover apenas como complemento no desktop.
- Resumo compacto da workforce e modos `Escritório`/`Operações` compartilhando o mesmo estado.
- Feed de atividade reutilizando eventos reais; sem criar polling ou dados fictícios.
- `prefers-reduced-motion`, foco visível, teclado, ARIA e alvos de toque de pelo menos 44 px.

## Regra de correção do usuário

Quando o usuário disser “cancela a anterior”, “essa” ou fornecer uma especificação substituta:

1. parar o escopo anterior;
2. não mesclar requisitos das duas versões;
3. registrar a anterior como cancelada;
4. tratar apenas a última especificação como fonte oficial;
5. reiniciar o gate de diagnóstico se a sequência exigida mudou.
