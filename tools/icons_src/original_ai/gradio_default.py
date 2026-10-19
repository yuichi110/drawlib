# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: gradio."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

Icon.setup()

w = 2.0

# Isometric diamond loop geometry (scaled to fit [10.7, 89.3])
cx = 50.0
cy_bot = 40.51
cy_top = 59.49

slope = 0.57315
ang_slope = math.atan(slope)
ang_deg = math.degrees(ang_slope)

dx_in = 23.87
dy_in = dx_in * slope  # 13.68

dy_out_sharp = 25.07
dx_out_sharp = dy_out_sharp / slope  # 43.74

r_lr = 4.4
r_tb = 3.2

# Softened Drawlib-toned stops matching official Gradio SVG (#F9D100 -> #F97700)
YELLOW_RGB = (248.0, 206.0, 62.0)
ORANGE_RGB = (242.0, 134.0, 48.0)


def _sample_gradio_hex(x: float, *, top_loop: bool) -> str:
    """Evaluate horizontal Gradio gradient at canvas coordinate x."""
    sx = 12.0 + (x - 50.0) * (23.92 / 78.52)
    t = (23.74 - sx) / (23.74 - 4.519) if top_loop else (sx - 0.182) / (19.377 - 0.182)
    t = max(0.0, min(1.0, t))
    r = (1.0 - t) * YELLOW_RGB[0] + t * ORANGE_RGB[0]
    g = (1.0 - t) * YELLOW_RGB[1] + t * ORANGE_RGB[1]
    b = (1.0 - t) * YELLOW_RGB[2] + t * ORANGE_RGB[2]
    return f"#{round(r):02X}{round(g):02X}{round(b):02X}"


def _clip_x_band(
    pts: list[tuple[float, float]],
    x0: float,
    x1: float,
) -> list[tuple[float, float]]:
    """Clip polygon to vertical slab x0 <= x <= x1 via Sutherland-Hodgman."""

    def _clip_edge(poly: list[tuple[float, float]], x_thresh: float, *, keep_ge: bool) -> list[tuple[float, float]]:
        if not poly:
            return []
        out: list[tuple[float, float]] = []
        n = len(poly)
        for i in range(n):
            p1 = poly[i]
            p2 = poly[(i + 1) % n]
            v1 = p1[0] - x_thresh
            v2 = p2[0] - x_thresh
            in1 = v1 >= 0.0 if keep_ge else v1 <= 0.0
            in2 = v2 >= 0.0 if keep_ge else v2 <= 0.0
            if in1 and in2:
                out.append(p2)
            elif in1 and not in2:
                u = v1 / (v1 - v2)
                out.append((x_thresh, p1[1] + u * (p2[1] - p1[1])))
            elif not in1 and in2:
                u = v1 / (v1 - v2)
                out.append((x_thresh, p1[1] + u * (p2[1] - p1[1])))
                out.append(p2)
        return out

    return _clip_edge(_clip_edge(pts, x0, keep_ge=True), x1, keep_ge=False)


def _build_diamond_loop(
    cy: float,
) -> tuple[
    list[tuple[float, float]],
    list[tuple[float, float]],
    list[tuple[float, float]],
    list[tuple[float, float]],
]:
    """Build outer contour, inner hole, upper half-ring, and lower half-ring centered at (cx, cy)."""
    d_lr = r_lr / math.sin(ang_slope)
    d_tb = r_tb / math.cos(ang_slope)

    cx_right = cx + dx_out_sharp - d_lr
    cx_left = cx - dx_out_sharp + d_lr
    cy_top_arc = cy + dy_out_sharp - d_tb
    cy_bot_arc = cy - dy_out_sharp + d_tb

    steps = 16
    right_arc: list[tuple[float, float]] = []
    a0, a1 = -90.0 + ang_deg, 90.0 - ang_deg
    for i in range(steps + 1):
        a = math.radians(a0 + (a1 - a0) * (i / steps))
        right_arc.append((cx_right + r_lr * math.cos(a), cy + r_lr * math.sin(a)))

    top_arc: list[tuple[float, float]] = []
    a0, a1 = 90.0 - ang_deg, 90.0 + ang_deg
    for i in range(steps + 1):
        a = math.radians(a0 + (a1 - a0) * (i / steps))
        top_arc.append((cx + r_tb * math.cos(a), cy_top_arc + r_tb * math.sin(a)))

    left_arc: list[tuple[float, float]] = []
    a0, a1 = 90.0 + ang_deg, 270.0 - ang_deg
    for i in range(steps + 1):
        a = math.radians(a0 + (a1 - a0) * (i / steps))
        left_arc.append((cx_left + r_lr * math.cos(a), cy + r_lr * math.sin(a)))

    bot_arc: list[tuple[float, float]] = []
    a0, a1 = 270.0 - ang_deg, 270.0 + ang_deg
    for i in range(steps + 1):
        a = math.radians(a0 + (a1 - a0) * (i / steps))
        bot_arc.append((cx + r_tb * math.cos(a), cy_bot_arc + r_tb * math.sin(a)))

    outer = [*right_arc, *top_arc, *left_arc, *bot_arc]
    inner = [
        (cx + dx_in, cy),
        (cx, cy + dy_in),
        (cx - dx_in, cy),
        (cx, cy - dy_in),
    ]

    mid = steps // 2  # index 8 is exactly y == cy on right_arc and left_arc
    upper_half = [
        *right_arc[mid:],
        *top_arc,
        *left_arc[: mid + 1],
        (cx - dx_in, cy),
        (cx, cy + dy_in),
        (cx + dx_in, cy),
    ]
    lower_half = [
        *left_arc[mid:],
        *bot_arc,
        *right_arc[: mid + 1],
        (cx + dx_in, cy),
        (cx, cy - dy_in),
        (cx - dx_in, cy),
    ]
    return outer, inner, upper_half, lower_half


def _draw_gradient_ring(
    outer: list[tuple[float, float]],
    upper_half: list[tuple[float, float]],
    lower_half: list[tuple[float, float]],
    *,
    top_loop: bool,
) -> None:
    """Fill a diamond loop with smooth vertical gradient strips without corner seams."""
    x_left_in = cx - dx_in
    x_right_in = cx + dx_in
    overlap = 0.22

    # Three exact horizontal zones so strips never straddle x_left_in or x_right_in
    zones = [
        (10.5, x_left_in, 16, True),
        (x_left_in, x_right_in, 46, False),
        (x_right_in, 89.5, 16, True),
    ]
    for z_min, z_max, z_cols, is_solid in zones:
        step = (z_max - z_min) / z_cols
        for i in range(z_cols):
            x0_base = z_min + i * step
            x1_base = z_min + (i + 1) * step
            x0 = x0_base - overlap
            x1 = x1_base + overlap
            col_hex = _sample_gradio_hex(0.5 * (x0_base + x1_base), top_loop=top_loop)
            st = Icon.fill_style(col_hex)

            if is_solid:
                s_poly = _clip_x_band(outer, x0, x1)
                if len(s_poly) >= 3:
                    polygon(s_poly, style=st)
            else:
                u_poly = _clip_x_band(upper_half, x0, x1)
                if len(u_poly) >= 3:
                    polygon(u_poly, style=st)
                l_poly = _clip_x_band(lower_half, x0, x1)
                if len(l_poly) >= 3:
                    polygon(l_poly, style=st)


bot_outer, bot_inner, bot_upper, bot_lower = _build_diamond_loop(cy_bot)
top_outer, top_inner, top_upper, top_lower = _build_diamond_loop(cy_top)

# 1. Bottom loop: smooth horizontal gradient (Yellow left -> Orange right)
_draw_gradient_ring(bot_outer, bot_upper, bot_lower, top_loop=False)
Icon.draw_round_polyline(bot_outer, width_units=w, color=Icon.DARK, closed=True)
Icon.draw_round_polyline(bot_inner, width_units=w, color=Icon.DARK, closed=True)

# 3. Top loop: smooth horizontal gradient (Orange left -> Yellow right)
_draw_gradient_ring(top_outer, top_upper, top_lower, top_loop=True)
Icon.draw_round_polyline(top_outer, width_units=w, color=Icon.DARK, closed=True)
Icon.draw_round_polyline(top_inner, width_units=w, color=Icon.DARK, closed=True)

# 4. Left crossover patch: Bottom loop's upper-left arm goes OVER Top loop's lower-left arm
x0_out, x1_out = 21.0, 36.0
x0_in, x1_in = cx - dx_in, 44.5

y0_out = (cy_bot + dy_out_sharp) + slope * (x0_out - cx)
y1_out = (cy_bot + dy_out_sharp) + slope * (x1_out - cx)
y0_in = cy_bot
y1_in = (cy_bot + dy_in) + slope * (x1_in - cx)

left_over_patch = [(x0_out, y0_out), (x1_out, y1_out), (x1_in, y1_in), (x0_in, y0_in)]

patch_cols = 28
p_min = min(x0_out, x0_in)
p_max = max(x1_out, x1_in)
p_step = (p_max - p_min) / patch_cols
p_overlap = 0.22
for i in range(patch_cols):
    px0_base = p_min + i * p_step
    px1_base = p_min + (i + 1) * p_step
    px0 = px0_base if i == 0 else px0_base - p_overlap
    px1 = px1_base if i == patch_cols - 1 else px1_base + p_overlap
    p_poly = _clip_x_band(left_over_patch, px0, px1)
    if len(p_poly) >= 3:
        col_hex = _sample_gradio_hex(0.5 * (px0_base + px1_base), top_loop=False)
        polygon(p_poly, style=Icon.fill_style(col_hex))

Icon.draw_round_segment((x0_out, y0_out), (x1_out, y1_out), width_units=w, color=Icon.DARK)
Icon.draw_round_segment((x0_in, y0_in), (x1_in, y1_in), width_units=w, color=Icon.DARK)

save()
