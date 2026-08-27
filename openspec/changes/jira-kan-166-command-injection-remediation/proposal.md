# Change: Remediate Command Injection in Report Endpoint

## Why

A command injection vulnerability (CWE-78) exists in the `/reports` endpoint where user-controlled input flows into a shell command executed via `subprocess.run()` with `shell=True`. An attacker can inject arbitrary shell commands by appending metacharacters to allowlisted report names (e.g., `inventory;whoami`). This violates security best practices and was flagged by Semgrep rule `flask-request-to-subprocess-shell`. The remediation preserves allowlisted report retrieval while eliminating the command injection vector.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-166
- Trigger: Jira webhook issue_created event
- Automation: Replicated Jira SAST Remediation factory

## Assumptions

- The report endpoint must continue to serve `inventory` and `adoptions` reports
- Shell command execution is not required; Python file I/O is acceptable
- Existing tests define the security contract: allowlisted reports pass, injection payloads are rejected
- The fix must reduce the Semgrep finding count from 1 to 0

## Non-Goals

- Adding new report types or dynamic report generation
- Changing the HTTP API contract (query parameter name, response format)
- Adding authentication or authorization (out of scope for this security fix)
- Modifying report file formats or storage location

## What Changes

- Replace `subprocess.run(shell=True)` with direct Python file reading
- Strengthen input validation from prefix check (`startswith()`) to exact match (`in REPORTS`)
- Eliminate shell metacharacter processing entirely

## Impact

- App behavior: Identical for valid requests; injection attempts now properly rejected
- Tests: Existing security test `test_report_endpoint_rejects_command_injection_payload` now passes
- Humans: Requires code review approval and merge approval; no deployment changes needed

## Human Gates

- Scope approval: Pre-approved via Jira issue KAN-166
- Review approval: Required before merge
- Merge approval: Required (OpenHands creates draft PR, does not merge)
- Deployment approval: Standard deployment process applies after merge
