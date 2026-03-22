"""Regression tests for script entrypoint compatibility."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class EntrypointCompatTests(unittest.TestCase):
    """Validate that script entrypoints support script and module invocation."""

    def _run(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, *args],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def _assert_help_ok(self, result: subprocess.CompletedProcess[str]) -> None:
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("usage:", result.stdout.lower())

    def test_script_mode_help(self) -> None:
        self._assert_help_ok(self._run("scripts/run_experiment.py", "--help"))
        self._assert_help_ok(self._run("scripts/run_experiment_plan.py", "--help"))
        self._assert_help_ok(self._run("scripts/summarize_results.py", "--help"))

    def test_module_mode_help(self) -> None:
        self._assert_help_ok(self._run("-m", "scripts.run_experiment", "--help"))
        self._assert_help_ok(self._run("-m", "scripts.run_experiment_plan", "--help"))
        self._assert_help_ok(self._run("-m", "scripts.summarize_results", "--help"))


if __name__ == "__main__":
    unittest.main()
