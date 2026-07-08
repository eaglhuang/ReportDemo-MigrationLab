from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path


def load_report(staging_csv: Path, report_code: str) -> dict[str, str] | None:
    with staging_csv.open("r", newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row.get("report_code") == report_code:
                return dict(row)
    return None


def decide(args: argparse.Namespace) -> dict[str, object]:
    report = load_report(args.staging_csv, args.report_code)
    checks = {
        "metadata_ready": report is not None,
        "role_allowed": args.role in {"compliance", "auditor", "admin"},
        "scope_allowed": report is not None and args.department == report.get("owner_department"),
        "audit_writable": args.audit_writable,
        "watermark_ready": args.watermark_ready,
    }
    allowed = all(checks.values())
    denied_reasons = [name for name, passed in checks.items() if not passed]
    return {
        "download_id": f"DL-{args.report_code}-{args.user}",
        "report_code": args.report_code,
        "user": args.user,
        "decision": "authorized" if allowed else "failed_closed",
        "checks": checks,
        "denied_reasons": denied_reasons,
        "file_name": report.get("file_name") if report else None,
        "sha256": report.get("sha256") if report else None,
        "decided_at": datetime.now(timezone.utc).isoformat(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate a fail-closed ReportDemo download request.")
    parser.add_argument("--staging-csv", type=Path, required=True)
    parser.add_argument("--report-code", required=True)
    parser.add_argument("--user", default="user-001")
    parser.add_argument("--role", default="compliance")
    parser.add_argument("--department", default="Compliance")
    parser.add_argument("--audit-writable", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--watermark-ready", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    result = decide(args)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{result['decision']} {args.report_code} -> {args.out}")


if __name__ == "__main__":
    main()
