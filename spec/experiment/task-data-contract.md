# Task and Data Contract

## 1. Task Definition
- Each task must be defined in `configs/tasks/<task>.yaml`.
- Minimum fields: `task.name`, `data.generator`, `data.n_var`, `data.train_num`, `data.test_num`.

## 2. Generator and Data Range
- `data.generator` must be an explicit and interpretable data generation strategy.
- `data.ranges` must define input ranges; implicit defaults are not allowed.

## 3. Noise Model
- Noise switch: `data.noise.enabled`
- Noise type: `data.noise.kind`
- Noise intensity: `data.noise.std`
- If noise is enabled, the source of intensity or task assumption must be documented.

## 4. Split and Seed Propagation
- Global seed: `reproducibility.seed_list`
- Split seed: determined by `split.split_seed_from_run_seed`
- Method seed: explicitly inherited or mapped by each method's parameters

## 5. Validation Checklist
- `n_var` matches the input dimensionality of the task formula
- `train_num/test_num` are positive integers
- When noise is enabled, `std > 0`
- Split strategy supports fair comparison across tasks
