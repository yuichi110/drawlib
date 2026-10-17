# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: service_van."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
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

w_outer = 2.0
w_inner = 1.6

# 1. Roof rack struts and rail (y=62..68)
for sx in (22.0, 38.0, 54.0):
    draw_round_segment((sx, 62.0), (sx, 67.5), width_units=w_outer, color=DARK)
draw_round_segment((17.0, 67.5), (59.0, 67.5), width_units=w_outer, color=DARK)

# 2. PASTEL_GREEN satellite / field comms dish on roof (x=34..54, y=67.5..86)
draw_round_segment((41.0, 67.5), (41.0, 73.5), width_units=w_outer, color=DARK)

# Parabolic dish bowl tilted up-right at 40 degrees
dish_cx, dish_cy = 42.5, 76.5
dish_r = 8.5
dish_pts: list[tuple[float, float]] = []
steps = 16
for i in range(steps + 1):
    ang = math.radians(130.0 + 180.0 * (i / steps))
    dish_pts.append((dish_cx + dish_r * math.cos(ang), dish_cy + dish_r * math.sin(ang)))
polygon(dish_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(dish_pts, width_units=w_outer, color=DARK, closed=True)

# Feed arm & WHITE LNB horn
draw_round_segment((42.5, 76.5), (49.5, 83.5), width_units=w_inner, color=DARK)
circle(
    (50.0, 84.0),
    radius=2.2,
    style=fill_style(WHITE, border_color=DARK, border_units=w_inner),
)

# 3. Van body upper shell (WHITE, y=26..62)
van_pts = [
    (12.0, 26.0),
    (12.0, 59.0),
    (15.0, 62.0),
    (63.0, 62.0),
    (76.0, 46.0),
    (87.0, 42.0),
    (88.0, 38.0),
    (88.0, 26.0),
]
polygon(van_pts, style=no_border_fill(WHITE))

# Lower two-tone beltline (PASTEL_BLUE, y=26..41)
lower_pts = [
    (12.0, 26.0),
    (12.0, 41.0),
    (87.2, 41.0),
    (88.0, 38.0),
    (88.0, 26.0),
]
polygon(lower_pts, style=no_border_fill(PASTEL_BLUE))
draw_round_segment((12.0, 41.0), (87.2, 41.0), width_units=w_inner, color=DARK)

# Van outer contour
draw_round_polyline(van_pts, width_units=w_outer, color=DARK, closed=True)

# 4. Cab window (PASTEL_BLUE_LIGHT) & rear cargo panel with PASTEL_GREEN stripe
win_pts = [
    (60.0, 45.0),
    (60.0, 58.0),
    (62.5, 58.0),
    (72.5, 45.0),
]
polygon(win_pts, style=no_border_fill(PASTEL_BLUE_LIGHT))
draw_round_polyline(win_pts, width_units=w_inner, color=DARK, closed=True)

# Side panel inset
rectangle(
    (36.0, 51.5),
    width=34.0,
    height=13.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_inner, shape_r=2.0),
)
# Green service stripe inside side panel
rectangle(
    (36.0, 51.5),
    width=26.0,
    height=4.5,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w_inner, shape_r=1.0),
)

# Headlight & bumper
rectangle(
    (86.0, 35.0),
    width=4.0,
    height=4.5,
    style=fill_style(WHITE, border_color=DARK, border_units=w_inner, shape_r=1.0),
)

# 5. Wheels
for wx in (27.0, 73.0):
    circle(
        (wx, 24.0),
        radius=8.2,
        style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_outer),
    )
    circle(
        (wx, 24.0),
        radius=3.6,
        style=fill_style(WHITE, border_color=DARK, border_units=w_inner),
    )

save()
