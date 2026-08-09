"""Repository documentation and Vercel deployment contract."""

import json
import pathlib
import tomllib

REPO = pathlib.Path(__file__).parents[1]


def _nav_targets(items: list[dict[str, object]]) -> list[str]:
    targets: list[str] = []
    for item in items:
        value = next(iter(item.values()))
        if isinstance(value, str):
            targets.append(value)
        else:
            targets.extend(_nav_targets(value))
    return targets


def test_zensical_navigation_points_to_real_repository_docs() -> None:
    config = tomllib.loads((REPO / "zensical.toml").read_text())
    project = config["project"]

    assert project["site_dir"] == "site"
    assert project["site_url"] == "https://python-template.leynier.dev/"
    for target in _nav_targets(project["nav"]):
        assert (REPO / "docs" / target).is_file(), target


def test_vercel_builds_the_zensical_static_output() -> None:
    config = json.loads((REPO / "vercel.json").read_text())

    # The repository has a pyproject.toml for its own tooling, but the deployed
    # artifact is static. Without this override Vercel selects its Python preset
    # and rejects the repository for not having an application entry point.
    assert config["framework"] is None
    assert config["outputDirectory"] == "site"
    assert "zensical build" in config["buildCommand"]
    assert "--strict" in config["buildCommand"]
    assert config["installCommand"] == "uv sync --locked --only-group docs"


def test_ci_builds_repository_documentation() -> None:
    workflow = (REPO / ".github" / "workflows" / "ci.yml").read_text()

    assert "Repository documentation" in workflow
    assert "zensical build --clean --strict" in workflow
    assert "needs: [lint, structure, presets, docs, toolchain, zizmor]" in workflow


def test_readme_presents_layers_simple_projects_and_agent_skills() -> None:
    readme = (REPO / "readme.md").read_text()

    for marker in (
        "Generate production-ready Python and AI stacks",
        "Typer CLI",
        "FastAPI API",
        "FastMCP",
        "Pydantic AI",
        "Lingo",
        "Violetear",
        "npx skills add leynier/python-template --list",
        "Pulumi",
        "Terraform",
    ):
        assert marker in readme
