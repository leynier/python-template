# Deployment and IaC

Choose one runtime destination. A deployed project retains a portable Docker
base and adds the selected platform's configuration.

## Targets

| Group | Targets |
| --- | --- |
| Portable and PaaS | Docker/Compose, Render, Fly.io, Vercel, Railway |
| AI platforms | Hugging Face Spaces, Modal, RunPod, BentoCloud |
| AWS | ECS, SageMaker |
| Google Cloud | Cloud Run, Vertex AI |
| Azure | Container Apps, Azure ML |

Modal, RunPod, and BentoCloud receive native Python adapters. Managed inference
targets use consistent health and prediction routes so container and platform
checks exercise the same application contract.

## Infrastructure as code

Pulumi and Terraform are available for AWS ECS, SageMaker, Cloud Run, Vertex
AI, Azure Container Apps, and Azure ML. Select `none` when the platform's native
configuration or an external infrastructure repository owns those resources.

Generated IaC is a starting resource graph, not permission to apply it. Review
account, region, naming, cost, secrets, state backend, and rollback before a
preview or plan becomes an update or apply.

## Verification sequence

1. Run the generated quality gates.
2. Build the Docker image and verify its health route locally.
3. Parse or validate the platform and IaC configuration.
4. Preview or plan cloud changes.
5. Deploy only with explicit authorization.
6. Verify the remote health route and one representative request.
