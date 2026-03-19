# 统一实验协议（模板）

本文档定义 KAN 符号回归项目的统一实验协议，用于保证：
- 可复现（同一配置可重复得到统计一致结果）
- 公平比较（不同方法在统一预算下对比）
- 结果可审计（输出字段固定且可追溯）

对应配置文件：
- `configs/base.yaml`
- `configs/tasks/univariate_quadratic.yaml`
- `configs/tasks/multivariate_sinexp.yaml`

## 1. 适用方法

统一方法名（必须与配置一致）：
- `kan`
- `gplearn`
- `bms`
- `qlattice`

## 2. 可复现原则

## 2.1 seed 规则

- 每次运行必须记录 `seed`。
- 全局随机源统一设置：`python random`、`numpy`、`torch`。
- 多次重复实验使用 `seed_list`，例如 `[42, 43, 44, 45, 46]`。

## 2.2 数据划分规则

- 每个任务显式声明：训练集/测试集规模、输入范围、噪声。
- 不允许不同方法使用不同数据划分。
- 训练集与测试集由同一个 seed 控制，且每轮重复保持一致。

## 2.3 预算规则（公平比较核心）

- 每个方法使用同等预算维度之一：
  - 固定训练时间上限（`time_budget_seconds`），或
  - 固定迭代预算（`fit_steps` / `generations` / `epochs`）。
- 不允许只对单一方法进行额外调参而不记录。
- 若方法需要分阶段训练（如 `kan` 的 `LBFGS + Adam`），需在配置中完整声明。

## 2.4 重复次数与统计

- 最少重复次数：`n_repeats >= 5`。
- 汇总指标必须输出：`mean`、`std`。
- 推荐附加：`median`、`min`、`max`。

## 3. 输出字段规范

每次单轮运行（per-run）至少输出：
- `task_name`
- `method`
- `seed`
- `train_size`
- `test_size`
- `time_seconds`
- `mse`
- `r2`
- `expression`（若可导出）
- `complexity`（若可计算，如节点数/深度）
- `status`（success / fail）
- `error_message`（失败时必填）

每个方法聚合输出（summary）至少包含：
- `task_name`
- `method`
- `n_repeats`
- `mse_mean`
- `mse_std`
- `r2_mean`
- `r2_std`
- `time_mean`
- `time_std`
- `success_rate`

## 4. 目录与产物建议

建议运行产物结构：
- `results/raw/<task_name>/<method>.csv`（逐次结果）
- `results/summary/<task_name>.csv`（方法聚合结果）
- `results/config_snapshot/<timestamp>.yaml`（配置快照）

## 5. 执行流程（建议）

1. 读取 `configs/base.yaml`。
2. 读取任务配置（`configs/tasks/*.yaml`）并深度合并。
3. 依次运行 `methods.enabled` 中的方法。
4. 按 `seed_list` 重复。
5. 写出 raw 与 summary。
6. 记录环境信息（Python、关键库版本、硬件）。

## 6. 合规检查清单（提交前）

- 是否记录了全部 seed？
- 是否所有方法使用同一数据划分？
- 是否预算一致且有据可查？
- 是否达到最小重复次数？
- 是否输出了规定字段？

---

最后更新：2026-03-19
