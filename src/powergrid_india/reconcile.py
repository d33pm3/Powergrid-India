"""Name-tolerant merge of live updates into the planning-grade baseline."""

from __future__ import annotations

import re
from typing import Any, Iterable, Mapping, MutableMapping

SCHEMA_FIELDS = [
    "Region",
    "State",
    "Substation_Name",
    "Type_AIS_GIS",
    "Voltage_Level",
    "Transformation_Capacity_MVA",
    "Renewable_Companies_Connected",
    "Project_Type",
    "Total_Capacity_MW",
    "Remarks",
    "Data_Source",
]

_ROMAN = {"i": "1", "ii": "2", "iii": "3", "iv": "4", "v": "5"}


def norm_key(name: str) -> str:
    """Normalize a substation name for matching.

    Casefold, drop PS / P.S. tokens, unify hyphen/space runs, and convert a
    trailing roman suffix (I–V) to arabic so "Khavda PS-I" and "Khavda-1"
    collapse to the same key.
    """
    s = re.sub(r"\s+", " ", str(name or "")).strip().casefold()
    s = re.sub(r"\bp\.?s\.?\b", " ", s)
    s = re.sub(r"[\s\-–—]+", "-", s).strip("-")
    m = re.search(r"-(i{1,3}|iv|v)$", s)
    if m:
        s = s[: m.start()] + "-" + _ROMAN[m.group(1)]
    return s


def coerce_mw(v: Any) -> int:
    """Coerce MW to int. Scraped values arrive as '3,500', '3500 MW', floats, or junk."""
    if isinstance(v, bool):
        return int(v)
    if isinstance(v, (int, float)):
        return int(v)
    digits = re.sub(r"[^\d]", "", str(v or ""))
    return int(digits) if digits else 0


# Public aliases used in the skill document
_norm_key = norm_key
_mw = coerce_mw


def reconcile(
    baseline_records: Iterable[Mapping[str, Any]],
    live_updates: Iterable[Mapping[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Merge live updates into baseline.

    Guards:
      (a) empty/missing name does not mint a phantom record
      (b) MW values are coerced to int before sort
      (c) name-key normalization absorbs PS-suffix / roman / spacing variants
    """
    master: dict[str, dict[str, Any]] = {}
    for r in baseline_records:
        rec = dict(r)
        rec["Total_Capacity_MW"] = coerce_mw(rec.get("Total_Capacity_MW"))
        name = str(rec.get("Substation_Name", "")).strip()
        if not name:
            continue
        rec["Substation_Name"] = name
        master[norm_key(name)] = rec

    for update in live_updates or []:
        raw_name = str(update.get("Substation_Name", "")).strip()
        if not raw_name:
            continue
        key = norm_key(raw_name)
        patched: MutableMapping[str, Any] = dict(update)
        if "Total_Capacity_MW" in patched:
            patched["Total_Capacity_MW"] = coerce_mw(patched["Total_Capacity_MW"])
        if key in master:
            for field in (
                "Total_Capacity_MW",
                "Renewable_Companies_Connected",
                "Transformation_Capacity_MVA",
                "Remarks",
                "Voltage_Level",
                "Type_AIS_GIS",
                "Project_Type",
                "State",
                "Region",
            ):
                if patched.get(field) not in (None, ""):
                    master[key][field] = patched[field]
            master[key]["Data_Source"] = "[SOURCE_LIVE]"
        else:
            new_rec = {f: patched.get(f, "") for f in SCHEMA_FIELDS}
            new_rec["Substation_Name"] = raw_name
            new_rec["Total_Capacity_MW"] = coerce_mw(patched.get("Total_Capacity_MW"))
            new_rec["Data_Source"] = "[SOURCE_LIVE:NEW]"
            master[key] = new_rec

    for rec in master.values():
        if not rec.get("Data_Source"):
            rec["Data_Source"] = "[SOURCE_FALLBACK:BASELINE]"

    return sorted(master.values(), key=lambda x: -coerce_mw(x.get("Total_Capacity_MW")))
