# Core Code Quality Gates

## 1. Script Layer
- Every new script must support `--help`.
- Argument parsing must provide defaults and clear error messages.
- File writes must explicitly specify encoding (recommended: `utf-8`).

## 2. Model Layer
- Model forward passes should assert input dimensions (already practiced in `KANLinear`/`KAN`).
- Changes that affect numerical stability must include a minimal validation note.

## 3. Regression Checks (Minimum Set)
- Config loading and merge flow is runnable.
- At least one task can successfully produce a plan file.
- New code does not break existing `efficient_kan` export interfaces.

## 4. Documentation Synchronization
- When adding config fields or result fields, `EXPERIMENT_PROTOCOL.md` and corresponding files in `spec/` must be updated in sync.
