# Cross-Layer Thinking Guide

## 1. Unified Chain
Any experiment change must answer these 5 questions:
1. Protocol layer: does it affect fairness/reproducibility?
2. Configuration layer: is the parameter change auditable?
3. Execution layer: can scripts run it reliably?
4. Result layer: is it persisted using unified fields?
5. Narrative layer: can it map to thesis/defense conclusions?

## 2. Common Disconnects
- Only changing notebooks without changing config: batch reproducibility is impossible
- Only changing models without changing protocol: comparisons become unfair
- Only showing figures without keeping result files: unauditable

## 3. Recommended Workflow
- First update `configs/tasks/*.yaml`
- Then run `scripts/run_experiment_plan.py`
- Finally update notebook presentations and conclusion text
