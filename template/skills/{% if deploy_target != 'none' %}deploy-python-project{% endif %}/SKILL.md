---
name: deploy-python-project
description: Validate and deploy this generated Python project using its selected target, portable Docker base, and optional Pulumi or Terraform configuration. Use for deployment preparation, local container checks, cloud previews, release rollout, health verification, or deployment troubleshooting.
---

# Deploy Python Project

Read `.copier-answers.yml` and `deploy/README.md` first; they identify the target, commands, environment variables, and any generated IaC.

## Workflow

1. Run the full project quality gates from `project-workflow`.
2. Build the generated Dockerfile locally. Start the image with explicit environment variables and verify its documented health route.
3. Validate target configuration as structured JSON, TOML, YAML, Python, or HCL. Never infer that a successful parse proves cloud readiness.
4. For Pulumi, run a preview before update. For Terraform, run format, init without changing remote state where possible, validate, and plan before apply.
5. Confirm account, region, project, service name, expected cost boundary, secrets source, and rollback strategy before creating or changing remote resources.
6. Deploy with the command documented in `deploy/README.md`, then verify the remote health route and one representative request.
7. Report the deployed revision, endpoint, verification evidence, and any manual DNS or secret-management step.

## Safety

- Do not deploy, apply IaC, delete resources, or expose a public endpoint without explicit authorization.
- Do not embed provider credentials in images, configuration, logs, or Git.
- Keep the Docker path usable even when the selected managed platform provides a native adapter.
