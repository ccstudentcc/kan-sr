# 实验执行契约

## 1. 生命周期
`plan -> run -> evaluate -> aggregate -> persist`

当前实现状态：
- `plan`：已实现（`scripts/run_experiment_plan.py`）
- `run/evaluate/aggregate/persist`：规范已定义，待统一执行器落地

## 2. 输入契约
- 输入1：`configs/base.yaml`
- 输入2：`configs/tasks/<task>.yaml`
- 输入3：CLI 覆盖参数（`--methods`、`--repeats`、`--out-dir`）

## 3. 输出契约
- `plan` 阶段输出：`*_plan.json`、`*_plan.csv`
- 后续阶段目标输出：`raw/*.csv`、`summary/*.csv`、`env/*.json`

## 4. 失败策略
- 配置结构错误：立即失败（fail fast）
- 单方法单 seed 失败：必须可见，写入 `status=fail` 与 `error_message`
- 不允许静默跳过失败项

## 5. 审计要求
- 每次运行应记录：任务、方法、seed、预算、时间戳
- 结果应可回链到配置快照与运行命令

