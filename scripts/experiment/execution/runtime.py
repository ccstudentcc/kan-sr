"""Runtime config, dataset generation, and parameter normalization."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Dict, Tuple

import numpy as np

from ..shared.config import deep_merge, load_yaml
from ..shared.constants import SUPPORTED_METHODS, SUPPORTED_TASK_GENERATORS
from .models import TaskRuntimeConfig


def parse_positive_int(value: Any, field_name: str) -> int:
    """Parse positive integer value."""
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be int, got: {value}") from exc
    if parsed <= 0:
        raise ValueError(f"{field_name} must be > 0, got: {parsed}")
    return parsed


def parse_seed(value: Any) -> int:
    """Parse seed as int."""
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"seed must be int, got: {value}") from exc


def resolve_run_id(plan_row: Dict[str, Any], fallback: str) -> str:
    """Resolve run_id from plan row with fallback."""
    run_id = str(plan_row.get("run_id", "")).strip()
    return run_id or fallback


def parse_ranges(raw_ranges: Any) -> Tuple[float, float]:
    """Parse data range from config value."""
    try:
        if isinstance(raw_ranges, str):
            values = json.loads(raw_ranges)
        else:
            values = raw_ranges
        if not isinstance(values, list) or len(values) != 2:
            raise ValueError
        low = float(values[0])
        high = float(values[1])
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid data range: {raw_ranges}") from exc
    if not low < high:
        raise ValueError(f"range lower bound must be < upper bound: {raw_ranges}")
    return low, high


def find_task_config_path(task_name: str, tasks_dir: Path = Path("configs/tasks")) -> Path:
    """Find task yaml path by matching task.name."""
    for task_path in sorted(tasks_dir.glob("*.yaml")):
        task_cfg = load_yaml(task_path)
        cfg_task_name = str(task_cfg.get("task", {}).get("name", "")).strip()
        if cfg_task_name == task_name:
            return task_path
    raise FileNotFoundError(f"Task config not found for task_name: {task_name}")


def resolve_task_runtime_config(task_name: str) -> TaskRuntimeConfig:
    """Resolve runtime task config by deep merging base+task YAML."""
    base_cfg = load_yaml(Path("configs/base.yaml"))
    task_cfg = load_yaml(find_task_config_path(task_name))
    merged = deep_merge(base_cfg, task_cfg)
    data_cfg = merged.get("data", {})
    generator = str(data_cfg.get("generator", "")).strip()
    if generator not in SUPPORTED_TASK_GENERATORS:
        raise ValueError(f"unsupported generator '{generator}' for task '{task_name}'")
    n_var = parse_positive_int(data_cfg.get("n_var"), "data.n_var")
    ranges = parse_ranges(data_cfg.get("ranges"))
    noise_cfg = data_cfg.get("noise", {})
    noise_enabled = bool(noise_cfg.get("enabled", False))
    noise_std = float(noise_cfg.get("std", 0.0))
    methods_cfg = merged.get("methods", {})
    methods = {
        method_name: dict(methods_cfg.get(method_name, {}).get("params", {}))
        for method_name in SUPPORTED_METHODS
    }
    return TaskRuntimeConfig(
        task_name=task_name,
        generator=generator,
        n_var=n_var,
        ranges=ranges,
        noise_enabled=noise_enabled,
        noise_std=noise_std,
        methods=methods,
    )


def generate_targets(generator: str, x_data: np.ndarray) -> np.ndarray:
    """Generate target values by task generator."""
    if generator == "quadratic":
        x = x_data[:, 0]
        return x**2 + x + 1.0
    if generator == "sin_exp":
        x1 = x_data[:, 0]
        x2 = x_data[:, 1]
        return x2 * np.exp(np.sin(np.pi * x1) + x1**2)
    raise ValueError(f"unsupported generator: {generator}")


def generate_dataset(
    *,
    task_cfg: TaskRuntimeConfig,
    seed: int,
    train_num: int,
    test_num: int,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Generate deterministic train/test dataset for one run."""
    low, high = task_cfg.ranges
    rng = np.random.default_rng(seed)
    x_train = rng.uniform(low=low, high=high, size=(train_num, task_cfg.n_var))
    x_test = rng.uniform(low=low, high=high, size=(test_num, task_cfg.n_var))
    y_train = generate_targets(task_cfg.generator, x_train)
    y_test = generate_targets(task_cfg.generator, x_test)

    if task_cfg.noise_enabled and task_cfg.noise_std > 0:
        y_train = y_train + rng.normal(loc=0.0, scale=task_cfg.noise_std, size=train_num)
    return x_train, y_train, x_test, y_test


def normalize_method_params(
    method: str, default_params: Dict[str, Any], budget_raw: str, seed: int
) -> Dict[str, Any]:
    """Prepare method params from config and plan budget caps."""
    params = copy.deepcopy(default_params)
    try:
        budget_cap = json.loads(str(budget_raw)) if str(budget_raw).strip() else {}
    except json.JSONDecodeError:
        budget_cap = {}

    if method == "gplearn":
        params.pop("random_state_from_run_seed", None)
        if "generations_cap" in budget_cap:
            params["generations"] = int(budget_cap["generations_cap"])
        params["random_state"] = seed
        metric = str(params.get("metric", "mse")).strip().lower()
        params["metric"] = "mse" if metric in {"mse", "mean_squared_error"} else metric
        return params

    if method == "kan":
        params["seed"] = seed
        if "fit_steps_cap" in budget_cap:
            params["fit_steps_cap"] = int(budget_cap["fit_steps_cap"])
        return params

    if method == "bms":
        if "epochs_cap" in budget_cap:
            params["epochs"] = int(budget_cap["epochs_cap"])
        params["seed"] = seed
        return params

    if method == "qlattice":
        if "n_models_cap" in budget_cap:
            params["n_models_to_eval"] = int(budget_cap["n_models_cap"])
        params["seed"] = seed
        return params

    return params
