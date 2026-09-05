# Substation Master Reference — 132 Records

Machine-readable baseline (planning-grade):

- [`substations-a.csv`](substations-a.csv) — rows 1–66
- [`substations-b.csv`](substations-b.csv) — rows 67–132

`parse_master_table()` concatenates both parts (132 unique rows, 130,500 MW).

Not a verified regulatory filing. After live research, `reconcile()` adds `Data_Source`.

| Dimension | Baseline |
|-----------|----------|
| Substations | 132 |
| Capacity | 130,500 MW |
| Regions | WR 54 / 76,550 MW; SR 36 / 31,480 MW; NR 18 / 17,800 MW; ER 16 / 4,000 MW; NER 8 / 670 MW |
| States / UTs | 30 |
| Voltage | 21 × 765/400 kV; 104 × 400/220 kV; 6 × 220 kV; 1 × 132 kV |
| BESS / PSP nodes | 9 |
| GEC-tagged nodes | 7 |
