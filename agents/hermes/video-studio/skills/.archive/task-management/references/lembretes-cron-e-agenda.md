# Rotinas de lembrete no Hermes — padrões validados (set/2026)

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
- Arquivo canônico: `~/MEGA/Documentos/ANIVERSARIOS.md` (tabela pessoa/data/relação). Novos aniversários: Igor manda por voz ("salva aniversário de X, dia DD/MM") → atualizar arquivo + criar 2 crons (aviso D-1 às 9h + aviso no dia às 9h) + registrar na memória.
- Padrão de nomes de job: "Aniversario <Nome> <DD-MM> aviso" e "HOJE Aniversario <Nome>".

## Conflitos de agenda do Igor (rotina fixa — checar antes de propor horários)
- Karatê: terça e quinta 20:00–22:00, sábado e domingo 09:00–11:00
- CrossFit: seg+qua ou qua+sex 20:00–21:00
- Musculação: seg (07–09h ou 22–23h), sáb/dom 12–14h
- Ao marcar compromissos (ex: com Tiago Braga), oferecer janelas fora desses blocos e SEMPRE 3 opções (flexibilidade fecha mais rápido).
