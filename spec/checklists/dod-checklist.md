# DoD 检查清单（Definition of Done）

## 1. 实验与配置
- 已明确任务目标与影响范围
- 已更新并校验相关 `configs/*.yaml`
- 重复次数与种子策略符合协议（默认 `n_repeats >= 5`）

## 2. 代码与脚本
- 关键入口可运行（至少可生成计划）
- 无静默失败（无 `except: pass`）
- 关键异常包含上下文信息（任务、方法、seed）

## 3. 结果与产物
- 产物落盘到约定目录（`output/`）
- 结果字段符合最小规范（raw/summary）
- 大文件新增有用途说明与来源映射

## 4. 文档同步
- 相关 `spec/` 文档已更新
- 如协议字段变更，`EXPERIMENT_PROTOCOL.md` 已同步
- 如结论更新，`CURRENT_WORK_REFERENCE.md` 或 README 对应内容已同步

## 5. 提交质量
- 提交说明包含 WHY 与影响范围
- 未提交无关临时文件或调试输出
- 变更可回滚且风险可解释

## 6. 语言规范
- 代码注释与 Docstring 为英文，且 Docstring 符合 Google 风格
- `print`/日志/结果字段为英文
- Notebook Markdown 为中文
- 已执行：`python scripts/check_language_policy.py`
