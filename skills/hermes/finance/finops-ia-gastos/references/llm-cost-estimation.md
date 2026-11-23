# IA-FINOPS Projeto — Estimativa de Custo LLM para Codificação com IA

## Quando usar

Usuário pediu explicitamente registrar custos estimados de todas as LLMs de mercado dentro da pasta de relatórios do projeto (ex.: ASCIJA), não apenas o consumo pessoal dele no OpenRouter.

## Fluxo

1. Calcular o volume total de tokens necessários para implementar os specs do projeto (ler TASKS.md + specs existentes; somar estimativas por task).
2. Gerar uma matriz de comparação cobrindo TODOS os providers relevantes (OpenAI, Anthropic, Gemini, Qwen/Tencent, Mistral, DeepSeek, Cohere/Meta).
3. Para cada modelo, incluir: preço input ($/M), preço output ($/M), custo estimado de implementação, e % do orçamento OpenRouter padrão ($100).
4. Aplicar multiplicador de overhead Hermès: a prática consome ~2x-3x sobre o custo teórico direto (contexto persistente, iteracões, verificações, erros/retry, system prompts fixos).
5. Destacar modelos proibidos (que consomem >40% do orçamento OpenRouter mensal sozinho) e recomendar um mix otimizado (ex.: 80% barato + 15% médio + 5% premium para arquitetura).
6. Incluir modelos gratuitos em preview (ex.: Gemini 2.5 Pro COT) — o preço atual é zero, mas registrar também o preço futuro estimado quando sair do período gratuito.

## Formato do arquivo

Salvar em `docs/relatorios/<YYYY-MM-DD>-IA-FINOPS-<DESCRICAO>.md` dentro da raiz do projeto.

Estrutura mínima:
```markdown
# IA-FINOPS — <Título>
Data | Autor | Escopo (tokens totais projetados)

## Resumo Executivo
| Métrica | Valor |
| ...

## Custo por Modelo — Todos os Fornecedores
Tabela comparativa: Provider > Modelo > Input($/M) > Output($/M) > Custo Impl. > % OR $100

## Top N por Custo/Benefício
Ranking com veredito.

## Modelos Proibidos (não viáveis economicamente)
Lista + aviso.

## Estratégia Recomendada
Mix de modelos recomendado + custo estimado com overhead.

## Observações Importantes
- Custo direto vs custo real (overhead Hermès)
- Previsão multi-fase se aplicável
- Limitações/preços estimados claramente marcados
```

## Conversão tokens → USD

Custo impl. ≈ `estimated_tokens × (input_price + output_price)` onde tokens está em milhões (ex.: 2,59M tokens → usar diretamente o valor sem multiplicar por M). Se houver desequilíbrio input/output conhecido, ajustar proporcionalmente.

Para projeção multi-fase: multiplicar custos unitários pelo número de fases.

## Preços de referência (outubro 2026)

### OpenAI (via API / OpenRouter)
| Modelo | Input $/M | Output $/M | Status |
|--------|-----------|------------|--------|
| GPT-4o | 2,50 | 10,00 | Ativo |
| GPT-4o-mini | 0,15 | 0,60 | Ativo |
| o4-mini | 1,10 | 4,40 | Ativo |
| o3-pro | 1,50 | 6,00 | Ativo |
| GPT-5 | estimado | estimado | Sem preço oficial |

### Anthropic (via API)
| Modelo | Input $/M | Output $/M | Status |
|--------|-----------|------------|--------|
| Haiku 3 | 0,25 | 1,25 | Ativo |
| Sonnet 4 | 3,00 | 15,00 | Ativo |
| Opus 3 | 15,00 | 75,00 | Ativo |

### Google / Gemini (Vertex AI / Google AI Studio)
| Modelo | Input $/M | Output $/M | Status |
|--------|-----------|------------|--------|
| Gemini 2.0 Flash | 0,10 | 0,30 | Ativo |
| Gemini 2.0 Pro | 1,25 | 5,00 | Ativo |
| Gemini 2.5 Pro | 1,25 | 5,00 | Ativo |
| Gemini 2.5 Pro COT | 0,00 | 0,00 | **GRATUITO** (preview) |

### Qwen / Tencent (via OpenRouter)
| Modelo | Input $/M | Output $/M | Status |
|--------|-----------|------------|--------|
| qwen3-coder | 0,12 | 0,36 | Ativo |
| GLM-4.5-flash | 0,10 | 0,30 | Ativo |

### Mistral / Cohere / DeepSeek / Meta (via OpenRouter)
| Modelo | Input $/M | Output $/M | Status |
|--------|-----------|------------|--------|
| Mistral Large | 0,24 | 0,75 | Ativo |
| Mistral Small | 0,08 | 0,25 | Ativo |
| DeepSeek V3 | 0,14 | 0,28 | Ativo |
| Command R+ | 0,24 | 0,75 | Ativo |
| Llama 3.3 70B | 0,10 | 0,30 | Ativo |

**Atualizar preços antes de gerar relatório.** Consultar `https://openrouter.ai/models` e sites oficiais dos providers.

## Overhead Hermès — Fator multiplicador

A prática real de codificação com IA consome mais que o custo teórico direto:

| Fator | Impacto |
|-------|---------|
| Contexto persistente por sessão (~5K-15K tokens fixos) | +15-25% |
| Iterações múltiplas por task (gerar→revisar→corriger→testar→ajustar) | +50-100% |
| Verificações (git push/pull, leitura de logs, validação) | +10-20% |
| System prompt (instruções + regras SOUL.md) | já incluído acima |
| Erros e retry (sintaxe inválida, schema errado) | +10-30% |

**Fator multiplicador realista: 2x a 3x sobre o custo teórico direto.** Sempre declarar explicitamente no relatório.

## Arquivos gerados neste fluxo

- `docs/relatorios/<date>-IA-FINOPS-*.md` — arquivo canônico do projeto
- `TASKS.md` — atualizado com nova entry F1-NNN ou similar
- `SESSION.md` — atualizado com registro da atividade
- Git push obrigatório após todos os arquivos

## Regras de segurança (aplicam-se também aqui)

- Nunca incluir valores de credenciais/chaves API na documentação. Substituir por `[REDACTED]`.
- Preços estimados devem ser claramente marcados como "estimado" ou "(estimado)".
- Preços reais obtidos via `/api/v1/models` (OpenRouter) ou sites oficiais são fonte de verdade.
