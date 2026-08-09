# Agent skills

The repository follows the open Agent Skills layout under `skills/`, so it is
discoverable by the `skills` CLI and compatible coding agents.

## Inspect and install

```bash
npx skills add leynier/python-template --list
npx skills add leynier/python-template --skill compose-python-stack
```

Repository skills:

- `compose-python-stack` translates a product goal into compatible layers and
  generates the project.
- `maintain-python-template` keeps catalog, Copier questions, templates,
  compiler outputs, and tests synchronized.
- `validate-python-stack` selects the appropriate repository or generated
  project gates and reports unavailable checks honestly.

## Skills inside generated projects

Every generated project contains `project-workflow`. Projects with an AI or ML
capability add `operate-ai-stack`; projects with a deploy target add
`deploy-python-project`. A simple CLI therefore receives no cloud or AI
instructions it cannot use.

From a generated project, confirm discovery with:

```bash
npx skills add . --list
```

Each skill includes `agents/openai.yaml` metadata and is validated with the
skill-creator validator in this repository's release process.
