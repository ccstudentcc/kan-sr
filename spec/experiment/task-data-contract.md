# 任务与数据契约

## 1. 任务定义
- 每个任务必须在 `configs/tasks/<task>.yaml` 中定义。
- 最小字段：`task.name`、`data.generator`、`data.n_var`、`data.train_num`、`data.test_num`。

## 2. 生成器与数据范围
- `data.generator` 必须是明确可解释的数据生成策略。
- `data.ranges` 必须给出输入范围，不允许隐式默认。

## 3. 噪声模型
- 噪声开关：`data.noise.enabled`
- 噪声类型：`data.noise.kind`
- 噪声强度：`data.noise.std`
- 若启用噪声，必须写清强度来源或任务假设。

## 4. 切分与 seed 传递
- 全局 seed：`reproducibility.seed_list`
- 切分 seed：由 `split.split_seed_from_run_seed` 决定
- 方法 seed：由每个方法参数显式继承或映射

## 5. 校验清单
- `n_var` 与任务公式输入维度一致
- `train_num/test_num` 为正整数
- 噪声开启时 `std > 0`
- 切分策略在任务间可公平比较

