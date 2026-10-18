# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: sqlite."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    WHITE,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 2.0


def _bezier(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    steps: int = 20,
) -> list[tuple[float, float]]:
    """Sample cubic Bezier curve excluding p0."""
    pts: list[tuple[float, float]] = []
    for i in range(1, steps + 1):
        t = i / steps
        mt = 1.0 - t
        x = (mt**3) * p0[0] + 3 * (mt**2) * t * p1[0] + 3 * mt * (t**2) * p2[0] + (t**3) * p3[0]
        y = (mt**3) * p0[1] + 3 * (mt**2) * t * p1[1] + 3 * mt * (t**2) * p2[1] + (t**3) * p3[1]
        pts.append((x, y))
    return pts


def _build_tile_bottom_wave(x0: float, y0: float, x1: float, r: float) -> list[tuple[float, float]]:
    """Build lower rounded-bottom wave area inside the square tile."""
    pts: list[tuple[float, float]] = [(x0, 29.0)]
    pts += _bezier((x0, 29.0), (28.0, 35.5), (48.0, 39.5), (x1, 39.0), 18)
    for i in range(9):
        ang = math.radians(0.0 - 90.0 * (i / 8))
        pts.append((x1 - r + r * math.cos(ang), y0 + r + r * math.sin(ang)))
    for i in range(9):
        ang = math.radians(270.0 - 90.0 * (i / 8))
        pts.append((x0 + r + r * math.cos(ang), y0 + r + r * math.sin(ang)))
    return pts


# 1. Rounded square tile background (Colors.Blue4 upper-left + Colors.Blue3 lower-right wave)
tile_cx, tile_cy = 41.0, 50.0
tile_w, tile_h = 58.0, 68.0
tile_r = 9.0
x0, y0 = tile_cx - tile_w / 2.0, tile_cy - tile_h / 2.0
x1, y1 = tile_cx + tile_w / 2.0, tile_cy + tile_h / 2.0

rectangle(
    (tile_cx, tile_cy),
    width=tile_w,
    height=tile_h,
    style=fill_style(Colors.Blue4, shape_r=tile_r),
)
polygon(_build_tile_bottom_wave(x0, y0, x1, tile_r), style=no_border_fill(Colors.Blue3))
draw_round_polyline(
    [(x0, 29.0), *_bezier((x0, 29.0), (28.0, 35.5), (48.0, 39.5), (x1, 39.0), 18)],
    width_units=1.6,
    color=DARK,
)
rectangle(
    (tile_cx, tile_cy),
    width=tile_w,
    height=tile_h,
    style=fill_style((0, 0, 0, 0), border_color=DARK, border_units=w, shape_r=tile_r),
)

# 2. Diagonal quill feather silhouette (Colors.Teal3) with iconic barbs
p_quill_tip = (59.5, 11.5)
p_vane_bot_l = (57.2, 31.0)
p_notch1_out = (53.2, 41.5)
p_notch1_in = (56.8, 39.5)
p_notch2_out = (54.5, 49.0)
p_notch2_in = (58.0, 47.0)
p_top_l = (71.5, 81.5)
p_plume_top = (84.8, 88.5)
p_top_r = (87.8, 72.5)
p_notch_r_out = (79.5, 51.5)
p_notch_r_in = (72.5, 48.0)
p_notch_r_low = (77.5, 49.5)
p_vane_bot_r = (63.5, 31.5)

feather_pts: list[tuple[float, float]] = [
    p_quill_tip,
    *_bezier(p_quill_tip, (57.5, 18.0), (57.0, 24.5), p_vane_bot_l, 12),
    *_bezier(p_vane_bot_l, (55.5, 35.0), (54.0, 38.5), p_notch1_out, 8),
    p_notch1_in,
    *_bezier(p_notch1_in, (55.5, 43.0), (54.8, 46.0), p_notch2_out, 8),
    p_notch2_in,
    *_bezier(p_notch2_in, (60.5, 61.0), (65.5, 73.5), p_top_l, 16),
    *_bezier(p_top_l, (75.5, 87.2), (81.0, 90.0), p_plume_top, 12),
    *_bezier(p_plume_top, (88.5, 86.5), (89.5, 80.0), p_top_r, 12),
    *_bezier(p_top_r, (86.2, 65.0), (83.2, 57.5), p_notch_r_out, 12),
    p_notch_r_in,
    p_notch_r_low,
    *_bezier(p_notch_r_low, (73.5, 42.5), (68.5, 36.0), p_vane_bot_r, 12),
    *_bezier(p_vane_bot_r, (61.5, 24.5), (60.2, 18.0), p_quill_tip, 12),
]

polygon(feather_pts, style=no_border_fill(Colors.Teal3))
draw_round_polyline(feather_pts, width_units=w, color=DARK, closed=True)

# 3. Tapered central feather shaft (WHITE with clear DARK border)
shaft_l = [(58.8, 26.0), *_bezier((58.8, 26.0), (61.5, 46.5), (69.5, 68.5), (81.2, 82.0), 18)]
shaft_r = [(81.2, 82.0), *_bezier((81.2, 82.0), (73.5, 66.0), (66.0, 44.5), (62.2, 26.0), 18)]
shaft_pts = [*shaft_l, *shaft_r]
polygon(shaft_pts, style=no_border_fill(WHITE))
draw_round_polyline(shaft_pts, width_units=1.5, color=DARK, closed=True)

save()
