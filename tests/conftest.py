"""Shared fixtures for the template test suite."""

import os
import shutil
import subprocess
from pathlib import Path

import pytest

BASE_ANSWERS: dict[str, object] = {
    "project_name": "Demo Project",
    "description": "A project generated from the template test suite",
    "author_name": "Ada Lovelace",
    "author_email": "ada@example.com",
    "github_username": "ada",
}


@pytest.fixture(scope="session")
def uv() -> str:
    """Path to the uv executable, skipping the test session if it is missing."""
    path = shutil.which("uv")
    if path is None:  # pragma: no cover - depends on the environment
        pytest.skip("uv is not installed")
    return path


def answers(**overrides: object) -> dict[str, object]:
    """Build a full answer set from the defaults plus ``overrides``."""
    return BASE_ANSWERS | overrides


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    """Run ``cmd`` inside ``cwd`` and capture its output.

    The template's own virtualenv is stripped from the environment so that uv
    resolves the generated project's environment instead of inheriting ours.
    """
    env = os.environ.copy()
    env.pop("VIRTUAL_ENV", None)
    return subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )


def assert_ok(result: subprocess.CompletedProcess[str], label: str) -> None:
    """Fail with readable output when ``result`` exited non-zero."""
    if result.returncode != 0:
        pytest.fail(
            f"{label} failed with exit code {result.returncode}\n"
            f"--- stdout ---\n{result.stdout}\n"
            f"--- stderr ---\n{result.stderr}"
        )
