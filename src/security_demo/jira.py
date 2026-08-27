from __future__ import annotations

from typing import Any

DISCLOSURE = "Created by an OpenHands AI agent on behalf of Rajiv Shah."


def adf_document(paragraphs: list[str]) -> dict[str, Any]:
    return {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [{"type": "text", "text": paragraph}],
            }
            for paragraph in paragraphs
        ],
    }


def demo_issue_fields(project: str = "KAN") -> dict[str, Any]:
    return {
        "project": {"key": project},
        "issuetype": {"name": "Task"},
        "summary": "[SAST] Remediate command injection in report endpoint",
        "labels": ["security-remediation"],
        "description": adf_document(
            [
                "Repository: rajshah4/openhands-security-remediation-demo",
                "Branch: demo/command-injection",
                "Semgrep rule: flask-request-to-subprocess-shell",
                (
                    "Finding: request data reaches subprocess.run with shell=True "
                    "in the report endpoint."
                ),
                (
                    "Acceptance: preserve allowlisted report retrieval, reject shell "
                    "metacharacter payloads, add regression coverage, and reduce the "
                    "Semgrep finding count from one to zero."
                ),
                "OpenHands must create a draft pull request and must not merge it.",
                DISCLOSURE,
            ]
        ),
    }


def jira_comment(text: str) -> dict[str, Any]:
    return {"body": adf_document([text, DISCLOSURE])}
