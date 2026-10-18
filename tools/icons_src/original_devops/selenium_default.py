# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: selenium."""

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    WHITE,
    draw_compound_polygon,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 2.0
w_in = 1.6


def _s(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Scale official 100x100 coords by 0.94 around (50, 50)."""
    return [(50.0 + (x - 50.0) * 0.94, 50.0 + (y - 50.0) * 0.94) for x, y in pts]


# 1. Rounded square badge (Colors.Green3)
rectangle(
    (50.0, 50.0),
    width=78.0,
    height=78.0,
    style=fill_style(Colors.Green3, border_color=DARK, border_units=w, shape_r=4.5),
)

# 2. Crisp WHITE 'S' polygon
s_pts = _s(
    [
        (45.1, 48.7),
        (43.98, 49.54),
        (42.25, 50.62),
        (40.41, 51.51),
        (38.49, 52.19),
        (36.51, 52.65),
        (34.49, 52.9),
        (32.43, 52.93),
        (30.13, 52.79),
        (28.03, 52.4),
        (26.13, 51.76),
        (24.45, 50.92),
        (23.0, 49.88),
        (21.79, 48.68),
        (20.82, 47.33),
        (20.12, 45.85),
        (19.69, 44.27),
        (19.54, 42.62),
        (19.68, 40.83),
        (20.09, 39.27),
        (20.73, 37.92),
        (21.57, 36.77),
        (22.58, 35.79),
        (23.74, 34.95),
        (25.02, 34.26),
        (26.39, 33.67),
        (29.27, 32.75),
        (32.14, 32.04),
        (34.79, 31.36),
        (36.97, 30.57),
        (37.81, 30.08),
        (38.45, 29.5),
        (38.85, 28.8),
        (38.99, 27.98),
        (38.86, 27.14),
        (38.48, 26.34),
        (37.83, 25.62),
        (36.91, 25.01),
        (35.73, 24.55),
        (34.26, 24.28),
        (32.56, 24.23),
        (30.88, 24.38),
        (29.24, 24.72),
        (27.65, 25.24),
        (26.13, 25.93),
        (24.7, 26.8),
        (23.36, 27.83),
        (22.36, 28.42),
        (21.77, 28.1),
        (18.72, 23.88),
        (18.61, 23.39),
        (18.84, 22.94),
        (20.35, 21.69),
        (22.05, 20.59),
        (23.94, 19.65),
        (26.03, 18.91),
        (28.33, 18.38),
        (30.85, 18.08),
        (32.66, 18.02),
        (35.26, 18.16),
        (37.59, 18.56),
        (39.63, 19.2),
        (41.41, 20.06),
        (42.91, 21.12),
        (44.15, 22.37),
        (45.12, 23.78),
        (45.84, 25.34),
        (46.29, 27.02),
        (46.48, 28.8),
        (46.34, 30.57),
        (45.94, 32.13),
        (45.3, 33.48),
        (44.46, 34.64),
        (43.45, 35.63),
        (42.28, 36.47),
        (41.01, 37.18),
        (38.22, 38.29),
        (35.31, 39.11),
        (32.52, 39.78),
        (30.08, 40.46),
        (28.22, 41.3),
        (27.58, 41.84),
        (27.18, 42.46),
        (27.04, 43.2),
        (27.16, 44.06),
        (27.5, 44.82),
        (28.06, 45.46),
        (28.84, 45.98),
        (29.81, 46.35),
        (30.97, 46.56),
        (32.35, 46.6),
        (33.84, 46.49),
        (35.31, 46.23),
        (36.74, 45.82),
        (38.13, 45.27),
        (39.45, 44.58),
        (41.1, 43.44),
        (41.62, 43.27),
        (42.15, 43.56),
        (45.2, 47.66),
        (45.36, 48.18),
    ]
)
polygon(s_pts, style=no_border_fill(WHITE))
draw_round_polyline(s_pts, width_units=w_in, color=DARK, closed=True)

# 3. Crisp WHITE 'e' compound polygon (transparent inner eye showing Colors.Green3)
e_outer = _s(
    [
        (62.53, 44.26),
        (60.46, 44.13),
        (58.46, 43.67),
        (56.56, 42.9),
        (54.81, 41.83),
        (53.23, 40.48),
        (51.9, 38.89),
        (50.84, 37.13),
        (50.09, 35.22),
        (49.65, 33.21),
        (49.53, 31.14),
        (49.7, 28.8),
        (50.2, 26.66),
        (51.0, 24.71),
        (52.08, 22.99),
        (53.41, 21.49),
        (54.97, 20.23),
        (56.73, 19.23),
        (58.68, 18.5),
        (60.77, 18.05),
        (63.0, 17.9),
        (65.11, 17.99),
        (67.17, 18.34),
        (69.16, 18.96),
        (71.06, 19.83),
        (72.84, 20.95),
        (73.08, 21.45),
        (72.96, 21.88),
        (70.85, 25.05),
        (70.35, 25.29),
        (69.91, 25.17),
        (68.48, 24.33),
        (66.96, 23.72),
        (65.35, 23.33),
        (63.71, 23.17),
        (61.96, 23.34),
        (60.44, 23.81),
        (59.15, 24.55),
        (58.1, 25.5),
        (57.3, 26.63),
        (56.76, 27.9),
        (56.56, 28.8),
        (56.8, 29.03),
        (74.48, 29.03),
        (75.03, 29.33),
        (75.18, 29.73),
        (75.15, 31.65),
        (74.85, 33.94),
        (74.26, 36.06),
        (73.41, 37.97),
        (72.31, 39.66),
        (70.98, 41.12),
        (69.43, 42.32),
        (67.67, 43.25),
        (65.74, 43.89),
        (63.64, 44.22),
    ]
)

e_hole = _s(
    [
        (62.65, 39.11),
        (64.05, 39.02),
        (65.34, 38.62),
        (66.5, 37.95),
        (67.48, 37.04),
        (68.22, 35.92),
        (68.71, 34.65),
        (68.86, 33.72),
        (68.62, 33.48),
        (56.68, 33.48),
        (56.44, 33.72),
        (56.63, 34.63),
        (57.14, 35.88),
        (57.89, 36.98),
        (58.86, 37.88),
        (60.0, 38.55),
        (61.28, 38.97),
    ]
)

draw_compound_polygon([e_outer, e_hole], color=WHITE)
draw_round_polyline(e_outer, width_units=w_in, color=DARK, closed=True)
draw_round_polyline(e_hole, width_units=w_in, color=DARK, closed=True)

# 4. Crisp WHITE top-right checkmark
check_pts = _s(
    [
        (48.7, 64.6),
        (53.7, 70.8),
        (62.1, 62.4),
        (80.8, 87.2),
        (86.4, 78.8),
        (62.3, 50.5),
    ]
)
polygon(check_pts, style=no_border_fill(WHITE))
draw_round_polyline(check_pts, width_units=w_in, color=DARK, closed=True)

save()
