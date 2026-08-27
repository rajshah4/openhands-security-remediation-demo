#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from security_demo.findings import normalize_semgrep

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RULE = ROOT / "security" / "rules" / "python-command-injection.yml"
DEFAULT_RAW_OUTPUT = ROOT / "security" / "findings" / "generated-semgrep-raw.json"
DEFAULT_OUTPUT = ROOT / "security" / "findings" / "generated-semgrep.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rule", type=Path, default=DEFAULT_RULE)
    parser.add_argument("--target", type=Path, default=ROOT / "src")
    parser.add_argument("--raw-output", type=Path, default=DEFAULT_RAW_OUTPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--expect",
        type=int,
        help="fail unless exactly this many findings are present",
    )
    args = parser.parse_args()

    result = subprocess.run(
        [
            "semgrep",
            "scan",
            "--config",
            str(args.rule),
            "--json",
            "--quiet",
            "--metrics=off",
            str(args.target),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode not in (0, 1):
        message = f"Semgrep failed with exit code {result.returncode}: {result.stderr.strip()}"
        raise SystemExit(message)

    raw_report = json.loads(result.stdout)
    normalized = normalize_semgrep(raw_report)
    args.raw_output.parent.mkdir(parents=True, exist_ok=True)
    args.raw_output.write_text(json.dumps(raw_report, indent=2, sort_keys=True) + "\n")
    args.output.write_text(json.dumps(normalized, indent=2, sort_keys=True) + "\n")

    count = len(normalized["findings"])
    print(f"SAST findings: {count}")
    print(f"Normalized report: {args.output}")
    if args.expect is not None and count != args.expect:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
