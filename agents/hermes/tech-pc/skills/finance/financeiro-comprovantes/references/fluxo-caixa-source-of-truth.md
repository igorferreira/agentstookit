# Fluxo de Caixa — Fonte da Verdade

## ⚠️ Pitfall: MD/CSV/XLSX podem desaparecer da raiz

Os arquivos `FLUXO-CAIXA-2026-2030.md`, `.csv` e `.xlsx` na raiz de `~/MEGA/Comprovantes/` são **derivados** e podem ser apagados acidentalmente (ex.: durante reorganização da pasta).

**Fonte canônica:** os JSONs em `2026/_Analises/cenarios/fluxo_xNN.json` são a fonte da verdade. Cada cenário (X16, X17, X18, X19...) tem seu JSON completo com todos os parâmetros e os 53 meses calculados.

### Procedimento de recuperação

1. Listar cenários disponíveis: `ls 2026/_Analises/cenarios/fluxo_x*.json`
2. Identificar o mais recente (maior número)
3. Carregar o JSON, verificar se os parâmetros batem com a realidade atual (CDB, faturas, etc.)
4. Se bater, regenerar MD + CSV + XLSX com `write_file` + `terminal python3`
5. Se não bater (ex.: CDB real diferente do JSON), criar novo cenário X(N+1) com os parâmetros corrigidos

### Regeneração rápida (quando o JSON está atualizado)

```bash
python3 /tmp/gerar_xNN.py  # script que lê o JSON e gera os 3 arquivos
```

### Nunca

- Confiar que `FLUXO-CAIXA-2026-2030.md` existe antes de tentar lê-lo
- Tentar ler o CSV/XLSX como fonte primária
- Assumir que o último cenário do INDEX-CENARIOS.md é o JSON mais recente (o INDEX pode estar desatualizado)
- Usar `execute_code` para gerar fluxo (bloqueado em cron/gateway); sempre `write_file` + `terminal`
