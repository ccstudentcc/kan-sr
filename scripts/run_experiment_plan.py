import argparse
import copy
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml

SUPPORTED_METHODS = {"kan", "gplearn", "bms", "qlattice"}


def load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data


def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    merged = copy.deepcopy(base)
    for key, value in override.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = copy.deepcopy(value)
    return merged


def validate_config(cfg: Dict[str, Any]) -> None:
    required_top = ["reproducibility", "experiment", "methods", "task", "data", "metrics"]
    for key in required_top:
        if key not in cfg:
            raise ValueError(f"Missing required section: {key}")

    experiment = cfg["experiment"]
    methods_cfg = cfg["methods"]
    if "enabled" not in methods_cfg or not methods_cfg["enabled"]:
        raise ValueError("methods.enabled must be non-empty")

    methods = set(methods_cfg["enabled"])
    unknown = methods - SUPPORTED_METHODS
    if unknown:
        raise ValueError(f"Unsupported methods: {sorted(unknown)}")

    repeats = experiment.get("n_repeats", 1)
    if not isinstance(repeats, int) or repeats <= 0:
        raise ValueError("experiment.n_repeats must be a positive integer")


def resolve_seeds(cfg: Dict[str, Any], repeats: int) -> List[int]:
    seeds = list(cfg["reproducibility"].get("seed_list", []))
    if not seeds:
        seeds = [42]
    if len(seeds) >= repeats:
        return [int(s) for s in seeds[:repeats]]

    base_seed = int(seeds[0])
    extended = [base_seed + i for i in range(repeats)]
    return extended


def resolve_methods(cfg: Dict[str, Any], methods_override: str) -> List[str]:
    if methods_override:
        methods = [m.strip() for m in methods_override.split(",") if m.strip()]
    else:
        methods = list(cfg["methods"]["enabled"])
    unknown = set(methods) - SUPPORTED_METHODS
    if unknown:
        raise ValueError(f"Unsupported methods in override: {sorted(unknown)}")
    return methods


def resolve_budget(cfg: Dict[str, Any], method: str) -> Tuple[Any, Any]:
    budget = cfg.get("budget", {})
    time_budget = budget.get("time_budget_seconds", "")
    per_method = budget.get("per_method", {}).get(method, {})
    return time_budget, per_method


def build_run_plan(
    cfg: Dict[str, Any], methods: List[str], repeats: int, run_id: str
) -> List[Dict[str, Any]]:
    experiment = cfg["experiment"]
    data = cfg["data"]
    metrics = cfg["metrics"]
    split = cfg.get("split", {})
    task = cfg["task"]
    seeds = resolve_seeds(cfg, repeats)
    split_from_seed = bool(split.get("split_seed_from_run_seed", True))
    regression_metrics = list(metrics.get("regression", ["mse", "r2"]))

    plan: List[Dict[str, Any]] = []
    for repeat_idx, run_seed in enumerate(seeds):
        split_seed = run_seed if split_from_seed else int(seeds[0])
        for method in methods:
            time_budget, method_budget = resolve_budget(cfg, method)
            plan.append(
                {
                    "project_name": cfg.get("project", {}).get("name", "KAN-Symbolic_Regression"),
                    "run_id": run_id,
                    "experiment_repeats": int(experiment["n_repeats"]),
                    "task_name": task.get("name", "unknown_task"),
                    "method": method,
                    "repeat_index": repeat_idx,
                    "seed": int(run_seed),
                    "split_seed": int(split_seed),
                    "n_var": data.get("n_var", ""),
                    "train_num": data.get("train_num", ""),
                    "test_num": data.get("test_num", ""),
                    "data_ranges": str(data.get("ranges", "")),
                    "noise_enabled": bool(data.get("noise", {}).get("enabled", False)),
                    "noise_std": data.get("noise", {}).get("std", ""),
                    "budget_time_seconds": time_budget,
                    "budget_method_cap": json.dumps(method_budget, ensure_ascii=False),
                    "report_metrics": ",".join(regression_metrics),
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                }
            )
    return plan


def save_plan(plan: List[Dict[str, Any]], out_dir: Path, run_id: str) -> Dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)

    json_path = out_dir / f"{run_id}_plan.json"
    csv_path = out_dir / f"{run_id}_plan.csv"

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)

    if plan:
        fieldnames = list(plan[0].keys())
        with csv_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(plan)

    return {"json": json_path, "csv": csv_path}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build reproducible experiment run plan.")
    parser.add_argument(
        "--base",
        "--base-config",
        dest="base",
        type=Path,
        default=Path("configs/base.yaml"),
        help="Base config path",
    )
    parser.add_argument(
        "--task",
        "--task-config",
        dest="task",
        type=Path,
        required=True,
        help="Task config path",
    )
    parser.add_argument(
        "--out-dir",
        "--output-root",
        dest="out_dir",
        type=Path,
        default=Path("output"),
        help="Output directory",
    )
    parser.add_argument("--methods", type=str, default="", help="Override methods, comma separated")
    parser.add_argument("--repeats", type=int, default=-1, help="Override repeats")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    base_cfg = load_yaml(args.base)
    task_cfg = load_yaml(args.task)
    cfg = deep_merge(base_cfg, task_cfg)

    methods = resolve_methods(cfg, args.methods)
    repeats = int(cfg.get("experiment", {}).get("n_repeats", 1))
    if args.repeats > 0:
        repeats = args.repeats

    validate_config(cfg)
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    plan = build_run_plan(cfg, methods=methods, repeats=repeats, run_id=run_id)
    paths = save_plan(plan, args.out_dir, run_id)

    print(f"[OK] Built run plan with {len(plan)} runs")
    print(f"[OK] JSON: {paths['json']}")
    print(f"[OK] CSV : {paths['csv']}")


if __name__ == "__main__":
    main()
