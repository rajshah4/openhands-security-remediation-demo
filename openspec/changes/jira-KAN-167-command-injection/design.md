# Design

## Context

The vulnerable `read_report()` function in `src/security_demo/app.py` (lines 15-27) uses string interpolation to construct a shell command and executes it with `subprocess.run(..., shell=True)`. The current allowlist validation uses `startswith()` which allows bypass attacks like `inventory; malicious_command; #`.

The Semgrep rule `flask-request-to-subprocess-shell` flags this pattern as CWE-78 (OS Command Injection). The `main` branch contains a secure reference implementation that eliminates the vulnerability.

## Decision

**Replace shell string execution with argument array execution:**

1. Use `REPORTS.get(report_name)` for exact dictionary key matching instead of `startswith()` validation.
2. Pass arguments as a list `["cat", str(REPORT_DIRECTORY / filename)]` instead of a shell string.
3. Remove `shell=True` parameter (defaults to `shell=False`).
4. Use `pathlib.Path` for safe path construction.

This approach:
- Prevents shell metacharacter interpretation completely.
- Maintains exact allowlist semantics (only `inventory` and `adoptions` are accepted).
- Requires minimal code changes (7 lines modified).
- Matches the secure pattern already validated on the `main` branch.

**Alternative considered but not implemented:** Replace subprocess with pure Python `filepath.read_text()`. While this would be even safer and more efficient, the acceptance criteria specify preserving the allowlisted report retrieval mechanism, and the minimal fix approach focuses on eliminating the vulnerability without changing the execution model.

## Risks

- **Risk**: The fix changes subprocess invocation from shell to non-shell mode, which could theoretically affect edge cases with special filename characters.
  - **Mitigation**: The allowlist uses simple alphanumeric names (`inventory`, `adoptions`), and the `.txt` extension is hardcoded. No special characters are present in valid inputs.

- **Risk**: Tests might have false positives if they only check HTTP status codes without validating that commands are actually blocked.
  - **Mitigation**: The existing test suite includes a focused security regression test (`test_report_endpoint_rejects_command_injection_payload`) that will continue to pass. Additional tests will be added for comprehensive metacharacter coverage.

- **Risk**: The Semgrep rule might not detect the fix and continue reporting a finding.
  - **Mitigation**: The `main` branch reference implementation with identical fix approach shows zero Semgrep findings. The validation plan includes running `scripts/run_sast.py --expect 0` to confirm.

## Validation Plan

1. **Unit tests**: Run `uv run pytest -q` to verify all tests pass, including new security regression tests.
2. **Linting**: Run `uv run ruff check .` to ensure code quality standards are met.
3. **SAST verification**: Run `uv run python scripts/run_sast.py --expect 0` to confirm the Semgrep finding count drops from 1 to 0.
4. **Manual verification**: The PR must include evidence that allowlisted reports (`inventory`, `adoptions`) still return successfully while shell metacharacter payloads are rejected.

## Evidence Checklist

- [x] **Stop 1 - Ticket**: Jira KAN-167 specifies command injection in report endpoint with Semgrep rule `flask-request-to-subprocess-shell`.
- [x] **Stop 2 - Wiki/Docs**: `README.md` and `docs/demo-runbook.md` confirm this is a SAST remediation demo. The `main` branch contains the secure reference implementation.
- [ ] **Stop 3 - Logs**: No log evidence required for this security fix (vulnerability is in code structure, not runtime behavior).
- [x] **Stop 4 - Repo/Files**: Vulnerable code identified in `src/security_demo/app.py` lines 15-27. Secure reference implementation exists on `main` branch at the same location.
- [ ] **Stop 5 - Tests/PR**: Tests to be run after implementation. Draft PR to be created with full validation results.
