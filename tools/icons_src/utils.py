# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Shared color palettes, style builders, and geometric primitives for `tools/icons_src/`."""

from __future__ import annotations

import math
from typing import Any

from drawlib.canvas import setup
from drawlib.lines import line, lines, lines_curved
from drawlib.shapes import arc, circle, ellipse, polygon, rectangle, shape
from drawlib.styles import Colors, Style

# ==============================================================================
# 1. Canvas Unit-to-Point Conversion (100x100 canvas -> 720pt width)
# ==============================================================================

CANVAS_SIZE: int = 100
CANVAS_DPI: int = 200
PTS_PER_UNIT: float = 720.0 / float(CANVAS_SIZE)

# Cubic Bezier kappa for exact 90-degree circular arc fillets
KAPPA: float = 0.55228475


def pt(units: float) -> float:
    """Convert stroke width in 100x100 canvas units into Matplotlib points."""
    return units * PTS_PER_UNIT


def setup_icon() -> None:
    """Initialize a transparent 100x100 icon canvas at 200 DPI (2000x2000 supersampled)."""
    setup(
        width=CANVAS_SIZE,
        height=CANVAS_SIZE,
        dpi=CANVAS_DPI,
        color=Colors.Canvas,
        alpha=0.0,
    )


# ==============================================================================
# 2. Color Palettes (`original/` and `gcp/`)
# ==============================================================================

DARK = Colors.Dark  # #323A48 (Deep Slate structural outline)
ORIG_STROKE: float = 2.7  # Refined structural stroke width in 100x100 units

PASTEL_BLUE = "#86A4F7"  # Soft Pastel Cornflower Blue (primary surface)
PASTEL_BLUE_LIGHT = "#ACC2FA"  # Lighter pastel blue companion tint
PASTEL_GREEN = "#7AD69E"  # Soft Pastel Mint/Sage Green (secondary/accent surface)
WHITE = Colors.White  # Crisp white fill (#FFFFFF)

# Modern 4-Color GCP Palette (core_products & category_*)
GCP_BLUE = "#4285F4"
GCP_RED = "#EA4335"
GCP_YELLOW = "#FBBC04"
GCP_GREEN = "#34A853"
GCP_DARK_BLUE = "#1A73E8"
GCP_GREY = "#9AA0A6"

# 3-Tone GCP Tech Blues (legacy & blue-toned services)
GCP_TECH_DARK = "#3367D6"
GCP_TECH_MID = "#4285F4"
GCP_TECH_MED_LIGHT = "#669DF6"
GCP_TECH_LIGHT = "#AECBFA"

# Hexagonal Badge Palette (legacy hexagonal plate icons)
GCP_HEX_LEFT = "#5C85DE"
GCP_HEX_RIGHT = "#4285F4"
GCP_HEX_SHADOW = "#3367D6"

# AWS Official Category Palette (Service & Category Icons)
AWS_ORANGE = "#ED7100"
AWS_TEAL = "#01A88D"
AWS_RED = "#DD344C"
AWS_PURPLE = "#8C4FFF"
AWS_PINK = "#E7157B"
AWS_MAGENTA = "#C925D1"
AWS_GREEN = "#7AA116"
AWS_SQUID_INK = "#232F3E"
AWS_GRAY_BORDER = "#7D8998"

# Azure Official Multi-Tone Palette
AZURE_BLUE = "#0078D4"
AZURE_DARK_BLUE = "#005BA1"
AZURE_LIGHT_BLUE = "#5EA0EF"
AZURE_PALE_BLUE = "#83B9F9"
AZURE_CYAN = "#50E6FF"
AZURE_LIGHT_CYAN = "#9CEBFF"
AZURE_PALE_CYAN = "#C3F1FF"
AZURE_TEAL = "#32BEDD"
AZURE_DARK_TEAL = "#198AB3"
AZURE_PURPLE = "#773ADC"
AZURE_LIGHT_PURPLE = "#A67AF4"
AZURE_DARK_PURPLE = "#341A6E"
AZURE_GREEN = "#76BC2D"
AZURE_LIGHT_GREEN = "#86D633"
AZURE_DARK_GREEN = "#5E9624"
AZURE_ORANGE = "#F78D1E"
AZURE_YELLOW = "#FFB900"
AZURE_RED = "#E62325"
AZURE_GRAY = "#949494"
AZURE_DARK_GRAY = "#707070"
AZURE_LIGHT_GRAY = "#CCCCCC"
AZURE_PALE_GRAY = "#F2F2F2"

# ==============================================================================
# 3. Style Factory Helpers
# ==============================================================================


def fill_style(
    fill_color: Any,
    *,
    border_color: Any | None = None,
    border_units: float = 0.0,
    shape_r: float | tuple[float, ...] | None = None,
    angle: float | None = None,
    alpha: float | None = None,
) -> Style:
    """Create a shape Style with unit-converted border width."""
    b_col = fill_color if border_color is None else border_color
    kw: dict[str, Any] = {
        "shape_fill_color": fill_color,
        "shape_line_color": b_col,
        "shape_line_width": pt(border_units) if border_units > 0 else 0.0,
        "shape_line_style": "solid",
    }
    if shape_r is not None:
        kw["shape_r"] = shape_r
    if angle is not None:
        kw["angle"] = angle
    if alpha is not None:
        kw["alpha"] = alpha
    return Style(**kw)


def no_border_fill(fill_color: Any, *, shape_r: float | None = None) -> Style:
    """Create a borderless fill style with zero line width and matching edge color."""
    kw: dict[str, Any] = {
        "shape_fill_color": fill_color,
        "shape_line_color": fill_color,
        "shape_line_width": 0.0,
    }
    if shape_r is not None:
        kw["shape_r"] = shape_r
    return Style(**kw)


def stroke_style(
    color: Any = DARK,
    *,
    width_units: float = ORIG_STROKE,
    line_style: str = "solid",
) -> Style:
    """Create a line/arc stroke Style with unit-converted stroke width."""
    return Style(
        line_color=color,
        line_width=pt(width_units),
        line_style=line_style,  # type: ignore[arg-type]
        shape_line_color=color,
        shape_line_width=pt(width_units),
        shape_line_style=line_style,  # type: ignore[arg-type]
        shape_fill_color=Colors.Transparent,
    )


# ==============================================================================
# 4. Line, Capsule & Path Primitives
# ==============================================================================


def corner_arc(
    p_in: tuple[float, float],
    corner: tuple[float, float],
    p_out: tuple[float, float],
) -> tuple[tuple[float, float], tuple[float, float], tuple[float, float]]:
    """Compute cubic Bezier control points for an exact 90-degree circular corner."""
    cx, cy = corner
    cp1 = (p_in[0] + KAPPA * (cx - p_in[0]), p_in[1] + KAPPA * (cy - p_in[1]))
    cp2 = (p_out[0] + KAPPA * (cx - p_out[0]), p_out[1] + KAPPA * (cy - p_out[1]))
    return (cp1, cp2, p_out)


def draw_cap(
    xy: tuple[float, float],
    *,
    width_units: float = ORIG_STROKE,
    color: Any = DARK,
) -> None:
    """Draw a circular round cap of diameter width_units at xy."""
    circle(xy, radius=width_units / 2.0, style=fill_style(color))


def draw_round_segment(
    xy1: tuple[float, float],
    xy2: tuple[float, float],
    *,
    width_units: float = ORIG_STROKE,
    color: Any = DARK,
) -> None:
    """Draw a straight line segment with smooth circular end caps."""
    line(xy1, xy2, style=stroke_style(color, width_units=width_units))
    r = width_units / 2.0
    st = fill_style(color)
    circle(xy1, radius=r, style=st)
    circle(xy2, radius=r, style=st)


def draw_round_polyline(
    points: list[tuple[float, float]],
    *,
    width_units: float = ORIG_STROKE,
    color: Any = DARK,
    corner_r: float = 0.0,
    closed: bool = False,
) -> None:
    """Draw a multi-point polyline with rounded joins and end caps."""
    st = stroke_style(color, width_units=width_units)
    pts = [*points, points[0]] if closed else points
    if corner_r > 0.0 and len(pts) >= 3:
        lines_curved(pts, r=corner_r, style=st)
    else:
        lines(pts, style=st)
    cap_st = fill_style(color)
    r = width_units / 2.0
    if corner_r > 0.0 and not closed:
        circle(pts[0], radius=r, style=cap_st)
        circle(pts[-1], radius=r, style=cap_st)
    else:
        for p in points:
            circle(p, radius=r, style=cap_st)


def draw_capsule(
    xy1: tuple[float, float],
    xy2: tuple[float, float],
    *,
    width_units: float,
    color: Any,
    cap_start: bool = True,
    cap_end: bool = True,
) -> None:
    """Draw a geometric stadium/capsule bar between xy1 and xy2 in canvas units."""
    x1, y1 = xy1
    x2, y2 = xy2
    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy)
    r = width_units / 2.0
    st = fill_style(color)
    if length > 1e-6:
        nx = -dy / length * r
        ny = dx / length * r
        verts = [
            (x1 + nx, y1 + ny),
            (x2 + nx, y2 + ny),
            (x2 - nx, y2 - ny),
            (x1 - nx, y1 - ny),
        ]
        polygon(verts, style=st)
    if cap_start:
        circle(xy1, radius=r, style=st)
    if cap_end:
        circle(xy2, radius=r, style=st)


def draw_chunky_arrow(
    *,
    y_center: float,
    x_tail: float,
    x_tip: float,
    x_head_base: float,
    shaft_half_h: float,
    head_half_h: float,
    fill_color: Any,
    border_units: float = ORIG_STROKE,
    border_color: Any = DARK,
) -> None:
    """Draw a unified single-polygon horizontal arrow with smooth rounded joins."""
    pts = [
        (x_tail, y_center - shaft_half_h),
        (x_head_base, y_center - shaft_half_h),
        (x_head_base, y_center - head_half_h),
        (x_tip, y_center),
        (x_head_base, y_center + head_half_h),
        (x_head_base, y_center + shaft_half_h),
        (x_tail, y_center + shaft_half_h),
    ]
    polygon(pts, style=fill_style(fill_color))
    if border_units > 0:
        draw_round_polyline(pts, width_units=border_units, color=border_color, closed=True)


# ==============================================================================
# 5. 3D & Domain Geometric Primitives
# ==============================================================================


def draw_iso_cube(
    cx: float,
    cy: float,
    radius: float,
    *,
    top_color: Any,
    left_color: Any,
    right_color: Any,
    border_color: Any | None = DARK,
    border_units: float = ORIG_STROKE,
) -> dict[str, tuple[float, float]]:
    """Draw an isometric 3D cube centered at (cx, cy) and return key vertices."""
    dx = radius * math.cos(math.radians(30.0))
    dy = radius * math.sin(math.radians(30.0))

    v_center = (cx, cy)
    v_top = (cx, cy + radius)
    v_tr = (cx + dx, cy + dy)
    v_br = (cx + dx, cy - dy)
    v_bottom = (cx, cy - radius)
    v_bl = (cx - dx, cy - dy)
    v_tl = (cx - dx, cy + dy)

    polygon([v_center, v_tl, v_top, v_tr], style=fill_style(top_color))
    polygon([v_center, v_bottom, v_bl, v_tl], style=fill_style(left_color))
    polygon([v_center, v_tr, v_br, v_bottom], style=fill_style(right_color))

    if border_color is not None and border_units > 0.0:
        outer = [v_top, v_tr, v_br, v_bottom, v_bl, v_tl]
        draw_round_polyline(outer, width_units=border_units, color=border_color, closed=True)
        for v in (v_tl, v_tr, v_bottom):
            draw_round_segment(v_center, v, width_units=border_units * 0.9, color=border_color)

    return {
        "center": v_center,
        "top": v_top,
        "tr": v_tr,
        "br": v_br,
        "bottom": v_bottom,
        "bl": v_bl,
        "tl": v_tl,
    }


def draw_cylinder_tier(
    cx: float,
    y_bottom: float,
    width: float,
    body_h: float,
    ry: float,
    *,
    body_color: Any,
    top_color: Any | None = None,
    border_color: Any = DARK,
    border_units: float = ORIG_STROKE,
    draw_top_cap: bool = True,
) -> None:
    """Draw a single 3D cylinder tier from y_bottom to y_bottom + body_h."""
    y_top = y_bottom + body_h
    w_half = width / 2.0

    ellipse((cx, y_bottom), width=width, height=ry * 2.0, style=fill_style(body_color))
    if body_h > 0:
        rectangle((cx, y_bottom + body_h / 2.0), width=width, height=body_h, style=fill_style(body_color))

    arc(
        (cx, y_bottom),
        width=width,
        height=ry * 2.0,
        angle_start=180.0,
        angle_end=360.0,
        style=stroke_style(border_color, width_units=border_units),
    )
    if body_h > 0:
        draw_round_segment((cx - w_half, y_bottom), (cx - w_half, y_top), width_units=border_units, color=border_color)
        draw_round_segment((cx + w_half, y_bottom), (cx + w_half, y_top), width_units=border_units, color=border_color)

    if draw_top_cap:
        t_col = body_color if top_color is None else top_color
        ellipse(
            (cx, y_top),
            width=width,
            height=ry * 2.0,
            style=fill_style(t_col, border_color=border_color, border_units=border_units),
        )


def build_shield_half_points(
    cx: float,
    y_bottom: float,
    y_top: float,
    half_w: float,
    *,
    side: str,
) -> list[tuple[float, float]]:
    """Generate smooth polygon vertices for the left or right half of a heraldic shield."""
    height = y_top - y_bottom
    y_shoulder = y_top - height * 0.11
    y_waist = y_bottom + height * 0.50
    sign = -1.0 if side == "left" else 1.0
    x_edge = cx + sign * half_w

    p0 = (x_edge, y_waist)
    p1 = (x_edge, y_bottom + height * 0.21)
    p2 = (cx + sign * (half_w * 0.45), y_bottom + height * 0.065)
    p3 = (cx, y_bottom)

    curve_pts: list[tuple[float, float]] = []
    steps = 20
    for i in range(steps + 1):
        t = i / steps
        mt = 1.0 - t
        bx = (mt**3) * p0[0] + 3 * (mt**2) * t * p1[0] + 3 * mt * (t**2) * p2[0] + (t**3) * p3[0]
        by = (mt**3) * p0[1] + 3 * (mt**2) * t * p1[1] + 3 * mt * (t**2) * p2[1] + (t**3) * p3[1]
        curve_pts.append((bx, by))

    return [
        (cx, y_top),
        (x_edge, y_shoulder),
        *curve_pts,
    ]


def build_sparkle_4pt_polygon(
    cx: float,
    cy: float,
    outer_r: float,
    inner_r: float,
) -> list[tuple[float, float]]:
    """Build smooth 4-pointed sparkle vertices in exact canvas coordinates."""
    tips = [
        (cx, cy + outer_r),
        (cx + outer_r, cy),
        (cx, cy - outer_r),
        (cx - outer_r, cy),
    ]
    diag = inner_r * math.cos(math.radians(45.0))
    controls = [
        (cx + diag, cy + diag),
        (cx + diag, cy - diag),
        (cx - diag, cy - diag),
        (cx - diag, cy + diag),
    ]
    pts: list[tuple[float, float]] = []
    steps = 16
    for i in range(4):
        p0 = tips[i]
        ctrl = controls[i]
        p2 = tips[(i + 1) % 4]
        for s in range(steps):
            t = s / steps
            mt = 1.0 - t
            bx = (mt**2) * p0[0] + 2 * mt * t * ctrl[0] + (t**2) * p2[0]
            by = (mt**2) * p0[1] + 2 * mt * t * ctrl[1] + (t**2) * p2[1]
            pts.append((bx, by))
    return pts


def draw_sparkle_4pt(
    cx: float,
    cy: float,
    outer_r: float,
    inner_r: float,
    *,
    fill_color: Any,
    border_color: Any | None = DARK,
    border_units: float = ORIG_STROKE,
) -> None:
    """Draw a smooth 4-pointed AI sparkle centered at (cx, cy)."""
    r = outer_r
    c = inner_r
    path_pts: list[Any] = [
        (r, 2 * r),
        ((r + c, r + c), (2 * r, r)),
        ((r + c, r - c), (r, 0.0)),
        ((r - c, r - c), (0.0, r)),
        ((r - c, r + c), (r, 2 * r)),
    ]
    shape(
        xy=(cx, cy),
        path_points=path_pts,
        is_default_center=True,
        style=fill_style(fill_color, border_color=border_color, border_units=border_units),
    )


# ==============================================================================
# 6. GCP Specific Geometric Helpers
# ==============================================================================


def draw_rounded_corner_block(
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    *,
    r: float,
    round_tl: bool = False,
    round_tr: bool = False,
    round_br: bool = False,
    round_bl: bool = False,
    color: str,
) -> None:
    """Draw an axis-aligned rectangular block with selective rounded corners."""
    st = fill_style(color)
    pts: list[tuple[float, float]] = []
    steps = 16

    if round_bl and r > 0:
        cx, cy = x0 + r, y0 + r
        for i in range(steps + 1):
            ang = math.radians(180.0 + 90.0 * (i / steps))
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    else:
        pts.append((x0, y0))

    if round_br and r > 0:
        cx, cy = x1 - r, y0 + r
        for i in range(steps + 1):
            ang = math.radians(270.0 + 90.0 * (i / steps))
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    else:
        pts.append((x1, y0))

    if round_tr and r > 0:
        cx, cy = x1 - r, y1 - r
        for i in range(steps + 1):
            ang = math.radians(0.0 + 90.0 * (i / steps))
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    else:
        pts.append((x1, y1))

    if round_tl and r > 0:
        cx, cy = x0 + r, y1 - r
        for i in range(steps + 1):
            ang = math.radians(90.0 + 90.0 * (i / steps))
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    else:
        pts.append((x0, y1))

    polygon(pts, style=st)


def draw_pin_h(
    x_inner: float,
    x_tip: float,
    yc: float,
    width: float,
    color: str,
) -> None:
    """Draw a horizontal pin with a flat inner root at x_inner and semicircular tip at x_tip."""
    r = width / 2.0
    st = fill_style(color)
    steps = 20
    pts: list[tuple[float, float]] = []
    if x_tip < x_inner:
        cx = x_tip + r
        pts.append((x_inner, yc + r))
        for i in range(steps + 1):
            ang = math.radians(90.0 + 180.0 * (i / steps))
            pts.append((cx + r * math.cos(ang), yc + r * math.sin(ang)))
        pts.append((x_inner, yc - r))
    else:
        cx = x_tip - r
        pts.append((x_inner, yc - r))
        for i in range(steps + 1):
            ang = math.radians(-90.0 + 180.0 * (i / steps))
            pts.append((cx + r * math.cos(ang), yc + r * math.sin(ang)))
        pts.append((x_inner, yc + r))
    polygon(pts, style=st)


def draw_pin_v(
    xc: float,
    y_inner: float,
    y_tip: float,
    width: float,
    color: str,
) -> None:
    """Draw a vertical pin with a flat inner root at y_inner and semicircular tip at y_tip."""
    r = width / 2.0
    st = fill_style(color)
    steps = 20
    pts: list[tuple[float, float]] = []
    if y_tip > y_inner:
        cy = y_tip - r
        pts.append((xc + r, y_inner))
        for i in range(steps + 1):
            ang = math.radians(0.0 + 180.0 * (i / steps))
            pts.append((xc + r * math.cos(ang), cy + r * math.sin(ang)))
        pts.append((xc - r, y_inner))
    else:
        cy = y_tip + r
        pts.append((xc - r, y_inner))
        for i in range(steps + 1):
            ang = math.radians(180.0 + 180.0 * (i / steps))
            pts.append((xc + r * math.cos(ang), cy + r * math.sin(ang)))
        pts.append((xc + r, y_inner))
    polygon(pts, style=st)


def draw_radial_spoke(
    cx: float,
    cy: float,
    angle_deg: float,
    r_inner: float,
    r_outer: float,
    width_units: float,
    color: str,
) -> None:
    """Draw a constant-width spoke whose inner edge follows a concentric concave circle of radius r_inner."""
    half_w = width_units / 2.0
    theta = math.radians(angle_deg)
    ux, uy = math.cos(theta), math.sin(theta)
    nx, ny = -uy, ux

    steps = 12
    verts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        t = -half_w + (2.0 * half_w) * (i / steps)
        d_rad = math.sqrt(max(0.0, r_inner * r_inner - t * t))
        px = cx + d_rad * ux + t * nx
        py = cy + d_rad * uy + t * ny
        verts.append((px, py))

    verts.append((cx + r_outer * ux + half_w * nx, cy + r_outer * uy + half_w * ny))
    verts.append((cx + r_outer * ux - half_w * nx, cy + r_outer * uy - half_w * ny))
    polygon(verts, style=fill_style(color))


def draw_gcp_hex_plate(
    cx: float = 50.0,
    cy: float = 50.0,
    radius: float = 42.0,
    *,
    left_color: str = GCP_HEX_LEFT,
    right_color: str = GCP_HEX_RIGHT,
    corner_r: float = 3.5,
) -> None:
    """Draw a standard GCP pointy-top two-tone hexagonal plate."""
    dx = radius * math.cos(math.radians(30.0))
    dy = radius * math.sin(math.radians(30.0))
    v_top = (cx, cy + radius)
    v_tr = (cx + dx, cy + dy)
    v_br = (cx + dx, cy - dy)
    v_bot = (cx, cy - radius)
    v_bl = (cx - dx, cy - dy)
    v_tl = (cx - dx, cy + dy)

    polygon(
        [v_top, v_tl, v_bl, v_bot],
        style=fill_style(left_color, shape_r=(0.0, corner_r, corner_r, 0.0)),
    )
    polygon(
        [v_top, v_bot, v_br, v_tr],
        style=fill_style(right_color, shape_r=(0.0, 0.0, corner_r, corner_r)),
    )


def _signed_area(ring: list[tuple[float, float]]) -> float:
    """Compute signed area of a 2D polygon ring (>0 for CCW, <0 for CW)."""
    n = len(ring)
    if n < 3:
        return 0.0
    area = 0.0
    for i in range(n):
        x1, y1 = ring[i]
        x2, y2 = ring[(i + 1) % n]
        area += x1 * y2 - x2 * y1
    return 0.5 * area


def _point_in_ring(pt_xy: tuple[float, float], ring: list[tuple[float, float]]) -> bool:
    """Ray-casting point-in-polygon check."""
    px, py = pt_xy
    inside = False
    n = len(ring)
    for i in range(n):
        x1, y1 = ring[i]
        x2, y2 = ring[(i + 1) % n]
        if ((y1 > py) != (y2 > py)) and (px < (x2 - x1) * (py - y1) / (y2 - y1 + 1e-12) + x1):
            inside = not inside
    return inside


def _orient_ring(ring: list[tuple[float, float]], *, ccw: bool) -> list[tuple[float, float]]:
    """Return a copy of ring oriented counter-clockwise (ccw=True) or clockwise (ccw=False)."""
    pts = list(ring)
    is_ccw = _signed_area(pts) > 0
    if is_ccw != ccw:
        pts.reverse()
    return pts


def _ring_inside_ring(inner: list[tuple[float, float]], outer: list[tuple[float, float]]) -> bool:
    """Return True if inner ring is contained inside outer ring (tolerant of shared boundary vertices)."""
    cx = sum(p[0] for p in inner) / len(inner)
    cy = sum(p[1] for p in inner) / len(inner)
    step = max(1, len(inner) // 8)
    samples = [(cx, cy), *(inner[k] for k in range(0, len(inner), step))]
    inside_cnt = sum(1 for pt in samples if _point_in_ring(pt, outer))
    return inside_cnt > len(samples) // 2


def _splice_holes_into_outer(
    outer: list[tuple[float, float]],
    holes: list[list[tuple[float, float]]],
) -> list[tuple[float, float]]:
    """Bridge inner CW hole rings into a CCW outer polygon ring at closest edge points."""
    pts: list[tuple[float, float]] = list(outer)
    prepared_holes: list[list[tuple[float, float]]] = []
    for raw_hole in holes:
        hole = _orient_ring(raw_hole, ccw=False)
        rmost = max(range(len(hole)), key=lambda k: hole[k][0])
        prepared_holes.append(hole[rmost:] + hole[:rmost])
    prepared_holes.sort(key=lambda h: -h[0][0])

    for hole in prepared_holes:
        hx, hy = hole[0]
        best_k = 0
        best_dist2 = float("inf")
        best_q = pts[0]
        m_pts = len(pts)
        for k in range(m_pts):
            ax, ay = pts[k]
            bx, by = pts[(k + 1) % m_pts]
            dx, dy = bx - ax, by - ay
            seg_len2 = dx * dx + dy * dy
            t = max(0.0, min(1.0, ((hx - ax) * dx + (hy - ay) * dy) / seg_len2)) if seg_len2 > 1e-12 else 0.0
            qx = round(ax + t * dx, 2)
            qy = round(ay + t * dy, 2)
            d2 = (hx - qx) ** 2 + (hy - qy) ** 2
            if d2 < best_dist2:
                best_dist2 = d2
                best_k = k
                best_q = (qx, qy)
        pts = pts[: best_k + 1] + [best_q, *hole, hole[0], best_q] + pts[best_k + 1 :]
    return pts


def draw_compound_polygon(
    rings: list[list[tuple[float, float]]],
    *,
    color: Any,
    alpha: float | None = None,
) -> None:
    """Draw a single or multi-contour polygon with transparent cutout holes using `polygon()`.

    Automatically determines outer contours (even containment depth, oriented CCW)
    and inner holes (odd containment depth, oriented CW) and bridges each hole to its
    parent outer contour with zero-width opposite-winding segments.
    """
    valid_rings = [r for r in rings if len(r) >= 3 and abs(_signed_area(r)) > 1e-5]
    if not valid_rings:
        return
    st = fill_style(color, alpha=alpha)
    if len(valid_rings) == 1:
        polygon(valid_rings[0], style=st)
        return

    n = len(valid_rings)
    areas = [abs(_signed_area(r)) for r in valid_rings]
    parents: list[int | None] = [None] * n
    depths: list[int] = [0] * n

    for i in range(n):
        containing = [
            j for j in range(n) if j != i and areas[j] > areas[i] and _ring_inside_ring(valid_rings[i], valid_rings[j])
        ]
        depths[i] = len(containing)
        if containing:
            parents[i] = min(containing, key=lambda j: areas[j])

    for i in range(n):
        if depths[i] % 2 != 0:
            continue
        outer = _orient_ring(valid_rings[i], ccw=True)
        child_holes = [valid_rings[j] for j in range(n) if parents[j] == i and depths[j] == depths[i] + 1]
        pts = _splice_holes_into_outer(outer, child_holes) if child_holes else outer
        polygon(pts, style=st)


def draw_layered_polygons(
    rings: list[list[tuple[float, float]]],
    *,
    fg_color: Any,
    bg_color: Any,
) -> None:
    """Draw multi-contour rings on a solid background by alternating fg_color and bg_color by containment depth."""
    valid_rings = [r for r in rings if len(r) >= 3 and abs(_signed_area(r)) > 1e-5]
    if not valid_rings:
        return
    n = len(valid_rings)
    areas = [abs(_signed_area(r)) for r in valid_rings]
    order = sorted(range(n), key=lambda i: -areas[i])
    for i in order:
        depth = sum(
            1 for j in range(n) if j != i and areas[j] > areas[i] and _ring_inside_ring(valid_rings[i], valid_rings[j])
        )
        col = fg_color if depth % 2 == 0 else bg_color
        polygon(valid_rings[i], style=fill_style(col))


def draw_aws_service_plate(color: Any) -> None:
    """Draw a standard AWS Architecture Service square background tile in [8.0, 92.0]."""
    rectangle((50.0, 50.0), width=84.0, height=84.0, style=fill_style(color))


def draw_aws_category_plate(color: Any, *, border_color: Any = "#879196") -> None:
    """Draw a standard AWS Category framed background tile in [8.0, 92.0]."""
    outer = [(8.0, 8.0), (92.0, 8.0), (92.0, 92.0), (8.0, 92.0)]
    inner = [(9.87, 9.87), (90.13, 9.87), (90.13, 90.13), (9.87, 90.13)]
    draw_compound_polygon([outer, inner], color=border_color)
    rectangle((50.0, 50.0), width=74.67, height=74.67, style=fill_style(color))



