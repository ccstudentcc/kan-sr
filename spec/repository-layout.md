# 仓库文件管理规范

## 1. 目标目录结构
- `docs/`：项目文档与规范外的说明材料
- `notebooks/`：全部实验与分析 Notebook
- `scripts/`：可复用的命令行脚本入口
- `configs/`：实验参数与协议配置
- `output/`：计划、原始结果、汇总结果、环境清单
- `raw/`：原始采集数据（不可逆实验输入）
- `model/`：模型快照与缓存资产
- `spec/`：工程与实验规范

## 2. 放置规则
- 新 Notebook 只允许放在 `notebooks/`，禁止新增到根目录。
- 新结果产物只允许放在 `output/`，禁止散落在根目录或 `docs/`。
- 说明文档默认放 `docs/`；规范文档放 `spec/`。

## 3. 命名规则
- Notebook：`<topic>_<goal>.ipynb`（例如 `pendulum_symbolic_regression.ipynb`）
- 输出文件：`<timestamp>_<task>_<artifact>.<ext>`
- 脚本：动词开头（如 `run_*.py`、`check_*.py`）

## 4. 迁移策略（兼容当前仓库）
- 根目录不保留 `*.ipynb`；Notebook 统一在 `notebooks/`。
- `results/` 视为 legacy 结果目录，不强制立即迁移历史文件。
- 新流程统一使用 `output/`，必要时保留 `results/` 只读归档。

## 5. 禁止事项
- 禁止在根目录新增一次性输出与临时文件。
- 禁止将实验结果放入 `docs/` 或 `spec/`。
