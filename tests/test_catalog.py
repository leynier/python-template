"""The declarative catalog is the single source of truth for v0.5."""

import json
import subprocess
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent


def test_catalog_compiles_without_drift() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/compile_catalog.py", "--check"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_catalog_and_public_artifact_match() -> None:
    source = yaml.safe_load((REPO / "catalog" / "components.yml").read_text())
    generated = json.loads(
        (REPO / "catalog" / "generated" / "catalog.json").read_text()
    )

    assert [item["id"] for item in generated["components"]] == [
        item["id"] for item in source["components"]
    ]
    assert len(generated["presets"]) == 12


def test_deliberately_excluded_projects_stay_excluded() -> None:
    text = (REPO / "catalog" / "components.yml").read_text().lower()
    for excluded in ("autogoal", "odmantic", "fastui", "reflex"):
        assert excluded not in text


def test_every_preset_is_exposed_by_copier() -> None:
    config = yaml.safe_load((REPO / "copier.yml").read_text())
    preset_choices = set(config["preset"]["choices"].values())
    source = yaml.safe_load((REPO / "catalog" / "presets.yml").read_text())
    preset_ids = {preset["id"] for preset in source["presets"]}

    assert preset_choices == preset_ids | {"custom"}


def test_compiled_dependency_template_contains_every_catalog_package() -> None:
    source = yaml.safe_load((REPO / "catalog" / "components.yml").read_text())
    compiled = (REPO / "template" / "_catalog_dependencies.jinja").read_text()

    for component in source["components"]:
        for package in component.get("packages", []):
            assert package in compiled, (component["id"], package)


def test_template_paths_fit_windows_checkout_limits() -> None:
    longest = max(
        (path.relative_to(REPO).as_posix() for path in (REPO / "template").rglob("*")),
        key=len,
    )
    # Hosted Actions adds roughly 40 characters before the repository path.
    assert len(longest) < 200, longest
