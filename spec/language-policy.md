# 语言与注释规范

## 1. 适用范围
- `efficient_kan/`、`scripts/`、`verify_install.py` 等代码文件
- `notebooks/*.ipynb`

## 2. 代码语言规则
- 代码注释必须使用英文。
- Docstring 必须使用 Google 风格，且内容为英文。
- 变量名、函数名、类名、异常信息、日志字段名统一使用英文。

## 3. 输出与打印规则
- 终端打印信息（`print`、日志输出）必须使用英文。
- 结果文件中的字段名与状态值必须使用英文（如 `status=success/fail`）。

## 4. Notebook 语言规则
- Notebook 的 Markdown 单元格文字必须使用中文（便于论文写作）。
- Notebook 代码单元中的注释、变量、函数、输出文本仍遵循英文规则。

## 5. 例外与兼容
- 引用外部原文可保留原语言，但需附简短中文说明（仅 Notebook markdown 允许）。
- 历史文件不强制一次性重写；新增与改动内容必须遵守本规范。

