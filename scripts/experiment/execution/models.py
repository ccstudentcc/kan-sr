"""Data models used by experiment execution."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Tuple


@dataclass(frozen=True)
class TaskRuntimeConfig:
    """Runtime task config resolved from task YAML."""

    task_name: str
    generator: str
    n_var: int
    ranges: Tuple[float, float]
    noise_enabled: bool
    noise_std: float
    methods: Dict[str, Dict[str, Any]]
