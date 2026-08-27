import json
from pathlib import Path

from security_demo.findings import normalize_semgrep


def test_normalize_semgrep_produces_stable_security_finding() -> None:
    fixture_path = Path(__file__).parent / "fixtures" / "semgrep-command-injection.json"
    report = json.loads(fixture_path.read_text())

    normalized = normalize_semgrep(report)

    assert normalized["schema_version"] == 1
    assert normalized["scanner"] == "semgrep"
    assert normalized["category"] == "sast"
    assert normalized["findings"] == [
        {
            "fingerprint": "2abe0b091856ae4d",
            "rule_id": "flask-request-to-subprocess-shell",
            "severity": "ERROR",
            "confidence": "HIGH",
            "cwe": [
                "CWE-78: Improper Neutralization of Special Elements used in an OS Command"
            ],
            "path": "src/security_demo/app.py",
            "line": 31,
            "message": "User-controlled request data reaches subprocess.run with shell=True.",
        }
    ]


def test_normalize_semgrep_handles_clean_report() -> None:
    assert normalize_semgrep({"results": []})["findings"] == []
