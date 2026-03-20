# Reproducibility Environment Manifest Specification

## 1. Objective
- Provide a minimum environment fingerprint for each experiment to ensure later reruns and comparisons.

## 2. Minimum Record Set
- Python version
- OS and platform information
- Key library versions (`numpy`, `torch`, `scikit-learn`, `pyyaml`, `pykan`, etc.)
- Task configuration file path and hash (recommended)
- Execution time and command

## 3. Storage Location
- Recommended: `output/env/<task_name>.json` or `output/env/<timestamp>.json`

## 4. Rerun Acceptance
- Same config and same seed can generate plans at the same scale
- Metric variance should remain within acceptable thresholds (defined per task)
- If variance is abnormal, possible causes must be recorded (hardware, dependencies, randomness implementation differences)
