"""Validate required output schemas for plan, raw, and summary artifacts.

Usage:
    python scripts/checks/check_output_schema.py --output-root output
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Iterable, Optional, Sequence, Set


PLAN_REQUIRED_FIELDS: Set[str] = {
    "run_id",
    "task_name",
    "method",
    "seed",
    "split_seed",
    "train_num",
    "test_num",
    "budget_time_seconds",
}

RAW_REQUIRED_FIELDS: Set[str] = {
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
}

SUMMARY_REQUIRED_FIELDS: Set[str] = {
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
}

ALLOWED_STATUS = {"success", "fail"}


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Validate output schema completeness.")
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("output"),
        help="Output root directory to validate.",
    )
    parser.add_argument(
        "--allow-placeholder",
        action="store_true",
        help="Allow simulated rows (`is_simulated=true`) in raw/summary outputs.",
    )
    return parser.parse_args()


def read_csv_dict_rows(path: Path) -> tuple[Sequence[str], list[dict[str, str]]]:
    """Read CSV header and all rows."""
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames or [], list(reader)


def validate_csv_header(path: Path, required_fields: Set[str], errors: list[str]) -> None:
    """Validate required header fields in a CSV file."""
    header = set(read_csv_dict_rows(path)[0])
    missing = sorted(required_fields - header)
    if missing:
        errors.append(f"{path}: missing required fields: {', '.join(missing)}")


def validate_plan_json(path: Path, required_fields: Set[str], errors: list[str]) -> None:
    """Validate required keys and semantics in every plan JSON record."""
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

    plan_run_ids: Set[str] = set()
    file_run_id = path.stem.replace("_plan", "")
    for idx, record in enumerate(data):
        if not isinstance(record, dict):
            errors.append(f"{path}: record {idx} is not an object")
            continue
        missing = sorted(required_fields - set(record.keys()))
        if missing:
            errors.append(f"{path}: record {idx} missing keys: {', '.join(missing)}")
            continue
        run_id = str(record.get("run_id", "")).strip()
        if not run_id:
            errors.append(f"{path}: record {idx} has empty run_id")
        else:
            plan_run_ids.add(run_id)
            if run_id != file_run_id:
                errors.append(
                    f"{path}: record {idx} run_id '{run_id}' does not match filename run_id '{file_run_id}'"
                )

    if len(plan_run_ids) > 1:
        errors.append(f"{path}: multiple run_id values found: {sorted(plan_run_ids)}")


def require_non_empty(files: Iterable[Path], label: str, errors: list[str]) -> list[Path]:
    """Ensure a section has at least one file."""
    collected = list(files)
    if not collected:
        errors.append(f"{label}: no files found")
    return collected


def latest_plan_json(output_root: Path) -> Optional[Path]:
    """Return latest plan JSON path under output root."""
    candidates = list(output_root.glob("*_plan.json"))
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def parse_float(
    value: str, *, min_value: Optional[float] = None, max_value: Optional[float] = None
) -> Optional[float]:
    """Parse float with optional bounds."""
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    if min_value is not None and parsed < min_value:
        return None
    if max_value is not None and parsed > max_value:
        return None
    return parsed


def parse_int(value: str, *, min_value: Optional[int] = None) -> Optional[int]:
    """Parse int with optional lower bound."""
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None
    if min_value is not None and parsed < min_value:
        return None
    return parsed


def parse_bool_string(value: str) -> Optional[bool]:
    """Parse bool from normalized string."""
    normalized = str(value).strip().lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    return None


def validate_raw_rows(path: Path, rows: list[dict[str, str]], errors: list[str]) -> None:
    """Validate row-level raw output semantics."""
    for row_idx, row in enumerate(rows, start=2):
        row_prefix = f"{path}:{row_idx}"
        run_id = str(row.get("run_id", "")).strip()
        if not run_id:
            errors.append(f"{row_prefix} run_id is empty")

        is_simulated = parse_bool_string(row.get("is_simulated", ""))
        if is_simulated is None:
            errors.append(f"{row_prefix} is_simulated must be true/false")

        status = str(row.get("status", "")).strip().lower()
        if status not in ALLOWED_STATUS:
            errors.append(f"{row_prefix} status must be one of {sorted(ALLOWED_STATUS)}")
            continue

        seed = parse_int(row.get("seed", ""))
        if seed is None:
            errors.append(f"{row_prefix} seed must be int")

        if status == "success":
            if str(row.get("error_message", "")).strip():
                errors.append(f"{row_prefix} success row must have empty error_message")
            if parse_float(row.get("mse", ""), min_value=0.0) is None:
                errors.append(f"{row_prefix} success row has invalid mse")
            if parse_float(row.get("r2", ""), min_value=-1.0, max_value=1.0) is None:
                errors.append(f"{row_prefix} success row has invalid r2")
            if parse_float(row.get("time_seconds", ""), min_value=0.0) is None:
                errors.append(f"{row_prefix} success row has invalid time_seconds")
            if parse_int(row.get("complexity", ""), min_value=0) is None:
                errors.append(f"{row_prefix} success row has invalid complexity")
            if not str(row.get("expression", "")).strip():
                errors.append(f"{row_prefix} success row must have non-empty expression")
        else:
            if not str(row.get("error_message", "")).strip():
                errors.append(f"{row_prefix} fail row must have non-empty error_message")


def validate_summary_rows(path: Path, rows: list[dict[str, str]], errors: list[str]) -> None:
    """Validate row-level summary output semantics."""
    for row_idx, row in enumerate(rows, start=2):
        row_prefix = f"{path}:{row_idx}"
        run_id = str(row.get("run_id", "")).strip()
        if not run_id:
            errors.append(f"{row_prefix} run_id is empty")

        if parse_bool_string(row.get("is_simulated", "")) is None:
            errors.append(f"{row_prefix} is_simulated must be true/false")

        n_repeats = parse_int(row.get("n_repeats", ""), min_value=1)
        if n_repeats is None:
            errors.append(f"{row_prefix} n_repeats must be positive int")

        success_rate = parse_float(row.get("success_rate", ""), min_value=0.0, max_value=1.0)
        if success_rate is None:
            errors.append(f"{row_prefix} success_rate must be float in [0,1]")

        mse_std = parse_float(row.get("mse_std", ""), min_value=0.0)
        r2_std = parse_float(row.get("r2_std", ""), min_value=0.0)
        time_std = parse_float(row.get("time_std", ""), min_value=0.0)
        if mse_std is None:
            errors.append(f"{row_prefix} mse_std must be non-negative float")
        if r2_std is None:
            errors.append(f"{row_prefix} r2_std must be non-negative float")
        if time_std is None:
            errors.append(f"{row_prefix} time_std must be non-negative float")


def check_placeholder_policy(
    paths: list[Path], errors: list[str], *, allow_placeholder: bool
) -> None:
    """Check whether placeholder/simulated outputs are allowed."""
    if allow_placeholder:
        return

    for path in paths:
        _, rows = read_csv_dict_rows(path)
        for row_idx, row in enumerate(rows, start=2):
            is_simulated = parse_bool_string(row.get("is_simulated", ""))
            if is_simulated:
                errors.append(
                    f"{path}:{row_idx} simulated output is not allowed; pass --allow-placeholder to override"
                )


def main() -> int:
    """Run schema checks and return process exit code."""
    args = parse_args()
    root = args.output_root
    errors: list[str] = []

    if not root.exists() or not root.is_dir():
        print(f"[ERROR] Output root does not exist or is not a directory: {root}")
        return 1

    latest_plan = latest_plan_json(root)
    if latest_plan is None:
        errors.append("plan json: no files found")
        plan_json_files: list[Path] = []
        plan_csv_files: list[Path] = []
    else:
        plan_json_files = [latest_plan]
        latest_csv = root / f"{latest_plan.stem}.csv"
        plan_csv_files = [latest_csv] if latest_csv.exists() else []
        if not plan_csv_files:
            errors.append(f"plan csv: matching csv not found for {latest_plan.name}")
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
        _, rows = read_csv_dict_rows(path)
        validate_raw_rows(path, rows, errors)
    for path in summary_csv_files:
        validate_csv_header(path, SUMMARY_REQUIRED_FIELDS, errors)
        _, rows = read_csv_dict_rows(path)
        validate_summary_rows(path, rows, errors)

    check_placeholder_policy(raw_csv_files + summary_csv_files, errors, allow_placeholder=args.allow_placeholder)

    if errors:
        print("[ERROR] Output schema validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("[OK] Output schema validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
