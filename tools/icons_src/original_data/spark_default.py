# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: spark."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_compound_polygon,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    setup_icon,
)


def _round_polygon_radii(
    vertices: list[tuple[float, float]],
    radii: tuple[float, ...],
    steps: int = 12,
) -> list[tuple[float, float]]:
    """Sample rounded-corner polygon matching Drawlib per-vertex shape_r."""
    n = len(vertices)
    pts: list[tuple[float, float]] = []
    for i in range(n):
        v_prev = vertices[(i - 1) % n]
        v_curr = vertices[i]
        v_next = vertices[(i + 1) % n]
        r_curr = radii[i]
        r_prev = radii[(i - 1) % n]
        r_next = radii[(i + 1) % n]

        dx_in = v_prev[0] - v_curr[0]
        dy_in = v_prev[1] - v_curr[1]
        d_in = math.hypot(dx_in, dy_in)

        dx_out = v_next[0] - v_curr[0]
        dy_out = v_next[1] - v_curr[1]
        d_out = math.hypot(dx_out, dy_out)

        if r_curr <= 0.0 or d_in == 0.0 or d_out == 0.0:
            pts.append(v_curr)
            continue

        avail_in = d_in * (r_curr / (r_prev + r_curr)) if (r_prev + r_curr) > d_in else r_curr
        avail_out = d_out * (r_curr / (r_curr + r_next)) if (r_curr + r_next) > d_out else r_curr
        r_eff = min(r_curr, avail_in, avail_out)
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

w = 2.0

# Outer 5-pointed tilted star vertices (tips P0..P4, valleys V0..V4)
outer_pts = [
    (45.5, 88.7),  # P0: top tip
    (59.0, 69.7),  # V0: top-right valley
    (87.7, 72.6),  # P1: right-top tip
    (69.5, 51.9),  # V1: right valley
    (79.1, 29.3),  # P2: right-bottom tip
    (54.8, 31.7),  # V2: bottom valley
    (33.1, 11.6),  # P3: bottom-left tip
    (31.8, 38.5),  # V3: left-bottom valley
    (11.6, 50.9),  # P4: left tip
    (35.2, 63.2),  # V4: top-left valley
]

# Inner 5-pointed tilted star cutout vertices (tips p0..p4, valleys v0..v4)
inner_pts = [
    (45.9, 76.8),  # p0: top inner tip
    (55.4, 61.8),  # v0: top-right inner valley
    (75.8, 66.4),  # p1: right-top inner tip
    (62.5, 51.1),  # v1: right inner valley
    (71.0, 35.4),  # p2: right-bottom inner tip
    (53.7, 40.0),  # v2: bottom inner valley
    (37.4, 22.5),  # p3: bottom-left inner tip
    (40.4, 45.5),  # v3: left-bottom inner valley
    (25.3, 51.4),  # p4: left inner tip
    (44.5, 57.4),  # v4: top-left inner valley
]

outer_radii = (4.2, 1.0, 4.2, 1.0, 4.2, 1.0, 4.2, 1.0, 4.2, 1.0)
outer_poly = _round_polygon_radii(outer_pts, outer_radii)

# 1. Base tilted star with transparent hollow star center (Colors.Orange3)
draw_compound_polygon([outer_poly, inner_pts], color=Colors.Orange3)

# 2. Dynamic top-right burst ray accented in Colors.Amber3
burst_ray = [
    outer_pts[1],  # V0
    outer_pts[2],  # P1
    outer_pts[3],  # V1
    inner_pts[3],  # v1
    inner_pts[2],  # p1
    inner_pts[1],  # v0
]
polygon(
    burst_ray,
    style=fill_style(Colors.Amber3, shape_r=(0.0, 4.2, 0.0, 0.0, 0.0, 0.0)),
)

# 3. Crisp seam lines and inner/outer structural outlines
draw_round_segment(inner_pts[1], outer_pts[1], width_units=1.7, color=DARK)
draw_round_segment(inner_pts[3], outer_pts[3], width_units=1.7, color=DARK)
draw_round_polyline(inner_pts, width_units=1.8, color=DARK, closed=True)
draw_round_polyline(outer_poly, width_units=w, color=DARK, closed=True)

save()
