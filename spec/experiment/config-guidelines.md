# 任务与配置规范

## 1. 目标
- 所有实验必须由配置驱动，避免把关键参数散落在 Notebook 代码单元中。
- 同一任务在不同方法（`kan/gplearn/bms/qlattice`）间保持公平预算与一致数据划分。

## 2. 配置层级
- 基线配置：`configs/base.yaml`
- 任务配置：`configs/tasks/*.yaml`
- 合并规则：深度合并，子配置覆盖父配置（与 `scripts/run_experiment_plan.py` 一致）。

## 3. 必填字段
- 顶层必须包含：`reproducibility`、`experiment`、`methods`、`task`、`data`、`metrics`
- `methods.enabled` 必须非空，且只允许 `kan/gplearn/bms/qlattice`
- `experiment.n_repeats` 必须为正整数

## 4. 变更规则
- 修改任何 `configs/*.yaml` 后，必须在提交说明中写清：变更原因、影响任务、是否影响可比性。
- 不允许只给单一方法增加额外预算而不记录；若确需方法特例，必须写入 `budget.per_method`。

## 5. Seed 与复现
- 默认使用 `reproducibility.seed_list`；`n_repeats` 应与种子数一致或由脚本显式扩展。
- 新任务必须声明数据范围、样本规模、噪声设置，不允许“隐式默认值”。

