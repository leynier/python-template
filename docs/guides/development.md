# Develop the template

## Set up

```bash
uv sync --all-groups
```

Catalog sources live in `catalog/components.yml` and `catalog/presets.yml`.
Generated JSON, Copier choices, dependency mapping, and reference pages must not
be edited by hand.

## Validate catalog changes

```bash
uv run python scripts/compile_catalog.py
uv run python scripts/compile_catalog.py --check
```

Review every generated diff. Then add the functional template, dependency,
configuration, documentation, and tests for the component.

## Run the gates

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest -n auto
uv run --group docs zensical build --clean --strict
```

Focused tests shorten iteration, but delivery requires the full suite. Hosted
CI validates generated toolchains on Linux, macOS, and Windows and runs the
credential-free AI preset vertical slices on Linux.

## Preview these docs

```bash
uv run --group docs zensical serve
```

The repository documentation is independent of the optional documentation
generated inside a user's project. Vercel builds this root site from
`zensical.toml`; generated projects retain their own Zensical configuration.
