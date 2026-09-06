# Powergrid-India

**Author:** DK Mendiratta

Unofficial public skill and workbook builder for **PAN India renewable-energy evacuation substations** on the CTU / PGCIL grid. This is not POWERGRID, PGCIL, or CTUIL software.

Canonical source: https://github.com/d33pm3/Powergrid-India

## This is / this is not

**This is** an unofficial planning workbook builder and AI skill for PAN-India RE evacuation substations.
**This is** a 132-row public baseline plus an optional live reconcile against public CTUIL / PGCIL / CEA / MNRE / GEC pages.
**This is** a local Python package that writes a 10-sheet `.xlsx` under `outputs/`.
**This is not** POWERGRID, PGCIL, or CTUIL official software.
**This is not** a verified connectivity, GNA/LTA, or CEA regulatory filing.
**This is not** a web app, API, Docker stack, or always-on scraper.
**This is not** tariff, discom, or thermal-plant modelling.
**This is not** a live-refreshed dataset in a fresh clone — the CLI uses the embedded baseline only.

The 132-record baseline is **planning-grade**, compiled from public reporting. Capacity, MVA, and developer-allocation figures are indicative. Rows that are not confirmed against a live source in the current session must be tagged `[SOURCE_FALLBACK:BASELINE]` and must not be described as verified regulatory filings.

## Who it is for

- RE planners mapping evacuation nodes and corridor capacity
- InvIT / transmission analysts who need a planning-grade master, not a filing
- GRC advisors checking source tags and planning vs verified claims
- Agent builders who will load `SKILL.md` and run the live-research path

## What it does

- Loads a 132-substation master (5 regions, 30 states, ~130,500 MW baseline)
- Optionally merges live updates from public CTUIL / PGCIL / CEA / MNRE / GEC sources (agent path only)
- Builds a 10-sheet `.xlsx` workbook (9 data sheets + an 8-block Analytics Dashboard)

## Workbook: 10 sheets and 11 columns

Sheets: `All_Substations`, `Regional_Summary`, `State_Summary`, `Western_Region`, `Northern_Region`, `Southern_Region`, `Eastern_Region`, `NorthEastern_Region`, `Top_50_Substations`, `Analytics_Dashboard`.

Columns on the master: `Region`, `State`, `Substation_Name`, `Type_AIS_GIS`, `Voltage_Level`, `Transformation_Capacity_MVA`, `Renewable_Companies_Connected`, `Project_Type`, `Total_Capacity_MW`, `Remarks`, `Data_Source`.

## Repository layout

```
Powergrid-India/
├── SKILL.md                         Skill workflow, schema, QA gates
├── references/
│   ├── substation-master.md         132-record baseline notes
│   ├── substations-a.csv            Baseline rows 1–66
│   ├── substations-b.csv            Baseline rows 67–132
│   └── generation-script.md         openpyxl builder reference
├── evals/                           Trigger and output eval cases
├── src/powergrid_india/             Runnable package
├── tests/                           Parser, reconcile, workbook tests
├── outputs/                         Local artefacts (gitignored)
├── LICENSE
├── SECURITY.md
└── pyproject.toml
```

This repository is a new public build. It is not linked to any private catalogue or private extractor repo.

## Use the baseline CLI (no live fetch)

This path does not call CTUIL, PGCIL, CEA, MNRE, or GEC. It builds the workbook from the embedded `substations-a.csv` + `substations-b.csv` baseline only. It is not a server and is not deployed as a web app.

Requires Python 3.10+ and `openpyxl`.

```bash
git clone https://github.com/d33pm3/Powergrid-India.git
cd Powergrid-India
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -e ".[dev]"
mkdir -p outputs
powergrid-india --output outputs/PAN_India_RE_Substations_Master_Data.xlsx
```

Equivalent module form:

```bash
python -m powergrid_india.cli --output outputs/PAN_India_RE_Substations_Master_Data.xlsx
```

## Run live research in an agent

Use this path when you need a refreshed workbook, not the frozen baseline.

1. Clone the repo (same commands as above, including `pip install -e ".[dev]"`).
2. Drop `SKILL.md` into the skill host (Claude Skills, Cursor, Grok custom skills, or equivalent).
3. Give the agent live web search and page-fetch. Point it at the five public URLs below.
4. The agent reconciles live hits against the 132-row baseline, tags `[SOURCE_LIVE]` or `[SOURCE_FALLBACK:BASELINE]`, then writes the same 10-sheet workbook under `outputs/`.

The CLI does not perform that live merge. Do not describe a baseline-only xlsx as a live-verified inventory.

## Tests

```bash
pytest -q
```

## Public sources (live-research targets)

- https://www.ctuil.in
- https://www.powergrid.in
- https://www.cea.nic.in
- https://www.mnre.gov.in
- https://www.powergrid.in/project/green-energy-corridor

## License

MIT. See `LICENSE`.

You may use this code; the xlsx is not a filing.
