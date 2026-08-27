#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from security_demo.automation import desired_mode

DEFAULT_HOST = "https://app.replicated.rajistics.com"
TARGET_NAMES = {
    "SDLC_1 - Jira to PR",
    "Security Demo - Jira SAST Remediation",
}


def request_json(url: str, api_key: str, method: str = "GET", payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode() if payload is not None else None
    request = Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method=method,
    )
    try:
        with urlopen(request, timeout=30) as response:
            return json.loads(response.read())
    except HTTPError as exc:
        body = exc.read().decode(errors="replace")
        raise RuntimeError(f"OpenHands API returned {exc.code}: {body}") from exc


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("security", "sdlc"))
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--host", default=os.getenv("OPENHANDS_HOST_RAJISTICS", DEFAULT_HOST))
    args = parser.parse_args()

    api_key = os.getenv("OPENHANDS_API_KEY_ORG")
    if not api_key:
        raise SystemExit("OPENHANDS_API_KEY_ORG is required")

    host = args.host.rstrip("/")
    response = request_json(f"{host}/api/automation/v1?limit=100", api_key)
    automations = response.get("automations", response.get("items", []))
    selected = [automation for automation in automations if automation["name"] in TARGET_NAMES]
    by_name = {automation["name"]: automation for automation in selected}
    missing = sorted(TARGET_NAMES - by_name.keys())
    if missing:
        raise SystemExit(f"Missing required automations: {', '.join(missing)}")

    security_mode = args.mode == "security"
    changes = []
    for name in sorted(TARGET_NAMES):
        automation = by_name[name]
        enabled = desired_mode(name, security_mode)
        changes.append({"id": automation["id"], "name": name, "enabled": enabled})
        if args.apply and automation.get("enabled") != enabled:
            request_json(
                f"{host}/api/automation/v1/{automation['id']}",
                api_key,
                method="PATCH",
                payload={"enabled": enabled},
            )

    print(json.dumps({"applied": args.apply, "mode": args.mode, "changes": changes}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
