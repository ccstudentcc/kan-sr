"""Regression tests for execution adapter helpers."""

from __future__ import annotations

import unittest

from scripts.experiment.execution.adapters import normalize_kan_width


class AdapterHelperTests(unittest.TestCase):
    """Keep adapter helper behavior stable across refactors."""

    def test_normalize_kan_width_accepts_plain_width(self) -> None:
        self.assertEqual(normalize_kan_width([2, 2, 1], n_var=2), [2, 2, 1])

    def test_normalize_kan_width_accepts_mutated_nested_width(self) -> None:
        self.assertEqual(
            normalize_kan_width([[2, 0], [2, 0], [1, 0]], n_var=2),
            [2, 2, 1],
        )

    def test_normalize_kan_width_falls_back_when_missing(self) -> None:
        self.assertEqual(normalize_kan_width(None, n_var=3), [3, 1])


if __name__ == "__main__":
    unittest.main()
