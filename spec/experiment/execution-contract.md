# Experiment Execution Contract

## 1. Lifecycle
`plan -> run -> evaluate -> aggregate -> persist`

Current implementation status:
- `plan`: implemented (`scripts/run_experiment_plan.py`)
- `run/evaluate/aggregate/persist`: specification defined, unified executor pending implementation

## 2. Input Contract
- Input 1: `configs/base.yaml`
- Input 2: `configs/tasks/<task>.yaml`
- Input 3: CLI override parameters (`--methods`, `--repeats`, `--out-dir`)

## 3. Output Contract
- `plan` stage outputs: `*_plan.json`, `*_plan.csv`
- Target outputs for later stages: `output/raw/*.csv`, `output/summary/*.csv`, `output/env/*.json`

## 4. Failure Strategy
- Invalid config structure: fail fast
- Failure of one method with one seed: must be visible and written with `status=fail` and `error_message`
- Silent skipping of failed items is not allowed

## 5. Audit Requirements
- Each run should record: task, method, seed, budget, and timestamp
- Results should be traceable to the config snapshot and execution command
