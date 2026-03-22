"""Shared helper functions for check scripts."""

from __future__ import annotations

from pathlib import Path
from typing import Optional


def latest_plan_json(output_root: Path) -> Optional[Path]:
    """Return latest plan JSON path under output root."""
    plan_dir = output_root / "plan"
    candidates = list(plan_dir.glob("*_plan.json")) if plan_dir.exists() else []
    if not candidates:
        candidates = list(output_root.glob("*_plan.json"))
    if not candidates:
        return None
    return max(candidates, key=lambda path: path.stat().st_mtime)
