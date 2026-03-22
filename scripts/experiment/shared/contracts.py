"""Shared data contract constants for experiment artifacts."""

from __future__ import annotations

PLAN_REQUIRED_FIELDS = (
    "run_id",
    "task_name",
    "method",
    "seed",
    "split_seed",
    "train_num",
    "test_num",
    "budget_time_seconds",
)

RAW_OUTPUT_FIELDS = (
    "run_id",
    "is_simulated",
    "task_name",
    "method",
    "seed",
    "mse",
    "r2",
    "time_seconds",
    "expression",
    "complexity",
    "status",
    "error_message",
)

RAW_COLUMNS_FOR_SUMMARY = (
    "run_id",
    "is_simulated",
    "task_name",
    "method",
    "mse",
    "r2",
    "time_seconds",
    "status",
)

SUMMARY_OUTPUT_FIELDS = (
    "run_id",
    "is_simulated",
    "task_name",
    "method",
    "n_repeats",
    "mse_mean",
    "mse_std",
    "r2_mean",
    "r2_std",
    "time_mean",
    "time_std",
    "success_rate",
)

ENV_REQUIRED_FIELDS = (
    "schema_version",
    "task_name",
    "run_id",
    "run_ids",
    "generated_at_utc",
    "python_version",
    "platform",
    "is_simulated",
    "methods",
    "n_methods",
    "raw_files",
)

ALLOWED_STATUS = {"success", "fail"}
