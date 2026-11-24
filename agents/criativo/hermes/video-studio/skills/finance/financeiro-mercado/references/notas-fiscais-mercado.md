# Captura de Notas Fiscais de Supermercado — Fase 1

## Visão Geral

Este fluxo captura fotos de notas fiscais de supermercado (NFC-e), extrai os itens de forma estruturada, e organiza em diretórios/bases de dados para análise posterior de preços.

**Padrão base:** O comprovante original fica em `~/MEGA/Comprovantes/AAAA/AAAA_MM_MES/` (mesmo padrão de `financeiro-comprovantes`). Os itens extraídos ficam em `~/MEGA/Documentos/Mercado/precos_itens.csv`.

## Pré-requisitos

- Foto da nota fiscal de supermercado (com QR code visível de preferência).
- Python 3.x com `requests`, `beautifulsoup4`, `opencv-python`, `Pillow` (já instalados).
- Script `/home/usuario/.hermes/skills/finance/financeiro-mercado/scripts/decodificar_nfce.py`.

## Fluxo Fase 1

### 1. Captura via Telegram

Usuário envia a foto via `@finance` no Telegram:

```
@finance [foto da nota]
```

O bot recebe, salva a foto temporariamente e chama o script de decodificação.

### 2. Decodificação e Extração

```bash
python3 ~/.hermes/skills/finance/financeiro-mercado/scripts/decodificar_nfce.py \
  /tmp/nota.jpg \
  --output nota_dados.json
```

**Saídas esperadas** (JSON):

```json
{
  "mercado": "Carrefour",
  "data": "2026-09-05",
  "valor_total": 123.45,
  "chave_nfce": "35260812345678901234567890123456789012AB",
  "fonte": "sefaz",
  "itens": [
    {
      "descricao": "Arroz Tipo 1 5kg",
      "quantidade": 1,
      "unidade": "UN",
      "valor_unitario": 28.90,
      "valor_total": 28.90
    },
    {
      "descricao": "Leite Integral 1L",
      "quantidade": 3,
      "unidade": "UN",
      "valor_unitario": 4.50,
      "valor_total": 13.50
    }
  ]
}
```

**Se falhar a decodificação do QR:**

- O script roda OCR do cabeçalho (mercado, data, valor total) via `tesseract`.
- Retorna `fonte: "ocr_parcial"` e `itens: []` (sem parsing dos itens).
- Usuário deve conferir manualmente depois e preenchê-los se necessário (Fase 2).

### 3. Armazenar Comprovante Original

Salvar a foto em:

```
~/MEGA/Comprovantes/AAAA/AAAA_MM/AAAA-MM-DD_NOTA-MERCADO-NOMELOJA-R$VALOR.jpg
```

**Exemplo:**

```
~/MEGA/Comprovantes/2026/2026_09_SET/2026-09-05_NOTA-MERCADO-CARREFOUR-BARRA-R$123.45.jpg
```

Criar arquivo `.md` irmão com metadados:

```
~/MEGA/Comprovantes/2026/2026_09_SET/2026-09-05_NOTA-MERCADO-CARREFOUR-BARRA-R$123.45.md
```

**Conteúdo do `.md`** (template):

```markdown
---
data: 2026-09-05
tipo: comprovante
subtipo: nota-fiscal-mercado
valor: 123.45
mercado: Carrefour
chave_nfce: 35260812345678901234567890123456789012AB
fonte_extracao: sefaz
status: processado
---

# Nota Fiscal — Carrefour — R$ 123.45

**Data**: 2026-09-05
**Valor Total**: R$ 123.45
**Chave de Acesso NFC-e**: `35260812345678901234567890123456789012AB`
**Fonte de Extração**: SEFAZ (itens estruturados)

## Itens

| Descrição | Qtd | Un | V. Unit | Total |
|---|---|---|---|---|
| Arroz Tipo 1 5kg | 1 | UN | 28.90 | 28.90 |
| Leite Integral 1L | 3 | UN | 4.50 | 13.50 |

---

*Registrado em: 2026-09-05T14:30:00 via decodificar_nfce.py*
```

### 4. Atualizar `precos_itens.csv`

Adicionar uma linha por item no arquivo:

```
~/MEGA/Documentos/Mercado/precos_itens.csv
```

**Formato CSV** (cabeçalho já existe):

```csv
data,mercado,produto_cru,quantidade,unidade,valor_unitario,valor_total,chave_nfce,ref_comprovante
2026-09-05,Carrefour,Arroz Tipo 1 5kg,1,UN,28.90,28.90,35260812345678901234567890123456789012AB,2026-09-05_NOTA-MERCADO-CARREFOUR-BARRA-R$123.45
2026-09-05,Carrefour,Leite Integral 1L,3,UN,4.50,13.50,35260812345678901234567890123456789012AB,2026-09-05_NOTA-MERCADO-CARREFOUR-BARRA-R$123.45
```

### 5. Atualizar `INDEX.md`

Manter um índice simples em:

```
~/MEGA/Documentos/Mercado/INDEX.md
```

**Conteúdo** (exemplo):

```markdown
# 🛒 Mercado — Rastreamento de Preços

## 📊 Resumo

| Métrica | Valor |
|---|---|
| Mercados Cadastrados | 3 |
| Notas Registradas | 12 |
| Último Registro | 2026-09-05 |
| Valor Médio de Compra | R$ 118.50 |

## 🏪 Mercados

### Carrefour
- **Endereço**: Av. das Américas, 3000
- **Visitas**: 8
- **Ticket Médio**: R$ 125.30
- **Última Visita**: 2026-09-05

### Pão de Açúcar
- **Endereço**: Rua X, nº Y
- **Visitas**: 3
- **Ticket Médio**: R$ 95.20
- **Última Visita**: 2026-08-30

### Zona Leste
- **Endereço**: Rua Z, nº Z
- **Visitas**: 1
- **Ticket Médio**: R$ 87.50
- **Última Visita**: 2026-08-25
```

## Troubleshooting

### QR Code não decodifica

- **Foto muito escura/de ângulo?** Tente fotografar novamente com melhor iluminação, de frente.
- **QR cortado na foto?** Usar OCR fallback (o script faz automaticamente).
- **Script reporta erro na SEFAZ?** O portal pode estar fora do ar ou o estado pode usar um layout diferente — nesse caso, Usuário deve conferir/preencher manualmente os itens.

### OCR retorna lixo

- Certificar que a foto está nítida (não borrada).
- Se o cabeçalho continuar ilegível, preencher os dados manualmente no `.md`.

### Atualizações de `INDEX.md` e `precos_itens.csv`

- A automação **completa** (atualização desses arquivos) será Fase 2+ — por enquanto é feita **manualmente** ou via script de integração que você passará para rodar.
- Nesta Fase 1, o essencial é a **captura + armazenamento do comprovante original**.

## Próximos Passos (Fase 2)

- Implementar catálogo de produtos com fuzzy matching (normalizar "Arroz Tipo 1 5kg" → "ARROZ_1KG_TIPO_1" com marca/loja).
- Automatizar a atualização de `INDEX.md` e `precos_itens.csv` via script.
- Análise histórica: calcular preço médio, variações, ranking de supermercados.
