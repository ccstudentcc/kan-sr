# Result Field Schema (Single Source of Truth)

## 1. Version
- Schema Version: `v1`
- Scope: `plan`, `raw`, `summary`, `env`

## 2. Plan Fields (Currently Implemented)
Required fields:
- `task_name` (string)
- `method` (string)
- `seed` (int)
- `split_seed` (int)
- `train_num` (int or empty)
- `test_num` (int or empty)
- `budget_time_seconds` (number or empty)
- `status` (to be populated in the later run stage)

## 3. Raw Fields (Target)
Required fields:
- `task_name`, `method`, `seed`
- `mse`, `r2`, `time_seconds`
- `expression`, `complexity`
- `status`, `error_message`

## 4. Summary Fields (Target)
Required fields:
- `task_name`, `method`, `n_repeats`
- `mse_mean/std`, `r2_mean/std`
- `time_mean/std`, `success_rate`

## 5. Unified Naming Rules
- Current configuration uses `train_num/test_num`; if external documents use `train_size/test_size`, treat them as synonymous mappings.
- New internal repository specifications must uniformly use `train_num/test_num`.

## 6. Compatibility and Changes
- New fields should be backward compatible (nullable by default)
- Deleting or renaming fields is a breaking change and requires protocol updates plus migration notes
