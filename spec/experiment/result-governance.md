# Result and Artifact Governance

## 1. Output Directory Convention
- All outputs must be written to `output/`, with the recommended structure:
  - `output/<timestamp>_plan.json`
  - `output/<timestamp>_plan.csv`
  - `output/raw/<task>/<method>.csv`
  - `output/summary/<task>.csv`
  - `output/env/<task>.json`
  - `output/config_snapshot/<timestamp>.yaml`
- The historical `results/` directory is retained as a legacy archive and must not be used for new results.

## 2. Minimum Fields
- Plan must include at least: `task_name`, `method`, `seed`, `split_seed`, `train_num`, `test_num`, `budget_time_seconds`
- Single run raw output must include at least: `task_name`, `method`, `seed`, `mse`, `r2`, `time_seconds`, `status`, `error_message`
- Summary must include at least: `mse_mean/std`, `r2_mean/std`, `time_mean/std`, `success_rate`
- Environment must include at least: `python_version`, `os`, `core_dependencies`

## 3. Model Asset Management
- Historical snapshots under `model/` are treated as experimental assets and must not be renamed or overwritten by default.
- New model snapshots must be traceable to task name, method name, and configuration version.

## 4. Large File Policy
- Large files such as `*.zip`, `*_state`, and `*_cache_data` may be added only when there is a real reproducibility need.
- When adding large files, the commit description must state their purpose and the corresponding experiment.

## 5. Traceability Rules
- Every key figure must be traceable back to: result file path + generation command + configuration file path.
- If traceability is missing, it must be marked as an "unauditable presentation" and cannot be used as final evidence.
