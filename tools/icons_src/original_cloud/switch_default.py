# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: switch."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# 1. 3D Cisco bento-box faces (front, top, right side)
front = [(14.0, 26.0), (70.0, 26.0), (70.0, 48.0), (14.0, 48.0)]
top = [(14.0, 48.0), (30.0, 72.0), (86.0, 72.0), (70.0, 48.0)]
right = [(70.0, 26.0), (86.0, 50.0), (86.0, 72.0), (70.0, 48.0)]

polygon(top, style=no_border_fill(WHITE))
polygon(front, style=no_border_fill(PASTEL_BLUE))
polygon(right, style=no_border_fill(PASTEL_BLUE_LIGHT))

draw_round_polyline(front, width_units=w, color=DARK, closed=True)
draw_round_polyline(top, width_units=w, color=DARK, closed=True)
draw_round_polyline(right, width_units=w, color=DARK, closed=True)

# 2. Front panel status LEDs (matching router's PASTEL_GREEN LEDs)
for led_x in (30.0, 54.0):
    circle(
        (led_x, 37.0),
        radius=3.5,
        style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
    )

# 3. Cisco switch-style bidirectional switching arrows on top WHITE face
aw = 2.3

# Upper row (y=64.0): left-pointing arrow on left, right-pointing arrow on right
y_up = 64.0
draw_round_segment((33.0, y_up), (50.0, y_up), width_units=aw, color=DARK)
draw_round_polyline([(37.5, y_up + 3.2), (33.0, y_up), (37.5, y_up - 3.2)], width_units=aw, color=DARK)

draw_round_segment((58.0, y_up), (75.0, y_up), width_units=aw, color=DARK)
draw_round_polyline([(70.5, y_up + 3.2), (75.0, y_up), (70.5, y_up - 3.2)], width_units=aw, color=DARK)

# Lower row (y=55.0): right-pointing arrow on left, left-pointing arrow on right
y_dn = 55.0
draw_round_segment((27.0, y_dn), (44.0, y_dn), width_units=aw, color=DARK)
draw_round_polyline([(39.5, y_dn + 3.2), (44.0, y_dn), (39.5, y_dn - 3.2)], width_units=aw, color=DARK)

draw_round_segment((52.0, y_dn), (69.0, y_dn), width_units=aw, color=DARK)
draw_round_polyline([(56.5, y_dn + 3.2), (52.0, y_dn), (56.5, y_dn - 3.2)], width_units=aw, color=DARK)

save()
