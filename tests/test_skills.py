"""Agent skill discovery and conditional generation tests."""

from pathlib import Path

import yaml
from conftest import answers

REPOSITORY_SKILLS = {
    "compose-python-stack",
    "maintain-python-template",
    "validate-python-stack",
}


def _assert_skill(skill_dir: Path, expected_name: str) -> None:
    skill_md = skill_dir / "SKILL.md"
    metadata = skill_dir / "agents" / "openai.yaml"
    assert skill_md.is_file()
    assert metadata.is_file()

    contents = skill_md.read_text()
    _, frontmatter, _ = contents.split("---", maxsplit=2)
    parsed = yaml.safe_load(frontmatter)
    assert parsed["name"] == expected_name
    assert parsed["description"]

    agent = yaml.safe_load(metadata.read_text())
    assert agent["interface"]["display_name"]
    assert f"${expected_name}" in agent["interface"]["default_prompt"]


def test_repository_skills_follow_the_agent_skills_layout() -> None:
    skills_root = Path(__file__).parents[1] / "skills"
    assert {path.name for path in skills_root.iterdir()} == REPOSITORY_SKILLS
    for name in REPOSITORY_SKILLS:
        _assert_skill(skills_root / name, name)


def test_simple_project_only_gets_the_common_workflow_skill(copie) -> None:
    project = copie.copy(extra_answers=answers(preset="typer-cli")).project_dir
    skills_root = project / "skills"

    assert {path.name for path in skills_root.iterdir()} == {"project-workflow"}
    _assert_skill(skills_root / "project-workflow", "project-workflow")


def test_ai_project_gets_the_ai_skill_without_deploy_skill(copie) -> None:
    project = copie.copy(
        extra_answers=answers(preset="pydantic-ai-openai", deploy_target="none")
    ).project_dir
    skills_root = project / "skills"

    assert {path.name for path in skills_root.iterdir()} == {
        "operate-ai-stack",
        "project-workflow",
    }
    _assert_skill(skills_root / "operate-ai-stack", "operate-ai-stack")


def test_deployed_simple_api_gets_deploy_skill_without_ai_skill(copie) -> None:
    project = copie.copy(
        extra_answers=answers(preset="fastapi-api", deploy_target="render")
    ).project_dir
    skills_root = project / "skills"

    assert {path.name for path in skills_root.iterdir()} == {
        "deploy-python-project",
        "project-workflow",
    }
    _assert_skill(skills_root / "deploy-python-project", "deploy-python-project")
