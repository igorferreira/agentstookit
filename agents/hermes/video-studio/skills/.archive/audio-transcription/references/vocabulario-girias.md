# Vocabulário de Gírias para Transcrição

Banco de conhecimento de gírias e termos coloquiais para melhorar a precisão de transcrições em português brasileiro.
Use como `initial_prompt` no faster-whisper quando o áudio for de contexto informal/rua.

## Drogas e relacionados

| Gíria | Significado |
|---|---|
| flor | maconha (qualidade superior) |
| Beck / bec / beque | cigarro de maconha |
| bolar | enrolar o cigarro de maconha |
| fumar / fumaça | usar maconha |
| onda / brisa | efeito da droga |
| boca | ponto de venda de drogas |
| corre | compra de drogas |
| prensado | maconha de baixa qualidade |

## Vocabulário de contexto — rua/festa

| Termo | Uso |
|---|---|
| copão | cerveja grande (copo de 500ml+) |
| gelada | cerveja |
| bora / vamo / vambora | vamos embora |
| tá ligado | entendeu? |
| mó | muito (ex: "mó calor") |
| trombar | encontrar alguém |

## Estratégia de prompt

Para áudios com muito ruído de rua e fala coloquial, usar `initial_prompt` com termos prováveis:

```
initial_prompt="flor, maconha, bec, beck, fumar, fumaça, onda, brisa, rua, viela, boca, buscar, pegar, comprar, bolar, gelada, copão, bora, trombar"
```

Isso reduz falsos cognatos fonéticos (ex: "lindando" → "lidando", "devava" → "devia") e melhora o acerto em gírias.
