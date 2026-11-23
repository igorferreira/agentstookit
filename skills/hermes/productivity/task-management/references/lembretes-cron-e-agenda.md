# Rotinas de lembrete no Hermes — padrões validados (set/2026)

## Criar lembretes one-shot via a tool `cronjob_manage` (caminho validado no Hermes atual)
Para "me avisa no dia X" (cobranças, vencimentos, aniversários), o caminho direto pela tool é:

- `cronjob_manage(action="create", schedule="2026-10-05T09:00:00", prompt="...", name="...", deliver="origin")` — schedule aceita one-shot ISO absoluto; `repeat` fica `once` automaticamente.
- O job roda em sessão NOVA sem contexto do chat: o `prompt` tem que ser AUTOCONTIDO (quem, quanto, chave Pix/valor, link pronto, e a instrução do que entregar). Não escreva "como combinamos".
- Evite aspas duplas dentro do prompt (escapam mal no payload JSON); texto simples e direto é mais seguro.
- Confirme na resposta: `next_run_at`, `deliver`, `repeat: once`. Verificar com `action="list"` se houver dúvida.

## Link de WhatsApp que abre a conversa com mensagem pronta (wa.me)
Para lembrar o Usuário de cobrar/falar com alguém: gere o deep-link e ENTREGUE-O no lembrete (o Usuário clica e manda — o agente nunca envia a mensagem ao terceiro diretamente):

```
https://wa.me/<DDI+DDD+numero, so digitos>?text=<mensagem url-encoded>
```

- Gere o encoding SEMPRE por código (`urllib.parse.quote(msg)` no Python) — nunca encode à mão; `?` e acentos quebram se escritos direto no link.
- No prompt do cron, embuta o link JÁ ENCODADO por inteiro (o job não reprocessa).

## Criar lembretes one-shot via CLI (mais confiável que a tool cronjob sem `schedule`)
A tool `cronjob` exige `schedule` explicitamente e falha com erro genérico quando omitido. O caminho validado via terminal:

```
hermes cron create "2026-09-24T09:00:00" "PROMPT do lembrete" --name "Nome do job" --repeat 1
```

**Pitfalls do CLI (custaram várias tentativas):**
- O prompt é POSICIONAL logo após o schedule — NÃO usar `--` antes dele (rejeitado como argumento não reconhecido).
- Flags (`--name`, `--repeat`) vão DEPOIS do prompt.
- Emojis/acentos no prompt funcionam; em `--name` evitar (usar sem acento: "Aniversario Dona Graca 25-09 aviso").
- `--repeat 1` = one-shot (dispara e encerra).

## Agenda de aniversários
- Arquivo canônico: `~/MEGA/Documentos/ANIVERSARIOS.md` (tabela pessoa/data/relação). Novos aniversários: Usuário manda por voz ("salva aniversário de X, dia DD/MM") → atualizar arquivo + criar 2 crons (aviso D-1 às 9h + aviso no dia às 9h) + registrar na memória.
- Padrão de nomes de job: "Aniversario <Nome> <DD-MM> aviso" e "HOJE Aniversario <Nome>".

## Conflitos de agenda do Usuário (rotina fixa — checar antes de propor horários)
- Karatê: terça e quinta 20:00–22:00, sábado e domingo 09:00–11:00
- CrossFit: seg+qua ou qua+sex 20:00–21:00
- Musculação: seg (07–09h ou 22–23h), sáb/dom 12–14h
- Ao marcar compromissos (ex: com Tiago Braga), oferecer janelas fora desses blocos e SEMPRE 3 opções (flexibilidade fecha mais rápido).
