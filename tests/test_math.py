# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Tests for drawlib.math and _core.l3_math modules."""

from __future__ import annotations

import math
from typing import cast

import pytest

import drawlib.math as dmath
from drawlib._core.l2_types import Bezier2, PathPoints
from drawlib._core.l3_math import (
    RoutingType,
    Side,
    compute_orthogonal_path,
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
from drawlib._core.l4_canvas_utils import ColorUtil


class TestGeometryMath:
    """Unit tests for geometric transformations and point arithmetic."""

    def test_rotate_point_origin(self) -> None:
        # Rotating (1, 0) by 90 degrees around origin -> (0, 1)
        res = rotate_point((1.0, 0.0), angle=90.0)
        assert pytest.approx(res[0], abs=1e-5) == 0.0
        assert pytest.approx(res[1], abs=1e-5) == 1.0

    def test_rotate_point_custom_center(self) -> None:
        # Rotating (3, 2) by 180 degrees around (2, 2) -> (1, 2)
        res = rotate_point((3.0, 2.0), angle=180.0, center=(2.0, 2.0))
        assert pytest.approx(res[0], abs=1e-5) == 1.0
        assert pytest.approx(res[1], abs=1e-5) == 2.0

    def test_get_point_on_ellipse(self) -> None:
        # Width=20 (rx=10), Height=10 (ry=5)
        # 0 deg -> right edge (cx + 10, cy)
        pt_right = get_point_on_ellipse(center=(50.0, 50.0), width=20.0, height=10.0, angle=0.0)
        assert pytest.approx(pt_right[0], abs=1e-5) == 60.0
        assert pytest.approx(pt_right[1], abs=1e-5) == 50.0

        # 90 deg -> top edge (cx, cy + 5)
        pt_top = get_point_on_ellipse(center=(50.0, 50.0), width=20.0, height=10.0, angle=90.0)
        assert pytest.approx(pt_top[0], abs=1e-5) == 50.0
        assert pytest.approx(pt_top[1], abs=1e-5) == 55.0

    def test_get_rotated_points(self) -> None:
        pts = [(1.0, 0.0), (0.0, 1.0)]
        rotated = get_rotated_points(pts, center=(0.0, 0.0), angle=90.0)
        assert pytest.approx(rotated[0][0], abs=1e-5) == 0.0
        assert pytest.approx(rotated[0][1], abs=1e-5) == 1.0
        assert pytest.approx(rotated[1][0], abs=1e-5) == -1.0
        assert pytest.approx(rotated[1][1], abs=1e-5) == 0.0

    def test_get_rotated_path_points(self) -> None:
        # Mix of flat (x, y) and bezier ((x1, y1), (x2, y2))
        path_pts: PathPoints = [(1.0, 0.0), ((2.0, 0.0), (3.0, 0.0))]
        rotated = get_rotated_path_points(path_pts, center=(0.0, 0.0), angle=90.0)
        assert pytest.approx(rotated[0][0], abs=1e-5) == 0.0
        assert pytest.approx(rotated[0][1], abs=1e-5) == 1.0
        bezier_seg = cast(Bezier2, rotated[1])
        assert isinstance(bezier_seg, tuple)
        assert pytest.approx(bezier_seg[0][0], abs=1e-5) == 0.0
        assert pytest.approx(bezier_seg[0][1], abs=1e-5) == 2.0
        assert pytest.approx(bezier_seg[1][0], abs=1e-5) == 0.0
        assert pytest.approx(bezier_seg[1][1], abs=1e-5) == 3.0

    def test_get_angle(self) -> None:
        assert pytest.approx(get_angle((0.0, 0.0), (1.0, 0.0)), abs=1e-5) == 0.0
        assert pytest.approx(get_angle((0.0, 0.0), (0.0, 1.0)), abs=1e-5) == 90.0
        assert pytest.approx(get_angle((0.0, 0.0), (-1.0, 0.0)), abs=1e-5) == 180.0
        assert pytest.approx(get_angle((0.0, 0.0), (0.0, -1.0)), abs=1e-5) == 270.0

    def test_get_distance(self) -> None:
        assert pytest.approx(get_distance((0.0, 0.0), (3.0, 4.0)), abs=1e-5) == 5.0

    def test_get_center_and_size(self) -> None:
        pts = [(10.0, 20.0), (30.0, 40.0)]
        center, size = get_center_and_size(pts)
        assert center == (20.0, 30.0)
        assert size == (20.0, 20.0)

    def test_get_center_and_size_empty_error(self) -> None:
        with pytest.raises(ValueError, match="must not be empty"):
            get_center_and_size([])

    def test_vector_arithmetic(self) -> None:
        assert plus_2points((1.0, 2.0), (3.0, 4.0)) == (4.0, 6.0)
        assert minus_2points((5.0, 7.0), (2.0, 3.0)) == (3.0, 4.0)

    def test_public_facade_exports(self) -> None:
        # Ensure drawlib.math exposes the expected symbols
        assert callable(dmath.compute_orthogonal_path)
        assert callable(dmath.rotate_point)
        assert callable(dmath.get_point_on_ellipse)
        assert callable(dmath.get_angle)
        assert callable(dmath.get_distance)
        assert callable(dmath.get_center_and_size)


class TestOrthogonalRouting:
    """Unit tests for orthogonal path routing."""

    def test_direct_routing(self) -> None:
        path = compute_orthogonal_path((0.0, 0.0), (10.0, 20.0), routing="direct")
        assert path == [(0.0, 0.0), (10.0, 20.0)]

    def test_collinear_shortcut(self) -> None:
        # Same X or same Y
        path_h = compute_orthogonal_path((0.0, 10.0), (20.0, 10.0))
        assert path_h == [(0.0, 10.0), (20.0, 10.0)]
        path_v = compute_orthogonal_path((10.0, 0.0), (10.0, 20.0))
        assert path_v == [(10.0, 0.0), (10.0, 20.0)]

    def test_horizontal_forward_routing(self) -> None:
        # Right exit to Left entry (ex > sx)
        path = compute_orthogonal_path((10.0, 10.0), (30.0, 30.0), start_side="right", end_side="left")
        assert path == [(10.0, 10.0), (20.0, 10.0), (20.0, 30.0), (30.0, 30.0)]

    def test_horizontal_backward_routing_with_offset(self) -> None:
        # Right exit to Left entry but target is behind (ex < sx)
        path = compute_orthogonal_path(
            (30.0, 10.0), (10.0, 30.0), start_side="right", end_side="left", offset=5.0
        )
        assert len(path) == 6
        assert path[0] == (30.0, 10.0)
        assert path[1] == (35.0, 10.0)
        assert path[2] == (35.0, 20.0)
        assert path[3] == (5.0, 20.0)
        assert path[4] == (5.0, 30.0)
        assert path[5] == (10.0, 30.0)

    def test_vertical_forward_routing(self) -> None:
        # Top exit to Bottom entry (ey > sy)
        path = compute_orthogonal_path((10.0, 10.0), (30.0, 30.0), start_side="top", end_side="bottom")
        assert path == [(10.0, 10.0), (10.0, 20.0), (30.0, 20.0), (30.0, 30.0)]

    def test_perpendicular_routing(self) -> None:
        # Right exit to Bottom entry
        path = compute_orthogonal_path((10.0, 10.0), (30.0, 30.0), start_side="right", end_side="bottom")
        assert path == [(10.0, 10.0), (30.0, 10.0), (30.0, 30.0)]


class TestColorContrastUtil:
    """Unit tests for ColorUtil contrast and luminance calculations."""

    def test_luminance_black_and_white(self) -> None:
        lum_white = ColorUtil.get_luminance((255, 255, 255))
        assert pytest.approx(lum_white, abs=1e-3) == 1.0

        lum_black = ColorUtil.get_luminance((0, 0, 0))
        assert pytest.approx(lum_black, abs=1e-3) == 0.0

    def test_contrast_text_transparent_background(self) -> None:
        assert ColorUtil.get_contrast_text_color(None) == (40, 40, 40, 1.0)
        assert ColorUtil.get_contrast_text_color((255, 255, 255, 0.0)) == (40, 40, 40, 1.0)
        # Low alpha (< 0.3)
        assert ColorUtil.get_contrast_text_color((255, 255, 255, 0.1)) == (40, 40, 40, 1.0)

    def test_contrast_text_bright_and_dark_backgrounds(self) -> None:
        # Pure white bg -> dark text
        assert ColorUtil.get_contrast_text_color((255, 255, 255)) == (40, 40, 40, 1.0)
        # Pure black bg -> light text
        assert ColorUtil.get_contrast_text_color((0, 0, 0)) == (255, 255, 255, 1.0)
        # Deep blue -> light text
        assert ColorUtil.get_contrast_text_color((20, 30, 80)) == (255, 255, 255, 1.0)
        # Yellow -> dark text
        assert ColorUtil.get_contrast_text_color((255, 255, 0)) == (40, 40, 40, 1.0)

    def test_contrast_text_custom_colors_and_threshold(self) -> None:
        res = ColorUtil.get_contrast_text_color(
            (0, 0, 0),
            dark_color=(10, 10, 10, 1.0),
            light_color=(240, 240, 240, 1.0),
        )
        assert res == (240, 240, 240, 1.0)
