# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server vendor icon: kvm (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse, polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
)

# ruff: noqa: E501
# fmt: off
setup_icon()

w_letter = 2.0
w_tux = 1.5
w_detail = 1.2
tux_slate = "#607085"

# 1. Right-side KVM vector letters in Colors.Gray6
letter_k: list[tuple[float, float]] = [(29.11, 41.84), (33.31, 41.84), (33.31, 48.1), (36.71, 51.94), (42.42, 41.84), (47.49, 41.84), (39.78, 55.65), (45.84, 62.94), (40.77, 62.94), (33.31, 53.79), (33.31, 62.94), (29.11, 62.94)]
letter_v: list[tuple[float, float]] = [(55.56, 41.84), (59.72, 41.84), (67.14, 62.94), (62.57, 62.94), (57.72, 47.5), (52.76, 62.94), (48.1, 62.94)]
letter_m: list[tuple[float, float]] = [(71.22, 41.84), (75.3, 41.84), (75.3, 54.04), (81.07, 41.4), (86.8, 54.04), (86.8, 41.84), (91.0, 41.84), (91.0, 62.94), (86.84, 62.94), (81.07, 50.15), (75.3, 62.94), (71.22, 62.94)]

for pts in (letter_k, letter_v, letter_m):
    polygon(pts, style=no_border_fill(Colors.Gray6))
    draw_round_polyline(pts, width_units=w_letter, color=DARK, closed=True)

# 2. Cute flat pastel sitting Tux on left
tux_body: list[tuple[float, float]] = [(16.15, 49.95), (16.65, 50.65), (17.45, 51.08), (18.45, 51.22), (19.55, 51.12), (20.55, 50.78), (21.35, 50.15), (21.95, 49.25), (22.28, 48.1), (22.5, 45.8), (23.26, 43.98), (24.62, 44.93), (25.81, 46.87), (26.64, 47.69), (26.97, 49.71), (27.46, 49.71), (27.95, 49.1), (28.41, 47.61), (28.16, 45.71), (27.34, 44.44), (24.58, 42.09), (25.98, 39.33), (26.27, 38.05), (26.18, 37.06), (13.08, 37.06), (13.12, 38.34), (11.88, 38.01), (10.9, 38.12), (9.75, 38.72), (9.08, 39.45), (9.21, 40.35), (10.48, 41.59), (12.54, 42.79), (14.4, 43.49), (15.72, 43.7), (16.02, 44.48), (15.9, 48.2), (15.98, 49.2)]
tux_belly: list[tuple[float, float]] = [(16.85, 43.65), (18.25, 43.1), (20.15, 43.95), (21.15, 42.65), (22.15, 40.05), (22.45, 38.5), (22.45, 37.06), (14.55, 37.06), (14.55, 39.45), (15.55, 40.95), (16.25, 42.65)]
tux_beak: list[tuple[float, float]] = [(16.55, 45.35), (17.25, 46.05), (18.35, 46.35), (19.65, 46.05), (20.55, 45.35), (20.35, 44.75), (19.55, 44.15), (18.45, 43.85), (17.35, 44.15), (16.7, 44.75)]

polygon(tux_body, style=no_border_fill(tux_slate))
draw_round_polyline(tux_body, width_units=w_tux, color=DARK, closed=True)

polygon(tux_belly, style=no_border_fill(WHITE))
draw_round_polyline(tux_belly, width_units=w_detail, color=DARK, closed=True)

# Cute flat Amber2 webbed feet at sitting base
ellipse((14.0, 36.9), width=3.8, height=2.2, style=fill_style(Colors.Amber3, border_color=DARK, border_units=w_detail, angle=8.0))
ellipse((23.1, 36.9), width=3.8, height=2.2, style=fill_style(Colors.Amber3, border_color=DARK, border_units=w_detail, angle=-8.0))

# Bright white eyes & crisp pupils
ellipse((17.35, 47.65), width=2.25, height=2.95, style=fill_style(WHITE, border_color=DARK, border_units=0.85, angle=5.0))
ellipse((19.65, 47.65), width=2.25, height=2.95, style=fill_style(WHITE, border_color=DARK, border_units=0.85, angle=-5.0))
circle((17.55, 47.7), radius=0.48, style=fill_style(DARK))
circle((19.45, 47.7), radius=0.48, style=fill_style(DARK))

# Amber2 beak
polygon(tux_beak, style=no_border_fill(Colors.Amber3))
draw_round_polyline(tux_beak, width_units=1.05, color=DARK, closed=True)

# 3. Three flat pastel juggling circles with WHITE vector K, V, M inside
r_ball = 2.95

# Circle K (Colors.Red3)
cx_k, cy_k = 11.9, 49.0
circle((cx_k, cy_k), radius=r_ball, style=fill_style(Colors.Red3, border_color=DARK, border_units=w_tux))
draw_round_segment((cx_k - 0.9, cy_k - 1.25), (cx_k - 0.9, cy_k + 1.25), width_units=0.82, color=WHITE)
draw_round_segment((cx_k - 0.9, cy_k), (cx_k + 0.9, cy_k + 1.25), width_units=0.82, color=WHITE)
draw_round_segment((cx_k - 0.3, cy_k + 0.35), (cx_k + 0.9, cy_k - 1.25), width_units=0.82, color=WHITE)

# Circle V (Colors.Blue3)
cx_v, cy_v = 15.8, 61.2
circle((cx_v, cy_v), radius=r_ball, style=fill_style(Colors.Blue3, border_color=DARK, border_units=w_tux))
draw_round_polyline([(cx_v - 1.0, cy_v + 1.2), (cx_v, cy_v - 1.2), (cx_v + 1.0, cy_v + 1.2)], width_units=0.82, color=WHITE)

# Circle M (Colors.Green3)
cx_m, cy_m = 25.0, 55.2
circle((cx_m, cy_m), radius=r_ball, style=fill_style(Colors.Green3, border_color=DARK, border_units=w_tux))
draw_round_polyline(
    [(cx_m - 1.2, cy_m - 1.1), (cx_m - 1.2, cy_m + 1.1), (cx_m, cy_m - 0.3), (cx_m + 1.2, cy_m + 1.1), (cx_m + 1.2, cy_m - 1.1)],
    width_units=0.72,
    color=WHITE,
)

save()
# fmt: on
