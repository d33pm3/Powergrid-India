# Generation Script Reference

The runnable implementation lives in `src/powergrid_india/`:

- `parser.py` — `parse_master_table()`
- `reconcile.py` — `norm_key()`, `coerce_mw()`, `reconcile()`
- `workbook.py` — `build_workbook_data()`, `write_data_sheet()`, `write_dashboard()`, `create_workbook()`
- `cli.py` — `python -m powergrid_india.cli`

Do not hand-assemble sheet JSON. Always derive the 9 datasets from reconciled records.

## Invocation

```python
from powergrid_india import parse_master_table, reconcile, create_workbook

records = reconcile(parse_master_table(), live_updates)
create_workbook(
    master_records=records,
    source_log=source_log,
    output_path="outputs/PAN_India_RE_Substations.xlsx",
)
```

```bash
python -m powergrid_india.cli --output outputs/PAN_India_RE_Substations_Master_Data.xlsx
```

## Colour palette

| Token | Hex | Use |
|-------|-----|-----|
| H_GREEN | `2E7D32` | Data-sheet headers |
| H_BLUE | `1C3A6B` | Dashboard block headers |
| H_TEAL | `00695C` | Dashboard sub-headers |
| H_AMBER | `E65100` | Planned / warning rows |
| H_GREY | `F5F5F5` | Alternate data rows |

## Sheet order (10)

1. All_Substations
2. Regional_Summary
3. State_Summary
4. Western_Region
5. Northern_Region
6. Southern_Region
7. Eastern_Region
8. NorthEastern_Region
9. Top_50_Substations
10. Analytics_Dashboard (8 blocks + epistemic caveat)

## Implementation notes (v2.1.2)

- Voltage tiers are exclusive: `400/220 kV` is not counted as `220 kV`.
- BESS/PSP filter matches `BESS`, `Pump Storage`, or `PSP` only (not Hydro-Solar).
- Name keys collapse `PS` tokens, hyphen/space runs, and roman suffixes I-V.
- MW values are coerced to int before aggregation and sort.
- Dashboard Block 8 includes the planning-grade baseline caveat.
- Checkpoints and workbooks write to `outputs/` (gitignored).
