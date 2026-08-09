# Composable layers

The generator treats architecture as a set of roles with compatibility rules.
This avoids the combinatorial maintenance cost of keeping a separate template
for every framework/provider/database/deploy permutation.

| Layer | Responsibility | Cardinality |
| --- | --- | --- |
| Workload | Primary shape and entry point | exactly one |
| Framework | Runtime or AI orchestration framework | zero or one |
| Interface | API, web, notebook, or terminal front end | zero or more |
| Model provider | Generative model access | zero or one |
| Embedding provider | Embedding model access | zero or one, independent |
| Data roles | SQL, document, vector, graph, cache | zero or one per role |
| SQL abstraction | SQLModel or SQLAlchemy | zero or one for eligible SQL stores |
| Auth | Request authentication | zero or one |
| Training extensions | Data, acceleration, tuning, optimization | zero or more |
| Serving | Model or gateway runtime | zero or one |
| MLOps and quality | Orchestration, evaluation, telemetry | zero or more |
| Deploy | Runtime destination | zero or one |
| IaC | Cloud resource definition | none, Pulumi, or Terraform |

## Compatibility is resolved before rendering

Copier validators reject combinations that cannot form a meaningful project.
Examples include using an agent framework for a plain library preset, adding a
SQL abstraction without a compatible SQL engine, or selecting IaC for a target
without a generated infrastructure contract.

Python compatibility is also visible in the catalog. The general baseline is
Python 3.12 or newer; components whose upstream support is narrower constrain
the available versions.

## Data roles stay explicit

A single engine can fill several roles when it supports them. Beaver, for
example, can cover document, vector, graph, and cache in a local-first stack.
That does not collapse the roles: each answer remains explicit, so a project can
later move only vector retrieval to a hosted engine without changing its graph
store.

## Portable deployment remains the base

Selecting a deploy target creates its native configuration and keeps a Docker
path. Cloud-specific Pulumi or Terraform is additive. Application code does not
become dependent on the IaC choice.
