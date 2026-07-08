from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def require(path: Path) -> None:
    if not path.exists() or path.stat().st_size == 0:
        raise ValueError(f"missing or empty: {path}")


def count_controllers(root: Path) -> int:
    return len(list((root / "Qutora.API" / "Controllers").glob("*.cs")))


def count_endpoints(root: Path) -> int:
    total = 0
    for path in (root / "Qutora.API" / "Controllers").glob("*.cs"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for token in ["[HttpGet", "[HttpPost", "[HttpPut", "[HttpDelete", "[HttpPatch"]:
            total += text.count(token)
    return total


def validate(args: argparse.Namespace) -> dict[str, object]:
    require(args.metadata)
    require(args.staging_csv)
    require(args.decision)
    require(args.watermark)

    metadata_rows = json.loads(args.metadata.read_text(encoding="utf-8"))
    with args.staging_csv.open("r", newline="", encoding="utf-8") as handle:
        staging_rows = list(csv.DictReader(handle))
    decision = json.loads(args.decision.read_text(encoding="utf-8"))
    watermark = json.loads(args.watermark.read_text(encoding="utf-8"))
    controllers = count_controllers(args.qutora_root)
    endpoints = count_endpoints(args.qutora_root)

    checks = {
        "metadata_rows_match_staging": len(metadata_rows) == len(staging_rows),
        "download_authorized": decision.get("decision") == "authorized",
        "watermark_has_check_code": bool(watermark.get("check_code")),
        "qutora_controllers_19": controllers == 19,
        "qutora_endpoints_173": endpoints == 173,
    }
    return {
        "result": "pass" if all(checks.values()) else "fail",
        "checks": checks,
        "counts": {
            "metadata_rows": len(metadata_rows),
            "staging_rows": len(staging_rows),
            "qutora_controllers": controllers,
            "qutora_endpoints": endpoints,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate ReportDemo PoC smoke outputs.")
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--staging-csv", type=Path, required=True)
    parser.add_argument("--decision", type=Path, required=True)
    parser.add_argument("--watermark", type=Path, required=True)
    parser.add_argument("--qutora-root", type=Path, default=Path("open-source-sandbox/qutora-api"))
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    result = validate(args)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if result["result"] != "pass":
        raise SystemExit(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"pass -> {args.out}")


if __name__ == "__main__":
    main()
