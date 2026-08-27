from __future__ import annotations

import hashlib
from typing import Any


def repository_path(path: str) -> str:
    normalized = path.replace("\\", "/")
    for marker in ("src/", "tests/"):
        index = normalized.find(marker)
        if index >= 0:
            return normalized[index:]
    return normalized


def normalize_semgrep(report: dict[str, Any]) -> dict[str, Any]:
    findings = []
    for result in report.get("results", []):
        extra = result.get("extra", {})
        metadata = extra.get("metadata", {})
        path = repository_path(result.get("path", ""))
        line = result.get("start", {}).get("line", 0)
        rule_id = metadata.get("rule_id", result.get("check_id", "").rsplit(".", 1)[-1])
        fingerprint_source = f"{rule_id}:{path}:{line}"
        fingerprint = hashlib.sha256(fingerprint_source.encode()).hexdigest()[:16]
        findings.append(
            {
                "fingerprint": fingerprint,
                "rule_id": rule_id,
                "severity": extra.get("severity", "UNKNOWN"),
                "confidence": metadata.get("confidence", "UNKNOWN"),
                "cwe": metadata.get("cwe", []),
                "path": path,
                "line": line,
                "message": extra.get("message", ""),
            }
        )

    return {
        "schema_version": 1,
        "scanner": "semgrep",
        "category": "sast",
        "findings": findings,
    }
