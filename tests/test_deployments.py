"""Structural coverage for deployment targets and cloud IaC adapters."""

import ast
import json
import tomllib
from pathlib import Path
from shutil import copytree, ignore_patterns

import hcl2
import yaml
from conftest import answers
from copier import run_copy

TARGETS: dict[str, tuple[dict[str, object], list[str]]] = {
    "docker": ({"workload": "api", "framework": "fastapi"}, ["compose.yaml"]),
    "render": ({"workload": "api", "framework": "fastapi"}, ["render.yaml"]),
    "fly": ({"workload": "api", "framework": "fastapi"}, ["fly.toml"]),
    "vercel": (
        {"workload": "api", "framework": "fastapi"},
        ["vercel.json", "api/index.py"],
    ),
    "railway": (
        {"workload": "api", "framework": "fastapi"},
        ["railway.toml"],
    ),
    "hf-spaces": (
        {"workload": "api", "framework": "fastapi"},
        ["README.md"],
    ),
    "modal": (
        {"workload": "api", "framework": "fastapi"},
        ["deploy/modal_app.py", "src/demo_project/deploy/modal_app.py"],
    ),
    "runpod": (
        {"workload": "inference", "framework": "none", "serving": "litellm"},
        ["handler.py", "src/demo_project/deploy/runpod_handler.py"],
    ),
    "bentocloud": (
        {"workload": "inference", "framework": "none", "serving": "bentoml"},
        ["bentofile.yaml", "src/demo_project/deploy/bentoml_service.py"],
    ),
    "aws-ecs": (
        {"workload": "api", "framework": "fastapi"},
        ["deploy/task-definition.json"],
    ),
    "aws-sagemaker": (
        {"workload": "inference", "framework": "none", "serving": "bentoml"},
        ["deploy/sagemaker-model.json"],
    ),
    "cloud-run": (
        {"workload": "api", "framework": "fastapi"},
        ["service.yaml"],
    ),
    "vertex-ai": (
        {"workload": "inference", "framework": "none", "serving": "bentoml"},
        ["deploy/vertex-model.json"],
    ),
    "azure-container-apps": (
        {"workload": "api", "framework": "fastapi"},
        ["deploy/container-app.yaml"],
    ),
    "azure-ml": (
        {"workload": "inference", "framework": "none", "serving": "bentoml"},
        ["deploy/endpoint.yml", "deploy/deployment.yml"],
    ),
}


def working_template(tmp_path: Path) -> Path:
    """Copy staged template changes without VCS checkout or Copier tasks."""
    template = tmp_path / "template"
    copytree(
        Path.cwd(),
        template,
        ignore=ignore_patterns(".git", ".venv", ".pytest_cache", "__pycache__"),
    )
    return template


def render(template: Path, destination: Path, **overrides: object) -> Path:
    template_answers: dict[str, object] = {
        "preset": "custom",
        "ai_capabilities": "none",
        "deploy_target": "none",
        "use_docs": False,
        "use_codeql": False,
        "use_docker": False,
    }
    run_copy(
        str(template),
        destination,
        data=answers(**(template_answers | overrides)),
        defaults=True,
        unsafe=True,
        skip_tasks=True,
    )
    return destination


def test_every_deployment_target_has_a_portable_adapter(tmp_path: Path) -> None:
    template = working_template(tmp_path)
    for target, (stack_answers, expected) in TARGETS.items():
        project = render(
            template,
            tmp_path / target,
            deploy_target=target,
            **stack_answers,
        )
        assert (project / "Dockerfile").is_file(), target
        assert (project / ".dockerignore").is_file(), target
        assert (project / "deploy/README.md").is_file(), target
        for relative in expected:
            assert (project / relative).is_file(), f"{target}: {relative}"

        for json_file in project.rglob("*.json"):
            json.loads(json_file.read_text())
        for toml_file in project.rglob("*.toml"):
            tomllib.loads(toml_file.read_text())
        for yaml_file in [*project.rglob("*.yaml"), *project.rglob("*.yml")]:
            yaml.safe_load(yaml_file.read_text())
        for python_file in project.rglob("*.py"):
            ast.parse(python_file.read_text(), filename=str(python_file))


def test_cloud_targets_render_both_iac_options(tmp_path: Path) -> None:
    template = working_template(tmp_path)
    cloud_targets = {
        target: values
        for target, values in TARGETS.items()
        if target
        in {
            "aws-ecs",
            "aws-sagemaker",
            "cloud-run",
            "vertex-ai",
            "azure-container-apps",
            "azure-ml",
        }
    }
    for target, (stack_answers, _) in cloud_targets.items():
        pulumi = render(
            template,
            tmp_path / f"{target}-pulumi",
            deploy_target=target,
            iac_provider="pulumi",
            **stack_answers,
        )
        ast.parse((pulumi / "infra/pulumi/__main__.py").read_text())
        tomllib.loads((pulumi / "infra/pulumi/pyproject.toml").read_text())
        yaml.safe_load((pulumi / "infra/pulumi/Pulumi.yaml").read_text())

        terraform = render(
            template,
            tmp_path / f"{target}-terraform",
            deploy_target=target,
            iac_provider="terraform",
            **stack_answers,
        )
        for hcl_file in (terraform / "infra/terraform").glob("*.tf"):
            with hcl_file.open() as stream:
                hcl2.load(stream)
