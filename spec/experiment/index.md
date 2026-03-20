# 实验规范索引

适用范围：`configs/`、`scripts/`、`EXPERIMENT_PROTOCOL.md`、各实验 Notebook。  
状态定义：`Adopted`（已采用）、`Adopted with Gaps`（已执行但存在缺口）、`Draft`（待补齐实现）。

| 规范 | 文件 | 状态 | 说明 |
|---|---|---|---|
| 任务与配置规范 | `config-guidelines.md` | Adopted | 对齐 `configs/base.yaml` 与 `configs/tasks/*.yaml` |
| 执行契约 | `execution-contract.md` | Adopted with Gaps | 定义 plan/run/report 的输入输出与失败策略 |
| 任务与数据契约 | `task-data-contract.md` | Adopted with Gaps | 统一生成器、切分、噪声、seed 传递链 |
| 结果字段 Schema | `result-schema.md` | Adopted with Gaps | 统一 plan/raw/summary/env 字段真源 |
| 可执行 Runbook | `minimal-executable-runbook.md` | Adopted | 本地最小可执行流程与验收 |
| 可复现清单规范 | `reproducibility-manifest.md` | Draft | 环境记录与复跑验收门槛 |
| Notebook 规范 | `notebook-guidelines.md` | Draft | 统一探索与产出职责边界 |
| 结果与产物治理 | `result-governance.md` | Adopted with Gaps | 统一 `output/` 字段、快照与可追溯性 |
| 质量门禁 | `quality-guidelines.md` | Adopted | 运行前后检查、复现实验最低要求 |
| 目录结构规范 | `directory-structure.md` | Adopted | 当前仓库结构约束与演进规则 |

Owner: Project Maintainers  
Last Verified: 2026-03-19
