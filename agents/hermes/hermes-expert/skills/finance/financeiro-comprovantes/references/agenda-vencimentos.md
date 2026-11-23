# Agenda de vencimentos — formato canônico

## Quando produzir

Quando o usuário pedir uma **agenda**, **calendário**, **cronograma de vencimentos**, **lista de contas a pagar ordenada por data** ou **visão geral de todas as obrigações** com status de pagamento.

## Estrutura

O documento deve conter:

1. **Mês atual (em aberto)**: cartões + contas fixas + demais obrigações, separados por tipo, ordenados por vencimento.
2. **Meses anteriores do mesmo ano**: resumo ou tabela compacta com status ✅ Pago. Se houver itens não pagos em mês anterior, destacá-los em vermelho/em separado.
3. **Meses seguintes (projeção)**: obrigações já contratadas (parcelamentos `x/y`, contratado futuro, compromissos conhecidos). Marcar valores provisórios com ◐.
4. **Resumo por mês**: tabela agregada com total mínimo estimado.
5. **Cartões sem informação documentada**: lista separada — não significa saldo zero.
6. **Observações relevantes**: home equity, VALLO, custo de vida, eventos futuros.

## Fontes a consolidar

- Para o **mês atual e passados**: `AAAA-MM_00_CONTROLE_PAGAMENTOS.md` e `AAAA-MM_00_DIVIDA.md`.
- Para **projeções futuras**: `_Controle_Anual/AAAA_00_CONTRATADO_FUTURO.md` e fichas de parcelamento `x/y` das faturas.
- Para **contas fixas recorrentes**: `MAPA-CUSTO-VIDA.md` (condomínio, luz, gás, telefone, academias, assinaturas, combustível).
- Para **limites e emissor**: relatório simplificado e inventário de cartões.

## Regras

- **Não projetar valores sem origem**: faturas futuras só entram com valor se houver linha `x/y` documentada, contrato de parcelamento ou registro em contratado-futuro. Caso contrário, usar `Indefinido` com ⬜ Aguardar fechamento.
- **Não tratar ausência como zero**: cartões sem fatura localizada entram numa seção à parte, não no total.
- **Separar cartão de conta fixa**: cartões têm seção própria; contas fixas recorrentes (condomínio, luz, etc.) vão em seção separada.
- **Marcar data-base de valores provisórios**: faturas abertas que podem mudar até o fechamento devem ter `~` ou nota explicitando que o valor é provisório.
- **Contas fixas sem vencimento exato**: usar `~10/08` (aproximado) quando o dia for conhecido mas não houver boleto emitido. Se o dia for totalmente desconhecido, usar `Mensal` e agrupar abaixo da tabela principal.
- **Total por mês**: sempre incluir dois totais — cartões mínimo e fixas recorrentes — e um total geral com ressalva de que pode ser maior quando faturas fecharem.
- **Legenda**: ✅ Pago | ⬜ Em aberto | ◐ Provisionado/parcial | — Não se aplica.
- **Incluir custo de vida fixo como referência**: mesmo que não seja cobrado em boleto (ex.: assinaturas de IA, academias), listar com valor estimado para dar visão completa do fluxo mensal.
- **VALLO e outros benefícios**: não entram como despesa; mencionar em observações como recurso disponível.
- **Home equity**: não incluir na agenda até contratação confirmada; mencionar em observações como pendente.
- **Quando houver dúvida sobre vencimento**: usar o cadastro histórico e marcar `a confirmar`; o nome do arquivo não deve conter vencimento inferido que não apareça na captura.

## Arquivo destino

Salvar em:
```
/home/usuario/MEGA/Comprovantes/2026/_Controle_Anual/AGENDA-VENCIMENTOS-2026.md
```

O nome inclui o ano para permitir versões anuais sem sobrescrever.

## Agendas mensais individuais

Além da agenda anual consolidada, criar um `AGENDA.md` dentro de cada pasta mensal:

```
/home/usuario/MEGA/Comprovantes/2026/2026_08_AGOSTO/AGENDA.md
/home/usuario/MEGA/Comprovantes/2026/2026_09_SETEMBRO/AGENDA.md
...
```

Cada agenda mensal contém apenas aquele mês: cartões (com valores) + contas fixas recorrentes + parcelas conhecidas. Incluir também a capacidade financeira (CLT + VALLO − custo de vida = folga para cartões).

**Diferença para o CONTROLE_PAGAMENTOS.md:** a agenda é mais visual, enxuta e de consulta rápida. O controle é o registro canônico de auditoria com links e comprovantes.

## Lembrete automático diário (cron + script)

Quando o usuário pedir lembretes automáticos de vencimento, implementar usando:

### Arquitetura

```
~/.hermes/scripts/
├── verificar-vencimentos.py   ← script no_agent=True
└── dados-vencimentos.json     ← cadastro de contas
```

### Script

- `verificar-vencimentos.py` (no_agent=True): lê o JSON, gera vencimentos do mês atual, filtra os que vencem em 0–5 dias, exibe mensagem formatada.
- Use `FAKE_DATE=YYYY-MM-DD` para testar sem alterar o cron.
- Use exit 0 com stdout vazio = silêncio (nada a vencer). Stdout não vazio = mensagem entregue pelo cron.
- Deduplicar cartões: se houver entrada específica em `meses_especificos`, pular a entrada genérica de `cartoes_padrao` que não tem valor.

### Cron job

Criar com `action=create`, `no_agent=True`, `script=verificar-vencimentos.py`, `schedule="0 8 * * *"`, `deliver="telegram"`.

### Cadastro (dados-vencimentos.json)

O JSON tem três seções:

- `recorrentes`: contas fixas que se repetem todo mês (condomínio, luz, academias, assinaturas IA, etc.). Cada uma tem nome, dia, valor e categoria.
- `cartoes_padrao`: cartões com dia de vencimento típico, sem valor fixo — servem de fallback quando não há entrada específica.
- `meses_especificos`: valores conhecidos para um mês específico (fatura fechada, parcela x/y, empréstimo). Incluir ano, mês, dia, valor e categoria.

### Manutenção

- Ao registrar uma nova fatura fechada, adicionar entrada em `meses_especificos`.
- Ao atualizar parcelas futuras (`x/y`), sincronizar com o JSON.
- Contas fixas que mudam de valor (ex.: Light varia) — atualizar no JSON.
- Nunca remover entradas passadas — elas servem como histórico e o script não as exibe (estão antes de hoje).
