---
name: validate-python-stack
description: Validate the Python Template repository or a project generated from it. Use before committing, publishing, deploying, or reviewing a stack to check catalog compilation, rendering, dependencies, formatting, tests, security workflows, skills, and representative runtime behavior.
---

# Validate Python Stack

Choose the validation path that matches the current directory and report exact failures without hiding skipped checks.

## Template Repository

1. Run `uv sync --all-groups`.
2. Run `uv run python scripts/compile_catalog.py --check`.
3. Run `uv run ruff check .` and `uv run ruff format --check .`.
4. Run `uv run pytest -n auto`. Use focused tests first while iterating, but finish with the full suite.
5. For every directory under `skills/`, run the skill-creator validator when available and run `npx --yes skills add . --list` to verify discovery.
6. Generate the changed presets or custom combinations and exercise their real CLI, API, MCP, training, serving, or deployment entry point as applicable.
7. If GitHub workflows changed and Docker is available, run the repository's local Actions validation before pushing.

## Generated Project

1. Read `.copier-answers.yml`, `readme.md`, and `pyproject.toml` to identify enabled layers.
2. Run `uv sync --all-groups`, `uv run ruff check .`, `uv run ruff format --check .`, and `uv run pytest`.
3. Run `npx --yes skills add . --list`; expect `project-workflow` and only the conditional skills appropriate to the selected stack.
4. Exercise the primary entry point. For a containerized target, build the Docker image and verify its health route locally when Docker is available.
5. Validate generated JSON, TOML, YAML, Python, and HCL as structured data rather than with string-only assertions.

## Reporting

Separate passed, failed, and unavailable checks. Include the command, relevant error, and whether the failure belongs to the template, the generated project, local infrastructure, or an external service.
