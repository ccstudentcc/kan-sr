# Repository File Management Specification

## 1. Target Directory Structure
- `docs/`: project documentation outside formal specs
- `notebooks/`: all experiment and analysis notebooks
- `scripts/`: reusable command-line entry scripts
- `configs/`: experiment parameters and protocol configs
- `output/`: plans, raw results, summaries, environment manifests
- `raw/`: raw collected data (irreversible experiment inputs)
- `model/`: model snapshots and cache assets
- `spec/`: engineering and experiment specifications

## 2. Placement Rules
- New notebooks must be placed in `notebooks/` only, never at repository root.
- New result artifacts must be placed in `output/` only, never scattered in root or `docs/`.
- General documents go to `docs/`; specification documents go to `spec/`.

## 3. Naming Rules
- Notebook: `<topic>_<goal>.ipynb` (for example, `pendulum_symbolic_regression.ipynb`)
- Output file: `<timestamp>_<task>_<artifact>.<ext>`
- Script: verb-first naming (for example, `run_*.py`, `check_*.py`)

## 4. Migration Strategy (Current Repo Compatible)
- Keep no `*.ipynb` files in root; notebooks are unified under `notebooks/`.
- `results/` is treated as a legacy results directory; historical files are not forced to migrate immediately.
- New workflows must use `output/`; keep `results/` as read-only archive if needed.

## 5. Prohibited Actions
- Do not add one-off outputs or temporary files in the repository root.
- Do not place experiment results in `docs/` or `spec/`.
