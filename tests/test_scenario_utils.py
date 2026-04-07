"""Direct unit tests for hk_var.scenario_utils (also covered via hk_var_model wrappers)."""

import numpy as np
import pytest

from hk_var.scenario_utils import invert_transforms, shock_in_level_space


class TestInvertTransformsDirect:
    def test_level_columns_unchanged(self):
        fc = np.array([[1.0, 2.0], [3.0, 4.0]])
        transforms = {"a": {"transform": "level"}, "b": {"transform": "level"}}
        out = invert_transforms(fc, ["a", "b"], transforms)
        np.testing.assert_array_equal(out, fc)

    def test_first_diff_cumulates_from_last_level(self):
        fc = np.array([[0.1, 0.0], [0.2, 0.0]])
        transforms = {
            "x": {"transform": "first_diff", "last_level": 5.0},
            "y": {"transform": "level"},
        }
        out = invert_transforms(fc, ["x", "y"], transforms)
        assert out[0, 0] == pytest.approx(5.0 + 0.1)
        assert out[1, 0] == pytest.approx(5.0 + 0.1 + 0.2)
        np.testing.assert_array_equal(out[:, 1], fc[:, 1])

    def test_missing_transform_defaults_to_level_passthrough(self):
        fc = np.array([[2.0]])
        out = invert_transforms(fc, ["z"], {})
        np.testing.assert_array_equal(out, fc)

    def test_does_not_mutate_input_array(self):
        fc = np.array([[0.5]])
        transforms = {"x": {"transform": "first_diff", "last_level": 1.0}}
        orig = fc.copy()
        invert_transforms(fc, ["x"], transforms)
        np.testing.assert_array_equal(fc, orig)


class TestShockInLevelSpaceDirect:
    def test_level_sets_terminal_observation(self):
        last = np.zeros((1, 2))
        transforms = {"a": {"transform": "level"}}
        out = shock_in_level_space(last, 0, 3.5, transforms, "a")
        assert out[-1, 0] == 3.5
        assert out[-1, 1] == 0.0

    def test_first_diff_sets_increment(self):
        last = np.zeros((1, 2))
        transforms = {"b": {"transform": "first_diff", "last_level": 2.0}}
        out = shock_in_level_space(last, 1, 5.0, transforms, "b")
        assert out[-1, 1] == pytest.approx(5.0 - 2.0)

    def test_does_not_mutate_input(self):
        last = np.ones((2, 3))
        orig = last.copy()
        shock_in_level_space(last, 0, 9.0, {"c": {"transform": "level"}}, "c")
        np.testing.assert_array_equal(last, orig)
