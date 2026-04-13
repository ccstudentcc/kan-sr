# KAN-Symbolic_Regression 中文论文材料

本目录将 `KAN-Symbolic_Regression` 里分散在 `README`、`CURRENT_WORK_REFERENCE`、`notebooks/`、`output/` 中的内容整理为中文论文写作材料。

在当前论文工作区里，这组材料更适合服务于 `symkan-experiments` 的主实验叙述，承担统一对比与扩展案例支撑，而不是单独充当全文主线。

## 文件说明

- [`01_研究边界与现有资产说明.md`](01_研究边界与现有资产说明.md)
- [`02_统一对比实验材料整理.md`](02_统一对比实验材料整理.md)
- [`03_扩展案例实验材料整理.md`](03_扩展案例实验材料整理.md)
- [`04_局限性与论文中需主动承认的问题.md`](04_局限性与论文中需主动承认的问题.md)

## 使用建议

- 如果要写“统一对比实验”，优先使用 `02_统一对比实验材料整理.md`。
- 如果要写“特殊函数、无监督学习、查找表压缩”等案例，优先使用 `03_扩展案例实验材料整理.md`。
- 如果要写“哪些资产是继承的、哪些结果目前还不能写满”，优先使用 `01_研究边界与现有资产说明.md` 与 `04_局限性与论文中需主动承认的问题.md`。

## 可引用的参考报告

- [`docs/paper_cn/01_研究边界与现有资产说明.md`](01_研究边界与现有资产说明.md)：适合引用资产边界、结果类型与继承产物说明。
- [`docs/paper_cn/02_统一对比实验材料整理.md`](02_统一对比实验材料整理.md)：适合引用统一脚本链路下的主结果表。
- [`docs/paper_cn/03_扩展案例实验材料整理.md`](03_扩展案例实验材料整理.md)：适合引用特殊函数、无监督关系发现和查找表压缩等补充案例。
- [`CURRENT_WORK_REFERENCE.md`](../CURRENT_WORK_REFERENCE.md)：适合引用历史工作与继承资产边界。
- [`EXPERIMENT_PROTOCOL.md`](../EXPERIMENT_PROTOCOL.md)：适合引用实验组织和执行口径。

## 可引用的数据来源

- [`output/summary/univariate_quadratic.csv`](../output/summary/univariate_quadratic.csv)：统一单变量对比任务主结果。
- [`output/summary/multivariate_sinexp.csv`](../output/summary/multivariate_sinexp.csv)：统一多变量对比任务主结果。
- [`output/env/univariate_quadratic.json`](../output/env/univariate_quadratic.json)：单变量任务环境记录。
- [`output/env/multivariate_sinexp.json`](../output/env/multivariate_sinexp.json)：多变量任务环境记录。
- [`output/raw/univariate_quadratic/`](../output/raw/univariate_quadratic)：单变量任务各方法表达式与原始结果。
- [`output/raw/multivariate_sinexp/`](../output/raw/multivariate_sinexp)：多变量任务各方法表达式与原始结果。

## 可引用的参考图表或图表来源

- [`notebooks/Comparison_of_different_methods_for_SR_univariate.ipynb`](../notebooks/Comparison_of_different_methods_for_SR_univariate.ipynb)：单变量任务的现有 notebook 图表示例来源。
- [`notebooks/Comparison_of_different_methods_for_SR_multivariate.ipynb`](../notebooks/Comparison_of_different_methods_for_SR_multivariate.ipynb)：多变量任务的现有 notebook 图表示例来源。
- [`notebooks/Special_function.ipynb`](../notebooks/Special_function.ipynb)：特殊函数案例图表与误差对照来源。
- [`notebooks/Reducing_the_lookup_table_size.ipynb`](../notebooks/Reducing_the_lookup_table_size.ipynb)：查找表压缩相关图表来源。
- 当前仓库没有单独维护的论文图目录；更稳妥的做法，是从 `output/summary`、`output/raw` 和相应 notebook 中重新出图，而不是直接截取 notebook 页面。
