"""Linux integration tests for the agent, MCP, RAG and interface presets."""

from pathlib import Path
from shutil import copytree, ignore_patterns

import pytest
from conftest import answers, assert_ok, run
from copier import run_copy

PRESETS = {
    "fastmcp-server": ["src/demo_project/mcp.py"],
    "pydantic-ai-openai": ["src/demo_project/agent.py", ".env.example"],
    "google-adk-gemini": ["src/demo_project/agent.py", ".env.example"],
    "strands-bedrock": ["src/demo_project/agent.py", ".env.example"],
    "langgraph-anthropic-api": [
        "src/demo_project/agent.py",
        "src/demo_project/interfaces/fastapi_app.py",
    ],
    "llamaindex-rag": [
        "src/demo_project/rag.py",
        "src/demo_project/data.py",
        "src/demo_project/interfaces/gradio_app.py",
    ],
    "local-lingo-app": [
        "src/demo_project/agent.py",
        "src/demo_project/data.py",
        "src/demo_project/interfaces/violetear_app.py",
    ],
    "litellm-gateway": [
        "src/demo_project/serving.py",
        "src/demo_project/data.py",
    ],
}


@pytest.mark.preset
@pytest.mark.parametrize(("preset", "expected_files"), PRESETS.items())
def test_ai_preset_vertical_slice(
    copie, uv: str, preset: str, expected_files: list[str]
) -> None:
    """Each affected preset installs, imports and passes its offline tests."""
    result = copie.copy(
        extra_answers=answers(
            preset=preset,
            use_docs=False,
            use_codeql=False,
            use_docker=False,
        )
    )
    assert result.exception is None, result.exception
    project = result.project_dir

    for relative in expected_files:
        assert (project / Path(relative)).is_file(), relative

    assert_ok(run([uv, "run", "ruff", "check", "."], project), "ruff check")
    assert_ok(
        run([uv, "run", "ruff", "format", "--check", "."], project),
        "ruff format",
    )
    assert_ok(run([uv, "run", "deptry", "src"], project), "deptry")
    assert_ok(run([uv, "run", "poe", "cov"], project), "coverage")


@pytest.mark.preset
@pytest.mark.parametrize("framework", ["fastapi", "flask"])
def test_data_and_auth_vertical_slice(copie, uv: str, framework: str) -> None:
    """The SQLModel, Alembic and API-key layers pass the generated gate."""
    result = copie.copy(
        extra_answers=answers(
            preset="custom",
            workload="api",
            framework=framework,
            sql_store="sqlite",
            sql_abstraction="sqlmodel",
            auth="api-key",
            use_docs=False,
            use_codeql=False,
            use_docker=False,
        )
    )
    assert result.exception is None, result.exception
    project = result.project_dir

    assert_ok(run([uv, "run", "ruff", "check", "."], project), "ruff check")
    assert_ok(
        run([uv, "run", "ruff", "format", "--check", "."], project),
        "ruff format",
    )
    assert_ok(run([uv, "run", "deptry", "src"], project), "deptry")
    assert_ok(run([uv, "run", "poe", "cov"], project), "coverage")


@pytest.mark.preset
def test_interface_auth_vertical_slice(copie, uv: str) -> None:
    """Authentication protects an AI interface before its workload executes."""
    result = copie.copy(
        extra_answers=answers(
            preset="langgraph-anthropic-api",
            auth="api-key",
            use_docs=False,
            use_codeql=False,
            use_docker=False,
        )
    )
    assert result.exception is None, result.exception
    project = result.project_dir

    assert_ok(run([uv, "run", "ruff", "check", "."], project), "ruff check")
    assert_ok(
        run([uv, "run", "ruff", "format", "--check", "."], project),
        "ruff format",
    )
    assert_ok(run([uv, "run", "deptry", "src"], project), "deptry")
    assert_ok(run([uv, "run", "poe", "cov"], project), "coverage")


@pytest.mark.preset
def test_ml_hybrid_vertical_slice(copie, uv: str) -> None:
    """A lightweight hybrid stack validates training, serving and workspace wiring."""
    result = copie.copy(
        extra_answers=answers(
            preset="custom",
            workload="hybrid",
            ai_capabilities="training",
            framework="scikit-learn",
            serving="bentoml",
            training_extensions=["optuna"],
            mlops_tools=["polars", "pandera"],
            quality_tools=["opentelemetry"],
            deploy_target="none",
            use_docs=False,
            use_codeql=False,
            use_docker=False,
        )
    )
    assert result.exception is None, result.exception
    project = result.project_dir

    assert (project / "packages/training/pyproject.toml").is_file()
    assert (project / "packages/service/pyproject.toml").is_file()
    assert_ok(run([uv, "run", "ruff", "check", "."], project), "ruff check")
    assert_ok(
        run([uv, "run", "ruff", "format", "--check", "."], project),
        "ruff format",
    )
    assert_ok(run([uv, "run", "deptry", "src"], project), "deptry")
    assert_ok(run([uv, "run", "poe", "cov"], project), "coverage")


def test_hf_finetuning_preset_renders_without_downloading_models(
    tmp_path: Path,
) -> None:
    """The heavyweight reference preset has its complete workspace and dependency set."""
    template = tmp_path / "template"
    copytree(
        Path.cwd(),
        template,
        ignore=ignore_patterns(".git", ".venv", ".pytest_cache", "__pycache__"),
    )
    project = tmp_path / "hf-project"
    run_copy(
        str(template),
        project,
        data=answers(
            preset="hf-finetuning",
            use_docs=False,
            use_codeql=False,
            use_docker=False,
        ),
        defaults=True,
        unsafe=True,
        skip_tasks=True,
    )

    pyproject = (project / "pyproject.toml").read_text()
    for dependency in (
        "transformers>=",
        "torch>=",
        "datasets>=",
        "accelerate>=",
        "peft>=",
        "trl>=",
        "bentoml>=",
        "mlflow>=",
    ):
        assert dependency in pyproject
    assert (project / "src/demo_project/training.py").is_file()
    assert (project / "src/demo_project/serving.py").is_file()
    assert (project / "packages/training/pyproject.toml").is_file()
    assert (project / "packages/service/pyproject.toml").is_file()


@pytest.mark.preset
@pytest.mark.parametrize(
    ("deploy_target", "workload", "framework", "serving", "entrypoint"),
    [
        ("modal", "api", "fastapi", "none", "deploy/modal_app.py"),
        ("runpod", "inference", "none", "litellm", "handler.py"),
        (
            "bentocloud",
            "inference",
            "none",
            "bentoml",
            "deploy/bentoml_service.py",
        ),
    ],
)
def test_python_deployment_adapter_vertical_slice(
    copie,
    uv: str,
    deploy_target: str,
    workload: str,
    framework: str,
    serving: str,
    entrypoint: str,
) -> None:
    """Python-native deployment SDKs install, import and pass the generated gate."""
    result = copie.copy(
        extra_answers=answers(
            preset="custom",
            workload=workload,
            framework=framework,
            serving=serving,
            deploy_target=deploy_target,
            use_docs=False,
            use_codeql=False,
            use_docker=False,
        )
    )
    assert result.exception is None, result.exception
    project = result.project_dir
    assert (project / entrypoint).is_file()

    assert_ok(run([uv, "run", "ruff", "check", "."], project), "ruff check")
    assert_ok(
        run([uv, "run", "ruff", "format", "--check", "."], project),
        "ruff format",
    )
    assert_ok(run([uv, "run", "deptry", "src"], project), "deptry")
    assert_ok(run([uv, "run", "poe", "cov"], project), "coverage")
