from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


FIELDS = [
    "sample_serial",
    "report_code",
    "report_name",
    "data_date",
    "confidentiality",
    "owner_department",
    "trace_id",
    "file_name",
    "sha256",
    "migration_status",
]


def load_rows(path: Path) -> list[dict[str, str]]:
    rows = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise ValueError("metadata input must be a JSON array")
    return rows


def project(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    projected: list[dict[str, str]] = []
    seen_codes: set[str] = set()
    for row in rows:
        report_code = str(row.get("report_code", "")).strip()
        if not report_code:
            raise ValueError("report_code is required")
        if report_code in seen_codes:
            raise ValueError(f"duplicate report_code: {report_code}")
        seen_codes.add(report_code)
        projected.append(
            {
                "sample_serial": str(row.get("sample_serial", "")).strip(),
                "report_code": report_code,
                "report_name": str(row.get("report_name", "")).strip(),
                "data_date": str(row.get("data_date", "")).strip(),
                "confidentiality": str(row.get("confidentiality", "")).strip(),
                "owner_department": str(row.get("owner_department", "")).strip(),
                "trace_id": str(row.get("trace_id", "")).strip(),
                "file_name": str(row.get("file_name", "")).strip(),
                "sha256": str(row.get("sha256", "")).strip(),
                "migration_status": "projected",
            }
        )
    return projected


def write_csv(rows: list[dict[str, str]], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Project ReportDemo metadata JSON into staging CSV.")
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    rows = project(load_rows(args.metadata))
    write_csv(rows, args.out)
    print(f"projected {len(rows)} rows to {args.out}")


if __name__ == "__main__":
    main()
