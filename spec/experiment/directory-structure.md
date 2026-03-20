# 实验目录结构规范

## 1. 当前结构分层
- `configs/`：实验协议与任务参数
- `scripts/`：可复用执行入口（非交互）
- `output/`：计划与评估产物（标准目录）
- `results/`：历史产物（legacy，只读归档）
- `notebooks/`：实验与分析 Notebook（标准目录）
- `docs/`：项目说明文档（非规范）
- `raw/`：原始传感器数据
- `model/`：模型快照与缓存资产

## 2. 新文件放置规则
- 新任务参数放 `configs/tasks/<task>.yaml`
- 新批量流程放 `scripts/`
- 新评估数据放 `output/`，不要放在项目根目录
- 新 Notebook 放 `notebooks/`
- 一般说明文档放 `docs/`，规范文档放 `spec/`
- 图像资源统一放 `img/`

## 3. 禁止事项
- 禁止把一次性实验脚本散落在根目录
- 禁止把“与任务无关”的临时输出提交进仓库
