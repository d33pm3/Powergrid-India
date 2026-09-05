"""Command-line entry point for the Powergrid-India workbook builder."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from .parser import parse_master_table
from .reconcile import reconcile
from .workbook import create_workbook, default_source_log


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="powergrid-india",
        description="Build the PAN India RE substations workbook from the planning-grade baseline.",
    )
    p.add_argument(
        "-o",
        "--output",
        default="outputs/PAN_India_RE_Substations_Master_Data.xlsx",
        help="Output .xlsx path (default: outputs/PAN_India_RE_Substations_Master_Data.xlsx)",
    )
    p.add_argument(
        "--master",
        default=None,
        help="Path to substation-master.md (default: references/substation-master.md)",
    )
    p.add_argument(
        "--checkpoint-csv",
        default="outputs/reconciled_checkpoint.csv",
        help="Write reconciled records to CSV before the workbook is saved.",
    )
    return p


def _write_checkpoint(records, path: str) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    if not records:
        return
    fields = list(records[0].keys())
    with out.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    baseline = parse_master_table(args.master)
    records = reconcile(baseline, live_updates=[])
    _write_checkpoint(records, args.checkpoint_csv)
    path, sheets = create_workbook(
        master_records=records,
        source_log=default_source_log(),
        output_path=args.output,
    )
    print(f"Saved: {path} ({len(sheets)} sheets, {len(records)} substations)")
    print(
        "Caveat: baseline is planning-grade and indicative — not a verified regulatory filing. "
        "Live research against CTUIL / PGCIL / CEA / MNRE / GEC was not run in this CLI path."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
