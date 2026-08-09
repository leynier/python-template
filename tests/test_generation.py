"""Structural tests: every variant renders, and renders the right files."""

import pathlib

import pytest
from conftest import answers

SIMPLE_WORKLOADS = ["library", "cli", "api"]


def test_template_source_paths_fit_windows_git() -> None:
    """Leave room for the deep temporary roots used by Windows CI."""
    template_root = pathlib.Path(__file__).parents[1] / "template"
    relative_paths = [
        str(path.relative_to(template_root.parent))
        for path in template_root.rglob("*")
        if path.is_file()
    ]
    longest = max(relative_paths, key=len)

    assert len(longest) <= 185, f"Template path is too long ({len(longest)}): {longest}"


@pytest.mark.parametrize("workload", SIMPLE_WORKLOADS)
def test_generates_cleanly(copie, workload: str) -> None:
    """Each workload renders without error."""
    result = copie.copy(extra_answers=answers(workload=workload))

    assert result.exception is None, result.exception
    assert result.exit_code == 0
    assert result.project_dir.is_dir()


@pytest.mark.parametrize("workload", SIMPLE_WORKLOADS)
def test_core_layout(copie, workload: str) -> None:
    """The src layout, typing marker and answers file are always present."""
    result = copie.copy(extra_answers=answers(workload=workload))
    project = result.project_dir

    assert (project / "src" / "demo_project" / "__init__.py").is_file()
    assert (project / "src" / "demo_project" / "py.typed").is_file()
    assert (project / "tests" / "test_demo_project.py").is_file()
    assert (project / "pyproject.toml").is_file()
    assert not (project / "_catalog_dependencies").exists()
    # Without this file `copier update` cannot work at all.
    assert (project / ".copier-answers.yml").is_file()


@pytest.mark.parametrize("workload", SIMPLE_WORKLOADS)
def test_lowercase_readme(copie, workload: str) -> None:
    """Readme is lowercase, and the packaging metadata agrees with it."""
    result = copie.copy(extra_answers=answers(workload=workload))
    project = result.project_dir

    assert (project / "readme.md").is_file()
    assert not (project / "README.md").exists()
    # A mismatch here makes `uv build` fail.
    assert 'readme = "readme.md"' in (project / "pyproject.toml").read_text()


@pytest.mark.parametrize("workload", SIMPLE_WORKLOADS)
def test_convention_files_stay_uppercase(copie, workload: str) -> None:
    """Files that GitHub and tooling match by exact name keep their case."""
    result = copie.copy(extra_answers=answers(workload=workload))
    project = result.project_dir

    for name in ("LICENSE", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "SECURITY.md"):
        assert (project / name).is_file(), name


def test_entrypoints_per_type(copie) -> None:
    """Each workload gets its own entry point module, and only that one."""
    library = copie.copy(extra_answers=answers(workload="library")).project_dir
    cli = copie.copy(extra_answers=answers(workload="cli")).project_dir
    api = copie.copy(extra_answers=answers(workload="api")).project_dir

    assert not (library / "src" / "demo_project" / "cli.py").exists()
    assert not (library / "src" / "demo_project" / "api.py").exists()

    assert (cli / "src" / "demo_project" / "cli.py").is_file()
    assert not (cli / "src" / "demo_project" / "api.py").exists()
    assert "[project.scripts]" in (cli / "pyproject.toml").read_text()

    assert (api / "src" / "demo_project" / "api.py").is_file()
    assert not (api / "src" / "demo_project" / "cli.py").exists()
    assert (
        'demo-project = "demo_project.api:main"' in (api / "pyproject.toml").read_text()
    )


def test_simple_presets_remain_first_class(copie) -> None:
    """The three simple recipes must never require an AI component."""
    cases = {
        "python-library": ("library", "none"),
        "typer-cli": ("cli", "typer"),
        "fastapi-api": ("api", "fastapi"),
    }
    for preset, (workload, framework) in cases.items():
        project = copie.copy(extra_answers=answers(preset=preset)).project_dir
        saved = (project / ".copier-answers.yml").read_text()
        assert f"workload: {workload}" in saved
        assert f"framework: {framework}" in saved
        assert "ai_capabilities: none" in saved


def test_flask_is_available_for_a_simple_api(copie) -> None:
    project = copie.copy(
        extra_answers=answers(
            preset="custom",
            workload="api",
            ai_capabilities="none",
            framework="flask",
        )
    ).project_dir

    api = (project / "src" / "demo_project" / "api.py").read_text()
    pyproject = (project / "pyproject.toml").read_text()
    tests = (project / "tests" / "test_demo_project.py").read_text()
    assert "from flask import Flask" in api
    assert '"flask>=3.1.2,<4"' in pyproject
    assert "app.test_client()" in tests


def test_sql_and_auth_layers_generate_together(copie) -> None:
    project = copie.copy(
        extra_answers=answers(
            preset="custom",
            workload="api",
            framework="fastapi",
            sql_store="sqlite",
            sql_abstraction="sqlmodel",
            auth="api-key",
        )
    ).project_dir

    package = project / "src" / "demo_project"
    pyproject = (project / "pyproject.toml").read_text()
    assert (package / "data.py").is_file()
    assert (package / "auth.py").is_file()
    assert (package / "settings.py").is_file()
    assert (project / "alembic.ini").is_file()
    assert (project / "migrations" / "env.py").is_file()
    assert '"sqlmodel>=0.0.39,<0.1"' in pyproject
    assert '"alembic>=1.19.1,<2"' in pyproject


def test_optional_features_are_omitted(copie) -> None:
    """Turning features off removes their files entirely."""
    result = copie.copy(
        extra_answers=answers(
            use_docs=False,
            publish_to_pypi=False,
            use_docker=False,
            use_devcontainer=False,
            use_codeql=False,
            agent_instructions=False,
        )
    )
    project = result.project_dir

    assert not (project / "zensical.toml").exists()
    assert not (project / "docs").exists()
    assert not (project / ".github" / "workflows" / "docs.yml").exists()
    assert not (project / ".github" / "workflows" / "publish.yml").exists()
    assert not (project / ".github" / "workflows" / "codeql.yml").exists()
    assert not (project / "Dockerfile").exists()
    assert not (project / ".devcontainer").exists()
    assert not (project / "AGENTS.md").exists()
    # CI and the workflow audit are not optional.
    assert (project / ".github" / "workflows" / "ci.yml").is_file()
    assert (project / ".github" / "workflows" / "zizmor.yml").is_file()


def test_optional_features_are_included(copie) -> None:
    """Turning features on renders their files."""
    result = copie.copy(
        extra_answers=answers(
            workload="api",
            use_docs=True,
            publish_to_pypi=True,
            use_docker=True,
            use_devcontainer=True,
        )
    )
    project = result.project_dir

    assert (project / "zensical.toml").is_file()
    assert (project / "docs" / "index.md").is_file()
    assert (project / "Dockerfile").is_file()
    assert (project / ".devcontainer" / "devcontainer.json").is_file()
    assert (project / ".github" / "workflows" / "publish.yml").is_file()


def test_license_texts(copie) -> None:
    """Each license choice produces its real text, and 'none' produces no file."""
    cases = {
        "MIT": "MIT License",
        "Apache-2.0": "Apache License",
        "BSD-3-Clause": "Redistribution and use in source and binary forms",
        "GPL-3.0-or-later": "GNU GENERAL PUBLIC LICENSE",
    }
    for spdx, marker in cases.items():
        project = copie.copy(
            extra_answers=answers(license=spdx, copyright_year="2026")
        ).project_dir
        text = (project / "LICENSE").read_text()
        assert marker in text, spdx
        # The raw source texts must never leak into the generated project.
        assert not (project / "licenses").exists()

    unlicensed = copie.copy(extra_answers=answers(license="none")).project_dir
    assert not (unlicensed / "LICENSE").exists()
    assert "license" not in (unlicensed / "pyproject.toml").read_text().split(
        "[build-system]"
    )[0].lower().replace("license-files", "")


def test_mit_license_is_personalised(copie) -> None:
    """The copyright line carries the author's name and the chosen year."""
    project = copie.copy(
        extra_answers=answers(license="MIT", copyright_year="2031")
    ).project_dir

    assert "Copyright (c) 2031 Ada Lovelace" in (project / "LICENSE").read_text()


def test_python_version_drives_the_ci_matrix(copie) -> None:
    """Only versions at or above the chosen minimum appear in CI."""
    project = copie.copy(extra_answers=answers(python_version="3.12")).project_dir
    workflow = (project / ".github" / "workflows" / "ci.yml").read_text()

    assert '"3.12"' in workflow
    assert '"3.13"' in workflow
    assert '"3.11"' not in workflow
    assert 'requires-python = ">=3.12"' in (project / "pyproject.toml").read_text()


def test_eol_python_versions_are_not_offered(copie) -> None:
    """Versions at or near end of life must not be selectable.

    v0.5 intentionally starts at 3.12, and older versions must not return.
    """
    import yaml

    config = yaml.safe_load(
        (pathlib.Path(__file__).resolve().parent.parent / "copier.yml").read_text()
    )
    choices = config["python_version"]["choices"]

    assert "3.10" not in choices
    assert "3.9" not in choices
    assert "3.11" not in choices
    assert config["python_version"]["default"] in choices


def test_workflows_have_no_leftover_jinja(copie) -> None:
    """GitHub Actions expressions survive rendering intact."""
    project = copie.copy(extra_answers=answers()).project_dir
    ci = (project / ".github" / "workflows" / "ci.yml").read_text()

    # The raw blocks must have produced real GitHub expressions...
    assert "${{ github.workflow }}" in ci
    assert "${{ matrix.python-version }}" in ci
    # ...and no Jinja tag may remain anywhere in the workflows.
    for workflow in (project / ".github" / "workflows").iterdir():
        content = workflow.read_text()
        assert "{%" not in content, workflow.name
        assert "{{ " not in content.replace("${{ ", ""), workflow.name


def test_actions_are_version_pinned(copie) -> None:
    """Every action is pinned to a release tag, never to a branch.

    Tags are used rather than commit SHAs for readability. What must never
    happen is a floating branch reference like `@main`, which silently changes
    under you.
    """
    import re

    project = copie.copy(extra_answers=answers()).project_dir
    uses = re.compile(r"uses:\s*(?P<action>[\w.-]+/[\w.-]+(?:/[\w.-]+)*)@(?P<ref>\S+)")

    found = 0
    for workflow in (project / ".github" / "workflows").iterdir():
        for match in uses.finditer(workflow.read_text()):
            found += 1
            ref = match["ref"]
            assert re.fullmatch(r"v\d+(\.\d+)*", ref), (
                f"{workflow.name}: {match['action']} is pinned to {ref!r}, "
                "expected a version tag such as v1 or v1.2.3"
            )
    assert found > 0


def test_zizmor_config_allows_tag_pins(copie) -> None:
    """The zizmor policy matches the pinning strategy actually in use.

    zizmor requires commit SHAs by default, so without this config every
    workflow would report an unpinned-uses finding.
    """
    project = copie.copy(extra_answers=answers()).project_dir
    config = (project / "zizmor.yml").read_text()

    assert "unpinned-uses" in config
    assert "ref-pin" in config


@pytest.mark.parametrize("workload", SIMPLE_WORKLOADS)
def test_changelog_is_lowercase(copie, workload: str) -> None:
    """A starter changelog ships with every project, lowercase per convention."""
    project = copie.copy(extra_answers=answers(workload=workload)).project_dir

    assert (project / "changelog.md").is_file()
    assert not (project / "CHANGELOG.md").exists()


def test_tasks_are_defined_in_pyproject(copie) -> None:
    """The Makefile was replaced by task definitions in pyproject.toml."""
    project = copie.copy(extra_answers=answers()).project_dir
    pyproject = (project / "pyproject.toml").read_text()

    assert not (project / "Makefile").exists()
    assert "[tool.poe.tasks]" in pyproject
    for task in ("lint", "format", "test", "check", "types"):
        assert f"\n{task} = " in pyproject, task


def test_api_reference_page(copie) -> None:
    """Docs include an mkdocstrings API page wired into the nav."""
    project = copie.copy(extra_answers=answers(use_docs=True)).project_dir

    api = (project / "docs" / "api.md").read_text()
    assert "::: demo_project" in api

    config = (project / "zensical.toml").read_text()
    assert 'plugins = ["mkdocstrings"]' in config
    assert "api.md" in config


def test_publish_workflow_does_not_cache(copie) -> None:
    """The release build must not restore a cache it could be poisoned by.

    zizmor flags this as a high severity cache-poisoning risk: the job that
    builds the published artifacts should not trust a shared cache.
    """
    project = copie.copy(
        extra_answers=answers(workload="library", publish_to_pypi=True)
    ).project_dir
    publish = (project / ".github" / "workflows" / "publish.yml").read_text()

    assert "enable-cache: true" not in publish
    assert "enable-cache: false" in publish


def test_publish_workflow_uses_trusted_publishing(copie) -> None:
    """No PyPI passwords or API tokens anywhere; OIDC only."""
    project = copie.copy(
        extra_answers=answers(workload="library", publish_to_pypi=True)
    ).project_dir
    publish = (project / ".github" / "workflows" / "publish.yml").read_text()

    assert "id-token: write" in publish
    assert "pypa/gh-action-pypi-publish" in publish
    for forbidden in ("PYPI_PASSWORD", "PYPI_USERNAME", "PYPI_API_TOKEN", "password:"):
        assert forbidden not in publish, forbidden


def test_social_links_render_only_when_selected(copie) -> None:
    """Only the chosen networks reach zensical.toml."""
    project = copie.copy(
        extra_answers=answers(
            use_docs=True,
            social_links=["github", "telegram"],
            telegram_handle="ada",
        )
    ).project_dir
    config = (project / "zensical.toml").read_text()

    assert "https://t.me/ada" in config
    assert "fontawesome/brands/github" in config
    assert "linkedin" not in config
    assert "instagram" not in config
