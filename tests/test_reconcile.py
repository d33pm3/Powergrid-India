from powergrid_india.reconcile import coerce_mw, norm_key, reconcile


def test_norm_key_collapses_ps_roman_and_spacing():
    assert norm_key("Khavda PS-I") == norm_key("Khavda PS-1")
    assert norm_key("Khavda PS-I") == norm_key("Khavda-1")
    assert norm_key("Bhadla PS") == norm_key("Bhadla")
    assert norm_key("Bhadla  PS") == norm_key("bhadla")


def test_coerce_mw_accepts_scraped_strings():
    assert coerce_mw("3,500") == 3500
    assert coerce_mw("3500 MW") == 3500
    assert coerce_mw(3500.9) == 3500
    assert coerce_mw(None) == 0
    assert coerce_mw("") == 0


def test_reconcile_rejects_empty_name_and_merges_variants():
    baseline = [
        {
            "Region": "WR",
            "State": "Gujarat",
            "Substation_Name": "Khavda PS-I",
            "Type_AIS_GIS": "GIS",
            "Voltage_Level": "765/400 kV",
            "Transformation_Capacity_MVA": "3x1500",
            "Renewable_Companies_Connected": "Adani Green Energy (5000 MW)",
            "Project_Type": "Solar/Wind/Hybrid",
            "Total_Capacity_MW": "7,000",
            "Remarks": "Active",
        }
    ]
    updates = [
        {"Substation_Name": "", "Total_Capacity_MW": 9999},
        {"Substation_Name": "Khavda-1", "Total_Capacity_MW": "7500 MW"},
        {"Substation_Name": "New Pool PS", "Region": "SR", "State": "Karnataka", "Total_Capacity_MW": 400},
    ]
    out = reconcile(baseline, updates)
    names = {r["Substation_Name"] for r in out}
    assert "" not in names
    assert "Khavda PS-I" in names
    khavda = next(r for r in out if r["Substation_Name"] == "Khavda PS-I")
    assert khavda["Total_Capacity_MW"] == 7500
    assert khavda["Data_Source"] == "[SOURCE_LIVE]"
    newborn = next(r for r in out if r["Substation_Name"] == "New Pool PS")
    assert newborn["Data_Source"] == "[SOURCE_LIVE:NEW]"
    assert newborn["Region"] == "SR"
    assert all(isinstance(r["Total_Capacity_MW"], int) for r in out)
