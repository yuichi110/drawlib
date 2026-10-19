# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code icon: tokio."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

Icon.setup()

SLATE = "#3E4756"
w_outline = 2.0
s = 40.0 / 41.0


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


cx0, cy0 = 50.0, 49.85
r_outer = 13.67
r_inner = 10.77
half_bar_w = 1.365
r_dot = 2.05
r_dot_ring = 28.70
half_root_deg = math.degrees(math.asin(half_bar_w / r_outer))

hub_outer: list[tuple[float, float]] = []
for k in range(12):
    ang_deg = k * 30.0
    ang_rad = math.radians(ang_deg)
    ux, uy = math.cos(ang_rad), math.sin(ang_rad)
    nx, ny = -uy, ux

    prev_left_deg = (k - 1) * 30.0 + half_root_deg
    curr_right_deg = ang_deg - half_root_deg
    arc_steps = 8
    for i in range(arc_steps + 1):
        t_deg = prev_left_deg + (curr_right_deg - prev_left_deg) * (i / arc_steps)
        t_rad = math.radians(t_deg)
        hub_outer.append((cx0 + r_outer * math.cos(t_rad), cy0 + r_outer * math.sin(t_rad)))

    r_tip = 41.0 if k % 2 == 0 else 23.92
    hub_outer.append((cx0 + r_tip * ux - half_bar_w * nx, cy0 + r_tip * uy - half_bar_w * ny))
    hub_outer.append((cx0 + r_tip * ux + half_bar_w * nx, cy0 + r_tip * uy + half_bar_w * ny))

hub_inner: list[tuple[float, float]] = []
for i in range(64):
    t_rad = math.radians(360.0 * (i / 64.0))
    hub_inner.append((cx0 + r_inner * math.cos(t_rad), cy0 + r_inner * math.sin(t_rad)))

dot_centers = [(cx0, cy0)]
for k in range(1, 12, 2):
    ang_rad = math.radians(k * 30.0)
    dot_centers.append((cx0 + r_dot_ring * math.cos(ang_rad), cy0 + r_dot_ring * math.sin(ang_rad)))

dot_polys: list[list[tuple[float, float]]] = []
for dx, dy in dot_centers:
    pts: list[tuple[float, float]] = []
    for i in range(36):
        t_rad = math.radians(360.0 * (i / 36.0))
        pts.append((dx + r_dot * math.cos(t_rad), dy + r_dot * math.sin(t_rad)))
    dot_polys.append(_sc(pts))

hub_outer_sc = _sc(hub_outer)
hub_inner_sc = _sc(hub_inner)

polygon(hub_outer_sc, holes=[hub_inner_sc], style=Icon.fill_style(SLATE))
for d_pts in dot_polys:
    polygon(d_pts, style=Icon.no_border_fill(SLATE))

Icon.draw_round_polyline(hub_outer_sc, width_units=w_outline, color=Icon.DARK, closed=True)
Icon.draw_round_polyline(hub_inner_sc, width_units=w_outline, color=Icon.DARK, closed=True)
for d_pts in dot_polys:
    Icon.draw_round_polyline(d_pts, width_units=w_outline, color=Icon.DARK, closed=True)

save()
