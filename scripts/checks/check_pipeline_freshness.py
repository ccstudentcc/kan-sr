"""Check timestamp freshness across plan/raw/summary artifacts.

The freshness contract is:
1) raw artifacts must not be older than the selected plan JSON.
2) summary artifact must not be older than any raw artifact of the same task.
3) summary artifact must not be older than the selected plan JSON.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set


@dataclass(frozen=True)
class TaskArtifacts:
    """Track per-task raw and summary artifacts."""

    task_name: str
    raw_files: List[Path]
    summary_file: Optional[Path]


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Validate freshness ordering for plan/raw/summary artifacts."
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("output"),
        help="Output root directory containing plan/raw/summary artifacts.",
    )
    parser.add_argument(
        "--plan-json",
        type=Path,
        default=None,
        help="Optional explicit plan JSON path. Defaults to latest plan under output/plan or output root.",
    )
    parser.add_argument(
        "--tolerance-seconds",
        type=float,
        default=1.0,
        help="Allowed negative timestamp drift in seconds to avoid filesystem precision false positives.",
    )
    return parser.parse_args()


def to_iso(path: Path) -> str:
    """Format file mtime as ISO string for diagnostics."""
    return datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds")


def latest_plan_json(output_root: Path) -> Optional[Path]:
    """Return latest plan JSON under output root, or None if absent."""
    plan_dir = output_root / "plan"
    candidates = list(plan_dir.glob("*_plan.json")) if plan_dir.exists() else []
    if not candidates:
        candidates = list(output_root.glob("*_plan.json"))
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def load_plan_tasks(plan_json: Path) -> List[str]:
    """Load unique task names from plan JSON records."""
    data = json.loads(plan_json.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"Plan file is not a JSON list: {plan_json}")

    tasks: List[str] = []
    seen = set()
    for index, record in enumerate(data):
        if not isinstance(record, dict):
            raise ValueError(f"Plan record {index} is not an object: {plan_json}")
        task_name = record.get("task_name")
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError(f"Plan record {index} missing valid task_name: {plan_json}")
        if task_name not in seen:
            seen.add(task_name)
            tasks.append(task_name)
    return tasks


def load_plan_run_id(plan_json: Path) -> str:
    """Load single run_id from plan JSON."""
    data = json.loads(plan_json.read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data:
        raise ValueError(f"Plan file must be a non-empty JSON list: {plan_json}")
    run_ids: Set[str] = set()
    for index, record in enumerate(data):
        if not isinstance(record, dict):
            raise ValueError(f"Plan record {index} is not an object: {plan_json}")
        run_id = str(record.get("run_id", "")).strip()
        if not run_id:
            raise ValueError(f"Plan record {index} missing run_id: {plan_json}")
        run_ids.add(run_id)
    if len(run_ids) != 1:
        raise ValueError(f"Plan has multiple run_id values: {sorted(run_ids)}")
    return next(iter(run_ids))


def read_run_ids_from_csv(path: Path) -> Set[str]:
    """Read unique run_id values from CSV rows."""
    with path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    return {str(row.get("run_id", "")).strip() for row in rows}


def collect_task_artifacts(output_root: Path, tasks: Iterable[str]) -> Dict[str, TaskArtifacts]:
    """Collect raw and summary files for each task from output root."""
    raw_root = output_root / "raw"
    summary_root = output_root / "summary"

    artifacts: Dict[str, TaskArtifacts] = {}
    for task_name in tasks:
        raw_files = sorted((raw_root / task_name).glob("*.csv"))
        summary_file = summary_root / f"{task_name}.csv"
        artifacts[task_name] = TaskArtifacts(
            task_name=task_name,
            raw_files=raw_files,
            summary_file=summary_file if summary_file.exists() else None,
        )
    return artifacts


def main() -> int:
    """Run freshness checks and return process exit code."""
    args = parse_args()
    output_root = args.output_root
    tolerance_seconds = args.tolerance_seconds
    errors: List[str] = []

    if not output_root.exists() or not output_root.is_dir():
        print(f"[ERROR] Output root does not exist or is not a directory: {output_root}")
        return 1

    plan_json = args.plan_json if args.plan_json is not None else latest_plan_json(output_root)
    if plan_json is None:
        print(f"[ERROR] No plan JSON found under: {output_root}")
        return 1
    if not plan_json.exists():
        print(f"[ERROR] Plan JSON does not exist: {plan_json}")
        return 1

    try:
        task_names = load_plan_tasks(plan_json)
        plan_run_id = load_plan_run_id(plan_json)
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"[ERROR] {exc}")
        return 1

    if not task_names:
        print(f"[ERROR] No tasks found in plan JSON: {plan_json}")
        return 1

    plan_mtime = plan_json.stat().st_mtime
    artifacts = collect_task_artifacts(output_root, task_names)

    for task_name, task_artifacts in artifacts.items():
        if not task_artifacts.raw_files:
            errors.append(
                f"{task_name}: no raw csv found under {output_root / 'raw' / task_name}"
            )
            continue

        for raw_file in task_artifacts.raw_files:
            raw_mtime = raw_file.stat().st_mtime
            if raw_mtime + tolerance_seconds < plan_mtime:
                errors.append(
                    f"{task_name}: raw older than plan "
                    f"({raw_file} @ {to_iso(raw_file)} < {plan_json} @ {to_iso(plan_json)})"
                )
            raw_run_ids = read_run_ids_from_csv(raw_file)
            if raw_run_ids != {plan_run_id}:
                errors.append(
                    f"{task_name}: raw file run_id mismatch in {raw_file}; "
                    f"expected [{plan_run_id}], got {sorted(raw_run_ids)}"
                )

        summary_file = task_artifacts.summary_file
        if summary_file is None:
            errors.append(
                f"{task_name}: summary missing ({output_root / 'summary' / f'{task_name}.csv'})"
            )
            continue

        summary_mtime = summary_file.stat().st_mtime
        if summary_mtime + tolerance_seconds < plan_mtime:
            errors.append(
                f"{task_name}: summary older than plan "
                f"({summary_file} @ {to_iso(summary_file)} < {plan_json} @ {to_iso(plan_json)})"
            )
        summary_run_ids = read_run_ids_from_csv(summary_file)
        if summary_run_ids != {plan_run_id}:
            errors.append(
                f"{task_name}: summary run_id mismatch in {summary_file}; "
                f"expected [{plan_run_id}], got {sorted(summary_run_ids)}"
            )

        newest_raw_mtime = max(raw_file.stat().st_mtime for raw_file in task_artifacts.raw_files)
        if summary_mtime + tolerance_seconds < newest_raw_mtime:
            newest_raw_file = max(task_artifacts.raw_files, key=lambda path: path.stat().st_mtime)
            errors.append(
                f"{task_name}: summary older than raw "
                f"({summary_file} @ {to_iso(summary_file)} < "
                f"{newest_raw_file} @ {to_iso(newest_raw_file)})"
            )

    if errors:
        print("[ERROR] Pipeline freshness check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("[OK] Pipeline freshness check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
