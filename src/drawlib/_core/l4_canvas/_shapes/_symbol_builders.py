# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Path and patch builder helpers for symbol, metaphor, and operator shapes."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable

from matplotlib.patches import Circle, PathPatch
from matplotlib.path import Path

from drawlib._core.l2_types import Coordinate, PathPoints
from drawlib._core.l3_math import rotate_point
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas._shapes._shape_utils import ShapeUtils

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


def _build_face_head_patch(
    cx: float,
    cy: float,
    radius: float,
    variant: str,
    cos_a: float,
    sin_a: float,
    face_fill: tuple[float, float, float, float] | str,
    stroke_color: tuple[float, float, float, float] | str,
    line_w: float,
    line_style: str,
) -> Circle | PathPatch:
    """Build the outer head silhouette patch for a face shape."""

    def xform_pt(lx: float, ly: float) -> tuple[float, float]:
        return (cx + lx * cos_a - ly * sin_a, cy + lx * sin_a + ly * cos_a)

    if variant == "skull":
        r = radius
        jw = r * 0.52
        jy_bot = -r * 0.92
        jy_cheek = -r * 0.28
        cr = r * 0.92
        cy_dome = r * 0.12
        local_verts = [
            (-jw, jy_cheek),
            (-jw, jy_bot + r * 0.16),
            (-jw, jy_bot),
            (-jw + r * 0.16, jy_bot),
            (jw - r * 0.16, jy_bot),
            (jw, jy_bot),
            (jw, jy_bot + r * 0.16),
            (jw, jy_cheek),
            (cr * 1.02, jy_cheek + r * 0.08),
            (cr * 1.05, cy_dome + r * 0.25),
            (cr * 0.78, r * 0.78),
            (cr * 0.42, r * 1.02),
            (-cr * 0.42, r * 1.02),
            (-cr * 0.78, r * 0.78),
            (-cr * 1.05, cy_dome + r * 0.25),
            (-cr * 1.02, jy_cheek + r * 0.08),
            (-jw, jy_cheek),
            (-jw, jy_cheek),
        ]
        codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.CURVE3,
            Path.CURVE3,
            Path.LINETO,
            Path.CURVE3,
            Path.CURVE3,
            Path.LINETO,
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
        verts = [xform_pt(lx, ly) for lx, ly in local_verts]
        return PathPatch(
            Path(vertices=verts, codes=codes),
            facecolor=face_fill,
            edgecolor=stroke_color,
            linewidth=line_w,
            linestyle=line_style,
            joinstyle="round",
            zorder=1,
        )

    if variant == "devil":
        r = radius
        local_pts: list[tuple[float, float]] = []
        codes_d: list[Any] = []

        def add_arc(deg_start: float, deg_end: float, steps: int) -> None:
            for i in range(steps + 1):
                rad_ang = math.radians(deg_start + (deg_end - deg_start) * (i / steps))
                pt = (r * math.cos(rad_ang), r * math.sin(rad_ang))
                if not local_pts:
                    local_pts.append(pt)
                    codes_d.append(Path.MOVETO)
                else:
                    local_pts.append(pt)
                    codes_d.append(Path.LINETO)

        add_arc(142.0, 398.0, 48)
        r_tip = (r * 0.62, r * 1.25)
        r_base_in = (r * math.cos(math.radians(66.0)), r * math.sin(math.radians(66.0)))
        local_pts.extend(
            [
                (r * 1.05, r * 0.85),
                (r * 0.94, r * 1.16),
                r_tip,
                (r * 0.62, r * 1.04),
                (r * 0.50, r * 0.96),
                r_base_in,
            ]
        )
        codes_d.extend([Path.CURVE4] * 6)
        add_arc(66.0, 114.0, 14)
        l_tip = (-r * 0.62, r * 1.25)
        l_base_out = (r * math.cos(math.radians(142.0)), r * math.sin(math.radians(142.0)))
        local_pts.extend(
            [
                (-r * 0.50, r * 0.96),
                (-r * 0.62, r * 1.04),
                l_tip,
                (-r * 0.94, r * 1.16),
                (-r * 1.05, r * 0.85),
                l_base_out,
            ]
        )
        codes_d.extend([Path.CURVE4] * 6)
        local_pts.append(local_pts[0])
        codes_d.append(Path.CLOSEPOLY)
        verts_d = [xform_pt(lx, ly) for lx, ly in local_pts]
        return PathPatch(
            Path(vertices=verts_d, codes=codes_d),
            facecolor=face_fill,
            edgecolor=stroke_color,
            linewidth=line_w,
            linestyle=line_style,
            joinstyle="round",
            zorder=1,
        )

    return Circle(
        xy=(cx, cy),
        radius=radius,
        facecolor=face_fill,
        edgecolor=stroke_color,
        linewidth=line_w,
        linestyle=line_style,
        zorder=1,
    )


def _build_skull_feature_patches(
    xform_pt: Callable[[float, float], tuple[float, float]],
    radius: float,
    feature_color: tuple[float, float, float, float],
    feature_w: float,
) -> list[Circle | PathPatch]:
    """Build eye sockets, nasal cavity, and teeth lines for the skull face variant."""
    r = radius
    eye_x = r * 0.34
    eye_y = r * 0.16
    eye_r = r * 0.20
    patches: list[Circle | PathPatch] = [
        Circle(
            xy=xform_pt(-eye_x, eye_y),
            radius=eye_r,
            facecolor=feature_color,
            edgecolor="none",
            linewidth=0,
            zorder=2,
        ),
        Circle(
            xy=xform_pt(eye_x, eye_y),
            radius=eye_r,
            facecolor=feature_color,
            edgecolor="none",
            linewidth=0,
            zorder=2,
        ),
    ]

    nw = r * 0.11
    ny_top = -r * 0.04
    ny_bot = -r * 0.24
    nose_verts = [
        xform_pt(0.0, ny_top),
        xform_pt(-nw, ny_bot),
        xform_pt(nw, ny_bot),
        xform_pt(0.0, ny_top),
    ]
    nose_codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
    patches.append(
        PathPatch(
            Path(vertices=nose_verts, codes=nose_codes),
            facecolor=feature_color,
            edgecolor="none",
            linewidth=0,
            zorder=2,
        )
    )

    t_top = -r * 0.52
    t_bot = -r * 0.92
    t_verts: list[tuple[float, float]] = []
    t_codes: list[Any] = []
    for tx in (-r * 0.24, 0.0, r * 0.24):
        t_verts.extend([xform_pt(tx, t_top), xform_pt(tx, t_bot)])
        t_codes.extend([Path.MOVETO, Path.LINETO])
    patches.append(
        PathPatch(
            Path(vertices=t_verts, codes=t_codes),
            facecolor="none",
            edgecolor=feature_color,
            linewidth=feature_w,
            capstyle="round",
            zorder=2,
        )
    )
    return patches


def _build_x_eye_face_patches(
    xform_pt: Callable[[float, float], tuple[float, float]],
    radius: float,
    variant: str,
    feature_color: tuple[float, float, float, float],
    feature_w: float,
) -> list[Circle | PathPatch]:
    """Build X-eyes and mouth patches for 'dizzy' and 'dead' face variants."""
    eye_x = radius * 0.33
    eye_y = radius * 0.18
    d = radius * 0.14
    x_verts = [
        xform_pt(-eye_x - d, eye_y - d),
        xform_pt(-eye_x + d, eye_y + d),
        xform_pt(-eye_x - d, eye_y + d),
        xform_pt(-eye_x + d, eye_y - d),
        xform_pt(eye_x - d, eye_y - d),
        xform_pt(eye_x + d, eye_y + d),
        xform_pt(eye_x - d, eye_y + d),
        xform_pt(eye_x + d, eye_y - d),
    ]
    x_codes = [
        Path.MOVETO,
        Path.LINETO,
        Path.MOVETO,
        Path.LINETO,
        Path.MOVETO,
        Path.LINETO,
        Path.MOVETO,
        Path.LINETO,
    ]
    patches: list[Circle | PathPatch] = [
        PathPatch(
            Path(vertices=x_verts, codes=x_codes),
            facecolor="none",
            edgecolor=feature_color,
            linewidth=feature_w * 1.15,
            capstyle="round",
            zorder=2,
        )
    ]

    my = -radius * 0.30
    if variant == "dizzy":
        w = radius * 0.38
        h = radius * 0.12
        m_verts = [
            xform_pt(-w, my),
            xform_pt(-w * 0.5, my + h),
            xform_pt(0.0, my),
            xform_pt(w * 0.5, my - h),
            xform_pt(w, my),
        ]
        m_codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3, Path.CURVE3, Path.CURVE3]
    else:
        rx = radius * 0.17
        ry = radius * 0.18
        kappa = 0.5522847498307936
        kx = rx * kappa
        ky = ry * kappa
        local_o = [
            (rx, my),
            (rx, my + ky),
            (kx, my + ry),
            (0.0, my + ry),
            (-kx, my + ry),
            (-rx, my + ky),
            (-rx, my),
            (-rx, my - ky),
            (-kx, my - ry),
            (0.0, my - ry),
            (kx, my - ry),
            (rx, my - ky),
            (rx, my),
            (rx, my),
        ]
        m_verts = [xform_pt(lx, ly) for lx, ly in local_o]
        m_codes = [
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

    patches.append(
        PathPatch(
            Path(vertices=m_verts, codes=m_codes),
            facecolor="none",
            edgecolor=feature_color,
            linewidth=feature_w,
            capstyle="round",
            joinstyle="round",
            zorder=2,
        )
    )
    return patches


def _build_face_feature_patches(
    cx: float,
    cy: float,
    radius: float,
    variant: str,
    cos_a: float,
    sin_a: float,
    feature_color: tuple[float, float, float, float],
    feature_w: float,
) -> list[Circle | PathPatch]:
    """Generate eye, eyebrow, and mouth patches for a face shape."""

    def xform_pt(lx: float, ly: float) -> tuple[float, float]:
        return (cx + lx * cos_a - ly * sin_a, cy + lx * sin_a + ly * cos_a)

    if variant == "skull":
        return _build_skull_feature_patches(xform_pt, radius, feature_color, feature_w)
    if variant in {"dizzy", "dead"}:
        return _build_x_eye_face_patches(xform_pt, radius, variant, feature_color, feature_w)

    eye_x = radius * 0.32
    if variant == "devil":
        eye_y = radius * 0.10
        eye_r = radius * 0.105
    elif variant == "angry":
        eye_y = radius * 0.13
        eye_r = radius * 0.105
    else:
        eye_y = radius * 0.20
        eye_r = radius * 0.11

    left_eye = Circle(
        xy=xform_pt(-eye_x, eye_y),
        radius=eye_r,
        facecolor=feature_color,
        edgecolor="none",
        linewidth=0,
        zorder=1,
    )
    right_eye = Circle(
        xy=xform_pt(eye_x, eye_y),
        radius=eye_r,
        facecolor=feature_color,
        edgecolor="none",
        linewidth=0,
        zorder=1,
    )
    patches: list[Circle | PathPatch] = [left_eye, right_eye]

    if variant in {"angry", "devil"}:
        bx_out = 0.50 if variant == "devil" else 0.48
        by_out = 0.38 if variant == "devil" else 0.40
        bx_in = 0.13 if variant == "devil" else 0.15
        by_in = 0.20 if variant == "devil" else 0.25
        brow_verts = [
            xform_pt(-radius * bx_out, radius * by_out),
            xform_pt(-radius * bx_in, radius * by_in),
            xform_pt(radius * bx_out, radius * by_out),
            xform_pt(radius * bx_in, radius * by_in),
        ]
        brow_codes = [Path.MOVETO, Path.LINETO, Path.MOVETO, Path.LINETO]
        patches.append(
            PathPatch(
                Path(vertices=brow_verts, codes=brow_codes),
                facecolor="none",
                edgecolor=feature_color,
                linewidth=feature_w,
                capstyle="round",
                joinstyle="round",
                zorder=1,
            )
        )

    if variant in {"smile", "devil"}:
        mx_out = 0.46 if variant == "devil" else 0.44
        my_out = -0.14 if variant == "devil" else -0.18
        m_verts = [
            xform_pt(-radius * mx_out, radius * my_out),
            xform_pt(-radius * 0.24, -radius * 0.54),
            xform_pt(radius * 0.24, -radius * 0.54),
            xform_pt(radius * mx_out, radius * my_out),
        ]
        m_codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
    elif variant == "neutral":
        m_verts = [
            xform_pt(-radius * 0.36, -radius * 0.28),
            xform_pt(radius * 0.36, -radius * 0.28),
        ]
        m_codes = [Path.MOVETO, Path.LINETO]
    elif variant in {"sad", "angry"}:
        m_verts = [
            xform_pt(-radius * 0.42, -radius * 0.42),
            xform_pt(-radius * 0.22, -radius * 0.14),
            xform_pt(radius * 0.22, -radius * 0.14),
            xform_pt(radius * 0.42, -radius * 0.42),
        ]
        m_codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
    else:
        # "surprised": open 'O' ellipse mouth
        rx = radius * 0.16
        ry = radius * 0.20
        my = -radius * 0.30
        kappa = 0.5522847498307936
        kx = rx * kappa
        ky = ry * kappa
        local_o = [
            (rx, my),
            (rx, my + ky),
            (kx, my + ry),
            (0.0, my + ry),
            (-kx, my + ry),
            (-rx, my + ky),
            (-rx, my),
            (-rx, my - ky),
            (-kx, my - ry),
            (0.0, my - ry),
            (kx, my - ry),
            (rx, my - ky),
            (rx, my),
            (rx, my),
        ]
        m_verts = [xform_pt(lx, ly) for lx, ly in local_o]
        m_codes = [
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

    patches.append(
        PathPatch(
            Path(vertices=m_verts, codes=m_codes),
            facecolor="none",
            edgecolor=feature_color,
            linewidth=feature_w,
            capstyle="round",
            joinstyle="round",
            zorder=1,
        )
    )
    return patches


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
                ShapeUtils.subpaths_to_compound_path(active_subpaths, cx, cy, angle),
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
            leg_verts.extend([xform_pt(r * 0.92 * ux, r * 0.92 * uy), xform_pt(r * 1.20 * ux, r * 1.20 * uy)])
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
    crack_path = ShapeUtils.subpaths_to_compound_path([crack_cw], cx, cy, angle)
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
    subpaths: list[list[Coordinate]] = [ShapeUtils.arc_points_local(0.0, 0.0, r_disk, 0.0, 360.0, 48)[:-1]]
    if variant == "ring":
        subpaths.append(ShapeUtils.arc_points_local(0.0, 0.0, r_disk * 0.58, 360.0, 0.0, 48)[:-1])

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
    return ShapeUtils.subpaths_to_compound_path(subpaths, cx, cy, angle)


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
        raw_all = ShapeUtils.arc_points_local(0.0, 0.0, 1.0, 90.0, 270.0, 48)
    else:
        t_ratio = 0.28 if variant in {"thin", "waxing"} else 0.46
        a1, a2 = 62.0, 298.0
        outer_raw = ShapeUtils.arc_points_local(0.0, 0.0, 1.0, a1, a2, 48)
        x_tip = math.cos(math.radians(a1))
        y_tip = math.sin(math.radians(a1))
        x_belly_in = -1.0 + t_ratio * (1.0 + x_tip)
        dx_sag = x_tip - x_belly_in
        r_in = (y_tip * y_tip + dx_sag * dx_sag) / (2.0 * dx_sag)
        cx_in = x_belly_in + r_in
        ang_in = math.degrees(math.asin(min(0.999, y_tip / r_in)))
        inner_raw = ShapeUtils.arc_points_local(cx_in, 0.0, r_in, 180.0 + ang_in, 180.0 - ang_in, 48)
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

    return ShapeUtils.subpaths_to_compound_path([local_pts], cx, cy, angle)


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

    path_points = ShapeUtils.round_polygon_points(world_pts, shape_r)
    return ShapeUtils.build_matplotlib_path(path_points)


def _gear_arc_bezier_segment(
    radius: float,
    a_start: float,
    a_end: float,
    cx: float,
    cy: float,
) -> tuple[Coordinate, Coordinate, Coordinate]:
    """Return cubic Bezier control and end points for a circular arc from a_start to a_end."""
    alpha = a_end - a_start
    k = (4.0 / 3.0) * math.tan(alpha / 4.0)
    x0 = cx + radius * math.cos(a_start)
    y0 = cy + radius * math.sin(a_start)
    x3 = cx + radius * math.cos(a_end)
    y3 = cy + radius * math.sin(a_end)
    cp1 = (x0 - k * radius * math.sin(a_start), y0 + k * radius * math.cos(a_start))
    cp2 = (x3 + k * radius * math.sin(a_end), y3 - k * radius * math.cos(a_end))
    return (cp1, cp2, (x3, y3))


def _build_gear_outer_path_points(
    cx: float,
    cy: float,
    num_teeth: int,
    radius_ext: float,
    radius_int: float,
    ext_ratio: float,
    int_ratio: float,
    angle: float,
    shape_r: float | tuple[float, ...] | None,
) -> PathPoints:
    """Build outer path points for a gear shape with either rounded corners or exact circular arcs."""
    pitch_angle = (2.0 * math.pi) / num_teeth
    half_ext = (ext_ratio * pitch_angle) / 2.0
    half_int = (int_ratio * pitch_angle) / 2.0
    start_angle = math.pi / 2.0 + math.radians(angle)

    radii = ShapeUtils._normalize_shape_radii(4 * num_teeth, shape_r)
    if radii is not None:
        points_world: list[Coordinate] = []
        for i in range(num_teeth):
            center_a = start_angle + i * pitch_angle
            a1 = center_a - half_int
            a2 = center_a - half_ext
            a3 = center_a + half_ext
            a4 = center_a + half_int
            points_world.append((cx + radius_int * math.cos(a1), cy + radius_int * math.sin(a1)))
            points_world.append((cx + radius_ext * math.cos(a2), cy + radius_ext * math.sin(a2)))
            points_world.append((cx + radius_ext * math.cos(a3), cy + radius_ext * math.sin(a3)))
            points_world.append((cx + radius_int * math.cos(a4), cy + radius_int * math.sin(a4)))
        return ShapeUtils.round_polygon_points(points_world, shape_r)

    path_points: PathPoints = []
    for i in range(num_teeth):
        center_a = start_angle + i * pitch_angle
        a1 = center_a - half_int
        a2 = center_a - half_ext
        a3 = center_a + half_ext
        a4 = center_a + half_int
        next_a1 = (start_angle + (i + 1) * pitch_angle) - half_int

        if i == 0:
            path_points.append((cx + radius_int * math.cos(a1), cy + radius_int * math.sin(a1)))
        path_points.append((cx + radius_ext * math.cos(a2), cy + radius_ext * math.sin(a2)))
        path_points.append(_gear_arc_bezier_segment(radius_ext, a2, a3, cx, cy))
        path_points.append((cx + radius_int * math.cos(a4), cy + radius_int * math.sin(a4)))
        path_points.append(_gear_arc_bezier_segment(radius_int, a4, next_a1, cx, cy))
    return path_points


def _build_not_equal_polygon(hw: float, hh: float, ht: float) -> list[Coordinate]:
    """Build a single unified 20-vertex polygon for the not-equal (≠) symbol without internal seams."""
    bh = min(ht * 0.85, hh * 0.24)
    y_mid = min(hh * 0.42, max(bh * 1.6, hh * 0.36))
    y1 = y_mid - bh
    y2 = y_mid + bh
    sw = min(ht * 0.85, hw * 0.28)
    ks = min(0.32, (hw - sw) / max(hh, 1e-6) * 0.55)

    def xl(y_val: float) -> float:
        return ks * y_val - sw

    def xr(y_val: float) -> float:
        return ks * y_val + sw

    return [
        (xr(hh), hh),
        (xl(hh), hh),
        (xl(y2), y2),
        (-hw, y2),
        (-hw, y1),
        (xl(y1), y1),
        (xl(-y1), -y1),
        (-hw, -y1),
        (-hw, -y2),
        (xl(-y2), -y2),
        (xl(-hh), -hh),
        (xr(-hh), -hh),
        (xr(-y2), -y2),
        (hw, -y2),
        (hw, -y1),
        (xr(-y1), -y1),
        (xr(y1), y1),
        (hw, y1),
        (hw, y2),
        (xr(y2), y2),
    ]


def _build_math_symbol_components(
    symbol: str,
    width: float,
    height: float,
    t_ratio: float,
) -> tuple[list[list[Coordinate]], list[tuple[Coordinate, float]]]:
    """Return local polygon vertex lists and circular dot specs for a math symbol."""
    s = min(width, height)
    t = t_ratio * s
    hw = width / 2.0
    hh = height / 2.0
    ht = t / 2.0

    if symbol in {"+", "plus"}:
        hx = min(ht, hw * 0.85)
        hy = min(ht, hh * 0.85)
        poly = [
            (hx, hy),
            (hx, hh),
            (-hx, hh),
            (-hx, hy),
            (-hw, hy),
            (-hw, -hy),
            (-hx, -hy),
            (-hx, -hh),
            (hx, -hh),
            (hx, -hy),
            (hw, -hy),
            (hw, hy),
        ]
        return [poly], []

    if symbol in {"-", "−", "minus"}:
        hy = min(ht, hh * 0.85)
        return [[(-hw, -hy), (hw, -hy), (hw, hy), (-hw, hy)]], []

    if symbol in {"*", "x", "×", "multiply"}:
        hs = s / 2.0
        ht_s = min(ht, hs * 0.72)
        arm = max(ht_s * 1.15, hs * 1.0)
        base_cross = [
            (ht_s, ht_s),
            (ht_s, arm),
            (-ht_s, arm),
            (-ht_s, ht_s),
            (-arm, ht_s),
            (-arm, -ht_s),
            (-ht_s, -ht_s),
            (-ht_s, -arm),
            (ht_s, -arm),
            (ht_s, -ht_s),
            (arm, -ht_s),
            (arm, ht_s),
        ]
        scale_x = width / s
        scale_y = height / s
        rotated: list[Coordinate] = []
        for px, py in base_cross:
            rx, ry = rotate_point((px, py), angle=45.0)
            rotated.append((rx * scale_x, ry * scale_y))
        return [rotated], []

    if symbol in {"=", "equal"}:
        bh = min(ht * 0.85, hh * 0.36)
        y_off = min(hh - bh, max(bh * 1.45, hh * 0.44))
        top_bar = [(-hw, y_off - bh), (hw, y_off - bh), (hw, y_off + bh), (-hw, y_off + bh)]
        bot_bar = [(-hw, -y_off - bh), (hw, -y_off - bh), (hw, -y_off + bh), (-hw, -y_off + bh)]
        return [top_bar, bot_bar], []

    if symbol in {"/", "÷", "divide"}:
        bh = min(ht * 0.82, hh * 0.25)
        bar = [(-hw, -bh), (hw, -bh), (hw, bh), (-hw, bh)]
        r_dot = min(bh * 1.25, (hh - bh) * 0.42)
        y_dot = min(hh - r_dot, max(bh + r_dot * 1.35, hh * 0.60))
        return [bar], [((0.0, y_dot), r_dot), ((0.0, -y_dot), r_dot)]

    return [_build_not_equal_polygon(hw, hh, ht)], []


def _build_math_symbol_path(
    cx: float,
    cy: float,
    symbol: str,
    width: float,
    height: float,
    t_ratio: float,
    angle: float,
    shape_r: float | tuple[float, ...] | None,
) -> Path:
    """Construct the world-space Matplotlib Path for a math_symbol."""
    polygons_local, dots_local = _build_math_symbol_components(symbol, width, height, t_ratio)
    sub_paths: list[Path] = []

    for poly in polygons_local:
        verts_world: list[Coordinate] = []
        for pt in poly:
            rx, ry = rotate_point(pt, angle=angle)
            verts_world.append((rx + cx, ry + cy))
        path_points = ShapeUtils.round_polygon_points(verts_world, shape_r)
        sub_paths.append(ShapeUtils.build_matplotlib_path(path_points))

    for dot_xy, dot_r in dots_local:
        rx, ry = rotate_point(dot_xy, angle=angle)
        sub_paths.append(ShapeUtils.build_ellipse_path(rx + cx, ry + cy, dot_r, dot_r, cw=False))

    if len(sub_paths) == 1:
        return sub_paths[0]
    return Path.make_compound_path(*sub_paths)


__all__ = [
    "_LIGHTNING_RAW_SPECS",
    "_SEG7_MASKS",
    "_build_7seg_digit_polygons",
    "_build_clock_hardware_patches",
    "_build_digital_clock_patches",
    "_build_face_feature_patches",
    "_build_face_head_patch",
    "_build_gear_outer_path_points",
    "_build_math_symbol_components",
    "_build_math_symbol_path",
    "_build_not_equal_polygon",
    "_build_skull_feature_patches",
    "_build_x_eye_face_patches",
    "_gear_arc_bezier_segment",
    "build_clock_patches",
    "build_heart_path",
    "build_lightning_path",
    "build_moon_path",
    "build_sun_path",
]
