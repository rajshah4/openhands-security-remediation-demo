# Change: Remediate Command Injection in Report Endpoint

## Why

The `/reports` endpoint contains a critical command injection vulnerability (CWE-78) where user-controlled input reaches `subprocess.run` with `shell=True`. This vulnerability allows attackers to execute arbitrary shell commands by injecting metacharacters into the `name` query parameter, potentially leading to data exfiltration, privilege escalation, or system compromise.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-167
- Trigger: Jira webhook `jira:issue_created` with label `security-remediation`
- Automation: OpenHands Enterprise SAST Remediation Demo
- Semgrep rule: `flask-request-to-subprocess-shell`
- CWE: CWE-78 (OS Command Injection)
- Severity: CRITICAL

## Assumptions

- The allowlist of valid report names (`inventory`, `adoptions`) must be preserved exactly as defined in the `REPORTS` dictionary.
- The endpoint is intended for retrieving predefined text reports only, not for executing arbitrary commands.
- The existing test suite expectations must continue to pass after remediation.
- The fix must eliminate the Semgrep finding completely (reduce count from 1 to 0).

## Non-Goals

- Replacing the subprocess approach with pure Python file reading (while preferable, this change focuses on the minimal security fix).
- Adding authentication or authorization to the endpoint.
- Adding rate limiting or other defense-in-depth measures.
- Modifying the report file format or storage location.

## What Changes

- Replace weak `startswith()` allowlist validation with exact dictionary key matching using `REPORTS.get()`.
- Convert shell string command to argument array format to prevent shell interpretation.
- Remove `shell=True` parameter from `subprocess.run()` to disable shell metacharacter processing.
- Add regression tests for additional shell metacharacter payloads.
- Add test for the `adoptions` report endpoint (currently missing coverage).

## Impact

- **App behavior**: Allowlisted report retrieval (`inventory`, `adoptions`) continues to work exactly as before. Shell metacharacter payloads are rejected with 404 responses.
- **Tests**: Existing security regression test continues to pass. New tests added for comprehensive shell metacharacter coverage and the adoptions endpoint.
- **Humans**: Security team can verify the Semgrep finding count drops from 1 to 0. Engineering must review and approve the PR before merge.

## Human Gates

- Scope approval: Confirmed - remediation matches acceptance criteria in KAN-167.
- Review approval: Required - draft PR must be reviewed by engineering and security teams.
- Merge approval: Required - human merge decision after review approval.
- Deployment approval: Required - human controls deployment to production environments.
