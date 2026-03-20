# Task and Configuration Specification

## 1. Objectives
- All experiments must be configuration-driven to avoid scattering critical parameters across notebook code cells.
- The same task must keep fair budgets and consistent data splits across methods (`kan/gplearn/bms/qlattice`).

## 2. Configuration Hierarchy
- Base configuration: `configs/base.yaml`
- Task configuration: `configs/tasks/*.yaml`
- Merge rule: deep merge, with child config overriding parent config (consistent with `scripts/run_experiment_plan.py`).

## 3. Required Fields
- The top level must include: `reproducibility`, `experiment`, `methods`, `task`, `data`, `metrics`
- `methods.enabled` must be non-empty and may only contain `kan/gplearn/bms/qlattice`
- `experiment.n_repeats` must be a positive integer

## 4. Change Rules
- After changing any `configs/*.yaml`, the commit description must state: reason for change, affected tasks, and whether comparability is impacted.
- Adding extra budget to only one method without documentation is not allowed; method-specific exceptions, if necessary, must be written in `budget.per_method`.

## 5. Seed and Reproducibility
- Use `reproducibility.seed_list` by default; `n_repeats` should match the seed count or be explicitly expanded by scripts.
- New tasks must declare data ranges, sample size, and noise settings; implicit default values are not allowed.
