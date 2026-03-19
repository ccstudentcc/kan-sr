# 方法适配接口契约

## 1. 背景
- 当前项目支持 `kan`、`gplearn`、`bms`、`qlattice`。
- 为保证公平比较与可扩展性，需要统一方法适配层接口。

## 2. 统一接口（建议）
- `fit(X_train, y_train, budget, seed)`
- `predict(X_test)`
- `export_expression()`（可选）
- `complexity()`（可选）
- `metadata()`（返回方法版本与关键参数）

## 3. 预算映射
- 全局预算：`budget.time_budget_seconds`
- 方法预算：`budget.per_method[method]`
- 适配器负责将统一预算映射到方法私有参数（如 `generations`、`epochs`、`fit_steps`）

## 4. 能力矩阵
- 不同方法可能不支持 `expression` 或 `complexity`。
- 不支持时必须返回空值并保持字段存在，禁止删列。

## 5. 异常映射
- 任意方法异常必须映射为统一输出：
  - `status=fail`
  - `error_message=<可定位信息>`

