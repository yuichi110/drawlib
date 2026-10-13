# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Path and patch builder helpers for 3D container, flow, and grouping shapes."""

from __future__ import annotations

import math
from typing import Any

from matplotlib.patches import PathPatch
from matplotlib.path import Path

from drawlib._core.l2_types import Coordinate
from drawlib._core.l3_colors import ColorUtils
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas._shapes._shape_utils import ShapeUtils


def _get_cylinder_fill_colors(
    style: Style,
) -> tuple[tuple[float, float, float, float] | str, tuple[float, float, float, float] | str]:
    """Get body fill and top cap fill colors for cylinder."""
    if style.shape_fill_color is None:
        return "none", "none"
    raw_fill = ColorUtils.get_mplot_rgba(style.shape_fill_color, alpha=style.alpha)
    if raw_fill[3] <= 0.0:
        return "none", "none"
    return raw_fill, ShapeUtils.lighten_rgba(raw_fill, 0.28)


def _build_cylinder_disk_patches(
    cx: float,
    cy: float,
    hw: float,
    hh: float,
    hr: float,
    ky: float,
    kx: float,
    disks: int,
    cos_a: float,
    sin_a: float,
    stroke_color: tuple[float, float, float, float] | str,
    line_w: float,
    line_style: str,
    has_stroke: bool,
) -> list[PathPatch]:
    """Generate divider curve patches for multi-disk cylinders."""
    if disks <= 1 or hh <= 0:
        return []

    d_color = stroke_color if has_stroke else (1.0, 1.0, 1.0, 0.7)
    d_w = line_w if has_stroke else 1.5
    step_h = (2 * hh) / disks
    d_codes = [
        Path.MOVETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
    ]
    patches: list[PathPatch] = []

    for i in range(1, disks):
        dy = -hh + i * step_h
        d_verts = [
            (-hw, dy),
            (-hw, dy - ky),
            (-kx, dy - hr),
            (0, dy - hr),
            (kx, dy - hr),
            (hw, dy - ky),
            (hw, dy),
        ]
        world_verts = [(cx + vx * cos_a - vy * sin_a, cy + vx * sin_a + vy * cos_a) for vx, vy in d_verts]
        patches.append(
            PathPatch(
                Path(vertices=world_verts, codes=d_codes),
                facecolor="none",
                edgecolor=d_color,
                linewidth=d_w,
                linestyle=line_style,
                zorder=1,
            )
        )
    return patches


def build_cylinder_patches(
    xy: Coordinate,
    width: float,
    height: float,
    disks: int,
    angle: float,
    style: Style,
) -> list[PathPatch]:
    """Build 3D cylinder body, cap, outline, and disk divider patches."""
    cx, cy = xy
    eh = min(width * 0.35, height * 0.35)
    hw = width / 2.0
    hh = max(0.0, (height - eh) / 2.0)
    hr = eh / 2.0

    kappa = 0.5522847498307936
    kx = hw * kappa
    ky = hr * kappa

    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    def xform(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
        return [(cx + vx * cos_a - vy * sin_a, cy + vx * sin_a + vy * cos_a) for vx, vy in pts]

    b_verts = [
        (-hw, hh),
        (-hw, -hh),
        (-hw, -hh - ky),
        (-kx, -hh - hr),
        (0, -hh - hr),
        (kx, -hh - hr),
        (hw, -hh - ky),
        (hw, -hh),
        (hw, hh),
        (hw, hh - ky),
        (kx, hh - hr),
        (0, hh - hr),
        (-kx, hh - hr),
        (-hw, hh - ky),
        (-hw, hh),
        (-hw, hh),
    ]
    b_codes = [
        Path.MOVETO,
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
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CLOSEPOLY,
    ]
    body_path = Path(vertices=xform(b_verts), codes=b_codes)

    t_verts = [
        (hw, hh),
        (hw, hh + ky),
        (kx, hh + hr),
        (0, hh + hr),
        (-kx, hh + hr),
        (-hw, hh + ky),
        (-hw, hh),
        (-hw, hh - ky),
        (-kx, hh - hr),
        (0, hh - hr),
        (kx, hh - hr),
        (hw, hh - ky),
        (hw, hh),
        (hw, hh),
    ]
    t_codes = [
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
        Path.CLOSEPOLY,
    ]
    top_path = Path(vertices=xform(t_verts), codes=t_codes)

    line_w = style.shape_line_width if style.shape_line_width is not None else 0.0
    has_stroke = style.shape_line_color is not None and line_w > 0
    line_style = style.shape_line_style if style.shape_line_style is not None else "solid"

    m_fill, top_fill = _get_cylinder_fill_colors(style)
    stroke_color = (
        ColorUtils.get_mplot_rgba(style.shape_line_color)
        if has_stroke and style.shape_line_color is not None
        else "none"
    )

    patches: list[PathPatch] = [
        PathPatch(body_path, facecolor=m_fill, edgecolor="none", linewidth=0, zorder=1),
        PathPatch(
            top_path,
            facecolor=top_fill,
            edgecolor=stroke_color if has_stroke else "none",
            linewidth=line_w,
            linestyle=line_style,
            zorder=1,
        ),
    ]

    if has_stroke:
        out_verts = [
            (-hw, hh),
            (-hw, -hh),
            (-hw, -hh - ky),
            (-kx, -hh - hr),
            (0, -hh - hr),
            (kx, -hh - hr),
            (hw, -hh - ky),
            (hw, -hh),
            (hw, hh),
        ]
        out_codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.LINETO,
        ]
        out_path = Path(vertices=xform(out_verts), codes=out_codes)
        patches.append(
            PathPatch(
                out_path,
                facecolor="none",
                edgecolor=stroke_color,
                linewidth=line_w,
                linestyle=line_style,
                zorder=1,
            )
        )

    patches.extend(
        _build_cylinder_disk_patches(
            cx=cx,
            cy=cy,
            hw=hw,
            hh=hh,
            hr=hr,
            ky=ky,
            kx=kx,
            disks=disks,
            cos_a=cos_a,
            sin_a=sin_a,
            stroke_color=stroke_color,
            line_w=line_w,
            line_style=line_style,
            has_stroke=has_stroke,
        )
    )
    return patches


def _arc_bezier_between(
    p0: tuple[float, float],
    p1: tuple[float, float],
    sagitta_ratio: float,
) -> list[tuple[tuple[float, float], Any]]:
    """Build circular arc cubic Bezier segments from p0 to p1 bulging outward (CCW)."""
    dx = p1[0] - p0[0]
    dy = p1[1] - p0[1]
    chord = math.hypot(dx, dy)
    if chord < 1e-9 or sagitta_ratio <= 1e-4:
        return [(p1, Path.LINETO)]

    nx = dy / chord
    ny = -dx / chord
    h = sagitta_ratio * chord
    r = (chord * chord) / (8.0 * h) + (h / 2.0)
    theta = 4.0 * math.atan((2.0 * h) / chord)

    mx = 0.5 * (p0[0] + p1[0])
    my = 0.5 * (p0[1] + p1[1])
    cx = mx + (h - r) * nx
    cy = my + (h - r) * ny

    angle_peak = math.atan2(ny, nx)
    a0 = angle_peak - 0.5 * theta
    a1 = angle_peak + 0.5 * theta

    num_seg = 1 if theta <= (math.pi * 0.55) else 2
    d_theta = (a1 - a0) / num_seg
    k = (4.0 / 3.0) * math.tan(d_theta / 4.0)

    segments: list[tuple[tuple[float, float], Any]] = []
    for i in range(num_seg):
        t0 = a0 + i * d_theta
        t1 = t0 + d_theta
        x0_s, y0_s = cx + r * math.cos(t0), cy + r * math.sin(t0)
        x1_s, y1_s = cx + r * math.cos(t1), cy + r * math.sin(t1)
        cp1 = (x0_s - k * r * math.sin(t0), y0_s + k * r * math.cos(t0))
        cp2 = (x1_s + k * r * math.sin(t1), y1_s - k * r * math.cos(t1))
        segments.extend([(cp1, Path.CURVE4), (cp2, Path.CURVE4), ((x1_s, y1_s), Path.CURVE4)])
    return segments


def _get_cloud_valleys_and_sagittas(
    variant: str,
    bump_ratio: float | None,
) -> tuple[list[tuple[float, float]], list[float]]:
    """Return valley coordinates and sagitta ratios for the selected cloud variant."""
    if variant in ("flat", "flat_bottom"):
        br = 0.24 if bump_ratio is None else bump_ratio
        scale_b = br / 0.24
        valleys = [
            (-0.34, -0.38),
            (0.36, -0.38),
            (0.32, 0.06),
            (0.02, 0.24),
            (-0.28, 0.12),
        ]
        sagittas = [0.0, 0.40 * scale_b, 0.42 * scale_b, 0.46 * scale_b, 0.40 * scale_b]
        return valleys, sagittas

    if variant in ("fluffy", "dense"):
        br = 0.20 if bump_ratio is None else bump_ratio
        scale_b = br / 0.20
        angles_deg = [-150, -120, -90, -60, -30, 0, 30, 62, 92, 122, 150, 180]
        radii_scale = [0.96, 0.94, 0.95, 0.94, 0.96, 0.98, 0.95, 0.98, 0.96, 0.95, 0.97, 0.96]
        valleys = [
            (0.38 * s * math.cos(math.radians(a)), 0.36 * s * math.sin(math.radians(a)))
            for a, s in zip(angles_deg, radii_scale, strict=True)
        ]
        return valleys, [0.38 * scale_b] * len(valleys)

    if variant in ("simple", "minimal"):
        br = 0.24 if bump_ratio is None else bump_ratio
        scale_b = br / 0.24
        angles_deg = [-145, -90, -35, 35, 90, 145]
        valleys = [(0.35 * math.cos(math.radians(a)), 0.32 * math.sin(math.radians(a))) for a in angles_deg]
        sagittas = [0.36 * scale_b, 0.36 * scale_b, 0.42 * scale_b, 0.38 * scale_b, 0.38 * scale_b, 0.42 * scale_b]
        return valleys, sagittas

    br = 0.22 if bump_ratio is None else bump_ratio
    scale_b = br / 0.22
    angles_deg = [-148, -108, -68, -26, 22, 68, 118, 156]
    radii_scale = [0.95, 0.92, 0.92, 0.95, 0.96, 0.98, 0.96, 0.95]
    valleys = [
        (0.37 * s * math.cos(math.radians(a)), 0.34 * s * math.sin(math.radians(a)))
        for a, s in zip(angles_deg, radii_scale, strict=True)
    ]
    sagittas = [
        0.34 * scale_b,
        0.32 * scale_b,
        0.34 * scale_b,
        0.42 * scale_b,
        0.40 * scale_b,
        0.45 * scale_b,
        0.38 * scale_b,
        0.42 * scale_b,
    ]
    return valleys, sagittas


def build_cloud_path(
    xy: tuple[float, float],
    width: float,
    height: float,
    variant: str,
    bump_ratio: float | None,
    angle: float,
) -> Path:
    """Build normalized and rotated cloud Path for the given variant and bump_ratio."""
    valleys, sagittas = _get_cloud_valleys_and_sagittas(variant, bump_ratio)
    raw_verts: list[tuple[float, float]] = [valleys[0]]
    codes: list[Any] = [Path.MOVETO]

    n = len(valleys)
    for i in range(n):
        segs = _arc_bezier_between(valleys[i], valleys[(i + 1) % n], max(0.0, sagittas[i]))
        for pt, code in segs:
            raw_verts.append(pt)
            codes.append(code)

    min_x = min(p[0] for p in raw_verts)
    max_x = max(p[0] for p in raw_verts)
    min_y = min(p[1] for p in raw_verts)
    max_y = max(p[1] for p in raw_verts)
    span_x = max(max_x - min_x, 1e-6)
    span_y = max(max_y - min_y, 1e-6)
    cx_norm = 0.5 * (min_x + max_x)
    cy_norm = 0.5 * (min_y + max_y)

    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    scaled_verts: list[tuple[float, float]] = []
    for vx, vy in raw_verts:
        lx = ((vx - cx_norm) / span_x) * width
        ly = ((vy - cy_norm) / span_y) * height
        rx = xy[0] + lx * cos_a - ly * sin_a
        ry = xy[1] + lx * sin_a + ly * cos_a
        scaled_verts.append((rx, ry))

    scaled_verts.append((0.0, 0.0))
    codes.append(Path.CLOSEPOLY)
    return Path(scaled_verts, codes)


def format_brace_styles(
    style: Style,
    text_style: Style | None = None,
) -> tuple[Style, Style | None]:
    """Validate and return style (supporting 'line' or 'shape') and optional text_style."""
    if not isinstance(style, Style):
        raise TypeError(f'Arg "style" must be Style, but {type(style)} given.')
    if "line" not in style.supports and "shape" not in style.supports:
        style.validate_for("line")
    if text_style is not None:
        if not isinstance(text_style, Style):
            raise TypeError(f'Arg "text_style" must be Style, but {type(text_style)} given.')
        text_style.validate_for("text")
    return style, text_style


def get_brace_stroke_options(style: Style) -> dict[str, Any]:
    """Extract Matplotlib PathPatch stroke options from Style for brace rendering."""
    lw = style.line_width
    if lw is None:
        lw = style.shape_line_width if (style.shape_line_width or 0.0) > 0.0 else 1.5

    col = style.line_color
    if col is None:
        col = (
            style.shape_line_color
            if (style.shape_line_width or 0.0) > 0.0 and style.shape_line_color is not None
            else style.shape_fill_color
        )
    rgba = ColorUtils.get_mplot_rgba(col) if col is not None else (0.0, 0.0, 0.0, 1.0)
    ls = style.line_style if style.line_style is not None else (style.shape_line_style or "solid")

    options: dict[str, Any] = {
        "facecolor": "none",
        "edgecolor": rgba,
        "linewidth": lw,
        "linestyle": ls,
        "capstyle": "round",
        "joinstyle": "round",
    }
    if style.alpha is not None:
        options["alpha"] = style.alpha
    return options


def _build_square_brace_local(
    hd: float,
    hs: float,
    depth: float,
    span: float,
    shape_r: float | None,
) -> tuple[list[tuple[float, float]], list[Any]]:
    """Build local canonical 'left' vertices and Path codes for square bracket '['."""
    r = 0.0 if shape_r is None else min(float(shape_r), depth * 0.9, span * 0.45)
    if r <= 1e-6:
        verts = [(hd, hs), (-hd, hs), (-hd, -hs), (hd, -hs)]
        codes: list[Any] = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO]
        return verts, codes

    k = 0.5522847498307936
    verts = [
        (hd, hs),
        (-hd + r, hs),
        (-hd + r * (1.0 - k), hs),
        (-hd, hs - r * (1.0 - k)),
        (-hd, hs - r),
        (-hd, -hs + r),
        (-hd, -hs + r * (1.0 - k)),
        (-hd + r * (1.0 - k), -hs),
        (-hd + r, -hs),
        (hd, -hs),
    ]
    codes = [
        Path.MOVETO,
        Path.LINETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.LINETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.LINETO,
    ]
    return verts, codes


def _build_curly_brace_local(
    hd: float,
    hs: float,
    depth: float,
    span: float,
    tip_ratio: float | None,
    tip_position_ratio: float | None,
) -> tuple[list[tuple[float, float]], list[Any]]:
    """Build local canonical 'left' vertices and Path codes for curly brace '{'."""
    tip_r = 0.50 if tip_ratio is None else tip_ratio
    pos_r = 0.50 if tip_position_ratio is None else tip_position_ratio

    tip_depth = tip_r * depth
    hook_depth = (1.0 - tip_r) * depth
    x_spine = -hd + tip_depth

    r_hook = min(max(hook_depth, depth * 0.15), span * 0.14)
    h_tip = min(max(tip_depth * 0.95, depth * 0.20), span * 0.16)

    y_tip = (pos_r - 0.5) * span
    y_tip = max(-hs + r_hook + h_tip, min(hs - r_hook - h_tip, y_tip))

    k = 0.5522847498307936
    verts = [
        (hd, hs),
        (x_spine + hook_depth * (1.0 - k), hs),
        (x_spine, hs - r_hook * (1.0 - k)),
        (x_spine, hs - r_hook),
        (x_spine, y_tip + h_tip),
        (x_spine, y_tip + h_tip * (1.0 - k)),
        (-hd + tip_depth * (1.0 - k), y_tip),
        (-hd, y_tip),
        (-hd + tip_depth * (1.0 - k), y_tip),
        (x_spine, y_tip - h_tip * (1.0 - k)),
        (x_spine, y_tip - h_tip),
        (x_spine, -hs + r_hook),
        (x_spine, -hs + r_hook * (1.0 - k)),
        (x_spine + hook_depth * (1.0 - k), -hs),
        (hd, -hs),
    ]
    codes: list[Any] = [
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
    ]
    return verts, codes


def build_brace_path(
    xy: tuple[float, float],
    width: float,
    height: float,
    symbol: str,
    direction: str | None,
    tip_ratio: float | None,
    tip_position_ratio: float | None,
    shape_r: float | None,
    angle: float,
) -> Path:
    """Build rotated open Path for curly {}, square [], and round () braces."""
    eff_dir = direction if direction is not None else ("right" if symbol in ("}", "]", ")") else "left")
    is_horizontal = eff_dir in ("top", "bottom")
    span = width if is_horizontal else height
    depth = height if is_horizontal else width
    hs = span / 2.0
    hd = depth / 2.0

    if symbol in ("[", "]", "[]", "square"):
        verts, codes = _build_square_brace_local(hd, hs, depth, span, shape_r)
    elif symbol in ("(", ")", "()", "round"):
        k_y = hs * 0.5522847498307936
        verts = [
            (hd, hs),
            (-hd * 0.25, hs),
            (-hd, k_y),
            (-hd, 0.0),
            (-hd, -k_y),
            (-hd * 0.25, -hs),
            (hd, -hs),
        ]
        codes = [
            Path.MOVETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
        ]
    else:
        verts, codes = _build_curly_brace_local(hd, hs, depth, span, tip_ratio, tip_position_ratio)

    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    transformed: list[tuple[float, float]] = []
    for lx, ly in verts:
        if eff_dir == "left":
            tx, ty = lx, ly
        elif eff_dir == "right":
            tx, ty = -lx, ly
        elif eff_dir == "top":
            tx, ty = ly, -lx
        else:
            tx, ty = ly, lx
        rx = xy[0] + tx * cos_a - ty * sin_a
        ry = xy[1] + tx * sin_a + ty * cos_a
        transformed.append((rx, ry))

    return Path(transformed, codes)


def _get_cube_face_fills(
    style: Style,
) -> tuple[
    tuple[float, float, float, float] | str,
    tuple[float, float, float, float] | str,
    tuple[float, float, float, float] | str,
]:
    """Derive front, top, and right-side face fills from a shape Style."""
    if style.shape_fill_color is None:
        return "none", "none", "none"

    raw = ColorUtils.get_mplot_rgba(style.shape_fill_color, alpha=style.alpha)
    if raw[3] <= 0.0:
        return "none", "none", "none"

    lum = 0.299 * raw[0] + 0.587 * raw[1] + 0.114 * raw[2]
    top_lift = 0.55 if lum > 0.85 else 0.28
    side_darken = 0.08 if lum > 0.85 else 0.18
    return raw, ShapeUtils.lighten_rgba(raw, top_lift), ShapeUtils.darken_rgba(raw, side_darken)


def build_cube_patches(
    xy: tuple[float, float],
    width: float,
    height: float,
    depth_ratio: float | None,
    angle: float,
    style: Style,
) -> tuple[list[PathPatch], tuple[float, float]]:
    """Build 3D cube face and outline patches and return (patches, front_face_text_xy)."""
    cx, cy = xy
    dr = 0.25 if depth_ratio is None else depth_ratio
    base_d = min(width, height) * dr
    dx = min(base_d, width * 0.48)
    dy = min(base_d * 0.82, height * 0.48)

    hw = width / 2.0
    hh = height / 2.0
    fx0, fx1 = -hw, hw - dx
    fy0, fy1 = -hh, hh - dy

    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    def xform(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
        return [(cx + vx * cos_a - vy * sin_a, cy + vx * sin_a + vy * cos_a) for vx, vy in pts]

    front_pts = [(fx0, fy0), (fx1, fy0), (fx1, fy1), (fx0, fy1), (fx0, fy0)]
    top_pts = [(fx0, fy1), (fx1, fy1), (hw, hh), (fx0 + dx, hh), (fx0, fy1)]
    side_pts = [(fx1, fy0), (hw, -hh + dy), (hw, hh), (fx1, fy1), (fx1, fy0)]
    codes_quad: list[Any] = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]

    front_fill, top_fill, side_fill = _get_cube_face_fills(style)
    patches: list[PathPatch] = [
        PathPatch(
            Path(vertices=xform(pts), codes=codes_quad),
            facecolor=fill,
            edgecolor="none",
            linewidth=0,
            zorder=1,
        )
        for pts, fill in ((top_pts, top_fill), (side_pts, side_fill), (front_pts, front_fill))
    ]

    line_w = style.shape_line_width if style.shape_line_width is not None else 0.0
    if style.shape_line_color is not None and line_w > 0:
        stroke_color = ColorUtils.get_mplot_rgba(style.shape_line_color, alpha=style.alpha)
        if stroke_color[3] > 0.0:
            line_style = style.shape_line_style if style.shape_line_style is not None else "solid"
            outer_pts = [
                (fx0, fy0),
                (fx1, fy0),
                (hw, -hh + dy),
                (hw, hh),
                (fx0 + dx, hh),
                (fx0, fy1),
                (fx0, fy0),
                (fx0, fy1),
                (fx1, fy1),
                (fx1, fy0),
                (fx1, fy1),
                (hw, hh),
            ]
            outer_codes: list[Any] = [
                Path.MOVETO,
                Path.LINETO,
                Path.LINETO,
                Path.LINETO,
                Path.LINETO,
                Path.LINETO,
                Path.CLOSEPOLY,
                Path.MOVETO,
                Path.LINETO,
                Path.LINETO,
                Path.MOVETO,
                Path.LINETO,
            ]
            patches.append(
                PathPatch(
                    Path(vertices=xform(outer_pts), codes=outer_codes),
                    facecolor="none",
                    edgecolor=stroke_color,
                    linewidth=line_w,
                    linestyle=line_style,
                    joinstyle="round",
                    capstyle="round",
                    zorder=1,
                )
            )

    fcx_local = 0.5 * (fx0 + fx1)
    fcy_local = 0.5 * (fy0 + fy1)
    text_xy = (
        cx + fcx_local * cos_a - fcy_local * sin_a,
        cy + fcx_local * sin_a + fcy_local * cos_a,
    )
    return patches, text_xy


def _build_document_sheet_paths(
    x0: float,
    y0: float,
    w: float,
    h: float,
    variant: str,
    wave_h: float,
    fold_s: float,
    cx: float,
    cy: float,
    cos_a: float,
    sin_a: float,
) -> tuple[Path, Path | None, Path]:
    """Build rotated (body_fill_path, flap_fill_path, stroke_path) for one document sheet."""

    def xform(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
        return [(cx + vx * cos_a - vy * sin_a, cy + vx * sin_a + vy * cos_a) for vx, vy in pts]

    has_bottom_wave = variant in ("wave", "standard", "double_wave", "snippet", "folded_wave", "report")
    has_top_wave = variant in ("double_wave", "snippet")
    has_fold = variant in ("folded", "page", "note", "folded_wave", "report")

    x1 = x0 + w
    xm = x0 + w * 0.5
    y1 = y0 + h

    yt_base = y1 - 0.5 * wave_h if has_top_wave else y1
    verts: list[tuple[float, float]] = [(x0, yt_base)]
    codes: list[Any] = [Path.MOVETO]

    if has_bottom_wave:
        yb_base = y0 + 0.5 * wave_h
        db = (2.0 / 3.0) * wave_h
        verts.extend(
            [
                (x0, yb_base),
                (x0 + w * 0.16, yb_base - db),
                (x0 + w * 0.34, yb_base - db),
                (xm, yb_base),
                (x0 + w * 0.66, yb_base + db),
                (x0 + w * 0.84, yb_base + db),
                (x1, yb_base),
            ]
        )
        codes.extend([Path.LINETO] + [Path.CURVE4] * 6)
    else:
        verts.extend([(x0, y0), (x1, y0)])
        codes.extend([Path.LINETO, Path.LINETO])

    if has_fold:
        verts.extend([(x1, y1 - fold_s), (x1 - fold_s, y1), (x0, y1)])
        codes.extend([Path.LINETO, Path.LINETO, Path.CLOSEPOLY])
    elif has_top_wave:
        dt = (2.0 / 3.0) * wave_h
        verts.extend(
            [
                (x1, yt_base),
                (x0 + w * 0.84, yt_base + dt),
                (x0 + w * 0.66, yt_base + dt),
                (xm, yt_base),
                (x0 + w * 0.34, yt_base - dt),
                (x0 + w * 0.16, yt_base - dt),
                (x0, yt_base),
                (x0, yt_base),
            ]
        )
        codes.extend([Path.LINETO] + [Path.CURVE4] * 6 + [Path.CLOSEPOLY])
    else:
        verts.extend([(x1, y1), (x0, y1)])
        codes.extend([Path.LINETO, Path.CLOSEPOLY])

    body_path = Path(vertices=xform(verts), codes=codes)
    flap_path: Path | None = None
    stroke_verts = list(verts)
    stroke_codes = list(codes)

    if has_fold:
        flap_verts = [
            (x1 - fold_s, y1),
            (x1 - fold_s, y1 - fold_s),
            (x1, y1 - fold_s),
            (x1 - fold_s, y1),
        ]
        flap_codes: list[Any] = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
        flap_path = Path(vertices=xform(flap_verts), codes=flap_codes)
        stroke_verts.extend(
            [
                (x1 - fold_s, y1),
                (x1 - fold_s, y1 - fold_s),
                (x1, y1 - fold_s),
            ]
        )
        stroke_codes.extend([Path.MOVETO, Path.LINETO, Path.LINETO])

    return body_path, flap_path, Path(vertices=xform(stroke_verts), codes=stroke_codes)


def _get_document_sheet_fills(
    raw_fill: tuple[float, float, float, float] | None,
    idx: int,
) -> tuple[tuple[float, float, float, float] | str, tuple[float, float, float, float] | str]:
    """Compute body fill and folded flap fill for a document sheet at stack index idx."""
    if raw_fill is None or raw_fill[3] <= 0.0:
        return "none", "none"

    fill_c = ShapeUtils.lighten_rgba(raw_fill, 0.14 * idx)
    lum = 0.299 * fill_c[0] + 0.587 * fill_c[1] + 0.114 * fill_c[2]
    flap_darken = 0.10 if lum > 0.85 else 0.20
    return fill_c, ShapeUtils.darken_rgba(fill_c, flap_darken)


def _get_document_text_center(
    cx: float,
    cy: float,
    hw: float,
    hh: float,
    sheet_w: float,
    sheet_h: float,
    wave_h: float,
    fold_s: float,
    variant: str,
    cos_a: float,
    sin_a: float,
) -> tuple[float, float]:
    """Calculate optical center on the front document sheet for embedded text."""
    fcx_local = -hw + sheet_w / 2.0
    if variant in ("wave", "standard"):
        fcy_local = -hh + wave_h * 0.50 + (sheet_h - wave_h * 0.50) / 2.0
    elif variant in ("folded_wave", "report"):
        fcy_local = -hh + wave_h * 0.45 + (sheet_h - wave_h * 0.45 - fold_s * 0.25) / 2.0
    elif variant in ("folded", "page", "note"):
        fcy_local = -hh + (sheet_h - fold_s * 0.20) / 2.0
    else:
        fcy_local = -hh + sheet_h / 2.0
    return (
        cx + fcx_local * cos_a - fcy_local * sin_a,
        cy + fcx_local * sin_a + fcy_local * cos_a,
    )


def build_document_patches(
    xy: tuple[float, float],
    width: float,
    height: float,
    variant: str,
    stacked: int,
    wave_ratio: float | None,
    fold_ratio: float | None,
    angle: float,
    style: Style,
) -> tuple[list[PathPatch], tuple[float, float]]:
    """Build document sheet patches (supporting stacked sheets and variants) and return (patches, text_xy)."""
    cx, cy = xy
    wr = 0.14 if wave_ratio is None else wave_ratio
    fr = 0.24 if fold_ratio is None else fold_ratio

    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    n = max(1, stacked)
    step_x = 0.0 if n == 1 else min(width * 0.075, 2.2)
    step_y = 0.0 if n == 1 else min(height * 0.075, 2.2)
    sheet_w = width - step_x * (n - 1)
    sheet_h = height - step_y * (n - 1)
    wave_h = sheet_h * wr
    fold_s = min(sheet_w, sheet_h) * fr

    line_w = style.shape_line_width if style.shape_line_width is not None else 0.0
    stroke_rgba = (
        ColorUtils.get_mplot_rgba(style.shape_line_color, alpha=style.alpha)
        if style.shape_line_color is not None and line_w > 0
        else None
    )
    has_stroke = stroke_rgba is not None and stroke_rgba[3] > 0.0
    line_style = style.shape_line_style if style.shape_line_style is not None else "solid"
    raw_fill = (
        ColorUtils.get_mplot_rgba(style.shape_fill_color, alpha=style.alpha)
        if style.shape_fill_color is not None
        else None
    )

    hw = width / 2.0
    hh = height / 2.0
    patches: list[PathPatch] = []

    for idx in range(n - 1, -1, -1):
        body_p, flap_p, stroke_p = _build_document_sheet_paths(
            -hw + idx * step_x,
            -hh + idx * step_y,
            sheet_w,
            sheet_h,
            variant,
            wave_h,
            fold_s,
            cx,
            cy,
            cos_a,
            sin_a,
        )
        fill_c, flap_c = _get_document_sheet_fills(raw_fill, idx)
        patches.append(
            PathPatch(
                body_p,
                facecolor=fill_c,
                edgecolor="none",
                linewidth=0,
                zorder=1,
            )
        )
        if flap_p is not None and flap_c != "none":
            patches.append(
                PathPatch(
                    flap_p,
                    facecolor=flap_c,
                    edgecolor="none",
                    linewidth=0,
                    zorder=1,
                )
            )

        needs_sep = (n > 1 or flap_p is not None) and fill_c != "none"
        edge_c: tuple[float, float, float, float] | str = (
            stroke_rgba if (has_stroke and stroke_rgba is not None) else ("#ffffff" if needs_sep else "none")
        )
        edge_w = line_w if has_stroke else (1.0 if needs_sep else 0.0)
        if edge_c != "none" and edge_w > 0:
            patches.append(
                PathPatch(
                    stroke_p,
                    facecolor="none",
                    edgecolor=edge_c,
                    linewidth=edge_w,
                    linestyle=line_style,
                    joinstyle="round",
                    capstyle="round",
                    zorder=1,
                )
            )

    text_xy = _get_document_text_center(cx, cy, hw, hh, sheet_w, sheet_h, wave_h, fold_s, variant, cos_a, sin_a)
    return patches, text_xy


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
    options = ShapeUtils.get_shape_options(style)

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
        body_patch = PathPatch(ShapeUtils.subpaths_to_compound_path([body_local], cx, cy, angle), **options)

        raw = (
            ColorUtils.get_mplot_rgba(style.shape_fill_color, alpha=style.alpha)
            if style.shape_fill_color is not None
            else (0.0, 0.0, 0.0, 0.0)
        )
        has_fill = style.shape_fill_color is not None and raw[3] > 0.0
        top_fill: Any = ShapeUtils.lighten_rgba(raw, 0.35) if has_fill else "none"
        ell_local = [
            (hw * math.cos(math.radians(a)), y_top + rim_ry * math.sin(math.radians(a))) for a in range(0, 360, 8)
        ]
        cap_opts = dict(options)
        cap_opts["facecolor"] = top_fill
        cap_patch = PathPatch(ShapeUtils.subpaths_to_compound_path([ell_local], cx, cy, angle), **cap_opts)
        return [body_patch, cap_patch], text_xy

    # "standard" or "flat"
    pts_local = [(-hw, hh), (hw, hh), (nw, y_neck), (nw, -hh), (-nw, -hh), (-nw, y_neck)]
    pts_world = xform(pts_local)
    path_points = ShapeUtils.round_polygon_points(pts_world, style.shape_r)
    path = ShapeUtils.build_matplotlib_path(path_points)
    return [PathPatch(path=path, **options)], text_xy


__all__ = [
    "_arc_bezier_between",
    "build_brace_path",
    "build_cloud_path",
    "build_cube_patches",
    "_build_curly_brace_local",
    "_build_cylinder_disk_patches",
    "build_cylinder_patches",
    "build_document_patches",
    "_build_document_sheet_paths",
    "_build_square_brace_local",
    "format_brace_styles",
    "get_brace_stroke_options",
    "_get_cloud_valleys_and_sagittas",
    "_get_cube_face_fills",
    "_get_cylinder_fill_colors",
    "_get_document_sheet_fills",
    "_get_document_text_center",
    "build_funnel_patches",
]
