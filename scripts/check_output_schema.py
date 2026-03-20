"""Validate required output schemas for plan, raw, and summary artifacts.

Usage:
    python scripts/check_output_schema.py --output-root output
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Iterable, Sequence, Set


PLAN_REQUIRED_FIELDS: Set[str] = {
    "task_name",
    "method",
    "seed",
    "split_seed",
    "train_num",
    "test_num",
    "budget_time_seconds",
}

RAW_REQUIRED_FIELDS: Set[str] = {
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
}

SUMMARY_REQUIRED_FIELDS: Set[str] = {
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
}


def read_csv_fieldnames(path: Path) -> Sequence[str]:
    """Read CSV header field names."""
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames or []


def validate_csv_header(path: Path, required_fields: Set[str], errors: list[str]) -> None:
    """Validate required header fields in a CSV file."""
    header = set(read_csv_fieldnames(path))
    missing = sorted(required_fields - header)
    if missing:
        errors.append(f"{path}: missing required fields: {', '.join(missing)}")


def validate_plan_json(path: Path, required_fields: Set[str], errors: list[str]) -> None:
    """Validate required keys in every plan JSON record."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{path}: invalid JSON ({exc})")
        return

    if not isinstance(data, list):
        errors.append(f"{path}: expected a JSON list of plan records")
        return

    if not data:
        errors.append(f"{path}: plan list is empty")
        return

    for idx, record in enumerate(data):
        if not isinstance(record, dict):
            errors.append(f"{path}: record {idx} is not an object")
            continue
        missing = sorted(required_fields - set(record.keys()))
        if missing:
            errors.append(f"{path}: record {idx} missing keys: {', '.join(missing)}")


def require_non_empty(files: Iterable[Path], label: str, errors: list[str]) -> list[Path]:
    """Ensure a section has at least one file."""
    collected = list(files)
    if not collected:
        errors.append(f"{label}: no files found")
    return collected


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Validate output schema completeness.")
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("output"),
        help="Output root directory to validate.",
    )
    return parser.parse_args()


def main() -> int:
    """Run schema checks and return process exit code."""
    args = parse_args()
    root = args.output_root
    errors: list[str] = []

    if not root.exists() or not root.is_dir():
        print(f"[ERROR] Output root does not exist or is not a directory: {root}")
        return 1

    plan_csv_files = require_non_empty(root.glob("*_plan.csv"), "plan csv", errors)
    plan_json_files = require_non_empty(root.glob("*_plan.json"), "plan json", errors)
    raw_dir = root / "raw"
    summary_dir = root / "summary"
    raw_csv_files = require_non_empty(raw_dir.rglob("*.csv"), "raw csv", errors)
    summary_csv_files = require_non_empty(summary_dir.rglob("*.csv"), "summary csv", errors)

    for path in plan_csv_files:
        validate_csv_header(path, PLAN_REQUIRED_FIELDS, errors)
    for path in plan_json_files:
        validate_plan_json(path, PLAN_REQUIRED_FIELDS, errors)
    for path in raw_csv_files:
        validate_csv_header(path, RAW_REQUIRED_FIELDS, errors)
    for path in summary_csv_files:
        validate_csv_header(path, SUMMARY_REQUIRED_FIELDS, errors)

    if errors:
        print("[ERROR] Output schema validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("[OK] Output schema validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
