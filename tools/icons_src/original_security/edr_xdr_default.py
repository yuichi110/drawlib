# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: edr_xdr."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    build_shield_half_points,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w_shape = 2.0
w_line = 2.0

# 1. Laptop screen bezel (bottom edge at y = 56 - 22 = 34.0)
rectangle(
    (47.0, 56.0),
    width=64.0,
    height=44.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w_shape, shape_r=5.0),
)

# 2. Inner WHITE screen
rectangle(
    (47.0, 56.0),
    width=54.0,
    height=34.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w_shape, shape_r=3.0),
)

# 3. Laptop keyboard base (top edge at y = 30.5 + 3.5 = 34.0, sharing bezel bottom seam)
rectangle(
    (47.0, 30.5),
    width=74.0,
    height=7.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_shape, shape_r=3.5),
)

# 4. ECG heartbeat pulse wave across screen
pulse_pts = [
    (25.0, 56.0),
    (35.0, 56.0),
    (40.0, 66.0),
    (46.0, 46.0),
    (51.0, 60.0),
    (55.0, 56.0),
    (65.0, 56.0),
]
draw_round_polyline(pulse_pts, width_units=w_line, color=DARK)

# 5. Bottom-right overlapping PASTEL_GREEN shield
sh_cx = 70.0
y_bot, y_top = 12.0, 54.0
half_w = 18.0

left_pts = build_shield_half_points(sh_cx, y_bot, y_top, half_w, side="left")
right_pts = build_shield_half_points(sh_cx, y_bot, y_top, half_w, side="right")
full_outline = left_pts + list(reversed(right_pts[1:-1]))

polygon(full_outline, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(full_outline, width_units=w_shape, color=DARK, closed=True)

# 6. Inner WHITE circle and DARK checkmark inside shield
circle(
    (sh_cx, 35.0),
    radius=8.5,
    style=fill_style(WHITE, border_color=DARK, border_units=w_shape),
)
draw_round_polyline(
    [(sh_cx - 3.8, 34.8), (sh_cx - 0.8, 31.8), (sh_cx + 4.0, 37.8)],
    width_units=w_line,
    color=DARK,
)

save()
