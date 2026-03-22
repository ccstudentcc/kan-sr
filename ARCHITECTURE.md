# Architecture Overview

## Purpose
This repository provides a reproducible symbolic-regression workflow with a strict artifact contract:
`plan -> run -> summarize -> checks`.

## Top-Level Components
- `configs/`: Base and task-specific experiment configuration.
- `scripts/experiment/`: Pipeline implementation modules.
- `scripts/checks/`: Validation gates for schema, freshness, coverage, and doc sync.
- `scripts/run_*.py` and `scripts/summarize_results.py`: Stable CLI entrypoints.
- `output/`: Runtime artifacts (`plan`, `raw`, `summary`, `env`).
- `spec/`: Protocol, workflow, and quality contracts.

## Scripts Subsystem
### Entry Layer
- `scripts/run_experiment_plan.py`
- `scripts/run_experiment.py`
- `scripts/summarize_results.py`
- `scripts/run_checks.py`

These files are thin entrypoints and should remain backward-compatible.

### Experiment Layer
- `scripts/experiment/planning/plan_builder.py`: Build run plans from merged config.
- `scripts/experiment/execution/app.py`: Orchestrate plan-row execution.
- `scripts/experiment/execution/runtime.py`: Task config resolution, dataset generation, runtime param normalization.
- `scripts/experiment/execution/adapters.py`: Method adapters (`kan`, `gplearn`, `bms`, `qlattice`).
- `scripts/experiment/execution/io.py`: Plan/raw I/O and fail-row normalization.
- `scripts/experiment/reporting/summarizer.py`: Aggregate raw artifacts to summary/env.
- `scripts/experiment/shared/`: Shared constants, config utilities, and artifact contracts.

### Checks Layer
- `scripts/checks/check_*.py`: Independent validation gates.
- `scripts/checks/common.py`: Shared helpers for check scripts.

## Data Flow
1. `plan_builder` merges `configs/base.yaml` + task config and writes `output/plan/*`.
2. `execution/app` loads one plan and writes grouped raw files to `output/raw/<task>/<method>.csv`.
3. `reporting/summarizer` aggregates raw files into:
   - `output/summary/<task>.csv`
   - `output/env/<task>.json`
4. `run_checks` executes all gates and fails fast on any contract violation.

## Module Boundaries
- `planning` must not depend on `execution` internals.
- `reporting` consumes only raw artifact contract, not adapter internals.
- `checks` validate contracts but do not mutate runtime artifacts.
- Shared contracts live in `scripts/experiment/shared/contracts.py` and should be the single source of truth for artifact fields.
