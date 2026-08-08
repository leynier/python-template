# Python Template

[![CI](https://github.com/leynier/python-template/actions/workflows/ci.yml/badge.svg)](https://github.com/leynier/python-template/actions/workflows/ci.yml)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/leynier/python-template/badge)](https://scorecard.dev/viewer/?uri=github.com/leynier/python-template)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Copier](https://img.shields.io/badge/template-copier-2ea44f)](https://copier.readthedocs.io)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Last commit](https://img.shields.io/github/last-commit/leynier/python-template.svg?style=flat)](https://github.com/leynier/python-template/commits)
[![Github Stars](https://img.shields.io/github/stars/leynier/python-template?style=flat&logo=github)](https://github.com/leynier/python-template/stargazers)

A modern Python project template with CI/CD ready for production.

## Usage

You need [uv](https://docs.astral.sh/uv). Nothing else.

```bash
uvx copier copy gh:leynier/python-template my-project
```

Answer the prompts and you get a working project: dependencies installed, git
initialised, tests passing.

To pull later improvements to this template into a project you already
generated:

```bash
cd my-project
uvx copier update
```

That last command is the reason this template uses Copier instead of
Cookiecutter — Cookiecutter has no way to update a project after generating it.

## What you get

One prompt, `project_type`, replaces what used to be three separate branches:

| `project_type` | What it generates                                    |
| -------------- | ---------------------------------------------------- |
| `library`      | An importable package                                |
| `cli`          | A command line app built with [Typer](https://typer.tiangolo.com) |
| `api`          | A web API built with [FastAPI](https://fastapi.tiangolo.com) |

### Tooling

- **[uv](https://docs.astral.sh/uv)** for dependencies, with a committed
  `uv.lock`, PEP 621 metadata and PEP 735 dependency groups.
- **[Ruff](https://docs.astral.sh/ruff)** for linting and formatting — one tool
  in place of flake8, black, isort and pyupgrade.
- **[ty](https://github.com/astral-sh/ty)** for type checking.
- **[deptry](https://deptry.com)** for undeclared and unused dependencies.
- **[pre-commit](https://pre-commit.com)** wiring all of the above into git
  hooks.
- `src/` layout with a `py.typed` marker.

### CI/CD, via GitHub Actions

- Test matrix across Linux, macOS and Windows × every supported Python version.
- Least-privilege `permissions:` on every workflow, concurrency groups, and
  actions pinned to full commit SHAs.
- **PyPI publishing with [Trusted Publishing](https://docs.pypi.org/trusted-publishers/)** —
  OIDC, no API tokens, with Sigstore attestations. The workflow refuses to
  publish if the git tag does not match the project version.
- **[CodeQL](https://codeql.github.com)** scanning and
  **[zizmor](https://github.com/zizmorcore/zizmor)** auditing the workflows
  themselves.
- Dependabot covering `uv`, `github-actions` and Docker.

### Documentation

Built with **[Zensical](https://zensical.org)**, the successor to Material for
MkDocs from the same team, with **[mkdocstrings](https://mkdocstrings.github.io)**
generating an API reference from your docstrings. Deployed to GitHub Pages via
OIDC on every push to `main`.

### Optional extras

A multi-stage `Dockerfile` running as a non-root user, a VS Code devcontainer,
and an `AGENTS.md` so AI coding agents pick up the project conventions.

## Two deliberate bets

This template adopts two tools that are not yet 1.0. Both are used in a way
that fails soft:

- **ty** is at `0.0.x` and has no plugin system. CI runs `ty check` with
  `continue-on-error: true`, so it reports findings without gating your build.
  When ty reaches 1.0, drop that line from `.github/workflows/ci.yml`.
- **Zensical** is at `0.0.x` and does not yet have full plugin parity with
  Material for MkDocs. mkdocstrings is verified to work — the test suite asserts
  the API reference is really rendered, not passed through — but other plugins
  may not be. Zensical reads `mkdocs.yml`, so moving back is cheap.

If you would rather not take those bets, answer `use_docs: false` and swap
`ty` for mypy in `pyproject.toml`.

## File naming

Generated projects use lowercase filenames (`readme.md`), except for files that
GitHub or tooling matches by exact name, which stay uppercase: `LICENSE`,
`CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `AGENTS.md`,
`Dockerfile` and `.github/ISSUE_TEMPLATE/`.

## Developing this template

```bash
uv sync --all-groups
uv run pytest -m "not slow"   # structural tests: what gets rendered
uv run pytest -m slow         # generates each variant and runs its toolchain
uv run pytest                 # everything
```

The slow suite is the important one: it generates every project type and runs
`uv sync`, Ruff, pytest, deptry, ty, `uv build` and the docs build inside each
generated project. The previous version of this template had no tests at all,
which is how it managed to sit broken for years without anyone noticing.

## Previous versions

The Cookiecutter version of this template is preserved on the
`legacy/cookiecutter-main`, `legacy/cookiecutter-typer` and
`legacy/cookiecutter-fastapi` branches. It is unmaintained: it targets Python
3.6, Poetry 1.1 and a retired version of the CodeQL action.

```bash
# The old, unmaintained way:
cookiecutter gh:leynier/python-template --checkout legacy/cookiecutter-main
```

## License

This project is collaborative and open source under the [MIT license](LICENSE).
Contributions are super appreciated.
