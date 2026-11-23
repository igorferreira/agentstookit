# Métricas de resposta e validação de rascunhos

## Distinguir mensagens enviadas, rascunhos e relatos

Antes de analisar texto colado no chat, classifique-o como trecho do export, rascunho ainda não enviado ou relato do usuário. Pesquise no arquivo original toda citação e confirme remetente e timestamp; não use contexto ou estilo para adivinhar autoria. Trate relatos de acontecimentos fora do export como relato, não como evidência documental. Se o arquivo não cobre o período, declare a lacuna e não complete a cronologia por inferência.

## Métrica de latência por bloco

Agrupar rajadas em blocos: mensagens consecutivas do mesmo autor com gap ≤5min
= 1 bloco. Medir resposta BLOCO a BLOCO (não msg a msg):

- média, mediana, P25/P50/P75/P90 (min)
- % de blocos respondidos ≤5min, ≤30min, 1-3h, >3h
- comparar os dois lados com tamanho da amostra, distribuição e exclusões; P90 descreve a cauda das latências, mas não identifica quem está mais investido ou "corre atrás"

Exemplo de formato: `n=<blocos>, mediana=<min>, P75=<min>, P90=<min>, % até 30 min=<percentual>`. Apresente valores calculados como descrição da amostra; eles não provam sentimentos, intenção ou compromisso e não devem ser usados para desqualificar a percepção de ninguém.

Perguntas ("?") e emojis afetivos por autor podem ser contados se a definição for explícita e estável. São ocorrências visíveis, não métricas de engajamento, investimento ou afeto; apresente-as sem converter a diferença num veredito sobre a relação.

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