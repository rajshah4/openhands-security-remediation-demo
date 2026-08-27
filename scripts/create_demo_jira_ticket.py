#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from security_demo.jira import demo_issue_fields


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--project", default="KAN")
    args = parser.parse_args()

    payload = {"fields": demo_issue_fields(args.project)}
    if not args.apply:
        print(json.dumps(payload, indent=2))
        return 0

    base_url = os.getenv("JIRA_API_BASE_URL", "").rstrip("/")
    token = os.getenv("JIRA_API_TOKEN")
    site_url = os.getenv("JIRA_SITE_URL", "").rstrip("/")
    if not base_url or not token:
        raise SystemExit("JIRA_API_BASE_URL and JIRA_API_TOKEN are required for --apply")

    request = Request(
        f"{base_url}/rest/api/3/issue",
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=30) as response:
            result = json.loads(response.read())
    except HTTPError as exc:
        body = exc.read().decode(errors="replace")
        raise RuntimeError(f"Jira API returned {exc.code}: {body}") from exc

    key = result["key"]
    print(json.dumps({"key": key, "url": f"{site_url}/browse/{key}"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
