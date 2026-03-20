"""Aggregate raw experiment outputs into per-task summary CSV files.

This script scans raw result files from:
    <raw-root>/<task>/*.csv

And writes one summary file per task to:
    <summary-root>/<task>.csv

Summary fields:
    task_name, method, n_repeats,
    mse_mean, mse_std, r2_mean, r2_std,
    time_mean, time_std, success_rate
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean, stdev
from typing import Dict, Iterable, List, Tuple


REQUIRED_COLUMNS = {"task_name", "method", "mse", "r2", "time_seconds", "status"}
SUMMARY_COLUMNS = [
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
]


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Aggregate raw experiment CSV files.")
    parser.add_argument(
        "--raw-root",
        type=Path,
        default=Path("output/raw"),
        help="Root directory containing per-task raw CSV files.",
    )
    parser.add_argument(
        "--summary-root",
        type=Path,
        default=Path("output/summary"),
        help="Output directory for per-task summary CSV files.",
    )
    return parser.parse_args()


def iter_task_raw_files(raw_root: Path) -> Iterable[Tuple[str, Path]]:
    """Yield (task_name, csv_path) for all raw CSV files under raw root."""
    if not raw_root.exists():
        return

    for task_dir in sorted(p for p in raw_root.iterdir() if p.is_dir()):
        for csv_path in sorted(task_dir.glob("*.csv")):
            yield task_dir.name, csv_path


def safe_float(value: str) -> float | None:
    """Convert a string value to float, returning None on failure."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def calc_mean_std(values: List[float]) -> Tuple[str, str]:
    """Return mean/std as fixed-point strings for a numeric list."""
    if not values:
        return "", ""
    if len(values) == 1:
        return f"{values[0]:.10g}", "0"
    return f"{mean(values):.10g}", f"{stdev(values):.10g}"


def aggregate_task(csv_files: List[Path], fallback_task_name: str) -> List[Dict[str, str]]:
    """Aggregate one task's raw CSV files into summary rows."""
    grouped: Dict[str, List[Dict[str, str]]] = defaultdict(list)

    for csv_path in csv_files:
        with csv_path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            columns = set(reader.fieldnames or [])
            missing = REQUIRED_COLUMNS - columns
            if missing:
                raise ValueError(
                    f"Missing required columns in {csv_path}: {sorted(missing)}"
                )
            for row in reader:
                method = (row.get("method") or "").strip()
                if not method:
                    continue
                grouped[method].append(row)

    summary_rows: List[Dict[str, str]] = []
    for method in sorted(grouped):
        rows = grouped[method]
        n_repeats = len(rows)
        success_rows = [
            r for r in rows if (r.get("status", "").strip().lower() == "success")
        ]
        success_rate = (len(success_rows) / n_repeats) if n_repeats else 0.0

        mse_values = [v for v in (safe_float(r.get("mse", "")) for r in success_rows) if v is not None]
        r2_values = [v for v in (safe_float(r.get("r2", "")) for r in success_rows) if v is not None]
        time_values = [v for v in (safe_float(r.get("time_seconds", "")) for r in success_rows) if v is not None]

        mse_mean, mse_std = calc_mean_std(mse_values)
        r2_mean, r2_std = calc_mean_std(r2_values)
        time_mean, time_std = calc_mean_std(time_values)

        task_name = (rows[0].get("task_name") or fallback_task_name).strip() or fallback_task_name
        summary_rows.append(
            {
                "task_name": task_name,
                "method": method,
                "n_repeats": str(n_repeats),
                "mse_mean": mse_mean,
                "mse_std": mse_std,
                "r2_mean": r2_mean,
                "r2_std": r2_std,
                "time_mean": time_mean,
                "time_std": time_std,
                "success_rate": f"{success_rate:.10g}",
            }
        )

    return summary_rows


def write_summary_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    """Write summary rows to a CSV file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SUMMARY_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    """Run aggregation for all tasks under raw root."""
    args = parse_args()
    raw_root: Path = args.raw_root
    summary_root: Path = args.summary_root

    task_to_files: Dict[str, List[Path]] = defaultdict(list)
    for task_name, csv_path in iter_task_raw_files(raw_root):
        task_to_files[task_name].append(csv_path)

    if not task_to_files:
        print(f"[WARN] No raw CSV files found under: {raw_root}")
        return

    total_tasks = 0
    total_rows = 0
    for task_name in sorted(task_to_files):
        rows = aggregate_task(task_to_files[task_name], fallback_task_name=task_name)
        out_path = summary_root / f"{task_name}.csv"
        write_summary_csv(out_path, rows)
        total_tasks += 1
        total_rows += len(rows)
        print(f"[OK] Wrote summary: {out_path} ({len(rows)} methods)")

    print(f"[OK] Aggregated {total_rows} method summaries across {total_tasks} tasks")


if __name__ == "__main__":
    main()
