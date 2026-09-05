---
name: powergrid-india
version: "2.1.2"
author: de-risk Consulting (DKM)
description: |
  PAN India RE Substation skill - 132+ CTU/PGCIL substations across 5 regions (WR, NR, SR, ER, NER) and 30 states. Performs live web research (CTUIL, PGCIL, CEA, MNRE, GEC), reconciles against the embedded baseline, and builds a 10-sheet XLSX workbook with an Analytics Dashboard.

  Always use this skill for: India RE substation data; RE-grid XLSX workbooks; PGCIL/CTUIL substation lists; GNA/LTA connectivity margins; Green Energy Corridor Phase-I/II; 765/400 kV evacuation nodes; BESS or Pump Storage nodes; RE parks (Khavda, Bhadla, Pang, Pavagada, Kurnool, Fatehgarh, Barmer, Rewa); RE developers (Adani Green, NTPC, SECI, ReNew, Greenko); FDRE/hybrid/PSP nodes; InvIT RE transmission assets. Invoke even for casual queries touching India RE substations, PGCIL, or CTUIL. Not for electricity tariff or regulatory-law questions, discom/utility financial modeling, or thermal topics with no RE evacuation angle.
changelog: |
  v2.1.2 (2026-09-06): Public release. Runnable package, exclusive voltage tiers,
  name-key hyphen fix, BESS/PSP filter excludes Hydro-Solar, portable outputs/,
  CSV baseline, epistemic caveat on Dashboard Block 8.
compatibility:
  python_packages: [openpyxl]
---

# Powergrid India — PAN India RE Substation Master Skill v2.1.2

Canonical source: https://github.com/d33pm3/Powergrid-India

## Package

```
Powergrid-India/
├── SKILL.md
├── references/substation-master.md
├── references/substations.csv          ← 132-row baseline
├── references/generation-script.md
├── evals/
├── src/powergrid_india/
└── tests/
```

## Part 0 — Contract

The 132-row baseline is **planning-grade, not a verified regulatory filing**. Tag unconfirmed rows `[SOURCE_FALLBACK:BASELINE]`. Live-confirmed rows may use `[SOURCE_LIVE]` / `[SOURCE_LIVE:NEW]`. Every workbook and chat answer carries this caveat.

Loop bounds: each of the 5 public fetches is attempted at most twice. Never simulate a source.

## Execution order

0. Plan deliverable and verification artifacts
1. Live research (CTUIL, PGCIL, CEA, MNRE, GEC) — current year in queries
2. `reconcile(parse_master_table(), live_updates)`
3. `build_workbook_data(records)` then `create_workbook(...)`
4. QA on the saved file (openpyxl re-open)

Public URLs only: https://www.ctuil.in, https://www.powergrid.in, https://www.cea.nic.in, https://www.mnre.gov.in, https://www.powergrid.in/project/green-energy-corridor

## Schema (11 columns)

Region, State, Substation_Name, Type_AIS_GIS, Voltage_Level, Transformation_Capacity_MVA, Renewable_Companies_Connected, Project_Type, Total_Capacity_MW, Remarks, Data_Source

## Baseline totals (recompute after live merge)

132 substations, 130,500 MW. WR 54 / 76,550; SR 36 / 31,480; NR 18 / 17,800; ER 16 / 4,000; NER 8 / 670. 30 states.

## Workbook (10 sheets)

All_Substations, Regional_Summary, State_Summary, Western_Region, Northern_Region, Southern_Region, Eastern_Region, NorthEastern_Region, Top_50_Substations, Analytics_Dashboard

Dashboard blocks: KPIs, regional, voltage tiers (exclusive match), project mix, 9 BESS/PSP nodes, GEC, top 15, source log + epistemic caveat.

Formatting: data headers `#2E7D32`, dashboard headers `#1C3A6B`, sub-headers `#00695C`, planned `#E65100`, freeze `A2`, auto-filter on all sheets.

## Implementation

Use `src/powergrid_india`. Do not hand-build sheet JSON. Checkpoints and xlsx go to `outputs/` (gitignored).

```bash
python -m powergrid_india.cli --output outputs/PAN_India_RE_Substations_Master_Data.xlsx
```
