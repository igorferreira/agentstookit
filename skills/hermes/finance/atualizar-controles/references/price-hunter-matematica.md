# Price Hunter — Matemática PhD para Comparação de Preços

> **Skill:** `price-hunter` (Dr. Preço PhD)
> **Criado:** 13/08/2026
> **Sites cobertos:** 8 (Mercado Livre, Shopee, Amazon, Magalu, Americanas, BoaDica, Kabum, AliExpress)

## ⚠️ Regra de ouro

**SEMPRE usar `browser-use-real` (Chrome via CDP em 127.0.0.1:9222).**

**NUNCA:**
- ❌ Confiar em snippet de web_search como preço atual
- ❌ Apresentar API ou scraping como equivalente a ver o site
- ❌ Inventar preço de "estimativa" se não viu na tela
- ❌ Repetir preço antigo que estava em cache

**SEMPRE:**
- ✅ Carregar a página real do produto
- ✅ Ler o preço, frete, vendedor, reputação direto da tela
- ✅ Tirar print se houver dúvida
- ✅ Se não conseguir confirmar, marcar "preço não confirmado"

## 🧮 Fórmula PhD: Custo Total

```
custo_total = (
    preco_vista × (1 - desconto_pix)
  + preco_parcelado × (1 + taxa_juros_mes)^parcelas - preco_vista
  + frete
  - cashback
  - pontos_fidelidade × valor_ponto
) × fator_risco_vendedor
```

### Fatores de risco por vendedor

| Reputação | Fator |
|---|---|
| Loja oficial (MercadoLíder Gold, Amazon, Magazine) | 1.00 |
| MercadoLíder Platinum | 1.02 |
| MercadoLíder | 1.05 |
| Vendedor novo (< 6 meses, < 100 vendas) | 1.30 (risco de fraude/garantia) |
| Vendedor com reclamações | 1.50+ |

## 📊 Decisão PIX vs Cartão (matemática)

- **PIX à vista:** desconto imediato (5-10% comum)
- **Cartão sem juros:** até 12x (rende mais que PIX se for investir)
- **Cartão com juros:** 15-20% a.m. — **NUNCA USAR**

**Regra de decisão:**
- Se tem CDB rendendo 1% a.m. (=12% a.a.): cartão sem juros > PIX (a partir de 3 meses)
- Se não tem reserva: PIX sempre
- Se cupom de 1ª compra (Shopee 10-20%): pode reverter

## 🎯 Casos especiais

### Cashback / cupons
- **Cupom de primeira compra Shopee:** 10-20% off
- **Cashback Méliuz:** até 5% em muitas lojas
- **PicPay:** cashback em compras específicas
- **Méliuz+ Itaú:** pontos em dobro

### Frete grátis
- Mercado Livre: full (azul) = grátis e rápido
- Shopee: > R$ X = grátis; abaixo = R$ 20-30
- Amazon: Prime = grátis; sem = R$ 15-25
- Magalu: > R$ X = grátis; abaixo = R$ 19

## 🔧 Setup do browser-use

```bash
# Já instalado em: ~/.local/bin/browser-use-real
# Inicia Chrome isolado em CDP 127.0.0.1:9222
# Sem gravações, sem telemetria
# Skills relacionadas: browser-use, mercadolivre-price-search, boadica-price-search
```

## 📋 Workflow padrão (3 passos)

### 1. Identificar SKU exato
Antes de comparar, Igor precisa definir:
- Marca + modelo + capacidade + cor
- Ex.: "SSD Kingston A400 480GB SATA III 2.5""

**NÃO normalizar = comparar maçãs com laranjas.**

### 2. Buscar em paralelo (8 sites)
1. Carregar página de busca com termo normalizado
2. Identificar SKU exato nos resultados
3. Clicar no produto
4. Extrair: preço à vista, preço parcelado, frete, vendedor, reputação, estoque, cupom

### 3. Tabular e ranquear

```
| Site | Preço Vista | Preço Parcelado | Frete | Total | Vendedor | Reputação | Link |
|------|-------------|------------------|-------|-------|----------|-----------|------|
| ML   | R$ 280      | 12× R$ 28,15    | R$ 25 | R$ 305| TechStore | 🟢 PLATINUM 98% | link |
| Shopee| R$ 290     | 12× R$ 29,00    | R$ 0  | R$ 290| Loja X    | 🟡 4.5★ 50 vendas | link |
```

## 📞 Comandos úteis (do usuário)

| Comando | Ação |
|---|---|
| "Quanto custa X?" | Pesquisa padrão nos 8 sites |
| "Vale a pena X por R$ Y?" | Análise de custo total + 3 cenários |
| "Onde compro X?" | Lista os 8 sites com preços |
| "Compara X" | Comparação lado a lado |
| "Cupom de primeira compra Shopee?" | Aplica cupom automaticamente |
| "Melhor PIX ou cartão?" | Decisão matemática |

## ⚠️ Limites

- ❌ Não comparar produtos diferentes (ex.: 480GB vs 1TB)
- ❌ Não inventar preços se não viu
- ❌ Não recomendar vendedores com reputação ruim
- ❌ Não usar cupom expirado / cashback falso
- ❌ Não navegar em sites bloqueados / logins que não tem

## 📚 Referências complementares

- `~/.hermes/skills/shopping/boadica-price-search/` — específico RJ
- `~/.hermes/skills/shopping/mercadolivre-price-search/` — específico ML
- `~/.hermes/skills/shopping/browser-use/` — navegação geral
- `~/.hermes/profiles/shopping/SOUL.md` — personalidade Dr. Preço PhD

## 📂 Histórico de buscas (criar ao usar)

Salvar em `~/MEGA/Compras/historico/AAAA-MM-DD_<produto>.md`:

```markdown
# Pesquisa: [Produto]
**Data:** DD/MM/YYYY HH:MM
**Por:** Igor

## Resultados
[tabela]

## Recomendação
[com matemática]

## Decisão
- [ ] Comprar
- [ ] Esperar
- [ ] Cotar outro produto
```

## Versão

- v1.0 (13/08/2026): criado por Hermes Agent — combina `boadica-price-search` + `mercadolivre-price-search` + `browser-use`