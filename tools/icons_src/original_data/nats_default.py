# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: nats."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 1.9

x_l, x_m, x_r = 11.0, 50.0, 89.0
y_b, y_m, y_t = 26.5, 58.5, 90.5
x_tail_l = 44.2
y_tail_m = 21.4
x_tail_r = 63.5
y_tail_tip = 9.5

# 1. Four quadrant fills
# Top-left quadrant (Colors.Blue3)
polygon(
    [(x_l, y_m), (x_m, y_m), (x_m, y_t), (x_l, y_t)],
    style=no_border_fill(Colors.Blue3),
)
# Top-right quadrant (Colors.Green3)
polygon(
    [(x_m, y_m), (x_r, y_m), (x_r, y_t), (x_m, y_t)],
    style=no_border_fill(Colors.Green3),
)
# Bottom-left quadrant with left tail bevel (Colors.Teal3)
polygon(
    [(x_l, y_b), (x_tail_l, y_b), (x_m, y_tail_m), (x_m, y_m), (x_l, y_m)],
    style=no_border_fill(Colors.Teal3),
)
# Bottom-right quadrant with main speech-bubble tail (Colors.Amber3)
polygon(
    [(x_m, y_tail_m), (x_tail_r, y_tail_tip), (x_tail_r, y_b), (x_r, y_b), (x_r, y_m), (x_m, y_m)],
    style=no_border_fill(Colors.Amber3),
)

# 2. Inner cross quadrant dividers
draw_round_segment((x_l, y_m), (x_r, y_m), width_units=1.6, color=DARK)
draw_round_segment((x_m, y_tail_m), (x_m, y_t), width_units=1.6, color=DARK)

# 3. Outer speech-bubble tile border
outer_pts = [
    (x_l, y_t),
    (x_r, y_t),
    (x_r, y_b),
    (x_tail_r, y_b),
    (x_tail_r, y_tail_tip),
    (x_tail_l, y_b),
    (x_l, y_b),
]
draw_round_polyline(outer_pts, width_units=w, color=DARK, closed=True)

# 4. Bold central white 'N'
n_pts = [
    (23.5, 41.5),
    (23.5, 76.0),
    (38.0, 76.0),
    (66.0, 49.5),
    (66.0, 76.0),
    (75.5, 76.0),
    (75.5, 41.5),
    (61.2, 41.5),
    (33.0, 68.5),
    (33.0, 41.5),
]
polygon(n_pts, style=no_border_fill(WHITE))
draw_round_polyline(n_pts, width_units=1.8, color=DARK, closed=True)

save()
