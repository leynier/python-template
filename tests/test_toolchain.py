"""Behavioural tests: the generated project actually installs and passes its own checks.

These are the tests that stop the template from rotting silently. They are slow
because each one creates a real virtual environment, so they are marked ``slow``
and can be deselected with ``-m "not slow"``.
"""

import pytest
from conftest import answers, assert_ok, run

PROJECT_TYPES = ["library", "cli", "api"]


@pytest.mark.slow
@pytest.mark.parametrize("project_type", PROJECT_TYPES)
def test_generated_project_passes_its_own_checks(
    copie, uv: str, project_type: str
) -> None:
    """Install the generated project and run the full quality gate on it."""
    result = copie.copy(extra_answers=answers(project_type=project_type))
    assert result.exception is None, result.exception
    project = result.project_dir

    assert_ok(run([uv, "sync", "--all-groups"], project), "uv sync")
    assert_ok(run([uv, "run", "ruff", "check", "."], project), "ruff check")
    assert_ok(
        run([uv, "run", "ruff", "format", "--check", "."], project), "ruff format"
    )
    assert_ok(run([uv, "run", "pytest", "-q"], project), "pytest")
    assert_ok(run([uv, "run", "deptry", "src"], project), "deptry")

    # ty is pre-1.0 and advisory in CI, so a finding must not fail the suite.
    # We still assert that it runs at all, which catches a broken config.
    ty = run([uv, "run", "ty", "check"], project)
    assert ty.returncode in (0, 1), f"ty crashed:\n{ty.stdout}\n{ty.stderr}"


@pytest.mark.slow
@pytest.mark.parametrize("project_type", PROJECT_TYPES)
def test_generated_project_builds(copie, uv: str, project_type: str) -> None:
    """The project produces an sdist and a wheel."""
    result = copie.copy(extra_answers=answers(project_type=project_type))
    project = result.project_dir

    assert_ok(run([uv, "build"], project), "uv build")

    artifacts = {path.suffix for path in (project / "dist").iterdir()}
    assert ".whl" in artifacts
    assert ".gz" in artifacts


@pytest.mark.slow
def test_generated_tests_actually_run(copie, uv: str) -> None:
    """Guard against a pytest config that collects tests but never runs them."""
    project = copie.copy(extra_answers=answers(project_type="api")).project_dir

    assert_ok(run([uv, "sync", "--all-groups"], project), "uv sync")
    pytest_run = run([uv, "run", "pytest", "-q"], project)
    assert_ok(pytest_run, "pytest")
    assert " passed" in pytest_run.stdout, (
        f"no tests were executed:\n{pytest_run.stdout}"
    )


@pytest.mark.slow
def test_docs_build(copie, uv: str) -> None:
    """Zensical builds the generated documentation site."""
    project = copie.copy(extra_answers=answers(use_docs=True)).project_dir

    assert_ok(run([uv, "sync", "--all-groups"], project), "uv sync")
    assert_ok(
        run([uv, "run", "--group", "docs", "zensical", "build"], project),
        "zensical build",
    )
    assert (project / "site" / "index.html").is_file()


@pytest.mark.slow
def test_api_reference_is_actually_rendered(copie, uv: str) -> None:
    """mkdocstrings really runs under Zensical, rather than emitting raw '::: '.

    Zensical does not have full plugin parity with Material for MkDocs, so this
    asserts the integration rather than assuming it.
    """
    project = copie.copy(extra_answers=answers(use_docs=True)).project_dir

    assert_ok(run([uv, "sync", "--all-groups"], project), "uv sync")
    assert_ok(
        run([uv, "run", "--group", "docs", "zensical", "build"], project),
        "zensical build",
    )

    page = (project / "site" / "api" / "index.html").read_text()
    # mkdocstrings-specific markup, not just the docstring text.
    assert "doc-object" in page
    # An unprocessed directive would mean the plugin never ran.
    assert ":::" not in page
    assert "greet" in page


@pytest.mark.slow
def test_poe_check_passes(copie, uv: str) -> None:
    """The task runner works and its aggregate task passes on a fresh project."""
    project = copie.copy(extra_answers=answers()).project_dir

    assert_ok(run([uv, "sync", "--all-groups"], project), "uv sync")
    assert_ok(run([uv, "run", "poe", "check"], project), "poe check")


@pytest.mark.slow
def test_cli_entrypoint_works(copie, uv: str) -> None:
    """The console script is installed and runs."""
    project = copie.copy(extra_answers=answers(project_type="cli")).project_dir

    assert_ok(run([uv, "sync", "--all-groups"], project), "uv sync")
    hello = run([uv, "run", "demo-project", "hello", "Ada"], project)
    assert_ok(hello, "cli hello")
    assert "Hello, Ada!" in hello.stdout
