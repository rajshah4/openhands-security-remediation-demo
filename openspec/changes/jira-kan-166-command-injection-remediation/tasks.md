# Tasks

- [x] Create OpenSpec-style change artifacts (proposal, spec delta, design, tasks)
- [ ] Validate OpenSpec structure with validation script
- [ ] Implement security fix in `src/security_demo/app.py`
  - [ ] Replace subprocess.run with pathlib.Path.read_text()
  - [ ] Change validation from startswith() to exact match (in REPORTS)
  - [ ] Remove shell=True and shell command construction
- [ ] Run unit tests (pytest)
- [ ] Run linter (ruff)
- [ ] Run SAST scan and verify zero findings
- [ ] Document evidence waypoints in PR
- [ ] Open draft pull request
- [ ] Update Jira issue KAN-166 with PR link
