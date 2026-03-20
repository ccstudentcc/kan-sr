# Experiment Quality Gates

## 1. Minimum Requirements Before Commit
- At least one configuration validation and plan generation must pass:
  - `python scripts/run_experiment_plan.py --task <task-yaml>`
- Record change impact: task scope, metric impact, and whether historical comparability is broken.

## 2. Minimum Reproducibility Standard
- For each task, `n_repeats >= 5`
- `seed_list` must be fixed and recorded
- Budget strategy must be unified (time budget preferred)

## 3. Failure Handling
- Exception swallowing is not allowed; failures must be written with `status=fail` and `error_message`
- A failed single run must not be skipped silently and must be visible in results

## 4. Consistency with Thesis Deliverables
- Thesis figures must map to specific files and fields under `output/summary`
- Any manual figure selection must include explicit selection rules

## 5. Gate Severity Levels
- P0 (blocking):
  - Plan command exit code must be `0`
  - `*_plan.json` and `*_plan.csv` must be generated
  - `plan row count = n_repeats * methods_count`
  - `plan.csv` must include key fields (`task_name/method/seed/split_seed/train_num/test_num/budget_time_seconds`)
- P1 (warning):
  - Runbook commands are inconsistent with the current repository state
  - Figures cannot be traced back to result artifacts

## 6. Minimum DoD
- Configuration, scripts, and documentation are consistent
- Key commands are executable
- Output fields conform to `result-schema.md`
