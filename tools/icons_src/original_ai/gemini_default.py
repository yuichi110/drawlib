# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: gemini."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    fill_style,
    setup_icon,
)

setup_icon()

w = 2.0
cx, cy = 50.0, 50.0

# Scale from official 24x24 SVG viewBox (half-span 10.9935) to 100x100 canvas (half-span 38.95)
SVG_HALF = 10.9935
CANVAS_HALF = 38.95
SCALE = CANVAS_HALF / SVG_HALF

# Softened Drawlib-toned colors corresponding to official Gemini SVG stops
BLUE_RGB = (78.0, 146.0, 247.0)  # softened #3186FF
GREEN_RGB = (50.0, 190.0, 116.0)  # softened #08B962
RED_RGB = (240.0, 96.0, 94.0)  # softened #F94543
YELLOW_RGB = (245.0, 193.0, 58.0)  # softened #FABC12

# Concave circular arc center (cx_a, cy_a) and radius R_ARC in SVG quadrant (+dx, +dy from center 12,12)
R_ARC_SVG = 14.13
ARC_CENTER_OFFSET_SVG = 14.165
TIP_R_SVG = 0.503
TIP_CENTER_OFFSET_SVG = SVG_HALF - TIP_R_SVG  # 10.4905


def _star_y_top_svg(dx_abs: float) -> float:
    """Return top boundary dy >= 0 in SVG-centered units for given |dx| <= SVG_HALF."""
    if dx_abs >= SVG_HALF:
        return 0.0
    # Transition point between top tip cap and concave side arc
    # Normal from (0, TIP_CENTER_OFFSET_SVG) to (ARC_CENTER_OFFSET_SVG, ARC_CENTER_OFFSET_SVG)
    vx = ARC_CENTER_OFFSET_SVG
    vy = ARC_CENTER_OFFSET_SVG - TIP_CENTER_OFFSET_SVG
    v_len = math.hypot(vx, vy)
    tx_top = (TIP_R_SVG * vx) / v_len  # ~0.4875
    tx_right = TIP_CENTER_OFFSET_SVG + (TIP_R_SVG * vy) / v_len  # ~10.618

    if dx_abs <= tx_top:
        # Top rounded tip cap: center (0, TIP_CENTER_OFFSET_SVG), radius TIP_R_SVG
        return TIP_CENTER_OFFSET_SVG + math.sqrt(max(0.0, TIP_R_SVG**2 - dx_abs**2))
    if dx_abs >= tx_right:
        # Right rounded tip cap: center (TIP_CENTER_OFFSET_SVG, 0), radius TIP_R_SVG
        rem = dx_abs - TIP_CENTER_OFFSET_SVG
        return math.sqrt(max(0.0, TIP_R_SVG**2 - rem**2))
    # Concave circular arc: center (ARC_CENTER_OFFSET_SVG, ARC_CENTER_OFFSET_SVG), radius R_ARC_SVG
    rem = ARC_CENTER_OFFSET_SVG - dx_abs
    return ARC_CENTER_OFFSET_SVG - math.sqrt(max(0.0, R_ARC_SVG**2 - rem**2))


def _star_half_height(x: float) -> float:
    """Return star half-height dy >= 0 in canvas units at canvas coordinate x."""
    dx_svg = abs(x - cx) / SCALE
    return _star_y_top_svg(dx_svg) * SCALE


def _linear_grad_alpha(
    sx: float,
    sy: float,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    max_t: float,
) -> float:
    """Compute SVG linearGradient alpha at SVG point (sx, sy)."""
    dx = x2 - x1
    dy = y2 - y1
    len_sq = dx * dx + dy * dy
    t = ((sx - x1) * dx + (sy - y1) * dy) / len_sq
    if t <= 0.0:
        return 1.0
    if t >= max_t:
        return 0.0
    return 1.0 - (t / max_t)


def _sample_gemini_hex(x: float, y: float) -> str:
    """Evaluate the 4-layer softened Gemini gradient at canvas point (x, y)."""
    sx = 12.0 + (x - cx) / SCALE
    sy = 12.0 - (y - cy) / SCALE

    r, g, b = BLUE_RGB

    # Layer 1: Bottom Green (7, 15.5) -> (11, 12), stop offset 1.0
    a_green = _linear_grad_alpha(sx, sy, 7.0, 15.5, 11.0, 12.0, 1.0)
    r = (1.0 - a_green) * r + a_green * GREEN_RGB[0]
    g = (1.0 - a_green) * g + a_green * GREEN_RGB[1]
    b = (1.0 - a_green) * b + a_green * GREEN_RGB[2]

    # Layer 2: Top Red (8, 5.5) -> (11.5, 11), stop offset 1.0
    a_red = _linear_grad_alpha(sx, sy, 8.0, 5.5, 11.5, 11.0, 1.0)
    r = (1.0 - a_red) * r + a_red * RED_RGB[0]
    g = (1.0 - a_red) * g + a_red * RED_RGB[1]
    b = (1.0 - a_red) * b + a_red * RED_RGB[2]

    # Layer 3: Left Yellow (3.5, 13.5) -> (17.5, 12), stop offset 0.46
    a_yellow = _linear_grad_alpha(sx, sy, 3.5, 13.5, 17.5, 12.0, 0.46)
    r = (1.0 - a_yellow) * r + a_yellow * YELLOW_RGB[0]
    g = (1.0 - a_yellow) * g + a_yellow * YELLOW_RGB[1]
    b = (1.0 - a_yellow) * b + a_yellow * YELLOW_RGB[2]

    ri = max(0, min(255, round(r)))
    gi = max(0, min(255, round(g)))
    bi = max(0, min(255, round(b)))
    return f"#{ri:02X}{gi:02X}{bi:02X}"


# 1. Render smooth gradient mesh clipped to the star interior
x_min = cx - CANVAS_HALF
x_max = cx + CANVAS_HALF
cols = 76
step = (x_max - x_min) / cols
overlap = 0.22

for i in range(cols):
    x0_base = x_min + i * step
    x1_base = x_min + (i + 1) * step
    x0 = x0_base if i == 0 else x0_base - overlap
    x1 = x1_base if i == cols - 1 else x1_base + overlap

    hh0 = _star_half_height(x0)
    hh1 = _star_half_height(x1)
    y_bot_min = cy - max(hh0, hh1)
    y_top_max = cy + max(hh0, hh1)

    col_height = y_top_max - y_bot_min
    if col_height <= 1e-4:
        continue
    rows = max(1, math.ceil(col_height / step))
    dy = col_height / rows

    for j in range(rows):
        y0_base = y_bot_min + j * dy
        y1_base = y_bot_min + (j + 1) * dy
        y0 = y0_base if j == 0 else y0_base - overlap
        y1 = y1_base if j == rows - 1 else y1_base + overlap

        # Clip left edge (x0) and right edge (x1) vertically to star contour
        l_bot = max(y0, cy - hh0)
        l_top = min(y1, cy + hh0)
        r_bot = max(y0, cy - hh1)
        r_top = min(y1, cy + hh1)

        if l_top <= l_bot and r_top <= r_bot:
            continue

        pts: list[tuple[float, float]] = []
        if l_top > l_bot:
            pts.append((x0, l_bot))
            pts.append((x0, l_top))
        else:
            pts.append((x0, 0.5 * (l_bot + l_top)))

        if r_top > r_bot:
            pts.append((x1, r_top))
            pts.append((x1, r_bot))
        else:
            pts.append((x1, 0.5 * (r_bot + r_top)))

        if len(pts) >= 3:
            mx = sum(p[0] for p in pts) / len(pts)
            my = sum(p[1] for p in pts) / len(pts)
            col_hex = _sample_gemini_hex(mx, my)
            polygon(pts, style=fill_style(col_hex))

# 2. Build smooth outer star contour using exact arc-angle sampling across all 4 quadrants
vx = ARC_CENTER_OFFSET_SVG
vy = ARC_CENTER_OFFSET_SVG - TIP_CENTER_OFFSET_SVG
ang_join = math.atan2(vy, vx)  # angle from top tip center to concave arc center (~20.1 deg)

quad_svg: list[tuple[float, float]] = []
# Top half-cap: from pi/2 down to ang_join
for k in range(8):
    ang = (math.pi / 2.0) - (math.pi / 2.0 - ang_join) * (k / 8)
    quad_svg.append((TIP_R_SVG * math.cos(ang), TIP_CENTER_OFFSET_SVG + TIP_R_SVG * math.sin(ang)))

# Concave circular arc: from (pi + ang_join) to (1.5*pi - ang_join)
ang_c_start = math.pi + ang_join
ang_c_end = 1.5 * math.pi - ang_join
for k in range(36):
    ang = ang_c_start + (ang_c_end - ang_c_start) * (k / 36)
    quad_svg.append(
        (
            ARC_CENTER_OFFSET_SVG + R_ARC_SVG * math.cos(ang),
            ARC_CENTER_OFFSET_SVG + R_ARC_SVG * math.sin(ang),
        )
    )

# Right half-cap: from (pi/2 - ang_join) down to 0
for k in range(9):
    ang = (math.pi / 2.0 - ang_join) * (1.0 - k / 8)
    quad_svg.append((TIP_CENTER_OFFSET_SVG + TIP_R_SVG * math.cos(ang), TIP_R_SVG * math.sin(ang)))

full_outer: list[tuple[float, float]] = []
for rot_deg in (0.0, 270.0, 180.0, 90.0):
    rad = math.radians(rot_deg)
    ca, sa = math.cos(rad), math.sin(rad)
    for sx_pt, sy_pt in quad_svg[:-1]:
        rx = sx_pt * ca - sy_pt * sa
        ry = sx_pt * sa + sy_pt * ca
        full_outer.append((cx + rx * SCALE, cy + ry * SCALE))

draw_round_polyline(full_outer, width_units=w, color=DARK, closed=True)

save()
