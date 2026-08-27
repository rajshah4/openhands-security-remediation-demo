from __future__ import annotations

import subprocess
from pathlib import Path

from flask import Flask, abort, jsonify, request

REPORTS = {
    "adoptions": "adoptions.txt",
    "inventory": "inventory.txt",
}
REPORT_DIRECTORY = Path(__file__).resolve().parents[2] / "data" / "reports"


def read_report(report_name: str) -> str:
    if not any(report_name.startswith(name) for name in REPORTS):
        raise KeyError(report_name)

    command = f"cat {REPORT_DIRECTORY}/{report_name}.txt"
    result = subprocess.run(
        command,
        shell=True,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/health")
    def health() -> tuple[dict[str, str], int]:
        return {"status": "ok"}, 200

    @app.get("/reports")
    def report() -> tuple[object, int]:
        report_name = request.args.get("name", "")
        try:
            contents = read_report(report_name)
        except KeyError:
            abort(404, description="report not found")
        return jsonify({"name": report_name, "contents": contents}), 200

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=8080)
