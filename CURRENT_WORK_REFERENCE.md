# KAN-Symbolic_Regression 现状与改进参考

> 目的：沉淀当前项目的可复用信息，明确“已有成果”和“可行创新点”，避免后续写作或答辩中被误解为仅复现/抄袭。

## 1. 项目来源与资产边界

- 本项目继承自已有仓库并在其基础上扩展。
- `*.pkl` 文件（如 `univariate_*.pkl`、`multivariate_*.pkl`）是历史训练产物，用于复现实验对比，不代表本轮新增创新。
- `model/` 目录中大量 `*_state` / `*_config.yml` / `*_cache_data` 也主要是历史实验快照。

结论：当前资产中“已有结果”与“新增贡献”必须在论文与答辩中显式区分。

## 2. 当前已有工作（按实验模块）

### 2.1 方法对比（单变量/多变量）

- 单变量对比：`Comparison_of_different_methods_for_SR_univariate.ipynb`
- 多变量对比：`Comparison_of_different_methods_for_SR_multivariate.ipynb`
- 对比方法：KAN / gplearn / BMS / QLattice
- 评估方式：可视化 + MSE / R2（绘图标签中给出）

### 2.2 应用实验

- 摆运动符号回归：`Pendulum_Motion.ipynb`
- 特殊函数（Si）拟合：`Special_function.ipynb`
- 无监督关系发现：`Unsupervised_Learning.ipynb`
- 查找表压缩（含奇异性讨论）：`Reducing_the_lookup_table_size.ipynb`
- EfficientKAN 可视化：`Plotting_Efficient_KAN.ipynb`

### 2.3 核心代码

- EfficientKAN 实现：`efficient_kan/kan.py`
- 导出接口：`efficient_kan/__init__.py`
- 环境核验脚本：`verify_install.py`

## 3. 现有工作的有效性（可写入论文）

1. 任务覆盖较完整：从合成函数到真实传感器数据，再到无监督关系发现与工程应用。
2. 部分任务具备“结构恢复”证据：
   - 摆运动中可恢复近似正弦结构。
   - 无监督实验中可恢复 `sin(6x)`、`exp(2x)` 与线性组合结构（近似系数）。
3. 特殊函数与查找表实验中已有明确数值结论（MSE 或误差变化趋势），不只是视觉对比。

## 4. 主要不足（必须主动承认）

1. 复现性控制不统一：部分 notebook 缺少统一 seed 与多次重复实验。
2. 统计稳健性不足：多数结论来自单次运行，缺少均值/方差/置信区间。
3. 公平比较协议不够完整：不同方法调参预算与搜索深度未严格对齐。
4. 评估维度偏少：目前以 MSE/R2 为主，缺少复杂度、外推能力、噪声鲁棒性等指标。
5. 工程化不足：以 notebook 为主，缺少统一脚本入口与自动化评测流水线。

## 5. 为避免“仅复现”的可行改进（优先级）

## P0（优先做，低风险高收益）

1. 建立统一实验协议（可复现基线）
- 统一数据划分、seed、训练步数、调参预算、硬件说明。
- 输出统一结果表：`mean ± std`（至少 5 次重复）。
- 交付物：`configs/` + `run_*.py` + `results/*.csv`。

2. 补齐公平对比
- 对 KAN / gplearn / BMS / QLattice 设定同等预算（搜索次数或时间预算）。
- 交付物：一份“公平性声明”与参数表（可直接入论文附录）。

3. 指标扩展
- 增加表达式复杂度（节点数/深度）、训练时长、推理时长、内存占用。
- 交付物：综合评分表（精度-复杂度-开销三维）。

## P1（体现研究增量，建议至少完成 1 项）

1. 符号化策略消融
- 比较 `auto_symbolic` 前后性能变化，分析何种网络宽度/深度下符号化收益为正。
- 交付物：消融图与结论规则（例如“小模型受益，大模型可能回退”）。

2. 奇异性区间鲁棒训练
- 在 `Reducing_the_lookup_table_size` 任务中系统扫描 `d_min`，加入重参数化或加权损失方案并对比。
- 交付物：方法改进曲线 + 理论解释（病态区间缓解效果）。

3. 噪声与外推评估
- 在单变量/多变量任务加入噪声强度扫描与 OOD 区间测试。
- 交付物：鲁棒性雷达图或曲线图。

## P2（可选加分）

1. 将核心流程脚本化并提供最小 CLI。
2. 为 `efficient_kan/kan.py` 增补单元测试与回归测试。
3. 增加失败案例库（何时 KAN 不适合）。

## 6. 建议的近期执行路线（两周可落地）

1. 第 1-2 天：确定统一协议与目录结构（seed、预算、数据切分）。
2. 第 3-6 天：跑完 P0 的多次重复实验并汇总表格。
3. 第 7-10 天：完成 1 个 P1（建议“符号化策略消融”或“奇异性区间鲁棒训练”）。
4. 第 11-14 天：整理图表与论文文本（方法、实验、威胁有效性、附录参数表）。

## 7. 论文中建议的“贡献表述模板”

可按以下结构陈述，避免被认为仅复现：

1. 我们复现并标准化了 KAN 与三类符号回归方法在统一协议下的对比基线。
2. 我们提出并验证了 **[你完成的改进项]**，在 **[任务]** 上带来 **[量化收益]**。
3. 我们补充了可复现资产（配置、脚本、统计汇总与失败案例），提升了该方向实验可验证性。

## 8. 本轮已落地更新（2026-03-19）

1. 新增统一实验协议文档：`EXPERIMENT_PROTOCOL.md`。
2. 新增统一配置骨架：
- `configs/base.yaml`
- `configs/tasks/univariate_quadratic.yaml`
- `configs/tasks/multivariate_sinexp.yaml`
3. 新增实验计划脚本：`scripts/run_experiment_plan.py`。
- 支持 `base + task` 配置深度合并。
- 支持 `--methods` 与 `--repeats` 覆盖。
- 自动输出可追溯计划文件（JSON/CSV）。
4. 新增结果目录占位：`results/.gitkeep`（用于后续 raw/summary 产物落盘）。

当前状态：已经具备“统一协议 + 统一配置 + 可执行计划生成”的最小可复现实验骨架，可在此基础上继续实现真实训练执行器与汇总统计。

## 9. 新增进展（2026-03-20）

1. 项目目录与规范体系重构完成：
- Notebook 已迁移到 `notebooks/`
- 输出目录统一为 `output/`
- 新增 `docs/`、`spec/` 规范体系并落地执行

2. 语言规范已工程化：
- `spec/` 文档统一英文
- `docs/` 主语言限定为中文
- 新增自动检查脚本：`scripts/checks/check_language_policy.py`

3. 实验流水线从“仅计划”升级为“计划 -> 原始结果 -> 汇总 + 环境清单”：
- 计划生成：`scripts/run_experiment_plan.py`
- 执行器：`scripts/run_experiment.py`（`kan`、`gplearn`、`bms`、`qlattice` 均已接入真实训练）
- 结果汇总：`scripts/summarize_results.py`
- 脚本分层：以上 3 个入口保持不变，核心实现已归类到 `scripts/experiment/` 子目录
  - `planning/`：实验计划生成
  - `execution/`：执行编排、适配器、I/O、运行时
  - `reporting/`：汇总与环境元数据输出
  - `shared/`：配置与常量复用
- 输出结构校验：`scripts/checks/check_output_schema.py`
- 覆盖一致性校验：`scripts/checks/check_plan_coverage.py`
- 时序新鲜度校验：`scripts/checks/check_pipeline_freshness.py`
- 结果可追溯校验：`scripts/checks/check_result_traceability.py`
- 改动-文档联动校验：`scripts/checks/check_required_updates.py`
- 一键检查入口：`scripts/run_checks.py`

4. 当前阶段性结论（用于论文表述）：
- 已具备可执行、可检查、可汇总的实验流水线骨架。
- 已具备 `output/env/<task>.json` 级别的运行环境与追溯元数据产物。
- 四条真实训练路径（`kan`、`gplearn`、`bms`、`qlattice`）均可执行。
- 下一步重点应转向“指标可信度验证 + 多任务批量复现实验 + 结果分析”。

## 11. 新增进展（2026-03-22）

1. `complexity` 指标统一口径：
- `scripts/run_experiment.py` 中四种方法全部改为按表达式 SymPy 节点数计算复杂度。
- 解析不安全或失败时返回 `1`，避免不同方法使用不一致的复杂度定义。

2. 已按最新重复次数配置重跑实验：
- `configs/base.yaml` 当前 `experiment.n_repeats: 1`
- 计划文件：`output/plan/20260322_175236_plan.json`（4 runs）
- raw 结果：`output/raw/univariate_quadratic/{kan,gplearn,bms,qlattice}.csv`

3. 当前校验状态：
- `check_language_policy`、`check_output_schema`、`check_doc_sync`、`check_pipeline_freshness`、`check_plan_coverage`、`check_result_traceability` 已通过
- `run_checks.py` 中仅 `check_required_updates` 依赖文档同步；本次更新即用于满足该门禁

## 12. 脚本优化进展（2026-03-22）

1. 入口兼容性修复：
- `scripts/run_experiment.py`、`scripts/run_experiment_plan.py`、`scripts/summarize_results.py` 已支持三种调用方式：
  - `python scripts/<entry>.py`
  - `python -m scripts.<entry_module>`
  - `import scripts.<entry_module>`

2. 契约与工具去重：
- 新增 `scripts/experiment/shared/contracts.py` 作为 plan/raw/summary/env 字段契约的统一来源。
- `scripts/experiment/execution/io.py` 与 `scripts/experiment/reporting/summarizer.py` 改为引用共享契约。
- 新增 `scripts/checks/common.py`，统一 `latest_plan_json` 逻辑，去除 `check_output_schema`、`check_pipeline_freshness`、`check_plan_coverage` 的重复实现。

3. 执行器可维护性优化：
- `scripts/experiment/execution/adapters.py` 新增方法注册表，执行分发改为注册表模式。
- `scripts/experiment/execution/app.py` 的 `execute_row` 逻辑拆为多个小函数，降低复杂度与修改风险。

4. 检查脚本复杂函数拆分：
- `scripts/checks/check_output_schema.py` 将 `validate_env_json` 拆分为身份、运行时、方法、原始文件四类校验函数。

## 10. 证据链最小复现命令（Traceability）

```bash
python scripts/run_experiment_plan.py --base-config configs/base.yaml --task-config configs/tasks/univariate_quadratic.yaml --output-root output
python scripts/run_experiment.py --plan-json output/plan/<timestamp>_plan.json --output-root output
python scripts/summarize_results.py --output-root output
python scripts/checks/check_language_policy.py
python scripts/checks/check_output_schema.py --output-root output --allow-placeholder
python scripts/checks/check_doc_sync.py
python scripts/checks/check_pipeline_freshness.py --output-root output
python scripts/checks/check_plan_coverage.py --output-root output
python scripts/checks/check_result_traceability.py
python scripts/checks/check_required_updates.py
python scripts/run_checks.py --output-root output --allow-placeholder
```

关键产物路径：
- `output/plan/<timestamp>_plan.json`
- `output/plan/<timestamp>_plan.csv`
- `output/raw/<task>/<method>.csv`
- `output/summary/<task>.csv`
- `output/env/<task>.json`

---

最后更新：2026-03-22
