# Monitoramento Automático de Eventos Financeiros (Cron Jobs)

## Padrão: vigia semanal de site externo

Quando um evento financeiro depende de publicação externa (ex: dissídio, CCT, proposta de acordo), criar um cron job `no_agent=True` com script Python.

### Estrutura do script

```python
#!/usr/bin/env python3
"""
Vigia [NOME] — Checa se [EVENTO] foi publicado.
Silêncio total se não houver novidade.
"""
import json, os, re, urllib.request
from datetime import datetime

STATE_FILE = os.path.expanduser("~/.hermes/scripts/estado-[nome].json")
URL = "https://..."

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f: return json.load(f)
    return {"last_known_title": "", "last_check": None}

def save_state(state):
    with open(STATE_FILE, "w") as f: json.dump(state, f)

state = load_state()

try:
    html = fetch_page()
    title, url = find_relevant(html)
    
    if title and title != state["last_known_title"]:
        state["last_known_title"] = title
        state["last_check"] = datetime.now().isoformat()
        save_state(state)
        print(f"🚨 [EVENTO] — NOVIDADE!")
        print(f"📄 {title}")
        print(f"🔗 {url}")
    else:
        state["last_check"] = datetime.now().isoformat()
        save_state(state)
        # Silêncio = sem output → sem mensagem no Telegram
        
except Exception as e:
    print(f"⚠️ Erro: {e}")
```

### Regras

1. **Salvar script** em `~/.hermes/scripts/` com nome descritivo
2. **Salvar estado** em `~/.hermes/scripts/estado-<nome>.json` — rastreia o último título conhecido
3. **Silêncio total** quando não houver novidade (sem output = sem mensagem)
4. **Primeira execução**: grava o estado mas não notifica (só notifica mudanças)
5. **Criar cron job** com `no_agent=True` e `script=<nome>.py`

### Criar o cron job

```
cronjob(
    action="create",
    name="Vigia [NOME]",
    schedule="0 9 * * 1",      # toda segunda 9h
    script="vigia-[nome].py",
    no_agent=True,
    deliver="origin"
)
```

### Exemplo: Vigia CCT FEAAC 2026-2027

- Script: `~/.hermes/scripts/vigia-cct-feaac.py`
- Estado: `~/.hermes/scripts/estado-cct-feaac.json`
- Cron: `81954c198916`, toda segunda 9h
- Site: `https://feaac.org.br/category/convencoes-e-acordos-coletivos/`
- Procura: posts com "2026-2027" ou "assinada" no título

## Padrão: vigia diário de arquivo local (AVISOS.md)

Para monitorar mudanças em arquivos locais (ex: novas linhas no AVISOS.md):

- Script: `~/.hermes/scripts/verificar-avisos.py`
- Estado: `~/.hermes/scripts/estado-avisos.json`
- Cron: `029ab7cf9525`, todo dia 8h10
- Lógica: compara número de linhas da tabela de Log com o estado salvo
