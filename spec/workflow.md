# Standard Execution Workflow

## 1. Requirement Clarification
- Define the task goal clearly: method improvement, protocol completion, result reproduction, or documentation output.
- Mark the impact scope: `configs/`, `scripts/`, `efficient_kan/`, `notebooks/`, `output/`.

## 2. Solution Design
- Prioritize minimum viable changes and avoid unnecessary cross-layer refactoring.
- If fairness is impacted, update protocol and configs before changing code.

## 3. Implementation Order
1. Update configuration (`configs/base.yaml` or `configs/tasks/*.yaml`)
2. Update execution scripts (`scripts/`)
3. Update model implementation if required (`efficient_kan/`)
4. Update notebook presentation and `spec/` documents last

## 4. Run and Validation
- Minimum validation command: `python scripts/run_experiment_plan.py --task <task-yaml>`
- Pass criteria: plan files are generated stably, fields are complete, and failures are visible.

## 5. Result Consolidation
- Save reproducible experiment outputs to `output/`.
- Write key conclusions back to `CURRENT_WORK_REFERENCE.md` or thesis figure/source notes.

## 6. Pre-Commit Synchronization
- Update relevant specification files (at least in `spec/experiment/*` or `spec/core/*`).
- In commit messages, include WHY and impact boundaries.

## 7. Language Compliance Check
- Code comments and docstrings: English (Google style).
- Print and logging outputs: English.
- Notebook markdown: Chinese.
- `spec/` documents: English-only.
- `docs/` documents: primarily Chinese.
- Run checker: `python scripts/check_language_policy.py`
