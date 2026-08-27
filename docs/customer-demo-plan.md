# Customer demo plan: security remediation with OpenHands Enterprise

## Customer request

The customer wants to understand automated SAST and DAST, open-source vulnerability and license remediation, the role OpenHands plays, and the pricing model.

## Positioning

OpenHands is the remediation and orchestration layer, not a replacement for the customer's scanner portfolio. Existing SAST, SCA, DAST, SBOM, and license-policy tools continue to detect and prioritize findings. OpenHands consumes their evidence, changes code or dependencies, runs the original validation, opens a pull request, and preserves human approval.

This separation is important: detection remains deterministic and governed by the security tool; the agent handles the context-heavy engineering work between finding and reviewed fix.

## Demonstrate one complete workflow

Use the tested Jira-triggered SAST path in this repository:

1. Start from Jira and create a KAN Task labeled `security-remediation`.
2. Show the Rajistics event automation and its narrow project, issue-type, and label filter.
3. Open the spawned conversation to show the audit trail: repository instructions, finding reproduction, source edit, regression test, scanner rerun, commit, and PR creation.
4. Open the draft PR and highlight:
   - Semgrep rule and CWE-78
   - finding fingerprint
   - one finding before and zero after
   - minimal code diff
   - regression coverage
   - exact commands and results
   - OpenHands conversation link
   - human merge gate
5. Open Jira again and show the PR, conversation, validation, and independent CI links posted back to the ticket.
6. Show the two successful GitHub Actions checks as independent verification.

## What this proves

- Event-driven operation from a system the customer already uses.
- Deterministic confirmation before the agent changes code.
- Repository-specific skills and guardrails checked into source control.
- Minimal remediation with functional and security regression tests.
- Closed-loop evidence in Jira, OpenHands, GitHub, Semgrep, and CI.
- Enterprise governance: isolated execution, auditable actions, scoped integrations, and a human approval boundary.

## Map to the broader request

### SAST

Use scanner findings from Semgrep, CodeQL, Snyk Code, Checkmarx, Fortify, or another product as normalized input. The demo already implements this pattern.

### Open-source vulnerability remediation

Add an SCA adapter for Dependabot, Snyk Open Source, Trivy, Grype, or the customer's chosen tool. OpenHands should update manifests and lockfiles, run compatibility tests, rerun the originating scanner, and open separate PRs for reviewable changes.

### License remediation

Ingest SBOM and license-policy findings. OpenHands can replace or upgrade dependencies and produce impact evidence, but legal policy and exceptions remain human-owned. Do not let an agent decide that a license is acceptable.

### DAST

Run ZAP, Burp, or the customer's scanner only against an explicitly authorized test environment. Pass a bounded finding to OpenHands, fix the application code, run tests, and rerun the exact authorized probe. Keep target allowlists and approval outside agent control.

## What to build next

Do not rebuild the existing vulnerability-fixer web UI yet. Jira, the OpenHands conversation, the draft PR, and scanner/CI evidence already provide a stronger enterprise story.

Prioritize these increments:

1. SCA adapter and dependency-upgrade scenario using the same finding contract.
2. Scanner-ingestion schema for Semgrep SARIF/JSON, CodeQL SARIF, Snyk JSON, and Trivy JSON.
3. Policy layer for severity, repository, ownership, and remediation SLA.
4. DAST adapter with explicit environment allowlist and pre-run approval.
5. License workflow that routes policy decisions and exceptions to legal/security owners.
6. Metrics for attempted fixes, clean rescans, accepted PRs, time-to-remediation, and cost per accepted fix.

Build a dedicated portal only if customers need cross-scanner queue management, portfolio analytics, or approval workflows that Jira and the scanner console cannot provide.

## Pricing discussion

Use the current official language: OpenHands Enterprise is custom-priced and offered as SaaS or self-hosted, with private VPC and BYOK options. Do not quote an unverified unit price.

Frame total adoption cost as:

- OpenHands Enterprise commercial agreement.
- Customer infrastructure for self-hosted execution.
- LLM consumption, either BYOK or contracted provider routing.
- Existing or new scanner licenses.
- Optional implementation and support services.

Collect these inputs for a commercial follow-up:

- users and teams
- repositories and primary languages
- findings per month and expected remediation volume
- required concurrency and turnaround objective
- SaaS versus self-hosted deployment
- model provider and data-residency requirements
- SSO, RBAC, audit, and support requirements
- scanner, Jira, Git, and CI integrations

## Official references

- [OpenHands vulnerability remediation](https://docs.openhands.dev/openhands/usage/use-cases/vulnerability-remediation)
- [OpenHands vulnerability-remediation plugin](https://github.com/OpenHands/extensions/tree/main/plugins/vulnerability-remediation)
- [OpenHands vulnerability-fixer example](https://github.com/OpenHands/vulnerability-fixer)
- [OpenHands Enterprise](https://www.openhands.dev/enterprise)
- [OpenHands pricing](https://www.openhands.dev/pricing)
