# DoD Checklist (Definition of Done)

## 1. Experiment and Configuration
- Task goal and impact scope are clearly defined
- Relevant `configs/*.yaml` are updated and validated
- Repeat count and seed strategy comply with protocol (default `n_repeats >= 5`)

## 2. Code and Scripts
- Key entry points are runnable (at least plan generation works)
- No silent failures (`except: pass` is forbidden)
- Critical exceptions include context (task, method, seed)

## 3. Results and Artifacts
- Artifacts are written to the agreed directory (`output/`)
- Result fields satisfy minimum spec requirements (raw/summary)
- `run_id` is consistent across `plan/raw/summary`
- Added large files include purpose and source mapping

## 4. Documentation Sync
- Relevant `spec/` files are updated
- If protocol fields changed, `EXPERIMENT_PROTOCOL.md` is synchronized
- If conclusions changed, corresponding content in `CURRENT_WORK_REFERENCE.md` or README is synchronized

## 5. Commit Quality
- Commit message includes WHY and impact scope
- No unrelated temporary files or debug output are committed
- Changes are reversible and risks are explainable

## 6. Language Policy
- Code comments and docstrings are English, and docstrings follow Google style
- `print`/logging/result fields are English
- Notebook markdown is Chinese
- `spec/` documents are English-only
- `docs/` documents are primarily Chinese
- Executed:
  - `python scripts/run_checks.py --output-root output` (real outputs), or
  - `python scripts/run_checks.py --output-root output --allow-placeholder` (placeholder stage)
