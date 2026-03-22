"""Plan/raw I/O helpers for experiment execution."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple


REQUIRED_OUTPUT_FIELDS = [
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
]


def load_plan(plan_path: Path) -> List[Dict[str, Any]]:
    """Load plan records from JSON or CSV."""
    suffix = plan_path.suffix.lower()
    if suffix == ".json":
        with plan_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError(f"JSON plan must be a list of rows: {plan_path}")
        return data

    if suffix == ".csv":
        with plan_path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            return list(reader)

    raise ValueError(f"Unsupported plan file type: {plan_path.suffix}")


def fail_row(
    *,
    run_id: str,
    task_name: str,
    method: str,
    seed: Any,
    error_message: str,
) -> Dict[str, Any]:
    """Build standardized failed row."""
    return {
        "run_id": run_id,
        "is_simulated": "false",
        "task_name": task_name,
        "method": method,
        "seed": seed,
        "mse": "",
        "r2": "",
        "time_seconds": "",
        "expression": "",
        "complexity": "",
        "status": "fail",
        "error_message": error_message,
    }


def write_grouped_raw(rows: List[Dict[str, Any]], out_dir: Path) -> List[Path]:
    """Write raw result rows grouped by task and method."""
    grouped: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}
    for row in rows:
        key = (str(row["task_name"]), str(row["method"]))
        grouped.setdefault(key, []).append(row)

    written_paths: List[Path] = []
    for (task_name, method), records in grouped.items():
        target_dir = out_dir / "raw" / task_name
        target_dir.mkdir(parents=True, exist_ok=True)
        target_csv = target_dir / f"{method}.csv"

        with target_csv.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=REQUIRED_OUTPUT_FIELDS)
            writer.writeheader()
            writer.writerows(records)

        written_paths.append(target_csv)

    return written_paths
