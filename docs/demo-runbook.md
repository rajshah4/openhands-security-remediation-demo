# Demo runbook

## Current deployment

- OpenHands Enterprise: `https://app.replicated.rajistics.com`
- security automation: `Security Demo - Jira SAST Remediation`
- automation ID: `c408b0c4-5523-4500-9602-91bc915d7034`
- template version: `1.0.1`
- normal state: security automation disabled; `SDLC_1 - Jira to PR` enabled
- Jira project: `KAN`
- trigger label: `security-remediation`
- source branch: `demo/command-injection`

## Preflight

From the repository `main` branch:

```bash
uv sync --all-groups
uv run pytest -q
uv run ruff check .
uv run python scripts/run_sast.py --expect 0
```

Confirm the vulnerable branch contract without deploying it:

```bash
git fetch origin
git show origin/demo/command-injection:src/security_demo/app.py | grep 'shell=True'
```

Confirm required Rajistics secret names exist; never print their values:

- `GITHUB_TOKEN`
- `JIRA_API_BASE_URL`
- `JIRA_API_TOKEN`
- `JIRA_SITE_URL`

## Activate security demo mode

The existing SDLC Jira automation has a broad trigger. Switch modes so one Jira ticket starts only one conversation:

```bash
uv run python scripts/switch_demo_mode.py security
uv run python scripts/switch_demo_mode.py security --apply
```

Expected state:

- `SDLC_1 - Jira to PR`: disabled
- `Security Demo - Jira SAST Remediation`: enabled

## Trigger from Jira

Preview the issue payload, then create a unique Jira Task:

```bash
uv run python scripts/create_demo_jira_ticket.py
uv run python scripts/create_demo_jira_ticket.py --apply
```

The created Task includes project `KAN`, type `Task`, and label `security-remediation`.

## Observe

Watch these artifacts:

1. Jira issue: the starting requirement and final evidence comments.
2. Rajistics Automations: a run under `Security Demo - Jira SAST Remediation`.
3. OpenHands conversation: scanner, code edit, tests, rescan, Git actions, and final summary.
4. Draft GitHub PR targeting `demo/command-injection`.
5. GitHub Actions: `Validate` push and pull-request checks.

Expected remediation evidence:

- initial Semgrep findings: one
- final Semgrep findings: zero
- rule: `flask-request-to-subprocess-shell`
- CWE: CWE-78
- tests and Ruff pass
- PR remains draft and unmerged
- Jira and PR contain the exact Rajistics conversation URL
- CI checks pass independently

## Restore normal mode

Always restore the original SDLC demo after the security run:

```bash
uv run python scripts/switch_demo_mode.py sdlc --apply
```

Expected state:

- `SDLC_1 - Jira to PR`: enabled
- `Security Demo - Jira SAST Remediation`: disabled

## Repeatability

The automation always clones the immutable `demo/command-injection` source branch and creates a unique Jira-keyed fix branch. No reset of `main` or the vulnerable branch is required. Close old draft PRs only when you no longer need their evidence; never merge a remediation PR into the demo source branch.

## Troubleshooting

- No run: verify mode, label, project, Task type, and `jira-direct` webhook delivery.
- Two runs: restore supported-API mode switching; the broad SDLC automation was probably left enabled.
- Scanner mismatch: stop without editing and confirm the source branch and pinned Semgrep version.
- Jira comment fails initially: reference `JIRA_API_BASE_URL` and `JIRA_API_TOKEN` explicitly on the `comment_jira.py` command so Enterprise injects them on demand.
- PR contains `${AUTOMATION_SESSION_URL}`: replace it with the exact Rajistics conversation URL through the GitHub REST API, then update the automation prompt before the next run.
- CI fails: treat the remediation as incomplete even if the automation run reports completed.
