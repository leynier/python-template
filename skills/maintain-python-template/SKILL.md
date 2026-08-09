---
name: maintain-python-template
description: Extend or repair the Python Template repository while keeping its catalog, Copier questions, templates, generated references, and tests synchronized. Use for adding a framework, provider, database, interface, ML tool, deployment target, preset, compatibility rule, or generated-project capability.
---

# Maintain Python Template

Make catalog-driven changes without creating a choice that renders but cannot run.

## Change Workflow

1. Inspect `catalog/components.yml`, `catalog/presets.yml`, `copier.yml`, the relevant files under `template/`, and existing tests before editing.
2. Define the component metadata and compatibility constraints in the catalog first. Keep each choice in exactly one architectural role unless it genuinely serves several roles.
3. Wire Copier defaults and choices to the catalog. Preserve the three simple presets and reject incompatible combinations with an actionable validator message.
4. Add functional source, dependency, configuration, test, README, and environment-variable templates for the component. Avoid placeholder-only integrations.
5. Run `uv run python scripts/compile_catalog.py --check`. If generated files are stale, run the command without `--check`, review all generated changes, then check again.
6. Add focused repository tests and generate at least one representative project. Validate its imports or endpoints, not only file presence.
7. Run the gates in `validate-python-stack` before proposing delivery.

## Invariants

- `catalog/generated/catalog.json`, `catalog/generated/choices.yml`, and `docs/reference/*.md` are compiler outputs; edit their sources instead.
- Generated projects use a `src` layout, `uv`, Ruff, pytest, typing, and reproducible dependency bounds.
- Optional layers must disappear cleanly when disabled.
- Conditional template path components must remain short enough to render on Windows.
- A deploy target keeps Docker portability; cloud IaC is limited to supported target/provider pairs.
