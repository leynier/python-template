"""`copier update` must work -- it is the whole reason for choosing Copier.

Cookiecutter cannot update already-generated projects. If this test breaks, the
main benefit of the migration is gone, so it is worth testing explicitly rather
than trusting that Copier "just works".
"""

import shutil
from pathlib import Path

import copier
import pytest
from conftest import BASE_ANSWERS, run

TEMPLATE_ROOT = Path(__file__).resolve().parent.parent


def _git(args: list[str], cwd: Path) -> None:
    result = run(["git", *args], cwd)
    if result.returncode != 0:  # pragma: no cover - only on a broken environment
        pytest.fail(f"git {' '.join(args)} failed:\n{result.stderr}")


def _init_repo(path: Path, tag: str) -> None:
    _git(["init", "--initial-branch=main"], path)
    _git(["config", "user.email", "test@example.com"], path)
    _git(["config", "user.name", "Test"], path)
    _git(["add", "-A"], path)
    _git(["commit", "-m", "initial"], path)
    _git(["tag", tag], path)


@pytest.fixture
def template_clone(tmp_path: Path) -> Path:
    """A standalone git copy of the template, tagged v1.0.0."""
    clone = tmp_path / "template"
    shutil.copytree(
        TEMPLATE_ROOT,
        clone,
        ignore=shutil.ignore_patterns(
            ".git", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache"
        ),
    )
    _init_repo(clone, "v1.0.0")
    return clone


@pytest.mark.slow
def test_update_pulls_in_template_changes(template_clone: Path, tmp_path: Path) -> None:
    """A project generated from v1.0.0 receives a change made in v1.0.1."""
    project = tmp_path / "project"

    copier.run_copy(
        str(template_clone),
        str(project),
        data=BASE_ANSWERS | {"workload": "library", "framework": "none"},
        defaults=True,
        unsafe=True,
        vcs_ref="v1.0.0",
        quiet=True,
    )
    assert (project / ".copier-answers.yml").is_file()
    _init_repo(project, "generated")

    # Advance the template: add a file that did not exist in v1.0.0.
    (template_clone / "template" / "NOTICE.md.jinja").write_text(
        "# Notice for {{ project_name }}\n"
    )
    _git(["add", "-A"], template_clone)
    _git(["commit", "-m", "add notice"], template_clone)
    _git(["tag", "v1.0.1"], template_clone)

    copier.run_update(
        str(project),
        defaults=True,
        unsafe=True,
        overwrite=True,
        quiet=True,
    )

    notice = project / "NOTICE.md"
    assert notice.is_file(), "copier update did not add the new template file"
    assert "Notice for Demo Project" in notice.read_text()


@pytest.mark.slow
def test_update_preserves_local_edits(template_clone: Path, tmp_path: Path) -> None:
    """An unrelated file the user wrote survives the update."""
    project = tmp_path / "project"

    copier.run_copy(
        str(template_clone),
        str(project),
        data=BASE_ANSWERS | {"workload": "library", "framework": "none"},
        defaults=True,
        unsafe=True,
        vcs_ref="v1.0.0",
        quiet=True,
    )

    user_file = project / "src" / "demo_project" / "my_module.py"
    user_file.write_text('"""Written by the user."""\n')
    _init_repo(project, "generated")

    (template_clone / "template" / "NOTICE.md.jinja").write_text("# Notice\n")
    _git(["add", "-A"], template_clone)
    _git(["commit", "-m", "add notice"], template_clone)
    _git(["tag", "v1.0.1"], template_clone)

    copier.run_update(
        str(project), defaults=True, unsafe=True, overwrite=True, quiet=True
    )

    assert user_file.is_file(), "copier update deleted a user-authored file"
    assert "Written by the user." in user_file.read_text()
