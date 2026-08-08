# Security Policy

## Scope

This repository is a project template. It ships GitHub Actions workflows,
dependency declarations and configuration that are copied into other people's
projects, so a problem here propagates to everything generated from it.

Reports about the template itself are in scope: a workflow that leaks
credentials, an over-permissioned token, a dependency pinned to something
malicious, or a generated default that is unsafe.

## Supported versions

The latest tag receives fixes. Older tags do not.

## Reporting a vulnerability

Please **do not** open a public issue.

Report privately through
[GitHub Security Advisories](https://github.com/leynier/python-template/security/advisories/new),
or by email to <leynier41@gmail.com>.

Please include:

- What the problem is and what an attacker could do with it.
- Which file or generated output is affected.
- Steps to reproduce, ideally the `copier` answers that produce the bad output.

You can expect an initial response within 7 days.

## Security posture of this repository

- GitHub Actions are pinned to release tags, and
  [zizmor](https://github.com/zizmorcore/zizmor) audits every workflow on
  change. The pinning policy is declared in `zizmor.yml`.
- Workflows declare least-privilege `permissions:`.
- Dependabot has a cooldown before adopting newly published releases.
- CodeQL and OpenSSF Scorecard run against this repository.

Generated projects get the same treatment, plus PyPI Trusted Publishing with
Sigstore attestations instead of long-lived API tokens.
