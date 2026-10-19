# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security icon: onelogin."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()

w_outer = 2.0
w_inner = 1.4
s = 40.0 / 40.98


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


one_mark = _sc([
    (56.12, 35.5), (56.11, 35.39), (56.1, 35.28), (56.09, 35.18), (56.07, 35.08),
    (56.04, 34.99), (56.01, 34.91), (55.97, 34.83), (55.92, 34.76), (55.87, 34.69),
    (55.82, 34.62), (55.75, 34.57), (55.68, 34.52), (55.61, 34.47), (55.53, 34.43),
    (55.45, 34.4), (55.36, 34.37), (55.26, 34.35), (55.16, 34.34), (55.05, 34.33),
    (54.94, 34.33), (47.57, 34.33), (47.45, 34.33), (47.35, 34.34), (47.24, 34.35),
    (47.15, 34.37), (47.06, 34.4), (46.97, 34.43), (46.89, 34.47), (46.82, 34.52),
    (46.75, 34.57), (46.69, 34.62), (46.63, 34.69), (46.58, 34.76), (46.54, 34.83),
    (46.5, 34.91), (46.46, 34.99), (46.44, 35.08), (46.42, 35.18), (46.4, 35.28),
    (46.39, 35.39), (46.39, 35.5), (46.39, 53.26), (40.75, 53.26), (40.64, 53.26),
    (40.53, 53.27), (40.43, 53.29), (40.33, 53.31), (40.24, 53.33), (40.16, 53.37),
    (40.08, 53.41), (40.01, 53.45), (39.94, 53.5), (39.87, 53.56), (39.82, 53.62),
    (39.77, 53.69), (39.72, 53.76), (39.68, 53.84), (39.65, 53.93), (39.62, 54.02),
    (39.6, 54.11), (39.59, 54.22), (39.58, 54.32), (39.58, 54.44), (39.58, 61.81),
    (39.58, 61.92), (39.59, 62.03), (39.6, 62.13), (39.62, 62.23), (39.65, 62.32),
    (39.68, 62.4), (39.72, 62.48), (39.77, 62.55), (39.82, 62.62), (39.87, 62.69),
    (39.94, 62.74), (40.01, 62.79), (40.08, 62.84), (40.16, 62.88), (40.24, 62.91),
    (40.33, 62.94), (40.43, 62.96), (40.53, 62.97), (40.64, 62.98), (40.75, 62.99),
    (55.12, 62.99), (55.23, 62.98), (55.33, 62.97), (55.43, 62.96), (55.52, 62.94),
    (55.6, 62.91), (55.67, 62.88), (55.73, 62.85), (55.79, 62.81), (55.84, 62.76),
    (55.89, 62.71), (55.93, 62.66), (55.96, 62.6), (55.99, 62.54), (56.02, 62.48),
    (56.04, 62.41), (56.05, 62.34), (56.06, 62.27), (56.07, 62.19), (56.08, 62.11),
    (56.08, 62.03), (56.08, 35.5),
])
# fmt: on

# 1. Dark slate/navy circular badge fill
circle((50.0, 50.0), radius=40.0, style=Icon.no_border_fill("#4B5668"))

# 2. White '1' mark + DARK 1.4 outline
polygon(one_mark, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(one_mark, width_units=w_inner, color=Icon.DARK, closed=True)

# 3. Outer circular DARK border
circle((50.0, 50.0), radius=40.0, style=Icon.stroke_style(Icon.DARK, width_units=w_outer))

save()
