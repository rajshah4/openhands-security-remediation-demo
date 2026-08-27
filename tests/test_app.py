from security_demo.app import create_app, read_report


def test_health_endpoint() -> None:
    client = create_app().test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_report_endpoint_returns_allowlisted_report() -> None:
    client = create_app().test_client()

    response = client.get("/reports?name=inventory")

    assert response.status_code == 200
    assert response.get_json() == {
        "name": "inventory",
        "contents": "Current inventory: 14 cats, 9 dogs, 3 rabbits.\n",
    }


def test_report_endpoint_rejects_command_injection_payload() -> None:
    client = create_app().test_client()

    response = client.get("/reports?name=inventory.txt%3Bprintf%20injected%3B%23")

    assert response.status_code == 404


def test_read_report_rejects_unknown_report() -> None:
    try:
        read_report("../../etc/passwd")
    except KeyError as exc:
        assert exc.args == ("../../etc/passwd",)
    else:
        raise AssertionError("unknown reports must be rejected")


def test_read_report_rejects_shell_metacharacters() -> None:
    """Regression test for CWE-78 command injection"""
    payloads = [
        "inventory; echo injected",
        "inventory && echo injected",
        "inventory | echo injected",
        "inventory; rm -rf /",
        "$(whoami)",
        "`whoami`",
    ]
    for payload in payloads:
        try:
            read_report(payload)
        except KeyError as exc:
            assert exc.args == (payload,)
        else:
            raise AssertionError(f"shell metacharacter payload must be rejected: {payload}")
