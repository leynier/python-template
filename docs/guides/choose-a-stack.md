# Choose a stack

Use a preset when it expresses the same product shape, even if one provider or
interface will change. Use `custom` when the workload itself or several layers
differ.

## Stay simple

- Choose `python-library` for reusable importable behavior.
- Choose `typer-cli` for commands, automation, and local developer tools.
- Choose `fastapi-api` for a JSON service. Custom API projects can select Flask.

These presets intentionally set AI capabilities to `none`.

## Expose tools to models

Choose `fastmcp-server` when the product boundary is MCP tools and resources.
It generates a FastMCP server and a tested local tool rather than wrapping an
agent around the server unnecessarily.

## Build an agent

Start with Pydantic AI, Google ADK, Strands Agents, LangGraph, or the local Lingo
recipe. Select the model provider separately. Pydantic AI can add selected
Pydantic AI Harness capabilities without making Harness mandatory.

## Build RAG

Choose the orchestration framework, model provider, embedding provider, vector
store, and user interface independently. Test ingestion and empty retrieval as
well as the successful answer path.

## Train or serve models

Training projects choose a framework plus optional datasets, acceleration,
fine-tuning, and experiment tooling. Hybrid projects use a `uv` workspace to
keep training and service dependencies separate. Serving can target BentoML,
LiteLLM, vLLM, Ollama, or Ray Serve.

## Finish with operations

Add only the evaluation, telemetry, orchestration, deployment, and IaC layers
the project will operate. An unused observability SDK is maintenance cost, not
production readiness.
