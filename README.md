# OpenHands Enterprise SAST Remediation Demo

A focused, Jira-triggered demonstration of OpenHands Enterprise turning a confirmed static-analysis finding into a tested, human-reviewable draft pull request.

This repository was initially created by an OpenHands AI agent on behalf of Rajiv Shah.

## Why this scenario

The demo uses one convincing path rather than shallowly covering every security category: a Semgrep command-injection finding in a small Flask service. The workflow shows the reusable pattern behind SAST, SCA, DAST, and license remediation:

```text
Jira Task
  -> Rajistics OpenHands Enterprise event automation
  -> deterministic scanner reproduces finding
  -> repository-local remediation skill
  -> minimal code fix and regression test
  -> scanner rerun proves finding is gone
  -> draft GitHub pull request plus Jira evidence
  -> human review and merge decision
```

OpenHands is the remediation and orchestration layer. The scanner remains the source of truth for detection.

## Branches

- `main`: clean reference implementation with zero findings.
- `demo/command-injection`: synthetic vulnerable implementation with exactly one Semgrep finding.
- `fix/<jira-key>-command-injection`: agent-created remediation branch targeting the vulnerable demo branch.

Intentional vulnerabilities never belong on `main`.

## Repository assets

- `security/rules/python-command-injection.yml`: focused Semgrep taint rule for CWE-78.
- `scripts/run_sast.py`: deterministic scan and finding normalization.
- `.agents/skills/sast-remediation/`: the repository-owned remediation workflow and acceptance contract.
- `automations/jira/sast-remediation/`: Rajistics prompt-preset event automation.
- `scripts/register_automation.py`: validates the production payload before idempotent registration.
- `scripts/switch_demo_mode.py`: safely switches the shared Jira webhook between the existing SDLC demo and this security demo.
- `scripts/create_demo_jira_ticket.py`: creates a narrowly scoped KAN Task using Jira OAuth credentials.
- `scripts/comment_jira.py`: posts remediation evidence back to Jira without exposing credentials.

## Local validation

Install the pinned environment and verify the clean branch:

```bash
uv sync --all-groups
uv run pytest -q
uv run ruff check .
uv run python scripts/run_sast.py --expect 0
```

On `demo/command-injection`, the last command changes to:

```bash
uv run python scripts/run_sast.py --expect 1
```

## Rajistics automation

The automation listens for `jira:issue_created` from the existing `jira-direct` webhook and requires all of:

- project `KAN`
- issue type `Task`
- label `security-remediation`

It clones `demo/command-injection`, reproduces the finding, follows the repository skill, opens a draft PR, and comments on the originating Jira issue.

The existing `SDLC_1 - Jira to PR` automation has a broad Jira trigger. Use the mode switch so one Jira ticket starts only one demo:

```bash
# Preview changes
uv run python scripts/switch_demo_mode.py security

# Activate security demo mode
uv run python scripts/switch_demo_mode.py security --apply

# Restore the normal SDLC demo afterward
uv run python scripts/switch_demo_mode.py sdlc --apply
```

The scripts expect credentials from the environment and never print their values.

## Create the demo ticket

```bash
# Inspect the Jira request first
uv run python scripts/create_demo_jira_ticket.py

# Create the ticket
uv run python scripts/create_demo_jira_ticket.py --apply
```

## Extend the pattern

Keep the same automation and evidence contract, then replace or add the deterministic adapter:

- SCA: Trivy, Snyk, Dependabot, or another dependency report.
- DAST: ZAP or Burp output from an explicitly authorized test environment.
- License: SBOM/license inventory plus a human-approved policy.

Each adapter should normalize evidence, invoke an agent only for actionable findings, rerun the originating tool, and preserve human approval for merge or policy exceptions.

## Safety

The vulnerable branch and test payloads are synthetic. Do not deploy the vulnerable application or run active security tests against external targets. The automation does not approve or merge pull requests.
