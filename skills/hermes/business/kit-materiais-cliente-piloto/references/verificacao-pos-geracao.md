# Verificação pós-delegação e pós-geração de artefatos (validado 04/09/2026)

Cenário: um `delegate_task` retornou `status=completed` com resumo otimista, mas
NENHUM arquivo foi criado — o subagente só leu referências e encerrou ("All").

## Regra

Após qualquer delegação OU geração de kit, verificar a existência REAL dos
artefatos antes de reportar sucesso ao Igor:

```python
from hermes_tools import terminal
from pathlib import Path

root = Path('/home/usuario/projetos/hermes-as-service')
esperados = [
    '07-apresentacoes/<NOME>.pptx',
    '07-apresentacoes/<NOME>.pdf',
    '06-audios-salvos/<ROTEIROS>.md',
    '08-kits-envio/<cliente>/MENSAGEM-E-ORDEM-DE-ENVIO.md',
]
for e in esperados:
    p = root / e
    print(('OK  ' if p.exists() else 'FALTA'), e)

# contagem de páginas/slides nos binários PDF
r = terminal('pdfinfo <PDF> | grep Pages', workdir=str(root))
print(r['output'].strip())
```

## Se algo faltar

- NÃO re-delegar imediatamente (o mesmo subagente pode falhar igual).
- Gerar direto no agente principal: `write_file` do script python-pptx
  (reusar helpers do script de referência) → rodar com `python3.12` →
  `libreoffice --headless --convert-to pdf` → auditoria visual → commit/sync.
- O transcript do subagente fica em
  `~/.hermes/cache/delegation/live/<deleg_id>/task-0.log` — `tail` nele mostra
  onde parou (neste caso: leu arquivos, "think All", final sem tool calls).

## Audit visual (2 rodadas)

1. `pdftoppm -png -r 50-80` + `montage -tile 4x2 -geometry 340x263+4+4`
2. `vision_analyze` perguntando explicitamente: cortes, sobreposições,
   texto ilegível, **erros de português e plurais** (FRENTE/FRENTES,
   TODAS AS FRENTES), nome correto da empresa (DGM Eletro, não DM).
