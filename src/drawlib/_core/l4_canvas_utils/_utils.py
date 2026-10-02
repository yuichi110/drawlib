# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""Utility module for canvas math and geometry operations."""

from typing import Any

from drawlib._core.l3_math import (
    get_angle,
    get_center_and_size,
    get_distance,
    get_point_on_ellipse,
    get_rotated_path_points,
    get_rotated_points,
    minus_2points,
    plus_2points,
    rotate_point,
)


def get_dict_value_none_keys_removed(options: dict[str, Any]) -> dict[str, Any]:
    """Return dictionary with None values filtered out.

    Args:
        options: Input dictionary.

    Returns:
        dict[str, Any]: Dictionary without None value entries.
    """
    return {key: value for key, value in options.items() if value is not None}


__all__ = [
    "get_angle",
    "get_center_and_size",
    "get_dict_value_none_keys_removed",
    "get_distance",
    "get_point_on_ellipse",
    "get_rotated_path_points",
    "get_rotated_points",
    "minus_2points",
    "plus_2points",
    "rotate_point",
]
