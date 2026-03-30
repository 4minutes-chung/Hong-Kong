import numpy as np


def invert_transforms(
    fc_transformed: np.ndarray,
    cols: list[str],
    transforms: dict,
) -> np.ndarray:
    """Convert transformed forecasts back to level paths."""
    fc_level = fc_transformed.copy()
    for j, col in enumerate(cols):
        info = transforms.get(col, {})
        if info.get("transform") == "first_diff":
            last_lev = info["last_level"]
            fc_level[:, j] = last_lev + np.cumsum(fc_transformed[:, j])
    return fc_level


def shock_in_level_space(
    last_obs: np.ndarray,
    col_idx: int,
    desired_level: float,
    transforms: dict,
    col_name: str,
) -> np.ndarray:
    """
    Apply a level-space scenario value to the model state.
    For differenced variables we map to delta = desired_level - last_level.
    """
    shocked = last_obs.copy()
    info = transforms.get(col_name, {})
    if info.get("transform") == "first_diff":
        current_last_level = info["last_level"]
        shocked[-1, col_idx] = desired_level - current_last_level
    else:
        shocked[-1, col_idx] = desired_level
    return shocked
