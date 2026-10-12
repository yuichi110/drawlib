# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Extended geometry builders for polygonal canvas shapes."""

from __future__ import annotations

import math

from matplotlib.path import Path

from drawlib._core.l2_types import Coordinate
from drawlib._core.l3_math import rotate_point
from drawlib._core.l4_canvas._shapes._basic_ext import _arc_points_local, _subpaths_to_compound_path
from drawlib._core.l4_canvas._shapes._util import ShapeUtil

_LIGHTNING_RAW_SPECS: dict[str, list[Coordinate]] = {
    "flat": [
        (-0.18, 0.50),
        (0.42, 0.50),
        (-0.04, 0.04),
        (0.28, 0.04),
        (-0.42, -0.50),
        (-0.08, -0.06),
        (-0.40, -0.06),
    ],
    "standard": [
        (0.22, 0.50),
        (-0.44, -0.06),
        (-0.02, -0.06),
        (-0.22, -0.50),
        (0.44, 0.06),
        (0.04, 0.06),
    ],
    "flat_double": [
        (-0.12, 0.50),
        (0.46, 0.50),
        (0.12, 0.20),
        (0.34, 0.20),
        (-0.02, -0.08),
        (0.22, -0.08),
        (-0.46, -0.50),
        (-0.20, -0.14),
        (-0.42, -0.14),
        (-0.14, 0.14),
        (-0.34, 0.14),
    ],
    "double": [
        (0.32, 0.50),
        (-0.36, 0.08),
        (-0.08, 0.08),
        (-0.42, -0.18),
        (-0.14, -0.18),
        (-0.34, -0.50),
        (0.34, -0.08),
        (0.08, -0.08),
        (0.42, 0.18),
        (0.14, 0.18),
    ],
    "angled": [
        (0.26, 0.50),
        (-0.42, 0.02),
        (-0.10, -0.08),
        (-0.32, -0.50),
        (0.42, -0.02),
        (0.10, 0.08),
    ],
    "slanted": [
        (0.30, 0.50),
        (-0.46, -0.08),
        (-0.04, -0.02),
        (-0.28, -0.50),
        (0.46, 0.08),
        (0.04, 0.02),
    ],
}

_EXPLOSION_STANDARD_SPECS: list[tuple[float, float]] = [
    (12.0, 1.00),
    (28.0, 0.56),
    (46.0, 0.92),
    (64.0, 0.54),
    (84.0, 0.98),
    (104.0, 0.56),
    (124.0, 0.90),
    (144.0, 0.54),
    (166.0, 0.96),
    (186.0, 0.58),
    (206.0, 0.92),
    (225.0, 0.52),
    (246.0, 0.98),
    (266.0, 0.55),
    (286.0, 0.90),
    (306.0, 0.54),
    (328.0, 0.96),
    (348.0, 0.58),
]

_EXPLOSION_HEAVY_SPECS: list[tuple[float, float]] = [
    (8.0, 1.00),
    (20.0, 0.52),
    (33.0, 0.88),
    (45.0, 0.50),
    (58.0, 0.98),
    (71.0, 0.54),
    (84.0, 0.90),
    (97.0, 0.48),
    (111.0, 0.96),
    (124.0, 0.52),
    (138.0, 0.86),
    (151.0, 0.50),
    (165.0, 1.00),
    (178.0, 0.54),
    (192.0, 0.90),
    (205.0, 0.48),
    (219.0, 0.96),
    (232.0, 0.52),
    (246.0, 0.88),
    (259.0, 0.50),
    (273.0, 0.98),
    (286.0, 0.54),
    (300.0, 0.90),
    (313.0, 0.48),
    (327.0, 0.96),
    (340.0, 0.52),
    (352.0, 0.88),
    (360.0, 0.54),
]


def build_lightning_path(
    xy: Coordinate,
    width: float,
    height: float,
    variant: str,
    mirror: bool,
    shape_r: float | tuple[float, ...] | None,
    angle: float,
) -> Path:
    """Build world-space Matplotlib Path for lightning shape variants."""
    cx, cy = xy
    key_map = {
        "sharp": "standard",
        "flat_top": "flat",
        "sharp_double": "double",
        "dynamic": "slanted",
    }
    raw = _LIGHTNING_RAW_SPECS.get(key_map.get(variant, variant), _LIGHTNING_RAW_SPECS["standard"])

    xs = [p[0] for p in raw]
    ys = [p[1] for p in raw]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    span_x = max(max_x - min_x, 1e-6)
    span_y = max(max_y - min_y, 1e-6)
    mx = 0.5 * (min_x + max_x)
    my = 0.5 * (min_y + max_y)

    world_pts: list[Coordinate] = []
    for px, py in raw:
        nx = (px - mx) / span_x
        if mirror:
            nx = -nx
        ny = (py - my) / span_y
        rx, ry = rotate_point((nx * width, ny * height), angle=angle)
        world_pts.append((cx + rx, cy + ry))

    path_points = ShapeUtil.round_polygon_points(world_pts, shape_r)
    return ShapeUtil.build_matplotlib_path(path_points)


def build_explosion_path(
    xy: Coordinate,
    width: float,
    height: float,
    variant: str,
    shape_r: float | tuple[float, ...] | None,
    angle: float,
) -> Path:
    """Build world-space Matplotlib Path for explosion shape variants."""
    cx, cy = xy
    hw, hh = width / 2.0, height / 2.0

    if variant in {"curved", "comic"}:
        peaks = [
            (15.0, 1.00),
            (55.0, 0.94),
            (95.0, 0.98),
            (140.0, 0.92),
            (188.0, 1.00),
            (232.0, 0.92),
            (278.0, 0.98),
            (325.0, 0.94),
        ]
        local_pts: list[Coordinate] = []
        n_p = len(peaks)
        for i in range(n_p):
            a0, r0 = peaks[i]
            a1, r1 = peaks[(i + 1) % n_p]
            if a1 < a0:
                a1 += 360.0
            p0 = (hw * r0 * math.cos(math.radians(a0)), hh * r0 * math.sin(math.radians(a0)))
            p1 = (hw * r1 * math.cos(math.radians(a1)), hh * r1 * math.sin(math.radians(a1)))
            a_mid = 0.5 * (a0 + a1)
            p_mid = (hw * 0.58 * math.cos(math.radians(a_mid)), hh * 0.58 * math.sin(math.radians(a_mid)))
            for step in range(8):
                t = step / 8.0
                omt = 1.0 - t
                qx = omt * omt * p0[0] + 2.0 * omt * t * p_mid[0] + t * t * p1[0]
                qy = omt * omt * p0[1] + 2.0 * omt * t * p_mid[1] + t * t * p1[1]
                local_pts.append((qx, qy))
        return _subpaths_to_compound_path([local_pts], cx, cy, angle)

    specs = _EXPLOSION_HEAVY_SPECS if variant in {"heavy", "wild"} else _EXPLOSION_STANDARD_SPECS
    world_pts: list[Coordinate] = []
    for a_deg, r_scale in specs:
        lx = hw * r_scale * math.cos(math.radians(a_deg))
        ly = hh * r_scale * math.sin(math.radians(a_deg))
        rx, ry = rotate_point((lx, ly), angle=angle)
        world_pts.append((cx + rx, cy + ry))

    path_points = ShapeUtil.round_polygon_points(world_pts, shape_r)
    return ShapeUtil.build_matplotlib_path(path_points)


def build_tag_path_and_center(
    xy: Coordinate,
    width: float,
    height: float,
    variant: str,
    mirror: bool,
    hole_ratio: float | None,
    shape_r: float | tuple[float, ...] | None,
    angle: float,
) -> tuple[Path, Coordinate]:
    """Build compound Path and rotated text center for tag shape variants."""
    cx, cy = xy
    hw, hh = width / 2.0, height / 2.0
    tip_w = min(height * 0.55, width * 0.32)
    h_ratio = 0.24 if hole_ratio is None else float(hole_ratio)
    hole_r = min(height * 0.36, tip_w * 0.45) * (h_ratio / 0.24)
    hole_r = min(hole_r, min(width, height) * 0.35)
    hole_lx = hw - tip_w * 0.78
    text_lx = -tip_w * 0.28

    if variant in {"rounded"}:
        r_end = hh
        x_arc = max(-hw + r_end * 0.2, hw - r_end)
        local_outer = [(-hw, -hh), *_arc_points_local(x_arc, 0.0, r_end, -90.0, 90.0, 24), (-hw, hh)]
    elif variant in {"chamfered", "beveled"}:
        ch_y = hh * 0.38
        local_outer = [
            (-hw, -hh),
            (hw - tip_w, -hh),
            (hw, -ch_y),
            (hw, ch_y),
            (hw - tip_w, hh),
            (-hw, hh),
        ]
    else:
        # "angled" or "standard"
        local_outer = [
            (-hw, -hh),
            (hw - tip_w, -hh),
            (hw, 0.0),
            (hw - tip_w, hh),
            (-hw, hh),
        ]

    if mirror:
        local_outer = [(-px, py) for px, py in reversed(local_outer)]
        hole_lx = -hole_lx
        text_lx = -text_lx

    world_outer: list[Coordinate] = []
    for lx, ly in local_outer:
        rx, ry = rotate_point((lx, ly), angle=angle)
        world_outer.append((cx + rx, cy + ry))

    if variant != "rounded" and shape_r is not None:
        outer_path = ShapeUtil.build_matplotlib_path(ShapeUtil.round_polygon_points(world_outer, shape_r))
    else:
        outer_path = _subpaths_to_compound_path([local_outer], cx, cy, angle)

    hole_cw = _arc_points_local(hole_lx, 0.0, hole_r, 360.0, 0.0, 32)[:-1]
    hole_path = _subpaths_to_compound_path([hole_cw], cx, cy, angle)
    tx_r, ty_r = rotate_point((text_lx, 0.0), angle=angle)
    return Path.make_compound_path(outer_path, hole_path), (cx + tx_r, cy + ty_r)


def build_plaque_path(
    xy: Coordinate,
    width: float,
    height: float,
    variant: str,
    cut_ratio: float | None,
    shape_r: float | tuple[float, ...] | None,
    angle: float,
) -> Path:
    """Build world-space Matplotlib Path for plaque shape variants."""
    cx, cy = xy
    hw, hh = width / 2.0, height / 2.0
    c_ratio = 0.22 if cut_ratio is None else float(cut_ratio)
    r = min(width, height) * min(0.45, c_ratio)

    if variant in {"concave", "standard"}:
        local_pts = (
            _arc_points_local(hw, -hh, r, 180.0, 90.0, 12)
            + _arc_points_local(hw, hh, r, 270.0, 180.0, 12)
            + _arc_points_local(-hw, hh, r, 0.0, -90.0, 12)
            + _arc_points_local(-hw, -hh, r, 90.0, 0.0, 12)
        )
        return _subpaths_to_compound_path([local_pts], cx, cy, angle)

    if variant in {"chamfered", "octagon"}:
        local_pts = [
            (-hw + r, -hh),
            (hw - r, -hh),
            (hw, -hh + r),
            (hw, hh - r),
            (hw - r, hh),
            (-hw + r, hh),
            (-hw, hh - r),
            (-hw, -hh + r),
        ]
    else:
        # "notched"
        local_pts = [
            (-hw + r, -hh),
            (hw - r, -hh),
            (hw - r, -hh + r),
            (hw, -hh + r),
            (hw, hh - r),
            (hw - r, hh - r),
            (hw - r, hh),
            (-hw + r, hh),
            (-hw + r, hh - r),
            (-hw, hh - r),
            (-hw, -hh + r),
            (-hw + r, -hh + r),
        ]

    world_pts: list[Coordinate] = []
    for lx, ly in local_pts:
        rx, ry = rotate_point((lx, ly), angle=angle)
        world_pts.append((cx + rx, cy + ry))
    path_points = ShapeUtil.round_polygon_points(world_pts, shape_r)
    return ShapeUtil.build_matplotlib_path(path_points)
