# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: rabbitmq."""

import math

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_compound_polygon,
    draw_round_polyline,
    fill_style,
    setup_icon,
)


def _round_polygon(
    vertices: list[tuple[float, float]],
    r: float,
    steps: int = 12,
) -> list[tuple[float, float]]:
    """Sample rounded-corner polygon matching Drawlib shape_r quadratic Bezier corners."""
    n = len(vertices)
    pts: list[tuple[float, float]] = []
    for i in range(n):
        v_prev = vertices[(i - 1) % n]
        v_curr = vertices[i]
        v_next = vertices[(i + 1) % n]

        dx_in = v_prev[0] - v_curr[0]
        dy_in = v_prev[1] - v_curr[1]
        d_in = math.hypot(dx_in, dy_in)

        dx_out = v_next[0] - v_curr[0]
        dy_out = v_next[1] - v_curr[1]
        d_out = math.hypot(dx_out, dy_out)

        r_eff = min(r, d_in / 2.0, d_out / 2.0)
        p_in = (v_curr[0] + (dx_in / d_in) * r_eff, v_curr[1] + (dy_in / d_in) * r_eff)
        p_out = (v_curr[0] + (dx_out / d_out) * r_eff, v_curr[1] + (dy_out / d_out) * r_eff)

        for s in range(steps + 1):
            t = s / steps
            mt = 1.0 - t
            bx = (mt**2) * p_in[0] + 2.0 * mt * t * v_curr[0] + (t**2) * p_out[0]
            by = (mt**2) * p_in[1] + 2.0 * mt * t * v_curr[1] + (t**2) * p_out[1]
            pts.append((bx, by))
    return pts


setup_icon()

w = 1.9

# 5x5 modular grid mapped to [12.0, 88.0] x [12.0, 88.0] (1 block = 15.2 units)
x0, x1, x2, x3, x4, x5 = 12.0, 27.2, 42.4, 57.6, 72.8, 88.0
y0, y1, y2, y3, y5 = 12.0, 27.2, 42.4, 57.6, 88.0

# 1. Main geometric rabbit block silhouette with open rounded-square eye hole (Colors.Orange3)
rabbit_pts = [
    (x0, y0),
    (x5, y0),
    (x5, y3),
    (x3, y3),
    (x3, y5),
    (x2, y5),
    (x2, y3),
    (x1, y3),
    (x1, y5),
    (x0, y5),
]
rabbit_poly = _round_polygon(rabbit_pts, r=3.6)

eye_cx = (x3 + x4) / 2.0
eye_cy = (y1 + y2) / 2.0
eye_half = 8.0
eye_pts = [
    (eye_cx - eye_half, eye_cy - eye_half),
    (eye_cx + eye_half, eye_cy - eye_half),
    (eye_cx + eye_half, eye_cy + eye_half),
    (eye_cx - eye_half, eye_cy + eye_half),
]
eye_hole_poly = _round_polygon(eye_pts, r=4.2)

draw_compound_polygon([rabbit_poly, eye_hole_poly], color=Colors.Orange3)
draw_round_polyline(rabbit_poly, width_units=w, color=DARK, closed=True)
draw_round_polyline(eye_hole_poly, width_units=1.8, color=DARK, closed=True)

# 2. Inner pastel ear accents (Colors.Orange2) inside both upright ears
for ear_cx in ((x0 + x1) / 2.0, (x2 + x3) / 2.0):
    rectangle(
        (ear_cx, 72.5),
        width=6.8,
        height=18.5,
        style=fill_style(Colors.Orange2, border_color=DARK, border_units=1.5, shape_r=3.0),
    )

save()
