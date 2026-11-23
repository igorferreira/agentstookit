# FGTS Extrato — extração e impacto na rescisão

## Extração do PDF

```bash
pdftotext -layout extrato_NOORDEN.pdf -
```

Campos a capturar:
- `VALOR PARA FINS RESCISÓRIOS` — base oficial para multa de 40%
- Saldo total (última linha do histórico)
- Saques com código `COD 60` → confirmam **saque-aniversário**
- Saques com prefixo `SAQUE DEP` e `SAQUE JAM` → depósitos e juros sacados no aniversário

## Confirmação da modalidade

| Lançamento | Modalidade | Implicação na rescisão |
|---|---|---|
| `SAQUE JAM - COD 60` ou `SAQUE DEP - COD 60` | **Saque-aniversário** | Na dispensa: recebe multa 40% mas NÃO saca saldo bloqueado |
| Nenhum saque COD 60 no histórico | Provável saque-rescisão | Na dispensa: saca saldo integral + multa 40% |

## Impacto nos cenários rescisórios (Usuário — extrato 23/07/2026)

| Campo | Valor |
|---|---:|
| Saldo total | R$ 42.209,32 |
| Saldo bloqueado (antecipação) | R$ 39.495,35 |
| Saldo não bloqueado por diferença aritmética | R$ 2.713,97 |
| Base para fins rescisórios | R$ 42.715,37 |
| Multa 40% | R$ 17.086,15 |

- **Pedido de demissão:** sem multa; não presumir saque imediato de saldo FGTS por esse motivo.
- **Dispensa sem justa causa no saque-aniversário:** recebe a multa rescisória estimada de R$ 17.086,15. Conforme orientação oficial do FGTS, a dispensa não libera automaticamente o saldo remanescente; não somar os R$ 2.713,97 ao caixa imediato apenas por estarem fora do valor bloqueado.
- O saldo da conta antiga de outro empregador não integra a base da multa rescisória do vínculo atual.
- Fonte oficial: https://www.fgts.gov.br/Paginas/trabalhador/saque/saque-aniversario.aspx

## Retorno ao saque-rescisão

Cancelar saque-aniversário → carência de **24 meses** para voltar ao saque-rescisão. Não fazer antes de decisão de desligamento.

## Arquivos salvos (Usuário)

- `rescisao-clt/evidencias/2026-07-23_EXTRATO-FGTS-NOORDEN-CAIXA.pdf`
- `rescisao-clt/evidencias/2026-07-23_EXTRATO-FGTS-NOORDEN-CAIXA.md` (histórico completo tabulado)
- `rescisao-clt/dados-contrato.json` → campos `fgts_*` atualizados com dados reais
