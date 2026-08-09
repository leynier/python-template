# Support model

Every catalog component has a support tier and a Python compatibility range.
The tier describes what this repository can verify; it is not a judgment about
the upstream project's general quality.

## Stable

The integration can be exercised locally or offline without a paid account.
Generated dependencies, imports, configuration, and representative behavior are
covered by the test suite.

## Platform

The integration depends on a hosted API or cloud account. The repository tests
the generated client boundary, configuration, parsability, and local contract.
Users still need to supply credentials, accept provider costs, and perform a
real deployment verification.

## Experimental

The upstream API or the integration surface is evolving. It remains useful, but
may support fewer combinations and carries a narrower compatibility promise.

## Inclusion criteria

A component should add a distinct architectural role, have active maintenance,
support the template's Python baseline, and permit a meaningful automated test.
New proposals should explain which layer they add and how a generated project
can validate the integration without embedding credentials.
