# Report Endpoint Security Spec Delta

## ADDED Requirements

### Requirement: Report endpoint must reject command injection payloads

#### Scenario: Shell metacharacter injection attempt is blocked

- Given a user sends a GET request to `/reports` with name parameter containing shell metacharacters
- When the name parameter is `inventory.txt;printf injected;#` or similar injection payload
- Then the server returns HTTP 404 and does not execute the injected command

#### Scenario: Allowlisted reports are retrieved successfully

- Given a user sends a GET request to `/reports` with a valid report name
- When the name parameter is `inventory` or `adoptions`
- Then the server returns HTTP 200 with the correct report contents

#### Scenario: Unknown report names are rejected

- Given a user sends a GET request to `/reports` with an unknown report name
- When the name parameter is not in the allowlist (e.g., `../../../etc/passwd`)
- Then the server returns HTTP 404

## MODIFIED Requirements

### Requirement: Report retrieval must not use shell command execution

#### Previous Behavior
- Report contents were retrieved via `subprocess.run("cat ...", shell=True)`
- Shell metacharacters in user input could be executed

#### New Behavior
- Report contents are retrieved via Python `pathlib.Path.read_text()`
- No shell interpreter is invoked
- Shell metacharacters have no special meaning
