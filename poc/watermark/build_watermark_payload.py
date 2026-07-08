from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def build_payload(decision: dict[str, object], ip: str) -> dict[str, object]:
    if decision.get("decision") != "authorized":
        raise ValueError("watermark payload requires an authorized download decision")
    issued_at = datetime.now(timezone.utc).isoformat()
    raw = "|".join(
        [
            str(decision.get("download_id", "")),
            str(decision.get("report_code", "")),
            str(decision.get("user", "")),
            ip,
            issued_at,
        ]
    )
    check_code = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16].upper()
    return {
        "download_id": decision["download_id"],
        "report_code": decision["report_code"],
        "user": decision["user"],
        "issued_at": issued_at,
        "ip": ip,
        "visible_text": f"user={decision['user']} report={decision['report_code']} check={check_code}",
        "check_code": check_code,
        "source_sha256": decision.get("sha256"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a deterministic watermark payload for drill evidence.")
    parser.add_argument("--decision", type=Path, required=True)
    parser.add_argument("--ip", default="127.0.0.1")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    decision = json.loads(args.decision.read_text(encoding="utf-8"))
    payload = build_payload(decision, args.ip)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"watermark payload {payload['check_code']} -> {args.out}")


if __name__ == "__main__":
    main()
