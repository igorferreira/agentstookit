# Diário de Conversas — Cronologia Automática

> **Criado:** 13/08/2026 04:30 (quinta)
> **Skill:** `cronologia-automatica`
> **Cron job ID:** `5e02d98f0186`

## 📁 Estrutura

```
~/MEGA/Documentos/diario_conversas/
├── README.md                          # documentação
├── AAAA-MM-DD.md                      # 1 arquivo por dia
├── scripts/
│   └── gerar_resumo.py                # script do cron noturno
└── (templates/ — opcional)
```

## ⚙️ Setup (já feito)

```bash
# 1. Pasta criada
mkdir -p ~/MEGA/Documentos/diario_conversas/scripts

# 2. Script de resumo (idempotente — pode rodar várias vezes)
cat > ~/MEGA/Documentos/diario_conversas/scripts/gerar_resumo.py << 'EOF'
from datetime import date, datetime
from pathlib import Path

DIARIO_DIR = Path('/home/igorferreira/MEGA/Documentos/diario_conversas')

def main():
    hoje = date.today()
    diario_path = DIARIO_DIR / f"{hoje.strftime('%Y-%m-%d')}.md"

    if not diario_path.exists():
        diario_path.write_text(f"""# Diário de Conversas — {hoje.strftime('%d/%m/%Y')} ({hoje.strftime('%A')})

> **Início:** {datetime.now().strftime('%H:%M:%S')}
> **Sessões:** 0
> **Mensagens:** 0

---

""")

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z (%A)')
    content = diario_path.read_text()

    if "## 📋 Resumo automático do dia" not in content:
        with diario_path.open('a') as f:
            f.write(f"""

---

## 📋 Resumo automático do dia — {timestamp}

> Gerado por cron às 23:00.

### Atividades do dia

_(em construção)_

### Pendências abertas

_(em construção)_

---

_Última atualização: {timestamp}_
""")

    print(f"✅ Diário atualizado: {diario_path}")

if __name__ == '__main__':
    main()
EOF

# 3. Cron job (todo dia às 23:00)
hermes cronjob create \
  --name "Resumo Diário de Conversas (cron noturno)" \
  --prompt "Execute o script:
python3.12 /home/igorferreira/MEGA/Documentos/diario_conversas/scripts/gerar_resumo.py
Após executar confirme atualização. NÃO modifique o script. NÃO crie outros arquivos." \
  --schedule "0 23 * * *"
```

## 🤖 Comportamento do agente

### Triggers automáticos

| Quando Igor disser | Ação |
|---|---|
| "checkpoint" | Adicionar checkpoint manual com timestamp + breve resumo |
| "resumo do dia" | Mostrar conteúdo do arquivo `AAAA-MM-DD.md` |
| "histórico [data]" | Mostrar conversa de `AAAA-MM-DD.md` |
| "fechar sessão" | Marcar timestamp final + sumário |

### Detecção passiva

- A cada ~10 mensagens, criar checkpoint automático
- Em início de conversa: criar/abrir arquivo do dia
- Em fim de conversa (despedida explícita): timestamp final

## 📋 Formato do checkpoint

```markdown
## HH:MM — Tópico resumido

**Igor disse:**
> ...

**Hermes respondeu:**
- ...

**Ações executadas:**
- [x] Ação 1
- [x] Ação 2

**Decisões:**
- Decisão X tomada

---
```

## 🔧 Comando manual

```bash
# Adicionar checkpoint ao diário do dia
TS=$(date '+%Y-%m-%d %H:%M:%S %Z (%A)')
DIARIO=~/MEGA/Documentos/diario_conversas/$(date '+%Y-%m-%d').md
cat >> $DIARIO << EOF

## ${TS} — [Tópico]

**Igor pediu:**
> [frase]

**Ações:**
- [x] [ação executada]

---
EOF
```

## ⚠️ Privacidade

- Mantido local em `~/MEGA/Documentos/`
- NÃO sincronizar automaticamente com cloud (pode ter info sensível)
- Pode conter decisões financeiras e contexto pessoal

## 📝 Histórico

- **13/08/2026 04:30** — v1.0 criado por Hermes Agent
  - Pasta criada
  - README.md
  - Script `gerar_resumo.py`
  - Cron job `5e02d98f0186` (todo dia 23:00)
  - Primeiro diário (`2026-08-13.md`) populado manualmente com 8 tópicos da sessão