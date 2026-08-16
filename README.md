# Weighted Scoring Toolkit (C)

A small C command-line toolkit for weighted-average scoring across three
scenarios, all built on one shared, reusable scoring function instead of
copy-pasted logic per use case.

## What it does

| Mode | Input fields | Weights | Output |
|---|---|---|---|
| 1. Employee performance | Productivity, Attendance, Teamwork | 0.5 / 0.3 / 0.2 | Weighted score per employee + top performer |
| 2. Weather severity | Temperature, Humidity, Wind Speed | 0.4 / 0.3 / 0.3 | Weighted score per city + most extreme (highest wind speed) |
| 3. Scholarship eligibility | Math, Science, English | 0.5 / 0.3 / 0.2 | Students scoring above the 90-point cutoff |

## Design

Each scenario originally used its own near-duplicate function for reading
input and computing a weighted average. This version consolidates that into:

- `weighted_average()` — the actual math, shared by all three modes.
- `collect_and_score()` — reads n records, scores them, and tracks the
  top record. It can rank by the blended weighted score (employees,
  students) or by a single raw field (weather, where "most extreme" means
  highest wind speed specifically, not the blended average).
- A `Record` struct to hold each entry's fields and score, and basic
  bounds checking on the record count (1–50) instead of trusting raw input.

## Build & run

```bash
gcc -Wall -o weighted_scoring weighted_scoring.c
./weighted_scoring
```

You'll be prompted to choose a mode (1–3), then enter the number of records
and their field values.

### Example: Employee performance evaluation

```
Choose a mode (1-3): 1
Enter number of employees: 3
Enter Employee 1 - Productivity: 85
Enter Employee 1 - Attendance: 90
Enter Employee 1 - Teamwork: 95
...
--- Results ---
Employee 1 - Weighted Score: 88.50
Employee 2 - Weighted Score: 69.00
Employee 3 - Weighted Score: 90.60

Top-Performing Employee: Employee 3 (Score: 90.60)
```

## Notes / possible extensions

- Weights and the eligibility cutoff are currently hard-coded per mode;
  a natural next step is loading them from a config file or CLI flags.
- Input is unvalidated beyond the record-count bounds check — production
  use would want to reject non-numeric or out-of-range field values.
