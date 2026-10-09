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
from drawlib._core.l3_colors import ColorUtil
from drawlib._core.l3_math import (
    RoutingType,
    Side,
    compute_orthogonal_path,
    get_angle,
    get_center_and_size,
    get_distance,
    get_intermediate_path_point,
    get_intermediate_path_points,
    get_intermediate_paths,
    get_intermediate_point,
    get_intermediate_points,
    get_point_on_ellipse,
    get_rotated_path_points,
    get_rotated_points,
    minus_2points,
    plus_2points,
    rotate_point,
)
from drawlib.canvas import clear
from drawlib.shapes import arrow_polyline
from drawlib.styles import Styles


class TestGeometryMath:
    """Unit tests for geometric transformations and point arithmetic."""

    def test_get_intermediate_point_and_points(self) -> None:
        mid = get_intermediate_point((10.0, 20.0), (30.0, 60.0))
        assert mid == (20.0, 40.0)

        pts = get_intermediate_points((0.0, 0.0), (40.0, 80.0), num=3, include_ends=False)
        assert pts == [(10.0, 20.0), (20.0, 40.0), (30.0, 60.0)]

        pts_ends = get_intermediate_points((0.0, 0.0), (40.0, 80.0), num=3, include_ends=True)
        assert pts_ends == [(0.0, 0.0), (10.0, 20.0), (20.0, 40.0), (30.0, 60.0), (40.0, 80.0)]

        with pytest.raises(ValueError, match="num must be >= 1"):
            get_intermediate_points((0.0, 0.0), (10.0, 10.0), num=0)

    def test_get_intermediate_path_point_and_points(self) -> None:
        # U-shaped path: seg0=60, seg1=80, seg2=60 -> total=200
        u_path = [(10.0, 80.0), (10.0, 20.0), (90.0, 20.0), (90.0, 80.0)]

        # 50% along path is at distance 100 -> midpoint of bottom bar (50, 20)
        mid = get_intermediate_path_point(u_path)
        assert mid == (50.0, 20.0)

        # num=3 -> 25% (dist 50), 50% (dist 100), 75% (dist 150)
        pts = get_intermediate_path_points(u_path, num=3, include_ends=False)
        assert pts == [(10.0, 30.0), (50.0, 20.0), (90.0, 30.0)]

        pts_ends = get_intermediate_path_points(u_path, num=3, include_ends=True)
        assert pts_ends == [
            (10.0, 80.0),
            (10.0, 30.0),
            (50.0, 20.0),
            (90.0, 30.0),
            (90.0, 80.0),
        ]

        # Degenerate zero-length path
        assert get_intermediate_path_point([(5.0, 5.0), (5.0, 5.0)]) == (5.0, 5.0)

        with pytest.raises(ValueError, match="at least 2 points"):
            get_intermediate_path_point([(10.0, 20.0)])

        with pytest.raises(ValueError, match="num must be >= 1"):
            get_intermediate_path_points(u_path, num=0)

    def test_get_intermediate_paths(self) -> None:
        u_path = [(10.0, 80.0), (10.0, 20.0), (90.0, 20.0), (90.0, 80.0)]
        sub_paths = get_intermediate_paths(u_path, num=3, include_ends=False)
        assert sub_paths == [
            [(10.0, 80.0), (10.0, 30.0)],
            [(10.0, 80.0), (10.0, 20.0), (50.0, 20.0)],
            [(10.0, 80.0), (10.0, 20.0), (90.0, 20.0), (90.0, 30.0)],
        ]

        sub_paths_ends = get_intermediate_paths(u_path, num=3, include_ends=True)
        assert len(sub_paths_ends) == 4
        assert sub_paths_ends[-1] == u_path

        # Corner-exact hit: L-path with equal legs (10 + 10 = 20), num=1 (t=0.5 -> dist 10)
        l_path = [(0.0, 10.0), (0.0, 0.0), (10.0, 0.0)]
        l_subs = get_intermediate_paths(l_path, num=1)
        assert l_subs == [[(0.0, 10.0), (0.0, 0.0)]]

    def test_get_intermediate_paths_with_arrow_polyline(self) -> None:
        clear()
        u_path = [(20.0, 75.0), (20.0, 25.0), (80.0, 25.0), (80.0, 75.0)]
        for sub_xys in get_intermediate_paths(u_path, num=20, include_ends=True):
            arrow_polyline(
                sub_xys,
                tail_width=2.5,
                head_width=6.0,
                head_length=6.0,
                style=Styles.PrimaryFlat.patch(shape_r=8.0),
            )
            arrow_polyline(
                sub_xys,
                tail_width=2.5,
                head_width=6.0,
                head_length=6.0,
                head="<->",
                style=Styles.PrimaryFlat.patch(shape_r=8.0),
            )

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
        assert callable(dmath.get_intermediate_point)
        assert callable(dmath.get_intermediate_points)
        assert callable(dmath.get_intermediate_path_point)
        assert callable(dmath.get_intermediate_path_points)
        assert callable(dmath.get_intermediate_paths)


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
        path = compute_orthogonal_path((30.0, 10.0), (10.0, 30.0), start_side="right", end_side="left", offset=5.0)
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
