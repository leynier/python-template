"""Unit coverage for catalog validation and deterministic compilation."""

import sys
from pathlib import Path
from typing import Any

import pytest
import yaml
from pydantic import ValidationError

from scripts import compile_catalog as catalog


def component(
    component_id: str = "library",
    *,
    layer: str = "workload",
    workloads: list[str] | None = None,
    packages: list[str] | None = None,
) -> dict[str, Any]:
    """Build valid component input with focused overrides."""
    return {
        "id": component_id,
        "name": component_id.title(),
        "layer": layer,
        "tier": "stable",
        "python": ">=3.12,<3.15",
        "workloads": workloads or [],
        "packages": packages or [],
    }


def preset_inputs(answers: dict[str, object] | None = None) -> list[dict[str, Any]]:
    """Build the exact twelve presets required by the schema."""
    return [
        {
            "id": f"preset-{index}",
            "name": f"Preset {index}",
            "description": "Test preset",
            "answers": answers or {"workload": "library", "framework": "none"},
        }
        for index in range(12)
    ]


def catalogs() -> tuple[catalog.ComponentCatalog, catalog.PresetCatalog]:
    """Return small valid catalogs for artifact unit tests."""
    components = catalog.ComponentCatalog.model_validate(
        {
            "schema_version": 1,
            "components": [
                component(packages=["example>=1,<2"]),
                component(
                    "fastapi",
                    layer="interface",
                    workloads=["api"],
                ),
            ],
        }
    )
    presets = catalog.PresetCatalog.model_validate(
        {"schema_version": 1, "presets": preset_inputs()}
    )
    return components, presets


def test_component_catalog_rejects_duplicates_and_missing_workloads() -> None:
    with pytest.raises(ValidationError, match="duplicate component ids"):
        catalog.ComponentCatalog.model_validate(
            {"schema_version": 1, "components": [component(), component()]}
        )

    with pytest.raises(ValidationError, match="must declare compatible workloads"):
        catalog.ComponentCatalog.model_validate(
            {
                "schema_version": 1,
                "components": [component("fastapi", layer="framework")],
            }
        )


def test_preset_catalog_requires_exactly_twelve_unique_ids() -> None:
    with pytest.raises(ValidationError, match="expected 12 presets"):
        catalog.PresetCatalog.model_validate(
            {"schema_version": 1, "presets": preset_inputs()[:-1]}
        )

    duplicates = preset_inputs()
    duplicates[-1]["id"] = duplicates[0]["id"]
    with pytest.raises(ValidationError, match="preset ids must be unique"):
        catalog.PresetCatalog.model_validate(
            {"schema_version": 1, "presets": duplicates}
        )


def test_load_yaml_and_selected_component_ids(tmp_path: Path) -> None:
    source = tmp_path / "catalog.yml"
    source.write_text("key: value\n")
    assert catalog.load_yaml(source) == {"key": "value"}
    assert catalog._selected_component_ids(
        {
            "workload": "agent",
            "framework": "langgraph",
            "interfaces": ["fastapi"],
            "metadata": 42,
            "capability": "agents",
        }
    ) == {"agent", "langgraph", "fastapi"}


@pytest.mark.parametrize(
    ("answers", "message"),
    [
        (
            {"workload": "library", "framework": "missing"},
            "references unknown components: missing",
        ),
        ({"framework": "none"}, "must select a workload"),
        (
            {"workload": "library", "interfaces": ["fastapi"]},
            "selects components incompatible with library: fastapi",
        ),
    ],
)
def test_load_catalogs_rejects_invalid_presets(
    monkeypatch: pytest.MonkeyPatch,
    answers: dict[str, object],
    message: str,
) -> None:
    components = {
        "schema_version": 1,
        "components": [
            component(),
            component("fastapi", layer="interface", workloads=["api"]),
        ],
    }
    presets = {"schema_version": 1, "presets": preset_inputs(answers)}
    payloads = iter((components, presets))
    monkeypatch.setattr(catalog, "load_yaml", lambda _path: next(payloads))

    with pytest.raises(ValueError, match=message):
        catalog.load_catalogs()


def test_load_catalogs_accepts_the_real_catalog() -> None:
    components, presets = catalog.load_catalogs()
    assert components.components
    assert len(presets.presets) == 12


def test_build_artifacts_contains_all_public_outputs() -> None:
    components, presets = catalogs()
    artifacts = catalog.build_artifacts(components, presets)

    public = artifacts[catalog.GENERATED / "catalog.json"]
    choices = yaml.safe_load(artifacts[catalog.GENERATED / "choices.yml"])
    dependencies = artifacts[catalog.ROOT / "template" / "_catalog_dependencies.jinja"]
    assert '"schema_version": 1' in public
    assert choices["interface"] == {"Fastapi": "fastapi"}
    assert '"example>=1,<2"' in dependencies
    assert "gunicorn>=23.0.0,<24" in dependencies
    assert (
        "Library (`library`)"
        in artifacts[catalog.ROOT / "docs" / "reference" / "components.md"]
    )
    assert (
        "## Preset 0" in artifacts[catalog.ROOT / "docs" / "reference" / "presets.md"]
    )


def test_compile_catalog_checks_and_writes_artifacts(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    components, presets = catalogs()
    first = tmp_path / "generated" / "first.txt"
    second = tmp_path / "generated" / "second.txt"
    monkeypatch.setattr(catalog, "ROOT", tmp_path)
    monkeypatch.setattr(catalog, "load_catalogs", lambda: (components, presets))
    monkeypatch.setattr(
        catalog,
        "build_artifacts",
        lambda _components, _presets: {first: "one\n", second: "two\n"},
    )

    assert catalog.compile_catalog(check=True) == 1
    stderr = capsys.readouterr().err
    assert "generated/first.txt" in stderr
    assert "Run: uv run python scripts/compile_catalog.py" in stderr

    assert catalog.compile_catalog(check=False) == 0
    assert first.read_text() == "one\n"
    assert second.read_text() == "two\n"
    assert catalog.compile_catalog(check=True) == 0

    second.write_text("stale\n")
    assert catalog.compile_catalog(check=True) == 1


def test_main_forwards_the_check_flag(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    received: list[bool] = []
    monkeypatch.setattr(
        catalog,
        "compile_catalog",
        lambda *, check: received.append(check) or 0,
    )
    monkeypatch.setattr(sys, "argv", ["compile_catalog.py", "--check"])

    assert catalog.main() == 0
    assert received == [True]
