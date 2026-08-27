# Report Security Spec Delta

## ADDED Requirements

### Requirement: Report endpoint must reject shell metacharacter injection attempts

#### Scenario: Shell command chaining is rejected

- Given the `/reports` endpoint accepts a `name` query parameter
- When a request includes shell command chaining metacharacters (`;`, `&&`, `||`)
- Then the server responds with HTTP 404 and does not execute the injected command

#### Scenario: Shell command substitution is rejected

- Given the `/reports` endpoint accepts a `name` query parameter
- When a request includes command substitution syntax (`$()` or backticks)
- Then the server responds with HTTP 404 and does not execute the substituted command

#### Scenario: Shell redirection is rejected

- Given the `/reports` endpoint accepts a `name` query parameter
- When a request includes redirection operators (`>`, `>>`, `<`, `|`)
- Then the server responds with HTTP 404 and does not perform the redirection

#### Scenario: Only exact allowlist matches are accepted

- Given the `REPORTS` dictionary contains exactly two entries: `inventory` and `adoptions`
- When a request uses an exact key match (`name=inventory` or `name=adoptions`)
- Then the server responds with HTTP 200 and the corresponding report contents
- When a request uses a partial match or any other value
- Then the server responds with HTTP 404

## PRESERVED Requirements

### Requirement: Report endpoint returns allowlisted reports

#### Scenario: Inventory report is retrieved successfully

- Given the `data/reports/inventory.txt` file exists
- When a request is made with `name=inventory`
- Then the server responds with HTTP 200 and the inventory report contents

#### Scenario: Adoptions report is retrieved successfully

- Given the `data/reports/adoptions.txt` file exists
- When a request is made with `name=adoptions`
- Then the server responds with HTTP 200 and the adoptions report contents

### Requirement: Unknown reports are rejected

#### Scenario: Path traversal attempts are rejected

- Given a request includes path traversal sequences (`../../etc/passwd`)
- When the request is processed
- Then the server responds with HTTP 404 or raises `KeyError`
