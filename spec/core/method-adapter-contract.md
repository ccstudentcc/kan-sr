# Method Adapter Interface Contract

## 1. Background
- The project currently supports `kan`, `gplearn`, `bms`, and `qlattice`.
- To ensure fair comparison and extensibility, the method adapter layer needs a unified interface.

## 2. Unified Interface (Recommended)
- `fit(X_train, y_train, budget, seed)`
- `predict(X_test)`
- `export_expression()` (optional)
- `complexity()` (optional)
- `metadata()` (returns method version and key parameters)

## 3. Budget Mapping
- Global budget: `budget.time_budget_seconds`
- Per-method budget: `budget.per_method[method]`
- The adapter is responsible for mapping unified budgets to method-specific parameters (e.g., `generations`, `epochs`, `fit_steps`).

## 4. Capability Matrix
- Different methods may not support `expression` or `complexity`.
- If unsupported, return empty values while keeping fields present; removing columns is forbidden.

## 5. Exception Mapping
- Any method exception must be mapped to a unified output:
  - `status=fail`
  - `error_message=<locatable information>`
