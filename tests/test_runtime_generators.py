"""Regression tests for runtime target generators."""

from __future__ import annotations

import unittest

import numpy as np

from scripts.experiment.execution.models import TaskRuntimeConfig
from scripts.experiment.execution.runtime import (
    generate_dataset,
    generate_targets,
    normalize_method_params,
)


class RuntimeGeneratorTests(unittest.TestCase):
    """Keep scripted task generators aligned with experiment notebooks."""

    def test_quadratic_generator_formula(self) -> None:
        x_data = np.array([[0.0], [2.0], [-1.0]])
        y = generate_targets("quadratic", x_data)
        expected = np.array([1.0, 7.0, 1.0])
        np.testing.assert_allclose(y, expected)

    def test_sin_exp_generator_matches_notebook_formula(self) -> None:
        x_data = np.array(
            [
                [0.0, 0.0],
                [1.0, 4.0],
                [-2.0, -4.0],
            ]
        )
        y = generate_targets("sin_exp", x_data)
        expected = np.sin(x_data[:, 0] ** 2) + np.exp(x_data[:, 1] / 4.0) + 1.0
        np.testing.assert_allclose(y, expected)

    def test_dataset_normalization_matches_notebook_mode(self) -> None:
        task_cfg = TaskRuntimeConfig(
            task_name="multivariate_sinexp",
            generator="sin_exp",
            n_var=2,
            ranges=(-4.0, 4.0),
            noise_enabled=False,
            noise_std=0.0,
            normalize_input=True,
            normalize_label=True,
            methods={},
        )
        x_train, y_train, _, _ = generate_dataset(
            task_cfg=task_cfg,
            seed=42,
            train_num=5000,
            test_num=500,
        )
        np.testing.assert_allclose(np.mean(x_train, axis=0), np.zeros(2), atol=5e-2)
        np.testing.assert_allclose(np.std(x_train, axis=0), np.ones(2), atol=5e-2)
        np.testing.assert_allclose(float(np.mean(y_train)), 0.0, atol=5e-2)
        np.testing.assert_allclose(float(np.std(y_train)), 1.0, atol=5e-2)

    def test_gplearn_init_depth_list_is_normalized_to_tuple(self) -> None:
        normalized = normalize_method_params(
            "gplearn",
            default_params={
                "population_size": 20000,
                "generations": 5,
                "init_depth": [4, 10],
                "metric": "mse",
            },
            budget_raw='{"generations_cap": 5}',
            seed=42,
        )
        self.assertEqual(normalized["init_depth"], (4, 10))


if __name__ == "__main__":
    unittest.main()
