# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: ups_power."""

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w_outer = 2.0
w_inner = 1.6

# 1. Cabinet base plinth feet
for foot_x in (32.0, 68.0):
    rectangle(
        (foot_x, 14.5),
        width=10.0,
        height=4.0,
        style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_outer, shape_r=1.5),
    )

# 2. Main UPS power cabinet enclosure (PASTEL_BLUE)
rectangle(
    (50.0, 51.0),
    width=56.0,
    height=70.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w_outer, shape_r=5.5),
)

# 3. Upper WHITE display / inverter compartment
rectangle(
    (50.0, 64.5),
    width=42.0,
    height=33.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w_inner, shape_r=3.5),
)

# 4. Central PASTEL_GREEN lightning bolt inside upper WHITE panel
bolt_pts = [
    (53.5, 77.5),
    (42.0, 64.0),
    (49.5, 64.0),
    (46.5, 51.5),
    (58.0, 65.0),
    (50.5, 65.0),
]
polygon(bolt_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(bolt_pts, width_units=w_inner, color=DARK, closed=True)

# 5. Three stacked PASTEL_GREEN battery charge bars in lower compartment
for bar_cy in (39.5, 31.5, 23.5):
    rectangle(
        (50.0, bar_cy),
        width=40.0,
        height=5.2,
        style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w_inner, shape_r=2.0),
    )

save()
