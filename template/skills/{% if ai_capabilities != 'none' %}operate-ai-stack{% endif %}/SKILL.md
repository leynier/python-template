---
name: operate-ai-stack
description: Develop, test, and troubleshoot this generated AI or ML workload across its framework, model and embedding providers, retrieval stores, interfaces, training, serving, and observability layers. Use when changing prompts, tools, agents, RAG, MCP, inference, fine-tuning, evaluations, or provider integration.
---

# Operate AI Stack

Treat `.copier-answers.yml` as the layer map and inspect the generated modules before assuming a framework or provider API.

## Workflow

1. Identify the workload, framework, model provider, embedding provider, data roles, interfaces, training extensions, serving engine, and quality tools that are actually enabled.
2. Preserve the boundary between model and embedding providers. Keep provider-specific construction in the generated provider module and inject it into framework code.
3. Use deterministic fakes for unit tests. Put real-provider checks behind explicit environment variables and never make the normal test suite spend tokens or require cloud credentials.
4. For agents and MCP, test tool schemas and error paths. For RAG, test ingestion, retrieval, empty results, and citation metadata. For training, test a tiny local batch and artifact creation. For inference, test health plus one prediction.
5. Record required secrets in `.env.example`, use the settings layer, and redact prompt, credential, and personal data from logs.
6. Run the project quality gates from `project-workflow`, followed by the smallest representative end-to-end check for the enabled stack.

## Operational Checks

- Pin or bound model and API dependencies; review upstream breaking changes before updating.
- Track latency, token or compute usage, provider errors, and evaluation quality separately.
- Make external calls timeout and fail clearly; do not silently switch providers or models.
- Require an explicit review before changing production prompts, tools with side effects, or model artifacts.
