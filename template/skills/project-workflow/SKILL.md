---
name: project-workflow
description: Develop, test, and maintain this generated Python project using its recorded Copier choices and uv toolchain. Use for any code, dependency, configuration, documentation, or test change in this project, including simple libraries, CLIs, APIs, and layered AI or ML applications.
---

# Project Workflow

Use the generated project as the source of truth for its enabled layers.

## Workflow

1. Read `.copier-answers.yml`, `pyproject.toml`, and `readme.md` before changing architecture or commands.
2. Preserve the `src` layout, public entry points, Python version, dependency groups, and existing user changes.
3. Add dependencies with `uv add` or `uv add --group dev`; do not hand-edit the lockfile.
4. Keep secrets out of source control. Document required values in `.env.example` and load them through the generated settings layer when present.
5. Add or update tests alongside behavior changes.
6. Run `uv sync --all-groups`, `uv run ruff check .`, `uv run ruff format --check .`, and `uv run pytest` before delivery.
7. If the project was created from a Git reference and needs upstream fixes, use `copier update` only from a clean worktree and review the resulting diff carefully.

## Entry Points

- For a library, verify imports and its public API.
- For a CLI, run its generated console command and a representative option.
- For an API or interface, start it locally and exercise the health or primary route.
- For MCP, agents, RAG, inference, training, or deployment, use the additional generated skill when present.
