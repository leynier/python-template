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


def test_python_312_is_the_global_minimum() -> None:
    source = yaml.safe_load((REPO / "catalog" / "components.yml").read_text())
    config = yaml.safe_load((REPO / "copier.yml").read_text())

    assert config["python_version"]["choices"] == ["3.12", "3.13", "3.14"]
    for component in source["components"]:
        assert component["python"].startswith(">=3.12,"), component["id"]


def test_every_copier_component_choice_exists_in_the_catalog() -> None:
    source = yaml.safe_load((REPO / "catalog" / "components.yml").read_text())
    component_ids = {component["id"] for component in source["components"]}
    config = yaml.safe_load((REPO / "copier.yml").read_text())
    choice_questions = (
        "workload",
        "framework",
        "interfaces",
        "model_provider",
        "embedding_provider",
        "sql_store",
        "document_store",
        "vector_store",
        "graph_store",
        "cache_store",
        "sql_abstraction",
        "auth",
        "serving",
        "training_extensions",
        "mlops_tools",
        "quality_tools",
        "deploy_target",
    )

    for question in choice_questions:
        selected = set(config[question]["choices"].values()) - {"none"}
        assert selected <= component_ids, (question, selected - component_ids)


def test_data_choices_match_their_catalog_roles() -> None:
    source = yaml.safe_load((REPO / "catalog" / "components.yml").read_text())
    config = yaml.safe_load((REPO / "copier.yml").read_text())

    for role in ("sql", "document", "vector", "graph", "cache"):
        catalog_ids = {
            component["id"]
            for component in source["components"]
            if role in component.get("roles", [])
        }
        question_ids = set(config[f"{role}_store"]["choices"].values()) - {"none"}
        assert question_ids == catalog_ids, role


def test_interface_workloads_are_declared_authoritatively() -> None:
    """Catalog compatibility mirrors the runtime combinations Copier supports."""
    source = yaml.safe_load((REPO / "catalog" / "components.yml").read_text())
    expected = {
        "fastapi": {"api", "agent", "rag"},
        "flask": {"api", "agent", "rag"},
        "streamlit": {"web", "agent", "rag"},
        "gradio": {"web", "agent", "rag"},
        "chainlit": {"agent", "rag"},
        "textual": {"tui", "agent", "rag"},
        "nicegui": {"web", "agent", "rag"},
        "fasthtml": {"web", "agent", "rag"},
        "violetear": {"web", "agent", "rag"},
        "jupyterlab": {"agent", "rag", "training", "hybrid"},
    }
    actual = {
        component["id"]: set(component["workloads"])
        for component in source["components"]
        if component["id"] in expected
    }

    assert actual == expected


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
