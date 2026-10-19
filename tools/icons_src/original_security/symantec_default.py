# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: symantec."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()

w = 2.0
w_pixel = 0.85
s = 0.96


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


cx, cy = _sc([(47.02, 44.49)])[0]
r_outer = 35.49 * s
r_inner = 24.36 * s

# 1. Pastel amber circle ring + WHITE inner circle, both outlined in DARK 1.6
circle(
    (cx, cy),
    radius=r_outer,
    style=Icon.fill_style(Colors.Amber3, border_color=Icon.DARK, border_units=w),
)
circle(
    (cx, cy),
    radius=r_inner,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w),
)

# 2. DARK checkmark and DARK pixel accent squares
dark_squares: list[list[tuple[float, float]]] = [
    _sc([(72.72, 77.48), (75.4, 77.48), (75.4, 74.96), (72.72, 74.96)]),
    _sc([(80.45, 80.01), (83.42, 80.01), (83.42, 77.33), (80.45, 77.33)]),
    _sc([(70.2, 80.01), (72.72, 80.01), (72.72, 77.48), (70.2, 77.48)]),
    _sc([(77.77, 77.48), (80.3, 77.48), (80.3, 74.96), (77.77, 74.96)]),
    _sc([(82.82, 88.32), (85.48, 88.32), (85.48, 85.66), (82.81, 85.66)]),
    _sc([(77.77, 85.49), (82.82, 85.49), (82.82, 82.67), (77.77, 82.67)]),
    _sc([(75.4, 82.83), (77.92, 82.83), (77.92, 77.48), (75.4, 77.48)]),
]
for sq in dark_squares:
    polygon(sq, style=Icon.no_border_fill(Icon.DARK))
    Icon.draw_round_polyline(sq, width_units=w_pixel, color=Icon.DARK, closed=True)

checkmark_pts = _sc([
    (75.4, 74.96), (75.4, 72.28), (72.72, 72.28), (72.72, 74.96),
    (68.42, 74.96), (68.42, 73.02), (66.03, 73.02), (66.03, 70.65),
    (63.37, 70.65), (63.37, 66.64), (60.69, 66.64), (60.69, 64.12),
    (58.9, 64.12), (58.9, 61.44), (56.96, 61.44), (56.63, 60.92),
    (56.25, 60.31), (55.84, 59.62), (55.37, 58.85), (54.9, 58.02),
    (54.4, 57.14), (53.88, 56.2), (53.35, 55.24), (52.81, 54.24),
    (52.26, 53.23), (51.72, 52.22), (51.2, 51.2), (50.69, 50.2),
    (50.19, 49.23), (49.71, 48.28), (49.28, 47.37), (48.87, 46.52),
    (48.49, 45.72), (48.17, 45.0), (47.91, 44.36), (47.05, 45.54),
    (46.2, 46.66), (45.38, 47.71), (44.57, 48.68), (43.78, 49.59),
    (43.01, 50.44), (42.25, 51.22), (41.51, 51.93), (40.79, 52.6),
    (40.09, 53.22), (39.4, 53.78), (38.73, 54.28), (38.07, 54.74),
    (37.44, 55.16), (36.81, 55.53), (36.21, 55.87), (35.62, 56.16),
    (35.04, 56.42), (34.48, 56.65), (33.94, 56.84), (33.64, 56.91),
    (33.35, 56.93), (33.06, 56.93), (32.77, 56.88), (32.5, 56.8),
    (32.25, 56.69), (32.0, 56.55), (31.8, 56.37), (31.62, 56.15),
    (31.47, 55.91), (31.36, 55.64), (31.3, 55.34), (31.27, 55.02),
    (31.31, 54.66), (31.42, 54.29), (31.57, 53.89), (31.79, 53.47),
    (32.08, 53.04), (32.45, 52.58), (32.9, 52.1), (33.95, 50.9),
    (34.94, 49.73), (35.86, 48.58), (36.71, 47.45), (37.51, 46.34),
    (38.26, 45.23), (38.94, 44.17), (39.58, 43.11), (40.18, 42.08),
    (40.73, 41.07), (41.24, 40.07), (41.73, 39.1), (42.18, 38.15),
    (42.6, 37.21), (43.01, 36.3), (43.38, 35.41), (43.75, 34.54),
    (44.1, 33.69), (44.45, 32.86), (44.78, 32.04), (44.98, 31.64),
    (45.25, 31.27), (45.56, 30.93), (45.91, 30.64), (46.3, 30.38),
    (46.71, 30.17), (47.16, 29.99), (47.62, 29.86), (48.08, 29.76),
    (48.57, 29.7), (49.05, 29.69), (49.52, 29.72), (49.98, 29.79),
    (50.42, 29.91), (50.84, 30.08), (51.22, 30.29), (51.58, 30.54),
    (51.89, 30.85), (52.15, 31.19), (52.35, 31.6), (52.7, 32.51),
    (53.06, 33.45), (53.43, 34.38), (53.81, 35.32), (54.22, 36.27),
    (54.63, 37.23), (55.07, 38.17), (55.5, 39.12), (55.96, 40.08),
    (56.43, 41.03), (56.91, 41.98), (57.4, 42.91), (57.9, 43.84),
    (58.41, 44.76), (58.94, 45.68), (59.47, 46.58), (60.03, 47.46),
    (60.58, 48.33), (61.14, 49.18), (61.72, 50.01), (61.72, 52.84),
    (63.79, 52.84), (63.79, 55.51), (66.02, 55.51), (66.02, 58.48),
    (68.55, 58.48), (68.55, 61.45), (71.07, 61.45), (71.07, 64.13),
    (73.3, 64.13), (73.3, 67.23), (75.68, 67.23), (75.68, 69.31),
    (77.76, 69.31), (77.76, 74.82), (75.38, 74.82),
])
polygon(checkmark_pts, style=Icon.no_border_fill(Icon.DARK))
Icon.draw_round_polyline(checkmark_pts, width_units=w_pixel, color=Icon.DARK, closed=True)
# Smooth 1.6 outline along the lower curved V-body of the checkmark
Icon.draw_round_polyline(checkmark_pts[14:113], width_units=w, color=Icon.DARK)

# 3. All amber pixel accent squares (outer and inner) drawn on top
amber_squares: list[list[tuple[float, float]]] = [
    _sc([(85.65, 85.49), (88.47, 85.49), (88.47, 82.67), (85.65, 82.67)]),
    _sc([(85.65, 91.0), (88.47, 91.0), (88.47, 88.18), (85.65, 88.18)]),
    _sc([(77.77, 82.83), (80.3, 82.83), (80.3, 80.16), (77.77, 80.16)]),
    _sc([(66.03, 70.65), (68.56, 70.65), (68.56, 68.13), (66.03, 68.13)]),
    _sc([(65.87, 61.45), (68.55, 61.45), (68.55, 64.13), (65.87, 64.13)]),
]
for sq in amber_squares:
    polygon(sq, style=Icon.no_border_fill(Colors.Amber3))
    Icon.draw_round_polyline(sq, width_units=w_pixel, color=Icon.DARK, closed=True)
# fmt: on

save()
