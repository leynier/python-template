# Contributing to Python Template

Contributions are welcome, from a focused bug report to a complete component
integration. The repository generates many possible projects, so changes must
keep the catalog, templates, and executable tests aligned.

## Report an issue

Use the [issue forms](https://github.com/leynier/python-template/issues/new/choose).
For a generated-project bug, include the relevant `.copier-answers.yml`, the
command that failed, and its output. Remove credentials before posting.

Security vulnerabilities belong in a private
[GitHub Security Advisory](https://github.com/leynier/python-template/security/advisories/new),
not a public issue.

## Propose a component

Explain:

- which architectural layer and workload it serves;
- how it differs from supported components in that role;
- its maintained Python versions and upstream stability;
- what functional source and configuration the template should generate; and
- how CI can validate it without paid credentials.

A new proposal should meet the inclusion criteria in the
[support model](docs/concepts/support.md).

## Develop a change

Create a focused branch from `main` and install every repository group:

```bash
git switch main
git pull --ff-only
git switch -c feat/short-description
uv sync --all-groups
```

For a catalog change, edit `catalog/components.yml` or `catalog/presets.yml`,
then compile deterministic outputs:

```bash
uv run python scripts/compile_catalog.py
uv run python scripts/compile_catalog.py --check
```

Do not edit `catalog/generated/`, `docs/reference/`, or
`template/_catalog_dependencies.jinja` by hand. Add functional source,
dependency, configuration, documentation, and tests for the selected component.

## Validate before opening a PR

```bash
uv run python scripts/compile_catalog.py --check
uv run ruff check .
uv run ruff format --check .
uv run pytest -n auto
uv run --group docs zensical build --clean --strict
npx skills add . --list
```

Generate and exercise at least one representative project. A test that only
checks file presence is not enough when an import, CLI command, endpoint, tool,
training step, or container health route can be validated locally.

Hosted CI repeats generated-project checks on Linux, macOS, and Windows. Keep
conditional source paths short enough for Windows temporary directories.

## Pull requests

Keep each PR centered on one layer or cohesive outcome. Describe the supported
combination, commands run, external checks that were unavailable, and any
credential-gated behavior that remains operationally unverified. By submitting
a contribution, you agree that it is licensed under this repository's
[MIT license](LICENSE).

## Contributors

- Leynier Gutiérrez González ([@leynier](https://github.com/leynier))
