"""Linux integration tests for the agent, MCP, RAG and interface presets."""

from pathlib import Path

import pytest
from conftest import answers, assert_ok, run

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
    assert_ok(run([uv, "run", "pytest", "-q"], project), "pytest")


@pytest.mark.preset
def test_data_and_auth_vertical_slice(copie, uv: str) -> None:
    """The SQLModel, Alembic and API-key layers pass the generated gate."""
    result = copie.copy(
        extra_answers=answers(
            preset="custom",
            workload="api",
            framework="fastapi",
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
    assert_ok(run([uv, "run", "pytest", "-q"], project), "pytest")
