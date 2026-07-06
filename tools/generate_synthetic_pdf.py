from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import date
from pathlib import Path


CONFIDENTIALITY = ["internal", "confidential", "high"]


def pdf_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def build_pdf(lines: list[str]) -> bytes:
    stream_lines = ["BT", "/F1 14 Tf", "72 760 Td"]
    for index, line in enumerate(lines):
        if index:
            stream_lines.append("0 -24 Td")
        stream_lines.append(f"({pdf_escape(line)}) Tj")
    stream_lines.append("ET")
    stream = "\n".join(stream_lines).encode("ascii")

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream",
    ]

    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for obj_id, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out.extend(f"{obj_id} 0 obj\n".encode("ascii"))
        out.extend(body)
        out.extend(b"\nendobj\n")
    xref_offset = len(out)
    out.extend(f"xref\n0 {len(objects)+1}\n".encode("ascii"))
    out.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        out.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    out.extend(
        f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode(
            "ascii"
        )
    )
    return bytes(out)


def generate(count: int, out_dir: Path, data_date: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    hash_rows = []
    for idx in range(1, count + 1):
        serial = f"SYN-{idx:04d}"
        report_code = f"RPT-INSIDER-{idx:03d}"
        confidentiality = CONFIDENTIALITY[(idx - 1) % len(CONFIDENTIALITY)]
        filename = f"{serial}-{report_code}.pdf"
        trace_id = f"TRACE-{serial}"
        lines = [
            "ReportDemo Synthetic PDF",
            f"sample_serial: {serial}",
            f"report_code: {report_code}",
            f"data_date: {data_date}",
            f"confidentiality: {confidentiality}",
            "owner_department: Compliance",
            f"trace_id: {trace_id}",
            "No production data. For migration drill only.",
        ]
        pdf_bytes = build_pdf(lines)
        pdf_path = out_dir / filename
        pdf_path.write_bytes(pdf_bytes)
        digest = hashlib.sha256(pdf_bytes).hexdigest()
        rows.append(
            {
                "sample_serial": serial,
                "report_code": report_code,
                "report_name": "ReportDemo synthetic insider trading report",
                "data_date": data_date,
                "confidentiality": confidentiality,
                "owner_department": "Compliance",
                "legacy_document_id": "",
                "trace_id": trace_id,
                "file_name": filename,
                "sha256": digest,
            }
        )
        hash_rows.append(
            {
                "sample_serial": serial,
                "file_name": filename,
                "sha256": digest,
                "file_size": len(pdf_bytes),
            }
        )

    (out_dir / "metadata-export.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    with (out_dir / "pdf-baseline-hash.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["sample_serial", "file_name", "sha256", "file_size"])
        writer.writeheader()
        writer.writerows(hash_rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic PDFs for ReportDemo migration drill.")
    parser.add_argument("--count", type=int, default=3, help="Number of PDFs to generate.")
    parser.add_argument("--out", type=Path, required=True, help="Output directory.")
    parser.add_argument("--data-date", default=date.today().isoformat(), help="Synthetic data date.")
    args = parser.parse_args()
    if args.count <= 0:
        raise SystemExit("--count must be positive")
    generate(args.count, args.out, args.data_date)
    print(f"generated {args.count} synthetic PDFs under {args.out}")


if __name__ == "__main__":
    main()
