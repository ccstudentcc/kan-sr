# 标准执行流程（Workflow）

## 1. 需求澄清
- 明确任务目标：方法改进、协议补齐、结果复现或文档输出。
- 标注影响范围：`configs/`、`scripts/`、`efficient_kan/`、Notebook、`results/`。

## 2. 方案设计
- 优先选择最小可行改动（MVP），避免跨层大改。
- 若影响公平比较，先更新协议与配置，再动代码。

## 3. 实施顺序
1. 更新配置（`configs/base.yaml` 或 `configs/tasks/*.yaml`）
2. 更新执行脚本（`scripts/`）
3. 必要时更新模型实现（`efficient_kan/`）
4. 最后更新 Notebook 展示与 `spec/` 文档

## 4. 运行与验证
- 最低验证命令：`python scripts/run_experiment_plan.py --task <task-yaml>`
- 验证通过标准：能稳定产出计划文件，字段完整，失败可见。

## 5. 结果沉淀
- 将可复现实验输出落盘到 `results/`。
- 关键结论回写到 `CURRENT_WORK_REFERENCE.md` 或论文图表来源说明。

## 6. 提交前同步
- 同步更新相关规范文件（至少 `spec/experiment/*` 或 `spec/core/*`）。
- 在提交说明中写明 WHY（为什么改）与影响边界。

