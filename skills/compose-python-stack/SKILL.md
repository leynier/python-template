---
name: compose-python-stack
description: Design and generate a compatible project from the Python Template component layers or presets. Use when choosing a workload, framework, AI providers, data engines, interfaces, training and serving tools, deployment target, or IaC option; also use when a user wants a simple library, CLI, or API without AI.
---

# Compose Python Stack

Turn a product goal into a supported stack, explain the consequential choices, and generate it with Copier.

## Workflow

1. Read `docs/reference/presets.md` and `docs/reference/components.md`. When exact compatibility matters, also read `catalog/generated/catalog.json`.
2. Ask only about choices that change the architecture. Prefer one of the documented presets when it is close; otherwise select `custom` and compose the layers.
3. Keep model and embedding providers independent. Select at most one provider for each data role. Do not add AI to a simple library, Typer CLI, or FastAPI/Flask API unless requested.
4. Select one deployment target. Docker is the portable base for deployed projects; select either no IaC, Pulumi, or Terraform where the chosen target supports it.
5. Generate into a new directory with `copier copy gh:leynier/python-template <destination>`, answering interactively. For automation, pass explicit values with repeated `-d key=value` arguments.
6. Enter the generated directory and run `uv sync --all-groups`, `uv run pytest`, `uv run ruff check .`, and `uv run ruff format --check .`.
7. Report the selected layers, generated entry points, required environment variables, and any cloud resources the user must configure.

## Guardrails

- Treat catalog compatibility rules as authoritative; do not force an invalid combination.
- Preserve the first-class `python-library`, `typer-cli`, and `fastapi-api` paths.
- Do not propose ODMantic, AutoGOAL, FastUI, or Reflex; they are intentionally outside the supported catalog.
- Prefer Python 3.12 or newer and `uv` for environment and command execution.
- Never deploy, create paid resources, or write credentials unless the user explicitly authorizes that action.
