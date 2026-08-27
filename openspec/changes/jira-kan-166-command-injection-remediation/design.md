# Design

## Context

The security demo Flask application provides a `/reports` endpoint that serves two allowlisted text reports: `inventory` and `adoptions`. The current implementation uses `subprocess.run()` with `shell=True` to execute `cat` commands, creating a command injection vulnerability flagged by Semgrep. Input validation using `startswith()` is insufficient because it allows appending shell metacharacters to allowlisted prefixes.

## Decision

1. **Remove subprocess entirely**: Replace `subprocess.run()` with `pathlib.Path.read_text()` for direct file reading
2. **Strengthen validation**: Change from `startswith()` prefix check to exact `in` membership test against `REPORTS` keys
3. **Use pathlib**: Leverage `pathlib.Path` for safe path construction (already imported in the file)

### Rationale

- **Defense in depth**: Eliminating shell invocation removes the entire attack surface
- **Simplicity**: Direct file I/O is simpler and faster than subprocess
- **Standard library**: No new dependencies required (pathlib and subprocess both stdlib)
- **Exact match**: `report_name in REPORTS` prevents suffix injection attacks

## Risks

### Risk: Path traversal via report filename lookup
**Mitigation**: The `REPORTS` dictionary maps user input to hardcoded filenames, preventing directory traversal. The validation `report_name in REPORTS` ensures only known keys are accepted.

### Risk: File not found at runtime
**Mitigation**: Report files are checked into version control at `data/reports/`. If missing, Python will raise `FileNotFoundError`, which is appropriate error behavior.

### Risk: Breaking existing functionality
**Mitigation**: Existing tests define the contract. All three tests in `tests/test_app.py` must pass:
- `test_report_endpoint_returns_allowlisted_report` (valid report retrieval)
- `test_report_endpoint_rejects_command_injection_payload` (security test)
- `test_read_report_rejects_unknown_report` (unknown report rejection)

## Validation Plan

Run the following commands in order:

1. **Install dependencies**: `uv sync --all-groups`
2. **Run unit tests**: `uv run pytest -q`
3. **Run linter**: `uv run ruff check .`
4. **Run SAST scan**: `uv run python scripts/run_sast.py --expect 0`

The final SAST scan must find zero findings, reducing the count from 1 to 0 as required by the acceptance criteria.
