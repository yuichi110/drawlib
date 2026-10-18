# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon: centos."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import DARK, draw_round_polyline, no_border_fill, setup_icon

setup_icon()

w = 2.0
s = 1.01
hg = 1.05
hg_d = hg * math.sqrt(2.0)

# Base geometric midlines around (50.0, 50.0)
x_l = 50.0 - (50.0 - 21.915) * s
x_r = 50.0 - (50.0 - 47.28) * s
y_b = 50.0 + (52.72 - 50.0) * s
y_t = 50.0 + (78.085 - 50.0) * s

cx_ld = 50.0 - (50.0 - 28.22) * s
r_mid = 17.935 * s
r_in = r_mid - hg_d
r_out = r_mid + hg_d

x_head_r = x_l - hg
y_sh = (52.72 - 50.0) * s - hg
dy_head = r_in - (cx_ld - x_head_r)

# Base k=0 cardinal LEFT arrow
base_cardinal: list[tuple[float, float]] = [
    (cx_ld - r_in, 50.0),
    (x_head_r, 50.0 - dy_head),
    (x_head_r, 50.0 - y_sh),
    (cx_ld + r_in - y_sh, 50.0 - y_sh),
    (cx_ld + r_in, 50.0),
    (cx_ld + r_in - y_sh, 50.0 + y_sh),
    (x_head_r, 50.0 + y_sh),
    (x_head_r, 50.0 + dy_head),
]

# Base k=0 Top-Left square pieces (diagonal arrow + 2 flanking triangles)
x_sq_l = x_l + hg
x_sq_r = x_r - hg
y_sq_b = y_b + hg
y_sq_t = y_t - hg

base_flank_bl: list[tuple[float, float]] = [
    (x_sq_l, y_sq_b),
    (cx_ld + r_in - (y_sq_b - 50.0), y_sq_b),
    (cx_ld, 50.0 + r_in),
    (x_sq_l, 50.0 + r_in - (cx_ld - x_sq_l)),
]

base_flank_tr: list[tuple[float, float]] = [
    (100.0 - py, 100.0 - px) for px, py in reversed(base_flank_bl)
]

y_wing_l = 50.0 + r_out - (cx_ld - x_sq_l)
x_shaft_b = cx_ld + r_out - (y_sq_b - 50.0)

base_diag_arrow: list[tuple[float, float]] = [
    (x_sq_l, y_sq_t),
    (x_sq_l, y_wing_l),
    (cx_ld, 50.0 + r_out),
    (x_shaft_b, y_sq_b),
    (x_sq_r, y_sq_b),
    (x_sq_r, 100.0 - x_shaft_b),
    (50.0 - r_out, 100.0 - cx_ld),
    (100.0 - y_wing_l, y_sq_t),
]


def rot90(pts: list[tuple[float, float]], k: int) -> list[tuple[float, float]]:
    """Rotate points by k * 90 degrees CCW around (50.0, 50.0)."""
    out = list(pts)
    for _ in range(k % 4):
        out = [(round(50.0 - (y - 50.0), 2), round(50.0 + (x - 50.0), 2)) for x, y in out]
    return [(round(x, 2), round(y, 2)) for x, y in out]


YELLOW_GREEN = "#A3D65C"
PURPLE_MAGENTA = "#B565A7"
ORANGE_AMBER = "#F5B856"
INDIGO_BLUE = "#6366B5"

# Color cycle for k = 0, 1, 2, 3 (90-degree CCW steps)
# k=0: Left arrow + Top-Left square
# k=1: Bottom arrow + Bottom-Left square
# k=2: Right arrow + Bottom-Right square
# k=3: Top arrow + Top-Right square
cardinal_colors = [PURPLE_MAGENTA, YELLOW_GREEN, INDIGO_BLUE, ORANGE_AMBER]
square_colors = [YELLOW_GREEN, INDIGO_BLUE, ORANGE_AMBER, PURPLE_MAGENTA]

for k in range(4):
    sq_col = square_colors[k]
    for base_pts in (base_flank_bl, base_flank_tr, base_diag_arrow):
        pts = rot90(base_pts, k)
        polygon(pts, style=no_border_fill(sq_col))
        draw_round_polyline(pts, width_units=w, color=DARK, closed=True)

for k in range(4):
    card_col = cardinal_colors[k]
    pts = rot90(base_cardinal, k)
    polygon(pts, style=no_border_fill(card_col))
    draw_round_polyline(pts, width_units=w, color=DARK, closed=True)

save()
