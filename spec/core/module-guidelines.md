# Module Design Guidelines

## 1. Layered Responsibilities
- `efficient_kan/`: model definitions and mathematical logic (e.g., `KANLinear`, `KAN`)
- `scripts/`: orchestration layer (read configs, build plans, write outputs)
- `configs/`: parameters and protocol only, no execution logic

## 2. Interface Constraints
- Public module interfaces are centralized in `efficient_kan/__init__.py`.
- Scripts should organize workflow through functions and avoid putting primary logic inside `if __name__ == "__main__"`.

## 3. Design Principles
- Prefer simple and explicit implementations; avoid over-abstraction.
- Prefer passing parameters via config objects instead of many implicit global variables.
- Code comments and docstrings must be in English; docstrings should use Google style.
- `print` and logging output must be in English to support automated parsing and auditing.

## 4. Extension Rules
- When adding a new method (beyond `kan/gplearn/bms/qlattice`):
  - First update the supported-method list and config validation.
  - Then add a task configuration example.
  - Finally update documentation and result-field mapping.
