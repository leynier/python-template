# Python Template

[![CI](https://github.com/leynier/python-template/actions/workflows/ci.yml/badge.svg)](https://github.com/leynier/python-template/actions/workflows/ci.yml)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/leynier/python-template/badge)](https://scorecard.dev/viewer/?uri=github.com/leynier/python-template)
[![Documentation](https://img.shields.io/badge/docs-python--template.leynier.dev-5c6ac4)](https://python-template.leynier.dev)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Copier](https://img.shields.io/badge/template-Copier-2ea44f)](https://copier.readthedocs.io)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Last commit](https://img.shields.io/github/last-commit/leynier/python-template.svg)](https://github.com/leynier/python-template/commits)
[![GitHub stars](https://img.shields.io/github/stars/leynier/python-template?logo=github)](https://github.com/leynier/python-template/stargazers)

Generate production-ready Python and AI stacks by combining frameworks, data engines, tooling, and cloud deployment.

Start with a simple library, CLI, or API. Or compose an agent, RAG system,
training workspace, inference service, data layer, UI, quality stack, and deploy
target without assembling the project conventions yourself.

## Quick start

Install nothing globally beyond [`uv`](https://docs.astral.sh/uv):

```bash
uvx copier copy --trust gh:leynier/python-template my-project
cd my-project
uv run pytest
```

Copier presents 12 editable recipes plus a custom layer-by-layer path. It
initializes Git and installs the selected dependencies after rendering.

Want the small version? These remain first-class choices with no AI dependency:

```text
Python Library     typed, buildable package
Typer CLI          tested command-line application
FastAPI API        production-shaped JSON service
```

## Compose the stack you need

The generator resolves each choice as a layer, so infrastructure can change
without replacing the application framework and model providers can change
without coupling them to the embedding provider.

| Layer | Examples |
| --- | --- |
| Workload | library, CLI, API, web, TUI, MCP, agent, RAG, inference, training, hybrid |
| Framework | FastAPI, Flask, FastMCP, Pydantic AI, LangGraph, LlamaIndex, Lingo, Transformers |
| Interface | Streamlit, Gradio, Chainlit, Textual, NiceGUI, FastHTML, Violetear, JupyterLab |
| Model provider | OpenAI, Anthropic, Gemini, Bedrock, Azure OpenAI, Ollama, OpenRouter and more |
| Embeddings | hosted provider or Sentence Transformers, selected independently |
| Data | SQL, document, vector, graph, and cache roles with one engine per role |
| Auth | API key, OAuth/OIDC, or Supabase Auth |
| Training | Lightning, Datasets, Accelerate, PEFT, TRL, Optuna |
| Serving | BentoML, LiteLLM, vLLM, Ollama, Ray Serve |
| MLOps and quality | Prefect, Dagster, DVC, MLflow, Ragas, DeepEval, OpenTelemetry and more |
| Deploy | Docker plus 14 managed or cloud targets |
| IaC | none, Pulumi, or Terraform for supported cloud targets |

The catalog currently contains 126 components with explicit workload, Python,
and support-tier metadata. See the complete [component
reference](https://python-template.leynier.dev/reference/components/).

## The 12 presets

Presets are useful starting points, not locked bundles. Every answer remains
editable during generation.

| Preset | Starting stack |
| --- | --- |
| `python-library` | Typed publishable package |
| `typer-cli` | Typer command-line app |
| `fastapi-api` | FastAPI JSON service |
| `fastmcp-server` | FastMCP tool server |
| `pydantic-ai-openai` | Pydantic AI + Harness + OpenAI |
| `google-adk-gemini` | Google ADK + Gemini |
| `strands-bedrock` | Strands Agents + Bedrock |
| `langgraph-anthropic-api` | LangGraph + Anthropic + FastAPI |
| `llamaindex-rag` | LlamaIndex + OpenAI + Pinecone + Gradio |
| `local-lingo-app` | Lingo + Ollama + Beaver + Violetear |
| `litellm-gateway` | LiteLLM + Redis + Docker |
| `hf-finetuning` | Transformers + PEFT/TRL + MLflow + BentoML |

Preselect one while keeping the remaining questions interactive:

```bash
uvx copier copy --trust \
  -d preset=fastmcp-server \
  gh:leynier/python-template my-tools
```

## Deploy without rebuilding the project

Every deployment choice keeps a portable Docker base. Choose one target among
Docker, Render, Fly.io, Vercel, Railway, Hugging Face Spaces, Modal, RunPod,
BentoCloud, AWS ECS, SageMaker, Cloud Run, Vertex AI, Azure Container Apps, or
Azure ML. The six cloud targets can additionally generate Pulumi or Terraform.

Managed inference variants expose consistent health and prediction contracts,
while Modal, RunPod, and BentoCloud receive native SDK adapters.

## Skills for AI coding agents

This repository is directly discoverable by the open Agent Skills CLI:

```bash
npx skills add leynier/python-template --list
npx skills add leynier/python-template --skill compose-python-stack
```

Repository skills help an agent compose, maintain, and validate stacks. Every
generated project also includes a common workflow skill and conditionally adds
AI and deployment skills matching its selected layers.

## What every generated project gets

- A `src/` layout, typed package marker, bounded dependencies, and committed
  `uv.lock`.
- Ruff, pytest, deptry, advisory `ty`, pre-commit, coverage, and Poe tasks.
- CI across Linux, macOS, and Windows, with least-privilege permissions and
  pinned actions.
- CodeQL, zizmor, Dependabot, issue forms, security policy, contribution guide,
  and changelog.
- Optional Zensical docs, PyPI Trusted Publishing, Docker, devcontainer, and
  agent instructions.
- A saved `.copier-answers.yml` so later template releases can be applied with
  `uvx copier update`.

## Support model

Catalog entries use three intentionally visible tiers:

- `stable`: open-source component exercised without external credentials.
- `platform`: hosted or cloud integration whose generated contract is tested
  offline; real deployment still requires the user's account and secrets.
- `experimental`: useful but evolving integration with a narrower compatibility
  promise.

The catalog favors maintained projects that add a distinct layer or a clear
end-to-end recipe.

## Develop the template

```bash
uv sync --all-groups
uv run python scripts/compile_catalog.py --check
uv run ruff check .
uv run ruff format --check .
uv run pytest -n auto
uv run --group docs zensical serve
```

The test suite renders compatible combinations, runs real generated toolchains,
parses deployment artifacts, checks `copier update`, and exercises representative
AI/ML vertical slices. Hosted CI repeats the generated-project tests on Linux,
macOS, and Windows.

Read the [documentation](https://python-template.leynier.dev), the
[contribution guide](CONTRIBUTING.md), or the [security policy](SECURITY.md).

## License

Python Template is collaborative open source under the [MIT license](LICENSE).
