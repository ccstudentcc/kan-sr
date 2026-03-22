"""Method adapters for experiment execution."""

from __future__ import annotations

import random
import re
import time
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
import sympy as sp
from sklearn.metrics import mean_squared_error, r2_score

_SAFE_EXPR_MAX_LEN = 1024
_SAFE_EXPR_ALLOWED = re.compile(r"^[A-Za-z0-9_+\-*/^().,\s]+$")


def execute_gplearn(
    *,
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_test: np.ndarray,
    y_test: np.ndarray,
    params: Dict[str, Any],
) -> Tuple[float, float, float, str, int]:
    """Train and evaluate one gplearn run."""
    from gplearn.genetic import SymbolicRegressor

    started = time.perf_counter()
    model = SymbolicRegressor(**params)
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    elapsed = time.perf_counter() - started
    mse = float(mean_squared_error(y_test, y_pred))
    r2 = float(r2_score(y_test, y_pred))
    expression = str(model._program) if getattr(model, "_program", None) is not None else ""
    complexity = count_expression_complexity(expression)
    return mse, r2, elapsed, expression, complexity


def normalize_kan_fit_stages(kan_params: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Build normalized fit stages from KAN params."""
    raw_stages = kan_params.get("fit_stages", [])
    stages: List[Dict[str, Any]] = []
    if isinstance(raw_stages, list) and raw_stages:
        for stage in raw_stages:
            if isinstance(stage, dict):
                stages.append(dict(stage))
    if stages:
        return stages
    return [{"opt": "LBFGS", "steps": 20, "lamb": 0.001, "lamb_entropy": 4.0}]


def apply_kan_fit_step_cap(stages: List[Dict[str, Any]], fit_steps_cap: int | None) -> List[Dict[str, Any]]:
    """Apply optional global fit-step cap across all stages."""
    if fit_steps_cap is None or fit_steps_cap <= 0:
        return stages

    remaining = fit_steps_cap
    capped_stages: List[Dict[str, Any]] = []
    for stage in stages:
        if remaining <= 0:
            break
        stage_copy = dict(stage)
        stage_steps = int(stage_copy.get("steps", 20))
        stage_copy["steps"] = max(1, min(stage_steps, remaining))
        remaining -= int(stage_copy["steps"])
        capped_stages.append(stage_copy)
    return capped_stages


def execute_kan(
    *,
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_test: np.ndarray,
    y_test: np.ndarray,
    params: Dict[str, Any],
) -> Tuple[float, float, float, str, int]:
    """Train and evaluate one KAN run using pykan."""
    import torch
    from kan import KAN

    width = params.get("width", [x_train.shape[1], 1])
    grid = int(params.get("grid", 3))
    k = int(params.get("k", 3))
    seed = int(params.get("seed", 0))
    fit_steps_cap_raw = params.get("fit_steps_cap")
    fit_steps_cap = int(fit_steps_cap_raw) if fit_steps_cap_raw is not None else None
    stages = apply_kan_fit_step_cap(normalize_kan_fit_stages(params), fit_steps_cap)
    symbolic_cfg = params.get("symbolic", {})
    enable_auto_symbolic = bool(symbolic_cfg.get("enable_auto_symbolic", False))

    dataset = {
        "train_input": torch.tensor(x_train, dtype=torch.float32),
        "train_label": torch.tensor(y_train.reshape(-1, 1), dtype=torch.float32),
        "test_input": torch.tensor(x_test, dtype=torch.float32),
        "test_label": torch.tensor(y_test.reshape(-1, 1), dtype=torch.float32),
    }

    model = KAN(
        width=width,
        grid=grid,
        k=k,
        seed=seed,
        device="cpu",
        auto_save=False,
    )
    started = time.perf_counter()
    for stage in stages:
        fit_kwargs = {
            "opt": stage.get("opt", "LBFGS"),
            "steps": int(stage.get("steps", 20)),
            "lamb": float(stage.get("lamb", 0.001)),
            "lamb_entropy": float(stage.get("lamb_entropy", 4.0)),
            "log": max(1, int(stage.get("log", 1))),
        }
        optional_keys = [
            "batch",
            "lr",
            "lamb_l1",
            "lamb_coef",
            "lamb_coefdiff",
            "update_grid",
            "grid_update_num",
            "start_grid_update_step",
            "stop_grid_update_step",
        ]
        for key in optional_keys:
            if key in stage:
                fit_kwargs[key] = stage[key]
        model.fit(dataset, **fit_kwargs)

    with torch.no_grad():
        y_pred = model(dataset["test_input"]).detach().cpu().numpy().reshape(-1)
    elapsed = time.perf_counter() - started
    mse = float(mean_squared_error(y_test, y_pred))
    r2 = float(r2_score(y_test, y_pred))

    expression = f"kan_numeric(width={width},grid={grid},k={k})"
    if enable_auto_symbolic:
        try:
            model.auto_symbolic(verbose=0)
            formula_tuple = model.symbolic_formula()
            formula_list = formula_tuple[0] if isinstance(formula_tuple, tuple) else formula_tuple
            if isinstance(formula_list, list) and formula_list:
                expression = str(formula_list[0])
        except Exception:  # noqa: BLE001
            expression = expression

    complexity = count_expression_complexity(expression)
    return mse, r2, elapsed, expression, complexity


def resolve_feature_names(n_var: int, params: Dict[str, Any]) -> List[str]:
    """Resolve feature names for dataframe-based adapters."""
    configured = params.get("features")
    if isinstance(configured, list) and len(configured) == n_var and all(
        isinstance(item, str) and item.strip() for item in configured
    ):
        return [str(item).strip() for item in configured]
    if n_var == 1:
        return ["x"]
    return [f"x{index + 1}" for index in range(n_var)]


def _is_safe_expression_text(expr: str) -> bool:
    """Return True when expression text looks safe to parse via SymPy."""
    text = str(expr).strip()
    if not text:
        return False
    if len(text) > _SAFE_EXPR_MAX_LEN:
        return False
    if "__" in text:
        return False
    return bool(_SAFE_EXPR_ALLOWED.fullmatch(text))


def count_expression_complexity(expr: str) -> int:
    """Count expression complexity as SymPy node count."""
    if not _is_safe_expression_text(expr):
        return 1
    try:
        sx = sp.sympify(expr)
    except Exception:  # noqa: BLE001
        return 1

    def _count_nodes(e: sp.Basic) -> int:
        if e.is_Atom:
            return 1
        return 1 + sum(_count_nodes(arg) for arg in e.args)

    return _count_nodes(sx)


def execute_bms(
    *,
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_test: np.ndarray,
    y_test: np.ndarray,
    params: Dict[str, Any],
) -> Tuple[float, float, float, str, int]:
    """Train and evaluate one BMS run."""
    from autora.theorist.bms import BMSRegressor

    seed = int(params.get("seed", 0))
    epochs = int(params.get("epochs", 200))
    ts = params.get("ts")

    np.random.seed(seed)
    random.seed(seed)
    model_kwargs: Dict[str, Any] = {"epochs": epochs}
    if isinstance(ts, list) and ts:
        model_kwargs["ts"] = ts

    started = time.perf_counter()
    model = BMSRegressor(**model_kwargs)
    model.fit(x_train, y_train)
    y_pred = np.asarray(model.predict(x_test)).reshape(-1)
    elapsed = time.perf_counter() - started

    mse = float(mean_squared_error(y_test, y_pred))
    r2 = float(r2_score(y_test, y_pred))

    model_obj = getattr(model, "model_", None)
    expression = str(model_obj) if model_obj is not None else ""
    complexity = count_expression_complexity(expression)
    return mse, r2, elapsed, expression, complexity


def execute_qlattice(
    *,
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_test: np.ndarray,
    y_test: np.ndarray,
    params: Dict[str, Any],
) -> Tuple[float, float, float, str, int]:
    """Train and evaluate one QLattice run."""
    import feyn

    n_var = x_train.shape[1]
    feature_names = resolve_feature_names(n_var, params)
    target_name = str(params.get("target", "y")).strip() or "y"
    n_epochs = int(params.get("n_epochs", 10))
    n_models_to_eval = int(params.get("n_models_to_eval", 10))
    random_seed_from_run_seed = bool(params.get("random_seed_from_run_seed", True))
    seed = int(params.get("seed", 0))

    train_frame = pd.DataFrame(x_train, columns=feature_names)
    train_frame[target_name] = y_train
    test_frame = pd.DataFrame(x_test, columns=feature_names)

    ql_seed = seed if random_seed_from_run_seed else -1
    started = time.perf_counter()
    qlattice = feyn.QLattice(random_seed=ql_seed)
    candidates = qlattice.auto_run(
        train_frame,
        output_name=target_name,
        n_epochs=max(1, n_epochs),
    )
    if not candidates:
        raise RuntimeError("QLattice returned no candidate models")

    usable = candidates[: max(1, n_models_to_eval)]
    best_model = None
    best_mse = None
    for candidate in usable:
        pred = np.asarray(candidate.predict(test_frame)).reshape(-1)
        candidate_mse = float(mean_squared_error(y_test, pred))
        if best_mse is None or candidate_mse < best_mse:
            best_mse = candidate_mse
            best_model = candidate

    if best_model is None:
        raise RuntimeError("QLattice failed to select best model")

    y_pred = np.asarray(best_model.predict(test_frame)).reshape(-1)
    elapsed = time.perf_counter() - started
    mse = float(mean_squared_error(y_test, y_pred))
    r2 = float(r2_score(y_test, y_pred))

    expression_obj = best_model.sympify(signif=6)
    expression = str(expression_obj)
    complexity = count_expression_complexity(expression)
    return mse, r2, elapsed, expression, complexity
