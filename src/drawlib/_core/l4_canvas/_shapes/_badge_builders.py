# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Path and patch builder helpers for callout, badge, and status indicator shapes."""

from __future__ import annotations

import math
from typing import Any

from matplotlib.patches import PathPatch
from matplotlib.path import Path

from drawlib._core.l2_types import Coordinate
from drawlib._core.l3_colors import ColorUtils
from drawlib._core.l3_math import rotate_point
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas._shapes._shape_utils import ShapeUtils

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


def build_forbidden_path(
    xy: Coordinate,
    radius: float,
    variant: str,
    thickness_ratio: float | None,
    angle: float,
) -> Path:
    """Build compound Matplotlib Path for forbidden shape variants."""
    cx, cy = xy
    t_ratio = 0.22 if thickness_ratio is None else float(thickness_ratio)
    t = radius * t_ratio
    r_in = max(radius * 0.1, radius - t)
    outer = ShapeUtils.arc_points_local(0.0, 0.0, radius, 0.0, 360.0, 72)[:-1]

    if variant in {"slash", "standard", "backslash"}:
        base_deg = 45.0 if variant == "backslash" else 135.0
        ht = t * 0.5
        alpha_deg = math.degrees(math.asin(min(0.95, ht / r_in)))
        hole1 = ShapeUtils.arc_points_local(0.0, 0.0, r_in, base_deg - alpha_deg, base_deg - 180.0 + alpha_deg, 36)
        hole2 = ShapeUtils.arc_points_local(0.0, 0.0, r_in, base_deg + 180.0 - alpha_deg, base_deg + alpha_deg, 36)
        return ShapeUtils.subpaths_to_compound_path([outer, hole1, hole2], cx, cy, angle)

    if variant == "cross":
        ht = t * 0.48
        alpha_deg = math.degrees(math.asin(min(0.95, ht / r_in)))
        holes: list[list[Coordinate]] = []
        for q_angle in (90.0, 0.0, -90.0, 180.0):
            rad_q = math.radians(q_angle)
            apex_dist = ht * math.sqrt(2.0)
            ax = apex_dist * math.cos(rad_q)
            ay = apex_dist * math.sin(rad_q)
            a_ccw = q_angle + 45.0 - alpha_deg
            a_cw = q_angle - 45.0 + alpha_deg
            arc_cw = ShapeUtils.arc_points_local(0.0, 0.0, r_in, a_ccw, a_cw, 24)
            holes.append([(ax, ay), *arc_cw])
        return ShapeUtils.subpaths_to_compound_path([outer, *holes], cx, cy, angle)

    # "no_entry" or "minus"
    bw = radius * 1.32
    bh = radius * 0.38
    r_c = radius * 0.08
    hx = bw / 2.0 - r_c
    hy = bh / 2.0 - r_c
    bar_cw = (
        ShapeUtils.arc_points_local(-hx, hy, r_c, 180.0, 90.0, 8)
        + ShapeUtils.arc_points_local(hx, hy, r_c, 90.0, 0.0, 8)
        + ShapeUtils.arc_points_local(hx, -hy, r_c, 0.0, -90.0, 8)
        + ShapeUtils.arc_points_local(-hx, -hy, r_c, -90.0, -180.0, 8)
    )
    return ShapeUtils.subpaths_to_compound_path([outer, bar_cw], cx, cy, angle)


def _local_check_pts(width: float, height: float, t_ratio: float) -> list[Coordinate]:
    """Build local centered L-checkmark vertices scaled to (width, height)."""
    s = min(width, height)
    t = s * t_ratio
    arm_l = s * 0.54
    arm_r = s * 0.96
    l_pts = [(0.0, 0.0), (arm_r, 0.0), (arm_r, t), (t, t), (t, arm_l), (0.0, arm_l)]
    angle_rad = math.radians(42.0)
    cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad)
    rot_pts = [(px * cos_a - py * sin_a, px * sin_a + py * cos_a) for px, py in l_pts]
    xs = [p[0] for p in rot_pts]
    ys = [p[1] for p in rot_pts]
    mx = 0.5 * (min(xs) + max(xs))
    my = 0.5 * (min(ys) + max(ys))
    span_x = max(max(xs) - min(xs), 1e-6)
    span_y = max(max(ys) - min(ys), 1e-6)
    return [((px - mx) / span_x * width, (py - my) / span_y * height) for px, py in rot_pts]


def build_checkmark_path(
    xy: Coordinate,
    width: float,
    height: float,
    variant: str,
    thickness_ratio: float | None,
    shape_r: float | tuple[float, ...] | None,
    angle: float,
) -> Path:
    """Build Matplotlib Path for checkmark shape variants."""
    cx, cy = xy
    t_ratio = 0.24 if thickness_ratio is None else float(thickness_ratio)

    if variant in {"standard", "check"}:
        local_pts = _local_check_pts(width, height, t_ratio)
        world_pts = [
            (
                rotate_point(pt, angle=angle)[0] + cx,
                rotate_point(pt, angle=angle)[1] + cy,
            )
            for pt in local_pts
        ]
        path_points = ShapeUtils.round_polygon_points(world_pts, shape_r)
        return ShapeUtils.build_matplotlib_path(path_points)

    radius = min(width, height) / 2.0
    outer = ShapeUtils.arc_points_local(0.0, 0.0, radius, 0.0, 360.0, 64)[:-1]
    if variant == "solid_circle":
        chk_s = radius * 1.15
        chk_cw = list(reversed(_local_check_pts(chk_s, chk_s * 0.85, t_ratio)))
        return ShapeUtils.subpaths_to_compound_path([outer, chk_cw], cx, cy, angle)

    # "circle"
    r_in = radius * max(0.2, 1.0 - t_ratio * 0.9)
    inner_cw = ShapeUtils.arc_points_local(0.0, 0.0, r_in, 360.0, 0.0, 64)[:-1]
    chk_s = radius * 0.96
    chk_ccw = _local_check_pts(chk_s, chk_s * 0.85, t_ratio)
    return ShapeUtils.subpaths_to_compound_path([outer, inner_cw, chk_ccw], cx, cy, angle)


def build_shield_path(
    xy: Coordinate,
    width: float,
    height: float,
    variant: str,
    angle: float,
) -> Path:
    """Build cubic-Bezier Matplotlib Path for shield shape variants."""
    cx, cy = xy
    hw = width / 2.0
    hh = height / 2.0
    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    def xform(pts: list[Coordinate]) -> list[Coordinate]:
        return [(cx + lx * cos_a - ly * sin_a, cy + lx * sin_a + ly * cos_a) for lx, ly in pts]

    if variant in {"classic", "standard", "crown"}:
        local_verts = [
            (0.0, hh),
            (hw * 0.45, hh * 0.86),
            (hw * 0.75, hh * 0.86),
            (hw, hh * 0.92),
            (hw, hh * 0.15),
            (hw, -hh * 0.42),
            (hw * 0.45, -hh * 0.78),
            (0.0, -hh),
            (-hw * 0.45, -hh * 0.78),
            (-hw, -hh * 0.42),
            (-hw, hh * 0.15),
            (-hw, hh * 0.92),
            (-hw * 0.75, hh * 0.86),
            (-hw * 0.45, hh * 0.86),
            (0.0, hh),
            (0.0, hh),
        ]
        codes = [
            Path.MOVETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.LINETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.LINETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CLOSEPOLY,
        ]
        return Path(vertices=xform(local_verts), codes=codes)

    if variant in {"round", "arch"}:
        local_verts = [
            (-hw, hh * 0.55),
            (-hw * 0.55, hh),
            (hw * 0.55, hh),
            (hw, hh * 0.55),
            (hw, hh * 0.08),
            (hw, -hh * 0.45),
            (hw * 0.45, -hh * 0.80),
            (0.0, -hh),
            (-hw * 0.45, -hh * 0.80),
            (-hw, -hh * 0.45),
            (-hw, hh * 0.08),
            (-hw, hh * 0.55),
            (-hw, hh * 0.55),
        ]
        codes = [
            Path.MOVETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.LINETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.LINETO,
            Path.CLOSEPOLY,
        ]
        return Path(vertices=xform(local_verts), codes=codes)

    # "flat" or "heater"
    local_verts = [
        (-hw, hh),
        (hw, hh),
        (hw, hh * 0.10),
        (hw, -hh * 0.45),
        (hw * 0.45, -hh * 0.80),
        (0.0, -hh),
        (-hw * 0.45, -hh * 0.80),
        (-hw, -hh * 0.45),
        (-hw, hh * 0.10),
        (-hw, hh),
    ]
    codes = [
        Path.MOVETO,
        Path.LINETO,
        Path.LINETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CLOSEPOLY,
    ]
    return Path(vertices=xform(local_verts), codes=codes)


def build_ribbon_patches(
    xy: Coordinate,
    width: float,
    height: float,
    variant: str,
    tail_width_ratio: float | None,
    drop_ratio: float | None,
    angle: float,
    style: Style,
) -> tuple[list[PathPatch], Coordinate]:
    """Build PathPatch list and front text coordinate for ribbon shape variants."""
    cx, cy = xy
    hw, hh = width / 2.0, height / 2.0
    rad = math.radians(angle)
    cos_a, sin_a = math.cos(rad), math.sin(rad)

    def xform_pt(lx: float, ly: float) -> Coordinate:
        return (cx + lx * cos_a - ly * sin_a, cy + lx * sin_a + ly * cos_a)

    if variant in {"flat", "banner"}:
        notch = min(height * 0.38, width * 0.14)
        pts = [
            (-hw, -hh),
            (hw, -hh),
            (hw - notch, 0.0),
            (hw, hh),
            (-hw, hh),
            (-hw + notch, 0.0),
        ]
        path = ShapeUtils.subpaths_to_compound_path([pts], cx, cy, angle)
        options = ShapeUtils.get_shape_options(style)
        return [PathPatch(path=path, **options)], xy

    t_ratio = 0.17 if tail_width_ratio is None else float(tail_width_ratio)
    d_ratio = 0.24 if drop_ratio is None else float(drop_ratio)
    tail_w = width * min(0.42, t_ratio)
    drop_h = height * min(0.48, d_ratio)
    main_h = height - drop_h
    x_in = hw - tail_w
    fold_w = tail_w * 0.42
    notch_x = hw - tail_w * 0.38

    if variant == "up":
        y_main_bot = -hh
        y_top = y_main_bot + main_h
        y_tail_bot = y_top - main_h * 0.72
        y_tail_top = hh
        left_fold = [(-x_in, y_top), (-x_in + fold_w, y_tail_top), (-x_in + fold_w, y_top)]
        right_fold = [(x_in, y_top), (x_in - fold_w, y_tail_top), (x_in - fold_w, y_top)]
    else:
        y_top = hh
        y_main_bot = y_top - main_h
        y_tail_top = y_main_bot + main_h * 0.72
        y_tail_bot = -hh
        left_fold = [(-x_in, y_main_bot), (-x_in + fold_w, y_tail_bot), (-x_in + fold_w, y_main_bot)]
        right_fold = [(x_in, y_main_bot), (x_in - fold_w, y_tail_bot), (x_in - fold_w, y_main_bot)]

    front_cy = 0.5 * (y_main_bot + y_top)
    front = [(-x_in, y_main_bot), (x_in, y_main_bot), (x_in, y_top), (-x_in, y_top)]
    left_tail = [
        (-hw, y_tail_top),
        (-x_in + fold_w, y_tail_top),
        (-x_in + fold_w, y_tail_bot),
        (-hw, y_tail_bot),
        (-notch_x, 0.5 * (y_tail_top + y_tail_bot)),
    ]
    right_tail = [
        (hw, y_tail_top),
        (x_in - fold_w, y_tail_top),
        (x_in - fold_w, y_tail_bot),
        (hw, y_tail_bot),
        (notch_x, 0.5 * (y_tail_top + y_tail_bot)),
    ]

    raw_fill = (
        ColorUtils.get_mplot_rgba(style.shape_fill_color, alpha=style.alpha)
        if style.shape_fill_color is not None
        else (0.0, 0.0, 0.0, 0.0)
    )
    has_fill = style.shape_fill_color is not None and raw_fill[3] > 0.0
    tail_fill: Any = ShapeUtils.darken_rgba(raw_fill, 0.16) if has_fill else "none"
    fold_fill: Any = ShapeUtils.darken_rgba(raw_fill, 0.40) if has_fill else "none"
    front_fill: Any = raw_fill if has_fill else "none"

    lw = style.shape_line_width if style.shape_line_width is not None else 0.0
    has_stroke = style.shape_line_color is not None and lw > 0.0
    stroke_col: Any = ColorUtils.get_mplot_rgba(style.shape_line_color, alpha=style.alpha) if has_stroke else "none"
    ls = style.shape_line_style if style.shape_line_style is not None else "solid"

    patches: list[PathPatch] = []
    for t_pts in (left_tail, right_tail):
        patches.append(
            PathPatch(
                ShapeUtils.subpaths_to_compound_path([t_pts], cx, cy, angle),
                facecolor=tail_fill,
                edgecolor=stroke_col,
                linewidth=lw,
                linestyle=ls,
                joinstyle="round",
                zorder=1,
            )
        )
    for f_pts in (left_fold, right_fold):
        patches.append(
            PathPatch(
                ShapeUtils.subpaths_to_compound_path([f_pts], cx, cy, angle),
                facecolor=fold_fill,
                edgecolor=stroke_col,
                linewidth=lw,
                linestyle=ls,
                joinstyle="round",
                zorder=1,
            )
        )
    patches.append(
        PathPatch(
            ShapeUtils.subpaths_to_compound_path([front], cx, cy, angle),
            facecolor=front_fill,
            edgecolor=stroke_col,
            linewidth=lw,
            linestyle=ls,
            joinstyle="round",
            zorder=1,
        )
    )
    return patches, xform_pt(0.0, front_cy)


def build_pin_path_and_center(
    xy: Coordinate,
    width: float,
    height: float,
    variant: str,
    hole_ratio: float | None,
    angle: float,
) -> tuple[Path, Coordinate]:
    """Build compound Path and rotated head center coordinate for pin shape variants."""
    cx, cy = xy
    hw = width / 2.0
    hh = height / 2.0

    if variant in {"pointer", "standard"}:
        r = min(hw, height * 0.36)
        head_cy = hh - r
        y_tip = -hh
        half_ang = 20.0
        local_outer = [
            (0.0, y_tip),
            *ShapeUtils.arc_points_local(0.0, head_cy, r, -90.0 + half_ang, 270.0 - half_ang, 48),
        ]
        local_head_cy = head_cy
        hole_r = r * float(hole_ratio) if hole_ratio is not None else None
    elif variant in {"teardrop", "drop", "pin"}:
        r = min(hw, height * 0.38)
        head_cy = hh - r
        y_tip = -hh
        dy = max(head_cy - y_tip, r * 1.05)
        alpha_deg = math.degrees(math.asin(min(0.98, r / dy)))
        local_outer = [
            (0.0, y_tip),
            *ShapeUtils.arc_points_local(0.0, head_cy, r, -alpha_deg, 180.0 + alpha_deg, 48),
        ]
        local_head_cy = head_cy
        hole_r = r * float(hole_ratio) if hole_ratio is not None else None
    else:
        # "badge"
        spike_l = height * 0.28
        body_h = height - spike_l
        y_bot_body = -hh + spike_l
        spike_hw = min(hw * 0.28, spike_l * 0.55)
        cr = min(hw * 0.35, body_h * 0.35)
        local_outer = (
            [(0.0, -hh), (spike_hw, y_bot_body)]
            + ShapeUtils.arc_points_local(hw - cr, y_bot_body + cr, cr, -90.0, 0.0, 8)
            + ShapeUtils.arc_points_local(hw - cr, hh - cr, cr, 0.0, 90.0, 8)
            + ShapeUtils.arc_points_local(-hw + cr, hh - cr, cr, 90.0, 180.0, 8)
            + ShapeUtils.arc_points_local(-hw + cr, y_bot_body + cr, cr, 180.0, 270.0, 8)
            + [(-spike_hw, y_bot_body)]
        )
        local_head_cy = 0.5 * (y_bot_body + hh)
        hole_r = min(hw, body_h / 2.0) * float(hole_ratio) if hole_ratio is not None else None

    subpaths = [local_outer]
    if hole_r is not None and hole_r > 0.0:
        subpaths.append(ShapeUtils.arc_points_local(0.0, local_head_cy, hole_r, 360.0, 0.0, 32)[:-1])

    path = ShapeUtils.subpaths_to_compound_path(subpaths, cx, cy, angle)
    rx, ry = rotate_point((0.0, local_head_cy), angle=angle)
    return path, (cx + rx, cy + ry)


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
        return ShapeUtils.subpaths_to_compound_path([local_pts], cx, cy, angle)

    specs = _EXPLOSION_HEAVY_SPECS if variant in {"heavy", "wild"} else _EXPLOSION_STANDARD_SPECS
    world_pts: list[Coordinate] = []
    for a_deg, r_scale in specs:
        lx = hw * r_scale * math.cos(math.radians(a_deg))
        ly = hh * r_scale * math.sin(math.radians(a_deg))
        rx, ry = rotate_point((lx, ly), angle=angle)
        world_pts.append((cx + rx, cy + ry))

    path_points = ShapeUtils.round_polygon_points(world_pts, shape_r)
    return ShapeUtils.build_matplotlib_path(path_points)


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
        local_outer = [(-hw, -hh), *ShapeUtils.arc_points_local(x_arc, 0.0, r_end, -90.0, 90.0, 24), (-hw, hh)]
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
        outer_path = ShapeUtils.build_matplotlib_path(ShapeUtils.round_polygon_points(world_outer, shape_r))
    else:
        outer_path = ShapeUtils.subpaths_to_compound_path([local_outer], cx, cy, angle)

    hole_cw = ShapeUtils.arc_points_local(hole_lx, 0.0, hole_r, 360.0, 0.0, 32)[:-1]
    hole_path = ShapeUtils.subpaths_to_compound_path([hole_cw], cx, cy, angle)
    tx_r, ty_r = rotate_point((text_lx, 0.0), angle=angle)
    return Path.make_compound_path(outer_path, hole_path), (cx + tx_r, cy + ty_r)


__all__ = [
    "_EXPLOSION_HEAVY_SPECS",
    "_EXPLOSION_STANDARD_SPECS",
    "_local_check_pts",
    "build_checkmark_path",
    "build_explosion_path",
    "build_forbidden_path",
    "build_pin_path_and_center",
    "build_ribbon_patches",
    "build_shield_path",
    "build_tag_path_and_center",
]
