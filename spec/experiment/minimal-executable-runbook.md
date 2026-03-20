# 最小可执行 Runbook

## 1. 目标与范围
- 目标：保证项目在当前阶段至少具备“可复现计划生成”能力。
- 范围：仅覆盖 `plan` 生成，不覆盖完整训练执行器。

## 2. 前置条件
- Python 环境可用
- 依赖安装完成（参考 `requirements.txt`）
- 在仓库根目录执行命令（Windows + pwsh）

## 3. 标准输入
- 全局配置：`configs/base.yaml`
- 任务配置：`configs/tasks/univariate_quadratic.yaml` 或 `configs/tasks/multivariate_sinexp.yaml`

## 4. 标准命令
```powershell
python scripts\run_experiment_plan.py --task configs\tasks\univariate_quadratic.yaml --out-dir output
python scripts\run_experiment_plan.py --task configs\tasks\multivariate_sinexp.yaml --out-dir output
```

## 5. 预期产物
- `output/<timestamp>_plan.json`
- `output/<timestamp>_plan.csv`

## 6. 快速验收
- 退出码为 `0`
- `plan.csv` 行数应满足：`n_repeats * methods.enabled_count`
- 以默认配置为例：`5 * 4 = 20`

## 7. 常见失败与处理
- 配置缺失字段：补齐 `reproducibility/experiment/methods/task/data/metrics`
- 方法名非法：只允许 `kan/gplearn/bms/qlattice`
- 重复次数非法：`experiment.n_repeats` 必须为正整数
