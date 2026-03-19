# 可复现环境清单规范

## 1. 目标
- 为每次实验提供最小环境指纹，确保后续可复跑与对比。

## 2. 最小记录集
- Python 版本
- OS 与平台信息
- 关键库版本（`numpy`、`torch`、`scikit-learn`、`pyyaml`、`pykan` 等）
- 任务配置文件路径与哈希（建议）
- 执行时间与命令

## 3. 存储位置
- 建议：`results/env/<task_name>.json` 或 `results/env/<timestamp>.json`

## 4. 复跑验收
- 同配置同 seed 可生成同规模计划
- 指标波动应在可接受阈值内（按任务定义）
- 若波动异常，需记录可能原因（硬件、依赖、随机性实现差异）

