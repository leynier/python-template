"""Behavioural tests: the generated project actually installs and passes its own checks.

These are the tests that stop the template from rotting silently.

Each one creates a real virtual environment, which is the dominant cost -- and
on Windows runners it is roughly ten times slower than on Linux. So they are
marked ``slow``, they are written to reuse one environment per test rather than
one per assertion, and CI runs them with ``-n auto``.
"""

import pytest
from conftest import answers, assert_ok, run

SIMPLE_WORKLOADS = ["library", "cli", "api"]


@pytest.mark.slow
@pytest.mark.parametrize("workload", SIMPLE_WORKLOADS)
def test_generated_project_passes_its_own_checks(copie, uv: str, workload: str) -> None:
    """Install the generated project and run the full quality gate on it."""
    result = copie.copy(extra_answers=answers(workload=workload))
    assert result.exception is None, result.exception
    project = result.project_dir

    assert_ok(run([uv, "sync", "--all-groups"], project), "uv sync")
    assert_ok(run([uv, "run", "ruff", "check", "."], project), "ruff check")
    assert_ok(
        run([uv, "run", "ruff", "format", "--check", "."], project), "ruff format"
    )
    assert_ok(run([uv, "run", "deptry", "src"], project), "deptry")

    pytest_run = run([uv, "run", "pytest", "-q"], project)
    assert_ok(pytest_run, "pytest")
    # Guards against a config that collects tests but never runs them, which is
    # how a broken asyncio_mode setting once hid three passing-looking tests.
    assert " passed" in pytest_run.stdout, (
        f"no tests were executed:\n{pytest_run.stdout}"
    )

    # ty is pre-1.0 and advisory in CI, so a finding must not fail the suite.
    # We still assert that it runs at all, which catches a broken config.
    ty = run([uv, "run", "ty", "check"], project)
    assert ty.returncode in (0, 1), f"ty crashed:\n{ty.stdout}\n{ty.stderr}"

    if workload == "cli":
        hello = run([uv, "run", "demo-project", "hello", "Ada"], project)
        assert_ok(hello, "cli entry point")
        assert "Hello, Ada!" in hello.stdout


@pytest.mark.slow
@pytest.mark.parametrize("workload", SIMPLE_WORKLOADS)
def test_generated_project_builds(copie, uv: str, workload: str) -> None:
    """The project produces an sdist and a wheel.

    ``uv build`` provisions its own build environment, so this deliberately
    does not run ``uv sync`` first.
    """
    result = copie.copy(extra_answers=answers(workload=workload))
    project = result.project_dir

    assert_ok(run([uv, "build"], project), "uv build")

    artifacts = {path.suffix for path in (project / "dist").iterdir()}
    assert ".whl" in artifacts
    assert ".gz" in artifacts


@pytest.mark.slow
def test_docs_build_with_api_reference(copie, uv: str) -> None:
    """Zensical builds the site, and mkdocstrings really renders the API page.

    Zensical does not have full plugin parity with Material for MkDocs, so the
    mkdocstrings integration is asserted rather than assumed.
    """
    project = copie.copy(extra_answers=answers(use_docs=True)).project_dir

    assert_ok(run([uv, "sync", "--all-groups"], project), "uv sync")
    assert_ok(
        run([uv, "run", "--group", "docs", "zensical", "build"], project),
        "zensical build",
    )

    assert (project / "site" / "index.html").is_file()

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
