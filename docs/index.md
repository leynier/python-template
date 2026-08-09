# Build the Python stack you actually need

Python Template generates production-ready Python and AI projects from
compatible layers. Start from one of 12 editable recipes or compose the
workload, framework, providers, data roles, interface, operations, and deploy
target yourself.

```bash
uvx copier copy --trust gh:leynier/python-template my-project
cd my-project
uv run pytest
```

## Small projects stay small

The Python Library, Typer CLI, and FastAPI API presets do not pull in an AI
framework. They receive the same tested packaging, CI, security, documentation,
and update path as larger stacks.

## AI and ML are layers, not a separate template

Choose an MCP server, agent, RAG app, inference service, training project, or
hybrid workspace. Model and embedding providers remain independent. SQL,
document, vector, graph, and cache roles each select their own engine. The
result is one coherent project rather than snippets from unrelated starters.

## Start here

- [Generate your first project](getting-started.md)
- [Choose between presets and custom layers](guides/choose-a-stack.md)
- [Understand the layer model](concepts/layers.md)
- [Install the agent skills](guides/agent-skills.md)
- [Review deployment and IaC targets](guides/deployment.md)
- [Browse all components](reference/components.md)
