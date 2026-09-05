"""Parse the 132-record baseline from references/substation-master.md."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .reconcile import SCHEMA_FIELDS, coerce_mw

COLUMN_MAP = {
    "Region": "Region",
    "State": "State",
    "Substation_Name": "Substation_Name",
    "Type": "Type_AIS_GIS",
    "Type_AIS_GIS": "Type_AIS_GIS",
    "Voltage_Level": "Voltage_Level",
    "Capacity_MVA": "Transformation_Capacity_MVA",
    "Transformation_Capacity_MVA": "Transformation_Capacity_MVA",
    "Companies_Connected": "Renewable_Companies_Connected",
    "Renewable_Companies_Connected": "Renewable_Companies_Connected",
    "Project_Type": "Project_Type",
    "Total_MW": "Total_Capacity_MW",
    "Total_Capacity_MW": "Total_Capacity_MW",
    "Remarks": "Remarks",
    "Data_Source": "Data_Source",
}


def _repo_root() -> Path:
    # src/powergrid_india/parser.py -> repo root is parents[2]
    here = Path(__file__).resolve()
    candidates = [
        here.parents[2] / "references" / "substation-master.md",
        here.parents[1] / "references" / "substation-master.md",
        Path.cwd() / "references" / "substation-master.md",
    ]
    for path in candidates:
        if path.is_file():
            return path.parent.parent if path.parent.name == "references" else path.parents[1]
    return here.parents[2]


def default_master_path() -> Path:
    root = _repo_root()
    path = root / "references" / "substation-master.md"
    if not path.is_file():
        raise FileNotFoundError(
            "substation-master.md not found. Expected at references/substation-master.md "
            f"relative to the repository root (looked near {root})."
        )
    return path


def parse_master_table(path: str | Path | None = None) -> list[dict[str, Any]]:
    """Read the four markdown section tables into schema-complete records."""
    master_path = Path(path) if path else default_master_path()
    text = master_path.read_text(encoding="utf-8")
    records: list[dict[str, Any]] = []
    header: list[str] | None = None

    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            header = None
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not cells:
            continue
        if set(cells[0]) <= {"-"} or cells[0].startswith("-"):
            continue
        if cells[0] == "Region" or (cells[0] in COLUMN_MAP and cells[0] == "Region"):
            header = [COLUMN_MAP.get(c, c) for c in cells]
            continue
        if header is None:
            continue
        if cells[0] not in {"WR", "NR", "SR", "ER", "NER"}:
            continue
        row = {f: "" for f in SCHEMA_FIELDS}
        for idx, field in enumerate(header):
            if idx < len(cells) and field in row:
                row[field] = cells[idx]
        name = str(row.get("Substation_Name", "")).strip()
        if not name:
            continue
        row["Substation_Name"] = name
        row["Total_Capacity_MW"] = coerce_mw(row.get("Total_Capacity_MW"))
        records.append(row)
    return records
