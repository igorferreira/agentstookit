---
name: llm-model-operations
description: "Use when discovering, downloading, quantizing, serving, benchmarking, comparing, or tracking language models. Route across Hugging Face Hub, llama.cpp, vLLM, lm-evaluation-harness, and Weights & Biases while preserving reproducible model and experiment metadata."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [llm, mlops, huggingface, llama-cpp, vllm, evaluation, wandb]
---

# LLM Model Operations

## Overview

A class-level workflow for the model lifecycle from artifact discovery through local or production inference to benchmark comparison and experiment tracking.

## Workflow Router

- **Find, inspect, download, cache, or upload models/datasets:** `references/huggingface-hub.md`.
- **Run local GGUF inference, quantize, optimize, or expose a lightweight server:** `references/llama-cpp.md` and `references/llama-cpp/`.
- **Serve high-throughput OpenAI-compatible inference:** `references/serving-llms-vllm.md` and `references/serving-llms-vllm/`.
- **Run standard/custom/distributed LLM benchmarks:** `references/evaluating-llms-harness.md` and `references/evaluating-llms-harness/`.
- **Track runs, sweeps, artifacts, and integrations:** `references/weights-and-biases.md` and `references/weights-and-biases/`.

## Integrated Workflow

1. Record the exact repository, revision, files, license, and trust-remote-code requirement.
2. Select runtime by workload: llama.cpp for compact GGUF/local deployment; vLLM for GPU throughput and an OpenAI-compatible service.
3. Record quantization, context length, tokenizer, chat template, device topology, and serving flags.
4. Benchmark with fixed task versions, seeds, few-shot settings, and generation parameters.
5. Track configurations and artifacts so comparisons can be reproduced rather than inferred from model names.
6. Verify downloads, launch health, sample inference, benchmark outputs, and persisted run metadata with real commands.

## Common Pitfalls

- Comparing benchmark numbers produced with different prompts, task versions, or few-shot settings.
- Treating similarly named quantizations as interchangeable.
- Launching a server without a health check and sample request.
- Uploading generated or converted artifacts without provenance and license review.

## Verification Checklist

- [ ] Exact model revision and artifact hashes recorded where practical
- [ ] Runtime and quantization fit hardware and workload
- [ ] Server health and sample generation verified
- [ ] Benchmark configuration is reproducible
- [ ] Experiment metadata and artifacts persisted
