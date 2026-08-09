# Getting started

## Requirements

Install [`uv`](https://docs.astral.sh/uv). Copier itself can run ephemerally
through `uvx`, so no global Python environment is required.

## Generate interactively

```bash
uvx copier copy --trust gh:leynier/python-template my-project
```

`--trust` allows the template's post-copy tasks to initialize Git and run
`uv sync`. The prompts first offer an editable preset, then expose the layers
and normal project metadata.

## Start from a preset

Preselect a recipe and keep the remaining answers interactive:

```bash
uvx copier copy --trust \
  -d preset=pydantic-ai-openai \
  gh:leynier/python-template my-agent
```

Use `-d key=value` repeatedly for automation. Keep the answer set in version
control through the generated `.copier-answers.yml` rather than maintaining a
second undocumented configuration.

## Verify the result

```bash
cd my-project
uv sync --all-groups
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

The generated `readme.md` documents its primary entry point, environment
variables, Docker command, deployment adapter, and release flow when enabled.

## Pull in later template releases

Commit or stash local work before updating, then run:

```bash
uvx copier update
uv sync --all-groups
uv run pytest
```

Copier performs a three-way update using `.copier-answers.yml`; review the diff
because template changes and project-specific edits can touch the same file.
