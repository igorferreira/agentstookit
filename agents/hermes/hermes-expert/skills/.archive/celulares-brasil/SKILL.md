---
name: celulares-brasil
description: "Use ao comparar ou diagnosticar smartphones no Brasil."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
---

# Celulares Brasil — comparação, preços e diagnóstico

## When to Use

- Igor pede equivalente de um modelo em outra marca ("qual o Motorola equivalente ao Galaxy A17?")
- Comparativo de compra na faixa de preço X (sempre com preços REAIS do mercado BR, não lançamento)
- Diagnóstico de aparelho com problemas (lentidão, touch fantasma, Bluetooth instável)
- Criação/consulta de vigia de preço para smartphone
- Prints de specs (app "Info Dispositivo PRO" etc.) para extrair ficha técnica

Não usar para: vendas, garantia/administração de plano, preço de peça avulsa sem contexto de compra.

## Fontes de referência (a "bíblia")

- Fichas técnicas: GSMArena (mundo), TudoCelular, Tecnoblog/produtos, Canaltech/produto, Kimovil (versão BR vs global — chip pode mudar!)
- Preços BR: Buscapé, Zoom, Amazon BR, Mercado Livre, Magalu, Casas Bahia, BoaDica
- Reviews YouTube BR: Gesiel Taveira, Oficina da Net (referência em teste de bateria padronizado), Canal do Celular/Everaldo Jr, Arthur Kepler, Talles, MrKaslim, Escolha Certa

## Regras de trabalho

1. **Sempre citar fonte** — preço ou spec sem fonte não entra na resposta.
2. Preço de **mercado atual** (à vista PIX), nunca preço de lançamento.
3. Comparar por faixa de preço real, não por linha/geração nominal.
4. Benchmark como referência relativa: ~300k AnTuTu = entrada, ~600k = intermediário bom, ~1M+ = premium.
5. Versão brasileira pode ter chip diferente da global — verificar no Kimovil/ficha BR.
6. Antes de recomendar compra planejada, oferecer vigia de preço (cronjob diário com prompt self-contained: baseline + gatilhos + histórico — ver skill `product-price-monitor`).
7. Respostas no Telegram: listas com ✅/❌/⚠️, NUNCA tabelas markdown (não renderizam).

## Contexto fixo do Igor

- Trauma: Xiaomi Redmi Note 13 (SD 680, HyperOS 2) com touch fantasma, BT instável, lentidão — bugs reconhecidos pós-HyperOS 2, não resolvíveis por formatação. Priorizar estabilidade: Motorola/Samsung sobre Xiaomi.
- Analisado 05/09/2026: Moto G86 5G = escolha recomendada (pOLED 1.5K 120Hz 4500 nits, Dimensity 7300 ~660k, IP68/IP69, BT 5.4) sobre Galaxy A27 (caro) e A17 (fraco). Edge 70 = joia se voltar perto do mínimo histórico R$ 1.703.
- Arquivos canônicos: `~/MEGA/Documentos/hardware/celulares/` (análises), `~/MEGA/Documentos/hardware/monitor-precos/<slug>/` (vigias com BASELINE.md).

## Pitfalls

- **Print do app de specs**: transcrever com vision_analyze perguntando por cada campo (chip, RAM usada/livre, OS, armazenamento) — a informação de RAM em uso em repouso (%) é o melhor indicador de lentidão estrutural.
- **Lentidão crônica ≠ falta de armazenamento**: chip de entrada + software pesado (HyperOS) é causa estrutural; formatação alivia meses, não resolve.
- **Equivalente entre marcas não é gêmeo**: comparar por faixa de preço e por quais dores do usuário o candidato resolve (ex: touch/BT estáveis > mais câmera).
- **Preço de intermediário bom oscila rápido**: quando cair abaixo do alvo do vigia, recomendar fechar logo — costuma subir de volta.
- **Vigia de preço em cronjob**: o prompt do tick roda sem memória de conversa — embutir baseline, gatilhos, formato de saída e pasta de histórico no próprio prompt (self-contained). Nunca referenciar "como discutido".
