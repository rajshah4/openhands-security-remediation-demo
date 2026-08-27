#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from security_demo.jira import jira_comment


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("issue_key")
    parser.add_argument("message")
    args = parser.parse_args()

    base_url = os.getenv("JIRA_API_BASE_URL", "").rstrip("/")
    token = os.getenv("JIRA_API_TOKEN")
    if not base_url or not token:
        raise SystemExit("JIRA_API_BASE_URL and JIRA_API_TOKEN are required")

    request = Request(
        f"{base_url}/rest/api/3/issue/{args.issue_key}/comment",
        data=json.dumps(jira_comment(args.message)).encode(),
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

    print(json.dumps({"comment_id": result.get("id"), "issue_key": args.issue_key}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
