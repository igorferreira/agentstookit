# Métricas de resposta e rascunhos do Igor — lições da sessão 07-08/09/2026

## Pitfall: rascunhos ditados não são dados do export

Igor costuma ditar mensagens que PRETENDE enviar ("devo mandar assim?") antes de
compartilhar o export real. Se ele depois diz "olha o que rolou" e cola texto,
distinguir: o texto é o export (dado) ou é o rascunho dele (plano)? Erros
cometidos em sessão real (2× na mesma madrugada):
1. Analisar o rascunho "bora malhar / eu passo aí pra te pegar" como se fosse
   mensagem RECEBIDA dela — quando era o que ele estava escrevendo.
2. Atribuir a ela o elogio "vc é muito forte" quando o grep na linha 2081-2082
   mostrava autor `igor ferreira`.

Regra dura:
- Toda atribuição de autoria exige `grep -n "trecho"` no .txt do export.
- O que Igor relata em texto livre é HIPÓTESE a validar contra o export.
- Se o export não cobre o período citado (ex: msgs de hoje após a hora do
  arquivo), declarar ausência de dado — nunca reconstruir por inferência.

## Métrica canônica de tempo de resposta (validada pelo Igor)

Agrupar rajadas em blocos: mensagens consecutivas do mesmo autor com gap ≤5min
= 1 bloco. Medir resposta BLOCO a BLOCO (não msg a msg):

- média, mediana, P25/P50/P75/P90 (min)
- % de blocos respondidos ≤5min, ≤30min, 1-3h, >3h
- comparar os dois lados: quem é mais rápido no P90 (revela quem "corre atrás"
  nos atrasos, vs a mediana que mostra o ritmo normal)

Exemplo validado (n=156 blocos): mediana 1min, P75 10min, P90 44min,
85% ≤30min — matou a percepção de "ela demora sempre" (era 15% dos casos
com peso emocional 10×).

Perguntas ("?") e emojis afetivos por autor também são métricas de
engajamento que Igor aceita bem — perguntas 51×20 e emojis 16×3 contaram
a história da assimetria de investimento.

## Snippet Python pronto (parse + blocos)

```python
import re, statistics
from datetime import datetime
txt = open(f'{pasta}/Conversa do WhatsApp com A.txt', encoding='utf-8').read()
txt = re.sub(r'[\u200e\u200f\u202a-\u202e\u2066-\u2069]', '', txt)  # bidi cleanup
pat = re.compile(r'^(\d{2}/\d{2}/\d{4}) (\d{2}:\d{2}) - ([^:]+): (.*)$')
msgs = [(datetime.strptime(f'{d} {t}', '%d/%m/%Y %H:%M'), w.strip(), b)
        for d, t, w, b in (m.groups() for m in map(pat.match, txt.splitlines()) if m)]
def autor(m): return 'IGOR' if 'igor' in m[1].lower() else 'ELA'
# blocos: rajada = msgs do mesmo autor com gap <= 5min
blocks = []
for m in msgs:
    if blocks and blocks[-1][2] == autor(m) and (m[0]-blocks[-1][1]).total_seconds() <= 300:
        blocks[-1] = (blocks[-1][0], m[0], autor(m))
    else:
        blocks.append((m[0], m[0], autor(m)))
# resposta de ELA a blocos do IGOR (e vice-versa), em minutos
resp = {k: [] for k in ('IGOR','ELA')}
for i in range(1, len(blocks)):
    dt = (blocks[i][0]-blocks[i-1][1]).total_seconds()/60
    if 0 < dt < 720:
        resp[blocks[i][2]].append(dt)
```