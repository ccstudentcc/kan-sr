# Minimal Executable Runbook

## 1. Goal and Scope
- Goal: ensure the project currently has at least reproducible plan-generation capability.
- Scope: only covers `plan` generation, not the full training executor.

## 2. Prerequisites
- Python environment is available
- Dependencies are installed (see `requirements.txt`)
- Run commands from the repository root (Windows + pwsh)

## 3. Standard Inputs
- Global configuration: `configs/base.yaml`
- Task configuration: `configs/tasks/univariate_quadratic.yaml` or `configs/tasks/multivariate_sinexp.yaml`

## 4. Standard Commands
```powershell
python scripts\run_experiment_plan.py --task configs\tasks\univariate_quadratic.yaml --out-dir output
python scripts\run_experiment_plan.py --task configs\tasks\multivariate_sinexp.yaml --out-dir output
```

## 5. Expected Artifacts
- `output/<timestamp>_plan.json`
- `output/<timestamp>_plan.csv`

## 6. Quick Acceptance
- Exit code is `0`
- `plan.csv` row count should satisfy: `n_repeats * methods.enabled_count`
- Using default config as an example: `5 * 4 = 20`

## 7. Common Failures and Handling
- Missing required config fields: fill in `reproducibility/experiment/methods/task/data/metrics`
- Invalid method name: only `kan/gplearn/bms/qlattice` are allowed
- Invalid repeat count: `experiment.n_repeats` must be a positive integer
