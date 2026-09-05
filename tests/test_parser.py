from collections import Counter

from powergrid_india.parser import parse_master_table
from powergrid_india.reconcile import reconcile


def test_master_table_is_132_unique_and_totals_130500():
    recs = parse_master_table()
    assert len(recs) == 132
    names = [r["Substation_Name"] for r in recs]
    assert len(set(names)) == 132
    assert sum(r["Total_Capacity_MW"] for r in recs) == 130_500
    regions = Counter(r["Region"] for r in recs)
    assert regions == {"WR": 54, "SR": 36, "NR": 18, "ER": 16, "NER": 8}
    assert len({r["State"] for r in recs}) == 30


def test_reconcile_baseline_only_tags_fallback():
    recs = reconcile(parse_master_table(), [])
    assert len(recs) == 132
    assert all(r["Data_Source"] == "[SOURCE_FALLBACK:BASELINE]" for r in recs)
    assert recs[0]["Substation_Name"] == "Pang PS"
    assert recs[0]["Total_Capacity_MW"] == 13_000
