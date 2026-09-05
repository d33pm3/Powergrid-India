# Powergrid-India

Public RegTech skill and workbook builder for **PAN India renewable-energy evacuation substations** on the CTU / PGCIL grid.

Canonical source: `https://github.com/d33pm3/Powergrid-India`

The 132-record baseline is **planning-grade**, compiled from public reporting. Capacity, MVA, and developer-allocation figures are indicative. Rows that are not confirmed against a live source in the current session must be tagged `[SOURCE_FALLBACK:BASELINE]` and must not be described as verified regulatory filings.

## What it does

- Loads a 132-substation master (5 regions, 30 states, ~130,500 MW baseline)
- Optionally merges live updates from public CTUIL / PGCIL / CEA / MNRE / GEC sources
- Builds a 10-sheet `.xlsx` workbook (9 data sheets + an 8-block Analytics Dashboard)

## Repository layout

```
Powergrid-India/
├── SKILL.md                         Skill workflow, schema, QA gates
├── references/
│   ├── substation-master.md         132-record baseline tables
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

## Install

```bash
python -m pip install -e ".[dev]"
```

Requires Python 3.10+ and `openpyxl`.

## Build the baseline workbook

```bash
python -m powergrid_india.cli --output outputs/PAN_India_RE_Substations_Master_Data.xlsx
```

The CLI path uses the embedded baseline only. Live research against public portals is specified in `SKILL.md` and is expected when an agent builds a refreshed workbook.

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
