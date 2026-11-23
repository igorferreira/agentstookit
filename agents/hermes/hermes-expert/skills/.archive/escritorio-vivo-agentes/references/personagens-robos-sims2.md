# Personagens e camadas visuais (Sims 2) — lições da rodada 11/09/2026

## Requisito do Igor (expresso, cobrado com print)
Cada agente é um MINI ROBÔ (não bolinha genérica):
- cabeça quadrada colorida com antena brilhante e 2 olhos LED
- plaquinha com NOME em cima da cabeça
- sentado em cadeira de escritório atrás da mesa

## CSS validado (v5, rodada 11/09)
- `.robo` (34x44px) com `--rc` = cor do agente
  - `.nome`: plaquinha em cima da cabeça (font .55rem, bg rgba(0,0,0,.55), borda na cor do robô)
  - `.antena`: pulso animado; fica dourada em `.falando`
  - `.cabeca`: quadrada 30x24 com gradiente color-mix; `.olhos` = 2 LEDs ciano piscando (animation blink 4s)
  - `.corpo` + `.braco.e/.d`
- Estados: `.sentado` (corpo encurtado), `.andando` (bob .35s), `.falando` (outline dourado)
- Estação: `.estacao` > `.mesa` (z=7) + `.cadeira` (z=4, atrás)
- CAMADAS (o bug que custou 3 rodadas): cadeira z=4 → mesa z=7 → robô SENTADO z=8 com `top` tal que a cabeça/plaquinha ficam ACIMA da mesa e a parte de baixo do corpo fica levemente atrás dela. Robô andando z=8 também.
- Posição sentado: `left = st.x+32; top = st.y-16` (relativo à estação em st.x, st.y)

## Sequência de QA que valida isso
1. headless screenshot 1400x900
2. vision_analyze perguntando especificamente: "robôs com plaquinha de nome na cabeça, sentados em cadeiras atrás das mesas?"
3. Iterar camadas até o print mostrar: cadeira atrás → robô → mesa na frente

## Falha comum
Substituir o bloco CSS do personagem antigo (.agent/.agente-s) por regex e APAGAR junto o CSS da estação (.mesa/.cadeira) — as mesas somem da tela. Sempre re-verificar que `.mesa{` e `.cadeira{` existem no HTML final.