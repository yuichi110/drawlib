# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Extended geometry builders for basic canvas shapes."""

from __future__ import annotations

import math
from collections.abc import Callable
from typing import Any

from matplotlib.patches import Circle, PathPatch
from matplotlib.path import Path

from drawlib._core.l2_types import Coordinate
from drawlib._core.l3_colors import ColorUtil
from drawlib._core.l3_math import rotate_point
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas._shapes._util import ShapeUtil

# 7-segment bitmask for digits 0-9: (a=top, b=top-right, c=bot-right, d=bot, e=bot-left, f=top-left, g=mid)
_SEG7_MASKS: dict[int, tuple[int, int, int, int, int, int, int]] = {
    0: (1, 1, 1, 1, 1, 1, 0),
    1: (0, 1, 1, 0, 0, 0, 0),
    2: (1, 1, 0, 1, 1, 0, 1),
    3: (1, 1, 1, 1, 0, 0, 1),
    4: (0, 1, 1, 0, 0, 1, 1),
    5: (1, 0, 1, 1, 0, 1, 1),
    6: (1, 0, 1, 1, 1, 1, 1),
    7: (1, 1, 1, 0, 0, 0, 0),
    8: (1, 1, 1, 1, 1, 1, 1),
    9: (1, 1, 1, 1, 0, 1, 1),
}


def _arc_points_local(
    cx: float,
    cy: float,
    r: float,
    a_start_deg: float,
    a_end_deg: float,
    n: int = 36,
) -> list[Coordinate]:
    """Sample points along a circular arc from a_start_deg to a_end_deg."""
    pts: list[Coordinate] = []
    for i in range(n + 1):
        a = math.radians(a_start_deg + (a_end_deg - a_start_deg) * (i / n))
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def _subpaths_to_compound_path(
    subpaths: list[list[Coordinate]],
    cx: float,
    cy: float,
    angle: float,
) -> Path:
    """Transform local polygon subpaths by (cx, cy, angle) and combine into a single Matplotlib Path."""
    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    all_verts: list[Coordinate] = []
    all_codes: list[Any] = []
    for sp in subpaths:
        if not sp:
            continue
        xformed = [(cx + lx * cos_a - ly * sin_a, cy + lx * sin_a + ly * cos_a) for lx, ly in sp]
        all_verts.extend(xformed)
        all_verts.append(xformed[0])
        all_codes.append(Path.MOVETO)
        all_codes.extend([Path.LINETO] * (len(xformed) - 1))
        all_codes.append(Path.CLOSEPOLY)
    return Path(vertices=all_verts, codes=all_codes)


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
    outer = _arc_points_local(0.0, 0.0, radius, 0.0, 360.0, 72)[:-1]

    if variant in {"slash", "standard", "backslash"}:
        base_deg = 45.0 if variant == "backslash" else 135.0
        ht = t * 0.5
        alpha_deg = math.degrees(math.asin(min(0.95, ht / r_in)))
        hole1 = _arc_points_local(0.0, 0.0, r_in, base_deg - alpha_deg, base_deg - 180.0 + alpha_deg, 36)
        hole2 = _arc_points_local(0.0, 0.0, r_in, base_deg + 180.0 - alpha_deg, base_deg + alpha_deg, 36)
        return _subpaths_to_compound_path([outer, hole1, hole2], cx, cy, angle)

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
            arc_cw = _arc_points_local(0.0, 0.0, r_in, a_ccw, a_cw, 24)
            holes.append([(ax, ay), *arc_cw])
        return _subpaths_to_compound_path([outer, *holes], cx, cy, angle)

    # "no_entry" or "minus"
    bw = radius * 1.32
    bh = radius * 0.38
    r_c = radius * 0.08
    hx = bw / 2.0 - r_c
    hy = bh / 2.0 - r_c
    bar_cw = (
        _arc_points_local(-hx, hy, r_c, 180.0, 90.0, 8)
        + _arc_points_local(hx, hy, r_c, 90.0, 0.0, 8)
        + _arc_points_local(hx, -hy, r_c, 0.0, -90.0, 8)
        + _arc_points_local(-hx, -hy, r_c, -90.0, -180.0, 8)
    )
    return _subpaths_to_compound_path([outer, bar_cw], cx, cy, angle)


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
        path_points = ShapeUtil.round_polygon_points(world_pts, shape_r)
        return ShapeUtil.build_matplotlib_path(path_points)

    radius = min(width, height) / 2.0
    outer = _arc_points_local(0.0, 0.0, radius, 0.0, 360.0, 64)[:-1]
    if variant == "solid_circle":
        chk_s = radius * 1.15
        chk_cw = list(reversed(_local_check_pts(chk_s, chk_s * 0.85, t_ratio)))
        return _subpaths_to_compound_path([outer, chk_cw], cx, cy, angle)

    # "circle"
    r_in = radius * max(0.2, 1.0 - t_ratio * 0.9)
    inner_cw = _arc_points_local(0.0, 0.0, r_in, 360.0, 0.0, 64)[:-1]
    chk_s = radius * 0.96
    chk_ccw = _local_check_pts(chk_s, chk_s * 0.85, t_ratio)
    return _subpaths_to_compound_path([outer, inner_cw, chk_ccw], cx, cy, angle)


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
        path = _subpaths_to_compound_path([pts], cx, cy, angle)
        options = ShapeUtil.get_shape_options(style)
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
        ColorUtil.get_mplot_rgba(style.shape_fill_color, alpha=style.alpha)
        if style.shape_fill_color is not None
        else (0.0, 0.0, 0.0, 0.0)
    )
    has_fill = style.shape_fill_color is not None and raw_fill[3] > 0.0
    tail_fill: Any = (raw_fill[0] * 0.84, raw_fill[1] * 0.84, raw_fill[2] * 0.84, raw_fill[3]) if has_fill else "none"
    fold_fill: Any = (raw_fill[0] * 0.60, raw_fill[1] * 0.60, raw_fill[2] * 0.60, raw_fill[3]) if has_fill else "none"
    front_fill: Any = raw_fill if has_fill else "none"

    lw = style.shape_line_width if style.shape_line_width is not None else 0.0
    has_stroke = style.shape_line_color is not None and lw > 0.0
    stroke_col: Any = (
        ColorUtil.get_mplot_rgba(style.shape_line_color, alpha=style.alpha) if has_stroke else "none"
    )
    ls = style.shape_line_style if style.shape_line_style is not None else "solid"

    patches: list[PathPatch] = []
    for t_pts in (left_tail, right_tail):
        patches.append(
            PathPatch(
                _subpaths_to_compound_path([t_pts], cx, cy, angle),
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
                _subpaths_to_compound_path([f_pts], cx, cy, angle),
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
            _subpaths_to_compound_path([front], cx, cy, angle),
            facecolor=front_fill,
            edgecolor=stroke_col,
            linewidth=lw,
            linestyle=ls,
            joinstyle="round",
            zorder=1,
        )
    )
    return patches, xform_pt(0.0, front_cy)


def build_funnel_patches(
    xy: Coordinate,
    width: float,
    height: float,
    variant: str,
    neck_width_ratio: float | None,
    neck_height_ratio: float | None,
    angle: float,
    style: Style,
) -> tuple[list[PathPatch], Coordinate]:
    """Build PathPatch list and text coordinate for funnel shape variants."""
    cx, cy = xy
    hw, hh = width / 2.0, height / 2.0
    nw_ratio = 0.26 if neck_width_ratio is None else float(neck_width_ratio)
    nh_ratio = 0.38 if neck_height_ratio is None else float(neck_height_ratio)
    nw = (width * nw_ratio) / 2.0
    y_neck = -hh + height * nh_ratio
    rad = math.radians(angle)
    cos_a, sin_a = math.cos(rad), math.sin(rad)

    def xform(pts: list[Coordinate]) -> list[Coordinate]:
        return [(cx + lx * cos_a - ly * sin_a, cy + lx * sin_a + ly * cos_a) for lx, ly in pts]

    text_xy = xform([(0.0, hh * 0.26)])[0]
    options = ShapeUtil.get_shape_options(style)

    if variant == "curved":
        local_v = [
            (-hw, hh),
            (hw, hh),
            (hw, 0.5 * (hh + y_neck)),
            (nw, 0.5 * (hh + y_neck)),
            (nw, y_neck),
            (nw, -hh),
            (-nw, -hh),
            (-nw, y_neck),
            (-nw, 0.5 * (hh + y_neck)),
            (-hw, 0.5 * (hh + y_neck)),
            (-hw, hh),
            (-hw, hh),
        ]
        codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CLOSEPOLY,
        ]
        return [PathPatch(Path(vertices=xform(local_v), codes=codes), **options)], text_xy

    if variant in {"3d", "cylinder"}:
        rim_ry = height * 0.14
        y_top = hh - rim_ry
        body_local = [(-hw, y_top), (hw, y_top), (nw, y_neck), (nw, -hh), (-nw, -hh), (-nw, y_neck)]
        body_patch = PathPatch(_subpaths_to_compound_path([body_local], cx, cy, angle), **options)

        raw = (
            ColorUtil.get_mplot_rgba(style.shape_fill_color, alpha=style.alpha)
            if style.shape_fill_color is not None
            else (0.0, 0.0, 0.0, 0.0)
        )
        has_fill = style.shape_fill_color is not None and raw[3] > 0.0
        top_fill: Any = (
            (
                min(1.0, raw[0] + (1.0 - raw[0]) * 0.35),
                min(1.0, raw[1] + (1.0 - raw[1]) * 0.35),
                min(1.0, raw[2] + (1.0 - raw[2]) * 0.35),
                raw[3],
            )
            if has_fill
            else "none"
        )
        ell_local = [
            (hw * math.cos(math.radians(a)), y_top + rim_ry * math.sin(math.radians(a)))
            for a in range(0, 360, 8)
        ]
        cap_opts = dict(options)
        cap_opts["facecolor"] = top_fill
        cap_patch = PathPatch(_subpaths_to_compound_path([ell_local], cx, cy, angle), **cap_opts)
        return [body_patch, cap_patch], text_xy

    # "standard" or "flat"
    pts_local = [(-hw, hh), (hw, hh), (nw, y_neck), (nw, -hh), (-nw, -hh), (-nw, y_neck)]
    pts_world = xform(pts_local)
    path_points = ShapeUtil.round_polygon_points(pts_world, style.shape_r)
    path = ShapeUtil.build_matplotlib_path(path_points)
    return [PathPatch(path=path, **options)], text_xy


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
        local_outer = [(0.0, y_tip), *_arc_points_local(0.0, head_cy, r, -90.0 + half_ang, 270.0 - half_ang, 48)]
        local_head_cy = head_cy
        hole_r = r * float(hole_ratio) if hole_ratio is not None else None
    elif variant in {"teardrop", "drop", "pin"}:
        r = min(hw, height * 0.38)
        head_cy = hh - r
        y_tip = -hh
        dy = max(head_cy - y_tip, r * 1.05)
        alpha_deg = math.degrees(math.asin(min(0.98, r / dy)))
        local_outer = [(0.0, y_tip), *_arc_points_local(0.0, head_cy, r, -alpha_deg, 180.0 + alpha_deg, 48)]
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
            + _arc_points_local(hw - cr, y_bot_body + cr, cr, -90.0, 0.0, 8)
            + _arc_points_local(hw - cr, hh - cr, cr, 0.0, 90.0, 8)
            + _arc_points_local(-hw + cr, hh - cr, cr, 90.0, 180.0, 8)
            + _arc_points_local(-hw + cr, y_bot_body + cr, cr, 180.0, 270.0, 8)
            + [(-spike_hw, y_bot_body)]
        )
        local_head_cy = 0.5 * (y_bot_body + hh)
        hole_r = min(hw, body_h / 2.0) * float(hole_ratio) if hole_ratio is not None else None

    subpaths = [local_outer]
    if hole_r is not None and hole_r > 0.0:
        subpaths.append(_arc_points_local(0.0, local_head_cy, hole_r, 360.0, 0.0, 32)[:-1])

    path = _subpaths_to_compound_path(subpaths, cx, cy, angle)
    rx, ry = rotate_point((0.0, local_head_cy), angle=angle)
    return path, (cx + rx, cy + ry)


def build_heart_path(
    xy: Coordinate,
    width: float,
    height: float,
    variant: str,
    angle: float,
) -> Path:
    """Build cubic-Bezier Matplotlib Path for heart shape variants."""
    cx, cy = xy
    hw, hh = width / 2.0, height / 2.0
    rad = math.radians(angle)
    cos_a, sin_a = math.cos(rad), math.sin(rad)

    def xform(pts: list[Coordinate]) -> list[Coordinate]:
        return [(cx + lx * cos_a - ly * sin_a, cy + lx * sin_a + ly * cos_a) for lx, ly in pts]

    cleft_y = hh * 0.52
    local_verts = [
        (0.0, -hh),
        (hw * 0.15, -hh * 0.72),
        (hw, -hh * 0.18),
        (hw, hh * 0.32),
        (hw, hh * 0.78),
        (hw * 0.62, hh),
        (hw * 0.34, hh),
        (hw * 0.12, hh),
        (0.0, hh * 0.76),
        (0.0, cleft_y),
        (0.0, hh * 0.76),
        (-hw * 0.12, hh),
        (-hw * 0.34, hh),
        (-hw * 0.62, hh),
        (-hw, hh * 0.78),
        (-hw, hh * 0.32),
        (-hw, -hh * 0.18),
        (-hw * 0.15, -hh * 0.72),
        (0.0, -hh),
        (0.0, -hh),
    ]
    codes = [
        Path.MOVETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CLOSEPOLY,
    ]
    outer_path = Path(vertices=xform(local_verts), codes=codes)
    if variant != "broken":
        return outer_path

    w_c = hw * 0.13
    c_left = [
        (-w_c * 0.5, hh * 0.65),
        (-hw * 0.18 - w_c, hh * 0.22),
        (hw * 0.14 - w_c, -hh * 0.14),
        (-w_c * 0.4, -hh * 0.75),
    ]
    c_right = [
        (w_c * 0.4, -hh * 0.75),
        (hw * 0.14 + w_c, -hh * 0.14),
        (-hw * 0.18 + w_c, hh * 0.22),
        (w_c * 0.5, hh * 0.65),
    ]
    crack_cw = list(reversed(c_left + c_right))
    crack_path = _subpaths_to_compound_path([crack_cw], cx, cy, angle)
    return Path.make_compound_path(outer_path, crack_path)


def build_sun_path(
    xy: Coordinate,
    radius: float,
    variant: str,
    num_rays: int,
    angle: float,
) -> Path:
    """Build compound Matplotlib Path for sun shape variants."""
    cx, cy = xy
    r_disk = radius * 0.54
    r_ray_base = radius * 0.66
    r_ray_tip = radius
    subpaths: list[list[Coordinate]] = [_arc_points_local(0.0, 0.0, r_disk, 0.0, 360.0, 48)[:-1]]
    if variant == "ring":
        subpaths.append(_arc_points_local(0.0, 0.0, r_disk * 0.58, 360.0, 0.0, 48)[:-1])

    half_ang = min(14.0, 110.0 / max(num_rays, 3))
    for i in range(num_rays):
        a_c = i * (360.0 / num_rays)
        ac = math.radians(a_c)
        if variant == "beams":
            ux, uy = math.cos(ac), math.sin(ac)
            px, py = -uy, ux
            bw = radius * 0.075
            beam = [
                (r_ray_base * ux - bw * px, r_ray_base * uy - bw * py),
                (r_ray_tip * ux - bw * px, r_ray_tip * uy - bw * py),
                (r_ray_tip * ux + bw * px, r_ray_tip * uy + bw * py),
                (r_ray_base * ux + bw * px, r_ray_base * uy + bw * py),
            ]
            subpaths.append(beam)
        else:
            a1 = math.radians(a_c - half_ang)
            a2 = math.radians(a_c + half_ang)
            tri = [
                (r_ray_base * math.cos(a1), r_ray_base * math.sin(a1)),
                (r_ray_tip * math.cos(ac), r_ray_tip * math.sin(ac)),
                (r_ray_base * math.cos(a2), r_ray_base * math.sin(a2)),
            ]
            subpaths.append(tri)
    return _subpaths_to_compound_path(subpaths, cx, cy, angle)


def build_moon_path(
    xy: Coordinate,
    width: float,
    height: float,
    variant: str,
    mirror: bool,
    angle: float,
) -> Path:
    """Build Matplotlib Path for moon shape variants."""
    cx, cy = xy
    if variant == "half":
        raw_all = _arc_points_local(0.0, 0.0, 1.0, 90.0, 270.0, 48)
    else:
        t_ratio = 0.28 if variant in {"thin", "waxing"} else 0.46
        a1, a2 = 62.0, 298.0
        outer_raw = _arc_points_local(0.0, 0.0, 1.0, a1, a2, 48)
        x_tip = math.cos(math.radians(a1))
        y_tip = math.sin(math.radians(a1))
        x_belly_in = -1.0 + t_ratio * (1.0 + x_tip)
        dx_sag = x_tip - x_belly_in
        r_in = (y_tip * y_tip + dx_sag * dx_sag) / (2.0 * dx_sag)
        cx_in = x_belly_in + r_in
        ang_in = math.degrees(math.asin(min(0.999, y_tip / r_in)))
        inner_raw = _arc_points_local(cx_in, 0.0, r_in, 180.0 + ang_in, 180.0 - ang_in, 48)
        raw_all = outer_raw + inner_raw[1:-1]

    xs = [p[0] for p in raw_all]
    ys = [p[1] for p in raw_all]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    mx = 0.5 * (min_x + max_x)
    my = 0.5 * (min_y + max_y)
    span_x = max(max_x - min_x, 1e-6)
    span_y = max(max_y - min_y, 1e-6)

    local_pts: list[Coordinate] = []
    for px, py in raw_all:
        nx = (px - mx) / span_x
        if mirror:
            nx = -nx
        ny = (py - my) / span_y
        local_pts.append((nx * width, ny * height))

    return _subpaths_to_compound_path([local_pts], cx, cy, angle)


def _build_7seg_digit_polygons(
    cx_d: float,
    cy_d: float,
    dw: float,
    dh: float,
    t: float,
) -> list[list[Coordinate]]:
    """Build the 7 hexagonal segment polygons (a..g) for a single digit centered at (cx_d, cy_d)."""
    hw = dw / 2.0
    hh = dh / 2.0
    ht = t / 2.0
    gap = t * 0.14

    def h_seg(y_c: float) -> list[Coordinate]:
        x0 = cx_d - hw + ht + gap
        x1 = cx_d + hw - ht - gap
        return [
            (x0 - ht * 0.7, y_c),
            (x0, y_c + ht),
            (x1, y_c + ht),
            (x1 + ht * 0.7, y_c),
            (x1, y_c - ht),
            (x0, y_c - ht),
        ]

    def v_seg(x_c: float, y_bot: float, y_top: float) -> list[Coordinate]:
        yb = y_bot + ht * 0.7 + gap
        yt = y_top - ht * 0.7 - gap
        return [
            (x_c, yb - ht * 0.7),
            (x_c - ht, yb),
            (x_c - ht, yt),
            (x_c, yt + ht * 0.7),
            (x_c + ht, yt),
            (x_c + ht, yb),
        ]

    return [
        h_seg(cy_d + hh - ht),
        v_seg(cx_d + hw - ht, cy_d, cy_d + hh),
        v_seg(cx_d + hw - ht, cy_d - hh, cy_d),
        h_seg(cy_d - hh + ht),
        v_seg(cx_d - hw + ht, cy_d - hh, cy_d),
        v_seg(cx_d - hw + ht, cy_d, cy_d + hh),
        h_seg(cy_d),
    ]


def _build_digital_clock_patches(
    cx: float,
    cy: float,
    radius: float,
    hour: float,
    minute: float,
    angle: float,
    face_fill: tuple[float, float, float, float] | str,
    stroke_color: tuple[float, float, float, float] | str,
    feature_color: tuple[float, float, float, float],
    line_w: float,
    line_style: str,
) -> list[Circle | PathPatch]:
    """Build rounded casing and active 7-segment polygon patches for digital clock variant."""
    rad = math.radians(angle)
    cos_a, sin_a = math.cos(rad), math.sin(rad)

    def xform_pt(lx: float, ly: float) -> Coordinate:
        return (cx + lx * cos_a - ly * sin_a, cy + lx * sin_a + ly * cos_a)

    w = radius * 2.15
    h = radius * 1.22
    hw, hh = w / 2.0, h / 2.0
    cr = min(w, h) * 0.22
    local_casing = [
        (-hw + cr, -hh),
        (hw - cr, -hh),
        (hw, -hh),
        (hw, -hh + cr),
        (hw, hh - cr),
        (hw, hh),
        (hw - cr, hh),
        (-hw + cr, hh),
        (-hw, hh),
        (-hw, hh - cr),
        (-hw, -hh + cr),
        (-hw, -hh),
        (-hw + cr, -hh),
    ]
    casing_codes = [
        Path.MOVETO,
        Path.LINETO,
        Path.CURVE3,
        Path.CURVE3,
        Path.LINETO,
        Path.CURVE3,
        Path.CURVE3,
        Path.LINETO,
        Path.CURVE3,
        Path.CURVE3,
        Path.LINETO,
        Path.CURVE3,
        Path.CURVE3,
    ]
    patches: list[Circle | PathPatch] = [
        PathPatch(
            Path(vertices=[xform_pt(lx, ly) for lx, ly in local_casing], codes=casing_codes),
            facecolor=face_fill,
            edgecolor=stroke_color,
            linewidth=line_w,
            linestyle=line_style,
            zorder=1,
        )
    ]

    h_int = int(round(hour)) % 24
    m_int = int(round(minute)) % 60
    digits = [h_int // 10, h_int % 10, m_int // 10, m_int % 10]
    dw = w * 0.165
    dh = h * 0.62
    seg_t = dw * 0.21
    dx_offsets = [-w * 0.31, -w * 0.115, w * 0.115, w * 0.31]

    active_subpaths: list[list[Coordinate]] = []
    for d_val, dx in zip(digits, dx_offsets, strict=True):
        mask = _SEG7_MASKS[d_val]
        polys = _build_7seg_digit_polygons(dx, 0.0, dw, dh, seg_t)
        for is_on, poly in zip(mask, polys, strict=True):
            if is_on:
                active_subpaths.append(poly)

    if active_subpaths:
        patches.append(
            PathPatch(
                _subpaths_to_compound_path(active_subpaths, cx, cy, angle),
                facecolor=feature_color,
                edgecolor="none",
                linewidth=0,
                zorder=2,
            )
        )

    dot_r = seg_t * 0.58
    for dy in (dh * 0.20, -dh * 0.20):
        patches.append(
            Circle(
                xy=xform_pt(0.0, dy),
                radius=dot_r,
                facecolor=feature_color,
                edgecolor="none",
                linewidth=0,
                zorder=2,
            )
        )
    return patches


def _build_clock_hardware_patches(
    variant: str,
    radius: float,
    xform_pt: Callable[[float, float], Coordinate],
    face_fill: tuple[float, float, float, float] | str,
    stroke_color: tuple[float, float, float, float] | str,
    feature_color: tuple[float, float, float, float],
    line_w: float,
    feature_w: float,
    line_style: str,
) -> list[PathPatch]:
    """Build outer stopwatch crown/button or alarm clock bells/legs."""
    r = radius
    hw_stroke = stroke_color if stroke_color != "none" else feature_color
    hw_lw = line_w if line_w > 0.0 else feature_w * 0.85

    if variant in {"stopwatch", "timer"}:
        stem_w = r * 0.16
        crown_w = r * 0.34
        crown_h = r * 0.14
        hw_local = [
            (-stem_w, r * 0.97),
            (-stem_w, r * 1.14),
            (-crown_w, r * 1.14),
            (-crown_w, r * 1.14 + crown_h),
            (crown_w, r * 1.14 + crown_h),
            (crown_w, r * 1.14),
            (stem_w, r * 1.14),
            (stem_w, r * 0.97),
            (-stem_w, r * 0.97),
        ]
        hw_codes = [Path.MOVETO] + [Path.LINETO] * 7 + [Path.CLOSEPOLY]
        ang = math.radians(48.0)
        ux, uy = math.cos(ang), math.sin(ang)
        px, py = -uy, ux
        bw, bl = r * 0.13, r * 0.22
        bx0, by0 = r * 0.96 * ux, r * 0.96 * uy
        hw_local.extend(
            [
                (bx0 - bw * px, by0 - bw * py),
                (bx0 - bw * px + bl * ux, by0 - bw * py + bl * uy),
                (bx0 + bw * px + bl * ux, by0 + bw * py + bl * uy),
                (bx0 + bw * px, by0 + bw * py),
                (bx0 - bw * px, by0 - bw * py),
            ]
        )
        hw_codes.extend([Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY])
        return [
            PathPatch(
                Path(vertices=[xform_pt(lx, ly) for lx, ly in hw_local], codes=hw_codes),
                facecolor=face_fill,
                edgecolor=hw_stroke,
                linewidth=hw_lw,
                linestyle=line_style,
                joinstyle="round",
                zorder=1,
            )
        ]

    if variant == "alarm":
        patches: list[PathPatch] = []
        for bell_deg in (50.0, 130.0):
            rad_b = math.radians(bell_deg)
            ux, uy = math.cos(rad_b), math.sin(rad_b)
            bcx, bcy = r * 1.06 * ux, r * 1.06 * uy
            br = r * 0.36
            b_local: list[Coordinate] = []
            b_codes: list[Any] = []
            for i in range(17):
                t = math.radians(-85.0 + 170.0 * (i / 16))
                dx = math.cos(t) * ux - math.sin(t) * uy
                dy = math.cos(t) * uy + math.sin(t) * ux
                b_local.append((bcx + br * dx - r * 0.08 * ux, bcy + br * dy - r * 0.08 * uy))
                b_codes.append(Path.MOVETO if i == 0 else Path.LINETO)
            b_local.append(b_local[0])
            b_codes.append(Path.CLOSEPOLY)
            patches.append(
                PathPatch(
                    Path(vertices=[xform_pt(lx, ly) for lx, ly in b_local], codes=b_codes),
                    facecolor=face_fill,
                    edgecolor=hw_stroke,
                    linewidth=hw_lw,
                    linestyle=line_style,
                    joinstyle="round",
                    zorder=1,
                )
            )
        leg_verts: list[Coordinate] = []
        leg_codes: list[Any] = []
        for leg_deg in (232.0, 308.0):
            rad_l = math.radians(leg_deg)
            ux, uy = math.cos(rad_l), math.sin(rad_l)
            leg_verts.extend(
                [xform_pt(r * 0.92 * ux, r * 0.92 * uy), xform_pt(r * 1.20 * ux, r * 1.20 * uy)]
            )
            leg_codes.extend([Path.MOVETO, Path.LINETO])
        patches.append(
            PathPatch(
                Path(vertices=leg_verts, codes=leg_codes),
                facecolor="none",
                edgecolor=hw_stroke,
                linewidth=feature_w * 1.2,
                capstyle="round",
                zorder=1,
            )
        )
        return patches

    return []


def build_clock_patches(
    xy: Coordinate,
    radius: float,
    variant: str,
    hour: float,
    minute: float,
    angle: float,
    face_fill: tuple[float, float, float, float] | str,
    stroke_color: tuple[float, float, float, float] | str,
    feature_color: tuple[float, float, float, float],
    feature_w: float,
    style: Style,
) -> list[Circle | PathPatch]:
    """Build patches for analog or 7-segment digital clock shape variants."""
    cx, cy = xy
    line_w = style.shape_line_width if style.shape_line_width is not None else 0.0
    line_style = style.shape_line_style if style.shape_line_style is not None else "solid"

    if variant == "digital":
        return _build_digital_clock_patches(
            cx=cx,
            cy=cy,
            radius=radius,
            hour=hour,
            minute=minute,
            angle=angle,
            face_fill=face_fill,
            stroke_color=stroke_color,
            feature_color=feature_color,
            line_w=line_w,
            line_style=line_style,
        )

    rad = math.radians(angle)
    cos_a, sin_a = math.cos(rad), math.sin(rad)

    def xform_pt(lx: float, ly: float) -> Coordinate:
        return (cx + lx * cos_a - ly * sin_a, cy + lx * sin_a + ly * cos_a)

    patches: list[Circle | PathPatch] = []
    patches.extend(
        _build_clock_hardware_patches(
            variant=variant,
            radius=radius,
            xform_pt=xform_pt,
            face_fill=face_fill,
            stroke_color=stroke_color,
            feature_color=feature_color,
            line_w=line_w,
            feature_w=feature_w,
            line_style=line_style,
        )
    )
    patches.append(
        Circle(
            xy=(cx, cy),
            radius=radius,
            facecolor=face_fill,
            edgecolor=stroke_color,
            linewidth=line_w,
            linestyle=line_style,
            zorder=1,
        )
    )

    if variant in {"ticks", "dial", "stopwatch", "timer"}:
        tick_verts: list[Coordinate] = []
        tick_codes: list[Any] = []
        for i in range(12):
            ang = math.radians(90.0 - i * 30.0)
            ux, uy = math.cos(ang), math.sin(ang)
            r_in = radius * (0.74 if i % 3 == 0 else 0.82)
            r_out = radius * 0.90
            tick_verts.extend([xform_pt(r_in * ux, r_in * uy), xform_pt(r_out * ux, r_out * uy)])
            tick_codes.extend([Path.MOVETO, Path.LINETO])
        patches.append(
            PathPatch(
                Path(vertices=tick_verts, codes=tick_codes),
                facecolor="none",
                edgecolor=feature_color,
                linewidth=feature_w * 0.75,
                capstyle="round",
                zorder=2,
            )
        )

    h_deg = 90.0 - ((hour % 12.0) + (minute / 60.0)) * 30.0
    m_deg = 90.0 - (minute % 60.0) * 6.0
    h_rad, m_rad = math.radians(h_deg), math.radians(m_deg)
    h_len, m_len = radius * 0.46, radius * 0.68
    hand_verts = [
        (cx, cy),
        xform_pt(h_len * math.cos(h_rad), h_len * math.sin(h_rad)),
        (cx, cy),
        xform_pt(m_len * math.cos(m_rad), m_len * math.sin(m_rad)),
    ]
    hand_codes = [Path.MOVETO, Path.LINETO, Path.MOVETO, Path.LINETO]
    patches.append(
        PathPatch(
            Path(vertices=hand_verts, codes=hand_codes),
            facecolor="none",
            edgecolor=feature_color,
            linewidth=feature_w * 1.15,
            capstyle="round",
            zorder=2,
        )
    )
    patches.append(
        Circle(
            xy=(cx, cy),
            radius=radius * 0.085,
            facecolor=feature_color,
            edgecolor="none",
            linewidth=0,
            zorder=3,
        )
    )
    return patches
