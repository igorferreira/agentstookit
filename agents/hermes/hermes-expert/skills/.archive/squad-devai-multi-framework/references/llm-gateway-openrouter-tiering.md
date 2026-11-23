# LLM Gateway Architecture & Tiering (OpenRouter Pattern)

## Overview
When dev squads use OpenRouter as a unified multi-model gateway, configure task-based routing across four main tiers:

| Tier | Recommended Model | Pricing (1M in / out) | Target Workloads | Trade-offs & Guardrails |
|---|---|---|---|---|
| **Free / Prototyping** | `stealth/ox-alpha` | $0.00 / $0.00 | PoCs, non-sensitive exploration, long-context analysis (1M tokens) | ⚠️ Prompts are logged by OpenRouter; tool-calling can exhibit formatting lapses. Never use for PII or confidential company data. |
| **High-Volume & Triage** | `google/gemini-3.7-flash`, `openai/gpt-5.6-luna` | ~$0.20–$0.75 / ~$1.20–$1.88 | Chatbots, RAG retrieval summarization, lightweight test generation | Low latency, highly cost-effective; slightly lower reasoning ceiling on deeply nested architectural refactoring. |
| **Open-Weights & Compliance** | `deepseek/deepseek-v4-pro` | ~$0.57–$1.32 / ~$1.15–$3.96 | High-throughput batch processing, internal squads, self-hosting option | 80.6% SWE-bench Verified; MIT license enables air-gapped or AWS EKS deployment for strict compliance. |
| **Production Engineering** | `anthropic/claude-sonnet-5`, `openai/gpt-5.6-sol` | ~$2.00–$5.00 / ~$10.00–$30.00 | Core in-repo code editing, complex architecture specs, CI/CD automated gates | 63.2% SWE-bench Pro / 88.8% Terminal-Bench 2.1; highest precision and strict schema enforcement. |

## Architecture Pattern
Use task-based routing in the agent harness:
```yaml
routing:
  chat_and_coding: anthropic/claude-sonnet-5
  auxiliary_vision: google/gemini-2.0-flash-001
  batch_evaluations: deepseek/deepseek-v4-pro
  experimental: stealth/ox-alpha
```
