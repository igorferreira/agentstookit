---
name: skill-arquivada
description: Arquivadas (jurídico, condomínio, criativo, mlops): busque aqui antes da web.
---

# Carregador de skills arquivadas

Skills sem uso (nunca, ou há mais de 30 dias) foram **arquivadas** para poupar tokens: não aparecem no índice de skills, mas continuam no disco em `~/.hermes/skills/.archive/`.
Use esta skill quando a tarefa pedir uma capacidade que nenhuma skill ativa cobre (ex.: análise jurídica, síndico/condomínio, criação visual, mlops, integrações do OpenClaw).

## Como usar

1. **Busque** (não use IA, só o script; ~300 tokens de saída):
   ```bash
   python3 ~/.hermes/scripts/buscar-skill-arquivada.py <palavras da tarefa>
   ```
   Ele mostra as 3 melhores skills arquivadas com o caminho do `SKILL.md`. Para ver todos os nomes: `--listar`.
2. **Carregue**: leia o `SKILL.md` indicado com `read_file` (o `skill_view` não enxerga a pasta `.archive`) e siga as instruções dele como se fosse uma skill ativa.
   Se ele citar arquivos de apoio (`references/`, `scripts/`), leia-os no mesmo diretório.
3. **Se vai usar sempre**, restaure: `python3 ~/.hermes/scripts/buscar-skill-arquivada.py --restaurar <nome>` (volta ao índice na próxima sessão, na raiz de `~/.hermes/skills/`).
4. Se nada casar, diga ao Usuário que não há skill arquivada para isso e siga sem skill.

## Regras

- Não restaure em lote nem "por precaução": cada skill ativa custa tokens em todo prompt.
- Lista de referência (com categoria original): `~/.hermes/docs/skills-arquivadas-INDEX.md`.
