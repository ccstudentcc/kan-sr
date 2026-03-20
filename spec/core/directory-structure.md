# Core Directory Structure Guidelines

## 1. Code Entry Points
- Execution entry points are in `scripts/`.
- Model implementation entry points are in `efficient_kan/`.

## 2. Responsibility Boundaries
- `efficient_kan/` must not directly depend on notebook variable state.
- `scripts/` must not implement deep model mathematics.
- `configs/` must not contain executable logic.

## 3. Rules for New Modules
- Every new module must declare a clear purpose and invocation path.
- Directory depth must not exceed 3 levels (excluding data asset directories).

## 4. Historical Asset Protection
- `model/` and `raw/` are data asset directories and are append-only by default; cleanup requires a separate change note.
