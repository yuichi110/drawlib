# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

import math
from typing import Any, cast

import pytest

from drawlib.v0_2.private.l2_types import TypePathPoints
from drawlib.v0_2.private.l5_canvas_utils._utils import (
    get_angle,
    get_center_and_size,
    get_dict_value_none_keys_removed,
    get_distance,
    get_rotated_path_points,
    get_rotated_points,
    minus_2points,
    plus_2points,
)


class TestStandaloneUtils:
    """Unit tests for standalone canvas geometry and dictionary helpers."""

    def test_get_rotated_points(self) -> None:
        """Verifies rotating coordinate points around a custom center point."""
        points = [(10.0, 0.0), (0.0, 10.0)]
        center = (0.0, 0.0)

        # 90 degrees rotation counter-clockwise
        rotated = get_rotated_points(points, center, 90.0)
        assert math.isclose(rotated[0][0], 0.0, abs_tol=1e-5)
        assert math.isclose(rotated[0][1], 10.0, abs_tol=1e-5)
        assert math.isclose(rotated[1][0], -10.0, abs_tol=1e-5)
        assert math.isclose(rotated[1][1], 0.0, abs_tol=1e-5)

    def test_get_rotated_path_points(self) -> None:
        """Verifies rotating nested path points and bezier control coordinate structures."""
        # Mix of coordinates and control coordinate tuples
        path: TypePathPoints = [(10.0, 0.0), ((0.0, 10.0), (10.0, 10.0))]
        center = (0.0, 0.0)

        rotated = get_rotated_path_points(path, center, 90.0)
        pt0 = cast(tuple[float, float], rotated[0])
        assert math.isclose(pt0[0], 0.0, abs_tol=1e-5)
        assert math.isclose(pt0[1], 10.0, abs_tol=1e-5)

        # Rotated control tuple
        control_tuple = cast(tuple[tuple[float, float], tuple[float, float]], rotated[1])
        pt_c0 = control_tuple[0]
        pt_c1 = control_tuple[1]
        # (0, 10) rotated 90 deg -> (-10, 0)
        assert math.isclose(pt_c0[0], -10.0, abs_tol=1e-5)
        assert math.isclose(pt_c0[1], 0.0, abs_tol=1e-5)
        # (10, 10) rotated 90 deg -> (-10, 10)
        assert math.isclose(pt_c1[0], -10.0, abs_tol=1e-5)
        assert math.isclose(pt_c1[1], 10.0, abs_tol=1e-5)

    def test_get_angle(self) -> None:
        """Verifies angle calculations in degrees [0, 360)."""
        # East/Right
        assert get_angle((0.0, 0.0), (10.0, 0.0)) == 0.0
        # North/Up
        assert get_angle((0.0, 0.0), (0.0, 10.0)) == 90.0
        # West/Left
        assert get_angle((0.0, 0.0), (-10.0, 0.0)) == 180.0
        # South/Down
        assert get_angle((0.0, 0.0), (0.0, -10.0)) == 270.0

    def test_get_distance(self) -> None:
        """Verifies Euclidean distance calculations."""
        assert get_distance((0.0, 0.0), (3.0, 4.0)) == 5.0
        assert get_distance((1.0, 1.0), (1.0, 1.0)) == 0.0

    def test_get_center_and_size(self) -> None:
        """Verifies center coordinates and bounding box size calculations."""
        points = [(0.0, 0.0), (10.0, 20.0), (5.0, 10.0)]
        center, size = get_center_and_size(points)
        assert center == (5.0, 10.0)
        assert size == (10.0, 20.0)

    def test_plus_minus_2points(self) -> None:
        """Verifies vector addition and subtraction."""
        assert plus_2points((1.0, 2.0), (3.0, 4.0)) == (4.0, 6.0)
        assert minus_2points((5.0, 7.0), (2.0, 3.0)) == (3.0, 4.0)

    def test_get_dict_value_none_keys_removed(self) -> None:
        """Verifies dictionary keys with None values are removed."""
        d: dict[str, Any] = {"a": 1, "b": None, "c": "hello"}
        assert get_dict_value_none_keys_removed(d) == {"a": 1, "c": "hello"}
