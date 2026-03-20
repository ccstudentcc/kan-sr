# 结果与产物治理

## 1. 输出目录约定
- 统一落盘到 `output/`，推荐结构：
  - `output/<timestamp>_plan.json`
  - `output/<timestamp>_plan.csv`
  - `output/raw/<task>/<method>.csv`
  - `output/summary/<task>.csv`
  - `output/env/<task>.json`
  - `output/config_snapshot/<timestamp>.yaml`
- 历史 `results/` 目录保留为 legacy 归档，不作为新增结果目录。

## 2. 最小字段
- 计划（plan）至少包含：`task_name`、`method`、`seed`、`split_seed`、`train_num`、`test_num`、`budget_time_seconds`
- 单轮（raw）至少包含：`task_name`、`method`、`seed`、`mse`、`r2`、`time_seconds`、`status`、`error_message`
- 汇总（summary）至少包含：`mse_mean/std`、`r2_mean/std`、`time_mean/std`、`success_rate`
- 环境（env）至少包含：`python_version`、`os`、`core_dependencies`

## 3. 模型资产管理
- `model/` 下历史快照视为“实验资产”，默认不重命名、不覆盖。
- 新增模型快照必须可追溯到任务名、方法名、配置版本。

## 4. 大文件策略
- `*.zip`、`*_state`、`*_cache_data` 等大文件仅在确有复现实验需求时新增。
- 新增大文件时，必须在提交说明注明用途和对应实验。

## 5. 可追溯性规则
- 每个关键图表必须可回链到：结果文件路径 + 生成命令 + 配置文件路径。
- 若无法回链，标记为“不可审计展示”，不能作为最终结论证据。
