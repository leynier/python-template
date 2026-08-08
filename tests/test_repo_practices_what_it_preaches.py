"""The template repository must apply its own advice to itself.

OpenSSF Scorecard flagged this repository for a missing security policy and for
having no static analysis, while the template happily handed both to every
project it generated. These tests stop that drift from coming back.
"""

import pathlib

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent


@pytest.mark.parametrize(
    "path",
    [
        "SECURITY.md",
        "changelog.md",
        "readme.md",
        "LICENSE",
        "zizmor.yml",
    ],
)
def test_repository_has_the_files_it_generates(path: str) -> None:
    assert (REPO / path).is_file(), f"{path} is missing from the template repository"


@pytest.mark.parametrize("workflow", ["ci.yml", "codeql.yml", "scorecard.yml"])
def test_repository_runs_the_workflows_it_generates(workflow: str) -> None:
    assert (REPO / ".github" / "workflows" / workflow).is_file()


def test_required_status_check_exists() -> None:
    """Branch protection requires a check named "CI"; something must produce it.

    Renaming or dropping this job would block every future merge, which is
    exactly what happened with the job name inherited from 2021.
    """
    import yaml

    ci = yaml.safe_load((REPO / ".github" / "workflows" / "ci.yml").read_text())
    names = {job.get("name") for job in ci["jobs"].values()}

    assert "CI" in names, f"no job produces the required 'CI' check; found {names}"
