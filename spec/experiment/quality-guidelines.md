# 实验质量门禁

## 1. 提交前最低要求
- 至少通过一次配置验证与计划生成：
  - `python scripts/run_experiment_plan.py --task <task-yaml>`
- 记录变更影响：任务范围、指标影响、是否破坏历史可比性。

## 2. 复现实验最低标准
- 每个任务 `n_repeats >= 5`
- 固定并记录 `seed_list`
- 统一预算策略（优先时间预算）

## 3. 失败处理
- 不允许吞异常；失败必须写入 `status=fail` 与 `error_message`
- 单次运行失败不能静默跳过，必须在结果中可见

## 4. 论文产出一致性
- 论文图表必须能映射到 `results/summary` 的具体文件与字段
- 任何“手工挑图”必须说明筛选规则

## 5. 门禁分级
- P0（阻断）：
  - 计划命令退出码必须为 `0`
  - 必须生成 `*_plan.json` 与 `*_plan.csv`
  - `plan 行数 = n_repeats * methods_count`
  - `plan.csv` 必含关键字段（`task_name/method/seed/split_seed/train_num/test_num/budget_time_seconds`）
- P1（警告）：
  - Runbook 命令与当前仓库状态不一致
  - 图表无法回链到结果产物

## 6. 最小 DoD
- 配置、脚本、文档三者一致
- 关键命令可执行
- 输出字段符合 `result-schema.md`
