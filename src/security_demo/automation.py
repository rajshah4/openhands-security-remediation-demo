from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SPEC_FIELDS = {
    "name",
    "model",
    "trigger",
    "timeout",
    "keep_alive",
    "repos",
    "template",
    "enabled",
}


def load_prompt_automation(spec_path: Path) -> dict[str, Any]:
    spec = json.loads(spec_path.read_text())
    payload = {key: value for key, value in spec.items() if key in SPEC_FIELDS}
    payload["prompt"] = (spec_path.parent / spec["prompt_file"]).read_text()
    return payload


def desired_mode(name: str, security_mode: bool) -> bool | None:
    if name == "SDLC_1 - Jira to PR":
        return not security_mode
    if name == "Security Demo - Jira SAST Remediation":
        return security_mode
    return None
