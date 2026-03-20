# Experiment Directory Structure Specification

## 1. Current Layered Structure
- `configs/`: experiment protocol and task parameters
- `scripts/`: reusable execution entry points (non-interactive)
- `output/`: plan and evaluation artifacts (standard directory)
- `results/`: historical artifacts (legacy, read-only archive)
- `notebooks/`: experiment and analysis notebooks (standard directory)
- `docs/`: project documentation (non-spec)
- `raw/`: raw sensor data
- `model/`: model snapshots and cache assets

## 2. Rules for Placing New Files
- New task parameters go to `configs/tasks/<task>.yaml`
- New batch workflows go to `scripts/`
- New evaluation data goes to `output/`, not the repository root
- New notebooks go to `notebooks/`
- General documentation goes to `docs/`, specification documents go to `spec/`
- Image assets must be placed under `img/`

## 3. Prohibitions
- Do not scatter one-off experiment scripts in the repository root
- Do not commit temporary outputs unrelated to tasks
