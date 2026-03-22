"""Check plan/raw/summary coverage consistency by run_id and key tuples."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


PlanKey = Tuple[str, str, str]


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Validate plan/raw/summary coverage consistency.")
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("output"),
        help="Output root directory.",
    )
    parser.add_argument(
        "--plan-json",
        type=Path,
        default=None,
        help="Optional explicit plan JSON. Defaults to latest plan under output/plan or output root.",
    )
    return parser.parse_args()


def latest_plan_json(output_root: Path) -> Optional[Path]:
    """Return latest plan JSON path."""
    plan_dir = output_root / "plan"
    candidates = list(plan_dir.glob("*_plan.json")) if plan_dir.exists() else []
    if not candidates:
        candidates = list(output_root.glob("*_plan.json"))
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def load_plan(path: Path) -> tuple[str, Dict[str, Set[PlanKey]], Dict[str, Set[str]]]:
    """Load plan expectations grouped by task."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data:
        raise ValueError(f"Plan JSON must be a non-empty list: {path}")

    run_ids = {
        str(row.get("run_id", "")).strip()
        for row in data
        if isinstance(row, dict) and str(row.get("run_id", "")).strip()
    }
    if not run_ids:
        raise ValueError(f"No valid run_id found in plan: {path}")
    if len(run_ids) != 1:
        raise ValueError(f"Multiple run_id values in plan: {sorted(run_ids)}")
    run_id = next(iter(run_ids))

    expected_keys: Dict[str, Set[PlanKey]] = defaultdict(set)
    expected_methods: Dict[str, Set[str]] = defaultdict(set)
    for idx, row in enumerate(data):
        if not isinstance(row, dict):
            raise ValueError(f"Plan row {idx} is not an object: {path}")
        task = str(row.get("task_name", "")).strip()
        method = str(row.get("method", "")).strip()
        seed = str(row.get("seed", "")).strip()
        if not task or not method or not seed:
            raise ValueError(f"Plan row {idx} missing task_name/method/seed: {path}")
        expected_keys[task].add((task, method, seed))
        expected_methods[task].add(method)
    return run_id, expected_keys, expected_methods


def read_csv_rows(path: Path) -> List[dict[str, str]]:
    """Read all CSV rows."""
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main() -> int:
    """Run coverage checks and return process exit code."""
    args = parse_args()
    root = args.output_root
    if not root.exists() or not root.is_dir():
        print(f"[ERROR] Output root does not exist or is not a directory: {root}")
        return 1

    plan_json = args.plan_json or latest_plan_json(root)
    if plan_json is None or not plan_json.exists():
        print(f"[ERROR] No plan json found under: {root}")
        return 1

    try:
        run_id, expected_keys, expected_methods = load_plan(plan_json)
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"[ERROR] {exc}")
        return 1

    errors: List[str] = []
    raw_root = root / "raw"
    summary_root = root / "summary"

    for task, task_expected_keys in expected_keys.items():
        task_raw_dir = raw_root / task
        if not task_raw_dir.exists():
            errors.append(f"{task}: missing raw directory {task_raw_dir}")
            continue

        actual_keys: Set[PlanKey] = set()
        actual_methods: Set[str] = set()
        for raw_file in sorted(task_raw_dir.glob("*.csv")):
            rows = read_csv_rows(raw_file)
            for row_idx, row in enumerate(rows, start=2):
                row_task = str(row.get("task_name", "")).strip()
                row_method = str(row.get("method", "")).strip()
                row_seed = str(row.get("seed", "")).strip()
                row_run_id = str(row.get("run_id", "")).strip()
                if row_run_id != run_id:
                    errors.append(
                        f"{raw_file}:{row_idx} run_id '{row_run_id}' does not match plan run_id '{run_id}'"
                    )
                if row_task and row_method and row_seed:
                    actual_keys.add((row_task, row_method, row_seed))
                    actual_methods.add(row_method)

        missing = sorted(task_expected_keys - actual_keys)
        extras = sorted(actual_keys - task_expected_keys)
        if missing:
            errors.append(f"{task}: missing raw rows for keys: {missing[:5]}{' ...' if len(missing) > 5 else ''}")
        if extras:
            errors.append(f"{task}: unexpected raw rows not in plan: {extras[:5]}{' ...' if len(extras) > 5 else ''}")

        summary_path = summary_root / f"{task}.csv"
        if not summary_path.exists():
            errors.append(f"{task}: missing summary file {summary_path}")
            continue
        summary_rows = read_csv_rows(summary_path)
        summary_methods = {str(row.get("method", "")).strip() for row in summary_rows}
        summary_run_ids = {str(row.get("run_id", "")).strip() for row in summary_rows}
        if summary_run_ids != {run_id}:
            errors.append(
                f"{summary_path}: run_id set {sorted(summary_run_ids)} does not match expected [{run_id}]"
            )

        missing_methods = sorted(expected_methods[task] - summary_methods)
        extra_methods = sorted(summary_methods - expected_methods[task])
        if missing_methods:
            errors.append(f"{task}: summary missing methods: {missing_methods}")
        if extra_methods:
            errors.append(f"{task}: summary has unexpected methods: {extra_methods}")

    if errors:
        print("[ERROR] Plan coverage check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("[OK] Plan coverage check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
