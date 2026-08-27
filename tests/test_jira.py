from security_demo.jira import DISCLOSURE, demo_issue_fields, jira_comment


def test_demo_issue_fields_are_narrowly_scoped() -> None:
    fields = demo_issue_fields()

    assert fields["project"] == {"key": "KAN"}
    assert fields["issuetype"] == {"name": "Task"}
    assert fields["labels"] == ["security-remediation"]
    text = " ".join(
        node["content"][0]["text"] for node in fields["description"]["content"]
    )
    assert "demo/command-injection" in text
    assert "flask-request-to-subprocess-shell" in text
    assert DISCLOSURE in text


def test_jira_comment_includes_ai_disclosure() -> None:
    body = jira_comment("Draft PR: https://github.com/example/repo/pull/1")
    paragraphs = body["body"]["content"]

    assert paragraphs[0]["content"][0]["text"].startswith("Draft PR:")
    assert paragraphs[1]["content"][0]["text"] == DISCLOSURE
