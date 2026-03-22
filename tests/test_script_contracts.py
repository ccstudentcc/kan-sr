"""Regression tests for shared script contracts and helpers."""

from __future__ import annotations

import shutil
import time
import unittest
from pathlib import Path

from scripts.checks.common import latest_plan_json
from scripts.checks.check_output_schema import (
    ENV_REQUIRED_FIELDS_SET,
    PLAN_REQUIRED_FIELDS_SET,
    RAW_REQUIRED_FIELDS,
    SUMMARY_REQUIRED_FIELDS,
)
from scripts.experiment.shared.contracts import (
    ENV_REQUIRED_FIELDS,
    PLAN_REQUIRED_FIELDS,
    RAW_OUTPUT_FIELDS,
    SUMMARY_OUTPUT_FIELDS,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


class ScriptContractTests(unittest.TestCase):
    """Keep artifact field contracts and plan discovery logic in sync."""

    def test_schema_sets_match_shared_contracts(self) -> None:
        self.assertSetEqual(RAW_REQUIRED_FIELDS, set(RAW_OUTPUT_FIELDS))
        self.assertSetEqual(SUMMARY_REQUIRED_FIELDS, set(SUMMARY_OUTPUT_FIELDS))
        self.assertSetEqual(PLAN_REQUIRED_FIELDS_SET, set(PLAN_REQUIRED_FIELDS))
        self.assertSetEqual(ENV_REQUIRED_FIELDS_SET, set(ENV_REQUIRED_FIELDS))

    def test_latest_plan_json_prefers_plan_dir(self) -> None:
        root = REPO_ROOT / "output" / "_tmp_latest_plan_json_case"
        shutil.rmtree(root, ignore_errors=True)
        plan_dir = root / "plan"
        plan_dir.mkdir(parents=True, exist_ok=True)

        root_legacy = root / "20240101_010101_plan.json"
        new_plan = plan_dir / "20240101_020202_plan.json"
        root_legacy.write_text("[]", encoding="utf-8")
        time.sleep(0.02)
        new_plan.write_text("[]", encoding="utf-8")

        picked = latest_plan_json(root)
        self.assertIsNotNone(picked)
        self.assertEqual(picked, new_plan)
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
