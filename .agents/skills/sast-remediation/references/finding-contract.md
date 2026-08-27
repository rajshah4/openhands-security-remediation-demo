# Finding contract

The demo starts only when all of these conditions are true:

- Jira project: `KAN`
- Jira issue type: `Task`
- Jira label: `security-remediation`
- repository: `rajshah4/openhands-security-remediation-demo`
- source branch: `demo/command-injection`
- scanner: Semgrep
- rule: `flask-request-to-subprocess-shell`
- category: SAST
- weakness: CWE-78 command injection
- expected initial count: one
- expected final count: zero

The normalized report is written to `security/findings/generated-semgrep.json`. Its fingerprint is supporting evidence, not an authorization token.

A valid remediation preserves report retrieval for the allowlisted `inventory` and `adoptions` names, rejects any unknown name, avoids `shell=True`, passes tests, and produces a clean Semgrep result.
