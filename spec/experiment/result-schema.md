# 结果字段 Schema（单一真源）

## 1. 版本
- Schema Version: `v1`
- 生效范围：`plan`、`raw`、`summary`、`env`

## 2. plan 字段（当前已实现）
必填字段：
- `task_name`（string）
- `method`（string）
- `seed`（int）
- `split_seed`（int）
- `train_num`（int or empty）
- `test_num`（int or empty）
- `budget_time_seconds`（number or empty）
- `status`（后续 run 阶段补充）

## 3. raw 字段（目标）
必填字段：
- `task_name`、`method`、`seed`
- `mse`、`r2`、`time_seconds`
- `expression`、`complexity`
- `status`、`error_message`

## 4. summary 字段（目标）
必填字段：
- `task_name`、`method`、`n_repeats`
- `mse_mean/std`、`r2_mean/std`
- `time_mean/std`、`success_rate`

## 5. 命名统一规则
- 当前配置使用 `train_num/test_num`；若外部文档出现 `train_size/test_size`，应视为同义映射。
- 仓库内新规范统一采用 `train_num/test_num`。

## 6. 兼容与变更
- 新增字段应保持向后兼容（默认可空）
- 删除或重命名字段属于破坏性变更，必须更新协议并记录迁移说明

