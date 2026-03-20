# Experiment Specification Index

Scope: `configs/`, `scripts/`, `EXPERIMENT_PROTOCOL.md`, and all experiment notebooks.  
Status definitions: `Adopted` (implemented), `Adopted with Gaps` (executed but with gaps), `Draft` (implementation pending).

| Specification | File | Status | Description |
|---|---|---|---|
| Task and Configuration Specification | `config-guidelines.md` | Adopted | Aligned with `configs/base.yaml` and `configs/tasks/*.yaml` |
| Execution Contract | `execution-contract.md` | Adopted with Gaps | Defines inputs/outputs and failure strategy for plan/run/report |
| Task and Data Contract | `task-data-contract.md` | Adopted with Gaps | Unifies generator, split, noise, and seed propagation chain |
| Result Field Schema | `result-schema.md` | Adopted with Gaps | Unifies the single source of truth for plan/raw/summary/env fields |
| Minimal Executable Runbook | `minimal-executable-runbook.md` | Adopted | Minimal local executable flow and acceptance checks |
| Reproducibility Manifest Specification | `reproducibility-manifest.md` | Draft | Environment recording and rerun acceptance thresholds |
| Notebook Specification | `notebook-guidelines.md` | Draft | Unifies responsibility boundaries between exploration and deliverables |
| Result and Artifact Governance | `result-governance.md` | Adopted with Gaps | Unifies `output/` fields, snapshots, and traceability |
| Quality Gates | `quality-guidelines.md` | Adopted | Pre/post-run checks and minimum reproducibility requirements |
| Directory Structure Specification | `directory-structure.md` | Adopted | Current repository structure constraints and evolution rules |

Owner: Project Maintainers  
Last Verified: 2026-03-19
