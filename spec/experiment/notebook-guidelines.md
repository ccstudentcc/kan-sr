# Notebook Specification

## 1. Role Definition
- Notebooks are for: exploratory analysis, visualization, and thesis figure generation.
- Training plan generation, batch execution, and result aggregation should be moved to `scripts/` (reusable and automatable).
- Notebook files must be placed under `notebooks/`; adding notebooks at the repository root is prohibited.

## 2. Structure Requirements
- Each notebook must start with: task objective, data source, core configuration, and random seed.
- Key output cells must be reproducible and must not depend on manual state.
- Writing sensitive paths or private API keys in cells is prohibited.
- Text in Markdown cells must be Chinese (for thesis writing and restatement).
- Comments, variable names, function names, and printed output in code cells must be English.

## 3. Result Consistency
- Chart metric names must be consistent with the protocol (for example, `mse`, `r2`).
- If notebook parameters differ from `configs/tasks/*.yaml`, the reason must be explicitly stated in the opening section.

## 4. Migration Principles
- Logic repeated across multiple notebooks (data generation, evaluation, plotting templates) should be extracted into scripts or modules.
- Logic that appears for the third time must be moved into the reusable code layer.
