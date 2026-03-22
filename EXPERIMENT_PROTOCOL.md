# 统一实验协议（Protocol v1）

本文档定义 KAN 符号回归项目的统一实验协议，目标是：
- 可复现：同配置可重复生成一致实验计划
- 公平比较：方法在统一预算与数据规则下对比
- 可审计：结果字段与产物路径可追踪

关联规范：
- `spec/experiment/index.md`
- `spec/experiment/result-schema.md`
- `spec/experiment/execution-contract.md`

## 1. 协议分层

### 1.1 Plan 阶段（已实现）
- 实现入口：`scripts/run_experiment_plan.py`
- 结构说明：入口脚本为兼容层，核心实现位于 `scripts/experiment/planning/plan_builder.py`
- 作用：读取 `base + task` 配置并生成运行计划
- 产物：`output/plan/*_plan.json`、`output/plan/*_plan.csv`

### 1.2 Run 阶段（已实现真实执行）
- 实现入口：`scripts/run_experiment.py`
- 结构说明：入口脚本为兼容层，核心实现位于 `scripts/experiment/execution/app.py`
- 执行内部模块：
  - 运行时与数据生成：`scripts/experiment/execution/runtime.py`
  - 方法适配器：`scripts/experiment/execution/adapters.py`
  - 计划/结果 I/O：`scripts/experiment/execution/io.py`
  - 运行时模型：`scripts/experiment/execution/models.py`
- 作用：按计划逐行执行方法适配器并输出 raw 结果
- 产物：`output/raw/<task>/<method>.csv`
- 当前状态：`kan`、`gplearn`、`bms`、`qlattice` 均为真实训练与评估路径

### 1.3 Report 阶段（已实现 summary + env）
- 实现入口：`scripts/summarize_results.py`
- 结构说明：入口脚本为兼容层，核心实现位于 `scripts/experiment/reporting/summarizer.py`
- 作用：按任务聚合 `raw` 结果并输出方法级统计
- 已实现产物：`output/summary/<task>.csv`
- 已实现产物：`output/env/<task>.json`

### 1.4 Shared 公共层
- 配置读写与深合并：`scripts/experiment/shared/config.py`
- 跨阶段常量：`scripts/experiment/shared/constants.py`

## 2. 适用方法
- `kan`
- `gplearn`
- `bms`
- `qlattice`

## 3. 可复现原则

### 3.1 Seed 规则
- 每次运行必须记录 `seed`
- 建议 `seed_list` 与 `n_repeats` 对齐
- 随机源建议统一控制：`python random`、`numpy`、`torch`

### 3.2 数据与切分规则
- 任务必须显式声明数据规模、范围、噪声配置
- 方法间使用统一切分策略与相同 seed 传递链

### 3.3 预算规则
- 优先使用统一时间预算 `time_budget_seconds`
- 方法私有预算通过 `budget.per_method` 映射，不允许隐式加码

## 4. 字段契约

### 4.1 Plan 字段（当前生效）
- `task_name`、`method`、`seed`、`split_seed`
- `train_num`、`test_num`
- `budget_time_seconds`

### 4.2 Run/Report 字段（目标）
- raw：`mse`、`r2`、`time_seconds`、`expression`、`complexity`、`status`、`error_message`
- summary：`mse_mean/std`、`r2_mean/std`、`time_mean/std`、`success_rate`
- env：`schema_version`、`task_name`、`run_id`、`run_ids`、`generated_at_utc`、`python_version`、`platform`、`is_simulated`、`methods`、`n_methods`、`raw_files`

### 4.3 complexity 口径（当前生效）
- 统一定义：`complexity = SymPy 解析后表达式语法树节点总数`
- 安全与容错：表达式不安全或无法解析时返回 `1`
- 适用范围：`kan`、`gplearn`、`bms`、`qlattice` 全部使用同一口径

## 5. 命名统一
- 协议统一使用 `train_num/test_num`
- 若出现 `train_size/test_size`，视为同义映射，禁止并行混用

## 6. 合规检查清单
- 配置可解析
- 计划可生成
- 行数满足 `n_repeats * method_count`
- 字段完整且命名一致
- 失败可见，不允许静默跳过
- `python scripts/checks/check_language_policy.py` 通过
- `python scripts/checks/check_output_schema.py --output-root output` 通过
- `python scripts/checks/check_doc_sync.py` 通过
- `python scripts/checks/check_pipeline_freshness.py --output-root output` 通过
- `python scripts/checks/check_plan_coverage.py --output-root output` 通过
- `python scripts/checks/check_result_traceability.py` 通过
- `python scripts/checks/check_required_updates.py` 通过
- `output/env/<task>.json` 存在且与 summary 任务一一对应
- `python scripts/run_checks.py --output-root output` 通过

## 7. 目录规范说明
- 结果目录统一为 `output/`
- 历史 `results/` 目录视为 legacy 资产，迁移前保持只读，避免破坏可追溯性

---
最后更新：2026-03-22
